"""
主窗口
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QSplitter, QMenuBar, QStatusBar,
                             QMessageBox, QApplication)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction, QIcon

import config
from gui.video_player import VideoPlayer
from gui.subtitle_panel import SubtitlePanel
from gui.control_panel import ControlPanel
from gui.upload_dialog import UploadDialog
from models.subtitle import SubtitleList
from models.video_info import VideoInfo


class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self):
        super().__init__()

        self.video_info: VideoInfo = None
        self.subtitle_list: SubtitleList = None
        self.repeat_mode = False
        self.repeat_count = 0
        self.repeat_current = 0
        self.repeat_segment = None

        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        """设置UI"""
        self.setWindowTitle("视频双语字幕生成与交互式复读系统")
        self.setMinimumSize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)

        # 创建中央widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)

        # 创建分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # 左侧：播放器
        self.video_player = VideoPlayer()
        splitter.addWidget(self.video_player)

        # 右侧：字幕和控制面板
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)

        # 字幕面板
        self.subtitle_panel = SubtitlePanel()
        right_layout.addWidget(self.subtitle_panel, stretch=1)

        # 控制面板
        self.control_panel = ControlPanel()
        right_layout.addWidget(self.control_panel)

        splitter.addWidget(right_panel)

        # 设置分割器比例
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 1)

        main_layout.addWidget(splitter)

        # 创建菜单栏
        self._create_menu_bar()

        # 创建工具栏
        self._create_tool_bar()

        # 创建状态栏
        self._create_status_bar()

        # 创建定时器（用于字幕同步）
        self.sync_timer = QTimer()
        self.sync_timer.setInterval(100)  # 每100毫秒检查一次
        self.sync_timer.timeout.connect(self._on_sync_timer)

    def _create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()

        # 文件菜单
        file_menu = menubar.addMenu("文件(&F)")

        # 打开视频
        open_action = QAction("打开视频(&O)...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self._on_open_video)
        file_menu.addAction(open_action)

        file_menu.addSeparator()

        # 退出
        exit_action = QAction("退出(&X)", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 帮助菜单
        help_menu = menubar.addMenu("帮助(&H)")

        # 关于
        about_action = QAction("关于(&A)", self)
        about_action.triggered.connect(self._on_about)
        help_menu.addAction(about_action)

    def _create_tool_bar(self):
        """创建工具栏"""
        # 暂时不显示工具栏，因为所有功能都已在菜单栏中
        pass

    def _create_status_bar(self):
        """创建状态栏"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")

    def _connect_signals(self):
        """连接信号"""
        # 播放器位置变化 -> 更新高亮字幕
        self.video_player.position_changed.connect(self._on_position_changed)

        # 字幕点击 -> 跳转播放器
        self.subtitle_panel.clicked.connect(self._on_subtitle_clicked)

        # 复读按钮点击 -> 开始复读
        self.control_panel.repeat_clicked.connect(self._on_repeat_clicked)

    # 事件处理

    def _on_open_video(self):
        """打开视频"""
        dialog = UploadDialog(self)
        dialog.video_loaded.connect(self._on_video_loaded)
        dialog.exec()

    def _on_video_loaded(self, video_info: VideoInfo, subtitle_list: SubtitleList):
        """
        视频加载完成

        Args:
            video_info: 视频信息
            subtitle_list: 字幕列表
        """
        self.video_info = video_info
        self.subtitle_list = subtitle_list

        # 加载视频到播放器
        self.video_player.load_video(video_info.path)

        # 设置字幕面板
        self.subtitle_panel.set_subtitle_list(subtitle_list)

        # 更新状态栏
        self.status_bar.showMessage(f"已加载: {video_info.name}")

        # 启动同步定时器
        self.sync_timer.start()

    def _on_position_changed(self, position: float):
        """
        播放位置变化

        Args:
            position: 当前位置（秒）
        """
        if not self.subtitle_list:
            return

        # 如果在复读模式中，检查是否需要循环
        if self.repeat_mode and self.repeat_segment:
            # 添加缓冲时间，确保完整听完最后一个单词
            if position >= self.repeat_segment.end + config.REPEAT_BUFFER_TIME:
                self.repeat_current += 1

                if self.repeat_current >= self.repeat_count:
                    # 复读完成，暂停视频
                    self.repeat_mode = False
                    self.video_player.pause()
                    self.control_panel.repeat_completed()
                    self.status_bar.showMessage(f"复读完成 (共{self.repeat_count}次)")
                else:
                    # 继续复读
                    self.control_panel.update_repeat_progress(
                        self.repeat_current + 1,
                        self.repeat_count
                    )
                    # 跳转到字幕开始位置
                    self.video_player.seek(self.repeat_segment.start)
                    # 确保继续播放
                    if not self.video_player.is_playing():
                        self.video_player.play()

        # 更新高亮字幕
        self.subtitle_panel.highlight_subtitle(position)

    def _on_subtitle_clicked(self, subtitle_id: int):
        """
        字幕点击事件

        Args:
            subtitle_id: 字幕序号
        """
        segment = self.subtitle_panel.get_segment_by_id(subtitle_id)

        if segment:
            # 跳转到字幕开始时间
            self.video_player.seek(segment.start)

            # 滚动字幕面板到指定位置
            self.subtitle_panel.scroll_to_subtitle(subtitle_id)

            # 更新控制面板
            self.control_panel.set_current_subtitle(subtitle_id, segment.text_en)

    def _on_repeat_clicked(self, count: int):
        """
        复读按钮点击

        Args:
            count: 复读次数（-1表示停止复读）
        """
        if count == -1:
            # 停止复读
            self._stop_repeat()
        else:
            # 开始复读
            self._start_repeat(count)

    def _start_repeat(self, count: int):
        """
        开始复读

        Args:
            count: 复读次数
        """
        if not self.subtitle_list:
            return

        # 获取当前时间点的字幕
        current_time = self.video_player.get_position()
        segment = self.subtitle_list.get_segment_at_time(current_time)

        if not segment:
            self.status_bar.showMessage("当前没有字幕可供复读")
            return

        # 设置复读模式
        self.repeat_mode = True
        self.repeat_count = count
        self.repeat_current = 0
        self.repeat_segment = segment

        # 跳转到字幕开始位置并播放
        self.video_player.seek(segment.start)
        self.video_player.play()

        # 更新控制面板
        self.control_panel.update_repeat_progress(1, count)

        self.status_bar.showMessage(f"开始复读: {count}次")

    def _stop_repeat(self):
        """停止复读"""
        self.repeat_mode = False
        self.repeat_count = 0
        self.repeat_current = 0
        self.repeat_segment = None

        self.control_panel.reset_repeat_button()
        self.status_bar.showMessage("复读已停止")

    def _on_sync_timer(self):
        """同步定时器"""
        pass

    def _on_about(self):
        """关于对话框"""
        QMessageBox.about(
            self,
            "关于",
            "<h3>视频双语字幕生成与交互式复读系统</h3>"
            "<p>一个智能的双语字幕系统，能够自动翻译视频内容，并提供交互式复读功能。</p>"
            "<p><b>功能特性:</b></p>"
            "<ul>"
            "<li>自动语音识别（基于OpenAI Whisper）</li>"
            "<li>中英双语字幕生成（基于Google Translate）</li>"
            "<li>交互式视频播放器</li>"
            "<li>点击字幕跳转到对应时间点</li>"
            "<li>自定义复读次数（0/3/10/20次）</li>"
            "</ul>"
        )

    def closeEvent(self, event):
        """关闭事件"""
        # 停止定时器
        self.sync_timer.stop()

        # 停止播放
        self.video_player.stop()

        event.accept()

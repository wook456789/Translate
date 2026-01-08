"""
上传对话框 - 视频上传和处理进度
"""

import os
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QProgressBar,
                             QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap

import config
from core.video_processor import VideoProcessor
from core.speech_recognizer import SpeechRecognizer
from core.translator import GoogleTranslator
from core.subtitle_generator import SubtitleGenerator
from models.subtitle import SubtitleList
from models.video_info import VideoInfo
from utils.file_utils import is_video_file, format_file_size
from utils.time_utils import format_duration


class ProcessVideoThread(QThread):
    """视频处理线程"""

    # 信号
    progress_updated = pyqtSignal(float, str)  # 进度更新 (progress, message)
    processing_completed = pyqtSignal(VideoInfo, SubtitleList)  # 处理完成
    error_occurred = pyqtSignal(str)  # 发生错误

    def __init__(self, video_path: str):
        super().__init__()

        self.video_path = video_path
        self.video_processor = VideoProcessor()
        self.speech_recognizer = SpeechRecognizer()
        self.translator = GoogleTranslator()
        self.subtitle_generator = SubtitleGenerator()

    def run(self):
        """运行处理流程"""
        try:
            # 步骤1: 获取视频信息
            self.progress_updated.emit(0.1, "正在分析视频...")
            video_info = self.video_processor.get_video_info(self.video_path)
            video_info.audio_path = self.video_processor.extract_audio(self.video_path)

            # 步骤2: 语音识别
            self.progress_updated.emit(0.2, "正在进行语音识别...")
            subtitle_list = self.speech_recognizer.transcribe(
                video_info.audio_path,
                language="en"
            )

            # 步骤3: 翻译
            self.progress_updated.emit(0.7, "正在翻译字幕...")
            subtitle_list = self.translator.translate_subtitle_list(subtitle_list)

            # 步骤4: 保存字幕
            self.progress_updated.emit(0.95, "正在保存字幕...")

            # 保存到缓存目录
            cache_path = self.subtitle_generator.save_to_cache(
                subtitle_list,
                self.video_path,
                format="json"
            )
            video_info.subtitle_path = cache_path

            # 同时保存到视频同目录，方便用户下次使用
            from pathlib import Path
            video_dir = Path(self.video_path).parent
            video_name = Path(self.video_path).stem
            user_subtitle_path = video_dir / f"{video_name}_bilingual.json"

            # 保存JSON格式
            self.subtitle_generator.save_json(subtitle_list, str(user_subtitle_path))

            # 同时保存SRT格式，方便通用播放器使用
            srt_path = video_dir / f"{video_name}_bilingual.srt"
            self.subtitle_generator.save_srt(subtitle_list, str(srt_path))

            # 完成
            self.progress_updated.emit(1.0, "处理完成！")
            self.processing_completed.emit(video_info, subtitle_list)

        except Exception as e:
            self.error_occurred.emit(f"处理失败: {str(e)}")


class UploadDialog(QDialog):
    """上传对话框"""

    # 信号
    video_loaded = pyqtSignal(VideoInfo, SubtitleList)  # 视频加载完成

    def __init__(self, parent=None):
        super().__init__(parent)

        self.video_path = None
        self.process_thread = None

        self._setup_ui()

    def _setup_ui(self):
        """设置UI"""
        self.setWindowTitle("上传视频")
        self.setModal(True)
        self.setMinimumWidth(600)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # 标题
        title_label = QLabel("选择要处理的英文视频文件")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title_label)

        # 说明
        info_label = QLabel("支持格式: " + ", ".join(config.SUPPORTED_VIDEO_FORMATS).upper())
        info_label.setStyleSheet("color: #666;")
        layout.addWidget(info_label)

        # 选择文件按钮
        self.select_button = QPushButton("选择视频文件")
        self.select_button.setStyleSheet("""
            QPushButton {
                background-color: #2196f3;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1976d2;
            }
        """)
        self.select_button.clicked.connect(self._on_select_file)
        layout.addWidget(self.select_button)

        # 视频信息显示
        self.video_info_label = QLabel("")
        self.video_info_label.setStyleSheet("color: #333; padding: 10px; background-color: #f5f5f5; border-radius: 5px;")
        self.video_info_label.setVisible(False)
        layout.addWidget(self.video_info_label)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # 状态标签
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #666;")
        self.status_label.setVisible(False)
        layout.addWidget(self.status_label)

        # 按钮栏
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        self.ok_button = QPushButton("确定")
        self.ok_button.setEnabled(False)
        self.ok_button.clicked.connect(self.accept)
        button_layout.addWidget(self.ok_button)

        layout.addLayout(button_layout)

    def _on_select_file(self):
        """选择文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择视频文件",
            "",
            f"视频文件 ({' '.join(config.SUPPORTED_VIDEO_FORMATS)});;所有文件 (*.*)"
        )

        if file_path:
            self.video_path = file_path

            # 检查是否已存在字幕文件
            from pathlib import Path
            video_dir = Path(file_path).parent
            video_name = Path(file_path).stem
            existing_subtitle = video_dir / f"{video_name}_bilingual.json"

            if existing_subtitle.exists():
                # 直接加载现有字幕，不再询问
                self._load_existing_subtitle(file_path, existing_subtitle)
                return

            # 没有现有字幕，开始处理
            self._start_processing()

    def _load_existing_subtitle(self, video_path: str, subtitle_path: str):
        """加载已存在的字幕"""
        try:
            from core.video_processor import VideoProcessor
            from core.subtitle_generator import SubtitleGenerator

            # 获取视频信息
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(50)
            self.status_label.setVisible(True)
            self.status_label.setText("✓ 发现已存在的字幕文件，正在加载...")
            self.select_button.setEnabled(False)

            video_processor = VideoProcessor()
            video_info = video_processor.get_video_info(video_path)

            # 加载字幕
            self.status_label.setText("正在加载字幕...")
            self.progress_bar.setValue(80)

            subtitle_generator = SubtitleGenerator()
            subtitle_list = subtitle_generator.load_json(str(subtitle_path))

            self.progress_bar.setValue(100)
            self.status_label.setText("✓ 加载完成！（使用已有字幕，无需重新翻译）")

            # 显示视频信息
            info_text = f"""<b>文件名:</b> {video_info.name}
<b>时长:</b> {format_duration(video_info.duration)}
<b>分辨率:</b> {video_info.resolution}
<b>文件大小:</b> {format_file_size(video_info.size)}
<b>字幕数量:</b> {len(subtitle_list)} 条
<b>字幕来源:</b> <span style="color: green;">已存在的文件（秒级加载）</span>"""
            self.video_info_label.setText(info_text)
            self.video_info_label.setVisible(True)

            # 启用确定按钮
            self.ok_button.setEnabled(True)

            # 保存结果
            self.video_info = video_info
            self.subtitle_list = subtitle_list

        except Exception as e:
            QMessageBox.critical(
                self,
                "加载失败",
                f"加载现有字幕失败：{str(e)}\n\n将重新生成字幕..."
            )
            # 重置状态并重新处理
            self.progress_bar.setVisible(False)
            self.status_label.setVisible(False)
            self.select_button.setEnabled(True)
            self._start_processing()

    def _start_processing(self):
        """开始处理"""
        if not self.video_path:
            return

        # 显示进度
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setVisible(True)
        self.status_label.setText("正在处理...")
        self.select_button.setEnabled(False)

        # 启动处理线程
        self.process_thread = ProcessVideoThread(self.video_path)
        self.process_thread.progress_updated.connect(self._on_progress_updated)
        self.process_thread.processing_completed.connect(self._on_processing_completed)
        self.process_thread.error_occurred.connect(self._on_error_occurred)
        self.process_thread.start()

    def _on_progress_updated(self, progress: float, message: str):
        """
        进度更新

        Args:
            progress: 进度值 (0-1)
            message: 状态消息
        """
        self.progress_bar.setValue(int(progress * 100))
        self.status_label.setText(message)

    def _on_processing_completed(self, video_info: VideoInfo, subtitle_list: SubtitleList):
        """
        处理完成

        Args:
            video_info: 视频信息
            subtitle_list: 字幕列表
        """
        # 显示视频信息
        info_text = f"""<b>文件名:</b> {video_info.name}
<b>时长:</b> {format_duration(video_info.duration)}
<b>分辨率:</b> {video_info.resolution}
<b>文件大小:</b> {format_file_size(video_info.size)}
<b>字幕数量:</b> {len(subtitle_list)} 条"""
        self.video_info_label.setText(info_text)
        self.video_info_label.setVisible(True)

        # 更新状态
        self.status_label.setText("处理完成！")
        self.progress_bar.setValue(100)

        # 启用确定按钮
        self.ok_button.setEnabled(True)

        # 保存结果供后续使用
        self.video_info = video_info
        self.subtitle_list = subtitle_list

    def _on_error_occurred(self, error_message: str):
        """
        发生错误

        Args:
            error_message: 错误消息
        """
        QMessageBox.critical(self, "错误", error_message)

        # 重置状态
        self.progress_bar.setVisible(False)
        self.status_label.setVisible(False)
        self.select_button.setEnabled(True)

    def accept(self):
        """确定按钮点击"""
        if hasattr(self, 'video_info') and hasattr(self, 'subtitle_list'):
            self.video_loaded.emit(self.video_info, self.subtitle_list)
        super().accept()

    def get_result(self):
        """获取处理结果"""
        if hasattr(self, 'video_info') and hasattr(self, 'subtitle_list'):
            return self.video_info, self.subtitle_list
        return None, None

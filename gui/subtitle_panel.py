"""
字幕面板组件
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QScrollArea,
                             QLabel, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QCursor

from models.subtitle import SubtitleList, SubtitleSegment
from utils.time_utils import milliseconds_to_time_string


class SubtitleLabel(QFrame):
    """单个字幕标签"""

    clicked = pyqtSignal(int)  # 点击信号，传递字幕序号

    def __init__(self, segment: SubtitleSegment, parent=None):
        super().__init__(parent)

        self.segment = segment
        self._is_active = False

        self._setup_ui()

    def _setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(4)

        # 时间标签
        time_label = QLabel(self._get_time_text())
        time_label.setStyleSheet("color: #666; font-size: 11px;")
        layout.addWidget(time_label)

        # 英文原文
        en_label = QLabel(self.segment.text_en)
        en_label.setWordWrap(True)
        en_label.setStyleSheet("color: #333; font-size: 13px; font-weight: bold;")
        layout.addWidget(en_label)

        # 中文翻译
        if self.segment.text_zh:
            zh_label = QLabel(self.segment.text_zh)
            zh_label.setWordWrap(True)
            zh_label.setStyleSheet("color: #666; font-size: 12px;")
            layout.addWidget(zh_label)

        # 设置基本样式
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._update_style()

    def _get_time_text(self) -> str:
        """获取时间文本"""
        start_ms = int(self.segment.start * 1000)
        end_ms = int(self.segment.end * 1000)
        return f"{milliseconds_to_time_string(start_ms)} - {milliseconds_to_time_string(end_ms)}"

    def set_active(self, active: bool):
        """
        设置活动状态

        Args:
            active: 是否为活动状态
        """
        self._is_active = active
        self._update_style()

    def _update_style(self):
        """更新样式"""
        if self._is_active:
            self.setStyleSheet("""
                SubtitleLabel {
                    background-color: #e3f2fd;
                    border-radius: 5px;
                    border: 2px solid #2196f3;
                }
            """)
        else:
            self.setStyleSheet("""
                SubtitleLabel {
                    background-color: #f5f5f5;
                    border-radius: 5px;
                    border: 1px solid #ddd;
                }
                SubtitleLabel:hover {
                    background-color: #e8e8e8;
                    border: 1px solid #bbb;
                }
            """)

    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.segment.id)
        super().mousePressEvent(event)


class SubtitlePanel(QWidget):
    """字幕面板"""

    clicked = pyqtSignal(int)  # 点击字幕信号

    def __init__(self, parent=None):
        super().__init__(parent)

        self.subtitle_list: SubtitleList = None
        self.subtitle_widgets: list[SubtitleLabel] = []
        self.current_highlight_id = None  # 当前高亮的字幕ID
        self.scroll_enabled = True  # 是否允许自动滚动
        self.user_scrolling = False  # 用户是否正在滚动
        self.last_scroll_time = 0  # 上次滚动时间
        self.scroll_threshold = 100  # 滚动间隔阈值（毫秒）

        self._setup_ui()

    def _setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # 标题
        title_label = QLabel("双语字幕")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px; background-color: #f0f0f0;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # 滚动区域
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        # 连接滚动条信号
        self.scroll_area.verticalScrollBar().valueChanged.connect(self._on_scroll_changed)

        # 容器widget
        self.container_widget = QWidget()
        self.container_layout = QVBoxLayout(self.container_widget)
        self.container_layout.setSpacing(8)
        self.container_layout.setContentsMargins(10, 10, 10, 10)
        self.container_layout.addStretch()

        self.scroll_area.setWidget(self.container_widget)
        layout.addWidget(self.scroll_area)

    def set_subtitle_list(self, subtitle_list: SubtitleList):
        """
        设置字幕列表

        Args:
            subtitle_list: 字幕列表对象
        """
        # 清除现有字幕
        self._clear_subtitles()

        self.subtitle_list = subtitle_list

        # 创建字幕widget
        for segment in subtitle_list.segments:
            subtitle_widget = SubtitleLabel(segment)
            subtitle_widget.clicked.connect(self._on_subtitle_clicked)
            self.subtitle_widgets.append(subtitle_widget)
            self.container_layout.insertWidget(
                self.container_layout.count() - 1,
                subtitle_widget
            )

    def _clear_subtitles(self):
        """清除所有字幕"""
        for widget in self.subtitle_widgets:
            widget.deleteLater()
        self.subtitle_widgets.clear()

    def highlight_subtitle(self, time: float):
        """
        高亮指定时间点的字幕

        Args:
            time: 时间点（秒）
        """
        if not self.subtitle_list:
            return

        # 找到对应的字幕片段
        segment = self.subtitle_list.get_segment_at_time(time)

        # 如果字幕没有变化，不重复处理
        if segment and segment.id == self.current_highlight_id:
            return

        self.current_highlight_id = segment.id if segment else None

        # 清除所有高亮
        for widget in self.subtitle_widgets:
            widget.set_active(False)

        # 高亮当前字幕
        if segment:
            for widget in self.subtitle_widgets:
                if widget.segment.id == segment.id:
                    widget.set_active(True)
                    # 只在允许滚动时才滚动
                    if self.scroll_enabled and not self.user_scrolling:
                        self._scroll_to_widget(widget)
                    break

    def _scroll_to_widget(self, widget: SubtitleLabel):
        """
        滚动到指定widget（智能滚动，将目标字幕放在视野中央）

        Args:
            widget: 目标widget
        """
        # 检查滚动频率，避免过于频繁
        import time
        current_time = time.time() * 1000  # 转换为毫秒
        if current_time - self.last_scroll_time < self.scroll_threshold:
            return

        self.last_scroll_time = current_time

        # 确保widget已显示
        widget.setVisible(True)

        # 计算滚动位置（将字幕放在视野中央）
        scroll_bar = self.scroll_area.verticalScrollBar()
        widget_geometry = widget.geometry()
        widget_top = widget_geometry.top()
        widget_height = widget_geometry.height()

        # 视口高度
        viewport_height = self.scroll_area.viewport().height()

        # 目标位置：让字幕显示在视口中央
        target_position = widget_top - (viewport_height // 2) + (widget_height // 2)

        # 确保滚动位置在有效范围内
        max_value = scroll_bar.maximum()
        min_value = scroll_bar.minimum()
        target_position = max(min_value, min(target_position, max_value))

        # 平滑滚动到目标位置
        scroll_bar.setValue(int(target_position))

    def _on_subtitle_clicked(self, subtitle_id: int):
        """
        字幕点击事件

        Args:
            subtitle_id: 字幕序号
        """
        self.clicked.emit(subtitle_id)

    def _on_scroll_changed(self, value: int):
        """
        滚动条值改变事件

        Args:
            value: 滚动条值
        """
        # 用户正在滚动时，暂停自动滚动
        self.user_scrolling = True

        # 使用定时器恢复自动滚动
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(500, self._enable_auto_scroll)

    def _enable_auto_scroll(self):
        """恢复自动滚动"""
        self.user_scrolling = False

    def scroll_to_subtitle(self, subtitle_id: int):
        """
        滚动到指定字幕（用于点击字幕时的跳转）

        Args:
            subtitle_id: 字幕序号
        """
        # 暂时禁用自动滚动标志
        self.scroll_enabled = False

        for widget in self.subtitle_widgets:
            if widget.segment.id == subtitle_id:
                self._scroll_to_widget(widget)
                break

        # 500ms后恢复自动滚动
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(500, lambda: setattr(self, 'scroll_enabled', True))

    def get_segment_by_id(self, subtitle_id: int) -> SubtitleSegment:
        """
        根据序号获取字幕片段

        Args:
            subtitle_id: 字幕序号

        Returns:
            字幕片段对象
        """
        if not self.subtitle_list:
            return None

        for segment in self.subtitle_list.segments:
            if segment.id == subtitle_id:
                return segment

        return None

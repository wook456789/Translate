"""
控制面板组件 - 复读控制
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QComboBox, QPushButton, QButtonGroup,
                             QRadioButton, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal

import config


class ControlPanel(QWidget):
    """控制面板"""

    # 信号
    repeat_clicked = pyqtSignal(int)  # 复读按钮点击，传递次数

    def __init__(self, parent=None):
        super().__init__(parent)

        self.selected_repeat_count = 0
        self.current_segment_id = None
        self.repeat_progress = 0

        self._setup_ui()

    def _setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        # 标题
        title_label = QLabel("复读控制")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; padding: 5px;")
        layout.addWidget(title_label)

        # 分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator)

        # 当前字幕信息
        self.current_subtitle_label = QLabel("当前字幕: 未选择")
        self.current_subtitle_label.setStyleSheet("color: #666; padding: 5px;")
        layout.addWidget(self.current_subtitle_label)

        # 复读次数选择
        repeat_label = QLabel("复读次数:")
        repeat_label.setStyleSheet("font-weight: bold; padding: 5px;")
        layout.addWidget(repeat_label)

        # 复读次数按钮组
        self.repeat_button_group = QButtonGroup(self)
        repeat_layout = QHBoxLayout()

        for count in config.REPEAT_COUNTS:
            if count == 0:
                label = "正常"
            else:
                label = str(count)

            radio_button = QRadioButton(label)
            self.repeat_button_group.addButton(radio_button, count)
            repeat_layout.addWidget(radio_button)

            # 默认选择0（正常播放）
            if count == 0:
                radio_button.setChecked(True)

        layout.addLayout(repeat_layout)

        # 连接按钮组信号
        self.repeat_button_group.buttonClicked.connect(self._on_repeat_count_changed)

        # 复读按钮
        self.repeat_button = QPushButton("开始复读")
        self.repeat_button.setEnabled(False)
        self.repeat_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        self.repeat_button.clicked.connect(self._on_repeat_button_clicked)
        layout.addWidget(self.repeat_button)

        # 复读进度显示
        self.progress_label = QLabel("")
        self.progress_label.setStyleSheet("color: #2196f3; font-weight: bold; padding: 5px;")
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.progress_label)

        # 弹簧
        layout.addStretch()

    def set_current_subtitle(self, subtitle_id: int, text: str = ""):
        """
        设置当前字幕

        Args:
            subtitle_id: 字幕序号
            text: 字幕文本（可选）
        """
        self.current_segment_id = subtitle_id

        # 更新显示
        if text:
            # 截断过长的文本
            display_text = text if len(text) <= 50 else text[:47] + "..."
            self.current_subtitle_label.setText(f"当前字幕 #{subtitle_id}: {display_text}")
        else:
            self.current_subtitle_label.setText(f"当前字幕: #{subtitle_id}")

        # 启用复读按钮
        self.repeat_button.setEnabled(True)
        self.repeat_button.setText("开始复读")

        # 重置进度显示
        self.progress_label.setText("")

        # 如果当前选择的是"正常"（0次），自动切换到3次
        if self.repeat_button_group.checkedId() == 0:
            # 找到3次的按钮并选中
            for button in self.repeat_button_group.buttons():
                if self.repeat_button_group.id(button) == 3:
                    button.setChecked(True)
                    break

    def clear_current_subtitle(self):
        """清除当前字幕"""
        self.current_segment_id = None
        self.current_subtitle_label.setText("当前字幕: 未选择")
        self.repeat_button.setEnabled(False)
        self.progress_label.setText("")

    def update_repeat_progress(self, current: int, total: int):
        """
        更新复读进度

        Args:
            current: 当前次数
            total: 总次数
        """
        self.repeat_progress = current
        self.progress_label.setText(f"复读进度: {current}/{total}")

    def repeat_completed(self):
        """复读完成"""
        self.progress_label.setText(f"复读完成 (共{self.selected_repeat_count}次)")
        self.repeat_button.setText("开始复读")

    def _on_repeat_count_changed(self, button):
        """
        复读次数改变

        Args:
            button: 被点击的按钮
        """
        self.selected_repeat_count = self.repeat_button_group.checkedId()

    def _on_repeat_button_clicked(self):
        """复读按钮点击"""
        if self.current_segment_id is None:
            return

        # 获取选中的复读次数
        selected_count = self.repeat_button_group.checkedId()

        # 如果选择的是"正常"（0次），提示用户选择次数
        if selected_count == 0:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                "请选择复读次数",
                "请先选择复读次数（3/10/20次），然后点击开始复读"
            )
            return

        # 切换复读状态
        if self.repeat_button.text() == "开始复读":
            self.repeat_button.setText("停止复读")
            self.repeat_clicked.emit(selected_count)
        else:
            self.repeat_button.setText("开始复读")
            self.repeat_clicked.emit(-1)  # -1表示停止复读

    def reset_repeat_button(self):
        """重置复读按钮"""
        self.repeat_button.setText("开始复读")
        self.progress_label.setText("")

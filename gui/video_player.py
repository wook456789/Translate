"""
视频播放器组件
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QSlider, QPushButton, QLabel, QFileDialog)
from PyQt6.QtCore import Qt, QUrl, QTimer, pyqtSignal
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget

from utils.time_utils import seconds_to_time_string


class VideoPlayer(QWidget):
    """视频播放器组件"""

    # 信号
    position_changed = pyqtSignal(float)  # 当前播放位置变化
    duration_changed = pyqtSignal(float)  # 视频时长变化
    playback_state_changed = pyqtSignal(bool)  # 播放状态变化

    def __init__(self, parent=None):
        super().__init__(parent)

        self.media_player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.video_widget = QVideoWidget(self)

        # 设置视频输出和音频输出
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(0.5)

        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # 视频显示区域
        layout.addWidget(self.video_widget, stretch=1)

        # 控制栏
        control_layout = QHBoxLayout()

        # 播放/暂停按钮
        self.play_button = QPushButton("播放")
        self.play_button.clicked.connect(self.toggle_playback)
        control_layout.addWidget(self.play_button)

        # 进度条
        self.position_slider = QSlider(Qt.Orientation.Horizontal)
        self.position_slider.setRange(0, 0)
        self.position_slider.sliderPressed.connect(self._on_slider_pressed)
        self.position_slider.sliderReleased.connect(self._on_slider_released)
        control_layout.addWidget(self.position_slider, stretch=1)

        # 时间显示
        self.time_label = QLabel("00:00:00 / 00:00:00")
        control_layout.addWidget(self.time_label)

        # 音量控制
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.setMaximumWidth(100)
        self.volume_slider.valueChanged.connect(self._on_volume_changed)
        control_layout.addWidget(self.volume_slider)

        layout.addLayout(control_layout)

        self._slider_pressed = False

    def _connect_signals(self):
        """连接信号"""
        self.media_player.positionChanged.connect(self._on_position_changed)
        self.media_player.durationChanged.connect(self._on_duration_changed)
        self.media_player.playbackStateChanged.connect(self._on_state_changed)

    def load_video(self, video_path: str):
        """
        加载视频文件

        Args:
            video_path: 视频文件路径
        """
        video_url = QUrl.fromLocalFile(video_path)
        self.media_player.setSource(video_url)

    def play(self):
        """播放视频"""
        self.media_player.play()

    def pause(self):
        """暂停视频"""
        self.media_player.pause()

    def stop(self):
        """停止视频"""
        self.media_player.stop()

    def toggle_playback(self):
        """切换播放/暂停"""
        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.pause()
        else:
            self.play()

    def seek(self, position: float):
        """
        跳转到指定位置

        Args:
            position: 目标位置（秒）
        """
        self.media_player.setPosition(int(position * 1000))

    def set_volume(self, volume: float):
        """
        设置音量

        Args:
            volume: 音量值 (0.0 - 1.0)
        """
        self.audio_output.setVolume(volume)

    def get_position(self) -> float:
        """
        获取当前播放位置

        Returns:
            当前位置（秒）
        """
        return self.media_player.position() / 1000.0

    def get_duration(self) -> float:
        """
        获取视频时长

        Returns:
            时长（秒）
        """
        return self.media_player.duration() / 1000.0

    def is_playing(self) -> bool:
        """
        是否正在播放

        Returns:
            如果正在播放返回True
        """
        return self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState

    # 事件处理

    def _on_position_changed(self, position: int):
        """播放位置变化"""
        position_seconds = position / 1000.0

        # 更新进度条（如果用户没有在拖动）
        if not self._slider_pressed:
            self.position_slider.setValue(int(position))

        # 更新时间显示
        duration = self.get_duration()
        current_time = seconds_to_time_string(position_seconds)
        total_time = seconds_to_time_string(duration)
        self.time_label.setText(f"{current_time} / {total_time}")

        # 发射信号
        self.position_changed.emit(position_seconds)

    def _on_duration_changed(self, duration: int):
        """视频时长变化"""
        duration_seconds = duration / 1000.0
        self.position_slider.setRange(0, int(duration))
        self.duration_changed.emit(duration_seconds)

    def _on_state_changed(self, state):
        """播放状态变化"""
        if state == QMediaPlayer.PlaybackState.PlayingState:
            self.play_button.setText("暂停")
            self.playback_state_changed.emit(True)
        else:
            self.play_button.setText("播放")
            self.playback_state_changed.emit(False)

    def _on_slider_pressed(self):
        """进度条按下"""
        self._slider_pressed = True

    def _on_slider_released(self):
        """进度条释放"""
        self._slider_pressed = False
        position = self.position_slider.value()
        self.media_player.setPosition(position)

    def _on_volume_changed(self, value: int):
        """音量变化"""
        volume = value / 100.0
        self.audio_output.setVolume(volume)

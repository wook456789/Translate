"""
视频信息数据模型
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class VideoInfo:
    """视频信息"""
    path: str  # 视频文件路径
    name: str  # 文件名
    duration: float  # 时长（秒）
    width: int  # 视频宽度
    height: int  # 视频高度
    fps: float  # 帧率
    size: int  # 文件大小（字节）
    audio_path: Optional[str] = None  # 提取的音频文件路径
    subtitle_path: Optional[str] = None  # 字幕文件路径

    @property
    def resolution(self) -> str:
        """获取分辨率字符串"""
        return f"{self.width}x{self.height}"

    @property
    def aspect_ratio(self) -> float:
        """获取宽高比"""
        return self.width / self.height if self.height > 0 else 0

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "path": self.path,
            "name": self.name,
            "duration": self.duration,
            "width": self.width,
            "height": self.height,
            "fps": self.fps,
            "size": self.size,
            "audio_path": self.audio_path,
            "subtitle_path": self.subtitle_path,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "VideoInfo":
        """从字典创建实例"""
        return cls(
            path=data["path"],
            name=data["name"],
            duration=data["duration"],
            width=data["width"],
            height=data["height"],
            fps=data["fps"],
            size=data["size"],
            audio_path=data.get("audio_path"),
            subtitle_path=data.get("subtitle_path"),
        )

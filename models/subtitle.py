"""
字幕数据模型
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class SubtitleSegment:
    """字幕片段"""
    id: int  # 序号
    start: float  # 开始时间（秒）
    end: float  # 结束时间（秒）
    text_en: str  # 英文原文
    text_zh: str = ""  # 中文翻译
    translating: bool = False  # 是否正在翻译

    @property
    def duration(self) -> float:
        """获取时长"""
        return self.end - self.start

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "id": self.id,
            "start": self.start,
            "end": self.end,
            "text_en": self.text_en,
            "text_zh": self.text_zh,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "SubtitleSegment":
        """从字典创建实例"""
        return cls(
            id=data["id"],
            start=data["start"],
            end=data["end"],
            text_en=data["text_en"],
            text_zh=data.get("text_zh", ""),
        )


@dataclass
class SubtitleList:
    """字幕列表"""
    segments: list[SubtitleSegment]
    language: str = "en"  # 原始语言

    def __len__(self) -> int:
        return len(self.segments)

    def __getitem__(self, index: int) -> SubtitleSegment:
        return self.segments[index]

    def append(self, segment: SubtitleSegment) -> None:
        """添加字幕片段"""
        self.segments.append(segment)

    def get_segment_at_time(self, time: float) -> Optional[SubtitleSegment]:
        """
        获取指定时间点的字幕片段

        Args:
            time: 时间点（秒）

        Returns:
            对应的字幕片段，如果不存在返回None
        """
        for segment in self.segments:
            if segment.start <= time <= segment.end:
                return segment
        return None

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "language": self.language,
            "segments": [seg.to_dict() for seg in self.segments],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "SubtitleList":
        """从字典创建实例"""
        segments = [SubtitleSegment.from_dict(seg) for seg in data["segments"]]
        return cls(segments=segments, language=data.get("language", "en"))

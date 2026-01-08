"""
字幕生成器模块 - 生成各种格式的字幕文件
"""

import json
from pathlib import Path
from typing import Optional

import config
from models.subtitle import SubtitleList
from utils.file_utils import get_cache_file_path


class SubtitleGenerator:
    """字幕生成器"""

    def __init__(self):
        pass

    def save_json(self, subtitle_list: SubtitleList, output_path: str) -> str:
        """
        保存JSON格式的字幕文件

        Args:
            subtitle_list: 字幕列表
            output_path: 输出文件路径

        Returns:
            保存的文件路径
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(subtitle_list.to_dict(), f, ensure_ascii=False, indent=2)

        return output_path

    def load_json(self, file_path: str) -> SubtitleList:
        """
        加载JSON格式的字幕文件

        Args:
            file_path: 字幕文件路径

        Returns:
            字幕列表对象
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return SubtitleList.from_dict(data)

    def save_srt(self, subtitle_list: SubtitleList, output_path: str) -> str:
        """
        保存SRT格式的字幕文件

        Args:
            subtitle_list: 字幕列表
            output_path: 输出文件路径

        Returns:
            保存的文件路径
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            for segment in subtitle_list.segments:
                # SRT格式: 序号
                f.write(f"{segment.id}\n")

                # 时间轴: HH:MM:SS,mmm --> HH:MM:SS,mmm
                start_time = self._seconds_to_srt_time(segment.start)
                end_time = self._seconds_to_srt_time(segment.end)
                f.write(f"{start_time} --> {end_time}\n")

                # 字幕文本（双语）
                f.write(f"{segment.text_en}\n")
                if segment.text_zh:
                    f.write(f"{segment.text_zh}\n")

                f.write("\n")

        return output_path

    def save_vtt(self, subtitle_list: SubtitleList, output_path: str) -> str:
        """
        保存WebVTT格式的字幕文件

        Args:
            subtitle_list: 字幕列表
            output_path: 输出文件路径

        Returns:
            保存的文件路径
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            # WebVTT头部
            f.write("WEBVTT\n\n")

            for segment in subtitle_list.segments:
                # 时间轴: HH:MM:SS.mmm --> HH:MM:SS.mmm
                start_time = self._seconds_to_vtt_time(segment.start)
                end_time = self._seconds_to_vtt_time(segment.end)
                f.write(f"{start_time} --> {end_time}\n")

                # 字幕文本（双语）
                f.write(f"{segment.text_en}\n")
                if segment.text_zh:
                    f.write(f"{segment.text_zh}\n")

                f.write("\n")

        return output_path

    def _seconds_to_srt_time(self, seconds: float) -> str:
        """
        将秒数转换为SRT时间格式 (HH:MM:SS,mmm)

        Args:
            seconds: 秒数

        Returns:
            SRT时间格式字符串
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        milliseconds = int((seconds % 1) * 1000)

        return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"

    def _seconds_to_vtt_time(self, seconds: float) -> str:
        """
        将秒数转换为WebVTT时间格式 (HH:MM:SS.mmm)

        Args:
            seconds: 秒数

        Returns:
            WebVTT时间格式字符串
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        milliseconds = int((seconds % 1) * 1000)

        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{milliseconds:03d}"

    def get_cache_path(self, video_path: str, format: str = "json") -> str:
        """
        获取字幕缓存文件路径

        Args:
            video_path: 视频文件路径
            format: 字幕格式 (json/srt/vtt)

        Returns:
            缓存文件路径
        """
        extension = f".{format}"
        return get_cache_file_path(
            video_path,
            config.SUBTITLE_CACHE_DIR,
            extension
        )

    def save_to_cache(self, subtitle_list: SubtitleList, video_path: str, format: str = "json") -> str:
        """
        保存字幕到缓存

        Args:
            subtitle_list: 字幕列表
            video_path: 视频文件路径
            format: 字幕格式 (json/srt/vtt)

        Returns:
            保存的文件路径
        """
        cache_path = self.get_cache_path(video_path, format)

        if format == "json":
            return self.save_json(subtitle_list, cache_path)
        elif format == "srt":
            return self.save_srt(subtitle_list, cache_path)
        elif format == "vtt":
            return self.save_vtt(subtitle_list, cache_path)
        else:
            raise ValueError(f"不支持的字幕格式: {format}")

    def load_from_cache(self, video_path: str, format: str = "json") -> Optional[SubtitleList]:
        """
        从缓存加载字幕

        Args:
            video_path: 视频文件路径
            format: 字幕格式 (json/srt/vtt)

        Returns:
            字幕列表对象，如果缓存不存在返回None
        """
        cache_path = self.get_cache_path(video_path, format)

        if not Path(cache_path).exists():
            return None

        if format == "json":
            return self.load_json(cache_path)
        else:
            # SRT和VTT格式暂不支持从缓存加载
            raise ValueError(f"暂不支持从缓存加载 {format} 格式的字幕")

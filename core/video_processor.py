"""
视频处理模块 - 使用FFmpeg进行视频处理
"""

import subprocess
import json
import os
from pathlib import Path
from typing import Optional, Tuple

import config
from models.video_info import VideoInfo
from utils.file_utils import get_cache_file_path, format_file_size
from utils.time_utils import seconds_to_time_string


class VideoProcessor:
    """视频处理器"""

    def __init__(self):
        self._check_ffmpeg()

    def _check_ffmpeg(self) -> None:
        """检查FFmpeg是否可用"""
        try:
            subprocess.run(
                ["ffmpeg", "-version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise RuntimeError(
                "FFmpeg未找到。请确保FFmpeg已安装并添加到系统PATH。\n"
                "Windows: 从 https://ffmpeg.org/download.html 下载并添加到PATH\n"
                "macOS: brew install ffmpeg\n"
                "Linux: sudo apt install ffmpeg"
            )

    def get_video_info(self, video_path: str) -> VideoInfo:
        """
        获取视频信息

        Args:
            video_path: 视频文件路径

        Returns:
            VideoInfo对象
        """
        # 使用ffprobe获取视频信息
        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            video_path
        ]

        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )

        info = json.loads(result.stdout.decode("utf-8"))

        # 解析视频流信息
        video_stream = None
        audio_stream = None

        for stream in info["streams"]:
            if stream["codec_type"] == "video" and video_stream is None:
                video_stream = stream
            elif stream["codec_type"] == "audio" and audio_stream is None:
                audio_stream = stream

        if video_stream is None:
            raise ValueError("视频文件中没有找到视频流")

        # 获取视频信息
        width = int(video_stream.get("width", 0))
        height = int(video_stream.get("height", 0))

        # 帧率处理
        fps_str = video_stream.get("r_frame_rate", "30/1")
        if "/" in fps_str:
            num, den = fps_str.split("/")
            fps = float(num) / float(den)
        else:
            fps = float(fps_str)

        # 时长和文件大小
        duration = float(info["format"].get("duration", 0))
        size = int(info["format"].get("size", 0))

        # 文件名
        name = Path(video_path).name

        return VideoInfo(
            path=video_path,
            name=name,
            duration=duration,
            width=width,
            height=height,
            fps=fps,
            size=size
        )

    def extract_audio(self, video_path: str, output_path: Optional[str] = None) -> str:
        """
        从视频中提取音频

        Args:
            video_path: 视频文件路径
            output_path: 输出音频文件路径（可选）

        Returns:
            提取的音频文件路径
        """
        if output_path is None:
            output_path = get_cache_file_path(
                video_path,
                config.AUDIO_CACHE_DIR,
                ".wav"
            )

        # 如果缓存文件已存在，直接返回
        if os.path.exists(output_path):
            return output_path

        # 使用FFmpeg提取音频
        cmd = [
            "ffmpeg",
            "-i", video_path,
            "-vn",  # 不处理视频
            "-acodec", "pcm_s16le",  # 使用PCM编码
            "-ar", "16000",  # 采样率16kHz（Whisper推荐）
            "-ac", "1",  # 单声道
            "-y",  # 覆盖已存在的文件
            output_path
        ]

        subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )

        return output_path

    def get_video_thumbnail(self, video_path: str, time: float = 1.0, size: Tuple[int, int] = (320, 180)) -> bytes:
        """
        获取视频缩略图

        Args:
            video_path: 视频文件路径
            time: 截取时间点（秒）
            size: 缩略图尺寸 (宽度, 高度)

        Returns:
            缩略图的字节数据
        """
        cmd = [
            "ffmpeg",
            "-i", video_path,
            "-ss", str(time),
            "-vframes", "1",
            "-s", f"{size[0]}x{size[1]}",
            "-f", "image2pipe",
            "-vcodec", "png",
            "-"
        ]

        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )

        return result.stdout

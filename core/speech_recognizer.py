"""
语音识别模块 - 使用Whisper进行语音识别
"""

import os
import time
from typing import Optional, Callable

import whisper
import torch

import config
from models.subtitle import SubtitleList, SubtitleSegment


class SpeechRecognizer:
    """语音识别器"""

    def __init__(self,
                 model_name: str = config.WHISPER_MODEL,
                 device: Optional[str] = None,
                 progress_callback: Optional[Callable[[str], None]] = None):
        """
        初始化语音识别器

        Args:
            model_name: Whisper模型名称 (tiny/base/small/medium/large)
            device: 运行设备 (cpu/cuda)，None则自动检测
            progress_callback: 进度回调函数
        """
        self.model_name = model_name
        self.device = self._get_device(device)
        self.progress_callback = progress_callback
        self.model = None

    def _get_device(self, device: Optional[str]) -> str:
        """检测可用的设备"""
        if device is not None:
            return device

        if torch.cuda.is_available():
            return "cuda"
        return "cpu"

    def _load_model(self) -> None:
        """加载Whisper模型"""
        if self.model is None:
            if self.progress_callback:
                self.progress_callback(f"正在加载Whisper模型 ({self.model_name})...")

            self.model = whisper.load_model(self.model_name, device=self.device)

            if self.progress_callback:
                self.progress_callback("模型加载完成")

    def transcribe(self,
                   audio_path: str,
                   language: str = "en") -> SubtitleList:
        """
        转录音频文件

        Args:
            audio_path: 音频文件路径
            language: 音频语言代码

        Returns:
            SubtitleList对象
        """
        self._load_model()

        if self.progress_callback:
            self.progress_callback("正在进行语音识别...")

        start_time = time.time()

        # 使用Whisper进行转录
        result = self.model.transcribe(
            audio_path,
            language=language,
            word_timestamps=True,
            verbose=False
        )

        elapsed_time = time.time() - start_time

        if self.progress_callback:
            self.progress_callback(f"语音识别完成 (耗时: {elapsed_time:.1f}秒)")

        # 将Whisper的结果转换为SubtitleList
        segments = []
        for i, segment in enumerate(result["segments"]):
            subtitle_segment = SubtitleSegment(
                id=i + 1,
                start=segment["start"],
                end=segment["end"],
                text_en=segment["text"].strip()
            )
            segments.append(subtitle_segment)

        return SubtitleList(segments=segments, language=language)

    def transcribe_with_progress(self,
                                  audio_path: str,
                                  language: str = "en",
                                  step_callback: Optional[Callable[[float, str], None]] = None) -> SubtitleList:
        """
        转录音频文件（带进度回调）

        Args:
            audio_path: 音频文件路径
            language: 音频语言代码
            step_callback: 进度回调函数 (progress: float, message: str)

        Returns:
            SubtitleList对象
        """
        self._load_model()

        if step_callback:
            step_callback(0, "正在进行语音识别...")

        start_time = time.time()

        # 使用Whisper进行转录
        result = self.model.transcribe(
            audio_path,
            language=language,
            word_timestamps=True,
            verbose=False
        )

        elapsed_time = time.time() - start_time

        if step_callback:
            step_callback(1.0, f"语音识别完成 (耗时: {elapsed_time:.1f}秒)")

        # 将Whisper的结果转换为SubtitleList
        segments = []
        total_segments = len(result["segments"])

        for i, segment in enumerate(result["segments"]):
            subtitle_segment = SubtitleSegment(
                id=i + 1,
                start=segment["start"],
                end=segment["end"],
                text_en=segment["text"].strip()
            )
            segments.append(subtitle_segment)

            # 更新进度
            if step_callback:
                progress = (i + 1) / total_segments
                step_callback(progress, f"处理字幕片段 {i + 1}/{total_segments}")

        return SubtitleList(segments=segments, language=language)

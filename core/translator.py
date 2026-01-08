"""
翻译模块 - 使用Google Translate进行翻译
"""

import time
import random
from typing import Optional, Callable

from googletrans import Translator
from googletrans.constants import LANGUAGES

import config
from models.subtitle import SubtitleList


class GoogleTranslator:
    """Google翻译器"""

    def __init__(self,
                 source_lang: str = config.TRANSLATION_SOURCE_LANG,
                 target_lang: str = config.TRANSLATION_TARGET_LANG,
                 progress_callback: Optional[Callable[[str], None]] = None):
        """
        初始化翻译器

        Args:
            source_lang: 源语言代码
            target_lang: 目标语言代码
            progress_callback: 进度回调函数
        """
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.progress_callback = progress_callback
        self.translator = Translator()
        self.max_retries = config.TRANSLATION_MAX_RETRIES  # 最大重试次数
        self.retry_delay = config.TRANSLATION_RETRY_DELAY  # 重试延迟（秒）

    def translate_text(self, text: str, retry_count: int = 0) -> str:
        """
        翻译单个文本（带重试机制）

        Args:
            text: 待翻译的文本
            retry_count: 当前重试次数

        Returns:
            翻译后的文本
        """
        if not text or not text.strip():
            return ""

        try:
            # 设置超时时间
            result = self.translator.translate(
                text,
                src=self.source_lang,
                dest=self.target_lang
            )
            return result.text

        except Exception as e:
            error_msg = str(e)

            # 如果是超时错误且未达到最大重试次数
            if 'timeout' in error_msg.lower() or 'timed out' in error_msg.lower():
                if retry_count < self.max_retries:
                    # 指数退避策略
                    wait_time = self.retry_delay * (2 ** retry_count) + random.uniform(0, 1)
                    print(f"翻译超时，{wait_time:.1f}秒后重试 ({retry_count + 1}/{self.max_retries})...")
                    time.sleep(wait_time)

                    # 重新创建translator实例
                    self.translator = Translator()

                    # 递归重试
                    return self.translate_text(text, retry_count + 1)
                else:
                    print(f"翻译失败（已重试{self.max_retries}次）: {error_msg}")
            else:
                print(f"翻译错误: {error_msg}")

            # 翻译失败时返回原文
            return text

    def translate_subtitle_list(self,
                                 subtitle_list: SubtitleList,
                                 batch_size: int = config.TRANSLATION_BATCH_SIZE,
                                 delay: float = config.TRANSLATION_DELAY) -> SubtitleList:
        """
        翻译字幕列表

        Args:
            subtitle_list: 字幕列表
            batch_size: 批次大小
            delay: 批次之间的延迟（秒）

        Returns:
            翻译后的字幕列表
        """
        if self.progress_callback:
            self.progress_callback("开始翻译字幕...")

        segments = subtitle_list.segments
        total_segments = len(segments)

        # 批量翻译
        for i in range(0, total_segments, batch_size):
            batch = segments[i:i + batch_size]

            for j, segment in enumerate(batch):
                # 更新进度
                current_index = i + j
                if self.progress_callback:
                    self.progress_callback(
                        f"翻译字幕 {current_index + 1}/{total_segments}"
                    )

                # 翻译文本
                segment.text_zh = self.translate_text(segment.text_en)

            # 批次之间延迟，避免API限流
            if i + batch_size < total_segments:
                time.sleep(delay)

        if self.progress_callback:
            self.progress_callback("字幕翻译完成")

        return subtitle_list

    def translate_subtitle_list_with_progress(self,
                                              subtitle_list: SubtitleList,
                                              batch_size: int = config.TRANSLATION_BATCH_SIZE,
                                              delay: float = config.TRANSLATION_DELAY,
                                              step_callback: Optional[Callable[[float, str], None]] = None) -> SubtitleList:
        """
        翻译字幕列表（带详细进度回调）

        Args:
            subtitle_list: 字幕列表
            batch_size: 批次大小
            delay: 批次之间的延迟（秒）
            step_callback: 进度回调函数 (progress: float, message: str)

        Returns:
            翻译后的字幕列表
        """
        if step_callback:
            step_callback(0, "开始翻译字幕...")

        segments = subtitle_list.segments
        total_segments = len(segments)

        # 批量翻译
        for i in range(0, total_segments, batch_size):
            batch = segments[i:i + batch_size]

            for j, segment in enumerate(batch):
                # 更新进度
                current_index = i + j
                progress = current_index / total_segments

                if step_callback:
                    step_callback(
                        progress,
                        f"翻译字幕 {current_index + 1}/{total_segments}"
                    )

                # 翻译文本
                segment.text_zh = self.translate_text(segment.text_en)

            # 批次之间延迟，避免API限流
            if i + batch_size < total_segments:
                time.sleep(delay)

        if step_callback:
            step_callback(1.0, "字幕翻译完成")

        return subtitle_list

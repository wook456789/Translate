"""
应用配置文件
"""

import os
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).parent

# 缓存目录
CACHE_DIR = BASE_DIR / "cache"
AUDIO_CACHE_DIR = CACHE_DIR / "audio"
SUBTITLE_CACHE_DIR = CACHE_DIR / "subtitles"

# 创建缓存目录
CACHE_DIR.mkdir(exist_ok=True)
AUDIO_CACHE_DIR.mkdir(exist_ok=True)
SUBTITLE_CACHE_DIR.mkdir(exist_ok=True)

# Whisper配置
WHISPER_MODEL = "base"  # 可选: tiny, base, small, medium, large
WHISPER_DEVICE = "cpu"  # 自动检测，如果可用则使用cuda

# 翻译配置
TRANSLATION_SOURCE_LANG = "en"
TRANSLATION_TARGET_LANG = "zh-CN"
TRANSLATION_BATCH_SIZE = 10  # 每次翻译的文本数量
TRANSLATION_DELAY = 1  # 翻译请求之间的延迟（秒）
TRANSLATION_MAX_RETRIES = 3  # 翻译失败最大重试次数
TRANSLATION_RETRY_DELAY = 2  # 翻译重试基础延迟（秒）

# 视频配置
SUPPORTED_VIDEO_FORMATS = [".mp4", ".mov", ".mkv", ".avi", ".flv", ".wmv"]

# 字幕配置
SUBTITLE_FORMAT = "json"  # 输出格式：json, srt, vtt

# GUI配置
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
VIDEO_PANEL_WIDTH = 900
SUBTITLE_PANEL_WIDTH = 500

# 复读配置
REPEAT_COUNTS = [0, 3, 10, 20]  # 可选的复读次数
REPEAT_BUFFER_TIME = 0.3  # 复读时句子结束后的缓冲时间（秒），确保完整听完最后一个单词

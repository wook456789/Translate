"""
文件操作工具函数
"""

import os
import hashlib
from pathlib import Path
from typing import Optional


def get_file_hash(file_path: str) -> str:
    """
    计算文件的MD5哈希值

    Args:
        file_path: 文件路径

    Returns:
        文件的MD5哈希值
    """
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def get_file_extension(file_path: str) -> str:
    """
    获取文件扩展名（小写，包含点号）

    Args:
        file_path: 文件路径

    Returns:
        文件扩展名，如 ".mp4"
    """
    return Path(file_path).suffix.lower()


def is_video_file(file_path: str, supported_formats: list) -> bool:
    """
    检查文件是否是支持的视频格式

    Args:
        file_path: 文件路径
        supported_formats: 支持的格式列表，如 [".mp4", ".mov"]

    Returns:
        如果是支持的视频格式返回True，否则返回False
    """
    ext = get_file_extension(file_path)
    return ext in supported_formats


def ensure_directory_exists(directory: str) -> None:
    """
    确保目录存在，如果不存在则创建

    Args:
        directory: 目录路径
    """
    Path(directory).mkdir(parents=True, exist_ok=True)


def get_cache_file_path(original_path: str, cache_dir: str, extension: str) -> str:
    """
    根据原文件路径生成缓存文件路径

    Args:
        original_path: 原文件路径
        cache_dir: 缓存目录
        extension: 缓存文件扩展名

    Returns:
        缓存文件路径
    """
    file_hash = get_file_hash(original_path)
    filename = f"{file_hash}{extension}"
    return str(Path(cache_dir) / filename)


def format_file_size(bytes_size: int) -> str:
    """
    格式化文件大小显示

    Args:
        bytes_size: 文件大小（字节）

    Returns:
        格式化的文件大小字符串
    """
    for unit in ["B", "KB", "MB", "GB"]:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f}{unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f}TB"


def safe_filename(filename: str) -> str:
    """
    生成安全的文件名（移除不安全字符）

    Args:
        filename: 原始文件名

    Returns:
        安全的文件名
    """
    # 移除路径分隔符和其他不安全字符
    unsafe_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    safe_name = filename
    for char in unsafe_chars:
        safe_name = safe_name.replace(char, '_')
    return safe_name

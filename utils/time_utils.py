"""
时间格式化工具函数
"""


def milliseconds_to_time_string(ms: int) -> str:
    """
    将毫秒转换为时间字符串 (HH:MM:SS.mmm)

    Args:
        ms: 毫秒数

    Returns:
        时间字符串，格式为 HH:MM:SS.mmm
    """
    hours = ms // 3600000
    minutes = (ms % 3600000) // 60000
    seconds = (ms % 60000) // 1000
    milliseconds = ms % 1000

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"


def seconds_to_time_string(seconds: float) -> str:
    """
    将秒数转换为时间字符串 (HH:MM:SS)

    Args:
        seconds: 秒数

    Returns:
        时间字符串，格式为 HH:MM:SS
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def time_string_to_seconds(time_str: str) -> float:
    """
    将时间字符串转换为秒数

    Args:
        time_str: 时间字符串，格式为 HH:MM:SS 或 HH:MM:SS.mmm

    Returns:
        秒数（浮点数）
    """
    parts = time_str.split(":")
    hours = int(parts[0])
    minutes = int(parts[1])

    # 处理秒和毫秒
    sec_parts = parts[2].split(".")
    seconds = int(sec_parts[0])
    milliseconds = int(sec_parts[1]) if len(sec_parts) > 1 else 0

    total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000
    return total_seconds


def format_duration(seconds: float) -> str:
    """
    格式化时长显示

    Args:
        seconds: 秒数

    Returns:
        格式化的时长字符串
    """
    if seconds < 60:
        return f"{int(seconds)}秒"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}分{secs}秒"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}小时{minutes}分"

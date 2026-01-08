#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试打包后的程序是否包含必要的文件"""

import sys
import os

def check_packaged_files():
    """检查打包后的文件"""

    print("=" * 60)
    print("打包文件检查工具")
    print("=" * 60)

    # 检查是否在打包环境中运行
    if getattr(sys, 'frozen', False):
        print(f"✓ 运行在打包环境")
        print(f"  可执行文件: {sys.executable}")
        print(f"  MEIPASS: {sys._MEIPASS}")

        # 检查 Whisper 模型
        model_path = os.path.join(sys._MEIPASS, 'models', 'whisper', 'base.pt')
        if os.path.exists(model_path):
            size_mb = os.path.getsize(model_path) / (1024 * 1024)
            print(f"✓ Whisper 模型: {model_path}")
            print(f"  大小: {size_mb:.1f} MB")
        else:
            print(f"✗ Whisper 模型未找到: {model_path}")

        # 检查 FFmpeg（可选）
        ffmpeg_names = ['ffmpeg.exe', 'ffmpeg']
        for name in ffmpeg_names:
            ffmpeg_path = os.path.join(sys._MEIPASS, name)
            if os.path.exists(ffmpeg_path):
                print(f"✓ FFmpeg: {ffmpeg_path}")
                break
        else:
            print(f"⚠ FFmpeg 未在打包目录中（使用 Qt 内置播放器不需要）")

        # 列出 models 目录
        models_dir = os.path.join(sys._MEIPASS, 'models')
        if os.path.exists(models_dir):
            print(f"\n✓ models 目录存在:")
            for root, dirs, files in os.walk(models_dir):
                level = root.replace(sys._MEIPASS, '').count(os.sep)
                indent = ' ' * 2 * level
                print(f'{indent}{os.path.basename(root)}/')
                subindent = ' ' * 2 * (level + 1)
                for file in files[:5]:  # 只显示前5个文件
                    print(f'{subindent}{file}')
                if len(files) > 5:
                    print(f'{subindent}... 和 {len(files) - 5} 个其他文件')

    else:
        print("✗ 未在打包环境中运行")
        print("  请运行 dist/Translate.exe 进行测试")

    print("=" * 60)

if __name__ == '__main__':
    check_packaged_files()
    input("\n按回车键退出...")

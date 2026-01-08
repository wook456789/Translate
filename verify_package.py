#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""验证打包后的文件是否包含 Whisper 模型"""

import sys
import os

print("=" * 60)
print("Translate.exe 打包验证工具")
print("=" * 60)

if getattr(sys, 'frozen', False):
    print(f"[OK] 运行在打包环境")
    print(f"可执行文件: {sys.executable}")
    print(f"MEIPASS: {sys._MEIPASS}")
    print()

    # 检查模型
    model_path = os.path.join(sys._MEIPASS, 'models', 'whisper', 'base.pt')
    if os.path.exists(model_path):
        size_mb = os.path.getsize(model_path) / (1024 * 1024)
        print(f"[OK] Whisper 模型已打包")
        print(f"路径: {model_path}")
        print(f"大小: {size_mb:.1f} MB")
    else:
        print(f"[ERROR] Whisper 模型未找到!")
        print(f"期望路径: {model_path}")

    # 列出 models 目录
    models_dir = os.path.join(sys._MEIPASS, 'models')
    if os.path.exists(models_dir):
        print()
        print("[INFO] models 目录内容:")
        for item in os.listdir(models_dir):
            item_path = os.path.join(models_dir, item)
            if os.path.isdir(item_path):
                print(f"  [DIR] {item}/")
                # 列出子目录内容
                sub_path = os.path.join(models_dir, item)
                if os.path.exists(sub_path):
                    for sub_item in os.listdir(sub_path)[:10]:
                        print(f"        {sub_item}")
            else:
                size = os.path.getsize(item_path) / 1024
                print(f"  [FILE] {item} ({size:.1f} KB)")
    else:
        print(f"[ERROR] models 目录不存在!")

else:
    print("[INFO] 当前在开发环境中运行")
    print("打包后运行此工具可以验证打包内容")

print()
print("=" * 60)
input("按回车键退出...")

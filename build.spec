# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(SPEC))

# 收集所有需要的数据文件
datas = [
    (os.path.join(current_dir, 'models', 'whisper'), 'models/whisper'),
    (os.path.join(current_dir, 'config.py'), '.'),
]

# 收集 PyQt6 插件（重要！）
datas += collect_data_files('PyQt6')

# 收集隐藏的导入
hiddenimports = [
    'whisper',
    'torch',
    'numpy',
    'googletrans',
    'ffmpeg',
    'PyQt6.QtCore',
    'PyQt6.QtGui',
    'PyQt6.QtWidgets',
    'PyQt6.QtMultimedia',
    'PyQt6.QtMultimediaWidgets',
    'PyQt6.QtNetwork',
]

# 收集 whisper 的子模块
hiddenimports += collect_submodules('whisper')
hiddenimports += collect_submodules('torch')

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[current_dir],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Translate',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 可以添加图标文件路径
)

@echo off
chcp 65001 >nul
echo ========================================
echo 视频双语字幕生成与交互式复读系统
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.10或更高版本
    pause
    exit /b 1
)

REM 检查FFmpeg是否安装
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo 警告: 未找到FFmpeg
    echo 请安装FFmpeg并添加到系统PATH
    echo.
    echo Windows安装方法:
    echo 1. 访问 https://ffmpeg.org/download.html
    echo 2. 下载Windows版本
    echo 3. 解压并添加到系统PATH
    echo.
    pause
    exit /b 1
)

REM 检查依赖是否安装
echo 检查Python依赖...
python -c "import PyQt6" >nul 2>&1
if errorlevel 1 (
    echo Python依赖未安装，正在安装...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo 依赖安装失败，请检查网络连接
        pause
        exit /b 1
    )
    echo.
    echo 依赖安装完成！
    echo.
)

echo 启动应用...
echo.
python main.py

if errorlevel 1 (
    echo.
    echo 应用运行出错
    pause
)

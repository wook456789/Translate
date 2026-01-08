"""
环境诊断脚本 - 帮助诊断常见的安装和运行问题
"""

import sys
import platform
import subprocess
from pathlib import Path


def print_section(title):
    """打印分节标题"""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def check_python():
    """检查Python环境"""
    print_section("Python环境检查")
    print(f"Python版本: {sys.version}")
    print(f"Python路径: {sys.executable}")
    print(f"系统架构: {platform.machine()}")
    print(f"操作系统: {platform.platform()}")


def check_module(module_name):
    """检查模块是否可导入"""
    try:
        __import__(module_name)
        print(f"✓ {module_name}: 已安装")
        return True
    except ImportError as e:
        print(f"✗ {module_name}: 未安装或导入失败")
        print(f"  错误: {e}")
        return False
    except Exception as e:
        print(f"✗ {module_name}: 加载失败")
        print(f"  错误: {e}")
        return False


def check_modules():
    """检查所有依赖模块"""
    print_section("依赖模块检查")

    modules = [
        "PyQt6",
        "PyQt6.QtCore",
        "PyQt6.QtWidgets",
        "PyQt6.QtMultimedia",
        "PyQt6.QtMultimediaWidgets",
        "whisper",
        "googletrans",
        "ffmpeg_python",
        "torch",
        "numpy"
    ]

    failed = []
    for module in modules:
        if not check_module(module):
            failed.append(module)

    return failed


def check_ffmpeg():
    """检查FFmpeg"""
    print_section("FFmpeg检查")

    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print("✓ FFmpeg: 已安装")
            # 提取版本信息
            version_line = result.stdout.split('\n')[0]
            print(f"  {version_line}")
            return True
    except FileNotFoundError:
        print("✗ FFmpeg: 未找到")
        print("  请安装FFmpeg并添加到系统PATH")
        return False
    except Exception as e:
        print(f"✗ FFmpeg: 检查失败 - {e}")
        return False


def check_vc_redist():
    """检查Visual C++运行库"""
    print_section("Visual C++运行库检查")

    # 检查常见的DLL文件
    dll_paths = [
        Path("C:/Windows/System32/msvcp140.dll"),
        Path("C:/Windows/System32/vcruntime140.dll"),
        Path("C:/Windows/System32/vcruntime140_1.dll"),
    ]

    missing = []
    for dll_path in dll_paths:
        if dll_path.exists():
            print(f"✓ {dll_path.name}: 已安装")
        else:
            print(f"✗ {dll_path.name}: 未找到")
            missing.append(dll_path.name)

    if missing:
        print("\n建议安装 Microsoft Visual C++ 2015-2022 Redistributable")
        print("下载地址: https://aka.ms/vs/17/release/vc_redist.x64.exe")

    return len(missing) == 0


def check_project_structure():
    """检查项目结构"""
    print_section("项目结构检查")

    required_files = [
        "main.py",
        "config.py",
        "requirements.txt",
        "core/video_processor.py",
        "core/speech_recognizer.py",
        "core/translator.py",
        "core/subtitle_generator.py",
        "gui/main_window.py",
        "gui/video_player.py",
        "gui/subtitle_panel.py",
        "gui/control_panel.py",
        "gui/upload_dialog.py",
        "models/subtitle.py",
        "models/video_info.py",
        "utils/file_utils.py",
        "utils/time_utils.py",
    ]

    base_path = Path(__file__).parent

    missing = []
    for file_path in required_files:
        full_path = base_path / file_path
        if full_path.exists():
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path}: 未找到")
            missing.append(file_path)

    return missing


def print_recommendations(failed_modules, ffmpeg_ok, vc_ok, missing_files):
    """打印建议"""
    print_section("诊断建议")

    if not failed_modules and ffmpeg_ok and vc_ok and not missing_files:
        print("✓ 所有检查通过！环境配置正确。")
        print("\n您现在可以运行应用:")
        print("  python main.py")
        print("或双击 run.bat")
        return

    recommendations = []

    if failed_modules:
        recommendations.append("1. 安装缺失的Python模块:")
        recommendations.append("   pip install -r requirements.txt")

    if not ffmpeg_ok:
        recommendations.append("2. 安装FFmpeg:")
        recommendations.append("   访问 https://ffmpeg.org/download.html")
        recommendations.append("   下载并安装，然后添加到系统PATH")

    if not vc_ok:
        recommendations.append("3. 安装Visual C++运行库:")
        recommendations.append("   下载: https://aka.ms/vs/17/release/vc_redist.x64.exe")
        recommendations.append("   安装后重启计算机")

    if missing_files:
        recommendations.append("4. 项目文件缺失，请确保项目完整")

    for rec in recommendations:
        print(rec)

    print("\n详细信息请查看 TROUBLESHOOTING.md")


def main():
    """主函数"""
    print("=" * 60)
    print(" 视频双语字幕系统 - 环境诊断工具")
    print("=" * 60)

    # 运行各项检查
    check_python()
    failed_modules = check_modules()
    ffmpeg_ok = check_ffmpeg()
    vc_ok = check_vc_redist()
    missing_files = check_project_structure()

    # 打印建议
    print_recommendations(failed_modules, ffmpeg_ok, vc_ok, missing_files)

    print("\n" + "=" * 60)
    print("诊断完成")
    print("=" * 60)

    # 等待用户按键
    input("\n按回车键退出...")


if __name__ == "__main__":
    main()

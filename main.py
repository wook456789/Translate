"""
应用入口
"""

import sys
import os

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt


from gui.main_window import MainWindow


def main():
    """主函数"""
    # 启用高DPI缩放
    if hasattr(Qt.ApplicationAttribute, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)

    # 创建应用
    app = QApplication(sys.argv)
    app.setApplicationName("视频双语字幕生成与交互式复读系统")
    app.setOrganizationName("VideoSubtitleSystem")

    # 设置应用样式
    app.setStyle("Fusion")

    # 创建并显示主窗口
    window = MainWindow()
    window.show()

    # 运行应用
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

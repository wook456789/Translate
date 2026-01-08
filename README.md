# 视频双语字幕生成与交互式复读系统

一个智能的双语字幕系统，能够自动翻译视频内容，并提供交互式复读功能，特别适合语言学习。

## ✨ 功能特性

- 🎬 **自动语音识别**：基于 OpenAI Whisper，高准确率
- 🌐 **中英双语字幕**：使用 Google Translate 自动翻译
- 🔄 **交互式复读**：点击任意句子即可设置复读（3/10/20 次）
- 💾 **智能缓存**：已处理的视频自动保存字幕，下次秒开
- 🎯 **字幕同步**：播放时自动高亮和滚动
- 📺 **视频播放**：内置播放器，支持所有常见格式

## 🚀 快速开始

### 方式一：使用打包的 exe（推荐）

1. 下载 `Translate.exe`（约 423MB）
2. 双击运行即可
3. 点击 **文件 → 打开视频** 选择您的视频

**注意**：首次启动需要 10-30 秒加载模型。

### 方式二：从源码运行

```bash
# 克隆仓库
git clone https://github.com/wook456789/Translate.git
cd Translate

# 安装依赖
pip install -r requirements.txt

# 运行程序
python main.py
```

## 📋 系统要求

- **操作系统**：Windows 10/11
- **Python**：3.10+ （仅源码版本）
- **网络**：翻译功能需要（语音识别完全离线）
- **内存**：建议 4GB+
- **FFmpeg**：需要添加到系统 PATH（仅源码版本）

## 🛠️ 技术栈

- **GUI**：PyQt6
- **语音识别**：OpenAI Whisper
- **翻译**：Google Translate (googletrans)
- **视频处理**：FFmpeg
- **打包**：PyInstaller

## 📁 项目结构

```
Translate/
├── main.py                 # 应用入口
├── config.py              # 配置文件
├── build.spec             # 打包配置
├── requirements.txt       # 依赖列表
├── core/                  # 核心模块
│   ├── video_processor.py    # 视频处理
│   ├── speech_recognizer.py  # 语音识别
│   ├── translator.py         # 翻译
│   └── subtitle_generator.py # 字幕生成
├── gui/                   # GUI 界面
│   ├── main_window.py        # 主窗口
│   ├── video_player.py       # 播放器
│   ├── subtitle_panel.py     # 字幕面板
│   ├── control_panel.py      # 控制面板
│   └── upload_dialog.py      # 上传对话框
├── models/                # 数据模型
│   ├── subtitle.py
│   └── video_info.py
└── utils/                 # 工具函数
```

## 📖 使用说明

详细使用说明请查看 [使用说明.md](使用说明.md)

### 基本流程

1. **打开视频**：文件 → 打开视频
2. **生成字幕**：自动识别和翻译（首次）
3. **播放学习**：
   - 点击字幕选择句子
   - 设置复读次数
   - 点击"开始复读"

### 字幕文件

生成的字幕保存在视频同目录：
- `{视频名}_bilingual.json` - 程序使用
- `{视频名}_bilingual.srt` - 标准格式

## 🔧 开发

### 打包

```bash
# 安装 PyInstaller
pip install pyinstaller

# 下载 Whisper 模型
python -c "import whisper; whisper.load_model('base')"
cp ~/.cache/whisper/base.pt models/whisper/

# 打包
pyinstaller build.spec
```

打包后的 exe 在 `dist/Translate.exe`

### 配置

编辑 `config.py` 可以修改：
- Whisper 模型大小（tiny/base/small/medium/large）
- 翻译语言
- 复读次数选项
- 缓冲时间等

## 🐛 故障排除

### 常见问题

1. **DLL 加载失败**：安装 [Visual C++ 运行库](https://aka.ms/vs/17/release/vc_redist.x64.exe)
2. **翻译超时**：检查网络连接，可能需要代理
3. **模型加载慢**：首次启动正常，10-30 秒
4. **FFmpeg 未找到**：确保 FFmpeg 已添加到系统 PATH

详细问题请查看 [TROUBLESHOOTING.md](TROUBLESHOOTING.md) 和 [BUILD.md](BUILD.md)

## 📝 更新日志

### v1.0.0 (2025-01-08)

- ✅ 初始版本
- ✅ Whisper 语音识别
- ✅ Google 翻译集成
- ✅ 交互式复读功能
- ✅ 字幕自动缓存
- ✅ 智能滚动优化
- ✅ 打包成单文件 exe
- ✅ 预打包 Whisper 模型

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可

MIT License

## 🙏 致谢

- [OpenAI Whisper](https://github.com/openai/whisper) - 语音识别
- [googletrans](https://github.com/ssut/py-googletrans) - 翻译
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - GUI 框架
- [FFmpeg](https://ffmpeg.org/) - 视频处理

---

**Made with ❤️ for language learners**

# 视频双语字幕生成与交互式复读系统

一个智能的本地桌面应用，能够自动翻译英文视频内容，生成中英双语字幕，并提供交互式复读功能。

## 功能特性

- 自动语音识别（基于OpenAI Whisper）
- 中英双语字幕生成（基于Google Translate）
- 交互式视频播放器
- 点击字幕跳转到对应时间点
- 自定义复读次数（0/3/10/20次）
- 复读进度显示
- 保持原视频质量

## 安装

### 前置要求

1. Python 3.10 或更高版本
2. FFmpeg（必须添加到系统PATH）

#### Windows安装FFmpeg：

1. 下载FFmpeg：https://ffmpeg.org/download.html
2. 解压到某个目录（如 `C:\ffmpeg`）
3. 将 `C:\ffmpeg\bin` 添加到系统PATH环境变量

#### macOS安装FFmpeg：

```bash
brew install ffmpeg
```

#### Linux安装FFmpeg：

```bash
sudo apt update
sudo apt install ffmpeg
```

### 安装Python依赖

```bash
pip install -r requirements.txt
```

## 使用方法

1. 启动应用：

```bash
python main.py
```

2. 点击"打开视频"按钮，选择要处理的英文视频文件

3. 等待系统自动处理（语音识别和翻译）

4. 处理完成后，视频会自动播放

5. 右侧字幕面板显示双语字幕

6. 点击任意字幕可跳转到对应时间点

7. 选择复读次数，点击"复读"按钮开始复读

## 复读功能

- **0次**：正常播放，不复读
- **3次**：重复播放当前句子3次
- **10次**：重复播放当前句子10次
- **20次**：重复播放当前句子20次

## 技术栈

- **GUI框架**：PyQt6
- **语音识别**：OpenAI Whisper
- **翻译服务**：Google Translate
- **视频处理**：FFmpeg
- **视频播放**：Qt QMediaPlayer

## 项目结构

```
├── main.py                      # 应用入口
├── requirements.txt             # 依赖清单
├── config.py                    # 配置文件
├── core/                        # 核心模块
│   ├── video_processor.py       # 视频处理
│   ├── speech_recognizer.py     # Whisper语音识别
│   ├── translator.py            # Google翻译
│   └── subtitle_generator.py    # 字幕生成器
├── gui/                         # GUI模块
│   ├── main_window.py           # 主窗口
│   ├── video_player.py          # 视频播放器组件
│   ├── subtitle_panel.py        # 字幕面板组件
│   ├── control_panel.py         # 控制面板组件
│   └── upload_dialog.py         # 上传对话框
├── models/                      # 数据模型
│   ├── subtitle.py              # 字幕数据模型
│   └── video_info.py            # 视频信息模型
└── utils/                       # 工具函数
    ├── time_utils.py            # 时间格式化工具
    └── file_utils.py            # 文件操作工具
```

## 常见问题

### FFmpeg未找到错误

确保FFmpeg已正确安装并添加到系统PATH。在终端中运行 `ffmpeg -version` 验证。

### Whisper模型下载慢

首次运行时，Whisper会自动下载模型。如果下载慢，可以手动下载模型文件并放到指定目录。

### 翻译API限流

如果遇到翻译API限流，可以调整翻译批次大小或在翻译请求之间添加延迟。

## 许可证

MIT License

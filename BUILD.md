# 打包说明

## 方案 B：智能混合版

这个版本包含以下特点：
- ✅ 已预下载 Whisper 模型（base 版本，约 145MB）
- ✅ 支持离线语音识别
- ✅ 使用 Google Translate 翻译（需要联网）
- ✅ 已生成的字幕文件可离线使用
- ✅ 打包成单个 exe 文件

## 打包步骤

### 1. 确保模型已下载

```bash
# 检查模型文件是否存在
ls models/whisper/base.pt
```

如果不存在，运行：
```bash
python -c "import whisper; whisper.load_model('base')"
cp ~/.cache/whisper/base.pt models/whisper/
```

### 2. 执行打包

```bash
# 使用 spec 文件打包
pyinstaller build.spec

# 或者直接使用命令（不推荐，因为需要指定很多参数）
# pyinstaller --onefile --windowed --add-data "models/whisper;models/whisper" main.py
```

### 3. 打包输出

打包成功后，在 `dist` 目录下会生成 `Translate.exe` 文件。

文件大小预计：
- 基础程序：约 300-400 MB
- 包含 Whisper 模型：约 450-500 MB

### 4. 测试

```bash
# 运行打包后的程序
dist\Translate.exe
```

## 注意事项

### 首次启动
- 模型加载需要 10-30 秒
- 这是正常现象，请耐心等待
- 后续使用会快很多

### 翻译功能
- 需要网络连接
- 如果网络不可用，翻译会失败
- 已生成的字幕文件可以离线播放

### FFmpeg
- 程序使用 FFmpeg 处理视频
- 需要系统安装 FFmpeg 或使用打包的版本

### 分发
- 可以直接分发 exe 文件
- 客户无需安装 Python
- 但仍需要网络连接用于翻译

## 故障排除

### 模型加载失败
如果提示找不到模型文件：
1. 确认 `models/whisper/base.pt` 存在
2. 检查 build.spec 中的路径配置
3. 重新打包

### FFmpeg 相关错误
如果提示 FFmpeg 未找到：
1. 安装 FFmpeg 到系统 PATH
2. 或者在 spec 文件中添加 FFmpeg 二进制文件

### 翻译失败
如果翻译一直失败：
1. 检查网络连接
2. 确认可以访问 Google 服务
3. 查看控制台输出（将 console=True 查看详细错误）

## 文件结构

打包后的文件结构（在 _MEIPASS 临时目录中）：
```
_MEIPASS/
├── models/
│   └── whisper/
│       └── base.pt          # Whisper 模型
├── config.py
├── core/
│   ├── __init__.py
│   ├── video_processor.py
│   ├── speech_recognizer.py
│   ├── translator.py
│   └── subtitle_generator.py
├── gui/
│   ├── __init__.py
│   ├── main_window.py
│   ├── video_player.py
│   ├── subtitle_panel.py
│   ├── control_panel.py
│   └── upload_dialog.py
├── models/
│   ├── __init__.py
│   ├── subtitle.py
│   └── video_info.py
├── utils/
│   ├── __init__.py
│   ├── time_utils.py
│   └── file_utils.py
├── main.py
└── ...其他依赖
```

## 优化建议

### 减小文件大小
1. 使用 UPX 压缩（已启用）
2. 排除不需要的模块（在 spec 文件的 excludes 中添加）
3. 使用更小的 Whisper 模型（tiny 版本约 40MB）

### 提高启动速度
1. 延迟加载模型（在首次使用时才加载）
2. 使用更小的模型
3. 添加启动画面

### 改善翻译体验
1. 实现本地翻译模型（完全离线）
2. 添加翻译缓存
3. 支持多个翻译服务自动切换

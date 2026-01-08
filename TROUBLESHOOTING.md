# 问题解决指南

## PyQt6 DLL加载失败问题

### 问题描述
```
ImportError: DLL load failed while importing QtCore: 找不到指定的程序。
```

### 解决方案

#### 方案1：安装Visual C++运行库（推荐）

PyQt6需要Microsoft Visual C++ 2015-2022 Redistributable。

1. **下载运行库**
   访问微软官网下载：
   https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist

   或直接下载链接：
   - 64位系统：https://aka.ms/vs/17/release/vc_redist.x64.exe
   - 32位系统：https://aka.ms/vs/17/release/vc_redist.x86.exe

2. **安装运行库**
   - 双击下载的 `vc_redist.x64.exe`（64位）或 `vc_redist.x86.exe`（32位）
   - 按照安装向导完成安装
   - 重启计算机

3. **验证安装**
   运行应用验证问题是否解决。

#### 方案2：使用预编译的PyQt6

如果方案1无效，尝试卸载并重新安装PyQt6：

```bash
pip uninstall PyQt6 PyQt6-Qt6 PyQt6_sip -y
pip install PyQt6 --no-cache-dir
```

#### 方案3：使用较新版本的PyQt6

```bash
pip uninstall PyQt6 PyQt6-Qt6 PyQt6_sip -y
pip install PyQt6==6.7.0
```

#### 方案4：使用虚拟环境

创建一个干净的虚拟环境：

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 运行应用
python main.py
```

### 快速诊断

运行以下命令检查问题：

```bash
python -c "import sys; print(f'Python: {sys.version}')"
python -c "import platform; print(f'系统: {platform.platform()}')"
python -c "import PyQt6; print(f'PyQt6: {PyQt6.QtCore.PYQT_VERSION_STR}')"
```

### 其他可能的解决方案

1. **更新pip**
```bash
python -m pip install --upgrade pip
```

2. **更新setuptools**
```bash
pip install --upgrade setuptools wheel
```

3. **检查系统PATH**
确保Python的Scripts目录在系统PATH中：
```
C:\Users\你的用户名\AppData\Local\Programs\Python\Python312\Scripts
```

### 如果问题仍然存在

请尝试以下操作：

1. 完全卸载Python和所有相关包
2. 重新安装Python 3.10或3.11（推荐3.11）
3. 安装Visual C++运行库
4. 重新安装项目依赖

### 临时解决方案：使用PyQt5

如果PyQt6问题无法解决，可以临时使用PyQt5：

```bash
pip uninstall PyQt6 PyQt6-Qt6 PyQt6_sip -y
pip install PyQt5
```

然后修改代码中的导入语句（将PyQt6改为PyQt5）。

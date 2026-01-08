# 翻译超时问题解决方案

## 问题说明

`翻译错误: The read operation timed out` 表示Google翻译API连接超时。

## 原因分析

### 1. 网络连接问题
- 无法连接到Google翻译服务器
- 网络速度慢或不稳定
- 防火墙或代理设置阻止连接

### 2. 国内网络环境
- Google服务在国内可能无法直接访问
- 需要代理或VPN才能使用

### 3. API限制
- Google翻译对频繁请求有限制
- 短时间内大量请求可能被拒绝

## 已实施的解决方案

### 1. 自动重试机制
```python
# 指数退避策略
wait_time = self.retry_delay * (2 ** retry_count) + random.uniform(0, 1)
```

- 第1次失败后等待2秒重试
- 第2次失败后等待4秒重试
- 第3次失败后等待8秒重试
- 最多重试3次

### 2. 延迟增加
- 批次之间延迟从1秒增加到2秒
- 避免触发API限流

### 3. 重新创建连接
- 每次重试时重新创建Translator实例
- 避免使用失效的连接

## 手动解决方案

### 方案1: 检查网络连接

1. 确认网络连接正常
2. 尝试访问 Google Translate 网页版
3. 如果无法访问，需要配置代理

### 方案2: 配置代理

如果需要使用代理，可以修改翻译器：

```python
# 在 core/translator.py 中修改
self.translator = Translator(proxies={
    'http': 'http://your-proxy:port',
    'https': 'https://your-proxy:port'
})
```

### 方案3: 使用VPN

1. 启动VPN或代理软件
2. 确保可以访问Google服务
3. 重新运行程序

### 方案4: 调整配置

如果网络较慢，可以增加重试次数和延迟时间：

编辑 `config.py`:

```python
# 增加重试次数
TRANSLATION_MAX_RETRIES = 5  # 默认3

# 增加重试延迟
TRANSLATION_RETRY_DELAY = 3  # 默认2

# 增加批次间延迟
TRANSLATION_DELAY = 2  # 默认1

# 减小批次大小
TRANSLATION_BATCH_SIZE = 5  # 默认10
```

### 方案5: 跳过翻译

如果翻译一直失败，可以临时跳过翻译：

```python
# 在 core/translator.py 的 translate_text 方法中
# 直接返回原文
return text
```

或者使用其他翻译服务（需要额外开发）

## 替代翻译方案

### 1. 使用百度翻译

需要注册百度翻译API：

```python
# 安装百度翻译SDK
pip install baidu-aip

from aip import AipTrans

APP_ID = 'your_app_id'
API_KEY = 'your_api_key'
SECRET_KEY = 'your_secret_key'

client = AipTrans(APP_ID, API_KEY, SECRET_KEY)
result = client.translate(text, from_lang='en', to_lang='zh')
```

### 2. 使用有道翻译

需要注册有道翻译API：

```python
import requests
import hashlib
import random

def youdao_translate(text):
    url = 'https://openapi.youdao.com/api'
    salt = str(random.randint(1, 65536))
    # 需要注册获取appKey和appSecret
    # ... 实现代码
```

### 3. 使用本地翻译模型

```python
# 使用opus-mt等本地模型
from transformers import pipeline

translator = pipeline('translation', model='Helsinki-NLP/opus-mt-en-zh')
result = translator(text)
```

优点：
- 无需网络
- 速度快
- 免费

缺点：
- 首次下载模型较大
- 翻译质量可能不如Google

## 测试网络连接

运行以下Python代码测试Google翻译连接：

```python
from googletrans import Translator

try:
    translator = Translator()
    result = translator.translate('Hello', src='en', dest='zh-CN')
    print(f"翻译成功: {result.text}")
except Exception as e:
    print(f"翻译失败: {e}")
```

## 建议的操作顺序

1. **首先**：检查网络连接，确认能访问Google
2. **然后**：如果网络正常但仍然超时，调整配置增加重试
3. **最后**：如果Google完全无法访问，考虑替代方案

## 临时解决方案

如果急需使用，可以暂时使用英文字幕：

1. 修改翻译器，直接返回原文
2. 或者使用已生成的英文字幕文件
3. 或者手动翻译重要片段

## 长期解决方案

建议：
1. 考虑集成多个翻译服务（Google、百度、有道）
2. 实现翻译服务自动切换
3. 支持本地翻译模型作为后备方案

"""
翻译连接测试脚本
用于测试Google翻译API是否可用
"""

import sys
import time
from googletrans import Translator


def test_translation():
    """测试翻译功能"""
    print("=" * 60)
    print("Google翻译连接测试")
    print("=" * 60)
    print()

    # 测试1: 简单翻译
    print("测试1: 简单翻译...")
    try:
        translator = Translator()
        result = translator.translate('Hello', src='en', dest='zh-CN')
        print(f"✓ 翻译成功: 'Hello' -> '{result.text}'")
    except Exception as e:
        print(f"✗ 翻译失败: {e}")
        return False

    print()

    # 测试2: 批量翻译
    print("测试2: 批量翻译...")
    test_texts = [
        "Hello world",
        "How are you?",
        "This is a test"
    ]

    success_count = 0
    for i, text in enumerate(test_texts, 1):
        try:
            translator = Translator()  # 每次重新创建实例
            result = translator.translate(text, src='en', dest='zh-CN')
            print(f"  {i}. '{text}' -> '{result.text}' ✓")
            success_count += 1
            time.sleep(0.5)  # 避免请求过快
        except Exception as e:
            print(f"  {i}. '{text}' -> 失败: {e} ✗")

    print()
    print(f"批量翻译结果: {success_count}/{len(test_texts)} 成功")

    print()

    # 测试3: 连续翻译（模拟实际使用）
    print("测试3: 连续翻译（10次）...")
    success_count = 0
    timeout_count = 0

    for i in range(10):
        try:
            translator = Translator()
            result = translator.translate(f'Test number {i+1}', src='en', dest='zh-CN')
            success_count += 1
            print(f"  {i+1}. ✓", end='')
            time.sleep(1)  # 模拟实际使用中的延迟
        except Exception as e:
            error_msg = str(e).lower()
            if 'timeout' in error_msg or 'timed out' in error_msg:
                timeout_count += 1
                print(f"  {i+1}. 超时 ✗", end='')
            else:
                print(f"  {i+1}. 失败 ✗", end='')

    print()
    print(f"连续翻译结果: {success_count}/10 成功, {timeout_count}/10 超时")

    print()
    print("=" * 60)

    # 判断结果
    if success_count >= 8:
        print("✓ 翻译服务正常")
        return True
    elif timeout_count >= 5:
        print("✗ 网络连接超时频繁")
        print("  建议: 检查网络连接或配置代理")
        return False
    else:
        print("⚠ 翻译服务不稳定")
        print("  建议: 增加重试次数和延迟时间")
        return False

    print("=" * 60)


if __name__ == "__main__":
    success = test_translation()

    print()
    if success:
        print("结论: Google翻译API可用，可以正常使用程序")
    else:
        print("结论: Google翻译API不可用或不稳定")
        print()
        print("建议:")
        print("1. 检查网络连接")
        print("2. 确认能否访问 translate.google.com")
        print("3. 如需代理，配置代理设置")
        print("4. 或者考虑使用其他翻译服务")

    input("\n按回车键退出...")

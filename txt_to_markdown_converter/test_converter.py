#!/usr/bin/env python3
"""
TXT to Markdown Converter Skill 测试脚本
测试各种格式化功能是否正常工作
"""

import os
import tempfile
import sys
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from txt_to_markdown_converter import TXTToMarkdownConverter


def test_title_formatting():
    """测试标题格式化功能"""
    print("🧪 测试标题格式化...")

    test_content = """概述
这是一个测试文档的概述部分

功能说明
这里有详细的功能列表

这是产品特性说明
包含多个产品特性

这是一行很长的内容，不应该被识别为标题因为它的长度超过了50个字符的限制，所以应该保持原样不添加标题标记。

结论
这是总结部分"""

    converter = TXTToMarkdownConverter()
    result = converter.convert_content(test_content)

    # 检查结果
    checks = [
        ("# 概述" in result, "一级标题格式化"),
        ("## 功能说明" in result, "二级标题格式化"),
        ("### 这是产品特性说明" in result, "三级标题格式化"),
        ("# 结论" in result, "关键词标题提升"),
        ("这是一行很长的内容" in result and "#" not in result, "长文本不被格式化为标题")
    ]

    all_passed = True
    for check, description in checks:
        if check:
            print(f"  ✅ {description}")
        else:
            print(f"  ❌ {description}")
            all_passed = False

    if all_passed:
        print("✅ 标题格式化测试通过")
        return True
    else:
        print("❌ 标题格式化测试失败")
        print("实际结果:")
        print(result)
        return False


def test_list_formatting():
    """测试列表格式化功能"""
    print("🧪 测试列表格式化...")

    test_content = """功能列表：
1. 自动识别格式
2. 智能处理内容
3. 优化文档结构

项目符号列表：
- 格式化文本
* 优化结构
• 提升可读性

中文数字列表：
一、第一项内容
二、第二项内容
三、第三项内容"""

    converter = TXTToMarkdownConverter()
    result = converter.convert_content(test_content)

    # 检查结果
    checks = [
        ("1. 自动识别格式" in result, "数字列表保持"),
        ("- 格式化文本" in result, "符号列表格式化"),
        ("1. 第一项内容" in result, "中文数字转换"),
        ("2. 第二项内容" in result, "中文数字转换2"),
        ("3. 第三项内容" in result, "中文数字转换3")
    ]

    all_passed = True
    for check, description in checks:
        if check:
            print(f"  ✅ {description}")
        else:
            print(f"  ❌ {description}")
            all_passed = False

    if all_passed:
        print("✅ 列表格式化测试通过")
        return True
    else:
        print("❌ 列表格式化测试失败")
        print("实际结果:")
        print(result)
        return False


def test_table_formatting():
    """测试表格格式化功能"""
    print("🧪 测试表格格式化...")

    test_content = """空格分隔表格：
姓名    年龄    城市
张三    25     北京
李四    30     上海

制表符表格：
姓名	年龄	城市
王五	28	广州
赵六	35	深圳"""

    converter = TXTToMarkdownConverter()
    result = converter.convert_content(test_content)

    # 检查结果
    checks = [
        ("姓名 | 年龄 | 城市" in result, "空格分隔表格格式化"),
        ("张三 | 25 | 北京" in result, "空格分隔内容格式化"),
        ("王五 | 28 | 广州" in result, "制表符表格格式化"),
        ("赵六 | 35 | 深圳" in result, "制表符表格内容格式化")
    ]

    all_passed = True
    for check, description in checks:
        if check:
            print(f"  ✅ {description}")
        else:
            print(f"  ❌ {description}")
            all_passed = False

    if all_passed:
        print("✅ 表格格式化测试通过")
        return True
    else:
        print("❌ 表格格式化测试失败")
        print("实际结果:")
        print(result)
        return False


def test_link_formatting():
    """测试链接格式化功能"""
    print("🧪 测试链接格式化...")

    test_content = """访问 https://www.example.com 获取更多信息
或者查看 www.documentation.com 了解文档
官网：http://localhost:8080
GitHub仓库：https://github.com/user/repo"""

    converter = TXTToMarkdownConverter()
    result = converter.convert_content(test_content)

    # 检查结果
    checks = [
        ("[https://www.example.com](https://www.example.com)" in result, "HTTPS链接格式化"),
        ("[www.documentation.com](https://www.documentation.com)" in result, "WWW链接格式化"),
        ("[http://localhost:8080](http://localhost:8080)" in result, "HTTP链接格式化"),
        ("[https://github.com/user/repo](https://github.com/user/repo)" in result, "GitHub链接格式化")
    ]

    all_passed = True
    for check, description in checks:
        if check:
            print(f"  ✅ {description}")
        else:
            print(f"  ❌ {description}")
            all_passed = False

    if all_passed:
        print("✅ 链接格式化测试通过")
        return True
    else:
        print("❌ 链接格式化测试失败")
        print("实际结果:")
        print(result)
        return False


def test_keyword_highlighting():
    """测试关键词高亮功能"""
    print("🧪 测试关键词高亮...")

    test_content = """使用 API 接口调用 HTTP 协议传输 JSON 数据
重要的功能包括核心算法和主要参数
必须注意安全性和性能问题
使用Python编程语言连接数据库"""

    converter = TXTToMarkdownConverter()
    result = converter.convert_content(test_content)

    # 检查结果
    checks = [
        ("`API`" in result, "API关键词高亮"),
        ("`HTTP`" in result, "HTTP关键词高亮"),
        ("`JSON`" in result, "JSON关键词高亮"),
        ("`Python`" in result, "Python关键词高亮"),
        ("`数据库`" in result, "中文关键词高亮"),
        ("**重要**" in result, "重要词汇强调"),
        ("**必须**" in result, "必须词汇强调")
    ]

    all_passed = True
    for check, description in checks:
        if check:
            print(f"  ✅ {description}")
        else:
            print(f"  ❌ {description}")
            all_passed = False

    if all_passed:
        print("✅ 关键词高亮测试通过")
        return True
    else:
        print("❌ 关键词高亮测试失败")
        print("实际结果:")
        print(result)
        return False


def test_code_protection():
    """测试代码块保护功能"""
    print("🧪 测试代码块保护...")

    test_content = """以下是代码示例：
```python
def hello_world():
    print("Hello, World")
    return True
```

这段代码应该保持原样不被格式化。

另外一段代码：
~~~javascript
function greet(name) {
    return `Hello, ${name}!`;
}
~~~

代码块内的内容不应该被格式化。"""

    converter = TXTToMarkdownConverter()
    result = converter.convert_content(test_content)

    # 检查代码块保护
    checks = [
        ("```python" in result, "Python代码块标记保持"),
        ("def hello_world():" in result, "Python代码内容保持"),
        ("~~~javascript" in result, "JavaScript代码块标记保持"),
        ("function greet(name)" in result, "JavaScript代码内容保持"),
        ("return `Hello, ${name}!`;" in result, "模板字符串保持")
    ]

    all_passed = True
    for check, description in checks:
        if check:
            print(f"  ✅ {description}")
        else:
            print(f"  ❌ {description}")
            all_passed = False

    if all_passed:
        print("✅ 代码块保护测试通过")
        return True
    else:
        print("❌ 代码块保护测试失败")
        print("实际结果:")
        print(result)
        return False


def test_file_operations():
    """测试文件操作功能"""
    print("🧪 测试文件操作...")

    test_content = """# 测试文档
这是一个测试文件

## 功能列表
1. 功能一
2. 功能二

### 技术栈
- Python
- Markdown

访问 https://example.com 了解更多"""

    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
        f.write(test_content)
        temp_file = f.name

    try:
        converter = TXTToMarkdownConverter()
        result_path = converter.convert_file(temp_file)

        # 检查输出文件是否存在
        if os.path.exists(result_path):
            # 检查文件内容
            with open(result_path, 'r', encoding='utf-8') as f:
                result_content = f.read()

            checks = [
                ("# 测试文档" in result_content, "标题保持"),
                ("1. 功能一" in result_content, "列表格式化"),
                ("- Python" in result_content, "符号列表"),
                ("[https://example.com]" in result_content, "链接格式化"),
                (result_path.endswith('.md'), "输出文件扩展名正确")
            ]

            all_passed = True
            for check, description in checks:
                if check:
                    print(f"  ✅ {description}")
                else:
                    print(f"  ❌ {description}")
                    all_passed = False

            if all_passed:
                print("✅ 文件操作测试通过")
                return True
            else:
                print("❌ 文件操作测试失败")
                print("实际结果:")
                print(result_content)
                return False
        else:
            print("  ❌ 输出文件不存在")
            return False

    finally:
        # 清理临时文件
        if os.path.exists(temp_file):
            os.unlink(temp_file)
        if 'result_path' in locals() and os.path.exists(result_path):
            os.unlink(result_path)


def test_complex_document():
    """测试复杂文档的综合格式化"""
    print("🧪 测试复杂文档综合格式化...")

    test_content = """项目概述
这是一个智能文档处理工具，能够自动识别和格式化各种内容。

主要功能
1. 智能标题识别
2. 列表格式化
3. 表格处理
4. 链接转换

技术实现
使用Python语言开发，支持多种编码格式。
核心算法包括：
- 文本模式识别
- 结构分析
- 格式推断

API接口
工具提供RESTful API接口：
http://localhost:8080/api/v1/format

配置示例
参数    值    说明
encoding    utf-8    文件编码
output    markdown    输出格式
backup    true    备份原文件

注意事项
重要：使用前请备份重要文件
必须确保有足够的磁盘空间
建议先在小文件上测试

代码示例
```python
def format_document(input_file):
    converter = TXTToMarkdownConverter()
    return converter.convert_file(input_file)
```

更多信息请访问 www.documentation.com"""

    converter = TXTToMarkdownConverter()
    result = converter.convert_content(test_content)

    # 检查综合格式化结果
    checks = [
        ("# 项目概述" in result, "项目概述标题"),
        ("## 主要功能" in result, "主要功能标题"),
        ("1. 智能标题识别" in result, "数字列表"),
        ("- 文本模式识别" in result, "符号列表"),
        ("参数 | 值 | 说明" in result, "表格格式化"),
        ("[http://localhost:8080/api/v1/format]" in result, "API链接"),
        ("`Python`" in result, "技术关键词"),
        ("**重要**" in result, "强调文本"),
        ("[www.documentation.com](https://www.documentation.com)" in result, "WWW链接"),
        ("```python" in result and "def format_document" in result, "代码块保护")
    ]

    all_passed = True
    for check, description in checks:
        if check:
            print(f"  ✅ {description}")
        else:
            print(f"  ❌ {description}")
            all_passed = False

    if all_passed:
        print("✅ 复杂文档综合格式化测试通过")
        return True
    else:
        print("❌ 复杂文档综合格式化测试失败")
        print("实际结果:")
        print(result)
        return False


def run_all_tests():
    """运行所有测试"""
    print("🚀 开始运行 TXT to Markdown Converter Skill 测试套件\n")

    tests = [
        test_title_formatting,
        test_list_formatting,
        test_table_formatting,
        test_link_formatting,
        test_keyword_highlighting,
        test_code_protection,
        test_file_operations,
        test_complex_document,
    ]

    passed = 0
    total = len(tests)

    for test_func in tests:
        try:
            if test_func():
                passed += 1
            print()  # 空行分隔
        except Exception as e:
            print(f"❌ 测试异常: {e}\n")

    print("=" * 60)
    print(f"📊 测试结果: {passed}/{total} 通过")

    if passed == total:
        print("🎉 所有测试通过！TXT to Markdown Converter Skill 运行正常。")
    else:
        print("⚠️  部分测试失败，请检查相关功能。")

    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
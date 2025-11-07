#!/usr/bin/env python3
"""
TXT to Markdown Converter Skill 演示脚本
快速演示skill的主要功能
"""

import os
import sys
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from txt_to_markdown_converter import TXTToMarkdownConverter


def demo_basic_functionality():
    """演示基本功能"""
    print("🚀 TXT to Markdown Converter Skill 功能演示")
    print("=" * 50)

    # 演示文本
    demo_text = """演示文档
这是一个功能演示文本

主要特性
1. 智能标题识别
2. 列表格式化
- 支持中文数字转换
* 统一列表符号

技术信息
使用Python语言开发
支持HTTP协议传输JSON数据

访问 https://demo.example.com 了解更多
"""

    print("📝 原始文本:")
    print("-" * 30)
    print(demo_text)
    print("-" * 30)

    # 转换
    converter = TXTToMarkdownConverter()
    result = converter.convert_content(demo_text)

    print("\n✨ 转换后的Markdown:")
    print("-" * 30)
    print(result)
    print("-" * 30)

    print("\n🎯 主要改进:")
    print("  ✅ 智能标题识别和分级")
    print("  ✅ 列表格式标准化")
    print("  ✅ 技术关键词高亮")
    print("  ✅ 链接自动转换")
    print("  ✅ 结构层次清晰化")


def demo_file_processing():
    """演示文件处理功能"""
    print("\n📁 文件处理演示")
    print("=" * 50)

    # 检查示例文件
    example_file = "example_input.txt"
    if os.path.exists(example_file):
        print(f"🔍 处理示例文件: {example_file}")

        converter = TXTToMarkdownConverter()
        output_path = converter.convert_file(example_file)

        print(f"✅ 转换完成!")
        print(f"📂 输入文件: {example_file}")
        print(f"📂 输出文件: {output_path}")

        # 显示文件大小对比
        input_size = os.path.getsize(example_file)
        output_size = os.path.getsize(output_path)

        print(f"📊 文件大小: {input_size} -> {output_size} 字节")

        if os.path.exists(output_path):
            print("✅ 输出文件已生成，可以查看转换效果！")
    else:
        print(f"❌ 示例文件 {example_file} 不存在")


def demo_customization():
    """演示自定义配置"""
    print("\n⚙️ 自定义配置演示")
    print("=" * 50)

    # 创建自定义配置
    custom_config = {
        'formatting_rules': {
            'headings': {
                'keywords': ['演示', '功能', '信息']  # 自定义标题关键词
            },
            'emphasis': {
                'important_words': {
                    'chinese': ['重要', '关键', '注意'],
                    'english': ['important', 'key', 'critical']
                }  # 自定义重要词汇
            },
            'keywords': {
                'highlight_tech_terms': True,
                'tech_keywords': {
                    'programming': ['Python', 'HTTP', 'JSON', '演示', '配置']
                }
            }
        }
    }

    demo_text = """演示文档
这是一个重要演示
包含关键配置信息
使用Python和JSON格式"""

    print("📝 使用自定义配置转换:")

    # 使用自定义配置
    converter = TXTToMarkdownConverter()
    converter.config.update(custom_config)

    result = converter.convert_content(demo_text)

    print("-" * 30)
    print(result)
    print("-" * 30)

    print("🎯 自定义效果:")
    print("  ✅ 标题关键词自定义")
    print("  ✅ 重要词汇自定义")
    print("  ✅ 技术关键词自定义")


def main():
    """主演示函数"""
    try:
        demo_basic_functionality()
        demo_file_processing()
        demo_customization()

        print("\n🎉 演示完成!")
        print("=" * 50)
        print("📚 更多信息请查看:")
        print("  - README.md: 详细文档")
        print("  - 使用说明.md: 中文使用指南")
        print("  - test_converter.py: 运行测试")
        print("  - example_input.txt: 示例输入文件")

    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
# TXT to Markdown Converter Skill

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Type](https://img.shields.io/badge/type-Claude_Skill-orange.svg)](#)

一个智能的TXT文件到Markdown格式转换器，能够自动识别文档结构并添加适当的Markdown格式化，提升文档的可读性和专业性。

## ✨ 主要功能

### 🎯 智能标题识别
- 自动检测标题行并添加适当的标题级别
- 支持中英文标题关键词识别
- 根据行长度和上下文智能判断标题级别

### 📝 列表格式化
- 自动识别并格式化有序列表和无序列表
- 支持中文数字转换为阿拉伯数字
- 统一列表符号格式

### 📊 表格处理
- 智能识别表格结构（制表符分隔或多空格分隔）
- 自动转换为标准Markdown表格格式
- 支持不规则表格的智能修复

### 🔗 链接格式化
- 自动识别HTTP/HTTPS链接并转换为Markdown链接格式
- 支持WWW链接自动补全协议
- 智能识别多种URL模式

### 💡 关键词高亮
- 技术术语自动添加代码高亮
- 重要词汇自动强调显示
- 支持自定义关键词列表

### 🛡️ 代码块保护
- 智能识别代码块并保持原格式
- 支持多种代码块标记语法
- 防止代码内容被错误格式化

## 🚀 快速开始

### 安装依赖

```bash
pip install pyyaml
```

### 基本使用

```bash
# 转换单个文件
python txt_to_markdown_converter.py input.txt

# 指定输出文件
python txt_to_markdown_converter.py input.txt -o output.md

# 原地转换（修改原文件）
python txt_to_markdown_converter.py input.txt --inplace

# 使用自定义配置
python txt_to_markdown_converter.py input.txt -c config.yaml

# 详细输出模式
python txt_to_markdown_converter.py input.txt -v
```

### Python API使用

```python
from txt_to_markdown_converter import TXTToMarkdownConverter

# 使用默认配置
converter = TXTToMarkdownConverter()
result = converter.convert_file("input.txt", "output.md")

# 使用自定义配置
converter = TXTToMarkdownConverter("config.yaml")
markdown_content = converter.convert_content(text_content)

# 原地转换
converter.convert_file("input.txt", "input.txt")
```

## 📋 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `input_file` | 输入的TXT文件路径 | 必需 |
| `-o, --output` | 输出文件路径 | 自动生成 |
| `-c, --config` | 配置文件路径 | 使用默认配置 |
| `--inplace` | 原地修改文件 | False |
| `-v, --verbose` | 详细输出模式 | False |

## ⚙️ 配置选项

### 配置文件结构

```yaml
# 技能信息
skill_info:
  name: "txt_to_markdown_converter"
  version: "1.0.0"
  description: "智能TXT转Markdown转换器"

# 文件处理设置
file_handling:
  supported_extensions: [".txt", ".text", ".log"]
  backup_original: true
  encoding: ["utf-8", "gbk", "gb2312"]
  output:
    suffix: "_formatted"
    extension: ".md"

# 格式化规则
formatting_rules:
  headings:
    auto_detect: true
    max_level: 6
    keywords: ["概述", "介绍", "总结", "功能", "特性"]

  lists:
    auto_detect: true
    convert_chinese_numbers: true
    unify_symbols: true

  tables:
    auto_detect: true
    min_columns: 2
    separator: " | "

  links:
    auto_format_urls: true
    add_brackets: true

  emphasis:
    auto_emphasize: true
    important_words: ["重要", "关键", "核心"]

  keywords:
    highlight_tech_terms: true
    tech_keywords:
      programming: ["API", "HTTP", "JSON", "Python"]
```

### 主要配置说明

#### 标题设置 (`headings`)
- `auto_detect`: 是否自动检测标题
- `max_level`: 最大标题级别（1-6）
- `keywords`: 标题关键词列表，包含这些词的行会被优先识别为标题

#### 列表设置 (`lists`)
- `auto_detect`: 是否自动检测列表
- `convert_chinese_numbers`: 是否转换中文数字为阿拉伯数字
- `unify_symbols`: 是否统一列表符号格式

#### 表格设置 (`tables`)
- `auto_detect`: 是否自动检测表格
- `min_columns`: 最小列数要求
- `separator`: 表格分隔符

## 🧪 测试

运行测试套件：

```bash
python test_converter.py
```

测试覆盖以下功能：
- ✅ 标题格式化
- ✅ 列表格式化
- ✅ 表格格式化
- ✅ 链接格式化
- ✅ 关键词高亮
- ✅ 代码块保护
- ✅ 文件操作
- ✅ 综合文档处理

## 📝 使用示例

### 输入文件 (example_input.txt)

```
项目概述
这是一个智能文档处理工具

主要功能
1. 智能标题识别
2. 列表格式化
- 格式化文本
* 优化结构

配置示例
参数    值    说明
encoding    utf-8    文件编码
output    markdown    输出格式

访问 https://example.com 了解更多
```

### 输出文件 (example_input_formatted.md)

```markdown
# 项目概述
这是一个智能文档处理工具

## 主要功能
1. 智能标题识别
2. 列表格式化
- 格式化文本
- 优化结构

### 配置示例
参数 | 值 | 说明
encoding | utf-8 | 文件编码
output | markdown | 输出格式

访问 [https://example.com](https://example.com) 了解更多
```

## 🔧 高级功能

### 批量处理

```python
import glob
from txt_to_markdown_converter import TXTToMarkdownConverter

converter = TXTToMarkdownConverter()

# 批量转换目录中的所有TXT文件
for txt_file in glob.glob("*.txt"):
    output_file = txt_file.replace('.txt', '.md')
    converter.convert_file(txt_file, output_file)
    print(f"转换完成: {txt_file} -> {output_file}")
```

### 自定义格式化规则

```python
from txt_to_markdown_converter import TXTToMarkdownConverter

# 创建自定义配置
custom_config = {
    'formatting_rules': {
        'headings': {
            'keywords': ['自定义标题关键词']
        },
        'emphasis': {
            'important_words': ['自定义', '重要', '词汇']
        }
    }
}

converter = TXTToMarkdownConverter()
converter.config.update(custom_config)
```

## 🐛 故障排除

### 常见问题

1. **编码错误**
   ```
   错误: UnicodeDecodeError
   解决: 确保文件编码为UTF-8，或在配置中添加其他编码格式
   ```

2. **代码块被错误格式化**
   ```
   问题: 代码内容被添加了不必要的格式
   解决: 确保代码块使用正确的标记（```或~~~）
   ```

3. **标题识别不准确**
   ```
   问题: 普通文本被识别为标题
   解决: 调整配置中的标题检测参数，如max_length
   ```

### 调试模式

```bash
# 启用详细输出查看处理过程
python txt_to_markdown_converter.py input.txt -v
```

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 📞 支持

如有问题或建议，请：
1. 查看文档和FAQ
2. 搜索已有的Issues
3. 创建新的Issue描述问题

---

**享受清晰的文档格式化体验！** 📚✨
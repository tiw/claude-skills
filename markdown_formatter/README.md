# Markdown 格式化技能

这是一个专门用于将 txt 文件格式化为 markdown 格式的 Claude 技能。

## 功能特性

- 🎯 **智能识别**: 自动识别文本结构类型
- 📝 **格式转换**: 将 txt 文件转换为清晰的 markdown 格式
- 🔧 **多种规则**: 支持标题、列表、代码块、链接等多种格式化规则
- 📋 **模板支持**: 提供常用的文档模板

## 技能组件

### 核心脚本
- `scripts/format_txt_to_md.py` - 主要的格式化脚本

### 格式化规则
- `references/formatting_rules.md` - 详细的格式化规则和最佳实践

### 模板文件
- `assets/templates/tech_doc_template.md` - 技术文档模板
- `assets/templates/note_template.md` - 笔记文档模板
- `assets/templates/readme_template.md` - README 文档模板

## 使用方法

当用户有以下请求时，技能会自动触发：
- "把这个txt文件转换为markdown"
- "格式化我的文本文件"
- "将这个文件转为markdown格式"
- "改善文档结构和可读性"

### 手动使用格式化脚本

```bash
# 格式化单个文件
python3 scripts/format_txt_to_md.py input.txt

# 指定输出文件
python3 scripts/format_txt_to_md.py input.txt output.md
```

## 支持的格式化功能

### 标题识别
- 自动识别全大写标题并转换为 `# 标题`
- 识别带冒号的标题并转换为 `## 标题:`

### 列表转换
- 支持各种符号列表 (•, -, *, +, ○, ▪, ▫)
- 保持有序列表格式 (1., 2., 3.)
- 支持嵌套列表

### 代码块处理
- 自动识别缩进代码块
- 添加 ``` 围栏格式
- 保持代码格式不变

### 链接和强调
- 自动转换 URL 为 markdown 链接
- 识别邮箱地址并添加 mailto 链接

## 示例

### 输入 (txt)
```
INTRODUCTION

This is a sample document.

FEATURES
• Easy to use
• Fast processing
• Reliable output

CODE EXAMPLE
    def hello():
        print("Hello")
```

### 输出 (markdown)
```markdown
# INTRODUCTION

This is a sample document.

# FEATURES

- Easy to use
- Fast processing
- Reliable output

# CODE EXAMPLE

```
    def hello():
        print("Hello")
```
```

## 安装和设置

1. 将技能文件夹放置在合适的目录
2. 确保 Python 3.6+ 可用
3. 给脚本添加执行权限：
   ```bash
   chmod +x scripts/format_txt_to_md.py
   ```

## 注意事项

- 格式化会保持原始内容的完整性
- 优先使用简单的 markdown 语法
- 对于复杂结构会提供清晰的注释
- 建议在格式化后检查结果是否符合预期
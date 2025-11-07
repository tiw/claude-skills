# TXT 到 Markdown 格式化规则

## 1. 标题识别规则

### 1.1 一级标题 (#)
- 全大写的单行文本
- 长度适中（通常小于 50 字符）
- 不包含句号等结束标点

**示例：**
```
INTRODUCTION
```
转换为：
```
# INTRODUCTION
```

### 1.2 二级标题 (##)
- 首字母大写的行
- 以冒号或句号结尾
- 独立成行的短语

**示例：**
```
Installation Guide:
```
转换为：
```
## Installation Guide
```

### 1.3 三级标题 (###)
- 缩进的标题行
- 带编号的小节标题

## 2. 列表识别规则

### 2.1 无序列表 (-)
- 以 -、*、+、•、○、▪、▫ 开头的行
- 连续的相似格式行

**示例：**
```
• First item
• Second item
• Third item
```
转换为：
```
- First item
- Second item
- Third item
```

### 2.2 有序列表 (1. 2. 3.)
- 以数字加点开头的行
- 连续编号的项目

**示例：**
```
1. Setup environment
2. Install dependencies
3. Run tests
```
保持原样（已经是 markdown 格式）

### 2.3 嵌套列表
- 通过缩进识别嵌套层级
- 每级缩进 2 个空格

## 3. 代码块识别规则

### 3.1 缩进代码块
- 连续 4 个空格或制表符开头的行
- 程序代码、配置文件内容

**示例：**
```
    def hello():
        print("Hello, World!")
```
转换为：
```
```
def hello():
    print("Hello, World!")
```
```

### 3.2 围栏代码块 (```)
- 以 ``` 或 ~~~ 开始和结束的块
- 可指定语言类型

## 4. 表格识别规则

### 4.1 管道表格
- 包含 | 分隔符的行
- 连续的类似结构行

**示例：**
```
Name | Age | City
John | 25 | New York
Jane | 30 | London
```
保持原样（已经是 markdown 格式）

## 5. 强调和链接规则

### 5.1 强调文本
- 包含在 *asterisks* 中的文本
- 包含在 **double asterisks** 中的文本

### 5.2 行内代码
- 包含在 `backticks` 中的文本
- 变量名、文件名、命令等

### 5.3 链接
- 自动识别 HTTP/HTTPS URL
- 自动识别邮箱地址

**示例：**
```
Visit https://example.com for more info.
Contact admin@example.com
```
转换为：
```
Visit [https://example.com](https://example.com) for more info.
Contact [admin@example.com](mailto:admin@example.com)
```

## 6. 段落和空行规则

### 6.1 段落分离
- 空行用于分隔段落
- 避免连续的多个空行
- 标题前后添加空行

### 6.2 行尾处理
- 移除行尾多余空格
- 保持适当的行长度

## 7. 特殊情况处理

### 7.1 保留格式
- 已经是 markdown 格式的内容保持不变
- 特殊符号和格式需要转义

### 7.2 语义保持
- 格式化不能改变原文的语义
- 保留所有原始信息

### 7.3 兼容性
- 生成标准的 markdown 语法
- 兼容常见的 markdown 渲染器

## 8. 质量检查

### 8.1 格式验证
- 检查 markdown 语法正确性
- 验证链接有效性

### 8.2 可读性检查
- 确保文档结构清晰
- 验证标题层级合理

### 8.3 完整性验证
- 确保没有丢失内容
- 验证格式化的一致性
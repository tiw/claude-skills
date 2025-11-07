#!/usr/bin/env python3
"""
TXT to Markdown 格式化工具
智能识别文本结构并转换为 markdown 格式
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple, Optional

class TxtToMarkdownFormatter:
    def __init__(self):
        self.rules = {
            'headers': [
                (r'^([A-Z]{2,})\s*$', r'# \1'),  # 全大写且较短的标题
                (r'^([A-Z][A-Za-z\s]+[.:])\s*$', r'## \1'),  # 带标点的标题
            ],
            'lists': [
                (r'^(\s*)[-*+]\s+(.+)$', r'\1- \2'),  # 无序列表
                (r'^(\s*)(\d+)\.\s+(.+)$', r'\1\2. \3'),  # 有序列表
                (r'^(\s*)([•○▪▫])\s+(.+)$', r'\1- \3'),  # 其他符号列表
            ],
            'code_blocks': [
                (r'^( {4}|\t)(.+)$', r'    \2'),  # 缩进代码块
            ],
            'emphasis': [
                (r'\*([^*\n]+)\*', r'*\1*'),  # 斜体
                (r'\*\*([^*\n]+)\*\*', r'**\1**'),  # 粗体
                (r'`([^`\n]+)`', r'`\1`'),  # 行内代码
            ],
            'links': [
                (r'(https?://[^\s]+)', r'[\1](\1)'),  # URL 链接
                (r'(\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b)', r'[\1](mailto:\1)'),  # 邮箱
            ],
        }

    def detect_structure(self, lines: List[str]) -> List[str]:
        """检测文本结构并应用相应的格式化规则"""
        formatted_lines = []
        i = 0

        while i < len(lines):
            line = lines[i].rstrip()
            next_line = lines[i + 1].rstrip() if i + 1 < len(lines) else ""

            # 跳过空行
            if not line.strip():
                formatted_lines.append("")
                i += 1
                continue

            # 检测并处理代码块
            if self._is_code_block(line, lines, i):
                code_lines = self._extract_code_block(lines, i)
                formatted_lines.extend(code_lines)
                i += len(code_lines)
                continue

            # 检测并处理表格
            if self._is_table_line(line):
                table_lines = self._extract_table(lines, i)
                formatted_lines.extend(table_lines)
                i += len(table_lines)
                continue

            # 应用标题格式化
            formatted_line = self._apply_header_formatting(line)

            # 应用列表格式化
            if not self._is_header(formatted_line):
                formatted_line = self._apply_list_formatting(formatted_line)

            # 应用其他格式化
            formatted_line = self._apply_emphasis_formatting(formatted_line)
            formatted_line = self._apply_link_formatting(formatted_line)

            formatted_lines.append(formatted_line)
            i += 1

        return formatted_lines

    def _is_code_block(self, line: str, lines: List[str], index: int) -> bool:
        """检测是否为代码块开始"""
        stripped = line.lstrip()
        if stripped.startswith(('```', '~~~')):
            return True

        # 检测连续的缩进行
        if line.startswith('    ') or line.startswith('\t'):
            return True

        # 检测接下来的行是否也是缩进
        if index + 1 < len(lines):
            next_line = lines[index + 1]
            if (next_line.startswith('    ') or next_line.startswith('\t')) and next_line.strip():
                return True

        return False

    def _extract_code_block(self, lines: List[str], start_index: int) -> List[str]:
        """提取代码块"""
        code_lines = []
        i = start_index

        # 检测代码块类型
        line = lines[i]
        if line.startswith('```') or line.startswith('~~~'):
            # fenced code block
            fence = line[:3]
            code_lines.append(line)
            i += 1

            while i < len(lines) and not lines[i].startswith(fence):
                code_lines.append(lines[i])
                i += 1

            if i < len(lines):
                code_lines.append(lines[i])
                i += 1
        else:
            # 缩进代码块
            code_lines.append('```')
            while i < len(lines) and (lines[i].startswith('    ') or lines[i].startswith('\t') or not lines[i].strip()):
                if lines[i].strip():
                    code_lines.append(lines[i].rstrip())
                else:
                    code_lines.append('')
                i += 1
            code_lines.append('```')

        return code_lines

    def _is_table_line(self, line: str) -> bool:
        """检测是否为表格行"""
        # 简单的表格检测：包含多个由 | 分隔的列
        if '|' not in line:
            return False

        parts = [p.strip() for p in line.split('|') if p.strip()]
        return len(parts) >= 2

    def _extract_table(self, lines: List[str], start_index: int) -> List[str]:
        """提取表格"""
        table_lines = []
        i = start_index

        while i < len(lines) and self._is_table_line(lines[i]):
            table_lines.append(lines[i].rstrip())
            i += 1

        return table_lines

    def _apply_header_formatting(self, line: str) -> str:
        """应用标题格式化"""
        # 只对全大写的简短行应用标题格式
        stripped = line.strip()
        if stripped.isupper() and len(stripped) < 50 and ' ' not in stripped or stripped.count(' ') <= 3:
            if all(c.isupper() or c.isspace() for c in stripped):
                return f"# {stripped}"

        # 检测带冒号的标题
        if stripped.endswith(':') and len(stripped) < 60:
            # 检查是否是标题（包含常见标题关键词）
            title_keywords = ['INTRODUCTION', 'INSTALLATION', 'USAGE', 'CONCLUSION', 'OVERVIEW', 'DESCRIPTION']
            for keyword in title_keywords:
                if keyword in stripped.upper():
                    return f"## {stripped}"

        return line

    def _is_header(self, line: str) -> bool:
        """检测是否为标题行"""
        return line.strip().startswith('#')

    def _apply_list_formatting(self, line: str) -> str:
        """应用列表格式化"""
        for pattern, replacement in self.rules['lists']:
            if re.match(pattern, line):
                return re.sub(pattern, replacement, line)
        return line

    def _apply_emphasis_formatting(self, line: str) -> str:
        """应用强调格式化"""
        for pattern, replacement in self.rules['emphasis']:
            line = re.sub(pattern, replacement, line)
        return line

    def _apply_link_formatting(self, line: str) -> str:
        """应用链接格式化"""
        for pattern, replacement in self.rules['links']:
            line = re.sub(pattern, replacement, line)
        return line

    def format_text(self, text: str) -> str:
        """格式化文本内容"""
        lines = text.split('\n')
        formatted_lines = self.detect_structure(lines)

        # 清理多余的空行
        cleaned_lines = []
        prev_empty = False

        for line in formatted_lines:
            if line.strip() == "":
                if not prev_empty:
                    cleaned_lines.append("")
                prev_empty = True
            else:
                cleaned_lines.append(line)
                prev_empty = False

        return '\n'.join(cleaned_lines)

    def format_file(self, input_path: str, output_path: Optional[str] = None) -> str:
        """格式化文件"""
        input_file = Path(input_path)

        if not input_file.exists():
            raise FileNotFoundError(f"输入文件不存在: {input_path}")

        # 读取输入文件
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 格式化内容
        formatted_content = self.format_text(content)

        # 确定输出路径
        if output_path is None:
            output_path = input_file.with_suffix('.md')
        else:
            output_path = Path(output_path)

        # 写入输出文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted_content)

        return str(output_path)

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python format_txt_to_md.py <输入文件> [输出文件]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    formatter = TxtToMarkdownFormatter()

    try:
        result_path = formatter.format_file(input_file, output_file)
        print(f"格式化完成: {result_path}")
    except Exception as e:
        print(f"格式化失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
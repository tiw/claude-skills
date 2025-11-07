#!/usr/bin/env python3
"""
TXT to Markdown Converter Skill
智能将TXT文件转换为格式化的Markdown文档

Author: AI Assistant
Version: 1.0.0
Description: 读取TXT文件，智能分析内容结构，自动添加Markdown格式化，
             保持原文内容不变，仅添加格式化来提升可读性和结构清晰度。
"""

import re
import sys
import argparse
import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import logging


class TXTToMarkdownConverter:
    """TXT转Markdown智能转换器"""

    def __init__(self, config_path: Optional[str] = None):
        """
        初始化转换器

        Args:
            config_path: 配置文件路径，如果为None则使用默认配置
        """
        self.config = self._load_config(config_path)
        self.lines = []
        self.formatted_lines = []
        self._setup_logging()

    def _setup_logging(self):
        """设置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """
        加载配置文件

        Args:
            config_path: 配置文件路径

        Returns:
            配置字典
        """
        if config_path is None:
            # 默认配置
            return {
                'formatting_rules': {
                    'headings': {
                        'auto_detect': True,
                        'max_level': 6,
                        'keywords': ['概述', '介绍', '总结', '结论', '功能', '特性']
                    },
                    'lists': {'auto_detect': True, 'convert_chinese_numbers': True},
                    'tables': {'auto_detect': True, 'min_columns': 2},
                    'links': {'auto_format_urls': True},
                    'emphasis': {'auto_emphasize': True},
                    'keywords': {'highlight_tech_terms': True}
                },
                'file_handling': {
                    'encoding': ['utf-8', 'gbk', 'gb2312'],
                    'output': {'suffix': '_formatted', 'extension': '.md'}
                }
            }

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.logger.warning(f"无法加载配置文件 {config_path}: {e}")
            return self._load_config(None)

    def convert_file(self, input_path: str, output_path: Optional[str] = None) -> str:
        """
        转换文件为Markdown格式

        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径，如果为None则自动生成

        Returns:
            输出文件路径
        """
        try:
            content = self._read_file(input_path)
            formatted_content = self.convert_content(content)

            if output_path is None:
                output_path = self._generate_output_path(input_path)

            self._write_file(output_path, formatted_content)
            self.logger.info(f"转换完成: {input_path} -> {output_path}")

            return output_path

        except Exception as e:
            self.logger.error(f"转换文件失败: {e}")
            raise

    def convert_content(self, content: str) -> str:
        """
        转换文本内容为Markdown格式

        Args:
            content: 原始文本内容

        Returns:
            格式化后的Markdown内容
        """
        self.lines = content.split('\n')
        self.formatted_lines = []

        i = 0
        while i < len(self.lines):
            line = self.lines[i]
            formatted_line = self._process_line(line, i)
            self.formatted_lines.append(formatted_line)
            i += 1

        return '\n'.join(self.formatted_lines)

    def _read_file(self, file_path: str) -> str:
        """读取文件内容"""
        encodings = self.config.get('file_handling', {}).get('encoding', ['utf-8'])

        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue

        raise ValueError(f"无法使用指定编码读取文件: {encodings}")

    def _write_file(self, file_path: str, content: str) -> None:
        """写入文件内容"""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def _generate_output_path(self, input_path: str) -> str:
        """生成输出文件路径"""
        input_file = Path(input_path)
        output_settings = self.config.get('file_handling', {}).get('output', {})

        suffix = output_settings.get('suffix', '_formatted')
        extension = output_settings.get('extension', '.md')

        return str(input_file.parent / f"{input_file.stem}{suffix}{extension}")

    def _process_line(self, line: str, index: int) -> str:
        """
        处理单行文本

        Args:
            line: 原始行文本
            index: 行索引

        Returns:
            处理后的行文本
        """
        original_line = line.rstrip()
        stripped = original_line.strip()

        # 空行保持不变
        if not stripped:
            return ''

        # 已经是Markdown格式的，保持不变
        if self._is_already_formatted(stripped):
            return original_line

        # 代码块检测和保护
        if self._is_in_code_block(index):
            return original_line

        # 智能标题检测
        if self._is_title_line(stripped, index):
            return self._format_as_title(stripped)

        # 列表检测和格式化
        if self._is_list_line(stripped):
            return self._format_as_list(stripped)

        # 表格检测和格式化
        if self._is_table_line(stripped):
            return self._format_as_table(stripped)

        # 引用检测
        if self._is_quote_line(stripped):
            return self._format_as_quote(stripped)

        # 链接格式化
        formatted_line = self._format_links(original_line)

        # 关键词高亮
        formatted_line = self._highlight_keywords(formatted_line)

        # 强调文本
        formatted_line = self._add_emphasis(formatted_line)

        return formatted_line

    def _is_already_formatted(self, line: str) -> bool:
        """检测是否已经是Markdown格式"""
        patterns = [
            r'^#{1,6}\s+',  # 标题
            r'^\s*[-*+]\s+',  # 无序列表
            r'^\s*\d+\.\s+',  # 有序列表
            r'^\s*>',  # 引用
            r'^\s*\|',  # 表格
            r'^(```|~~~|###)',  # 代码块
            r'^\s*[-+*]\s+',  # 列表
        ]

        return any(re.match(pattern, line) for pattern in patterns)

    def _is_in_code_block(self, index: int) -> bool:
        """检测是否在代码块内"""
        if not (0 <= index < len(self.lines)):
            return False

        line = self.lines[index].strip()

        # 检查当前行是否是代码块标记
        if line.startswith(('```', '~~~', '###')):
            return True

        # 向前查找代码块开始标记
        for i in range(max(0, index - 50), index):
            prev_line = self.lines[i].strip()
            if prev_line.startswith(('```', '~~~', '###')):
                # 查找对应的结束标记
                fence_char = prev_line[0] if prev_line.startswith('###') else prev_line[:3]
                for j in range(i + 1, min(len(self.lines), i + 100)):
                    if self.lines[j].strip().startswith(fence_char):
                        return i < index < j
                return True

        return False

    def _is_title_line(self, line: str, index: int) -> bool:
        """智能检测标题行"""
        heading_config = self.config.get('formatting_rules', {}).get('headings', {})

        if not heading_config.get('auto_detect', True):
            return False

        # 行太长不可能是标题
        max_length = heading_config.get('max_length', 50)
        if len(line) > max_length:
            return False

        # 行太短不可能是标题
        min_length = heading_config.get('min_length', 2)
        if len(line) < min_length:
            return False

        # 以标点符号结尾不太可能是标题
        if any(line.endswith(punct) for punct in ['。', '，', '；', '：', '、', '）', ')', '】', ']', '.', ',', ';', ':']):
            return False

        # 检查标题关键词
        keywords = heading_config.get('keywords', [])
        if any(keyword in line for keyword in keywords):
            return True

        # 检查段落边界
        prev_empty = index == 0 or not self.lines[index-1].strip()
        next_empty = index == len(self.lines)-1 or not self.lines[index+1].strip()

        # 独立成行的短文本很可能是标题
        if prev_empty and len(line) < 30:
            return True

        return False

    def _format_as_title(self, line: str) -> str:
        """格式化为标题"""
        heading_config = self.config.get('formatting_rules', {}).get('headings', {})
        max_level = heading_config.get('max_level', 6)

        # 检查标题关键词，提升级别
        keywords = heading_config.get('keywords', [])
        if any(keyword in line for keyword in keywords):
            level = 1  # 包含关键词的直接作为一级标题
        else:
            # 根据长度确定标题级别
            if len(line) < 15:
                level = 2  # 普通短文本作为二级标题
            elif len(line) < 25:
                level = 3  # 中等长度作为三级标题
            else:
                level = 4  # 长文本作为四级标题

        # 限制最大级别
        level = min(level, max_level)

        return f"{'#' * level} {line}"

    def _is_list_line(self, line: str) -> bool:
        """检测列表行"""
        list_config = self.config.get('formatting_rules', {}).get('lists', {})

        if not list_config.get('auto_detect', True):
            return False

        # 已有的列表标记
        if re.match(r'^[-*+•]\s+', line) or re.match(r'^\d+[\.\)]\s+', line):
            return True

        # 中文数字列表
        if re.match(r'^[一二三四五六七八九十百千万][、\.\)]\s*', line):
            return True

        # 以列表符号开头但格式不规范
        if line and line[0] in '-*+•' and len(line) > 1 and line[1] != ' ':
            return True

        return False

    def _format_as_list(self, line: str) -> str:
        """格式化列表"""
        list_config = self.config.get('formatting_rules', {}).get('lists', {})
        stripped = line.strip()

        # 如果已经有正确的格式，保持不变
        if re.match(r'^[-*+•]\s+', stripped) or re.match(r'^\d+[\.\)]\s+', stripped):
            return line

        # 中文数字转换
        if list_config.get('convert_chinese_numbers', True):
            chinese_map = list_config.get('chinese_number_map', {
                '一': '1', '二': '2', '三': '3', '四': '4', '五': '5',
                '六': '6', '七': '7', '八': '8', '九': '9', '十': '10'
            })

            for cn, num in chinese_map.items():
                if stripped.startswith(cn):
                    result = stripped.replace(cn, num, 1)
                    result = re.sub(r'[、\.\)]+', '.', result)
                    return f"{result} "

        # 修复不规范符号
        if stripped and stripped[0] in '-*+•' and (len(stripped) == 1 or stripped[1] != ' '):
            return f"{stripped[0]} {stripped[1:] if len(stripped) > 1 else ''}"

        return line

    def _is_table_line(self, line: str) -> bool:
        """检测表格行"""
        table_config = self.config.get('formatting_rules', {}).get('tables', {})

        if not table_config.get('auto_detect', True):
            return False

        # 制表符分隔
        if '\t' in line and line.count('\t') >= table_config.get('min_columns', 2) - 1:
            return True

        # 多空格分隔
        parts = re.split(r'\s{2,}', line.strip())
        if len(parts) >= table_config.get('min_columns', 2):
            # 检查是否都是简短文本（表格特征）
            short_parts = [p for p in parts if len(p.strip()) < 20]
            if len(short_parts) >= len(parts) * 0.6:
                return True

        return False

    def _format_as_table(self, line: str) -> str:
        """格式化表格"""
        table_config = self.config.get('formatting_rules', {}).get('tables', {})
        separator = table_config.get('separator', ' | ')

        # 优先使用制表符分割
        if '\t' in line:
            parts = line.split('\t')
        else:
            parts = re.split(r'\s{2,}', line.strip())

        # 清理每列内容
        clean_parts = [part.strip() for part in parts if part.strip()]
        return separator.join(clean_parts)

    def _is_quote_line(self, line: str) -> bool:
        """检测引用行"""
        return line.startswith('>') or line.startswith('"') or line.startswith('"')

    def _format_as_quote(self, line: str) -> str:
        """格式化引用"""
        stripped = line.strip()

        if stripped.startswith('>'):
            return line
        elif stripped.startswith('"') and stripped.endswith('"'):
            return f"> {stripped[1:-1]}"
        elif stripped.startswith('"') and stripped.endswith('"'):
            return f"> {stripped[1:-1]}"

        return f"> {stripped}"

    def _format_links(self, line: str) -> str:
        """格式化链接"""
        links_config = self.config.get('formatting_rules', {}).get('links', {})

        if not links_config.get('auto_format_urls', True):
            return line

        # HTTP/HTTPS 链接
        line = re.sub(
            r'(https?://[^\s\)]+)',
            r'[\1](\1)',
            line
        )

        # WWW 链接
        line = re.sub(
            r'(^|\s)(www\.[^\s]+)',
            r'\1[\2](https://\2)',
            line
        )

        return line

    def _highlight_keywords(self, line: str) -> str:
        """高亮技术关键词"""
        keywords_config = self.config.get('formatting_rules', {}).get('keywords', {})

        if not keywords_config.get('highlight_tech_terms', True):
            return line

        tech_keywords = keywords_config.get('tech_keywords', {})
        all_keywords = []

        # 收集所有技术关键词
        for category, keywords in tech_keywords.items():
            if isinstance(keywords, list):
                all_keywords.extend(keywords)

        for keyword in all_keywords:
            if keyword in line and f'`{keyword}`' not in line:
                # 使用单词边界避免部分匹配
                pattern = r'\b' + re.escape(keyword) + r'\b'
                line = re.sub(pattern, f'`{keyword}`', line)

        return line

    def _add_emphasis(self, line: str) -> str:
        """添加强调"""
        emphasis_config = self.config.get('formatting_rules', {}).get('emphasis', {})

        if not emphasis_config.get('auto_emphasize', True):
            return line

        important_words = emphasis_config.get('important_words', {})
        all_important = []

        # 收集所有重要词汇
        for category, words in important_words.items():
            if isinstance(words, list):
                all_important.extend(words)

        for word in all_important:
            if word in line and f'**{word}**' not in line:
                # 使用单词边界
                pattern = r'\b' + re.escape(word) + r'\b'
                line = re.sub(pattern, f'**{word}**', line, flags=re.IGNORECASE)

        return line


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='TXT转Markdown格式化器 - 智能将TXT文件转换为结构清晰的Markdown文档'
    )
    parser.add_argument('input_file', help='输入的TXT文件路径')
    parser.add_argument('-o', '--output', help='输出文件路径（可选）')
    parser.add_argument('-c', '--config', help='配置文件路径（可选）')
    parser.add_argument('--inplace', action='store_true', help='原地修改文件')
    parser.add_argument('-v', '--verbose', action='store_true', help='详细输出')

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        converter = TXTToMarkdownConverter(args.config)

        if args.inplace:
            output_path = args.input_file
            # 更改文件扩展名为.md
            if output_path.endswith('.txt'):
                output_path = output_path[:-4] + '.md'
        else:
            output_path = args.output

        result_path = converter.convert_file(args.input_file, output_path)

        if args.inplace:
            print(f"✅ 文件已格式化: {result_path}")
        else:
            print(f"✅ 转换完成，输出文件: {result_path}")

    except Exception as e:
        print(f"❌ 转换失败: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
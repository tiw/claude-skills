#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工作规划结构分析工具
解析总纲文档的章节结构和主题分布
"""

import argparse
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple


class PlanAnalyzer:
    def __init__(self):
        self.heading_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)

    def analyze_structure(self, file_path: str) -> Dict:
        """分析markdown文件的结构"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 提取标题结构
        headings = self._extract_headings(content)

        # 分析主题分布
        themes = self._analyze_themes(content, headings)

        # 生成结构报告
        structure = {
            'file_path': file_path,
            'total_headings': len(headings),
            'heading_levels': self._count_levels(headings),
            'main_sections': [h for h in headings if h['level'] <= 2],
            'detailed_structure': headings,
            'themes': themes
        }

        return structure

    def _extract_headings(self, content: str) -> List[Dict]:
        """提取所有标题及其位置"""
        headings = []
        lines = content.split('\n')

        for i, line in enumerate(lines):
            match = self.heading_pattern.match(line)
            if match:
                level = len(match.group(1))
                title = match.group(2).strip()
                headings.append({
                    'level': level,
                    'title': title,
                    'line_number': i + 1,
                    'content_preview': self._get_content_preview(content, i)
                })

        return headings

    def _get_content_preview(self, content: str, heading_line: int) -> str:
        """获取标题后的内容预览"""
        lines = content.split('\n')
        start = heading_line
        end = min(start + 5, len(lines))

        preview_lines = []
        for i in range(start + 1, end):
            if lines[i].startswith('#'):
                break
            preview_lines.append(lines[i])

        preview = ' '.join(preview_lines).strip()
        return preview[:100] + '...' if len(preview) > 100 else preview

    def _analyze_themes(self, content: str, headings: List[Dict]) -> List[Dict]:
        """分析文档主题"""
        themes = []

        # 基于一级和二级标题识别主要主题
        main_headings = [h for h in headings if h['level'] <= 2]

        for heading in main_headings:
            theme_keywords = self._extract_keywords(heading['title'] + ' ' + heading['content_preview'])
            themes.append({
                'title': heading['title'],
                'level': heading['level'],
                'keywords': theme_keywords,
                'line_number': heading['line_number']
            })

        return themes

    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        # 简单的关键词提取逻辑
        common_words = {'的', '和', '在', '是', '为', '了', '与', '中', '有', '及', '等', '或', '将', '会', '对', '进行'}
        words = re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+', text.lower())
        keywords = [word for word in words if len(word) > 1 and word not in common_words]
        return list(set(keywords))[:10]  # 返回前10个独特关键词

    def _count_levels(self, headings: List[Dict]) -> Dict[int, int]:
        """统计各级标题数量"""
        levels = {}
        for heading in headings:
            level = heading['level']
            levels[level] = levels.get(level, 0) + 1
        return levels


def main():
    parser = argparse.ArgumentParser(description='分析工作规划文档结构')
    parser.add_argument('file_path', help='要分析的markdown文件路径')
    parser.add_argument('--output', '-o', help='输出分析结果到文件')
    parser.add_argument('--format', choices=['json', 'text'], default='text', help='输出格式')

    args = parser.parse_args()

    analyzer = PlanAnalyzer()
    structure = analyzer.analyze_structure(args.file_path)

    if args.format == 'json':
        output = json.dumps(structure, ensure_ascii=False, indent=2)
    else:
        output = format_structure_as_text(structure)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"结构分析结果已保存到: {args.output}")
    else:
        print(output)


def format_structure_as_text(structure: Dict) -> str:
    """将结构分析结果格式化为文本"""
    output = []
    output.append("=" * 50)
    output.append(f"文档结构分析: {structure['file_path']}")
    output.append("=" * 50)
    output.append("")

    # 基本信息
    output.append("📊 基本信息:")
    output.append(f"  总标题数: {structure['total_headings']}")
    output.append(f"  主要章节数: {len(structure['main_sections'])}")
    output.append("")

    # 标题层级分布
    output.append("📈 标题层级分布:")
    for level, count in sorted(structure['heading_levels'].items()):
        prefix = "#" * level
        output.append(f"  {prefix} 级标题: {count} 个")
    output.append("")

    # 主要章节
    output.append("📋 主要章节:")
    for section in structure['main_sections']:
        prefix = "#" * section['level']
        preview = section['content_preview'][:50]
        output.append(f"  {prefix} {section['title']}")
        if preview:
            output.append(f"    预览: {preview}...")
    output.append("")

    # 主题分析
    output.append("🏷️ 主题分析:")
    for theme in structure['themes']:
        prefix = "#" * theme['level']
        keywords = ", ".join(theme['keywords'][:5])
        output.append(f"  {prefix} {theme['title']}")
        output.append(f"    关键词: {keywords}")

    return "\n".join(output)


if __name__ == "__main__":
    main()
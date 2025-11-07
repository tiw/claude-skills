#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工作规划整合工具
将多个子规划智能匹配并整合到总纲规划的相应部分
"""

import argparse
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from difflib import SequenceMatcher
import jieba


class PlanMerger:
    def __init__(self):
        self.heading_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
        self.load_default_matching_rules()

    def load_default_matching_rules(self):
        """加载默认匹配规则"""
        self.matching_rules = {
            'keywords_weight': 0.5,
            'structure_weight': 0.3,
            'position_weight': 0.2,
            'min_similarity': 0.1,
            'content_separators': {
                'main': '\n--- 子规划内容 ---\n',
                'sub': '\n\n'
            }
        }

    def merge_plans(self, master_file: str, subplans_dir: str, output_file: str) -> Dict:
        """整合规划文档"""
        # 读取总纲文档
        with open(master_file, 'r', encoding='utf-8') as f:
            master_content = f.read()

        # 分析总纲结构
        master_structure = self._analyze_document_structure(master_content)

        # 读取所有子规划
        subplans = self._load_subplans(subplans_dir)

        # 匹配子规划到总纲章节
        matches = self._match_subplans_to_sections(subplans, master_structure)

        # 生成整合文档
        merged_content = self._generate_merged_document(
            master_content, master_structure, matches, subplans
        )

        # 保存结果
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(merged_content)

        # 生成整合报告
        report = {
            'master_file': master_file,
            'subplans_count': len(subplans),
            'matches_found': len(matches),
            'output_file': output_file,
            'matching_details': matches,
            'unmatched_subplans': [sp for sp in subplans if sp['name'] not in [m['subplan'] for m in matches]]
        }

        return report

    def _analyze_document_structure(self, content: str) -> List[Dict]:
        """分析文档结构"""
        headings = []
        lines = content.split('\n')

        for i, line in enumerate(lines):
            match = self.heading_pattern.match(line)
            if match:
                level = len(match.group(1))
                title = match.group(2).strip()

                # 提取章节内容
                section_content = self._extract_section_content(content, i, level)

                headings.append({
                    'level': level,
                    'title': title,
                    'line_number': i + 1,
                    'content': section_content,
                    'keywords': self._extract_keywords(title + ' ' + section_content[:200])
                })

        return headings

    def _extract_section_content(self, content: str, start_line: int, current_level: int) -> str:
        """提取章节内容"""
        lines = content.split('\n')
        content_lines = []

        # 跳过当前标题行，从下一行开始
        for i in range(start_line + 1, len(lines)):
            line = lines[i]

            # 检查是否遇到同级或更高级标题
            heading_match = self.heading_pattern.match(line)
            if heading_match:
                heading_level = len(heading_match.group(1))
                if heading_level <= current_level:
                    break

            content_lines.append(line)

        return '\n'.join(content_lines).strip()

    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        # 使用jieba进行中文分词
        words = jieba.lcut(text.lower())

        # 过滤停用词和短词
        stop_words = {'的', '和', '在', '是', '为', '了', '与', '中', '有', '及', '等', '或', '将', '会', '对', '进行', '工作', '规划', '计划'}
        keywords = [word for word in words if len(word) > 1 and word not in stop_words and word.strip()]

        # 返回前10个最常见的关键词
        word_freq = {}
        for word in keywords:
            word_freq[word] = word_freq.get(word, 0) + 1

        return [word for word, _ in sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]]

    def _load_subplans(self, subplans_dir: str) -> List[Dict]:
        """加载所有子规划文件"""
        subplans = []
        subplan_path = Path(subplans_dir)

        for file_path in subplan_path.glob('*.md'):
            # 跳过总纲文件（假设总纲文件不在此目录中，或者通过名称排除）
            if file_path.name.startswith('总纲') or file_path.name.startswith('master'):
                continue

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 分析子规划结构
            structure = self._analyze_document_structure(content)

            subplans.append({
                'name': file_path.stem,
                'file_path': str(file_path),
                'content': content,
                'structure': structure,
                'keywords': self._extract_keywords(content)
            })

        return subplans

    def _match_subplans_to_sections(self, subplans: List[Dict], master_structure: List[Dict]) -> List[Dict]:
        """将子规划匹配到总纲章节"""
        matches = []

        for subplan in subplans:
            best_match = self._find_best_section_match(subplan, master_structure)

            if best_match and best_match['similarity'] >= self.matching_rules['min_similarity']:
                matches.append({
                    'subplan': subplan['name'],
                    'section_index': best_match['section_index'],
                    'section_title': best_match['section_title'],
                    'similarity': best_match['similarity'],
                    'match_reason': best_match['reason']
                })

        return matches

    def _find_best_section_match(self, subplan: Dict, master_structure: List[Dict]) -> Optional[Dict]:
        """为子规划找到最佳匹配章节"""
        best_match = None
        max_similarity = 0

        for i, section in enumerate(master_structure):
            # 考虑1-3级标题作为匹配目标
            if section['level'] > 3:
                continue

            similarity = self._calculate_similarity(subplan, section)

            if similarity > max_similarity:
                max_similarity = similarity
                best_match = {
                    'section_index': i,
                    'section_title': section['title'],
                    'similarity': similarity,
                    'reason': self._generate_match_reason(subplan, section, similarity)
                }

        return best_match if max_similarity > 0 else None

    def _calculate_similarity(self, subplan: Dict, section: Dict) -> float:
        """计算子规划与章节的相似度"""
        # 关键词相似度
        subplan_keywords = set(subplan['keywords'])
        section_keywords = set(section['keywords'])

        if not subplan_keywords or not section_keywords:
            keyword_similarity = 0
        else:
            intersection = subplan_keywords.intersection(section_keywords)
            union = subplan_keywords.union(section_keywords)
            keyword_similarity = len(intersection) / len(union) if union else 0

        # 文本相似度（使用简单的字符串匹配）
        text_similarity = SequenceMatcher(
            None,
            subplan['content'][:500],
            section['title'] + ' ' + section['content'][:500]
        ).ratio()

        # 综合相似度
        total_similarity = (
            keyword_similarity * self.matching_rules['keywords_weight'] +
            text_similarity * (1 - self.matching_rules['keywords_weight'])
        )

        return total_similarity

    def _generate_match_reason(self, subplan: Dict, section: Dict, similarity: float) -> str:
        """生成匹配原因说明"""
        common_keywords = set(subplan['keywords']).intersection(set(section['keywords']))

        reason_parts = []
        if common_keywords:
            reason_parts.append(f"共同关键词: {', '.join(list(common_keywords)[:3])}")

        if similarity > 0.5:
            reason_parts.append("内容高度相关")
        elif similarity > 0.3:
            reason_parts.append("内容较为相关")
        else:
            reason_parts.append("内容部分相关")

        return "; ".join(reason_parts)

    def _generate_merged_document(self, master_content: str, master_structure: List[Dict],
                                matches: List[Dict], subplans: List[Dict]) -> str:
        """生成整合后的文档"""
        lines = master_content.split('\n')
        result_lines = []

        # 创建子规划查找字典
        subplan_dict = {sp['name']: sp for sp in subplans}

        # 按行号排序匹配
        matches_by_line = sorted(matches,
                               key=lambda x: master_structure[x['section_index']]['line_number'],
                               reverse=True)

        processed_indices = set()

        for i, line in enumerate(lines):
            result_lines.append(line)

            # 检查是否是需要插入内容的位置
            for match in matches_by_line:
                section_idx = match['section_index']
                section = master_structure[section_idx]

                if (i == section['line_number'] and
                    section_idx not in processed_indices):

                    # 插入子规划内容
                    subplan = subplan_dict[match['subplan']]
                    separator = self.matching_rules['content_separators']['main']

                    result_lines.append(separator)
                    result_lines.append(f"### 📋 {subplan['name']}")
                    result_lines.append("")

                    # 添加子规划内容
                    subplan_lines = subplan['content'].split('\n')
                    for subline in subplan_lines:
                        if subline.strip():  # 跳过空行
                            result_lines.append(f"  {subline}")

                    result_lines.append("")
                    processed_indices.add(section_idx)
                    break

        return '\n'.join(result_lines)


def main():
    parser = argparse.ArgumentParser(description='整合工作规划文档')
    parser.add_argument('master_file', help='总纲规划文件路径')
    parser.add_argument('subplans_dir', help='子规划文件目录')
    parser.add_argument('output_file', help='输出文件路径')
    parser.add_argument('--report', '-r', help='生成匹配报告文件')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细信息')

    args = parser.parse_args()

    merger = PlanMerger()

    if args.verbose:
        print("🚀 开始整合工作规划...")
        print(f"📖 总纲文件: {args.master_file}")
        print(f"📁 子规划目录: {args.subplans_dir}")
        print(f"💾 输出文件: {args.output_file}")
        print()

    try:
        report = merger.merge_plans(args.master_file, args.subplans_dir, args.output_file)

        print("✅ 规划整合完成!")
        print(f"📊 处理了 {report['subplans_count']} 个子规划文件")
        print(f"🔗 成功匹配 {report['matches_found']} 个子规划到相应章节")

        if report['unmatched_subplans']:
            print(f"⚠️  未匹配的子规划: {len(report['unmatched_subplans'])} 个")
            for unmatched in report['unmatched_subplans']:
                print(f"   - {unmatched['name']}")

        if args.report:
            with open(args.report, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"📋 匹配报告已保存到: {args.report}")

    except Exception as e:
        print(f"❌ 整合过程中出现错误: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
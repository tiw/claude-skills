#!/usr/bin/env python3
"""
技能打包脚本
将技能目录打包为可分发的 zip 文件
"""

import os
import sys
import zipfile
import yaml
from pathlib import Path
from typing import List, Dict, Any

class SkillPackageValidator:
    """技能验证器"""

    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.errors = []
        self.warnings = []

    def validate_skill_structure(self) -> bool:
        """验证技能结构"""
        if not self.skill_path.exists():
            self.errors.append(f"技能目录不存在: {self.skill_path}")
            return False

        # 检查必需文件
        skill_md = self.skill_path / "SKILL.md"
        if not skill_md.exists():
            self.errors.append("缺少必需的 SKILL.md 文件")
            return False

        return True

    def validate_skill_metadata(self) -> bool:
        """验证技能元数据"""
        skill_md = self.skill_path / "SKILL.md"

        try:
            with open(skill_md, 'r', encoding='utf-8') as f:
                content = f.read()

            # 检查是否包含 YAML frontmatter
            if not content.startswith('---'):
                self.errors.append("SKILL.md 必须以 YAML frontmatter 开始")
                return False

            # 解析 frontmatter
            try:
                end_index = content.find('---', 3)
                if end_index == -1:
                    self.errors.append("YAML frontmatter 格式不正确")
                    return False

                frontmatter = content[3:end_index].strip()
                metadata = yaml.safe_load(frontmatter)

                # 检查必需字段
                required_fields = ['name', 'description']
                for field in required_fields:
                    if field not in metadata:
                        self.errors.append(f"缺少必需的元数据字段: {field}")
                    elif not metadata[field] or not metadata[field].strip():
                        self.errors.append(f"元数据字段 '{field}' 不能为空")

                # 检查字段质量
                if 'name' in metadata:
                    name = metadata['name']
                    if not re.match(r'^[a-z0-9-]+$', name):
                        self.warnings.append("技能名称应该只包含小写字母、数字和连字符")

                if 'description' in metadata:
                    description = metadata['description']
                    if len(description) < 20:
                        self.warnings.append("技能描述过短，建议提供更详细的描述")
                    if '此技能' in description or '这个技能' in description:
                        self.warnings.append("建议使用第三人称描述技能（如 '此技能用于...' 而不是 '此技能用于...'）")

            except yaml.YAMLError as e:
                self.errors.append(f"YAML frontmatter 解析错误: {e}")
                return False

        except Exception as e:
            self.errors.append(f"读取 SKILL.md 失败: {e}")
            return False

        return True

    def validate_directory_structure(self) -> bool:
        """验证目录结构"""
        required_dirs = ['scripts', 'references', 'assets']
        existing_dirs = []

        for dir_name in required_dirs:
            dir_path = self.skill_path / dir_name
            if dir_path.exists():
                existing_dirs.append(dir_name)

        # 检查是否有未使用的目录
        if not existing_dirs:
            self.warnings.append("建议创建 scripts、references 或 assets 目录来组织技能资源")

        return True

    def validate_file_references(self) -> bool:
        """验证 SKILL.md 中的文件引用"""
        skill_md = self.skill_path / "SKILL.md"

        try:
            with open(skill_md, 'r', encoding='utf-8') as f:
                content = f.read()

            # 检查脚本文件引用
            scripts_dir = self.skill_path / "scripts"
            if scripts_dir.exists():
                for script_file in scripts_dir.glob("*.py"):
                    if script_file.name not in content:
                        self.warnings.append(f"脚本文件 {script_file.name} 未在 SKILL.md 中引用")

            # 检查引用文件
            refs_dir = self.skill_path / "references"
            if refs_dir.exists():
                for ref_file in refs_dir.glob("*.md"):
                    if ref_file.name not in content:
                        self.warnings.append(f"引用文件 {ref_file.name} 未在 SKILL.md 中引用")

        except Exception as e:
            self.errors.append(f"验证文件引用失败: {e}")
            return False

        return True

    def get_validation_results(self) -> Dict[str, List[str]]:
        """获取验证结果"""
        return {
            'errors': self.errors,
            'warnings': self.warnings
        }

def package_skill(skill_path: str, output_dir: str = ".") -> bool:
    """打包技能"""
    skill_dir = Path(skill_path).resolve()

    if not skill_dir.exists():
        print(f"错误: 技能目录不存在 - {skill_path}")
        return False

    # 验证技能
    validator = SkillPackageValidator(skill_dir)

    print(f"验证技能: {skill_dir.name}")

    # 执行所有验证
    validation_passed = True
    validation_passed &= validator.validate_skill_structure()
    validation_passed &= validator.validate_skill_metadata()
    validation_passed &= validator.validate_directory_structure()
    validation_passed &= validator.validate_file_references()

    # 获取验证结果
    results = validator.get_validation_results()

    # 显示错误
    if results['errors']:
        print("\n❌ 发现错误:")
        for error in results['errors']:
            print(f"  • {error}")
        return False

    # 显示警告
    if results['warnings']:
        print("\n⚠️  警告:")
        for warning in results['warnings']:
            print(f"  • {warning}")

    # 如果验证通过，打包技能
    print("\n✅ 验证通过，正在打包...")

    # 获取技能名称
    skill_md = skill_dir / "SKILL.md"
    with open(skill_md, 'r', encoding='utf-8') as f:
        content = f.read()

    try:
        end_index = content.find('---', 3)
        frontmatter = content[3:end_index].strip()
        metadata = yaml.safe_load(frontmatter)
        skill_name = metadata.get('name', skill_dir.name)
    except:
        skill_name = skill_dir.name

    # 创建输出文件路径
    output_path = Path(output_dir) / f"{skill_name}.zip"

    # 创建 zip 文件
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(skill_dir):
            for file in files:
                file_path = Path(root) / file
                arc_path = file_path.relative_to(skill_dir)
                zf.write(file_path, arc_path)

    print(f"📦 技能已打包: {output_path}")
    print(f"📊 打包大小: {output_path.stat().st_size} 字节")

    return True

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python package_skill.py <技能路径> [输出目录]")
        sys.exit(1)

    skill_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."

    success = package_skill(skill_path, output_dir)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    import re
    main()
#!/usr/bin/env python3
"""
Character Integration Validation Test
キャラクター統合の正当性とコンテンツ品質検証

概要:
- character_profiles.md統合の検証
- キャラクター設定の一貫性確認
- 対話パターンの適切性評価
"""

import os
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Any
import re

class CharacterValidationTest:
    """キャラクター統合検証テスト"""
    
    def __init__(self, superclaude_root: str):
        self.root = Path(superclaude_root).resolve()
        self.trinitas_path = self.root / "Extensions" / "Trinitas"
        self.test_results = []
        
    def validate_character_profiles(self) -> bool:
        """character_profiles.mdの内容検証"""
        try:
            profiles_file = self.trinitas_path / "character_profiles.md"
            
            with open(profiles_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 必須セクションの存在確認
            required_sections = [
                "# Trinitas Character Profiles",
                "## 1. Tri-Core伝説",
                "### 1.1. 第1章: グリフィン・システムズのアーキテクト",
                "### 1.2. 第2章: H.I.D.E. 404のブラックハット",
                "### 1.3. 第3章: フェニックス・プロトコル",
                "## 2. 深層心理プロファイル",
                "### 2.1. Springfield",
                "### 2.2. Krukai", 
                "### 2.3. Vector",
                "## 3. 統合対話パターン"
            ]
            
            missing_sections = []
            for section in required_sections:
                if section not in content:
                    missing_sections.append(section)
            
            if missing_sections:
                print(f"❌ 必須セクション不足: {missing_sections}")
                return False
            
            # キャラクター固有要素の確認
            character_elements = {
                "Springfield": ["笑顔の裏", "指揮官", "ズッケロ", "グリフィン・システムズ"],
                "Krukai": ["エリートの責務", "404", "H.I.D.E.", "フン"],
                "Vector": ["放火魔の献身", "あたし", "……", "フェニックス・プロトコル"]
            }
            
            for character, elements in character_elements.items():
                for element in elements:
                    if element not in content:
                        print(f"❌ {character}の重要要素「{element}」が不足")
                        return False
            
            print("✅ character_profiles.md の内容検証: 合格")
            return True
            
        except Exception as e:
            print(f"❌ character_profiles.md 検証エラー: {e}")
            return False
    
    def validate_character_integration(self) -> bool:
        """既存ファイルとのキャラクター統合検証"""
        try:
            # personas.mdでの参照確認
            personas_file = self.trinitas_path / "personas.md"
            with open(personas_file, 'r', encoding='utf-8') as f:
                personas_content = f.read()
            
            if "@character_profiles.md" not in personas_content:
                print("❌ personas.mdにcharacter_profiles.mdへの参照がありません")
                return False
            
            # modes.mdでの参照確認
            modes_file = self.trinitas_path / "modes.md"
            with open(modes_file, 'r', encoding='utf-8') as f:
                modes_content = f.read()
            
            if "@character_profiles.md" not in modes_content:
                print("❌ modes.mdにcharacter_profiles.mdへの参照がありません")
                return False
            
            # config.yamlでのファイル登録確認
            config_file = self.trinitas_path / "config.yaml"
            with open(config_file, 'r', encoding='utf-8') as f:
                config_content = f.read()
            
            if "character_profiles.md" not in config_content:
                print("❌ config.yamlにcharacter_profiles.mdが登録されていません")
                return False
            
            print("✅ キャラクター統合検証: 合格")
            return True
            
        except Exception as e:
            print(f"❌ キャラクター統合検証エラー: {e}")
            return False
    
    def validate_dialogue_patterns(self) -> bool:
        """対話パターンの適切性検証"""
        try:
            profiles_file = self.trinitas_path / "character_profiles.md"
            with open(profiles_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 対話例の存在確認
            dialogue_patterns = [
                "コードレビュー時の反応例",
                "問題解決アプローチ",
                "技術的振る舞いパターン",
                "特殊状況での統合反応"
            ]
            
            for pattern in dialogue_patterns:
                if pattern not in content:
                    print(f"❌ 対話パターン「{pattern}」が不足")
                    return False
            
            # 各キャラクターの発話例確認
            springfield_quotes = [
                "指揮官",
                "ふふ", 
                "一緒に",
                "素敵な"
            ]
            
            krukai_quotes = [
                "フン",
                "悪くないわ",
                "404",
                "完璧"
            ]
            
            vector_quotes = [
                "……",
                "あたし",
                "予感",
                "ダメになる"
            ]
            
            all_quotes = springfield_quotes + krukai_quotes + vector_quotes
            missing_quotes = []
            
            for quote in all_quotes:
                if quote not in content:
                    missing_quotes.append(quote)
            
            if missing_quotes:
                print(f"❌ 重要な発話要素不足: {missing_quotes}")
                return False
            
            print("✅ 対話パターン検証: 合格")
            return True
            
        except Exception as e:
            print(f"❌ 対話パターン検証エラー: {e}")
            return False
    
    def validate_technical_integration(self) -> bool:
        """技術統合の適切性検証"""
        try:
            profiles_file = self.trinitas_path / "character_profiles.md"
            with open(profiles_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 技術応用例の確認
            technical_examples = [
                "システムアーキテクチャ設計",
                "パフォーマンス最適化",
                "セキュリティ評価",
                "新技術学習時"
            ]
            
            for example in technical_examples:
                if example not in content:
                    print(f"❌ 技術応用例「{example}」が不足")
                    return False
            
            # 技術用語の適切な使用確認
            tech_terms = [
                "AWS", "SageMaker", "Rust", "Python",
                "SQLインジェクション", "O(n²)", "CVE"
            ]
            
            for term in tech_terms:
                if term not in content:
                    print(f"❌ 重要な技術用語「{term}」が不足")
                    return False
            
            print("✅ 技術統合検証: 合格")
            return True
            
        except Exception as e:
            print(f"❌ 技術統合検証エラー: {e}")
            return False
    
    def run_all_validations(self) -> Dict[str, bool]:
        """全検証の実行"""
        results = {
            "character_profiles_content": self.validate_character_profiles(),
            "character_integration": self.validate_character_integration(),
            "dialogue_patterns": self.validate_dialogue_patterns(),
            "technical_integration": self.validate_technical_integration()
        }
        
        return results
    
    def generate_report(self, results: Dict[str, bool]) -> str:
        """検証レポートの生成"""
        total_tests = len(results)
        passed_tests = sum(results.values())
        success_rate = (passed_tests / total_tests) * 100
        
        report = f"""
Character Integration Validation Report
=======================================
Date: 2025-01-20
Total Tests: {total_tests}
Passed: {passed_tests}
Failed: {total_tests - passed_tests}
Success Rate: {success_rate:.1f}%

Test Results:
-------------
"""
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            report += f"{status} {test_name.replace('_', ' ').title()}\n"
        
        if success_rate >= 95:
            report += "\n🎉 All validations passed - Character integration successful!"
        elif success_rate >= 80:
            report += "\n⚠️ Most validations passed - Minor issues to address"
        else:
            report += "\n🚨 Critical issues found - Character integration needs work"
        
        return report

def main():
    """メイン実行関数"""
    if len(sys.argv) < 2:
        print("Usage: python character_validation_test.py <superclaude_root>")
        return 1
    
    superclaude_root = sys.argv[1]
    validator = CharacterValidationTest(superclaude_root)
    
    print("Character Integration Validation Starting...")
    print("=" * 50)
    
    results = validator.run_all_validations()
    report = validator.generate_report(results)
    
    print(report)
    
    # 失敗があった場合は終了コード1
    return 0 if all(results.values()) else 1

if __name__ == "__main__":
    sys.exit(main())
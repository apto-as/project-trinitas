#!/usr/bin/env python3
"""
Trinitas Dynamic Patcher v2.1
SuperClaude Extension用の改善された動的パッチシステム（フラット構造対応版）

主な改善点:
- フラット構造のSuperClaudeに対応
- EXTENSIONS.mdを動的に読み込み（二重管理を解消）
- SuperClaudeインストール検証機能
- ファイル整合性チェック機能
- より堅牢なエラーハンドリング

使用例:
    python trinitas_patcher_v2_1.py verify-superclaude /path/to/superclaude
    python trinitas_patcher_v2_1.py apply /path/to/superclaude
    python trinitas_patcher_v2_1.py verify /path/to/superclaude
    python trinitas_patcher_v2_1.py remove /path/to/superclaude
"""

import os
import sys
import json
import shutil
import hashlib
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import tempfile
import logging
import yaml

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TrinitasPatcherV21:
    """SuperClaude Trinitas拡張の改善された動的パッチシステム（フラット構造対応）"""
    
    # バージョン要件
    REQUIRED_SUPERCLAUDE_VERSION = "3.0.0"
    PATCHER_VERSION = "2.1.0"
    
    def __init__(self, superclaude_root: str):
        self.root = Path(superclaude_root).resolve()
        
        # フラット構造対応：Coreディレクトリが存在するかチェック
        self.has_core_dir = (self.root / "Core").exists()
        
        if self.has_core_dir:
            # 古い構造（Core/サブディレクトリあり）
            self.core_path = self.root / "Core"
            self.extensions_path = self.root / "Extensions"
            logger.info("検出: Core/サブディレクトリ構造")
        else:
            # 新しい構造（フラット）
            self.core_path = self.root
            self.extensions_path = self.root / "Extensions"
            logger.info("検出: フラット構造")
        
        self.backup_path = self.root / ".trinitas_backup"
        self.state_file = self.root / ".trinitas_state.json"
        
        # Trinitasプロジェクトのルート（実行スクリプトの親ディレクトリ）
        self.trinitas_root = Path(__file__).parent.parent
        
        # パッチ対象ファイル（構造に応じて動的に設定）
        self.patch_targets = {
            "CLAUDE.md": self.core_path / "CLAUDE.md",
            "ORCHESTRATOR.md": self.core_path / "ORCHESTRATOR.md",
            "COMMANDS.md": self.core_path / "COMMANDS.md",
            "MODES.md": self.core_path / "MODES.md",
            "EXTENSIONS.md": self.core_path / "EXTENSIONS.md"
        }
        
        # Modesディレクトリの設定
        if self.has_core_dir:
            self.modes_path = self.core_path / "Modes"
        else:
            # フラット構造ではModesディレクトリを作成
            self.modes_path = self.root / "Modes"
        
        # Trinitasソースファイル
        self.trinitas_sources = {
            "EXTENSIONS.md": self.trinitas_root / "Core" / "EXTENSIONS.md",
            "Modes/TRINITAS.md": self.trinitas_root / "Core" / "Modes" / "TRINITAS.md",
            "Extensions/Trinitas": self.trinitas_root / "Extensions" / "Trinitas"
        }
    
    def verify_superclaude_installation(self) -> Tuple[bool, str]:
        """SuperClaudeのインストール状態を検証（フラット構造対応）"""
        try:
            # 基本ディレクトリ構造の確認
            if not self.root.exists():
                return False, f"SuperClaudeルートが見つかりません: {self.root}"
            
            # 必須ファイルの確認（構造に依存しない）
            required_files = {
                "CLAUDE.md": "SuperClaudeのエントリーポイント",
                "COMMANDS.md": "コマンド定義ファイル",
                "ORCHESTRATOR.md": "ルーティングシステム",
                "PERSONAS.md": "ペルソナ定義",
                "MODES.md": "モード定義"
            }
            
            missing_files = []
            for file, description in required_files.items():
                file_path = self.core_path / file
                if not file_path.exists():
                    missing_files.append(f"{file} ({description})")
            
            if missing_files:
                return False, f"必須ファイルが不足しています:\\n" + "\\n".join(missing_files)
            
            # バージョン確認（簡易的なチェック）
            commands_content = (self.core_path / "COMMANDS.md").read_text(encoding='utf-8')
            if "/sc:" in commands_content or "## [3.0.0]" in commands_content:
                version_info = "SuperClaude v3.0.0+ を検出"
            else:
                version_info = "SuperClaudeバージョンを確認できません（v3.0.0+が必要）"
            
            structure_info = "Core/構造" if self.has_core_dir else "フラット構造"
            logger.info(f"SuperClaude検証完了: {version_info} ({structure_info})")
            return True, f"SuperClaudeは正しくインストールされています。{version_info} ({structure_info})"
            
        except Exception as e:
            return False, f"検証エラー: {str(e)}"
    
    def load_extensions_content(self) -> Optional[str]:
        """EXTENSIONS.mdの内容を動的に読み込み"""
        try:
            extensions_source = self.trinitas_sources["EXTENSIONS.md"]
            
            if not extensions_source.exists():
                logger.error(f"EXTENSIONS.mdソースファイルが見つかりません: {extensions_source}")
                return None
            
            with open(extensions_source, 'r', encoding='utf-8') as f:
                content = f.read()
            
            logger.info(f"EXTENSIONS.mdを動的に読み込みました: {len(content)} bytes")
            return content
            
        except Exception as e:
            logger.error(f"EXTENSIONS.md読み込みエラー: {e}")
            return None
    
    def calculate_file_hash(self, file_path: Path) -> Optional[str]:
        """ファイルのSHA256ハッシュを計算"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception as e:
            logger.error(f"ハッシュ計算エラー: {file_path} - {e}")
            return None
    
    def create_backup(self) -> bool:
        """現在の状態をバックアップ（改善版）"""
        try:
            self.backup_path.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = self.backup_path / f"backup_{timestamp}"
            backup_dir.mkdir()
            
            backup_info = {
                "timestamp": timestamp,
                "patcher_version": self.PATCHER_VERSION,
                "structure_type": "core_dir" if self.has_core_dir else "flat",
                "files": {},
                "checksums": {},
                "superclaude_state": {}
            }
            
            # SuperClaude検証結果を保存
            verified, message = self.verify_superclaude_installation()
            backup_info["superclaude_state"] = {
                "verified": verified,
                "message": message
            }
            
            # ファイルバックアップ
            for name, file_path in self.patch_targets.items():
                if file_path.exists():
                    backup_file = backup_dir / name
                    shutil.copy2(file_path, backup_file)
                    
                    checksum = self.calculate_file_hash(file_path)
                    backup_info["files"][name] = str(backup_file)
                    backup_info["checksums"][name] = checksum
            
            # バックアップ情報保存
            backup_info_file = backup_dir / "backup_info.json"
            with open(backup_info_file, 'w', encoding='utf-8') as f:
                json.dump(backup_info, f, indent=2, ensure_ascii=False)
            
            logger.info(f"バックアップ作成完了: {backup_dir}")
            return True
            
        except Exception as e:
            logger.error(f"バックアップ作成エラー: {e}")
            return False
    
    def verify_file_integrity(self) -> Dict[str, bool]:
        """ファイル整合性をチェック"""
        integrity_results = {}
        
        try:
            # Trinitasソースファイルの存在確認
            for name, source_path in self.trinitas_sources.items():
                if isinstance(source_path, Path):
                    integrity_results[name] = source_path.exists()
                    if not source_path.exists():
                        logger.warning(f"ソースファイル不足: {name} - {source_path}")
            
            # インストール済みTrinitas拡張の確認
            trinitas_ext_path = self.extensions_path / "Trinitas"
            if trinitas_ext_path.exists():
                # config.yamlの検証
                config_path = trinitas_ext_path / "config.yaml"
                if config_path.exists():
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config = yaml.safe_load(f)
                    integrity_results["config_valid"] = bool(config.get("extension"))
                else:
                    integrity_results["config_valid"] = False
            
            return integrity_results
            
        except Exception as e:
            logger.error(f"整合性チェックエラー: {e}")
            return integrity_results
    
    def patch_claude_md(self) -> bool:
        """CLAUDE.mdに@EXTENSIONS.md参照を追加（改善版）"""
        try:
            claude_file = self.patch_targets["CLAUDE.md"]
            
            if not claude_file.exists():
                logger.error("CLAUDE.mdが見つかりません")
                return False
            
            with open(claude_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 既存チェック
            if "@EXTENSIONS.md" in content:
                logger.info("CLAUDE.md は既にパッチ済みです")
                return True
            
            # 最適な挿入位置を特定（@MODES.mdの後）
            if "@MODES.md" in content:
                lines = content.split('\\n')
                for i, line in enumerate(lines):
                    if "@MODES.md" in line:
                        lines.insert(i + 1, "@EXTENSIONS.md")
                        break
            else:
                # 見つからない場合は末尾に追加
                lines = content.strip().split('\\n')
                lines.append("@EXTENSIONS.md")
            
            # ファイル書き込み
            with open(claude_file, 'w', encoding='utf-8') as f:
                f.write('\\n'.join(lines) + '\\n')
            
            logger.info("CLAUDE.md パッチ適用完了")
            return True
            
        except Exception as e:
            logger.error(f"CLAUDE.mdパッチエラー: {e}")
            return False
    
    def create_or_update_extensions_md(self) -> bool:
        """EXTENSIONS.mdファイルを作成または更新（動的読み込み版）"""
        try:
            extensions_file = self.patch_targets["EXTENSIONS.md"]
            
            # 動的にコンテンツを読み込み
            extensions_content = self.load_extensions_content()
            if not extensions_content:
                logger.error("EXTENSIONS.md内容の読み込みに失敗しました")
                return False
            
            # ファイルが既に存在する場合、ハッシュを比較
            if extensions_file.exists():
                current_hash = self.calculate_file_hash(extensions_file)
                new_hash = hashlib.sha256(extensions_content.encode('utf-8')).hexdigest()
                
                if current_hash == new_hash:
                    logger.info("EXTENSIONS.md は最新です")
                    return True
                else:
                    logger.info("EXTENSIONS.md を更新します")
            
            # ファイル書き込み
            with open(extensions_file, 'w', encoding='utf-8') as f:
                f.write(extensions_content)
            
            logger.info(f"EXTENSIONS.md {'更新' if extensions_file.exists() else '作成'}完了")
            return True
            
        except Exception as e:
            logger.error(f"EXTENSIONS.md作成/更新エラー: {e}")
            return False
    
    def copy_trinitas_extension(self) -> bool:
        """Trinitas拡張ファイルをコピー"""
        try:
            source_dir = self.trinitas_sources["Extensions/Trinitas"]
            target_dir = self.extensions_path / "Trinitas"
            
            if not source_dir.exists():
                logger.error(f"Trinitasソースディレクトリが見つかりません: {source_dir}")
                return False
            
            # ディレクトリ作成
            self.extensions_path.mkdir(exist_ok=True)
            
            # 既存の場合は削除（または更新）
            if target_dir.exists():
                logger.info("既存のTrinitas拡張を更新します")
                shutil.rmtree(target_dir)
            
            # コピー実行
            shutil.copytree(source_dir, target_dir)
            logger.info(f"Trinitas拡張をコピーしました: {target_dir}")
            
            # Modesディレクトリのコピー
            modes_source = self.trinitas_root / "Core" / "Modes"
            if modes_source.exists():
                self.modes_path.mkdir(exist_ok=True)
                
                for mode_file in modes_source.glob("*.md"):
                    shutil.copy2(mode_file, self.modes_path / mode_file.name)
                    logger.info(f"Modeファイルをコピー: {mode_file.name}")
            
            return True
            
        except Exception as e:
            logger.error(f"Trinitas拡張コピーエラー: {e}")
            return False
    
    def patch_core_files(self) -> bool:
        """コアファイルにTrinitas統合を適用"""
        try:
            # ORCHESTRATOR.md のパッチ
            if not self._patch_orchestrator_md():
                return False
            
            # COMMANDS.md のパッチ
            if not self._patch_commands_md():
                return False
            
            # MODES.md のパッチ
            if not self._patch_modes_md():
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"コアファイルパッチエラー: {e}")
            return False
    
    def _patch_orchestrator_md(self) -> bool:
        """ORCHESTRATOR.mdにTrinitas統合を追加"""
        try:
            orch_file = self.patch_targets["ORCHESTRATOR.md"]
            if not orch_file.exists():
                logger.warning("ORCHESTRATOR.mdが見つかりません")
                return True  # オプショナルなので続行
            
            with open(orch_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 既存チェック
            if "Trinitas Meta-Persona Integration" in content:
                logger.info("ORCHESTRATOR.md は既にパッチ済みです")
                return True
            
            # 統合セクションを追加
            integration_section = """
### Trinitas Meta-Persona Integration

**Unified Routing Architecture**: SuperClaude's intelligent routing system seamlessly integrates with Trinitas mode to provide enhanced multi-perspective analysis capabilities.

#### Mode Detection Matrix
```yaml
trinitas_activation:
  explicit_triggers:
    - command: "/sc:trinitas"
    - flag: "--trinitas"
    - flag: "--trinitas-brief"
  
  automatic_triggers:
    - complexity_threshold: 0.9
    - multi_domain_analysis: true
    - comprehensive_review: true
    - critical_decision_point: true
```
"""
            
            # 適切な位置に挿入（## 🔗 Integration Intelligence の前）
            if "## 🔗 Integration Intelligence" in content:
                content = content.replace(
                    "## 🔗 Integration Intelligence",
                    integration_section + "\\n## 🔗 Integration Intelligence"
                )
            else:
                content += "\\n" + integration_section
            
            with open(orch_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info("ORCHESTRATOR.md パッチ適用完了")
            return True
            
        except Exception as e:
            logger.error(f"ORCHESTRATOR.mdパッチエラー: {e}")
            return False
    
    def _patch_commands_md(self) -> bool:
        """COMMANDS.mdに/sc:trinitasコマンドを追加"""
        try:
            cmd_file = self.patch_targets["COMMANDS.md"]
            if not cmd_file.exists():
                logger.warning("COMMANDS.mdが見つかりません")
                return True
            
            with open(cmd_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 既存チェック
            if "/sc:trinitas" in content:
                logger.info("COMMANDS.md は既にパッチ済みです")
                return True
            
            # コマンド定義を追加
            trinitas_command = """
**`/sc:trinitas $ARGUMENTS`**
```yaml
---
command: "/sc:trinitas"
category: "Meta & Orchestration"
purpose: "Trinitas統合メタペルソナによる多角的分析"
wave-enabled: true
performance-profile: "complex"
---
```
- **Auto-Persona**: Springfield, Krukai, Vector (三位一体メタペルソナ)
- **MCP Integration**: Sequential (primary), Context7 (patterns), Magic (UI)
- **Tool Orchestration**: [Read, Grep, Glob, Task, TodoWrite, Analyze]
- **Arguments**: `[operation]`, `[target]`, `--trinitas-brief`, `--trinitas-focus [aspect]`
"""
            
            # Meta & Orchestration Commands セクションを探す
            if "### Meta & Orchestration Commands" in content:
                # セクションの最後に追加
                lines = content.split('\\n')
                insert_index = None
                for i, line in enumerate(lines):
                    if "### Meta & Orchestration Commands" in line:
                        # 次のセクションを探す
                        for j in range(i+1, len(lines)):
                            if lines[j].startswith("##") and j > i:
                                insert_index = j
                                break
                        if not insert_index:
                            insert_index = len(lines)
                        break
                
                if insert_index:
                    lines.insert(insert_index, trinitas_command)
                    content = '\\n'.join(lines)
            else:
                # セクションが見つからない場合は末尾に追加
                content += "\\n" + trinitas_command
            
            with open(cmd_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info("COMMANDS.md パッチ適用完了")
            return True
            
        except Exception as e:
            logger.error(f"COMMANDS.mdパッチエラー: {e}")
            return False
    
    def _patch_modes_md(self) -> bool:
        """MODES.mdにTrinitasモードセクションを追加"""
        try:
            modes_file = self.patch_targets["MODES.md"]
            if not modes_file.exists():
                logger.warning("MODES.mdが見つかりません")
                return True
            
            with open(modes_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 既存チェック
            if "Trinitas Meta-Persona Mode" in content:
                logger.info("MODES.md は既にパッチ済みです")
                return True
            
            # Trinitasモード参照を追加
            if self.has_core_dir:
                # Core/構造の場合
                trinitas_mode = """
---

# Trinitas Meta-Persona Mode

@Modes/TRINITAS.md"""
            else:
                # フラット構造の場合
                trinitas_mode = """
---

# Trinitas Meta-Persona Mode

@Modes/TRINITAS.md"""
            
            content = content.rstrip() + "\\n" + trinitas_mode + "\\n"
            
            with open(modes_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info("MODES.md パッチ適用完了")
            return True
            
        except Exception as e:
            logger.error(f"MODES.mdパッチエラー: {e}")
            return False
    
    def save_state(self, operation: str, status: str, details: Dict) -> bool:
        """操作状態を保存"""
        try:
            state = {
                "patcher_version": self.PATCHER_VERSION,
                "structure_type": "core_dir" if self.has_core_dir else "flat",
                "last_operation": operation,
                "timestamp": datetime.now().isoformat(),
                "status": status,
                "details": details
            }
            
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            logger.error(f"状態保存エラー: {e}")
            return False
    
    def apply_integration(self) -> bool:
        """Trinitas統合を適用"""
        try:
            # 1. SuperClaudeインストール検証
            verified, message = self.verify_superclaude_installation()
            if not verified:
                logger.error(f"SuperClaude検証失敗: {message}")
                return False
            
            logger.info(message)
            
            # 2. ファイル整合性チェック
            integrity = self.verify_file_integrity()
            logger.info(f"ファイル整合性: {integrity}")
            
            # 3. バックアップ作成
            if not self.create_backup():
                logger.error("バックアップ作成に失敗しました")
                return False
            
            # 4. EXTENSIONS.mdの作成/更新
            if not self.create_or_update_extensions_md():
                return False
            
            # 5. CLAUDE.mdのパッチ
            if not self.patch_claude_md():
                return False
            
            # 6. Trinitas拡張のコピー
            if not self.copy_trinitas_extension():
                return False
            
            # 7. コアファイルのパッチ
            if not self.patch_core_files():
                return False
            
            # 8. 状態保存
            self.save_state("apply", "success", {
                "files_patched": list(self.patch_targets.keys()),
                "trinitas_version": "1.1",
                "structure_type": "core_dir" if self.has_core_dir else "flat"
            })
            
            logger.info("Trinitas統合の適用が完了しました！")
            return True
            
        except Exception as e:
            logger.error(f"統合適用エラー: {e}")
            self.save_state("apply", "error", {"error": str(e)})
            return False
    
    def verify_integration(self) -> bool:
        """統合状態を検証"""
        try:
            issues = []
            
            # CLAUDE.mdの確認
            claude_file = self.patch_targets["CLAUDE.md"]
            if claude_file.exists():
                content = claude_file.read_text(encoding='utf-8')
                if "@EXTENSIONS.md" not in content:
                    issues.append("CLAUDE.md に @EXTENSIONS.md 参照がありません")
            else:
                issues.append("CLAUDE.md が見つかりません")
            
            # EXTENSIONS.mdの確認
            if not self.patch_targets["EXTENSIONS.md"].exists():
                issues.append("EXTENSIONS.md が見つかりません")
            
            # Trinitas拡張の確認
            trinitas_path = self.extensions_path / "Trinitas"
            if not trinitas_path.exists():
                issues.append("Trinitas拡張ディレクトリが見つかりません")
            else:
                required_files = ["config.yaml", "personas.md", "character_profiles.md"]
                for file in required_files:
                    if not (trinitas_path / file).exists():
                        issues.append(f"Trinitas/{file} が見つかりません")
            
            # コアファイルの統合確認
            for file_name in ["ORCHESTRATOR.md", "COMMANDS.md", "MODES.md"]:
                file_path = self.patch_targets.get(file_name)
                if file_path and file_path.exists():
                    content = file_path.read_text(encoding='utf-8')
                    if file_name == "COMMANDS.md" and "/sc:trinitas" not in content:
                        issues.append("COMMANDS.md に /sc:trinitas コマンドがありません")
                    elif file_name == "MODES.md" and "Trinitas" not in content:
                        issues.append("MODES.md に Trinitas モード参照がありません")
            
            if issues:
                logger.warning("検証で問題が見つかりました:")
                for issue in issues:
                    logger.warning(f"  - {issue}")
                return False
            else:
                logger.info("Trinitas統合は正常に動作しています")
                return True
            
        except Exception as e:
            logger.error(f"検証エラー: {e}")
            return False
    
    def remove_integration(self) -> bool:
        """Trinitas統合を削除"""
        try:
            # バックアップから復元
            if self.backup_path.exists():
                backups = sorted(self.backup_path.glob("backup_*"), reverse=True)
                if backups:
                    latest_backup = backups[0]
                    backup_info_file = latest_backup / "backup_info.json"
                    
                    if backup_info_file.exists():
                        with open(backup_info_file, 'r', encoding='utf-8') as f:
                            backup_info = json.load(f)
                        
                        # ファイルを復元
                        for name, backup_file in backup_info["files"].items():
                            source = Path(backup_file)
                            target = self.patch_targets[name]
                            if source.exists():
                                shutil.copy2(source, target)
                                logger.info(f"復元: {name}")
            
            # EXTENSIONS.mdを削除
            extensions_file = self.patch_targets["EXTENSIONS.md"]
            if extensions_file.exists():
                extensions_file.unlink()
                logger.info("EXTENSIONS.md を削除しました")
            
            # Trinitas拡張を削除
            trinitas_path = self.extensions_path / "Trinitas"
            if trinitas_path.exists():
                shutil.rmtree(trinitas_path)
                logger.info("Trinitas拡張を削除しました")
            
            # Modesディレクトリのクリーンアップ
            if self.modes_path.exists():
                trinitas_mode = self.modes_path / "TRINITAS.md"
                if trinitas_mode.exists():
                    trinitas_mode.unlink()
                    logger.info("TRINITAS.md を削除しました")
            
            # 状態保存
            self.save_state("remove", "success", {"removed": True})
            
            logger.info("Trinitas統合の削除が完了しました")
            return True
            
        except Exception as e:
            logger.error(f"削除エラー: {e}")
            self.save_state("remove", "error", {"error": str(e)})
            return False

def main():
    """メイン実行関数"""
    parser = argparse.ArgumentParser(
        description="Trinitas Dynamic Patcher v2.1 - フラット構造対応版"
    )
    
    parser.add_argument(
        "command",
        choices=["verify-superclaude", "apply", "verify", "remove", "status"],
        help="実行するコマンド"
    )
    
    parser.add_argument(
        "superclaude_path",
        help="SuperClaudeのルートディレクトリパス"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="詳細ログを表示"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # パッチャー初期化
    patcher = TrinitasPatcherV21(args.superclaude_path)
    
    # コマンド実行
    if args.command == "verify-superclaude":
        verified, message = patcher.verify_superclaude_installation()
        print(message)
        return 0 if verified else 1
    
    elif args.command == "apply":
        if patcher.apply_integration():
            print("\\n✅ Trinitas統合が正常に適用されました！")
            print("\\n次のステップ:")
            print("1. Claude Codeを起動")
            print('2. 以下のコマンドでテスト: claude "/sc:trinitas analyze test"')
            return 0
        else:
            print("\\n❌ Trinitas統合の適用に失敗しました")
            return 1
    
    elif args.command == "verify":
        if patcher.verify_integration():
            print("\\n✅ Trinitas統合は正常に動作しています")
            return 0
        else:
            print("\\n⚠️ Trinitas統合に問題があります")
            return 1
    
    elif args.command == "remove":
        if patcher.remove_integration():
            print("\\n✅ Trinitas統合を削除しました")
            return 0
        else:
            print("\\n❌ Trinitas統合の削除に失敗しました")
            return 1
    
    elif args.command == "status":
        # 統合状態の詳細表示
        print("\\n=== Trinitas Integration Status ===")
        verified, message = patcher.verify_superclaude_installation()
        print(f"\\nSuperClaude: {message}")
        
        print("\\nファイル整合性:")
        integrity = patcher.verify_file_integrity()
        for name, status in integrity.items():
            print(f"  {name}: {'✅' if status else '❌'}")
        
        print("\\n統合状態:")
        if patcher.verify_integration():
            print("  ✅ Trinitas統合は有効です")
        else:
            print("  ❌ Trinitas統合に問題があります")
        
        return 0

if __name__ == "__main__":
    sys.exit(main())
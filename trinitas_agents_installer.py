#!/usr/bin/env python3
"""
Trinitas Agents Installer v3.0
Claude Code Native Agents対応の新世代インストーラー

従来のExtension Systemから、Claude Code Native Agentsへの完全移行を支援
"""

import os
import sys
import shutil
import hashlib
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import logging

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TrinitasAgentsInstaller:
    """Trinitas Agents System v2.0 インストーラー"""
    
    VERSION = "3.0.0"
    
    def __init__(self, claude_path: str = None):
        """
        初期化
        
        Args:
            claude_path: ~/.claude ディレクトリのパス（省略時は自動検出）
        """
        if claude_path:
            self.claude_root = Path(claude_path).resolve()
        else:
            # 自動検出: ~/.claude
            self.claude_root = Path.home() / ".claude"
        
        self.agents_path = self.claude_root / "agents"
        self.backup_path = self.claude_root / ".trinitas_agents_backup"
        
        # Trinitasプロジェクトルート
        self.trinitas_root = Path(__file__).parent
        self.agents_source = self.trinitas_root / "SuperClaude" / "Extensions" / "Trinitas" / "agents"
        
        # インストール対象エージェント
        self.agent_files = [
            "springfield.md",
            "krukai.md", 
            "vector.md",
            "trinitas.md"
        ]
    
    def verify_claude_code_installation(self) -> Tuple[bool, str]:
        """Claude Codeインストール状態を検証"""
        try:
            # ~/.claude ディレクトリの存在確認
            if not self.claude_root.exists():
                return False, f"Claude Codeがインストールされていません: {self.claude_root}が存在しません"
            
            # 基本ファイルの存在確認
            required_files = ["CLAUDE.md", "COMMANDS.md", "PERSONAS.md"]
            missing_files = []
            
            for file in required_files:
                if not (self.claude_root / file).exists():
                    missing_files.append(file)
            
            if missing_files:
                return False, f"Claude Code設定ファイルが不足: {', '.join(missing_files)}"
            
            logger.info(f"Claude Code検証完了: {self.claude_root}")
            return True, f"Claude Codeは正しくインストールされています: {self.claude_root}"
            
        except Exception as e:
            return False, f"検証エラー: {str(e)}"
    
    def verify_agents_source(self) -> Tuple[bool, str]:
        """Trinitasエージェントソースファイルを検証"""
        try:
            if not self.agents_source.exists():
                return False, f"エージェントソースディレクトリが見つかりません: {self.agents_source}"
            
            missing_agents = []
            for agent_file in self.agent_files:
                if not (self.agents_source / agent_file).exists():
                    missing_agents.append(agent_file)
            
            if missing_agents:
                return False, f"エージェントファイルが不足: {', '.join(missing_agents)}"
            
            logger.info("Trinitasエージェントソース検証完了")
            return True, "すべてのTrinitasエージェントファイルが確認されました"
            
        except Exception as e:
            return False, f"ソース検証エラー: {str(e)}"
    
    def create_backup(self) -> bool:
        """既存のエージェントファイルをバックアップ"""
        try:
            if not self.agents_path.exists():
                logger.info("既存のagentsディレクトリが存在しないため、バックアップをスキップ")
                return True
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = self.backup_path / f"backup_{timestamp}"
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            # 既存のTrinitasエージェントをバックアップ
            backed_up_files = []
            for agent_file in self.agent_files:
                existing_file = self.agents_path / agent_file
                if existing_file.exists():
                    backup_file = backup_dir / agent_file
                    shutil.copy2(existing_file, backup_file)
                    backed_up_files.append(agent_file)
            
            if backed_up_files:
                logger.info(f"バックアップ作成完了: {len(backed_up_files)}ファイル → {backup_dir}")
            else:
                logger.info("バックアップ対象ファイルなし")
            
            return True
            
        except Exception as e:
            logger.error(f"バックアップエラー: {e}")
            return False
    
    def install_agents(self) -> bool:
        """Trinitasエージェントファイルをインストール"""
        try:
            # agentsディレクトリ作成
            self.agents_path.mkdir(exist_ok=True)
            
            installed_files = []
            for agent_file in self.agent_files:
                source_file = self.agents_source / agent_file
                target_file = self.agents_path / agent_file
                
                # ファイルコピー
                shutil.copy2(source_file, target_file)
                installed_files.append(agent_file)
                logger.info(f"インストール完了: {agent_file}")
            
            logger.info(f"Trinitasエージェント インストール完了: {len(installed_files)}ファイル")
            return True
            
        except Exception as e:
            logger.error(f"インストールエラー: {e}")
            return False
    
    def verify_installation(self) -> Tuple[bool, List[str]]:
        """インストール状態を検証"""
        try:
            issues = []
            
            # agentsディレクトリの確認
            if not self.agents_path.exists():
                issues.append("agentsディレクトリが存在しません")
                return False, issues
            
            # 各エージェントファイルの確認
            for agent_file in self.agent_files:
                agent_path = self.agents_path / agent_file
                if not agent_path.exists():
                    issues.append(f"{agent_file}が見つかりません")
                else:
                    # ファイル内容の基本チェック
                    content = agent_path.read_text(encoding='utf-8')
                    if "name:" not in content or "description:" not in content:
                        issues.append(f"{agent_file}の形式が不正です")
            
            success = len(issues) == 0
            if success:
                logger.info("Trinitasエージェント インストール検証: 成功")
            else:
                logger.warning(f"インストール検証で {len(issues)} 個の問題を検出")
            
            return success, issues
            
        except Exception as e:
            logger.error(f"検証エラー: {e}")
            return False, [f"検証エラー: {str(e)}"]
    
    def remove_agents(self) -> bool:
        """Trinitasエージェントを削除"""
        try:
            removed_files = []
            
            for agent_file in self.agent_files:
                agent_path = self.agents_path / agent_file
                if agent_path.exists():
                    agent_path.unlink()
                    removed_files.append(agent_file)
                    logger.info(f"削除完了: {agent_file}")
            
            if removed_files:
                logger.info(f"Trinitasエージェント削除完了: {len(removed_files)}ファイル")
            else:
                logger.info("削除対象のTrinitasエージェントが見つかりませんでした")
            
            return True
            
        except Exception as e:
            logger.error(f"削除エラー: {e}")
            return False
    
    def cleanup_legacy_extension(self) -> bool:
        """旧Extension Systemの残存ファイルをクリーンアップ"""
        try:
            cleaned_items = []
            
            # 1. CLAUDE.mdから不適切な参照を削除
            claude_file = self.claude_root / "CLAUDE.md"
            if claude_file.exists():
                content = claude_file.read_text(encoding='utf-8')
                original_content = content
                
                # Extensions参照を削除
                lines_to_remove = [
                    "@Extensions/Trinitas/commands.md",
                    "@Extensions/Trinitas/personas.md"
                ]
                
                for line in lines_to_remove:
                    if line in content:
                        content = content.replace(line + "\n", "")
                        content = content.replace(line, "")
                        cleaned_items.append(f"CLAUDE.md: {line}")
                
                if content != original_content:
                    claude_file.write_text(content, encoding='utf-8')
                    logger.info("CLAUDE.mdから旧Extension参照を削除")
            
            # 2. Extensions/Trinitasディレクトリの削除
            extensions_trinitas = self.claude_root / "Extensions" / "Trinitas"
            if extensions_trinitas.exists():
                shutil.rmtree(extensions_trinitas)
                cleaned_items.append("Extensions/Trinitasディレクトリ")
                logger.info("旧Extension/Trinitasディレクトリを削除")
            
            # 3. EXTENSIONS.mdの削除（Trinitasのみの場合）
            extensions_md = self.claude_root / "EXTENSIONS.md"
            if extensions_md.exists():
                content = extensions_md.read_text(encoding='utf-8')
                if "Trinitas" in content and len(content.split('\n')) < 50:  # 簡易判定
                    # Trinitasのみの可能性が高い場合は削除
                    extensions_md.unlink()
                    cleaned_items.append("EXTENSIONS.md")
                    logger.info("旧EXTENSIONS.mdを削除")
            
            if cleaned_items:
                logger.info(f"レガシーExtension System クリーンアップ完了: {len(cleaned_items)}項目")
            else:
                logger.info("クリーンアップ対象の旧システムファイルなし")
            
            return True
            
        except Exception as e:
            logger.error(f"クリーンアップエラー: {e}")
            return False
    
    def install(self) -> bool:
        """完全インストールプロセス"""
        try:
            logger.info("=== Trinitas Agents System v2.0 インストール開始 ===")
            
            # 1. Claude Code検証
            verified, message = self.verify_claude_code_installation()
            if not verified:
                logger.error(f"Claude Code検証失敗: {message}")
                return False
            logger.info(message)
            
            # 2. ソースファイル検証
            verified, message = self.verify_agents_source()
            if not verified:
                logger.error(f"ソースファイル検証失敗: {message}")
                return False
            logger.info(message)
            
            # 3. バックアップ作成
            if not self.create_backup():
                logger.error("バックアップ作成に失敗")
                return False
            
            # 4. 旧システムクリーンアップ
            if not self.cleanup_legacy_extension():
                logger.warning("旧システムクリーンアップで問題が発生（続行）")
            
            # 5. エージェントインストール
            if not self.install_agents():
                logger.error("エージェントインストールに失敗")
                return False
            
            # 6. インストール検証
            success, issues = self.verify_installation()
            if not success:
                logger.error("インストール検証失敗:")
                for issue in issues:
                    logger.error(f"  - {issue}")
                return False
            
            logger.info("=== Trinitas Agents System v2.0 インストール完了 ===")
            return True
            
        except Exception as e:
            logger.error(f"インストールプロセスエラー: {e}")
            return False

def main():
    """メイン実行関数"""
    parser = argparse.ArgumentParser(
        description="Trinitas Agents Installer v3.0 - Claude Code Native Agents対応"
    )
    
    parser.add_argument(
        "command",
        choices=["install", "verify", "remove", "status", "cleanup"],
        help="実行するコマンド"
    )
    
    parser.add_argument(
        "--claude-path",
        help="~/.claude ディレクトリのパス（省略時は自動検出）"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="詳細ログを表示"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # インストーラー初期化
    installer = TrinitasAgentsInstaller(args.claude_path)
    
    # コマンド実行
    if args.command == "install":
        if installer.install():
            print("\n✅ Trinitas Agents System v2.0 インストール成功！")
            print("\n使用方法:")
            print("1. Claude Codeを起動")
            print('2. 以下のようなタスクでエージェントが自動起動:')
            print('   - "Analyze this system comprehensively" → Trinitas agent')
            print('   - "Plan the project architecture" → Springfield agent') 
            print('   - "Optimize this code" → Krukai agent')
            print('   - "Check for security vulnerabilities" → Vector agent')
            return 0
        else:
            print("\n❌ インストールに失敗しました")
            return 1
    
    elif args.command == "verify":
        success, issues = installer.verify_installation()
        if success:
            print("\n✅ Trinitas Agents は正しくインストールされています")
            return 0
        else:
            print("\n⚠️ インストールに問題があります:")
            for issue in issues:
                print(f"  - {issue}")
            return 1
    
    elif args.command == "remove":
        if installer.remove_agents():
            print("\n✅ Trinitas Agents を削除しました")
            return 0
        else:
            print("\n❌ 削除に失敗しました")
            return 1
    
    elif args.command == "cleanup":
        if installer.cleanup_legacy_extension():
            print("\n✅ 旧Extension Systemファイルをクリーンアップしました")
            return 0
        else:
            print("\n❌ クリーンアップに失敗しました")
            return 1
    
    elif args.command == "status":
        print("\n=== Trinitas Agents System Status ===")
        
        # Claude Code検証
        verified, message = installer.verify_claude_code_installation()
        print(f"\nClaude Code: {message}")
        
        # ソースファイル検証
        verified, message = installer.verify_agents_source()
        print(f"ソースファイル: {message}")
        
        # インストール状態
        success, issues = installer.verify_installation()
        if success:
            print("\nインストール状態: ✅ 正常")
        else:
            print("\nインストール状態: ❌ 問題あり")
            for issue in issues:
                print(f"  - {issue}")
        
        return 0

if __name__ == "__main__":
    sys.exit(main())
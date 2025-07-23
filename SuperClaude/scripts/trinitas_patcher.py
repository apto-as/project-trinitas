#!/usr/bin/env python3
"""
Trinitas Dynamic Patcher v1.0
SuperClaude Extension用の動的パッチシステム

概要:
- SuperClaudeコアファイルへの最小限の非侵入的変更
- Fork互換性を保つ動的統合
- ORCHESTRATOR.mdへのTrinitasメタペルソナ統合
- 安全なロールバック機能

使用例:
    python trinitas_patcher.py install /path/to/superclaude
    python trinitas_patcher.py verify /path/to/superclaude
    python trinitas_patcher.py rollback /path/to/superclaude
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

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TrinitasPatcher:
    """SuperClaude Trinitas拡張の動的パッチシステム"""
    
    def __init__(self, superclaude_root: str):
        self.root = Path(superclaude_root).resolve()
        self.core_path = self.root / "Core"
        self.extensions_path = self.root / "Extensions"
        self.backup_path = self.root / ".trinitas_backup"
        self.state_file = self.root / ".trinitas_state.json"
        
        # パッチ対象ファイル
        self.patch_targets = {
            "CLAUDE.md": self.core_path / "CLAUDE.md",
            "ORCHESTRATOR.md": self.core_path / "ORCHESTRATOR.md",
            "EXTENSIONS.md": self.core_path / "EXTENSIONS.md"
        }
        
        # Trinitasファイル
        self.trinitas_files = {
            "config.yaml": self.extensions_path / "Trinitas" / "config.yaml",
            "commands.md": self.extensions_path / "Trinitas" / "commands.md",
            "README.md": self.extensions_path / "Trinitas" / "README.md"
        }
    
    def validate_environment(self) -> bool:
        """環境の妥当性チェック"""
        try:
            # SuperClaudeルート検証
            if not self.root.exists():
                logger.error(f"SuperClaudeルートが見つかりません: {self.root}")
                return False
            
            # Core/ディレクトリ検証
            if not self.core_path.exists():
                logger.error(f"Core/ディレクトリが見つかりません: {self.core_path}")
                return False
            
            # 必須ファイル検証
            required_files = ["CLAUDE.md", "ORCHESTRATOR.md"]
            for file in required_files:
                file_path = self.core_path / file
                if not file_path.exists():
                    logger.error(f"必須ファイルが見つかりません: {file_path}")
                    return False
            
            logger.info("環境検証完了")
            return True
            
        except Exception as e:
            logger.error(f"環境検証エラー: {e}")
            return False
    
    def create_backup(self) -> bool:
        """現在の状態をバックアップ"""
        try:
            # バックアップディレクトリ作成
            self.backup_path.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = self.backup_path / f"backup_{timestamp}"
            backup_dir.mkdir()
            
            # ファイルバックアップ
            backup_info = {
                "timestamp": timestamp,
                "files": {},
                "checksums": {}
            }
            
            for name, file_path in self.patch_targets.items():
                if file_path.exists():
                    backup_file = backup_dir / name
                    shutil.copy2(file_path, backup_file)
                    
                    # チェックサム計算
                    with open(file_path, 'rb') as f:
                        content = f.read()
                        checksum = hashlib.sha256(content).hexdigest()
                    
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
    
    def patch_claude_md(self) -> bool:
        """CLAUDE.mdに@EXTENSIONS.md参照を追加"""
        try:
            claude_file = self.patch_targets["CLAUDE.md"]
            
            # 現在の内容読み込み
            with open(claude_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 既に@EXTENSIONS.mdが存在するかチェック
            if "@EXTENSIONS.md" in content:
                logger.info("CLAUDE.md は既にパッチ済みです")
                return True
            
            # @EXTENSIONS.mdを末尾に追加
            lines = content.strip().split('\n')
            lines.append("@EXTENSIONS.md")
            
            # ファイル書き込み
            with open(claude_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines) + '\n')
            
            logger.info("CLAUDE.md パッチ完了")
            return True
            
        except Exception as e:
            logger.error(f"CLAUDE.md パッチエラー: {e}")
            return False
    
    def create_extensions_md(self) -> bool:
        """EXTENSIONS.mdファイルを作成"""
        try:
            extensions_file = self.patch_targets["EXTENSIONS.md"]
            
            if extensions_file.exists():
                logger.info("EXTENSIONS.md は既に存在します")
                return True
            
            # EXTENSIONS.mdの内容
            extensions_content = """# EXTENSIONS.md - SuperClaude Extension System

SuperClaude拡張システム - 独立性を保ちながらコア機能を拡張

## Overview

SuperClaude Extension Systemは、コア機能への最小限の変更で、強力な拡張機能を追加できるモジュラーアーキテクチャです。各拡張は独立したディレクトリに配置され、動的に読み込まれます。

## Architecture

```
SuperClaude/
├── Core/                    # SuperClaudeコア（最小限の変更）
│   ├── CLAUDE.md           # エントリーポイント（@EXTENSIONS.md追加）
│   └── EXTENSIONS.md       # 拡張システム管理（このファイル）
└── Extensions/             # 拡張モジュール配置
    └── {ExtensionName}/    # 個別拡張ディレクトリ
        ├── config.yaml     # 拡張設定
        ├── commands.md     # コマンド定義
        ├── personas.md     # ペルソナ定義
        └── README.md       # 拡張ドキュメント
```

## Extension Loading Protocol

### Auto-Discovery Process
1. **Extensions/ ディレクトリスキャン**: 利用可能な拡張を自動検出
2. **config.yaml読み込み**: 各拡張の設定とメタデータを取得
3. **互換性チェック**: SuperClaudeバージョンとの互換性を確認
4. **動的統合**: コマンド、ペルソナ、フラグの動的統合
5. **競合解決**: 名前空間の衝突や機能重複の自動解決

### Extension Configuration Format
```yaml
extension:
  name: "ExtensionName"
  version: "1.0.0"
  description: "Extension description"
  author: "Extension Author"
  
compatibility:
  superclaude_min: "3.0.0"
  superclaude_max: "3.x.x"
  
integration:
  commands:
    - name: "/sc:command"
      file: "commands.md"
      priority: 100
  
  personas:
    - name: "CustomPersona"
      file: "personas.md"
      integration_type: "independent|hierarchical|meta"
  
  flags:
    - name: "--custom-flag"
      description: "Custom flag description"
  
dependencies:
  required: []
  optional: ["Sequential", "Context7"]
  
hooks:
  pre_load: "setup.py"
  post_load: "validate.py"
```

## Currently Loaded Extensions

@Extensions/Trinitas/config.yaml

## Extension Development Guidelines

### Core Principles
- **Independence**: 拡張はSuperClaudeコアに最小限の依存
- **Modularity**: 各拡張は独立して開発・テスト・配布可能
- **Compatibility**: 既存機能との競合を避ける設計
- **Graceful Degradation**: 拡張が無効でもコア機能は正常動作

### File Structure Requirements
```
ExtensionName/
├── config.yaml          # 必須: 拡張メタデータ
├── README.md            # 必須: 拡張ドキュメント
├── commands.md          # オプション: コマンド定義
├── personas.md          # オプション: ペルソナ定義
├── flags.md             # オプション: フラグ定義
├── integration.md       # オプション: 統合ガイド
└── scripts/             # オプション: 自動化スクリプト
    ├── install.py
    ├── validate.py
    └── uninstall.py
```

### Integration Types

#### Independent Extensions
- SuperClaudeコアと並行して動作
- 独自のコマンド空間を使用
- 既存機能への影響なし

#### Hierarchical Extensions  
- 既存ペルソナの上位に位置
- 既存機能を統括・制御
- 高度な統合機能を提供

#### Meta Extensions
- SuperClaudeの動作方式を拡張
- ルーティングロジックの変更
- フレームワーク自体の機能追加

## Extension Management

### Installation
```bash
# 自動インストール
python trinitas_installer.py install /path/to/superclaude

# 手動配置
cp -r ExtensionName/ SuperClaude/Extensions/
```

### Validation
```bash
# 拡張整合性チェック
python trinitas_validator.py check

# 互換性テスト
python trinitas_validator.py compatibility
```

### Updates
```bash
# 拡張更新
python trinitas_updater.py update ExtensionName

# Fork同期
python trinitas_updater.py sync-upstream
```

## Security and Safety

### Validation Rules
- **Config Schema**: config.yamlの厳密なスキーマ検証
- **File Integrity**: 拡張ファイルのハッシュ検証
- **Sandbox Execution**: 拡張スクリプトの安全な実行
- **Permission Control**: 拡張の権限制御

### Conflict Resolution
- **Namespace Protection**: コア機能との名前衝突防止
- **Priority System**: 複数拡張間の優先度制御
- **Graceful Fallback**: 競合時の安全な代替動作

## Troubleshooting

### Common Issues
1. **Extension Not Loading**: config.yamlの検証エラー
2. **Command Conflicts**: 既存コマンドとの名前衝突
3. **Compatibility Issues**: SuperClaudeバージョン不一致
4. **Performance Impact**: 拡張による性能劣化

### Diagnostic Tools
```bash
# 拡張状態診断
python trinitas_diagnostic.py status

# 詳細ログ出力
python trinitas_diagnostic.py --verbose

# 競合検出
python trinitas_diagnostic.py conflicts
```

---

**Extension System v1.0** - 独立性と拡張性を両立する次世代アーキテクチャ

*Built for extensibility, designed for compatibility, engineered for the future.*
"""
            
            # ファイル書き込み
            with open(extensions_file, 'w', encoding='utf-8') as f:
                f.write(extensions_content)
            
            logger.info("EXTENSIONS.md 作成完了")
            return True
            
        except Exception as e:
            logger.error(f"EXTENSIONS.md 作成エラー: {e}")
            return False
    
    def patch_orchestrator_md(self) -> bool:
        """ORCHESTRATOR.mdにTrinitasメタペルソナ統合を追加"""
        try:
            orchestrator_file = self.patch_targets["ORCHESTRATOR.md"]
            
            # 現在の内容読み込み
            with open(orchestrator_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 既にTrinitas統合が存在するかチェック
            if "Trinitas Meta-Persona" in content:
                logger.info("ORCHESTRATOR.md は既にTrinitas統合済みです")
                return True
            
            # Trinitas統合セクションを追加
            trinitas_integration = """

## 🌸 Trinitas Meta-Persona Integration

Enhanced intelligent routing with hierarchical meta-persona control system.

### Meta-Persona Hierarchy Control

**Trinitas Router Integration**: When Trinitas mode is active, the routing system operates under hierarchical meta-persona control.

```yaml
meta_persona_routing:
  when_trinitas_active:
    primary_routing: "Springfield/Krukai/Vector による戦略的ルーティング"
    delegation_control: "メタペルソナが適切な専門家を選出・統制"
    execution_oversight: "三位一体による統合的品質管理"
    
  routing_enhancement:
    strategic_layer: "Springfield - 全体戦略とプロジェクト方向性"
    technical_layer: "Krukai - 技術的最適化と実装品質"
    validation_layer: "Vector - リスク評価と安全性検証"
```

### Enhanced Pattern Recognition

**Trinitas Pattern Detection**: Meta-persona system enhances pattern recognition with compound intelligence.

```yaml
trinitas_pattern_enhancement:
  complexity_assessment:
    meta_analysis: "三視点による複合的複雑度評価"
    strategic_complexity: "Springfield - プロジェクト影響度・長期性"
    technical_complexity: "Krukai - 実装難易度・品質要件"
    risk_complexity: "Vector - セキュリティ・安全性リスク"
    
  domain_identification:
    meta_domain_mapping: "複数ドメインの相互関係分析"
    strategic_domains: [project_management, architecture, documentation]
    technical_domains: [implementation, optimization, quality]
    risk_domains: [security, testing, validation]
```

### Meta-Persona Routing Table

| Pattern | Trinitas Response | Meta-Controller | Auto-Activates |
|---------|------------------|-----------------|-----------------|
| "comprehensive analysis" | Springfield主導 | strategic_oversight | architect, mentor, analyzer |
| "optimal implementation" | Krukai主導 | technical_excellence | performance, backend, refactorer |
| "security assessment" | Vector主導 | risk_management | security, analyzer, qa |
| "system design" | 三位一体統合 | coordinated_analysis | All relevant personas |

### Delegation Intelligence Enhancement

**Trinitas Delegation Control**: Meta-persona system enhances delegation decisions with strategic oversight.

```yaml
meta_delegation_protocol:
  delegation_decision_matrix:
    springfield_criteria: "戦略的重要度・チーム影響・長期保守性"
    krukai_criteria: "技術的複雑度・品質基準・パフォーマンス要件"
    vector_criteria: "リスクレベル・セキュリティ要件・安全性基準"
    
  enhanced_specialization:
    meta_oversight: "各専門家の作業を適切なメタペルソナが監督"
    quality_assurance: "三位一体による統合的品質検証"
    conflict_resolution: "メタペルソナレベルでの意思決定調停"
```

### Auto-Activation Enhancement

**Trinitas Auto-Activation**: Enhanced auto-activation with meta-persona intelligence.

```yaml
trinitas_auto_activation:
  threshold_enhancement:
    base_threshold: 0.9  # Trinitas auto-activation threshold
    domain_multipliers:
      multi_domain_analysis: 1.2
      comprehensive_scope: 1.1
      enterprise_scale: 1.15
      
  trigger_conditions:
    complexity_triggers:
      - "複合ドメイン分析要求"
      - "企業規模プロジェクト"
      - "包括的システム評価"
    keyword_triggers:
      - "comprehensive", "systematically", "thoroughly"
      - "enterprise", "large-scale", "multi-stage"
      - "strategic", "optimize", "analyze"
```

---

**Trinitas Integration v1.0** - SuperClaudeの知性を三位一体の力で拡張

*"Springfield の戦略、Krukai の技術、Vector のリスク管理 - 統合された完璧性"*

"""
            
            # コンテンツ末尾に追加
            updated_content = content.rstrip() + trinitas_integration
            
            # ファイル書き込み
            with open(orchestrator_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            logger.info("ORCHESTRATOR.md Trinitas統合完了")
            return True
            
        except Exception as e:
            logger.error(f"ORCHESTRATOR.md パッチエラー: {e}")
            return False
    
    def ensure_trinitas_structure(self) -> bool:
        """Trinitas拡張構造の確保"""
        try:
            # Extensions/Trinitas/ ディレクトリ作成
            trinitas_dir = self.extensions_path / "Trinitas"
            trinitas_dir.mkdir(parents=True, exist_ok=True)
            
            # 必要なファイルが存在するかチェック
            missing_files = []
            for name, file_path in self.trinitas_files.items():
                if not file_path.exists():
                    missing_files.append(name)
            
            if missing_files:
                logger.warning(f"Trinitasファイルが不足: {missing_files}")
                logger.info("必要なファイルを手動で配置してください")
            else:
                logger.info("Trinitas拡張構造確認完了")
            
            return True
            
        except Exception as e:
            logger.error(f"Trinitas構造確保エラー: {e}")
            return False
    
    def save_state(self, operation: str, status: str) -> bool:
        """パッチ状態の保存"""
        try:
            state = {
                "operation": operation,
                "status": status,
                "timestamp": datetime.now().isoformat(),
                "version": "1.0.0",
                "files_modified": list(self.patch_targets.keys())
            }
            
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            logger.error(f"状態保存エラー: {e}")
            return False
    
    def install(self) -> bool:
        """Trinitas拡張のインストール"""
        logger.info("Trinitas拡張インストール開始...")
        
        # 環境検証
        if not self.validate_environment():
            return False
        
        # バックアップ作成
        if not self.create_backup():
            return False
        
        try:
            # パッチ適用
            if not self.patch_claude_md():
                return False
            
            if not self.create_extensions_md():
                return False
            
            if not self.patch_orchestrator_md():
                return False
            
            if not self.ensure_trinitas_structure():
                return False
            
            # 状態保存
            self.save_state("install", "completed")
            
            logger.info("✅ Trinitas拡張インストール完了")
            logger.info("🔧 SuperClaudeでの使用例:")
            logger.info("   /sc:trinitas analyze user-authentication")
            logger.info("   /sc:trinitas implement feature --trinitas-brief")
            
            return True
            
        except Exception as e:
            logger.error(f"インストールエラー: {e}")
            self.save_state("install", "failed")
            return False
    
    def verify(self) -> bool:
        """インストール状況の検証"""
        logger.info("Trinitas拡張状況検証中...")
        
        try:
            issues = []
            
            # ファイル存在確認
            for name, file_path in self.patch_targets.items():
                if not file_path.exists():
                    issues.append(f"❌ {name} が見つかりません: {file_path}")
                else:
                    logger.info(f"✅ {name} 確認済み")
            
            # Trinitasファイル確認
            for name, file_path in self.trinitas_files.items():
                if not file_path.exists():
                    issues.append(f"⚠️  Trinitas/{name} が見つかりません: {file_path}")
                else:
                    logger.info(f"✅ Trinitas/{name} 確認済み")
            
            # 状態ファイル確認
            if self.state_file.exists():
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                logger.info(f"📊 前回の操作: {state.get('operation')} ({state.get('status')})")
            
            if issues:
                logger.warning("検出された問題:")
                for issue in issues:
                    logger.warning(f"  {issue}")
                return False
            else:
                logger.info("✅ Trinitas拡張は正常にインストールされています")
                return True
                
        except Exception as e:
            logger.error(f"検証エラー: {e}")
            return False
    
    def rollback(self) -> bool:
        """最新バックアップからのロールバック"""
        logger.info("Trinitas拡張ロールバック開始...")
        
        try:
            if not self.backup_path.exists():
                logger.error("バックアップが見つかりません")
                return False
            
            # 最新バックアップを検索
            backup_dirs = [d for d in self.backup_path.iterdir() 
                          if d.is_dir() and d.name.startswith("backup_")]
            
            if not backup_dirs:
                logger.error("有効なバックアップが見つかりません")
                return False
            
            latest_backup = max(backup_dirs, key=lambda x: x.name)
            logger.info(f"ロールバック対象: {latest_backup}")
            
            # バックアップ情報読み込み
            backup_info_file = latest_backup / "backup_info.json"
            with open(backup_info_file, 'r', encoding='utf-8') as f:
                backup_info = json.load(f)
            
            # ファイル復元
            for name, backup_file_path in backup_info["files"].items():
                target_file = self.patch_targets[name]
                if Path(backup_file_path).exists():
                    shutil.copy2(backup_file_path, target_file)
                    logger.info(f"復元完了: {name}")
            
            # EXTENSIONS.mdを削除（バックアップに存在しない場合）
            extensions_file = self.patch_targets["EXTENSIONS.md"]
            if extensions_file.exists() and "EXTENSIONS.md" not in backup_info["files"]:
                extensions_file.unlink()
                logger.info("EXTENSIONS.md 削除完了")
            
            # 状態保存
            self.save_state("rollback", "completed")
            
            logger.info("✅ ロールバック完了")
            return True
            
        except Exception as e:
            logger.error(f"ロールバックエラー: {e}")
            self.save_state("rollback", "failed")
            return False

def main():
    """メイン実行関数"""
    parser = argparse.ArgumentParser(
        description="Trinitas Dynamic Patcher - SuperClaude Extension Integration Tool"
    )
    parser.add_argument(
        "operation",
        choices=["install", "verify", "rollback"],
        help="実行する操作"
    )
    parser.add_argument(
        "superclaude_path",
        help="SuperClaudeルートディレクトリのパス"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="詳細ログ出力"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # パッチャー初期化
    patcher = TrinitasPatcher(args.superclaude_path)
    
    # 操作実行
    if args.operation == "install":
        success = patcher.install()
    elif args.operation == "verify":
        success = patcher.verify()
    elif args.operation == "rollback":
        success = patcher.rollback()
    else:
        logger.error(f"未知の操作: {args.operation}")
        return 1
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
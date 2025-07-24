# EXTENSIONS.md - SuperClaude Extension System

SuperClaude拡張システム - 独立性を保ちながらコア機能を拡張

## Overview

SuperClaude Extension Systemは、コア機能への最小限の変更で、強力な拡張機能を追加できるモジュラーアーキテクチャです。各拡張は独立したディレクトリに配置され、動的に読み込まれます。

## Architecture

```
~/.claude/                   # SuperClaudeルート（フラット構造）
├── CLAUDE.md               # エントリーポイント（@EXTENSIONS.md追加）
├── EXTENSIONS.md           # 拡張システム管理（このファイル）
├── COMMANDS.md             # コマンド定義
├── MODES.md                # モード定義
├── PERSONAS.md             # ペルソナ定義
├── Modes/                  # モードファイル
│   └── TRINITAS.md        # Trinitasメタペルソナモード
└── Extensions/             # 拡張モジュール配置
    └── {ExtensionName}/    # 個別拡張ディレクトリ
        ├── config.yaml     # 拡張設定
        ├── commands.md     # コマンド定義
        ├── personas.md     # ペルソナ定義
        └── README.md       # 拡張ドキュメント
```

## Extension Loading Protocol

### Auto-Discovery Process
1. **Extensions/ ディレクトリスキャン**: ~/.claude/Extensions/ 内の利用可能な拡張を自動検出
2. **config.yaml読み込み**: 各拡張の設定とメタデータを取得
3. **互換性チェック**: SuperClaudeバージョンとの互換性を確認（フラット構造対応）
4. **動的統合**: コマンド、ペルソナ、フラグのフラット構造への動的統合
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
# 自動インストール（フラット構造対応）
python trinitas_patcher_v2_1.py apply ~/.claude

# 手動配置
cp -r ExtensionName/ ~/.claude/Extensions/
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
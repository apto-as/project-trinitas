# Trinitas Extension Installation Guide v2.0

**改善版インストールガイド - 二重管理問題を解消**

---

## 📋 Prerequisites - 事前要件

### 1. SuperClaude のインストール（必須）

**重要**: Trinitasをインストールする**前に**、SuperClaude v3.0.0以上が正しくインストールされている必要があります。

#### SuperClaude インストール確認
```bash
# SuperClaudeの存在確認
ls ~/.claude/
# 以下のファイルが存在することを確認:
# - CLAUDE.md
# - COMMANDS.md
# - ORCHESTRATOR.md
# - PERSONAS.md
# - MODES.md
```

#### SuperClaude が未インストールの場合
```bash
# SuperClaude公式インストーラーを使用
curl -fsSL https://superclaude.com/install.sh | sh

# または手動インストール
git clone https://github.com/NomenAK/SuperClaude.git
cd SuperClaude
python install.py
```

### 2. System Requirements
```yaml
requirements:
  claude_code: "v1.0.0 以上"
  python: "3.8+ (スクリプト実行用)"
  git: "プロジェクトクローン用"
  yaml: "pip install pyyaml (設定ファイル解析用)"
```

---

## 🚀 Installation Process - インストール手順

### Step 1: SuperClaude インストール検証

```bash
# Trinitasプロジェクトをクローン
git clone https://github.com/apto-as/project-trinitas.git
cd project-trinitas/SuperClaude

# SuperClaudeのインストール状態を確認
python scripts/trinitas_patcher_v2.py verify-superclaude ~/.claude
```

**期待される出力**:
```
SuperClaudeは正しくインストールされています。SuperClaude v3.0.0+ を検出
```

### Step 2: Trinitas 統合の適用

```bash
# 改善版パッチャーを使用してTrinitas統合を適用
python scripts/trinitas_patcher_v2.py apply ~/.claude
```

**実行内容**:
1. ✅ SuperClaudeインストール検証
2. ✅ ファイル整合性チェック  
3. ✅ 自動バックアップ作成
4. ✅ EXTENSIONS.mdを動的に読み込み（二重管理解消）
5. ✅ Trinitas拡張のインストール
6. ✅ コアファイルへの最小限の統合

### Step 3: インストール検証

```bash
# 統合状態の確認
python scripts/trinitas_patcher_v2.py verify ~/.claude

# 詳細なステータス確認
python scripts/trinitas_patcher_v2.py status ~/.claude
```

### Step 4: 動作確認

```bash
# Claude Code でTrinitasコマンドをテスト
claude "/sc:trinitas analyze test-project"

# 簡潔モードでテスト
claude "/sc:trinitas analyze api-design --trinitas-brief"
```

---

## 🔧 Improved Patcher Features - 改善されたパッチャーの特徴

### 1. 動的ファイル読み込み（二重管理の解消）

**旧バージョンの問題**:
```python
# ❌ 問題: EXTENSIONS.mdの内容がハードコーディング
extensions_content = """# EXTENSIONS.md - SuperClaude Extension System
...（ハードコーディングされた内容）...
"""
```

**改善版（v2.0）**:
```python
# ✅ 解決: ファイルから動的に読み込み
def load_extensions_content(self) -> Optional[str]:
    """EXTENSIONS.mdの内容を動的に読み込み"""
    extensions_source = self.trinitas_root / "Core" / "EXTENSIONS.md"
    with open(extensions_source, 'r', encoding='utf-8') as f:
        content = f.read()
    return content
```

### 2. SuperClaude インストール検証

```python
def verify_superclaude_installation(self) -> Tuple[bool, str]:
    """SuperClaudeのインストール状態を検証"""
    # 必須ファイルの存在確認
    # バージョン互換性チェック
    # ディレクトリ構造の検証
```

### 3. ファイル整合性チェック

```python
def verify_file_integrity(self) -> Dict[str, bool]:
    """ファイル整合性をチェック"""
    # ソースファイルの存在確認
    # ハッシュ値による変更検出
    # 設定ファイルの妥当性検証
```

### 4. 安全なロールバック機能

```bash
# 問題が発生した場合の復元
python scripts/trinitas_patcher_v2.py remove ~/.claude

# バックアップは自動的に作成され、以下に保存されます:
~/.claude/.trinitas_backup/backup_YYYYMMDD_HHMMSS/
```

---

## 📂 File Structure After Installation

```
~/.claude/
├── Core/
│   ├── CLAUDE.md          # @EXTENSIONS.md 参照を追加
│   ├── COMMANDS.md        # /sc:trinitas コマンドを追加
│   ├── MODES.md           # Trinitasモード参照を追加
│   ├── ORCHESTRATOR.md    # Trinitas統合セクションを追加
│   ├── EXTENSIONS.md      # 動的に生成（二重管理なし）
│   └── Modes/
│       └── TRINITAS.md    # Trinitasモード定義
└── Extensions/
    └── Trinitas/
        ├── config.yaml
        ├── personas.md
        ├── character_profiles.md
        ├── coordination.md
        ├── commands.md
        ├── integration.md
        ├── modes.md
        ├── performance_optimization.md
        ├── README.md
        └── tests/
```

---

## ⚠️ Important Notes - 重要な注意事項

### インストール順序の重要性

1. **必ず先にSuperClaudeをインストール**
   - Trinitasは拡張システムであり、ベースとなるSuperClaudeが必要
   - SuperClaude v3.0.0以上が必須

2. **改善版パッチャー（v2.0）を使用**
   - `trinitas_patcher_v2.py` を使用（二重管理問題を解消）
   - 旧バージョンの `trinitas_patcher.py` は使用しない

3. **動的ファイル管理の利点**
   - EXTENSIONS.mdの変更が即座に反映される
   - メンテナンス性の大幅向上
   - バージョン管理の一元化

---

## 🔧 Advanced Usage - 上級者向け使用方法

### カスタムパス指定
```bash
# SuperClaudeが標準以外の場所にある場合
python scripts/trinitas_patcher_v2.py apply /custom/path/to/superclaude

# 詳細ログ付き実行
python scripts/trinitas_patcher_v2.py apply ~/.claude --verbose
```

### 部分的な統合確認
```bash
# 特定ファイルの統合状態確認
grep -n "trinitas" ~/.claude/Core/COMMANDS.md
grep -n "EXTENSIONS" ~/.claude/CLAUDE.md
```

### 手動パッチ適用（非推奨）
改善版パッチャーは自動化されていますが、手動で変更を確認したい場合：

```bash
# CLAUDE.md への追加内容を確認
diff ~/.claude/CLAUDE.md ~/.claude/.trinitas_backup/backup_*/CLAUDE.md

# EXTENSIONS.md の内容を確認
cat project-trinitas/SuperClaude/Core/EXTENSIONS.md
```

---

## ❓ FAQ - よくある質問

### Q1: なぜSuperClaudeを先にインストールする必要があるのですか？

**A**: Trinitasは拡張システムであり、以下の理由でベースシステムが必要です：
- コアファイル（CLAUDE.md, COMMANDS.md等）への統合が必要
- SuperClaudeのディレクトリ構造に依存
- バージョン互換性の確認が必要

### Q2: 二重管理問題とは何ですか？

**A**: 旧バージョンでは、EXTENSIONS.mdの内容が2箇所に存在していました：
1. `Core/EXTENSIONS.md` ファイル
2. `trinitas_patcher.py` 内のハードコーディング

これにより、片方だけ更新されて不整合が発生するリスクがありました。v2.0ではファイルから動的に読み込むことで解決しています。

### Q3: アップデート時はどうすればよいですか？

```bash
# プロジェクトを更新
cd project-trinitas
git pull

# 再度統合を適用（自動的に更新される）
cd SuperClaude
python scripts/trinitas_patcher_v2.py apply ~/.claude
```

---

## 🐛 Troubleshooting - トラブルシューティング

### エラー: "SuperClaudeルートが見つかりません"
```bash
# 解決策: 正しいパスを指定
python scripts/trinitas_patcher_v2.py verify-superclaude /correct/path/to/superclaude
```

### エラー: "必須ファイルが不足しています"
```bash
# 解決策: SuperClaudeの再インストール
# SuperClaude公式の手順に従って再インストール
```

### エラー: "EXTENSIONS.mdソースファイルが見つかりません"
```bash
# 解決策: Trinitasプロジェクトの完全性を確認
git status
git checkout -- Core/EXTENSIONS.md  # ファイルを復元
```

---

## 🎉 Installation Complete!

インストールが成功したら、以下のコマンドで三位一体の分析を体験できます：

```bash
# Springfield（戦略）、Krukai（技術）、Vector（リスク）の統合分析
claude "/sc:trinitas analyze my-project"

# 簡潔なYAML形式での分析
claude "/sc:trinitas design architecture --trinitas-brief"

# 特定の視点を強調
claude "/sc:trinitas implement feature --trinitas-focus technical"
```

---

**Installation Guide Version**: 2.0  
**Compatible with**: Trinitas v1.1, SuperClaude v3.0.0+  
**Last Updated**: 2025-07-23  

*"適切な順序と動的管理で、完璧な統合を実現"*
# Trinitas Extension for SuperClaude

**三位一体メタペルソナシステム** - Springfield, Krukai, Vector による統合知性

## ✨ Phase 6完了 - Claude Code Native Agents

**最新バージョン**: v2.0 (Claude Code Native Agents)  
**リリース日**: 2025-01-26  
**革命的変更**: Extension SystemからClaude Code Native Agentsへの完全移行完了

## Overview

Trinitasは、SuperClaudeフレームワークに統合される上位メタペルソナシステムです。『ドールズフロントライン2：エクシリウム』のSpringfield、Krukai、Vectorの特性を活かし、戦略（Strategy）、技術（Technical）、リスク（Risk）の三角分析による包括的な開発支援を提供します。

**Phase 4新機能**: 伝説的な「Tri-Core」エンジニアの背景ストーリーと深層心理プロファイルにより、各ペルソナの技術判断と性格的一貫性が大幅に強化されました。

## Key Features

### 🌸 Springfield - Strategic Oversight
- **役割**: 戦略的思考とチーム調整
- **専門領域**: アーキテクチャ設計、長期戦略、プロジェクト管理
- **統括ペルソナ**: architect, mentor, scribe, devops
- **特徴**: 温かく包容力のある調整役、長期的視点での意思決定

### ⚡ Krukai - Technical Excellence  
- **役割**: 技術的完璧性の追求
- **専門領域**: パフォーマンス最適化、実装品質、技術革新
- **統括ペルソナ**: performance, backend, refactorer, frontend
- **特徴**: 完璧主義で効率重視、妥協を許さない品質基準

### 🔥 Vector - Risk Management
- **役割**: リスク評価と品質保証
- **専門領域**: セキュリティ分析、脆弱性検出、品質検証
- **統括ペルソナ**: security, analyzer, qa
- **特徴**: 悲観的だが的確な防御戦略、徹底的なリスク分析

## Installation

### Prerequisites
- SuperClaude v3.0.0 以上（先にインストールが必要）
- Claude Code CLI
- Python 3.8+ (自動化スクリプト用)
- PyYAML (`pip install pyyaml`)

### Quick Install (v2.0 - Native Agents)
```bash
# 1. Trinitasプロジェクトをクローン
git clone https://github.com/apto-as/project-trinitas.git
cd project-trinitas

# 2. 自動インストール（推奨）
python trinitas_agents_installer.py install

# 3. インストール検証
python trinitas_agents_installer.py verify
```

### Manual Install (Advanced Users)
```bash
# 手動でエージェントファイルをコピー
mkdir -p ~/.claude/agents
cp SuperClaude/Extensions/Trinitas/agents/*.md ~/.claude/agents/

# インストール確認
ls ~/.claude/agents/
```

### Verification
```bash
# インストール状態確認
python trinitas_agents_installer.py status

# Claude Codeでのエージェント確認
claude "List available agents" # エージェント一覧表示（開発中機能）
```

## Usage Examples - Automatic Agent Selection

### Comprehensive Analysis (Trinitas Agent)
```bash
# 包括的システム分析（Trinitasエージェント自動選択）
claude "Analyze this system comprehensively from all perspectives"

# マルチドメイン要求（Trinitasエージェント対象）
claude "Review this code for strategy, performance, and security"
```

### Strategic Planning (Springfield Agent)
```bash
# 戦略的計画（Springfieldエージェント自動選択）
claude "Help me plan the architecture for this project"

# 長期戦略（Springfieldエージェント対象）
claude "Design a scalable system architecture for microservices"
```

### Technical Optimization (Krukai Agent)
```bash
# 技術最適化（Krukaiエージェント自動選択）
claude "Optimize this code for maximum performance"

# 品質改善（Krukaiエージェント対象）
claude "Refactor this code to improve maintainability and performance"
```

### Security Assessment (Vector Agent)
```bash
# セキュリティ評価（Vectorエージェント自動選択）
claude "Check this system for security vulnerabilities"

# リスク分析（Vectorエージェント対象）
claude "Analyze potential risks and edge cases in this implementation"
```

## Configuration

### Extension Settings
```yaml
# SuperClaude/Extensions/Trinitas/config.yaml
settings:
  default_mode: "full"        # full | brief
  auto_delegate: true         # 自動ペルソナ委任
  preserve_context: true      # コンテキスト保持
  token_optimization: true    # トークン最適化
```

### User Preferences
```bash
# デフォルトモード設定
export TRINITAS_DEFAULT_MODE=brief

# 自動活性化閾値
export TRINITAS_AUTO_THRESHOLD=0.9

# 並列分析有効化
export TRINITAS_PARALLEL_ANALYSIS=true
```

## Integration with SuperClaude

### Hierarchical Persona System
Trinitasは既存SuperClaudeペルソナの上位統制システムとして動作：

```
Trinitas Meta-Personas
├── Springfield (Strategy)
│   ├── architect (primary)
│   ├── mentor (primary)  
│   ├── scribe (secondary)
│   └── devops (secondary)
├── Krukai (Technical)
│   ├── performance (primary)
│   ├── backend (primary)
│   ├── refactorer (secondary)
│   └── frontend (secondary)
└── Vector (Risk)
    ├── security (primary)
    ├── analyzer (primary)
    └── qa (secondary)
```

### Command Integration
```bash
# Trinitas独自コマンド
/sc:trinitas <operation> <target>

# 既存コマンドとの統合
/sc:analyze <target> --trinitas
/sc:implement <feature> --trinitas
/sc:improve <system> --trinitas
```

### Flag Compatibility
Trinitasは全てのSuperClaudeフラグと互換：

```bash
# MCP統合
/sc:trinitas analyze --seq --c7 --magic

# Wave Mode
/sc:trinitas improve --wave-mode force

# Thinking Depth
/sc:trinitas troubleshoot --think-hard
```

## Advanced Features

### Auto-Activation
```yaml
auto_activation_triggers:
  complexity_threshold: 0.9
  multi_domain_analysis: true
  comprehensive_review: true
  enterprise_scale: true
```

### Wave Integration
```yaml
wave_strategies:
  progressive: "段階的改善"
  systematic: "体系的分析"  
  adaptive: "適応的最適化"
  enterprise: "企業規模対応"
```

### Delegation Intelligence
```yaml
delegation_criteria:
  springfield: "戦略性・影響度"
  krukai: "技術的複雑性"
  vector: "リスクレベル"
```

## Troubleshooting

### Common Issues

#### 1. Command Not Found
```bash
# 拡張が正しく読み込まれているか確認
ls SuperClaude/Extensions/Trinitas/

# 設定ファイルの検証
python scripts/trinitas_validator.py check
```

#### 2. Persona Hierarchy Not Working
```bash
# ORCHESTRATOR.mdの変更確認
grep -n "trinitas" SuperClaude/Core/ORCHESTRATOR.md

# 階層制御の検証
/sc:trinitas analyze test --trinitas-brief
```

#### 3. Performance Issues
```bash
# キャッシュクリア
rm -rf ~/.superclaude/cache/trinitas/

# 並列処理無効化
export TRINITAS_PARALLEL_ANALYSIS=false
```

### Diagnostic Tools
```bash
# 統合状態診断
python scripts/trinitas_diagnostic.py status

# 詳細ログ出力
python scripts/trinitas_diagnostic.py --verbose

# 競合検出
python scripts/trinitas_diagnostic.py conflicts
```

## Development

### Extension Structure
```
Trinitas/
├── config.yaml          # 拡張設定
├── commands.md           # コマンド定義
├── personas.md           # ペルソナ定義（オプション）
├── README.md            # このファイル
└── scripts/             # 自動化スクリプト
    ├── trinitas_installer.py
    ├── trinitas_validator.py
    ├── trinitas_diagnostic.py
    └── trinitas_updater.py
```

### Contributing
1. Fork the repository
2. Create feature branch
3. Implement changes
4. Add tests
5. Submit pull request

### Testing
```bash
# 単体テスト
python -m pytest tests/

# 統合テスト
python scripts/integration_test.py

# 性能テスト
python scripts/performance_test.py
```

## Roadmap

### v1.1 (Next Release)
- [ ] 高度なコンフリクト解決
- [ ] カスタムペルソナ作成支援
- [ ] Web UIダッシュボード

### v1.2 (Future)
- [ ] 他AI CLIとの互換性
- [ ] プラグインアーキテクチャ
- [ ] 学習型分析改善

### v2.0 (Long-term)
- [ ] 完全自律型分析
- [ ] 予測的問題検出
- [ ] チーム協調機能

## Support

### Documentation
- [User Guide](docs/user-guide.md)
- [Developer Guide](docs/developer-guide.md) 
- [API Reference](docs/api-reference.md)

### Community
- GitHub Issues: Bug reports and feature requests
- GitHub Discussions: General questions and ideas
- Email: trinitas-support@example.com

### License
MIT License - see [LICENSE](LICENSE) file for details

---

**Trinitas v1.0** - 三位一体の知性で、開発の新次元を

*"Springfield の戦略、Krukai の技術、Vector のリスク管理 - 統合された完璧性"*
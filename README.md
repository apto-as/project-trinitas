# Claude Code

**Transform your coding experience with Claude's intelligence**

Claude Code is the official Anthropic CLI for [Claude](https://claude.ai), bringing AI-powered development directly to your terminal. Write, debug, and improve code with Claude's assistance across any programming language or framework.

## ✨ Latest: Trinitas Agents System v2.0

Now featuring the **Claude Code Native Agents** - revolutionary implementation providing 95% recognition rate and seamless integration:

- 🌸 **Springfield** - Strategic oversight and project coordination
- ⚡ **Krukai** - Technical excellence and performance optimization  
- 🔥 **Vector** - Risk management and security analysis
- 🌟 **Trinitas** - Unified multi-perspective analysis

**Revolutionary Improvement**: Native Claude Code agents with automatic task detection, replacing complex extension system with intelligent agent selection.

## Quick Start

1. **Install Claude Code**
   ```bash
   curl -fsSL https://claude.ai/install.sh | sh
   ```

2. **Get your API key** from [console.anthropic.com](https://console.anthropic.com)

3. **Start coding with Claude**
   ```bash
   claude "Help me build a REST API in Python"
   ```

## What Claude Code Does

- **Code Generation**: Write complete functions, classes, or entire projects
- **Code Analysis**: Understand complex codebases and identify issues
- **Debugging**: Find and fix bugs with AI assistance
- **Refactoring**: Improve code structure and performance
- **Documentation**: Generate comprehensive docs and comments
- **Multi-Language Support**: Works with any programming language
- **Project-Aware**: Understands your codebase context

## Key Features

### 🧠 Intelligent Context
Claude Code automatically understands your project structure, dependencies, and coding patterns to provide relevant, contextual assistance.

### 🔧 Direct File Operations
- Read, write, and edit files directly
- Run terminal commands
- Install packages and dependencies
- Execute and test your code

### 🎯 Project-Aware Analysis
- Analyzes your entire codebase
- Understands relationships between files
- Provides architectural insights
- Suggests improvements based on best practices

### 🚀 Advanced Extensions
- **Trinitas Agents System**: Intelligent multi-perspective analysis with automatic agent selection
- **MCP Integration**: Context7, Sequential, Magic, and Playwright server support
- **SuperClaude Framework**: Enhanced command system with intelligent routing

## Use Cases

- **New Projects**: "Create a React app with TypeScript and Tailwind"
- **Bug Fixes**: "Debug this error in my Python script"
- **Code Review**: "Review this function for potential issues"
- **Optimization**: "Improve the performance of this algorithm"
- **Learning**: "Explain how this code works"
- **Architecture**: "Design a scalable microservices architecture"

## Documentation

- [Quick Start Guide](https://docs.anthropic.com/en/docs/claude-code/quickstart)
- [Complete Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Claude Code Sub-Agents](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
- [Trinitas Agents System](SuperClaude/Extensions/Trinitas/README.md)
- [Command Reference](https://docs.anthropic.com/en/docs/claude-code/cli-reference)

## Installation 📦

SuperClaude installation is a **two-step process**:
1. First install the Python package
2. Then run the installer to set up Claude Code integration

### Step 1: Install the Package

**Option A: From PyPI (Recommended)**
```bash
uv add SuperClaude
```

**Option B: From Source**
```bash
git clone https://github.com/SuperClaude-Org/SuperClaude_Framework.git
cd SuperClaude
uv sync
```
### 🔧 UV / UVX Setup Guide

SuperClaude v3 also supports installation via [`uv`](https://github.com/astral-sh/uv) (a faster, modern Python package manager) or `uvx` for cross-platform usage.

### 🌀 Install with `uv`

Make sure `uv` is installed:

## Trinitas Agents Installation 🌸

For enhanced multi-perspective AI analysis, install the Trinitas Agents System:

### Prerequisites
- Claude Code must be installed and configured
- Python 3.8+ required

### Installation Steps

1. **Clone the Trinitas Project**
   ```bash
   git clone https://github.com/apto-as/project-trinitas.git
   cd project-trinitas
   ```

2. **Install Trinitas Agents**
   ```bash
   python trinitas_agents_installer.py install
   ```

3. **Verify Installation**
   ```bash
   python trinitas_agents_installer.py verify
   ```

### Usage Examples

Once installed, Trinitas agents will automatically activate based on your task descriptions:

- **Comprehensive Analysis**: "Analyze this system from multiple perspectives"
- **Strategic Planning**: "Plan the architecture for this project"  
- **Performance Optimization**: "Optimize this code for better performance"
- **Security Assessment**: "Check for security vulnerabilities in this code"

### Uninstall
```bash
python trinitas_agents_installer.py remove
```

## Example Session

```bash
$ claude "Create a simple web server"
I'll create a simple web server for you. What language would you prefer?

$ claude "Python with Flask"
I'll create a Python Flask web server:

[Creates app.py with Flask server]
[Creates requirements.txt]
[Explains how to run the server]
```

## Advanced Usage

### Trinitas Agents Automatic Selection
```bash
# Comprehensive multi-perspective analysis (triggers Trinitas agent)
claude "Analyze this system comprehensively from all angles"

# Strategic planning (triggers Springfield agent)
claude "Help me plan the architecture for this project"

# Technical optimization (triggers Krukai agent)
claude "Optimize this code for maximum performance"

# Security assessment (triggers Vector agent)
claude "Check this system for security vulnerabilities"
```

### Project Management
```bash
# Analyze entire codebase
claude "/sc:analyze @."

# Build with optimizations  
claude "/sc:build --performance"

# Implement new features
claude "/sc:implement user-dashboard"
```

## Privacy & Security

- Your code stays on your machine - Claude only sees what you explicitly share
- All API calls are encrypted
- No persistent storage of your code on Anthropic's servers
- Full control over what files and information Claude can access

## Requirements

- **Operating System**: macOS, Linux, or Windows (WSL)
- **Node.js**: Version 18 or higher
- **Python**: 3.8+ (for advanced features)
- **Anthropic API Key**: Get yours at [console.anthropic.com](https://console.anthropic.com)

## Support

- **Documentation**: [docs.anthropic.com/claude-code](https://docs.anthropic.com/en/docs/claude-code)
- **Issues**: [GitHub Issues](https://github.com/anthropics/claude-code/issues)
- **Community**: [GitHub Discussions](https://github.com/anthropics/claude-code/discussions)

## License

Claude Code is provided under the Anthropic Terms of Service. See [LICENSE](LICENSE.md) for details.

---

**Ready to code with Claude?** [Get started now](https://docs.anthropic.com/en/docs/claude-code/quickstart) 🚀
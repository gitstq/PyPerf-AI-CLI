<div align="center">

# 🔥 PyPerf-AI-CLI

**輕量級終端Python代碼性能智能分析與AI優化引擎**

*Lightweight Terminal Python Code Performance Intelligence Engine*

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-orange.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Cross--Platform-lightgrey.svg)]()

[English](#english) | [简体中文](#简体中文) | [繁體中文](#繁體中文)

</div>

---

<a name="english"></a>
## 🇺🇸 English

### 🎉 Project Introduction

**PyPerf-AI-CLI** is a lightweight terminal-based Python code performance intelligence engine that combines **zero-dependency pure Python profiling** with **AI-powered bottleneck diagnosis** and **interactive ASCII dashboards**. Inspired by the growing need for accessible performance analysis tools in the AI era, this project delivers professional-grade profiling capabilities without requiring complex installations or heavy frameworks.

**Core Value Propositions:**
- 🚀 **Zero Dependencies** — Pure Python standard library, runs anywhere Python exists
- 🤖 **AI-Powered Analysis** — Supports GLM-5.1, OpenAI, Claude, DeepSeek, and more
- 📊 **Interactive TUI** — Beautiful ASCII flame graphs and performance dashboards
- 📝 **Multi-Format Reports** — Export to Markdown, HTML, JSON with one command
- ⚡ **Lightning Fast** — Minimal overhead profiling with cProfile backend

**Pain Points Solved:**
- Traditional profilers output raw data that's hard to interpret
- AI code generation often produces inefficient algorithms
- Performance optimization requires expert knowledge
- Existing tools are heavy, complex, or platform-specific

### ✨ Core Features

| Feature | Description |
|---------|-------------|
| 🔍 **Smart Profiling** | Function-level, script-level, and block-level profiling with cProfile |
| 🤖 **AI Diagnosis** | Intelligent bottleneck detection with optimization suggestions |
| 🔥 **Flame Graphs** | ASCII art flame graphs in terminal — no browser needed |
| 📊 **TUI Dashboard** | Interactive performance dashboard with color-coded metrics |
| 📝 **Rich Reports** | Auto-generated Markdown/HTML reports with optimization code |
| 🔄 **Compare Mode** | Side-by-side performance comparison of multiple scripts |
| 🌐 **Multi-LLM** | Supports Zhipu, OpenAI, Anthropic, DeepSeek, Aliyun |
| 📦 **Zero Install** | Single Python file deployment, no pip dependencies |

### 🚀 Quick Start

#### Requirements
- Python 3.8+
- (Optional) LLM API Key for AI analysis

#### Installation

```bash
# Clone the repository
git clone https://github.com/gitstq/PyPerf-AI-CLI.git
cd PyPerf-AI-CLI

# Install in development mode
pip install -e .

# Or run directly without installation
python -m pyperf_ai --help
```

#### Basic Usage

```bash
# Profile a Python script
pyperf-ai your_script.py

# Profile with interactive TUI dashboard
pyperf-ai your_script.py --tui

# Profile with AI analysis (requires API key)
pyperf-ai your_script.py --ai --key YOUR_API_KEY --model glm-5.1

# Export HTML report
pyperf-ai your_script.py -f html -o report.html

# Compare multiple scripts
pyperf-ai --compare script1.py script2.py script3.py

# Run built-in demo
pyperf-ai --demo
```

#### Environment Variables

```bash
export LLM_API_KEY="your-api-key-here"
pyperf-ai your_script.py --ai
```

### 📖 Detailed Usage Guide

#### Profiling Modes

**1. Script Profiling**
```bash
pyperf-ai examples/demo_slow.py
```

**2. Function Profiling (Python API)**
```python
from pyperf_ai import PerfProfiler

profiler = PerfProfiler()
result = profiler.profile_function(your_function, arg1, arg2)
```

**3. Block Profiling (Context Manager)**
```python
from pyperf_ai import PerfProfiler

profiler = PerfProfiler()
with profiler.profile_block("critical_section"):
    # Your code here
    pass
```

#### AI Analysis Configuration

| Provider | Model Example | API Endpoint |
|----------|--------------|--------------|
| Zhipu (智谱) | `glm-5.1`, `glm-4` | open.bigmodel.cn |
| OpenAI | `gpt-4`, `gpt-3.5-turbo` | api.openai.com |
| DeepSeek | `deepseek-chat` | api.deepseek.com |
| Anthropic | `claude-3-opus` | api.anthropic.com |
| Aliyun | `qwen-turbo` | dashscope.aliyuncs.com |

#### Report Formats

| Format | Command | Best For |
|--------|---------|----------|
| ASCII | `--format ascii` | Terminal viewing |
| Markdown | `--format markdown` | Documentation |
| HTML | `--format html` | Sharing & presentation |
| JSON | `--format json` | Data processing |

### 💡 Design Philosophy

**Why PyPerf-AI-CLI?**

1. **Accessibility First** — Performance profiling shouldn't require a PhD. We make it as simple as running one command.
2. **AI-Augmented** — Let AI do the heavy lifting of interpreting profiler output and suggesting optimizations.
3. **Zero Friction** — No dependencies, no configuration files, no complex setup. Just Python.
4. **Developer Experience** — Beautiful terminal output that makes performance data actually readable.

**Technical Choices:**
- `cProfile` backend: battle-tested, minimal overhead
- Pure standard library: maximum compatibility
- urllib for HTTP: no requests dependency
- ANSI colors: works in all modern terminals

### 📦 Packaging & Deployment

```bash
# Run tests
make test

# Build distribution
make build

# Clean artifacts
make clean

# Run demo
make demo
```

### 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit with conventional commits (`feat:`, `fix:`, `docs:`)
4. Push to your fork
5. Open a Pull Request

### 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

<a name="简体中文"></a>
## 🇨🇳 简体中文

### 🎉 项目介绍

**PyPerf-AI-CLI** 是一款轻量级终端Python代码性能智能分析引擎，将**零依赖纯Python性能分析**、**AI驱动的瓶颈诊断**和**交互式ASCII仪表盘**融为一体。在AI时代，开发者越来越需要易用的性能分析工具，本项目应运而生，无需复杂安装或重量级框架即可提供专业级的分析能力。

**核心价值：**
- 🚀 **零依赖** — 纯Python标准库，有Python就能运行
- 🤖 **AI智能诊断** — 支持GLM-5.1、OpenAI、Claude、DeepSeek等
- 📊 **交互式TUI** — 精美的ASCII火焰图与性能仪表盘
- 📝 **多格式报告** — 一键导出Markdown、HTML、JSON
- ⚡ **极速分析** — 基于cProfile后端，开销极小

**解决痛点：**
- 传统分析器输出原始数据难以解读
- AI生成的代码常包含低效算法
- 性能优化需要专家知识门槛
- 现有工具笨重、复杂或平台受限

### ✨ 核心特性

| 特性 | 说明 |
|------|------|
| 🔍 **智能分析** | 函数级、脚本级、代码块级cProfile分析 |
| 🤖 **AI诊断** | 智能瓶颈检测与优化建议 |
| 🔥 **火焰图** | 终端ASCII火焰图，无需浏览器 |
| 📊 **TUI仪表盘** | 彩色编码指标的交互式性能仪表盘 |
| 📝 **丰富报告** | 自动生成含优化代码的Markdown/HTML报告 |
| 🔄 **对比模式** | 多脚本并排性能对比 |
| 🌐 **多LLM支持** | 支持智谱、OpenAI、Anthropic、DeepSeek、阿里云 |
| 📦 **零安装** | 单文件部署，无需pip依赖 |

### 🚀 快速开始

#### 环境要求
- Python 3.8+
- （可选）LLM API Key用于AI分析

#### 安装

```bash
# 克隆仓库
git clone https://github.com/gitstq/PyPerf-AI-CLI.git
cd PyPerf-AI-CLI

# 开发模式安装
pip install -e .

# 或直接运行，无需安装
python -m pyperf_ai --help
```

#### 基础用法

```bash
# 分析Python脚本
pyperf-ai your_script.py

# 交互式TUI仪表盘
pyperf-ai your_script.py --tui

# AI智能分析（需API Key）
pyperf-ai your_script.py --ai --key YOUR_API_KEY --model glm-5.1

# 导出HTML报告
pyperf-ai your_script.py -f html -o report.html

# 多脚本对比
pyperf-ai --compare script1.py script2.py script3.py

# 运行内置演示
pyperf-ai --demo
```

#### 环境变量

```bash
export LLM_API_KEY="your-api-key-here"
pyperf-ai your_script.py --ai
```

### 📖 详细使用指南

#### 分析模式

**1. 脚本分析**
```bash
pyperf-ai examples/demo_slow.py
```

**2. 函数分析（Python API）**
```python
from pyperf_ai import PerfProfiler

profiler = PerfProfiler()
result = profiler.profile_function(your_function, arg1, arg2)
```

**3. 代码块分析（上下文管理器）**
```python
from pyperf_ai import PerfProfiler

profiler = PerfProfiler()
with profiler.profile_block("critical_section"):
    # 你的代码
    pass
```

#### AI分析配置

| 提供商 | 模型示例 | API端点 |
|--------|---------|---------|
| 智谱AI | `glm-5.1`, `glm-4` | open.bigmodel.cn |
| OpenAI | `gpt-4`, `gpt-3.5-turbo` | api.openai.com |
| DeepSeek | `deepseek-chat` | api.deepseek.com |
| Anthropic | `claude-3-opus` | api.anthropic.com |
| 阿里云 | `qwen-turbo` | dashscope.aliyuncs.com |

#### 报告格式

| 格式 | 命令 | 适用场景 |
|------|------|---------|
| ASCII | `--format ascii` | 终端查看 |
| Markdown | `--format markdown` | 文档编写 |
| HTML | `--format html` | 分享与演示 |
| JSON | `--format json` | 数据处理 |

### 💡 设计思路

**为什么选择PyPerf-AI-CLI？**

1. **无障碍优先** — 性能分析不应需要博士学位，一条命令即可搞定
2. **AI增强** — 让AI承担解读分析器输出和提出优化建议的重任
3. **零摩擦** — 无依赖、无配置文件、无复杂设置，只需Python
4. **开发者体验** — 精美的终端输出，让性能数据真正可读

**技术选型：**
- `cProfile`后端：久经考验，开销极小
- 纯标准库：最大兼容性
- urllib实现HTTP：无requests依赖
- ANSI颜色：兼容所有现代终端

### 📦 打包与部署

```bash
# 运行测试
make test

# 构建分发包
make build

# 清理构建产物
make clean

# 运行演示
make demo
```

### 🤝 贡献指南

欢迎贡献！请遵循以下规范：

1. Fork本仓库
2. 创建功能分支（`git checkout -b feature/amazing-feature`）
3. 使用约定式提交（`feat:`、`fix:`、`docs:`）
4. 推送到你的Fork
5. 发起Pull Request

### 📄 开源协议

本项目采用 MIT 协议开源 — 详见 [LICENSE](LICENSE)。

---

<a name="繁體中文"></a>
## 🇹🇼 繁體中文

### 🎉 項目介紹

**PyPerf-AI-CLI** 是一款輕量級終端Python代碼性能智能分析引擎，將**零依賴純Python性能分析**、**AI驅動的瓶頸診斷**和**交互式ASCII儀表盤**融為一體。在AI時代，開發者越來越需要易用的性能分析工具，本項目應運而生，無需複雜安裝或重量級框架即可提供專業級的分析能力。

**核心價值：**
- 🚀 **零依賴** — 純Python標準庫，有Python就能運行
- 🤖 **AI智能診斷** — 支持GLM-5.1、OpenAI、Claude、DeepSeek等
- 📊 **交互式TUI** — 精美的ASCII火焰圖與性能儀表盤
- 📝 **多格式報告** — 一鍵導出Markdown、HTML、JSON
- ⚡ **極速分析** — 基於cProfile後端，開銷極小

**解決痛點：**
- 傳統分析器輸出原始數據難以解讀
- AI生成的代碼常包含低效算法
- 性能優化需要專家知識門檻
- 現有工具笨重、複雜或平台受限

### ✨ 核心特性

| 特性 | 說明 |
|------|------|
| 🔍 **智能分析** | 函數級、腳本級、代碼塊級cProfile分析 |
| 🤖 **AI診斷** | 智能瓶頸檢測與優化建議 |
| 🔥 **火焰圖** | 終端ASCII火焰圖，無需瀏覽器 |
| 📊 **TUI儀表盤** | 彩色編碼指標的交互式性能儀表盤 |
| 📝 **豐富報告** | 自動生成含優化代碼的Markdown/HTML報告 |
| 🔄 **對比模式** | 多腳本並排性能對比 |
| 🌐 **多LLM支持** | 支持智譜、OpenAI、Anthropic、DeepSeek、阿里雲 |
| 📦 **零安裝** | 單文件部署，無需pip依賴 |

### 🚀 快速開始

#### 環境要求
- Python 3.8+
- （可選）LLM API Key用於AI分析

#### 安裝

```bash
# 克隆倉庫
git clone https://github.com/gitstq/PyPerf-AI-CLI.git
cd PyPerf-AI-CLI

# 開發模式安裝
pip install -e .

# 或直接運行，無需安裝
python -m pyperf_ai --help
```

#### 基礎用法

```bash
# 分析Python腳本
pyperf-ai your_script.py

# 交互式TUI儀表盤
pyperf-ai your_script.py --tui

# AI智能分析（需API Key）
pyperf-ai your_script.py --ai --key YOUR_API_KEY --model glm-5.1

# 導出HTML報告
pyperf-ai your_script.py -f html -o report.html

# 多腳本對比
pyperf-ai --compare script1.py script2.py script3.py

# 運行內置演示
pyperf-ai --demo
```

#### 環境變量

```bash
export LLM_API_KEY="your-api-key-here"
pyperf-ai your_script.py --ai
```

### 📖 詳細使用指南

#### 分析模式

**1. 腳本分析**
```bash
pyperf-ai examples/demo_slow.py
```

**2. 函數分析（Python API）**
```python
from pyperf_ai import PerfProfiler

profiler = PerfProfiler()
result = profiler.profile_function(your_function, arg1, arg2)
```

**3. 代碼塊分析（上下文管理器）**
```python
from pyperf_ai import PerfProfiler

profiler = PerfProfiler()
with profiler.profile_block("critical_section"):
    # 你的代碼
    pass
```

#### AI分析配置

| 提供商 | 模型示例 | API端點 |
|--------|---------|---------|
| 智譜AI | `glm-5.1`, `glm-4` | open.bigmodel.cn |
| OpenAI | `gpt-4`, `gpt-3.5-turbo` | api.openai.com |
| DeepSeek | `deepseek-chat` | api.deepseek.com |
| Anthropic | `claude-3-opus` | api.anthropic.com |
| 阿里雲 | `qwen-turbo` | dashscope.aliyuncs.com |

#### 報告格式

| 格式 | 命令 | 適用場景 |
|------|------|---------|
| ASCII | `--format ascii` | 終端查看 |
| Markdown | `--format markdown` | 文檔編寫 |
| HTML | `--format html` | 分享與演示 |
| JSON | `--format json` | 數據處理 |

### 💡 設計思路

**為什麼選擇PyPerf-AI-CLI？**

1. **無障礙優先** — 性能分析不應需要博士學位，一條命令即可搞定
2. **AI增強** — 讓AI承擔解讀分析器輸出和提出優化建議的重任
3. **零摩擦** — 無依賴、無配置文件、無複雜設置，只需Python
4. **開發者體驗** — 精美的終端輸出，讓性能數據真正可讀

**技術選型：**
- `cProfile`後端：久經考驗，開銷極小
- 純標準庫：最大兼容性
- urllib實現HTTP：無requests依賴
- ANSI顏色：兼容所有現代終端

### 📦 打包與部署

```bash
# 運行測試
make test

# 構建分發包
make build

# 清理構建產物
make clean

# 運行演示
make demo
```

### 🤝 貢獻指南

歡迎貢獻！請遵循以下規範：

1. Fork本倉庫
2. 創建功能分支（`git checkout -b feature/amazing-feature`）
3. 使用約定式提交（`feat:`、`fix:`、`docs:`）
4. 推送到你的Fork
5. 發起Pull Request

### 📄 開源協議

本項目採用 MIT 協議開源 — 詳見 [LICENSE](LICENSE)。

---

<div align="center">

**Made with 🔥 by PyPerf-AI Team**

</div>

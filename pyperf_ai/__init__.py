"""
PyPerf-AI-CLI - Lightweight Terminal Python Code Performance Intelligence Engine
轻量级终端Python代码性能智能分析与AI优化引擎

Zero Dependencies, Multi-LLM Backend, TUI Dashboard, Multi-Format Export
"""

__version__ = "1.0.0"
__author__ = "gitstq"
__license__ = "MIT"

from .profiler import PerfProfiler
from .analyzer import PerfAnalyzer
from .reporter import PerfReporter
from .tui import PerfTUI

__all__ = ["PerfProfiler", "PerfAnalyzer", "PerfReporter", "PerfTUI"]

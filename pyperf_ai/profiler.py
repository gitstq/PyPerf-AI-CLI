"""
Core Performance Profiler Module
核心性能分析器模块 - 零依赖纯Python实现
"""

import cProfile
import pstats
import io
import time
import sys
import os
import json
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, asdict
from contextlib import contextmanager


@dataclass
class FunctionStats:
    """函数级性能统计"""
    func_name: str
    file_path: str
    line_no: int
    call_count: int
    total_time: float
    cumulative_time: float
    per_call_time: float
    is_builtin: bool


@dataclass
class ProfileResult:
    """分析结果数据结构"""
    target: str
    total_time: float
    timestamp: str
    function_stats: List[FunctionStats]
    top_hotspots: List[Dict[str, Any]]
    summary: Dict[str, Any]


class PerfProfiler:
    """
    Python代码性能分析器
    基于cProfile实现，零外部依赖
    """

    def __init__(self, sort_by: str = "cumulative", top_n: int = 20):
        self.sort_by = sort_by
        self.top_n = top_n
        self._profiler = cProfile.Profile()
        self._results: Optional[ProfileResult] = None

    def profile_function(self, func: Callable, *args, **kwargs) -> ProfileResult:
        """分析单个函数性能"""
        self._profiler.enable()
        start_time = time.perf_counter()
        try:
            result = func(*args, **kwargs)
        finally:
            self._profiler.disable()
            end_time = time.perf_counter()

        self._results = self._parse_stats(
            target=func.__name__,
            total_time=end_time - start_time
        )
        return self._results

    def profile_script(self, script_path: str) -> ProfileResult:
        """分析Python脚本性能"""
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"Script not found: {script_path}")

        start_time = time.perf_counter()
        self._profiler.enable()
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                code = compile(f.read(), script_path, 'exec')
                exec(code, {'__name__': '__main__', '__file__': script_path})
        finally:
            self._profiler.disable()
            end_time = time.perf_counter()

        self._results = self._parse_stats(
            target=script_path,
            total_time=end_time - start_time
        )
        return self._results

    @contextmanager
    def profile_block(self, block_name: str = "code_block"):
        """上下文管理器：分析代码块性能"""
        start_time = time.perf_counter()
        self._profiler.enable()
        try:
            yield self
        finally:
            self._profiler.disable()
            end_time = time.perf_counter()
            self._results = self._parse_stats(
                target=block_name,
                total_time=end_time - start_time
            )

    def _parse_stats(self, target: str, total_time: float) -> ProfileResult:
        """解析cProfile统计数据"""
        stream = io.StringIO()
        stats = pstats.Stats(self._profiler, stream=stream)
        stats.sort_stats(self.sort_by)

        func_stats = []
        top_hotspots = []

        # 获取所有函数统计
        for func, (cc, nc, tt, ct, callers) in stats.stats.items():
            file_path, line_no, func_name = func
            is_builtin = file_path == "~"

            fs = FunctionStats(
                func_name=func_name,
                file_path=file_path if not is_builtin else "[built-in]",
                line_no=line_no if not is_builtin else 0,
                call_count=nc,
                total_time=tt,
                cumulative_time=ct,
                per_call_time=ct / nc if nc > 0 else 0,
                is_builtin=is_builtin
            )
            func_stats.append(fs)

        # 按累计时间排序，提取热点
        func_stats.sort(key=lambda x: x.cumulative_time, reverse=True)
        top_funcs = [f for f in func_stats[:self.top_n] if not f.is_builtin]

        for i, f in enumerate(top_funcs[:10], 1):
            top_hotspots.append({
                "rank": i,
                "function": f.func_name,
                "location": f"{f.file_path}:{f.line_no}",
                "calls": f.call_count,
                "total_time_ms": round(f.total_time * 1000, 3),
                "cumulative_time_ms": round(f.cumulative_time * 1000, 3),
                "per_call_ms": round(f.per_call_time * 1000, 3),
                "time_percent": round((f.cumulative_time / total_time) * 100, 2) if total_time > 0 else 0
            })

        # 计算汇总信息
        total_calls = sum(f.call_count for f in func_stats)
        builtin_calls = sum(f.call_count for f in func_stats if f.is_builtin)
        user_calls = total_calls - builtin_calls

        summary = {
            "total_time_ms": round(total_time * 1000, 3),
            "total_functions": len(func_stats),
            "user_functions": len([f for f in func_stats if not f.is_builtin]),
            "builtin_functions": len([f for f in func_stats if f.is_builtin]),
            "total_calls": total_calls,
            "user_calls": user_calls,
            "builtin_calls": builtin_calls,
            "avg_calls_per_function": round(total_calls / len(func_stats), 2) if func_stats else 0
        }

        return ProfileResult(
            target=target,
            total_time=total_time,
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            function_stats=func_stats,
            top_hotspots=top_hotspots,
            summary=summary
        )

    def get_results(self) -> Optional[ProfileResult]:
        """获取分析结果"""
        return self._results

    def print_stats(self):
        """打印统计报告到终端"""
        if not self._results:
            print("No profiling results available. Run profile first.")
            return

        stats = pstats.Stats(self._profiler)
        stats.sort_stats(self.sort_by)
        stats.print_stats(self.top_n)

    def export_json(self, filepath: str):
        """导出结果为JSON"""
        if not self._results:
            raise ValueError("No results to export")

        data = {
            "target": self._results.target,
            "total_time_ms": round(self._results.total_time * 1000, 3),
            "timestamp": self._results.timestamp,
            "summary": self._results.summary,
            "top_hotspots": self._results.top_hotspots,
            "all_functions": [
                {
                    "function": f.func_name,
                    "file": f.file_path,
                    "line": f.line_no,
                    "calls": f.call_count,
                    "total_time_ms": round(f.total_time * 1000, 3),
                    "cumulative_time_ms": round(f.cumulative_time * 1000, 3)
                }
                for f in self._results.function_stats[:50]
            ]
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def reset(self):
        """重置分析器状态"""
        self._profiler = cProfile.Profile()
        self._results = None

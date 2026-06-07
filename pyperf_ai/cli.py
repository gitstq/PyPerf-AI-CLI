"""
Command Line Interface Module
命令行接口模块
"""

import sys
import os
import argparse
import json
from typing import Optional

from .profiler import PerfProfiler
from .analyzer import PerfAnalyzer
from .reporter import PerfReporter
from .tui import PerfTUI


def create_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        prog="pyperf-ai",
        description="🔥 PyPerf-AI-CLI - Lightweight Terminal Python Code Performance Intelligence Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pyperf-ai script.py                    # Profile a Python script
  pyperf-ai script.py --ai --key KEY     # Profile with AI analysis
  pyperf-ai script.py -f html -o report  # Export HTML report
  pyperf-ai script.py --tui              # Interactive TUI dashboard
  pyperf-ai --demo                       # Run built-in demo
        """
    )

    parser.add_argument("target", nargs="?", help="Python script or function to profile")
    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")

    # Profiling options
    profile_group = parser.add_argument_group("Profiling Options")
    profile_group.add_argument("--sort", "-s", default="cumulative",
                               choices=["tottime", "cumtime", "ncalls", "name"],
                               help="Sort stats by (default: cumulative)")
    profile_group.add_argument("--top", "-n", type=int, default=20,
                               help="Number of top functions to show (default: 20)")

    # AI Analysis options
    ai_group = parser.add_argument_group("AI Analysis Options")
    ai_group.add_argument("--ai", "-a", action="store_true",
                          help="Enable AI-powered analysis")
    ai_group.add_argument("--key", "-k", help="LLM API key")
    ai_group.add_argument("--model", "-m", default="glm-5.1",
                          help="LLM model (default: glm-5.1)")

    # Output options
    output_group = parser.add_argument_group("Output Options")
    output_group.add_argument("--format", "-f", default="ascii",
                              choices=["ascii", "markdown", "html", "json"],
                              help="Output format (default: ascii)")
    output_group.add_argument("--output", "-o", help="Output file path")
    output_group.add_argument("--tui", "-t", action="store_true",
                              help="Interactive TUI dashboard")
    output_group.add_argument("--no-color", action="store_true",
                              help="Disable colored output")

    # Other
    parser.add_argument("--demo", action="store_true",
                        help="Run built-in performance demo")
    parser.add_argument("--compare", nargs="+", metavar="SCRIPT",
                        help="Compare multiple scripts performance")

    return parser


def run_demo():
    """运行内置演示"""
    print("🔥 PyPerf-AI Demo - Running sample profiling...")
    print()

    # Demo: 低效的斐波那契计算
    def fibonacci_slow(n):
        if n <= 1:
            return n
        return fibonacci_slow(n - 1) + fibonacci_slow(n - 2)

    def fibonacci_fast(n, memo={}):
        if n in memo:
            return memo[n]
        if n <= 1:
            return n
        memo[n] = fibonacci_fast(n - 1, memo) + fibonacci_fast(n - 2, memo)
        return memo[n]

    profiler = PerfProfiler()

    print("Profiling slow fibonacci(25)...")
    result_slow = profiler.profile_function(fibonacci_slow, 25)

    profiler.reset()
    print("Profiling fast fibonacci(100)...")
    result_fast = profiler.profile_function(fibonacci_fast, 100)

    # Display comparison
    tui = PerfTUI()
    tui.render_compare([result_slow, result_fast], ["fibonacci_slow(25)", "fibonacci_fast(100)"])

    print("\n💡 Key Insight:")
    print(f"  Slow version: {result_slow.summary['total_time_ms']:.2f}ms with {result_slow.summary['total_calls']:,} calls")
    print(f"  Fast version: {result_fast.summary['total_time_ms']:.2f}ms with {result_fast.summary['total_calls']:,} calls")
    speedup = result_slow.summary['total_time_ms'] / result_fast.summary['total_time_ms'] if result_fast.summary['total_time_ms'] > 0 else 0
    print(f"  Speedup: {speedup:.0f}x faster with memoization!")


def main():
    """主入口函数"""
    parser = create_parser()
    args = parser.parse_args()

    # Handle demo mode
    if args.demo:
        run_demo()
        return 0

    # Handle compare mode
    if args.compare:
        profiler = PerfProfiler(sort_by=args.sort, top_n=args.top)
        results = []
        for script in args.compare:
            if os.path.exists(script):
                results.append(profiler.profile_script(script))
                profiler.reset()
            else:
                print(f"⚠️ Script not found: {script}")

        if len(results) >= 2:
            tui = PerfTUI()
            tui.render_compare(results, args.compare)
        return 0

    # Validate target
    if not args.target:
        parser.print_help()
        return 1

    if not os.path.exists(args.target):
        print(f"❌ Error: File not found: {args.target}")
        return 1

    # Run profiling
    profiler = PerfProfiler(sort_by=args.sort, top_n=args.top)
    print(f"🔥 Profiling: {args.target}")
    print("⏳ Running analysis...")

    try:
        result = profiler.profile_script(args.target)
    except Exception as e:
        print(f"❌ Profiling failed: {e}")
        return 1

    # AI Analysis
    ai_result = None
    if args.ai:
        print("🤖 Running AI analysis...")
        api_key = args.key or os.environ.get("LLM_API_KEY")
        analyzer = PerfAnalyzer(api_key=api_key, model=args.model)

        # Try to read source code
        source_code = None
        try:
            with open(args.target, 'r', encoding='utf-8') as f:
                source_code = f.read()
        except:
            pass

        ai_result = analyzer.analyze(result, source_code)

    # Output
    reporter = PerfReporter()

    if args.tui:
        tui = PerfTUI()
        tui.render_dashboard(result, ai_result)
    else:
        if args.format == "ascii":
            print(reporter.generate_ascii_report(result, ai_result))
        elif args.format == "markdown":
            print(reporter.generate_markdown_report(result, ai_result))
        elif args.format == "html":
            print(reporter.generate_html_report(result, ai_result))
        elif args.format == "json":
            # JSON export via profiler
            pass

    # Save to file
    if args.output:
        fmt = args.format
        if fmt == "ascii":
            fmt = "markdown"  # Default to markdown for file output

        filepath = args.output
        if not os.path.splitext(filepath)[1]:
            ext_map = {"markdown": ".md", "html": ".html", "json": ".json"}
            filepath += ext_map.get(fmt, ".md")

        reporter.save_report(result, ai_result, filepath, fmt)
        print(f"\n💾 Report saved to: {filepath}")

    # Also export JSON data
    json_path = None
    if args.output:
        base = os.path.splitext(args.output)[0]
        json_path = base + ".json"
    else:
        json_path = "pyperf_report.json"

    profiler.export_json(json_path)
    if not args.output:
        print(f"💾 Raw data exported to: {json_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

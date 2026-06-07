"""
Terminal User Interface Module
终端交互式界面模块 - 纯ASCII艺术实现
"""

import sys
import os
from typing import Optional, Any, List


class PerfTUI:
    """
    终端交互式性能仪表盘
    零依赖，纯ANSI转义序列实现
    """

    # ANSI颜色码
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BG_DARK = "\033[48;5;235m"
    BG_BLUE = "\033[48;5;24m"

    def __init__(self):
        self.width = self._get_terminal_width()

    def _get_terminal_width(self) -> int:
        """获取终端宽度"""
        try:
            return os.get_terminal_size().columns
        except:
            return 80

    def clear(self):
        """清屏"""
        print("\033[2J\033[H", end="")

    def print_header(self, title: str):
        """打印标题头"""
        w = min(self.width, 80)
        print(f"{self.BOLD}{self.CYAN}╔{'═' * (w - 2)}╗{self.RESET}")
        print(f"{self.BOLD}{self.CYAN}║{title.center(w - 2)}║{self.RESET}")
        print(f"{self.BOLD}{self.CYAN}╚{'═' * (w - 2)}╝{self.RESET}")

    def print_section(self, title: str):
        """打印分节标题"""
        w = min(self.width, 80)
        print(f"\n{self.BOLD}{self.YELLOW}▶ {title}{self.RESET}")
        print(f"{self.DIM}{'─' * min(60, w - 4)}{self.RESET}")

    def print_metric(self, label: str, value: str, unit: str = "", color: str = ""):
        """打印指标"""
        c = getattr(self, color.upper(), self.WHITE) if color else self.WHITE
        print(f"  {self.DIM}{label}:{self.RESET} {c}{self.BOLD}{value}{self.RESET} {self.DIM}{unit}{self.RESET}")

    def draw_bar(self, label: str, percent: float, width: int = 40, color: str = ""):
        """绘制ASCII进度条"""
        c = getattr(self, color.upper(), self.GREEN) if color else self.GREEN
        filled = int(width * percent / 100)
        bar = "█" * filled + "░" * (width - filled)
        print(f"  {label:<20} {c}{bar}{self.RESET} {percent:>5.1f}%")

    def draw_flame_bar(self, func_name: str, percent: float, time_ms: float, width: int = 50):
        """绘制火焰图风格的条形"""
        # 根据百分比选择颜色
        if percent > 30:
            color = self.RED
        elif percent > 15:
            color = self.YELLOW
        elif percent > 5:
            color = self.GREEN
        else:
            color = self.BLUE

        bar_width = int(width * min(percent, 100) / 100)
        if bar_width == 0:
            bar_width = 1

        bar = "▓" * bar_width
        name = func_name[:25] if len(func_name) > 25 else func_name
        print(f"  {color}{bar:<{width}}{self.RESET} {self.BOLD}{percent:>5.1f}%{self.RESET}  {self.DIM}{time_ms:>8.2f}ms{self.RESET}  {name}")

    def render_dashboard(self, profile_result: Any, ai_result: Optional[Any] = None):
        """渲染完整仪表盘"""
        self.clear()
        self.width = self._get_terminal_width()

        # Header
        self.print_header("🔥 PyPerf-AI Performance Dashboard")

        # Basic Info
        self.print_section("📋 Analysis Overview")
        self.print_metric("Target", profile_result.target[:50])
        self.print_metric("Timestamp", profile_result.timestamp)
        self.print_metric("Total Time", f"{profile_result.summary['total_time_ms']:.2f}", "ms", "cyan")

        # Summary Cards
        self.print_section("📊 Statistics")
        print(f"  {self.BG_DARK}  Functions: {self.BOLD}{profile_result.summary['user_functions']}{self.RESET}{self.BG_DARK}  │  Calls: {self.BOLD}{profile_result.summary['total_calls']:,}{self.RESET}{self.BG_DARK}  │  Avg/Func: {self.BOLD}{profile_result.summary['avg_calls_per_function']}{self.RESET}{self.BG_DARK}  {self.RESET}")

        # AI Score
        if ai_result:
            self.print_section("🤖 AI Assessment")
            score = ai_result.overall_score
            grade = ai_result.performance_grade
            grade_colors = {"A": self.GREEN, "B": self.GREEN, "C": self.YELLOW, "D": self.YELLOW, "F": self.RED}
            gc = grade_colors.get(grade, self.WHITE)

            # Score circle (ASCII art)
            print(f"""
    {gc}     ██████
   ███    ███
  ███  {self.BOLD}{score}{self.RESET}{gc}  ███   Grade: {self.BOLD}{grade}{self.RESET}
  ███        ███
   ███      ███
     ████████{self.RESET}
""")
            print(f"  {self.DIM}Bottleneck:{self.RESET} {ai_result.bottleneck_analysis[:100]}")

        # Flame Graph (ASCII)
        self.print_section("🔥 Performance Flame Graph")
        print(f"  {self.DIM}{'Function':<30} {'Time %':>8} {'Time (ms)':>10}{self.RESET}")
        print(f"  {self.DIM}{'─' * 60}{self.RESET}")

        for h in profile_result.top_hotspots[:12]:
            self.draw_flame_bar(h['function'], h['time_percent'], h['cumulative_time_ms'])

        # Suggestions
        if ai_result and ai_result.suggestions:
            self.print_section("💡 Optimization Suggestions")
            for i, s in enumerate(ai_result.suggestions[:5], 1):
                sev_colors = {"critical": self.RED, "high": self.YELLOW, "medium": self.CYAN, "low": self.GREEN}
                sc = sev_colors.get(s.severity, self.WHITE)
                sev_emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}.get(s.severity, "⚪")
                print(f"  {sev_emoji} {sc}[{s.severity.upper()}]{self.RESET} {self.BOLD}{s.category.upper()}{self.RESET}")
                print(f"     {s.description[:70]}")
                if s.expected_improvement:
                    print(f"     {self.GREEN}→ {s.expected_improvement[:60]}{self.RESET}")
                print()

        # Footer
        w = min(self.width, 80)
        print(f"\n{self.DIM}{'─' * w}{self.RESET}")
        print(f"{self.DIM}  PyPerf-AI-CLI v1.0.0 │ Use --help for more options │ Report exported{self.RESET}")
        print()

    def render_compare(self, results: List[Any], labels: List[str]):
        """渲染对比视图"""
        self.clear()
        self.print_header("📊 Performance Comparison")

        if len(results) != len(labels):
            print("Error: Results and labels count mismatch")
            return

        # Find max time for normalization
        max_time = max(r.summary['total_time_ms'] for r in results) if results else 1

        self.print_section("Execution Time Comparison")
        for r, label in zip(results, labels):
            pct = (r.summary['total_time_ms'] / max_time) * 100 if max_time > 0 else 0
            color = "green" if pct < 50 else "yellow" if pct < 80 else "red"
            self.draw_bar(label[:20], pct, color=color)
            print(f"     {self.DIM}Time: {r.summary['total_time_ms']:.2f}ms │ Functions: {r.summary['user_functions']} │ Calls: {r.summary['total_calls']:,}{self.RESET}")

        print()

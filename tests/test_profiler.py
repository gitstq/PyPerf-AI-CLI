"""
Unit Tests for PyPerf-AI Profiler
"""

import unittest
import sys
import os
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pyperf_ai.profiler import PerfProfiler, ProfileResult


class TestPerfProfiler(unittest.TestCase):
    """测试性能分析器核心功能"""

    def setUp(self):
        self.profiler = PerfProfiler()

    def test_profile_simple_function(self):
        """测试简单函数分析"""
        def sample_func():
            total = 0
            for i in range(1000):
                total += i
            return total

        result = self.profiler.profile_function(sample_func)
        self.assertIsInstance(result, ProfileResult)
        self.assertEqual(result.target, "sample_func")
        self.assertGreater(result.total_time, 0)
        self.assertGreater(len(result.function_stats), 0)
        self.assertGreater(len(result.top_hotspots), 0)

    def test_profile_with_args(self):
        """测试带参数的函数分析"""
        def multiply(a, b):
            return a * b

        result = self.profiler.profile_function(multiply, 10, 20)
        self.assertEqual(result.target, "multiply")

    def test_profile_script(self):
        """测试脚本分析"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("""
for i in range(100):
    x = i ** 2
""")
            temp_path = f.name

        try:
            result = self.profiler.profile_script(temp_path)
            self.assertEqual(result.target, temp_path)
            self.assertGreater(result.summary['total_calls'], 0)
        finally:
            os.unlink(temp_path)

    def test_profile_block(self):
        """测试代码块分析"""
        with self.profiler.profile_block("test_block"):
            data = [i ** 2 for i in range(500)]

        result = self.profiler.get_results()
        self.assertIsNotNone(result)
        self.assertEqual(result.target, "test_block")

    def test_export_json(self):
        """测试JSON导出"""
        def sample():
            return sum(range(100))

        self.profiler.profile_function(sample)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name

        try:
            self.profiler.export_json(temp_path)
            self.assertTrue(os.path.exists(temp_path))
            self.assertGreater(os.path.getsize(temp_path), 0)
        finally:
            os.unlink(temp_path)

    def test_reset(self):
        """测试重置功能"""
        def sample():
            return 42

        self.profiler.profile_function(sample)
        self.assertIsNotNone(self.profiler.get_results())

        self.profiler.reset()
        self.assertIsNone(self.profiler.get_results())

    def test_summary_stats(self):
        """测试汇总统计"""
        def recursive_sum(n):
            if n <= 0:
                return 0
            return n + recursive_sum(n - 1)

        result = self.profiler.profile_function(recursive_sum, 50)
        summary = result.summary

        self.assertIn('total_time_ms', summary)
        self.assertIn('total_functions', summary)
        self.assertIn('user_functions', summary)
        self.assertIn('total_calls', summary)
        self.assertGreater(summary['total_calls'], 50)


class TestPerfAnalyzer(unittest.TestCase):
    """测试AI分析器"""

    def setUp(self):
        from pyperf_ai.analyzer import PerfAnalyzer
        self.analyzer = PerfAnalyzer()

    def test_local_analysis(self):
        """测试本地启发式分析"""
        profiler = PerfProfiler()

        def slow_func():
            result = []
            for i in range(1000):
                result.append(i ** 2)
            return result

        profile_result = profiler.profile_function(slow_func)
        ai_result = self.analyzer.analyze(profile_result)

        self.assertIsNotNone(ai_result)
        self.assertGreaterEqual(ai_result.overall_score, 0)
        self.assertLessEqual(ai_result.overall_score, 100)
        self.assertIn(ai_result.performance_grade, ['A', 'B', 'C', 'D', 'F'])
        self.assertIsInstance(ai_result.suggestions, list)

    def test_analysis_without_api_key(self):
        """测试无API Key时的离线分析"""
        profiler = PerfProfiler()

        def test_func():
            return sum(range(100))

        profile_result = profiler.profile_function(test_func)
        ai_result = self.analyzer.analyze(profile_result)

        self.assertIsNotNone(ai_result)
        self.assertTrue(len(ai_result.bottleneck_analysis) > 0)


class TestPerfReporter(unittest.TestCase):
    """测试报告生成器"""

    def setUp(self):
        from pyperf_ai.reporter import PerfReporter
        from pyperf_ai.analyzer import PerfAnalyzer
        self.reporter = PerfReporter()
        self.analyzer = PerfAnalyzer()
        self.profiler = PerfProfiler()

    def test_ascii_report(self):
        """测试ASCII报告"""
        def sample():
            return [i * 2 for i in range(100)]

        result = self.profiler.profile_function(sample)
        ai_result = self.analyzer.analyze(result)

        report = self.reporter.generate_ascii_report(result, ai_result)
        self.assertIn("PyPerf-AI", report)
        self.assertIn("sample", report)

    def test_markdown_report(self):
        """测试Markdown报告"""
        def sample():
            return sum(range(50))

        result = self.profiler.profile_function(sample)
        report = self.reporter.generate_markdown_report(result)

        self.assertIn("#", report)
        self.assertIn("Performance Summary", report)

    def test_html_report(self):
        """测试HTML报告"""
        def sample():
            return [i ** 3 for i in range(30)]

        result = self.profiler.profile_function(sample)
        report = self.reporter.generate_html_report(result)

        self.assertIn("<html", report)
        self.assertIn("</html>", report)
        self.assertIn("PyPerf-AI", report)

    def test_save_report(self):
        """测试报告保存"""
        def sample():
            return sum(range(20))

        result = self.profiler.profile_function(sample)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            temp_path = f.name

        try:
            self.reporter.save_report(result, None, temp_path, "markdown")
            self.assertTrue(os.path.exists(temp_path))
            with open(temp_path, 'r') as f:
                content = f.read()
            self.assertIn("PyPerf-AI", content)
        finally:
            os.unlink(temp_path)


if __name__ == '__main__':
    unittest.main(verbosity=2)

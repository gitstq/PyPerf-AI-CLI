"""
AI-Powered Performance Analysis Module
AI驱动性能智能分析模块 - 支持多LLM后端
"""

import json
import re
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import urllib.request
import urllib.error


@dataclass
class OptimizationSuggestion:
    """优化建议数据结构"""
    category: str
    severity: str  # critical, high, medium, low
    description: str
    original_code: Optional[str]
    optimized_code: Optional[str]
    expected_improvement: str
    line_reference: Optional[str]


@dataclass
class AIAnalysisResult:
    """AI分析结果"""
    overall_score: int  # 0-100
    performance_grade: str  # A, B, C, D, F
    bottleneck_analysis: str
    suggestions: List[OptimizationSuggestion]
    complexity_assessment: str
    memory_insights: str


class PerfAnalyzer:
    """
    性能智能分析器
    支持GLM-5.1、OpenAI、Claude等多LLM后端
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "glm-5.1"):
        self.api_key = api_key
        self.model = model
        self._provider = self._detect_provider(model)

    def _detect_provider(self, model: str) -> str:
        """自动检测LLM提供商"""
        model_lower = model.lower()
        if "glm" in model_lower or "chatglm" in model_lower:
            return "zhipu"
        elif "gpt" in model_lower or "openai" in model_lower:
            return "openai"
        elif "claude" in model_lower:
            return "anthropic"
        elif "deepseek" in model_lower:
            return "deepseek"
        elif "qwen" in model_lower or "ali" in model_lower:
            return "aliyun"
        return "zhipu"  # 默认智谱

    def analyze(self, profile_result: Any, source_code: Optional[str] = None) -> AIAnalysisResult:
        """
        对性能分析结果进行AI智能诊断
        """
        # 构建分析提示词
        prompt = self._build_analysis_prompt(profile_result, source_code)

        # 如果有API Key，调用LLM；否则使用本地启发式分析
        if self.api_key:
            try:
                return self._call_llm(prompt, profile_result)
            except Exception as e:
                print(f"⚠️ LLM analysis failed: {e}, falling back to local analysis")
                return self._local_analysis(profile_result, source_code)
        else:
            return self._local_analysis(profile_result, source_code)

    def _build_analysis_prompt(self, profile_result: Any, source_code: Optional[str]) -> str:
        """构建AI分析提示词"""
        hotspots = profile_result.top_hotspots
        summary = profile_result.summary

        prompt = f"""你是一位Python性能优化专家。请分析以下性能分析数据并提供优化建议。

## 性能概况
- 总执行时间: {summary['total_time_ms']} ms
- 分析函数总数: {summary['total_functions']}
- 用户函数数: {summary['user_functions']}
- 总调用次数: {summary['total_calls']}

## 热点函数 (Top 10)
"""
        for h in hotspots:
            prompt += f"""
{h['rank']}. {h['function']}
   - 位置: {h['location']}
   - 调用次数: {h['calls']}
   - 累计时间: {h['cumulative_time_ms']} ms ({h['time_percent']}%)
   - 单次调用: {h['per_call_ms']} ms
"""

        if source_code:
            prompt += f"""
## 源代码
```python
{source_code[:3000]}
```
"""

        prompt += """
请提供以下分析（用JSON格式返回）：
{
  "overall_score": 85,
  "performance_grade": "B",
  "bottleneck_analysis": "详细描述主要性能瓶颈...",
  "complexity_assessment": "时间/空间复杂度评估...",
  "memory_insights": "内存使用分析...",
  "suggestions": [
    {
      "category": "algorithm|data_structure|io|memory|concurrency",
      "severity": "critical|high|medium|low",
      "description": "问题描述",
      "solution": "优化方案",
      "expected_improvement": "预期提升"
    }
  ]
}
"""
        return prompt

    def _call_llm(self, prompt: str, profile_result: Any) -> AIAnalysisResult:
        """调用LLM API进行分析"""
        if self._provider == "zhipu":
            return self._call_zhipu(prompt, profile_result)
        elif self._provider == "openai":
            return self._call_openai(prompt, profile_result)
        elif self._provider == "deepseek":
            return self._call_deepseek(prompt, profile_result)
        else:
            return self._local_analysis(profile_result, None)

    def _call_zhipu(self, prompt: str, profile_result: Any) -> AIAnalysisResult:
        """调用智谱GLM API"""
        url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
        data = json.dumps({
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
            "max_tokens": 4000
        }).encode('utf-8')

        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        )

        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
            content = result['choices'][0]['message']['content']
            return self._parse_llm_response(content, profile_result)

    def _call_openai(self, prompt: str, profile_result: Any) -> AIAnalysisResult:
        """调用OpenAI API"""
        url = "https://api.openai.com/v1/chat/completions"
        data = json.dumps({
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
            "max_tokens": 4000
        }).encode('utf-8')

        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        )

        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
            content = result['choices'][0]['message']['content']
            return self._parse_llm_response(content, profile_result)

    def _call_deepseek(self, prompt: str, profile_result: Any) -> AIAnalysisResult:
        """调用DeepSeek API"""
        url = "https://api.deepseek.com/v1/chat/completions"
        data = json.dumps({
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
            "max_tokens": 4000
        }).encode('utf-8')

        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        )

        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
            content = result['choices'][0]['message']['content']
            return self._parse_llm_response(content, profile_result)

    def _parse_llm_response(self, content: str, profile_result: Any) -> AIAnalysisResult:
        """解析LLM返回的JSON响应"""
        try:
            # 提取JSON部分
            json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group(1))
            else:
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    data = json.loads(json_match.group())
                else:
                    raise ValueError("No JSON found in response")

            suggestions = []
            for s in data.get("suggestions", []):
                suggestions.append(OptimizationSuggestion(
                    category=s.get("category", "general"),
                    severity=s.get("severity", "medium"),
                    description=s.get("description", ""),
                    original_code=s.get("original_code"),
                    optimized_code=s.get("optimized_code"),
                    expected_improvement=s.get("expected_improvement", ""),
                    line_reference=s.get("line_reference")
                ))

            return AIAnalysisResult(
                overall_score=data.get("overall_score", 70),
                performance_grade=data.get("performance_grade", "C"),
                bottleneck_analysis=data.get("bottleneck_analysis", ""),
                suggestions=suggestions,
                complexity_assessment=data.get("complexity_assessment", ""),
                memory_insights=data.get("memory_insights", "")
            )
        except Exception as e:
            print(f"⚠️ Failed to parse LLM response: {e}")
            return self._local_analysis(profile_result, None)

    def _local_analysis(self, profile_result: Any, source_code: Optional[str]) -> AIAnalysisResult:
        """
        本地启发式分析（零依赖离线模式）
        基于性能数据模式识别提供优化建议
        """
        hotspots = profile_result.top_hotspots
        summary = profile_result.summary
        suggestions = []

        # 分析热点模式
        total_time = summary['total_time_ms']

        if not hotspots:
            return AIAnalysisResult(
                overall_score=100,
                performance_grade="A",
                bottleneck_analysis="未检测到明显的性能热点。",
                suggestions=[],
                complexity_assessment="代码执行效率良好。",
                memory_insights="内存使用模式正常。"
            )

        # 检查是否存在单一热点垄断
        top_time_percent = hotspots[0]['time_percent'] if hotspots else 0
        if top_time_percent > 50:
            suggestions.append(OptimizationSuggestion(
                category="algorithm",
                severity="critical",
                description=f"函数 '{hotspots[0]['function']}' 占用了 {top_time_percent}% 的执行时间，存在严重的性能瓶颈。",
                original_code=None,
                optimized_code=None,
                expected_improvement="通过算法优化可能提升 50-80% 整体性能",
                line_reference=hotspots[0]['location']
            ))

        # 检查高频低耗时函数（可能存在循环内冗余调用）
        for h in hotspots:
            if h['calls'] > 1000 and h['per_call_ms'] < 0.01:
                suggestions.append(OptimizationSuggestion(
                    category="algorithm",
                    severity="high",
                    description=f"函数 '{h['function']}' 被调用 {h['calls']} 次，可能存在循环内冗余调用。",
                    original_code=None,
                    optimized_code=None,
                    expected_improvement="通过缓存/内联优化可能减少 30-60% 调用开销",
                    line_reference=h['location']
                ))
                break

        # 检查I/O相关瓶颈
        io_keywords = ['read', 'write', 'open', 'load', 'save', 'fetch', 'request', 'db']
        for h in hotspots:
            func_lower = h['function'].lower()
            if any(kw in func_lower for kw in io_keywords) and h['time_percent'] > 10:
                suggestions.append(OptimizationSuggestion(
                    category="io",
                    severity="high",
                    description=f"I/O操作 '{h['function']}' 是主要瓶颈，考虑使用异步I/O或批处理。",
                    original_code=None,
                    optimized_code=None,
                    expected_improvement="异步化可能提升 40-70% I/O密集型场景性能",
                    line_reference=h['location']
                ))
                break

        # 检查递归/深度调用
        deep_funcs = [h for h in hotspots if h['calls'] > 100 and h['cumulative_time_ms'] > h['total_time_ms'] * 2]
        if deep_funcs:
            suggestions.append(OptimizationSuggestion(
                category="algorithm",
                severity="medium",
                description=f"检测到深层调用链，函数 '{deep_funcs[0]['function']}' 可能存在递归或过度嵌套。",
                original_code=None,
                optimized_code=None,
                expected_improvement="尾递归优化或迭代改写可能提升 20-40%",
                line_reference=deep_funcs[0]['location']
            ))

        # 计算综合评分
        score = 100
        if top_time_percent > 60:
            score -= 30
        elif top_time_percent > 40:
            score -= 20
        elif top_time_percent > 20:
            score -= 10

        score -= min(len(suggestions) * 5, 30)
        score = max(0, min(100, score))

        # 确定等级
        if score >= 90:
            grade = "A"
        elif score >= 80:
            grade = "B"
        elif score >= 70:
            grade = "C"
        elif score >= 60:
            grade = "D"
        else:
            grade = "F"

        bottleneck_desc = f"""基于性能分析数据，共分析 {summary['user_functions']} 个用户函数，总调用 {summary['user_calls']} 次。
主要性能热点为 '{hotspots[0]['function']}'（占 {hotspots[0]['time_percent']}% 执行时间）。
""" if hotspots else "未检测到明显性能瓶颈。"

        return AIAnalysisResult(
            overall_score=score,
            performance_grade=grade,
            bottleneck_analysis=bottleneck_desc,
            suggestions=suggestions,
            complexity_assessment="基于调用图分析，建议检查高频调用路径的算法复杂度。",
            memory_insights="当前分析模式显示内存使用与调用频率正相关，建议关注大对象分配。"
        )

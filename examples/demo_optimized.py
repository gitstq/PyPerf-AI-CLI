"""
Optimized version of demo script
优化后的示例脚本 - 展示改进后的性能
"""

import time
from functools import lru_cache


@lru_cache(maxsize=None)
def fibonacci_memoized(n):
    """优化的记忆化斐波那契 - O(n)"""
    if n <= 1:
        return n
    return fibonacci_memoized(n - 1) + fibonacci_memoized(n - 2)


def find_duplicates_set(data):
    """优化的重复查找 - O(n)"""
    seen = set()
    duplicates = set()
    for item in data:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return list(duplicates)


def efficient_string_join(items):
    """优化的字符串拼接"""
    return ", ".join(str(item) for item in items)


def cached_calculation(n):
    """缓存计算结果"""
    base = sum(range(100))  # 只计算一次
    return [i + base for i in range(n)]


def main():
    print("Running optimized performance demo...")

    # 优化1: 记忆化斐波那契
    print("Computing fibonacci(300)...")
    start = time.time()
    fib_result = fibonacci_memoized(300)
    print(f"Result length: {len(str(fib_result))} digits, Time: {time.time() - start:.3f}s")

    # 优化2: O(n)重复查找
    print("\nFinding duplicates...")
    data = list(range(100)) + list(range(50, 150))
    start = time.time()
    dups = find_duplicates_set(data)
    print(f"Duplicates: {len(dups)}, Time: {time.time() - start:.3f}s")

    # 优化3: 高效字符串拼接
    print("\nConcatenating strings...")
    items = list(range(500))
    start = time.time()
    text = efficient_string_join(items)
    print(f"Length: {len(text)}, Time: {time.time() - start:.3f}s")

    # 优化4: 缓存计算
    print("\nCached calculations...")
    start = time.time()
    calc_results = cached_calculation(200)
    print(f"Results: {len(calc_results)}, Time: {time.time() - start:.3f}s")

    print("\nDone! Compare with demo_slow.py to see the improvements.")


if __name__ == "__main__":
    main()

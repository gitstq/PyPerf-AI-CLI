"""
Demo script with intentional performance issues
用于演示性能分析的示例脚本（包含故意设计的性能问题）
"""

import time


def fibonacci_recursive(n):
    """低效的递归斐波那契 - O(2^n)"""
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


def find_duplicates_brute_force(data):
    """低效的重复查找 - O(n^2)"""
    duplicates = []
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            if data[i] == data[j] and data[i] not in duplicates:
                duplicates.append(data[i])
    return duplicates


def inefficient_string_concat(items):
    """低效的字符串拼接"""
    result = ""
    for item in items:
        result += str(item) + ", "
    return result


def repeated_calculation(n):
    """重复计算"""
    results = []
    for i in range(n):
        # 每次循环都重新计算相同的值
        base = sum(range(100))
        results.append(i + base)
    return results


def main():
    print("Running performance demo with intentional bottlenecks...")

    # 瓶颈1: 递归斐波那契
    print("Computing fibonacci(30)...")
    start = time.time()
    fib_result = fibonacci_recursive(30)
    print(f"Result: {fib_result}, Time: {time.time() - start:.3f}s")

    # 瓶颈2: O(n^2)重复查找
    print("\nFinding duplicates...")
    data = list(range(100)) + list(range(50, 150))
    start = time.time()
    dups = find_duplicates_brute_force(data)
    print(f"Duplicates: {len(dups)}, Time: {time.time() - start:.3f}s")

    # 瓶颈3: 低效字符串拼接
    print("\nConcatenating strings...")
    items = list(range(500))
    start = time.time()
    text = inefficient_string_concat(items)
    print(f"Length: {len(text)}, Time: {time.time() - start:.3f}s")

    # 瓶颈4: 重复计算
    print("\nRepeated calculations...")
    start = time.time()
    calc_results = repeated_calculation(200)
    print(f"Results: {len(calc_results)}, Time: {time.time() - start:.3f}s")

    print("\nDone! Profile this script to see AI optimization suggestions.")


if __name__ == "__main__":
    main()

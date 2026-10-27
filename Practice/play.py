"""第 1 天练习：手写均值与描述统计。

跑法（在 prob-sim 目录下，本机用 py 不要用 python）：
    py Practice/play.py
    py -m Practice.play
"""


def mean(data: list[float]) -> float:
    """返回 data 的算术平均值。

    手写累加器而不用内置 sum()，为的是把 for 循环 + 累加这个模式练熟：
    先把所有数加进 total，最后除以个数。
    """
    total = 0.0
    for x in data:
        total += x
    return total / len(data)


def median(data: list[float]) -> float:
    """返回 data 的中位数（偶数个取中间两个的平均）。

    先排序再取中间；sorted() 返回新列表，不会改动传入的 data。
    """
    sorted_data = sorted(data)
    mid = len(sorted_data) // 2
    if len(sorted_data) % 2 == 0:
        return (sorted_data[mid] + sorted_data[mid - 1]) / 2
    return sorted_data[mid]


def describe(data: list[float]) -> None:
    """打印 data 的个数、最大值、最小值、中位数。"""
    print("个数:", len(data))
    print("最大:", max(data))
    print("最小:", min(data))
    print("中位数:", median(data))


def main() -> None:
    """脚本入口：跑几个例子，肉眼对一下结果。"""
    # data = [1, 2, 3, 4, 5]
    # print("平均值:", mean(data))                    # 期望 3.0
    # print("另一组平均值:", mean([20, 30, 40, 50]))  # 期望 35.0
    # describe(data)                                 # 期望 5 / 5 / 1
    print(median([3, 1, 2]))
    print(median([3, 1, 2, 4]))
    describe([100, 200])

if __name__ == "__main__":
    main()

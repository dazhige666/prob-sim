"""K-S 拟合检验统计量的样本点模拟。

单一职责：只算数学，不打印、不读文件。
调用方拿到 list[float] 自己决定怎么用。
"""

import random

from prob_sim.base import Distribution, ParamSpec
from prob_sim.registry import REGISTRY


def one_d(n: int) -> float:
    """抽 n 个 U(0,1)，返回 K-S 统计量 D 的一个样本。

    D_n = max_i max(i/n - U_(i), U_(i) - (i-1)/n)
    """
    data = []
    for _ in range(n):
        data.append(random.random())
    sorted_data = sorted(data)
    best = 0.0
    for i, u in enumerate(sorted_data, start=1):
        left = i / n - u
        right = u - (i - 1) / n
        best = max(best, left, right)
    return best


def simulate(n: int, m: int, seed: int | None = None) -> list[float]:
    """重复 m 次 one_d(n)，返回 m 个 D 的样本。

    seed 不为 None 时固定随机种子，同样的 seed 得到同样的结果。
    """
    if seed is not None:
        random.seed(seed)
    result = []
    for _ in range(m):
        result.append(one_d(n))
    return result


def ks_sample(params: dict[str,int], count: int, seed: int | None = None) -> list[float]:
    """registry 的统一入口：参数字典 + 个数 + 种子。"""
    return simulate(int(params["n"]), count, seed)


# 登记到全局注册表：key 是命令行/前端用的名字
REGISTRY["ks"] = Distribution(
    name="ks",
    params=[ParamSpec(name="n", default=100, description="样本量")],
    sampler=ks_sample,
)

"""接口定义：所有分布共用的数据结构。

这里只有「长什么样」，没有「怎么算」——具体算法在各分布自己的模块里。
"""

from dataclasses import dataclass
from typing import Callable


@dataclass
class ParamSpec:
    """一个可调参数：名字、默认值、给人看的说明。"""

    name: str
    default: float
    description: str = ""


@dataclass
class Distribution:
    """一个分布：名字、参数表、采样函数。

    sampler 的签名固定为 (params: dict, count: int, seed: int | None)
    -> list[float]，这样命令行和前端才能用同一套代码调所有分布。
    """

    name: str
    params: list[ParamSpec]
    sampler: Callable[..., list[float]]

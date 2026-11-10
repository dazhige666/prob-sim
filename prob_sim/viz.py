"""直方图：把一组样本分桶、算密度。

单一职责：只做纯计算，不读文件、不打印、不碰全局状态。
调用方读好 out/*.json 里的 samples 再传进来。
"""


def histogram(samples: list[float], bins: int) -> tuple[list[float], list[float]]:
    """把 samples 切成 bins 个等宽桶，返回 (edges, density)。

    edges:   bins + 1 个桶边界，从 min(samples) 到 max(samples) 均匀分布。
    density: bins 个桶的密度，density[i] * 桶宽 = 第 i 桶的面积；
             所有面积加起来是 1.0（概率）。

    坑：x == max(samples) 时下标会正好等于 bins，要夹到 bins - 1。
    """
    raise NotImplementedError

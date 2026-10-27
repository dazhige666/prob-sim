"""prob_sim：概率分布模拟包。

导入本包时自动完成两件事：
1. 导入 ks 模块（它的副作用是把自己的采样器登记进 REGISTRY）
2. 把 REGISTRY 暴露到包这一层，调用方可以直接 `from prob_sim import REGISTRY`
"""

from prob_sim import ks  # noqa: F401  导入即注册，别删
from prob_sim.registry import REGISTRY  # noqa: F401

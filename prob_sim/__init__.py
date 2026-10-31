"""prob_sim：概率分布模拟包。

导入本包时自动完成两件事：
1. 导入 ks 模块（它的副作用是把自己的采样器登记进 REGISTRY）
2. 把 REGISTRY 暴露到包这一层，调用方可以直接 `from prob_sim import REGISTRY`
"""

from prob_sim import ks  # noqa: F401  导入即注册，别删
from prob_sim.registry import REGISTRY  # noqa: F401

# mypy --strict 打开了 no-implicit-reexport：显式声明这是对外公开的名字，
# 这样 `from prob_sim import REGISTRY` 才不会被判成 attr-defined 错误。
__all__ = ["REGISTRY"]

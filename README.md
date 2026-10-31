# prob-sim

**一句话**：K-S 统计量的样本点模拟器。给样本量 `n` 和重复次数 `m`，输出 `m` 个 `D`，落盘成 JSON。

一期（计算部分）完成于 2026-11-01。可视化与另外三个分布属于二期。

## 现状

| 项 | 状态 |
| --- | --- |
| 核心算法（`one_d` / `simulate`） | ✅ 完成 |
| 包结构 + 注册表（加分布不改主流程） | ✅ 完成 |
| 命令行 + JSON 输出 | ✅ 完成 |
| 参数校验（`--n` / `--count`） | ✅ 完成 |
| 测试 `test_ks.py`（3 个断言） | ✅ 全绿 |
| `mypy --strict` | ✅ 零问题 |
| 可视化（直方图 + 理论曲线） | ❌ 未做（二期第一件事） |
| Gamma / Laplace / Cauchy | ❌ 未做（二期） |

**环境**：Python 3.14.0（`C:\Users\lizhi\AppData\Local\Programs\Python\Python314`），**纯标准库，禁止 numpy**。

## 文件地图

| 路径 | 职责 | 关键符号 |
| --- | --- | --- |
| `prob_sim/base.py` | 接口定义，只声明不实现 | `ParamSpec`、`Distribution` |
| `prob_sim/registry.py` | 全局注册表 | `REGISTRY: dict[str, Distribution]` |
| `prob_sim/ks.py` | K-S 的数学实现 | `one_d`、`simulate`、`ks_sample` |
| `prob_sim/__init__.py` | 导入即注册，并把 `REGISTRY` 提到包层 | `from prob_sim import REGISTRY` |
| `cli.py` | 命令行入口：解析 → 采样 → 落盘 | `main`、`force_utf8_output` |
| `test_ks.py` | 三个断言的最小测试 | — |
| `Practice/` | 学习草稿区（`play.py` 等），**不是交付代码** | — |
| `out/` | 输出目录，被 `.gitignore` 忽略 | — |

## 对外接口

```python
from prob_sim.ks import one_d, simulate, ks_sample
from prob_sim import REGISTRY

one_d(n: int) -> float
    # 抽 n 个 U(0,1)，返回一个 D。
    # D_n = max_i max(i/n - U_(i), U_(i) - (i-1)/n)

simulate(n: int, m: int, seed: int | None = None) -> list[float]
    # 重复 m 次 one_d(n)，返回 m 个 D；seed 非 None 时结果可复现。

ks_sample(params: dict[str, int], count: int, seed: int | None = None) -> list[float]
    # 注册表统一入口，从 params["n"] 取样本量。

REGISTRY["ks"] -> Distribution
    # Distribution(name="ks", params=[ParamSpec("n", 100, "样本量")], sampler=ks_sample)
```

**参数含义**：`n` = 每组样本量（正整数）；`m` / `count` = 重复次数（正整数）；`seed` = 随机种子（整数或 `None`）。

## 运行

```bash
cd prob-sim

# 默认：n=100, count=1000, 输出 out/ks.json
python cli.py

# 完整用法
python cli.py --n 50 --count 500 --seed 7 --out out/reg1.json

# 测试 / 类型检查
python test_ks.py
python -m mypy --strict prob_sim cli.py test_ks.py
```

## 输出格式

```json
{
  "distribution": "ks",
  "params": {"n": 100},
  "count": 1000,
  "seed": 42,
  "samples": [0.0431, 0.1017, ...]
}
```

`samples` 长度等于 `count`，每个元素是一个 `D`，取值在 `[0, 1]`。

## 坑与约束

- **禁止 numpy**：这是需求方定的，改用 `random` + `statistics`。
- **`seed` 只在 `simulate` 里设一次**：`random.seed(seed)` 必须在任何抽样之前；放在 `one_d` 里会变成“每组同种子”。
- **Windows 中文乱码**：写文件要 `encoding="utf-8"`；终端输出要 `force_utf8_output()`（等价 `chcp 65001`）。
- **`--out` 只给文件名时**：`os.path.dirname("ks.json")` 返回 `""`，直接 `os.makedirs("")` 会抛 `FileNotFoundError [WinError 3]`，所以要先判空。
- **`argparse` 只管类型不管值**：负数也能通过 `type=int`，值校验得自己写（用 `parser.error` 而不是 `raise`，退出码 2 且无 traceback）。
- **`Practice/` 是草稿区**：里面的代码是学习痕迹，不代表项目质量，别照着它改 `prob_sim/`。

## 三个待解问题（一期留下的）

1. **n 很大时**（10⁶ 级）排序开销是 O(n log n)，K-S 有没有更省的做法？当前 `one_d` 每轮都排一次序。
2. **理论曲线用 `K(√n·D)` 近似**，有限 n 下误差多大？要不要在可视化里改用精确分位表？
3. **离散分布**（如 Poisson）不能直接套 K-S——阶梯和理论 CDF 都有跳变，D 的分布会不同，二期要单独处理。

## 下一步

1. **可视化**：`out/*.json` 的 `samples` 画直方图，叠 `K(√n·x)` 理论曲线，纯 Python 生成 SVG/HTML（不引 numpy）。
2. **三个分布**：`gamma.py` / `laplace.py` / `cauchy.py`，各写一个 `sampler` 登记进 `REGISTRY`，主流程不动。
3. **XML 导出**：`exporters.to_xml(samples)`，给后续工具链用。

## 改动记录

| 日期 | 改了什么 |
| --- | --- |
| 2026-10-23 | 建仓，第 1 天练习（`mean` / `describe`） |
| 2026-10-27 | 第 2–5 天：加 `median`、`one_d`、`simulate`，拆出 `prob_sim/` 包 |
| 2026-10-29 | 第 6 天：`cli.py` + JSON 落盘 |
| 2026-10-31 | 第 7 天参数校验；第 8 天测试 + mypy；环境修复（PATH、Store 别名） |
| 2026-11-01 | 一期收尾：全链路回归、补本 README、打 tag `v0.1.0` |

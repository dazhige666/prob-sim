# prob-sim

概率分布模拟与可视化（课程项目）。当前阶段：个人作业 **K-S 分布**的样本点模拟，纯标准库实现（禁止 numpy）。

## 文件地图

| 路径 | 职责 | 关键内容 |
| --- | --- | --- |
| `Practice/__init__.py` | 包标记 | 空文件，让 `Practice` 可被 import |
| `Practice/play.py` | 第 1–4 天练习 | `mean` / `median` / `describe`；`main()` 调 `simulate` 打印统计量 |
| `Practice/README.md` | 本文件 | 结构、跑法、坑、学习进度、改动记录 |
| `prob_sim/__init__.py` | 包入口 | 导入 `ks`（触发注册）、导出 `REGISTRY` |
| `prob_sim/base.py` | 接口定义 | `ParamSpec`（参数描述）、`Distribution`（名字 + 参数表 + 采样函数） |
| `prob_sim/registry.py` | 分发表 | `REGISTRY: dict[str, Distribution]`，各分布模块导入时把自己塞进来 |
| `prob_sim/ks.py` | K-S 分布 | `one_d(n)` 算一个 D；`simulate(n, m, seed)` 算 m 个；`ks_sample` 是注册表入口 |

后续（还没有）：`cli.py`（命令行 + JSON 落盘）、Gamma / Laplace / Cauchy 模块。

## 运行方式

**所有命令都在 `prob-sim` 目录下执行**（`py -m` 的形式要求当前目录在 `sys.path` 里）：

```bash
# 练习脚本：必须用 -m，直接 py Practice/play.py 会因为找不到 prob_sim 包而报错
py -m Practice.play

# 包级冒烟测试
py -c "from prob_sim import REGISTRY; print(list(REGISTRY))"          # ['ks']
py -c "from prob_sim.ks import simulate; print(len(simulate(50, 10)))"  # 10
```

> 注意：这台机器上的 `python` 是 Microsoft Store 的占位程序，运行时静默退出（exit code 49）。
> 统一用 `py`（Python Launcher）调用。若控制台中文显示成乱码，先执行 `chcp 65001`。

`py -m Practice.play` 的期望输出（seed=123，n=100，m=1000）：

```
个数: 1000
均值: 0.08668
中位数: 0.08220
最大: 0.22113
最小: 0.03297
```

## 对外接口

```python
from prob_sim.ks import one_d, simulate

one_d(n: int) -> float
# 抽 n 个 U(0,1)，返回一个 K-S 统计量 D。n ≥ 1。D ∈ (0, 1)。

simulate(n: int, m: int, seed: int | None = None) -> list[float]
# 重复 m 次 one_d(n)，返回长度 m 的列表。
# seed 不为 None 时结果可复现：同 seed 两次调用逐项相同。

ks_sample(params: dict, count: int, seed: int | None = None) -> list[float]
# registry 统一签名；params 里必须有 "n"（样本量）。
```

`REGISTRY["ks"]` 是 `Distribution(name="ks", params=[ParamSpec("n", 100)], sampler=ks_sample)`。

## 坑与约束

- **不能用 numpy**：这是作业硬要求，全部用标准库（`random`、`math`、`statistics`）。
- **用 `py` 不用 `python`**：`python` 命中 Store 占位程序，静默退出（exit 49）；`py` 正常。
- **练习脚本只能用 `py -m Practice.play` 跑**：直接 `py Practice/play.py` 时 `sys.path[0]` 是 `Practice/`，看不到同级的 `prob_sim/`，会 `ModuleNotFoundError`。不要用 `sys.path.append` 打补丁。
- 包名 `Practice` 首字母大写是用户指定的写法，不按 PEP 8 小写惯例，别改。
- 包目录名是 `prob_sim`（下划线），仓库目录名是 `prob-sim`（连字符）——连字符不能出现在 `import` 语句里。
- 目录名用纯英文（`prob-sim`），避免中文路径在打包/命令行里出乱码。
- Windows 下读文件要写 `encoding="utf-8"`，写 JSON 同理。
- 采样逻辑只放模块顶层函数，模块级不要写会打印的代码（`import` 时会执行）。
- `prob_sim/base.py` 不能 import `registry` 或 `ks`，否则循环导入。

## 学习进度

### 第 1 天（2026-10-23）：语法热身

**学了**：`def` 定义函数、默认参数的位置规则、`for` 循环、累加器模式、`len/max/min`、参数与全局变量的区别。
**写了**：`mean(data)`（循环累加后除以个数）、`describe(data)`（打印三个统计量）、`main()` 入口。
**踩过的坑**：

1. **函数声明了参数却用全局变量**：`def mean(l)` 里写 `for x in xs`，参数 `l` 完全没被使用，函数只对全局 `xs` 生效。教训：参数是函数和外界唯一的接口，不接上等于没写参数。
2. **`sum = 0` 覆盖内置 `sum()`**：之后调用 `sum(...)` 会报 `'int' object is not callable`。改名 `total`。
3. **`l` 当变量名**：PEP 8 的 E741，字形像 `1`，读代码容易看错。
4. **模块级 `print` 会在 `import` 时执行**：第 5 天拆包时统一包进 `if __name__ == "__main__":`。

**验证**：`describe([100, 200])` 输出 `2 / 200 / 100`，证明参数真的生效，而不是在读全局变量。

### 第 2 天（2026-10-24）：中位数

**学了**：`sorted()` 返回新列表、`//` 整除、奇偶分支、`if/return` 早退出（不再写多余的 `else`）。
**写了**：`median(data)`，偶数个取中间两个的平均；`describe` 加一行输出。
**验证**：`median([3,1,2]) == 2.0`、`median([4,1,3,2]) == 2.5`、`describe([100,200])` 出 150.0。

### 第 3 天（2026-10-25）：一个 D

**学了**：`random.random()` 产生 U(0,1)、`enumerate(..., start=1)` 让序号从 1 开始、循环里用 `best = max(best, left, right)` 累积最大值。
**写了**：`one_d(n)`。
**踩过的坑**：

1. **`max = 0.0` 覆盖内置 `max()`**：改用 `best`。
2. **`max = right` 无条件执行**：把上一轮存下的 `left` 冲掉，等价于只取最后一个点。改用 `best = max(best, left, right)`。
3. **`best = ...` 少缩进 4 格**：语句跑到 `for` 外面，循环里什么也没累积。Python 靠缩进划分代码块。

**验证**：每个 n 跑 2000 次取中位数——n=10/100/1000 得 0.2458/0.0826/0.0260，与理论值 0.83/√n 吻合；结果恒为正且 < 1。

### 第 4 天（2026-10-26）：重复 m 次

**学了**：`seed: int | None = None` 联合类型注解、默认参数、`random.seed()` 必须在抽数之前、列表累积两种写法（append / 推导式）。
**写了**：`simulate(n, m, seed)`。
**踩过的坑**：`[one_d(n)] * m` 只调用一次再复制，m 个值全相同；`random.seed(seed)` 放进循环会导致每次重置同一串随机数。
**验证**：同 seed 两次结果逐项相同；换 seed 不同；n=100 的 m=1000 个 D 中位数 0.0825 ≈ 0.83/√100。

### 第 5 天（2026-10-27）：拆包

**学了**：包 = 带 `__init__.py` 的目录；`import` 靠 `sys.path` 找模块，直接跑脚本时 `sys.path[0]` 是脚本所在目录；`@dataclass` 自动生成 `__init__`/`__repr__`；注册表模式（模块导入时把自己的采样器登记进 `REGISTRY`，调用方只认名字）。
**写了**：`prob_sim/` 四个文件；`ks.py` 末尾登记 `REGISTRY["ks"]`；`play.py` 改为从包里 import。
**踩过的坑**：

1. **文件建在仓库根**：`base.py`/`ks.py` 必须是 `prob_sim/` 目录里的文件，否则 `from prob_sim.ks import ...` 找不到。
2. **`_init_.py` 拼写**：`__init__.py` 前后各两个下划线，少一个就不算包标记。
3. **根目录残留 `__init__.py`**：会把整个仓库根当成包，导入路径混乱。
4. **`from prob_sim import REGISTRY` 报 ImportError**：空的 `__init__.py` 不会导出子模块里的名字，要在 `__init__.py` 里显式 `from prob_sim.registry import REGISTRY`。

**验证**：`list(REGISTRY) == ['ks']`；`len(simulate(50, 10, seed=1)) == 10`；`py -m Practice.play` 输出五行统计。

### 第 6 天（2026-10-29）：cli + JSON 落盘

**学了**：`argparse` 的选项 vs 位置参数、`--x` 去掉横线才是属性名、`dest` 改属性名、`parse_args()` 返回 `Namespace`、`json.dump` + `encoding="utf-8"` + `ensure_ascii=False`、`os.path.dirname` 对纯文件名返回空字符串。

**写了**：`cli.py` —— `main()` 里五步：取 `REGISTRY["ks"]` → 解析四参数 → 调 `sampler` → 建目录 → 写 JSON。

**踩过的坑**：

1. **`print(parser)` 看不到解析结果**：`args = parser.parse_args()` 那一行才产生 `args`；打印 `parser` 只会得到解析器对象。
2. **`--n` 和 `n` 不是一回事**：注册时带横线是选项（`--n 50`），不带是位置参数（`50`），后者传 `--n` 会 `unrecognized arguments`。
3. **`--out ks.json` 时 `dirname` 返回 `""`**：`os.makedirs("")` 抛 `FileNotFoundError`，要先 `if out_dir:`。
4. **`mian` 拼成 `main` 的笔误**：两处一致所以不报错，但 `from cli import main` 会失败。

**验证**：`py cli.py --n 100 --count 1000 --seed 42` 生成 `out/ks.json`，五键齐全、`samples` 长度 1000；`--out bare.json` 不崩；同 seed 两次 `samples` 逐项相同。

### 第 8 天（待做）：mypy 静态检查 + 变量可视化

**任务**：

1. 装：`py -m pip install mypy`（联网装到用户目录，不动系统 Python）
2. 跑：`py -m mypy prob_sim`
3. 看报错：mypy 会输出 `error: Argument 1 to "..." has incompatible type "..."` 并带行号指向问题——这就是 Python 版的「编译期报错」
4. 修到 `Success: no issues found in N source files`
5. **可视化**：把 `one_d(4)` 的代码贴进 https://pythontutor.com ，单步执行，看 `sorted_data` 和 `best` 每一轮怎么变

**为什么要做**：Python 默认只在运行到那一行时才检查类型，mypy 把这件事提前到「写完就能查」。初学者看一次「注解写错 → 工具精确指出哪一行哪个参数」，对类型系统的理解会比读十页文档都实感。

## 改动记录

- 2026-10-23：创建 `prob-sim/Practice/`，写第 1 天练习 `play.py`（`mean` / `describe`），跑通输出 3.875。
- 2026-10-23：用户手写 `play.py` 完成第 1 天任务；`mean`/`describe` 已改为使用参数而非全局变量，`describe([100,200])` 验证输出 2/200/100。
- 2026-10-23：按约定重写 `play.py`——补 docstring、类型注解、`main()` 入口、`if __name__ == "__main__"` 保护，统一命名与空格；行为不变。
- 2026-10-27：第 2 天加 `median()`；第 3 天加 `one_d()`；第 4 天加 `simulate()`（均用户手写，我审校）。
- 2026-10-27：第 5 天拆出 `prob_sim/` 包（`__init__` / `base` / `registry` / `ks`）；修 `__init__.py` 未导出 `REGISTRY`、`ks.py` 导入位置与空格；README 补齐接口、运行方式与第 2–5 天学习进度。
- 2026-10-29：加入第 8 天任务（mypy 静态检查 + pythontutor 变量可视化），排在第 6–7 天（cli + 校验）之后。
- 2026-10-29：第 6 天 `cli.py`（argparse + JSON 落盘）；注释补齐六步流程，修 `mian`→`main`、default 改从 `dist.params` 取。

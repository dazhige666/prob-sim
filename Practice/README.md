# prob-sim · Practice（练习区）

学习过程记录，**不属于交付物**。项目本身的说明见 [../README.md](../README.md)。

## 这个目录是什么

练习草稿区，不算交付物：

- `basics.py` —— 第 1–4 天练习（`mean` / `median` / `describe`）

交付代码在上一层（`prob_sim/` + `cli.py`）；**文件地图、对外接口、运行方式、项目级坑**都在 [../README.md](../README.md)，这里不重复。

## 跑练习

必须用 `-m`，且当前目录是 `prob-sim/`（直接 `py Practice/basics.py` 会因为找不到 `prob_sim` 包报错）：

```bash
py -m Practice.basics
```

期望输出（`seed=123`，`n=100`，`m=1000`）：

```
个数: 1000
均值: 0.08668
中位数: 0.08220
最大: 0.22113
最小: 0.03297
```

## 第 9 天练习：两个 demo（2026-11-01 完成）

目标：证明样本点能“出境”的两条路（HTTP / XML）。只读注册表，**不改 `prob_sim/`**。

**A. `demo_flask.py`**

- 两个路由：`/` 返回一行 HTML；`/api/ks` 读查询参数 `n` / `count` / `seed`，调用 `REGISTRY["ks"].sampler(...)`，返回和 `out/ks.json` 同结构的 JSON
- 验收：`py -m Practice.demo_flask` → 浏览器看 `http://127.0.0.1:5000/api/ks?n=50&count=7`，`samples` 有 7 个
- 三个坑：5000 被占就换端口；`debug=True` 会开两个进程；查询参数永远是字符串，`int()` 失败要给 400 而不是 500

**B. `demo_xml.py`**

- 读 `out/ks.json`，用 `xml.etree.ElementTree` 写成 `<ks n=.. count=.. seed=..><d i="1">0.072026</d>...</ks>`
- 验收：`ET.parse("out/ks.xml")` 的根 `tag == "ks"`，`len(root)` 等于样本数
- 坑：节点文本只能存字符串，浮点要 `f"{x:.6f}"`；写文件要指定 `encoding="utf-8"`

依赖：A 需要 `flask`（本机 3.1.3 已装），其余纯标准库。

## 练习区约定

- 包名 `Practice` 首字母大写是刻意写法，不按 PEP 8 改。
- 直接用 `py Practice/basics.py` 会 `ModuleNotFoundError`；不要用 `sys.path.append` 打补丁。
- 这里可以随便改、随便删，过期也不用留。

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
**写了**：`prob_sim/` 四个文件；`ks.py` 末尾登记 `REGISTRY["ks"]`；`basics.py` 改为从包里 import。
**踩过的坑**：

1. **文件建在仓库根**：`base.py`/`ks.py` 必须是 `prob_sim/` 目录里的文件，否则 `from prob_sim.ks import ...` 找不到。
2. **`_init_.py` 拼写**：`__init__.py` 前后各两个下划线，少一个就不算包标记。
3. **根目录残留 `__init__.py`**：会把整个仓库根当成包，导入路径混乱。
4. **`from prob_sim import REGISTRY` 报 ImportError**：空的 `__init__.py` 不会导出子模块里的名字，要在 `__init__.py` 里显式 `from prob_sim.registry import REGISTRY`。

**验证**：`list(REGISTRY) == ['ks']`；`len(simulate(50, 10, seed=1)) == 10`；`py -m Practice.basics` 输出五行统计。

### 第 6 天（2026-10-29）：cli + JSON 落盘

**学了**：`argparse` 的选项 vs 位置参数、`--x` 去掉横线才是属性名、`dest` 改属性名、`parse_args()` 返回 `Namespace`、`json.dump` + `encoding="utf-8"` + `ensure_ascii=False`、`os.path.dirname` 对纯文件名返回空字符串。

**写了**：`cli.py` —— `main()` 里五步：取 `REGISTRY["ks"]` → 解析四参数 → 调 `sampler` → 建目录 → 写 JSON。

**踩过的坑**：

1. **`print(parser)` 看不到解析结果**：`args = parser.parse_args()` 那一行才产生 `args`；打印 `parser` 只会得到解析器对象。
2. **`--n` 和 `n` 不是一回事**：注册时带横线是选项（`--n 50`），不带是位置参数（`50`），后者传 `--n` 会 `unrecognized arguments`。
3. **`--out ks.json` 时 `dirname` 返回 `""`**：`os.makedirs("")` 抛 `FileNotFoundError`，要先 `if out_dir:`。
4. **`mian` 拼成 `main` 的笔误**：两处一致所以不报错，但 `from cli import main` 会失败。

**验证**：`py cli.py --n 100 --count 1000 --seed 42` 生成 `out/ks.json`，五键齐全、`samples` 长度 1000；`--out bare.json` 不崩；同 seed 两次 `samples` 逐项相同。

### 第 7 天（2026-10-31）：参数校验 + 输出编码

**学了**：`parser.error()` 与 `raise` 的区别（前者打印 usage、退出码 2、无 traceback）、`sys.stdout.reconfigure()` 改流编码、fail fast（解析完立刻校验，别算完才发现）。
**写了**：`cli.py` 加两条 `if args.n < 1` / `if args.count < 1` 校验；`force_utf8_output()` 统一输出编码。
**踩过的坑**：

1. **提示文案和条件不一致**：条件是 `< 1`（允许 1），文案写「必须大于1」（暗示 1 不行）。文案要能复述条件本身。
2. **`if args.n < 1 :` 冒号前多空格**（PEP 8 E203）。
3. **管道里中文乱码**：不是代码错，是流的编码（GBK）和内容（UTF-8）不匹配；`reconfigure(encoding="utf-8")` 解决。

**验证**：`--n 0` / `--n -5` / `--count 0` / `--n abc` 全部退出码 2，`--n 1 --count 1` 正常放行；正常命令照常出 JSON。

### 第 8 天（2026-10-31 完成）：测试 + mypy

**A. 测试 `test_ks.py`**：三个断言——D 全在 [0,1]、中位数落在 0.83/√50 的 ±30%、`simulate(50, 2000, seed=42)` 两次逐项相等。做了变异测试（把阈值改成 `median > 0.5`）确认断言真的会炸。

**B. mypy**：`py -m pip install mypy`（2.4.1）→ `py -m mypy prob_sim` 一次 `Success`；但那是注解宽松的结果，`--strict` 才逼出一条真问题：

```
prob_sim\ks.py:43: error: Missing type arguments for generic type "dict"  [type-arg]
```

改成 `dict[str, int]` 后 `--strict` 也 `Success: no issues found in 4 source files`。

**学到的一件事**：mypy 普通模式通过 ≠ 类型没问题，它只查你标注出来的部分；`--strict` 才把容器的元素类型也纳入检查。

**未做（可选）**：pythontutor 单步 `one_d(4)`。

### 第 9 天（2026-11-01）：两条出口——HTTP 与 XML

**学了**：Flask 的最小骨架（`@app.route` + 查询参数 + `jsonify`）、查询参数永远是字符串所以要显式 `int()`、400 与 500 的分工；`ElementTree` 四件套（`Element` / `SubElement` / `set` / `text`）、`.write(..., encoding="utf-8", xml_declaration=True)`；路径的三种写法（绝对、相对 cwd、`Path(__file__).parent`）以及 `mkdir(parents=True, exist_ok=True)`。

**写了**：`demo_flask.py`（`GET /api/ks?n=&count=&seed=`）、`demo_xml.py`（采样 → 建树 → 写 `out/ks.xml` → 读回校验）。两份都补了注释，说明每一步"为什么"而不只是"做什么"。

**踩过的坑**：

1. **`SubElement` 写在循环外**：只建了一个 `<d>`，循环里反复改它，最后只剩最后一个值（`len(root) == 1`）。子节点是"每轮一个"，必须和 `set`/`text` 一起放进循环体。
2. **`write()` 不给 `encoding`**：默认写 `us-ascii`，声明和实际内容口径不一致。
3. **相对路径跟着 cwd 走**：同一个 `"test.xml"`，从 `prob-sim/` 跑和从 `Practice/` 跑落在两个不同目录。
4. **`Path(__file__)` 只管写文件，不管 import**：在 `Practice/` 里 `py demo_xml.py` 仍会 `ModuleNotFoundError: No module named 'prob_sim'`——模块查找看的是 `sys.path`，所以还是得在 `prob-sim/` 根目录用 `-m`。

**验证**：`/api/ks?n=100&count=5&seed=7` 返回 200 且 `samples` 长度 5、键名与 `cli.py` 一致；`n=abc` 返回 400 + 中文错误；同 seed 两次逐字节相同。`out/ks.xml` 解析后 `tag=ks`、`attrib={n:100,count:1000}`、`len(root)=1000`、每个 `<d>` 恰好 6 位小数。

## 改动记录

- 2026-10-23：创建 `prob-sim/Practice/`，写第 1 天练习 `basics.py`（`mean` / `describe`），跑通输出 3.875。
- 2026-10-23：用户手写 `basics.py` 完成第 1 天任务；`mean`/`describe` 已改为使用参数而非全局变量，`describe([100,200])` 验证输出 2/200/100。
- 2026-10-23：按约定重写 `basics.py`——补 docstring、类型注解、`main()` 入口、`if __name__ == "__main__"` 保护，统一命名与空格；行为不变。
- 2026-10-27：第 2 天加 `median()`；第 3 天加 `one_d()`；第 4 天加 `simulate()`（均用户手写，我审校）。
- 2026-10-27：第 5 天拆出 `prob_sim/` 包（`__init__` / `base` / `registry` / `ks`）；修 `__init__.py` 未导出 `REGISTRY`、`ks.py` 导入位置与空格；README 补齐接口、运行方式与第 2–5 天学习进度。
- 2026-10-29：加入第 8 天任务（mypy 静态检查 + pythontutor 变量可视化），排在第 6–7 天（cli + 校验）之后。
- 2026-10-29：第 6 天 `cli.py`（argparse + JSON 落盘）；注释补齐六步流程，修 `mian`→`main`、default 改从 `dist.params` 取。
- 2026-10-31：第 7 天参数校验（`parser.error`，退出码 2）；加 `force_utf8_output()` 修管道中文乱码；README 补第 7 天进度。
- 2026-10-31：第 8 天 `test_ks.py`（三个断言，变异测试确认有效）；mypy 2.4.1；`--strict` 逼出 `ks.py:43` 的 `dict` 缺参数并修成 `dict[str, int]`。
- 2026-10-31：解释器环境修复——用户 PATH 前置 Python314 目录、删除 WindowsApps 里的 Store 别名；README 同步说明。
- 2026-11-01：一期收尾——全链路回归（n=50 / n=1000 的 D 中位数与 0.83/√n 吻合）、补项目级 `README.md`（文件地图/接口/坑/三个待解问题）、打 tag `v0.1.0`。第 9 天 `demo_flask.py` / `demo_xml.py` 未写（预习性质，不算交付）。
- 2026-11-01：`play.py` 改名 `basics.py`（名字说明内容而非状态）；新增第 9 天两个 demo（`demo_flask.py` / `demo_xml.py`），均已实测跑通。
- 2026-11-01：删掉我代写的两个 demo 草稿，README 第 9 天一节改为「任务要求 + 验收」；练习由一个写成一个审。
- 2026-11-01：第 9 天 A 完成——`demo_flask.py` 键名统一为 `samples`，补注释；实测 200 / 400 / 同 seed 复现三种情形。
- 2026-11-01：第 9 天 B 完成——`demo_xml.py` 修三个问题（`SubElement` 移进循环、根节点补属性、`write` 指定 utf-8），改用 `Path(__file__)` 定位输出，补读回校验与注释。`out/ks.xml` 1000 个子节点、全部 6 位小数。
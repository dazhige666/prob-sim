# prob-sim

概率分布模拟与可视化（课程项目）。当前阶段：个人作业 **K-S 分布**的样本点模拟，纯标准库实现（禁止 numpy）。

## 文件地图

| 路径 | 职责 | 关键内容 |
| --- | --- | --- |
| `Practice/__init__.py` | 包标记 | 空文件，让 `Practice` 可被 import |
| `Practice/play.py` | 第 1 天练习 | `mean(data)` 手写均值；`describe(data)` 打印个数/最大/最小；`main()` 跑示例 |
| `Practice/README.md` | 本文件 | 结构、跑法、坑、学习进度、改动记录 |

后续（按 10 天计划逐步加，现在还没有）：
`prob_sim/base.py`、`prob_sim/registry.py`、`prob_sim/ks.py`、`cli.py`。

## 运行方式

在 `prob-sim` 目录下：

```bash
py Practice/play.py
# 或
py -m Practice.play
```

> 注意：这台机器上的 `python` 是 Microsoft Store 的占位程序，运行时静默退出（exit code 49）。
> 统一用 `py`（Python Launcher）调用。若控制台中文显示成乱码，先执行 `chcp 65001`。

期望输出：

```
平均值: 3.0
另一组平均值: 35.0
个数: 5
最大: 5
最小: 1
```

## 坑与约束

- **不能用 numpy**：这是作业硬要求，全部用标准库（`random`、`math`、`statistics`）。
- **用 `py` 不用 `python`**：`python` 命中 Store 占位程序，静默退出（exit 49）；`py` 正常。
- 包名 `Practice` 首字母大写是用户指定的写法，不按 PEP 8 小写惯例，别改。
- 目录名用纯英文（`prob-sim`），避免中文路径在打包/命令行里出乱码。
- Windows 下读文件要写 `encoding="utf-8"`，写 JSON 同理。
- 作业里所有分发/采样逻辑都放在模块顶层函数里，模块级不要写会打印的代码（`import` 时会执行）。

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
**下一步**：第 2 天给 `describe` 加"中位数"——`sorted(data)` 排序 + `len(data) // 2` 取中间。

## 改动记录

- 2026-10-23：创建 `prob-sim/Practice/`，写第 1 天练习 `play.py`（`mean` / `describe`），跑通输出 3.875。
- 2026-10-23：用户手写 `play.py` 完成第 1 天任务；`mean`/`describe` 已改为使用参数而非全局变量，`describe([100,200])` 验证输出 2/200/100。
- 2026-10-23：按约定重写 `play.py`——补 docstring、类型注解、`main()` 入口、`if __name__ == "__main__"` 保护，统一命名与空格；行为不变。

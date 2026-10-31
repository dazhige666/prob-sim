"""命令行入口：解析参数 → 调 REGISTRY → 写 JSON。

用法（在 prob-sim 目录下执行）：
    py cli.py --n 100 --count 1000 --seed 42
    py cli.py --n 50 --count 200 --out out/small.json
"""

# ── 参数命名笔记（2026-10-29 加，写代码前先读一遍）──────────────────────
# add_argument("--n")  → 选项：命令行写 `--n 50`，代码里用 args.n
# add_argument("n")    → 位置参数：命令行写 `py cli.py 50`，代码里同样是 args.n
#
# 属性名都是 args.n，区别只在命令行怎么给：
#   - 带 --：它是"带名字的可选参数"，不带 -- 就传不进来
#   - 不带 --：它按位置排队，用户多写 --n 会报
#             `error: unrecognized arguments: --n`
# 所以 `--` 不是装饰，它是在声明"这是个带名字的可选参数"。
#
# 想改属性名用 dest：add_argument("--n", dest="sample_size")
#     → 命令行仍是 --n，代码里用 args.sample_size
# 横线自动转下划线：--sample-size → args.sample_size
# ─────────────────────────────────────────────────────────────────────

import argparse
import json
import os
import sys

from prob_sim import REGISTRY


def force_utf8_output() -> None:
    """把 stdout/stderr 切成 UTF-8，等价于先在终端执行 `chcp 65001`。

    Windows 终端默认代码页是 936（GBK），中文经管道或重定向输出时
    会变成乱码；统一成 UTF-8 后，cmd / PowerShell / Git Bash 里都对。
    某些被替换过的 stream 没有 reconfigure（或被关闭），跳过即可。
    """
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def main() -> None:
    """一次完整的运行：取分布 → 解析参数 → 采样 → 落盘。"""
    force_utf8_output()
    # 1. 从注册表按名字取分布。
    #    只认名字不认函数，以后换 gamma 只改这一个字符串。
    dist = REGISTRY["ks"]

    # 2. 声明命令行参数。
    #    --n 的默认值从 dist.params 拿，保证默认值只有一处来源；
    #    --count / --seed / --out 是所有分布共用的，不属于某个分布。
    parser = argparse.ArgumentParser(description="K-S 统计量采样")
    parser.add_argument("--n", type=int, default=dist.params[0].default, help="每组样本量")
    parser.add_argument("--count", type=int, default=1000, help="重复多少次")
    parser.add_argument("--seed", type=int, default=None, help="随机种子，给了就可复现")
    parser.add_argument("--out", default="out/ks.json", help="输出 JSON 路径")
    args = parser.parse_args()
    # 3. 校验参数值。argparse 只保证"类型对"，不保证"值合理"。
    #    用 parser.error 而不是 raise：它会打印 usage 一行、退出码 2，没有 traceback。
    if args.n < 1:
        parser.error(f"--n必须大等于1，收到{args.n}")
    if args.count < 1:
        parser.error(f"--count必须大等于1，收到{args.count}")

    # 4. 采样。params 用字典传，这是 registry 约定的统一签名：
    #    命令行和前端都走这一个入口，不用认识具体分布。
    samples = dist.sampler({"n": args.n}, seed=args.seed, count=args.count)

    # 5. 准备输出目录。
    #    --out 只给文件名时 dirname 返回空字符串，此时不建目录（直接写当前目录）。
    out_dir = os.path.dirname(args.out)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    # 6. 组装要落盘的内容。
    #    params 用推导式从规格生成：以后加 shape/scale，这里一个字不用改。
    payload = {
        "distribution": dist.name,
        "params": {spec.name: getattr(args, spec.name) for spec in dist.params},
        "count": args.count,
        "seed": args.seed,
        "samples": samples,
    }

    # 7. 写 JSON。encoding="utf-8" 防 Windows 乱码，
    #    ensure_ascii=False 让中文保持原样而不是被转成 \uXXXX。
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False)


if __name__ == "__main__":
    main()

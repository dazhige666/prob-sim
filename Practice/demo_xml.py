"""第 9 天 demo B：把 out/ks.json 的 samples 转成 XML。

跑法（必须在 prob-sim/ 目录下，且先跑过一次 cli.py）：
    py cli.py --n 100 --count 1000 --seed 42 --out out/ks.json
    py -m Practice.demo_xml

产物 out/ks.xml 长这样：
    <?xml version='1.0' encoding='utf-8'?>
    <ks n="100" count="10" seed="42">
      <d i="1">0.043100</d>
      <d i="2">0.101700</d>
    </ks>

要点：XML 是树，Element 是节点；文本内容永远当字符串存，浮点要自己格式化。
"""
from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path

SRC = Path("out/ks.json")
DST = Path("out/ks.xml")


def build_tree(data: dict) -> ET.Element:
    """把 cli.py 产出的 JSON 字典转成 Element 树。"""
    seed = data.get("seed")
    root = ET.Element(
        "ks",
        {
            "n": str(data["params"]["n"]),
            "count": str(data["count"]),
            "seed": "" if seed is None else str(seed),
        },
    )
    for i, value in enumerate(data["samples"], start=1):
        ET.SubElement(root, "d", {"i": str(i)}).text = f"{value:.6f}"
    return root


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"找不到 {SRC}，先跑一次 cli.py 生成它")
    data = json.loads(SRC.read_text(encoding="utf-8"))
    root = build_tree(data)

    # 缩进一下，方便人眼也方便 diff；ElementTree 3.9+ 自带
    ET.indent(root)
    ET.ElementTree(root).write(DST, encoding="utf-8", xml_declaration=True)
    print(f"{DST} 写入 {len(root)} 个样本点")


if __name__ == "__main__":
    main()

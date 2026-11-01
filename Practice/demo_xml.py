"""第 9 天 B：把一组 K-S 统计量 D 写成 XML，再读回来验证。

跑法（必须在 prob-sim/ 根目录，否则找不到 prob_sim 包）：

    py -m Practice.demo_xml

产物：Practice/out/ks.xml
"""

import xml.etree.ElementTree as ET
from pathlib import Path

from prob_sim import REGISTRY


def main() -> None:
    dist = REGISTRY["ks"]
    samples = dist.sampler({"n": 100}, count=1000, seed=42)

    # 根节点是"外箱"，属性是箱子上贴的标签。set() 只接受字符串。
    root = ET.Element("ks")
    root.set("n", "100")
    root.set("count", "1000")

    # 子节点是"每轮一个"：SubElement 必须在循环体内，
    # 放外面就变成反复改同一个 <d>，最后只剩最后一个值。
    for i, x in enumerate(samples, start=1):
        d = ET.SubElement(root, "d")
        d.set("i", str(i))
        d.text = f"{x:.6f}"  # 文本也只能是字符串，浮点先格式化

    # 用脚本自身位置定位输出目录：从哪个 cwd 启动都写到同一处
    base = Path(__file__).resolve().parent
    out = base / "out" / "ks.xml"
    out.parent.mkdir(parents=True, exist_ok=True)  # out/ 不存在就建，已有不报错

    # 没有 encoding 时默认写 us-ascii，声明和实际口径会不一致
    ET.ElementTree(root).write(out, encoding="utf-8", xml_declaration=True)

    # 写进去 ≠ 写对了：解析回来数一遍子节点，这才叫验收
    back = ET.parse(out).getroot()
    print(f"写到 {out}")
    print(f"tag={back.tag} attrib={back.attrib} 子节点数={len(back)}")


if __name__ == "__main__":
    main()

"""第 9 天 demo A：用 Flask 把 K-S 样本点从 HTTP 吐出去。

跑法（必须在 prob-sim/ 目录下）：
    py -m Practice.demo_flask

然后浏览器打开：
    http://127.0.0.1:5000/api/ks?n=50&count=7

和 CLI 的关系：JSON 的五个键与 out/ks.json 一致（distribution / params / count / seed / samples），
区别只在于数据走网络而不是落盘。

这不是交付物：没有日志、没有并发考虑、debug 全关。它存在的意义是证明
"prob_sim 内核可以被另一种入口调用一遍还不改一行代码"。
"""
from __future__ import annotations

from flask import Flask, jsonify, request

from prob_sim import REGISTRY

app = Flask(__name__)


@app.get("/")
def index() -> str:
    """一行 HTML，方便确认服务活着。"""
    return "<h1>prob-sim</h1><p>试试 <code>/api/ks?n=50&amp;count=7</code></p>"


@app.get("/api/ks")
def api_ks():
    """查询参数 n / count / seed → K-S 样本点 JSON。

    参数全是字符串，得自己转；坏输入返回 400 而不是 500。
    """
    try:
        n = int(request.args.get("n", "100"))
        count = int(request.args.get("count", "1000"))
        seed_raw = request.args.get("seed")
        seed = int(seed_raw) if seed_raw is not None else None
    except ValueError:
        return jsonify({"error": "n / count / seed 必须是整数"}), 400

    if n < 1 or count < 1:
        return jsonify({"error": "n 和 count 必须 >= 1"}), 400

    dist = REGISTRY["ks"]
    samples = dist.sampler({"n": n}, count=count, seed=seed)
    return jsonify(
        {
            "distribution": dist.name,
            "params": {"n": n},
            "count": count,
            "seed": seed,
            "samples": samples,
        }
    )


if __name__ == "__main__":
    # debug=False：开了重载器会起两个进程，日志会重复
    app.run(host="127.0.0.1", port=5000, debug=False)

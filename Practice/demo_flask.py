"""第 9 天 A：用 Flask 把 K-S 采样暴露成 HTTP 接口。

跑法（必须在 prob-sim/ 根目录，否则找不到 prob_sim 包）：

    py -m Practice.demo_flask

然后用浏览器打开：

    http://127.0.0.1:5000/api/ks?n=100&count=5&seed=7
"""

from flask import Flask, jsonify, request

from prob_sim import REGISTRY

app = Flask(__name__)
# 中文错误信息直接输出，而不是转成 \uXXXX（和 cli.py 的 ensure_ascii=False 一致）
app.json.ensure_ascii = False


@app.route("/api/ks")
def api_ks():
    # 查询参数永远是字符串：显式 int() 转换，失败回 400，
    # 否则 ValueError 会窜成 500，调用方分不清是自己参数错还是服务坏了。
    try:
        n = int(request.args.get("n", 100))
        count = int(request.args.get("count", 1000))
        seed_raw = request.args.get("seed")
        seed = int(seed_raw) if seed_raw is not None else None
    except ValueError:
        return {"error": "n/count/seed 必须为整数"}, 400

    # 只读注册表，不碰 prob_sim/ 内部实现
    dist = REGISTRY["ks"]
    samples = dist.sampler({"n": n}, count=count, seed=seed)

    # 键名与 cli.py 导出的 JSON 保持同一份口径（distribution/params/count/seed/samples）
    return jsonify(
        distribution=dist.name,
        params={"n": n},
        count=count,
        seed=seed,
        samples=samples,
    )


if __name__ == "__main__":
    app.run()

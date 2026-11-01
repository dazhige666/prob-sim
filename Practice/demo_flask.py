from flask import Flask, jsonify, request
from prob_sim import REGISTRY

app = Flask(__name__)


@app.route("/api/ks")
def api_ks():
    try:
        n = int(request.args.get("n", 100))
        count = int(request.args.get("count", 1000))
        seed_raw = request.args.get("seed")
        seed = int(seed_raw) if seed_raw is not None else None

    except ValueError:
        return {"error":"n/count/seed必须为整数"},400

    dist = REGISTRY["ks"]
    samples = dist.sampler({"n":n}, count=count, seed=seed)

    return {"distribution":dist.name, "params":{"n":n}, "count":count, "seed":seed, "samples":samples}





if __name__ == "__main__":
    app.run()
import argparse

from prob_sim import REGISTRY

parser = argparse.ArgumentParser()
parser.add_argument("--n", type=int,default=100)
parser.add_argument("--count", type=int,default=1000)
parser.add_argument("--seed", type=int,default=None)
parser.add_argument("--out", default="out/ks.json")
args = parser.parse_args()


# print(args)


dist = REGISTRY["ks"]
samples = dist.sampler({"n": args.n}, seed=args.seed, count=args.count)


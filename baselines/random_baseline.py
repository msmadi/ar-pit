"""Random baseline: a uniform score in [0, 1]; paraphrase if score >= 0.5.

Usage: python -m baselines.random_baseline data/test.data [--seed 0] > random.output
"""
import argparse
import random

from arpi import load_pairs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("test")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    for _ in load_pairs(args.test):
        s = rng.random()
        print(f"{'true' if s >= 0.5 else 'false'}\t{s:.4f}")


if __name__ == "__main__":
    main()

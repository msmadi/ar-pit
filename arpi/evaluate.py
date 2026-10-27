"""Score system output against gold labels (PIT-2015 metrics).

Usage:
    python -m arpi.evaluate GOLD SYSTEM

GOLD:   a .label file (or a .data file with labels in field 5)
SYSTEM: one line per test pair: "true|false<TAB>score" with score in [0, 1].
        A line holding only a score is also accepted (label = score >= 0.5).

T1:PI  - precision / recall / F1 for the paraphrase class, debatable gold pairs excluded.
T2:STS - Pearson r between system score and gold 0-5 score over all pairs, plus
         maxF1 (and its precision / recall) over the precision-recall curve.
"""
from __future__ import annotations

import math
import sys
from typing import List, Optional, Sequence, Tuple

from .io import DEBATABLE, PARAPHRASE, load_labels, load_pairs, score_to_pi


def read_system(path: str) -> List[Tuple[bool, float]]:
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            cols = line.split()
            if len(cols) >= 2:
                out.append((cols[0].lower() == "true", float(cols[1])))
            else:
                s = float(cols[0])
                out.append((s >= 0.5, s))
    return out


def read_gold(path: str) -> List[Optional[int]]:
    if path.endswith(".data"):
        return [p.score for p in load_pairs(path)]
    return load_labels(path)


def prf(gold: Sequence[bool], pred: Sequence[bool]) -> Tuple[float, float, float]:
    tp = sum(g and p for g, p in zip(gold, pred))
    fp = sum((not g) and p for g, p in zip(gold, pred))
    fn = sum(g and not p for g, p in zip(gold, pred))
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    return prec, rec, f1


def pearson(x: Sequence[float], y: Sequence[float]) -> float:
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    return sxy / math.sqrt(sxx * syy) if sxx and syy else 0.0


def max_f1(gold: Sequence[bool], scores: Sequence[float]) -> Tuple[float, float, float]:
    """Best F1 over every threshold on the system score."""
    best = (0.0, 0.0, 0.0)  # f1, p, r
    for t in sorted(set(scores)):
        p, r, f = prf(gold, [s >= t for s in scores])
        if f > best[0]:
            best = (f, p, r)
    return best[0], best[1], best[2]


def evaluate(gold_scores: List[Optional[int]], system: List[Tuple[bool, float]]) -> dict:
    if len(gold_scores) != len(system):
        raise ValueError(f"gold has {len(gold_scores)} pairs, system output has {len(system)}")

    # T1:PI on non-debatable pairs
    keep = [i for i, g in enumerate(gold_scores) if g is not None and score_to_pi(g) != DEBATABLE]
    g_pi = [score_to_pi(gold_scores[i]) == PARAPHRASE for i in keep]
    p_pi = [system[i][0] for i in keep]
    pi_p, pi_r, pi_f = prf(g_pi, p_pi)

    # T2:STS on all labelled pairs
    idx = [i for i, g in enumerate(gold_scores) if g is not None]
    gs = [float(gold_scores[i]) for i in idx]
    ss = [system[i][1] for i in idx]
    r = pearson(ss, gs)
    # maxF1 is computed on the non-debatable pairs, as in the PIT-2015 scorer
    mf, mp, mr = max_f1(g_pi, [system[i][1] for i in keep])

    return {
        "PI_F1": pi_f, "PI_Precision": pi_p, "PI_Recall": pi_r,
        "STS_Pearson": r, "STS_maxF1": mf, "STS_maxPrecision": mp, "STS_maxRecall": mr,
        "n_PI": len(keep), "n_STS": len(idx),
    }


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        sys.exit(1)
    res = evaluate(read_gold(argv[0]), read_system(argv[1]))
    print(f"T1:PI   F1={res['PI_F1']:.3f}  P={res['PI_Precision']:.3f}  R={res['PI_Recall']:.3f}  (n={res['n_PI']})")
    print(f"T2:STS  Pearson={res['STS_Pearson']:.3f}  maxF1={res['STS_maxF1']:.3f}  "
          f"maxP={res['STS_maxPrecision']:.3f}  maxR={res['STS_maxRecall']:.3f}  (n={res['n_STS']})")


if __name__ == "__main__":
    main()

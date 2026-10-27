"""Smoke tests on a tiny fixture built from the guideline examples.

Run: python -m pytest tests/   (or: python tests/test_smoke.py)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from arpi import load_labels, load_pairs, parse_label, score_to_pi
from arpi.evaluate import evaluate

FIX = Path(__file__).parent / "fixtures"


def test_label_parsing():
    assert parse_label("(3, 2)") == 3
    assert parse_label("(2,3)") == 2
    assert parse_label("5") == 5
    assert parse_label("") is None
    assert [score_to_pi(s) for s in range(6)] == [
        "non-paraphrase", "non-paraphrase", "debatable",
        "paraphrase", "paraphrase", "paraphrase"]


def test_load():
    train = load_pairs(FIX / "train.data")
    assert len(train) == 5
    assert [p.pi_label for p in train] == [
        "paraphrase", "paraphrase", "non-paraphrase", "non-paraphrase", "debatable"]
    assert load_labels(FIX / "test.label") == [5, 3, 2, 0]


def test_evaluate_perfect_system():
    gold = load_labels(FIX / "test.label")
    system = [(g >= 3, g / 5) for g in gold]
    res = evaluate(gold, system)
    assert res["PI_F1"] == 1.0
    assert res["n_PI"] == 3          # debatable pair excluded
    assert abs(res["STS_Pearson"] - 1.0) < 1e-9


if __name__ == "__main__":
    test_label_parsing(); test_load(); test_evaluate_perfect_system()
    print("all smoke tests passed")

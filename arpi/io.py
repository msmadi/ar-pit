"""Reading the SemEval-2015 PIT style files used by this dataset."""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

FIELDS = ["topic_id", "topic_name", "sent_1", "sent_2", "label", "sent_1_tag", "sent_2_tag"]

PARAPHRASE, NON_PARAPHRASE, DEBATABLE = "paraphrase", "non-paraphrase", "debatable"

_VOTES = re.compile(r"^\(\s*(\d)\s*,\s*(\d)\s*\)$")


def parse_label(raw: str) -> Optional[int]:
    """Return the 0-5 score for a label in vote form "(a, b)" or score form "k".

    In vote form the number of positive votes ``a`` (out of five) is the score.
    Returns None for an empty or unrecognised label.
    """
    raw = raw.strip()
    if not raw:
        return None
    m = _VOTES.match(raw)
    if m:
        return int(m.group(1))
    if raw.isdigit() and 0 <= int(raw) <= 5:
        return int(raw)
    return None


def score_to_pi(score: Optional[int]) -> Optional[str]:
    """Map a 0-5 score to the binary PI class (3-5 / 2 / 0-1)."""
    if score is None:
        return None
    if score >= 3:
        return PARAPHRASE
    if score == 2:
        return DEBATABLE
    return NON_PARAPHRASE


@dataclass
class Pair:
    topic_id: str
    topic_name: str
    sent_1: str
    sent_2: str
    label: str = ""
    sent_1_tag: str = ""
    sent_2_tag: str = ""

    @property
    def score(self) -> Optional[int]:
        return parse_label(self.label)

    @property
    def pi_label(self) -> Optional[str]:
        return score_to_pi(self.score)


def load_pairs(path: str | Path) -> List[Pair]:
    """Load a ``.data`` file (UTF-8, tab-separated, no header)."""
    pairs = []
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.rstrip("\n\r")
            if not line.strip():
                continue
            cols = line.split("\t")
            if len(cols) < 4:
                raise ValueError(f"{path}:{n}: expected 7 tab-separated fields, got {len(cols)}")
            cols += [""] * (len(FIELDS) - len(cols))
            pairs.append(Pair(*cols[: len(FIELDS)]))
    return pairs


def load_labels(path: str | Path) -> List[Optional[int]]:
    """Load gold 0-5 scores from a ``.label`` file.

    Accepts lines that hold only the label, or SemEval-style lines whose first
    or fifth tab-separated field is the label.
    """
    scores = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            cols = line.rstrip("\n\r").split("\t")
            candidates = [cols[0]] + ([cols[4]] if len(cols) >= 5 else []) + cols[1:]
            score = next((s for s in map(parse_label, candidates) if s is not None), None)
            scores.append(score)
    return scores

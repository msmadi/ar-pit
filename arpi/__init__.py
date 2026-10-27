"""Utilities for the Arabic News Tweets PI & STS dataset (AR-PIT)."""
from .io import Pair, load_pairs, load_labels, parse_label, score_to_pi

__all__ = ["Pair", "load_pairs", "load_labels", "parse_label", "score_to_pi"]
__version__ = "1.0.0"

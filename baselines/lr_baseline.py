"""Logistic regression with n-gram overlap features (Das & Smith, 2009),
adapted to Arabic as in AL-Smadi et al. (2017):
  * NLTK wordpunct_tokenize instead of word_tokenize
  * NLTK ISRI Arabic root stemmer instead of Porter

Features: precision, recall and F1 of 1-3 gram overlap on surface tokens and on
stemmed tokens (18 features). Debatable training pairs are dropped.

Usage: python -m baselines.lr_baseline data/train.data data/test.data > lr.output
"""
import argparse
from collections import Counter

from sklearn.linear_model import LogisticRegression

from arpi import load_pairs
from arpi.io import DEBATABLE, PARAPHRASE
from arpi.text import stem, tokenize


def ngrams(tokens, n):
    return Counter(tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1))


def overlap_features(t1, t2):
    feats = []
    for n in (1, 2, 3):
        a, b = ngrams(t1, n), ngrams(t2, n)
        common = sum((a & b).values())
        p = common / sum(a.values()) if a else 0.0
        r = common / sum(b.values()) if b else 0.0
        f = 2 * p * r / (p + r) if p + r else 0.0
        feats += [p, r, f]
    return feats


def featurize(pair):
    t1, t2 = tokenize(pair.sent_1), tokenize(pair.sent_2)
    return overlap_features(t1, t2) + overlap_features(stem(t1), stem(t2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("train")
    ap.add_argument("test")
    args = ap.parse_args()

    train = [p for p in load_pairs(args.train) if p.pi_label not in (None, DEBATABLE)]
    X = [featurize(p) for p in train]
    y = [int(p.pi_label == PARAPHRASE) for p in train]
    clf = LogisticRegression(max_iter=1000).fit(X, y)

    test = load_pairs(args.test)
    for prob in clf.predict_proba([featurize(p) for p in test])[:, 1]:
        print(f"{'true' if prob >= 0.5 else 'false'}\t{prob:.4f}")


if __name__ == "__main__":
    main()

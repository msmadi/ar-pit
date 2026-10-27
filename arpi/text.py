"""Light Arabic preprocessing that mirrors the paper's pipeline (NLTK-based)."""
import re

from nltk.stem.isri import ISRIStemmer
from nltk.tokenize import wordpunct_tokenize

_DIACRITICS = re.compile(r"[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED\u0640]")  # incl. tatweel
_URL = re.compile(r"https?://\S+|www\.\S+")
_SOURCE_TAGS = re.compile(r"#?(العربية_عاجل|الجزيرة_عاجل)|^\s*عاجل\s*\|")
_STEMMER = ISRIStemmer()


def normalize(text: str) -> str:
    text = _URL.sub(" ", text)
    text = _SOURCE_TAGS.sub(" ", text)
    text = _DIACRITICS.sub("", text)
    text = re.sub("[إأآ]", "ا", text)
    text = text.replace("#", " ").replace("_", " ")
    text = re.sub(r"[^\u0600-\u06FF0-9\s]", " ", text)  # drop non-Arabic letters and punctuation
    return re.sub(r"\s+", " ", text).strip()


def tokenize(text: str):
    return wordpunct_tokenize(normalize(text))


def stem(tokens):
    return [_STEMMER.stem(t) for t in tokens]

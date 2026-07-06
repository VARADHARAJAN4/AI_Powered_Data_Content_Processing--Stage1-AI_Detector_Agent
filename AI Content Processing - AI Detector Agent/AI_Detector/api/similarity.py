import re
from difflib import SequenceMatcher


def semantic_similarity(text_a: str, text_b: str) -> float:
    a = re.sub(r"\s+", " ", text_a).strip().lower()
    b = re.sub(r"\s+", " ", text_b).strip().lower()
    if not a or not b:
        return 0.0
    return round(SequenceMatcher(None, a, b).ratio() * 100, 1)

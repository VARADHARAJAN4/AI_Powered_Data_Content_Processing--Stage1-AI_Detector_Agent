import re


def grammar_score(original: str, rewritten: str) -> float:
    original_words = len(re.findall(r"\b\w+\b", original))
    rewritten_words = len(re.findall(r"\b\w+\b", rewritten))
    if not rewritten_words:
        return 0.0
    punctuation = rewritten.count(".") + rewritten.count("!") + rewritten.count("?")
    score = min(100.0, 85.0 + (punctuation * 2.0) + ((original_words - rewritten_words) * 0.01))
    return round(max(0.0, score), 1)

import re


def calculate_readability(text: str) -> float:
    words = re.findall(r"\b\w+\b", text)
    sentences = re.split(r"(?<=[.!?])\s+", text)
    if not words or not sentences:
        return 0.0
    words_per_sentence = len(words) / max(1, len(sentences))
    syllables = sum(max(1, len(re.findall(r"[aeiouy]+", w.lower()))) for w in words)
    grade = 0.39 * (len(words) / max(1, len(sentences))) + 11.8 * (syllables / max(1, len(words))) - 15.59
    return round(max(1.0, grade), 1)

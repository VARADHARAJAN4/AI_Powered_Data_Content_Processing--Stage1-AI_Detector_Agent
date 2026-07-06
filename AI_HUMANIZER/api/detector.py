import math
import re


def estimate_ai_likeness(text: str) -> float:
    cleaned = re.sub(r"\s+", " ", text).strip()
    if not cleaned:
        return 0.0

    sentences = re.split(r"(?<=[.!?])\s+", cleaned)
    sentence_count = max(1, len(sentences))
    avg_sentence_len = sum(len(s.split()) for s in sentences) / sentence_count
    punctuation_ratio = sum(1 for ch in cleaned if ch in ".,;:") / max(1, len(cleaned))
    repetition_penalty = 0.0
    words = re.findall(r"\b\w+\b", cleaned.lower())
    if words:
        unique_ratio = len(set(words)) / len(words)
        repetition_penalty = max(0.0, 0.5 - unique_ratio)

    score = 40 + min(45, int(avg_sentence_len * 2.2)) + int(punctuation_ratio * 100) + int(repetition_penalty * 100)
    return round(min(100, score), 1)

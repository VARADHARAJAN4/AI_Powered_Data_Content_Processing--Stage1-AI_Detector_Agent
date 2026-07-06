import requests
from config import OLLAMA_URL, OLLAMA_MODEL


def rewrite_text(text: str) -> str:
    prompt = (
        "You are an expert human writing editor. Rewrite the following text so it sounds natural,"
        " fluent, and human-written while preserving meaning and avoiding repetition.\n\n"
        f"Text:\n{text}"
    )
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=20,
        )
        response.raise_for_status()
        data = response.json()
        result = data.get("response", "").strip()
        if result:
            return result
    except Exception:
        pass

    return _fallback_rewrite(text)


def _fallback_rewrite(text: str) -> str:
    sentences = [s.strip() for s in text.split(".") if s.strip()]
    if not sentences:
        return text
    rewritten = []
    for sentence in sentences:
        rewritten.append(sentence.strip() + ".")
    return " ".join(rewritten)

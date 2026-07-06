import logging
import re
from datetime import datetime
from time import perf_counter

from flask import Flask, jsonify, render_template, request, send_from_directory

from config import APP_TITLE, MAX_TEXT_LENGTH, OUTPUT_DIR, LOG_DIR
from api.detector import estimate_ai_likeness
from api.readability import calculate_readability
from api.rewrite import rewrite_text
from api.similarity import semantic_similarity
from evaluation.grammar import grammar_score
from preprocessing.cleaner import clean_text

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["MAX_CONTENT_LENGTH"] = MAX_TEXT_LENGTH * 1024

LOG_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=LOG_DIR / "app.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


@app.get("/")
def index():
    return render_template("index.html", title=APP_TITLE)


def infer_source_details(text: str, ai_score: float):
    lowered = text.lower()
    if ai_score >= 70:
        if any(keyword in lowered for keyword in ["ai model", "gpt", "openai", "chatgpt", "davinci", "claude", "bard"]):
            ai_source = "GPT-like"
        elif any(keyword in lowered for keyword in ["claude", "anthropic", "ai assistant", "assistant"]) :
            ai_source = "Claude-like"
        elif any(keyword in lowered for keyword in ["llama", "meta", "alpaca", "vicuna", "flan"]):
            ai_source = "LLaMA-like"
        else:
            ai_source = "Likely AI-generated"
    else:
        ai_source = "Not clearly AI-generated"

    if any(keyword in lowered for keyword in ["dear", "subject", "regards", "recipient", "meeting", "appointment", "schedule"]):
        source_type = "Email"
    elif any(keyword in lowered for keyword in ["article", "study", "research", "abstract", "introduction", "findings"]):
        source_type = "Article"
    elif any(keyword in lowered for keyword in ["blog", "guide", "tips", "tutorial", "today", "here's"]):
        source_type = "Blog"
    elif any(keyword in lowered for keyword in ["essay", "thesis", "argument", "conclusion", "therefore", "however"]):
        source_type = "Essay"
    else:
        source_type = "General"

    return ai_source, source_type


@app.post("/analyze")
def analyze():
    payload = request.get_json(silent=True) or {}
    text = (payload.get("text") or "").strip()
    start_time = perf_counter()

    if not text:
        return jsonify({"error": "Please enter some text to analyze."}), 400

    cleaned_text = clean_text(text)
    if len(cleaned_text) > MAX_TEXT_LENGTH:
        return jsonify({"error": f"Text must be {MAX_TEXT_LENGTH} characters or fewer."}), 400

    if not cleaned_text:
        return jsonify({"error": "The input text became empty after cleaning."}), 400

    original_score = estimate_ai_likeness(cleaned_text)
    rewritten_text = rewrite_text(cleaned_text)
    rewritten_score = estimate_ai_likeness(rewritten_text)
    similarity_score = semantic_similarity(cleaned_text, rewritten_text)
    readability_grade = calculate_readability(cleaned_text)
    grammar_quality = grammar_score(cleaned_text, rewritten_text)

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    download_name = f"humanized_{timestamp}.txt"
    download_path = OUTPUT_DIR / download_name
    download_path.write_text(rewritten_text, encoding="utf-8")

    ai_source, source_type = infer_source_details(cleaned_text, original_score)
    processing_time_ms = round((perf_counter() - start_time) * 1000, 1)
    logging.info("Analyzed text of length %s", len(cleaned_text))

    return jsonify(
        {
            "original_score": original_score,
            "rewritten_score": rewritten_score,
            "similarity_score": similarity_score,
            "readability_grade": readability_grade,
            "grammar_score": grammar_quality,
            "rewritten_text": rewritten_text,
            "download_url": f"/download/{download_name}",
            "ai_source": ai_source,
            "source_type": source_type,
            "word_count": len(cleaned_text.split()),
            "character_count": len(cleaned_text),
            "processing_time_ms": processing_time_ms,
        }
    )


@app.get("/download/<path:filename>")
def download(filename: str):
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

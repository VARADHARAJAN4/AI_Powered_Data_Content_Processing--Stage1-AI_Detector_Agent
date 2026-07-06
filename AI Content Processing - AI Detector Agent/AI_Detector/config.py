import os
from pathlib import Path

APP_TITLE = "AI Detector Agent"
MAX_TEXT_LENGTH = 1000
PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_ROOT / "downloads"
LOG_DIR = PROJECT_ROOT / "logs"
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")

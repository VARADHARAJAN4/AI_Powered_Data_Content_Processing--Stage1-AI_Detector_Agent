# AI Detector Agent

AI Humanizer Agent is an open-source prototype web application that analyzes a short piece of text, estimates how likely it is to be AI-generated, and visualizations.

This project is designed as a locally runnable toolkit for researchers, writers, and editors who want to explore how text transforms when optimized for a more human style and to view detector-based estimates responsibly.

Key features
- Estimate AI-likeness using a lightweight heuristic detector
- Semantic similarity and readability scoring
- Grammar-quality estimation
- Interactive trend chart with client-side history, stacked/grouped views, and metric toggles
- Export humanized text as a downloadable TXT

Technology stack
- Python 3.12+ (tested with 3.14)
- Flask web server
- Chart.js for interactive visualization
- Local heuristics: readability, perplexity-like heuristics, burstiness-style signals
- Optional: Ollama or other local LLM endpoints for higher-quality rewrites

Repository layout
- `app.py` — Flask app and API endpoints
- `config.py` — project configuration
- `requirements.txt` — minimal Python dependencies
- `api/` — analysis modules (detector, rewrite, similarity, readability)
- `preprocessing/` — text cleaning utilities
- `evaluation/` — grammar/readability helpers
- `static/` — client assets (CSS, JS)
- `templates/` — Jinja2 HTML templates
- `downloads/` — generated outputs

Security & privacy
- This app is intended for local use. If you point the rewrite step at an external LLM service (Ollama or APIs), be mindful that text will be transmitted to that endpoint.
- AI-likeness scores are probabilistic heuristics and should not be treated as definitive proof of authorship.

Quickstart (local)
1. Create and activate a Python environment (recommended).

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

3. Run the app

```powershell
python app.py
```

4. Open the UI in your browser: `http://127.0.0.1:5000`

Optional: enable Ollama or another local LLM
- Set `OLLAMA_URL` and `OLLAMA_MODEL` in the environment or `config.py` to enable higher-quality rewrites via a local LLM endpoint.

Development notes
- The chart stores recent runs in `localStorage` for quick trend analysis. To persist across machines, implement a server-side storage option.
- The detector is intentionally simple and designed to be replaced or augmented with more robust estimators (perplexity models, DetectGPT variants, ensemble methods).

Limitations
- No detector is perfect — false positives and negatives are expected.
- The rewrite fallback is conservative; enabling a local LLM will generally improve rewrite quality but requires model availability.

Contributing
- Suggestions, improvements, and pull requests are welcome. Please open issues describing the problem or feature request.

License
- MIT License (replace with your preferred license if needed)

Acknowledgements
- Built as a practical prototype based on an AI detection / humanization flow document. Uses open-source libraries for visualization and web serving.

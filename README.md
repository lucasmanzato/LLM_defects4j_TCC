# LLM Defects4J Bug Snippet Filter

This project adds a method-level snippet filter over Java repositories, inspired by Defects4J bug themes. It extracts Java methods and ranks potentially bug-prone snippets via heuristics and optionally a Google Gemini LLM.

## Features
- Java method extraction (via `javalang`, with regex fallback)
- Heuristic bug detection: string `==`, off-by-one, empty catch, swallowed exception, resource leaks, equals without null-check
- Optional LLM classification (Google Gemini), merging scores and labels
- JSON output with top-ranked snippets

## Setup
```powershell
python -m pip install -r requirements.txt
```

Optionally, set Google Gemini credentials to enable LLM classification:
```powershell
$env:GEMINI_API_KEY = "AIzaSy..."
# Optional: choose model
$env:GEMINI_MODEL = "gemini-1.5-flash"
```

## Quick Start
Assuming the repo has already been cloned to `dados/commons-lang` by `data_acquisition.py`:
```powershell
python run_filter.py
```
Output will be saved to `dados/bug_snippets.json`.

To run without LLM and heuristics only:
```powershell
$env:USE_LLM = "0"
python run_filter.py
```

To target a different repo path or output file:
```powershell
$env:REPO_PATH = "C:\\path\\to\\java-repo"
$env:OUT_PATH = "C:\\path\\to\\output.json"
python run_filter.py

## Filtering Controls
- `PATTERNS`: Comma-separated labels to keep (e.g., `equals-without-null-check,string-equality-using-==`).
- `STRICT_FILTER`: When `1`, require all `PATTERNS` to be present; otherwise, any overlap.
- `TOP_K`: Limit number of results (default 50).

Examples:
```powershell
$env:PATTERNS = "equals-without-null-check,string-equality-using-=="
$env:STRICT_FILTER = "0"
$env:TOP_K = "30"
python run_filter.py
```
```

## Getting a Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikeys)
2. Create a new API key (free tier available)
3. Set the environment variable as shown above
4. Gemini is free for experimentation; higher usage may require billing

## Notes
- LLM usage is optional and wrapped with fallback; if API calls fail, only heuristics are used.
- Heuristics aim to reflect common patterns seen across Defects4J projects, but they are approximations; LLM can improve precision.
- Google Gemini offers a free tier, making this approach accessible without immediate billing.

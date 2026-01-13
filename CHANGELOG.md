# Changelog

## v0.1.0 — 2026-01-12

### Added
- Heuristic bug detection pipeline with 6 patterns:
  - `string-equality-using-==`, `equals-without-null-check`, `off-by-one-length`, `empty-catch`, `swallowed-exception`, `resource-not-closed`.
- LLM integration via Google Gemini (google-genai SDK) with graceful fallback to heuristics when quota is exhausted.
- Filtering controls via environment: `PATTERNS`, `STRICT_FILTER`, `TOP_K`, `USE_LLM`.
- JSON output (`dados/bug_snippets.json`) with metadata and heuristic fix suggestions.
- CSV export utility (`LLM_defects4j_TCC/export_csv.py`) → `dados/bug_snippets.csv`.
- Data acquisition script (`LLM_defects4j_TCC/data_acquisition.py`) using GitPython for cloning and validation.
- Documentation: `README.md`, `RELATORIO.txt` (pipeline details), `TROUBLESHOOTING.txt` (Gemini quota & setup).

### Changed
- Migrated LLM SDK from deprecated `google-generativeai` to `google-genai` (0.2.0+).

### Known Issues
- Gemini API free tier quota exhausted (429 RESOURCE_EXHAUSTED). LLM fields (`llm`, `llm_fix`) remain null until quota renews or billing is enabled.

### How to Run
1. Install deps: `pip install -r LLM_defects4j_TCC/requirements.txt`
2. Clone & count: `python LLM_defects4j_TCC/data_acquisition.py`
3. Run filter (heuristics): `python LLM_defects4j_TCC/run_filter.py`
4. Optional filters (PowerShell):
   - `$env:PATTERNS = "equals-without-null-check,string-equality-using-=="`
   - `$env:STRICT_FILTER = "0"`; `$env:TOP_K = "20"`
5. Export CSV: `python LLM_defects4j_TCC/export_csv.py`

# Nyaya Saathi: AI legal first-aid for India (Kuku assignment, Problem 2)

Conversational helper for six everyday problems: security deposit, consumer refund, unpaid salary, bounced cheque, online/UPI fraud, legal notice received.
It builds the case file, explains where you stand, lists proof to gather, drafts a notice, and prepares a role-play prompt. It refers out-of-scope and risky matters to a real lawyer / NALSA 15100.

## Run (2 minutes, free)
```
pip install -r requirements.txt
python run_tests.py            # offline mode, no key needed -> writes outputs/ (43 cases + 25 guard probes; date pinned via NYAYA_TODAY)
streamlit run app.py           # chat UI
```
LLM mode (swappable by env vars, nothing else changes):
```
export LLM_PROVIDER=gemini  LLM_API_KEY=...  LLM_MODEL=gemini-2.5-flash     # free tier
export LLM_PROVIDER=anthropic LLM_API_KEY=... LLM_MODEL=claude-sonnet-5-5
export LLM_PROVIDER=openai  LLM_API_KEY=... LLM_BASE_URL=https://api.groq.com/openai/v1 LLM_MODEL=llama-3.3-70b-versatile
python run_tests.py            # same 20 cases through the LLM; outputs/ is overwritten, copy the folder first
```
## Files
- `core.py`  triage, red flags, facts, retrieval, **citation guard**, notice templates (no LLM, fully testable)
- `llm.py`   provider layer + grounded prompt + case-file extraction; falls back to offline on any error
- `data/kb.json`  18 source-tagged legal snippets; entries with a `verify` note must be re-checked against the official text
- `tests/cases.json`, `run_tests.py`, `outputs/`  20 cases, unedited outputs, guard probes

- `tests/guard_cases.json`  24 adversarial/legitimate sentences for the citation guard
- `AUDIT.md`  what an independent audit found wrong in v1 and what changed
- `make_doc.py`  regenerates `solution_doc.pdf` (fill the [PLACEHOLDERS])

"""Provider-agnostic LLM layer. Swap models by changing env vars only:
  LLM_PROVIDER = anthropic | gemini | openai | mock | offline
  LLM_MODEL, LLM_API_KEY, LLM_BASE_URL (openai-compatible: Groq, OpenRouter, Together, local Ollama ...)
Plain `requests` only, so nothing breaks when a provider SDK changes."""
import json, os, re
import requests
import core

DEFAULTS = {"anthropic": "claude-sonnet-5-5", "gemini": "gemini-2.5-flash", "openai": "llama-3.3-70b-versatile"}
BASES = {"openai": "https://api.groq.com/openai/v1"}


def provider():
    return os.getenv("LLM_PROVIDER", "offline").lower()


def call_llm(system, user, max_tokens=1500, temperature=0.2):
    p, key = provider(), os.getenv("LLM_API_KEY", "")
    model = os.getenv("LLM_MODEL", DEFAULTS.get(p, ""))
    if p == "mock":
        return os.getenv("MOCK_REPLY", "")
    if p == "anthropic":
        r = requests.post("https://api.anthropic.com/v1/messages", timeout=60,
                          headers={"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
                          json={"model": model, "max_tokens": max_tokens, "temperature": temperature, "system": system,
                                "messages": [{"role": "user", "content": user}]})
        r.raise_for_status()
        return "".join(b.get("text", "") for b in r.json()["content"])
    if p == "gemini":
        r = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}", timeout=60,
                          json={"systemInstruction": {"parts": [{"text": system}]},
                                "contents": [{"role": "user", "parts": [{"text": user}]}],
                                "generationConfig": {"temperature": temperature, "maxOutputTokens": max_tokens}})
        r.raise_for_status()
        return "".join(x.get("text", "") for x in r.json()["candidates"][0]["content"]["parts"])
    if p == "openai":
        base = os.getenv("LLM_BASE_URL", BASES["openai"]).rstrip("/")
        r = requests.post(f"{base}/chat/completions", timeout=60, headers={"Authorization": f"Bearer {key}"},
                          json={"model": model, "max_tokens": max_tokens, "temperature": temperature,
                                "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]})
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    raise RuntimeError("no LLM provider configured")


SYSTEM = """You are Nyaya Saathi, a careful legal-information assistant for ordinary people in India. You are NOT a lawyer.
HARD RULES:
1. Use ONLY the facts in CONTEXT (verified legal snippets, each tagged [ID]). Cite the tag after every legal statement, e.g. [RENT-DEPOSIT].
2. NEVER name any Act, Section, rule, court case or judgment that is not written in CONTEXT. If the user needs law that is not in CONTEXT, say "I don't have verified information on that; please ask a lawyer or your District Legal Services Authority (NALSA 15100)".
3. Never predict that the user will win, and never promise outcomes, amounts or timelines beyond CONTEXT.
4. Reply in the user's language ({lang}); keep sentences short and plain. Keep numbers, helpline numbers and law names exactly as in CONTEXT.
5. Structure: What I understood / Where you stand / What to do next (numbered) / Proof to gather / Questions for you (max 3) / When you need a real lawyer.
6. If WARNINGS or FLAGS are present, state them first, plainly. If the matter is out of scope, say so and refer; do not guess.
7. End with one line: you are an AI, not a lawyer; verify before acting."""

CASE_SYSTEM = """Extract a case file from the user's messages. Return ONLY JSON with keys:
summary (one sentence), parties (list), timeline (list of {date_or_text, event}), amount_rs (number or null),
proof_have (list), proof_missing (list), missing_info (list of max 3 questions). Use only what the user said; use null/[] if unknown. Do not add any law."""


def build_prompt(text, a):
    ctx = "\n".join(f"[{i}] {core.KB_BY_ID[i]['text']} (source: {core.KB_BY_ID[i]['source']})" for i in a["kb_ids"])
    cat = core.CATEGORIES.get(a["category"], {})
    hints = f"\nSTEPS TO ADAPT: {cat.get('steps')}\nPROOF LIST: {cat.get('proof')}" if cat else ""
    return (f"CONTEXT:\n{ctx}{hints}\n\nFLAGS: {[m for _, m in a['flags']]}\nWARNINGS: {a['warnings']}\n"
            f"CATEGORY: {a['category']}  OUT_OF_SCOPE_TERMS: {a['out_of_scope']}\nCLARIFYING QUESTIONS TO ASK: {a['questions']}\n\nUSER MESSAGES:\n{text}")


def extract_case(text):
    try:
        raw = call_llm(CASE_SYSTEM, text, max_tokens=700, temperature=0)
        return json.loads(re.search(r"\{.*\}", raw, re.S).group(0))
    except Exception:
        f = core.extract_facts(text)
        return {"summary": text[:160], "amount_rs": f["amount_rs"], "timeline": [], "proof_have": [], "proof_missing": [], "missing_info": core.analyse(text)["questions"]}


def respond(text, lang=None):
    """Deterministic triage -> verified retrieval -> LLM phrasing -> guard. Falls back to offline on any failure."""
    a = core.analyse(text, lang)
    if provider() == "offline" or a["category"] in (None, "out_of_scope") or any(f[0] in ("self_harm",) for f in a["flags"]):
        return core.respond_offline(text, lang)   # sensitive / out-of-scope paths never go through free generation
    try:
        raw = call_llm(SYSTEM.format(lang={"hi": "Hindi (Devanagari)", "hinglish": "Hinglish (Roman script)", "en": "English"}[a["lang"]]), build_prompt(text, a))
        clean, removed = core.guard(raw, a["kb_ids"], core.trusted_text(text, a))
        notice = core.build_notice(a["category"], a["facts"]) if not a["flags"] else None
        return dict(analysis=a, answer=clean, removed=removed, notice=notice, case=extract_case(text), mode=f"llm:{provider()}")
    except Exception as e:
        r = core.respond_offline(text, lang)
        r["mode"] = f"offline (fallback: {type(e).__name__})"
        return r

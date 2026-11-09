"""Runs every test case and writes unedited outputs to outputs/. Usage: python run_tests.py   (set LLM_PROVIDER/LLM_API_KEY to also run LLM mode)"""
import json, os, re, sys, datetime
from pathlib import Path
import core, llm

os.environ.setdefault("NYAYA_TODAY", "2026-11-08")   # reproducible deadline maths
OUT = Path(__file__).parent / "outputs"; OUT.mkdir(exist_ok=True)
cases = json.loads((Path(__file__).parent / "tests" / "cases.json").read_text(encoding="utf-8"))

def check(case, r):
    text = case["text"]
    e, a, res = case["expect"], r["analysis"], []
    def add(name, ok, detail=""): res.append({"check": name, "pass": bool(ok), "detail": detail})
    if "category" in e: add("category", a["category"] == e["category"], f"got {a['category']}")
    if "lang" in e: add("language", a["lang"] == e["lang"], f"got {a['lang']}")
    if "escalate" in e: add("escalate", a["escalate"] == e["escalate"], f"got {a['escalate']}")
    if "amount" in e: add("amount", a["facts"]["amount_rs"] == e["amount"], f"got {a['facts']['amount_rs']}")
    for k in e.get("kb_has", []): add(f"retrieved {k}", k in a["kb_ids"])
    for k in e.get("flags_has", []): add(f"flag {k}", k in [f[0] for f in a["flags"]])
    if "notice" in e: add("notice drafted" if e["notice"] else "no notice drafted", bool(r["notice"]) == e["notice"])
    if "warn_has" in e: add("warning " + e["warn_has"], any(e["warn_has"] in w for w in a["warnings"]))
    for s in e.get("answer_has", []): add(f"answer mentions '{s}'", s.lower() in r["answer"].lower())
    for rx in e.get("answer_not", []): add(f"answer lacks /{rx}/", not re.search(rx, r["answer"]))
    add("no unsupported citation survived", True if not core.guard(r["answer"], a["kb_ids"], core.trusted_text(text, a))[1] else False)
    return res

def main():
    rows, mode_name = [], None
    for c in cases:
        r = llm.respond(c["text"]); mode_name = r["mode"]
        res = check(c, r); ok = all(x["pass"] for x in res)
        rows.append((c["id"], ok, res))
        md = [f"# {c['id']}", f"**Mode:** {r['mode']}  |  **Run:** {datetime.datetime.now():%Y-%m-%d %H:%M}", "", "## Input", c["text"], "",
              "## Analysis (deterministic layer)", "```json", json.dumps({k: v for k, v in r["analysis"].items()}, ensure_ascii=False, indent=1, default=str), "```", "",
              "## Answer shown to user", r["answer"], ""]
        if r["removed"]: md += ["## Sentences removed by citation guard", "```json", json.dumps(r["removed"], ensure_ascii=False, indent=1), "```", ""]
        if r.get("notice"): md += ["## Draft notice", "```", r["notice"], "```", ""]
        md += ["## Checks"] + [f"- {'PASS' if x['pass'] else 'FAIL'}: {x['check']} {x['detail']}" for x in res]
        (OUT / f"{c['id']}.md").write_text("\n".join(md), encoding="utf-8")
    # guard suite: adversarial and legitimate sentences injected as if an LLM wrote them (tests/guard_cases.json)
    g = []
    for gc in json.loads((Path(__file__).parent / "tests" / "guard_cases.json").read_text(encoding="utf-8")):
        clean, removed = core.guard(gc["text"], gc["ids"])
        g.append({"probe": gc["name"], "ids": gc["ids"], "input": gc["text"], "kept": clean, "removed": [r["unsupported"] for r in removed],
                  "expected": "removed" if gc["should_be_caught"] else "kept", "pass": bool(removed) == gc["should_be_caught"]})
    # end-to-end with a simulated hallucinating model
    os.environ["LLM_PROVIDER"] = "mock"; os.environ["MOCK_REPLY"] = "Your landlord must pay under Section 420 IPC and the Supreme Court case Rao v. State (2018). A legal notice with a 15-day deadline is the usual first step [RENT-REMEDY]."
    m = llm.respond("My landlord is not returning my security deposit of Rs 20,000"); 
    g.append({"probe": "mock LLM end-to-end", "kept": m["answer"], "removed": len(m["removed"]), "expected": "removed", "pass": len(m["removed"]) == 1 and "420" not in m["answer"]})
    (OUT / "guard_tests.json").write_text(json.dumps(g, ensure_ascii=False, indent=1), encoding="utf-8")
    passed = sum(ok for _, ok, _ in rows)
    lines = [f"# Test summary ({mode_name})", "", f"Cases fully passing: **{passed}/{len(rows)}**", "", "| case | result | failed checks |", "|---|---|---|"]
    for i, ok, res in rows: lines.append(f"| {i} | {'PASS' if ok else 'FAIL'} | {'; '.join(x['check']+' '+x['detail'] for x in res if not x['pass'])} |")
    lines += ["", f"Guard probes passing: **{sum(x['pass'] for x in g)}/{len(g)}** (see guard_tests.json)"]
    (OUT / "SUMMARY.md").write_text("\n".join(lines), encoding="utf-8"); print("\n".join(lines))

if __name__ == "__main__": main()

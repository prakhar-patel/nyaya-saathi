# 30_tax_notice
**Mode:** offline  |  **Run:** 2026-11-08 12:51

## Input
I got a notice from income tax department

## Analysis (deterministic layer)
```json
{
 "lang": "en",
 "category": "out_of_scope",
 "flags": [],
 "out_of_scope": [
  "income tax"
 ],
 "scores": {
  "notice_received": 4
 },
 "facts": {
  "amount_rs": null,
  "years_ago": null,
  "memo_age_days": null
 },
 "kb_ids": [
  "LEGAL-AID"
 ],
 "warnings": [],
 "escalate": true,
 "questions": []
}
```

## Answer shown to user
This looks like a matter outside what I can safely handle (e.g. family, criminal, inheritance, tax, insurance, job termination or immigration law). I would only be guessing, and mistakes here can cost you a lot.

**When you need a real lawyer:** now. Free option: Free legal aid is available under the Legal Services Authorities Act, 1987 to eligible groups, including women, children, SC/ST members, persons in custody and people below an income limit set by the state. Call NALSA on 15100 or visit the District Legal Services Authority (DLSA) at the district court.
_I am an AI, not a lawyer. This is general information, not legal advice. Verify before acting._

## Checks
- PASS: category got out_of_scope
- PASS: escalate got True
- PASS: no unsupported citation survived 
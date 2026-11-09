# 38_heldout_criminal_threat_in_notice
**Mode:** offline  |  **Run:** 2026-11-08 12:51

## Input
They sent me a notice saying pay Rs 3 lakh or face a criminal case

## Analysis (deterministic layer)
```json
{
 "lang": "en",
 "category": "notice_received",
 "flags": [
  [
   "case_against",
   "A case, complaint or court date against you is involved or has been threatened. Please see a lawyer before replying to anything."
  ]
 ],
 "out_of_scope": [],
 "scores": {
  "notice_received": 2
 },
 "facts": {
  "amount_rs": 300000,
  "years_ago": null,
  "memo_age_days": null
 },
 "kb_ids": [
  "LEGAL-NOTICE-RECEIVED",
  "LIMITATION-GEN",
  "LEGAL-AID"
 ],
 "warnings": [],
 "escalate": true,
 "questions": [
  "Is what they say right, wrong, or partly right?"
 ]
}
```

## Answer shown to user
**⚠️ A case, complaint or court date against you is involved or has been threatened. Please see a lawyer before replying to anything.**

**What I understood:** You received a legal notice; amount mentioned: Rs 300,000

**Where you stand:**
- If you receive a legal notice: do not ignore it. Note the date received and any deadline, read exactly what is claimed, keep the envelope or email, and reply in writing with your side of the facts before the deadline. A court summons is different from a notice; it carries a hearing date and should be shown to a lawyer immediately. [LEGAL-NOTICE-RECEIVED]
- Under the Limitation Act, 1963, the general period to sue for recovery of money or on a contract is three years. A claim filed after the limitation period can be dismissed, so old claims need urgent attention. [LIMITATION-GEN]

**What to do next:**
1. Note today's date, the deadline in the notice and who sent it.
2. Do not ignore it; do not sign or pay in panic.
3. Reply in writing before the deadline, sticking to facts (a lawyer should review the reply).
4. If it is a court summons with a hearing date, see a lawyer immediately.

**Proof to gather:**
- The notice itself (all pages, envelope/email)
- Date and mode of receipt
- Any agreement, payment proof or messages relevant to what is claimed

**When you need a real lawyer:** see one if the other side hires a lawyer, a court summons arrives, the amount is large, or you are unsure about forum or deadlines. Free help: NALSA 15100 / your District Legal Services Authority [LEGAL-AID].

**To help you better, tell me:**
- Is what they say right, wrong, or partly right?

_I am an AI, not a lawyer. This is general information, not legal advice. Verify before acting._

## Checks
- PASS: category got notice_received
- PASS: escalate got True
- PASS: flag case_against 
- PASS: no unsupported citation survived 
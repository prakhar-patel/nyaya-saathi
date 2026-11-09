# 17_eviction
**Mode:** offline  |  **Run:** 2026-11-08 12:51

## Input
My landlord is evicting me without notice, what can I do?

## Analysis (deterministic layer)
```json
{
 "lang": "en",
 "category": "rent_deposit",
 "flags": [
  [
   "eviction",
   "Eviction rules are state-specific and time-sensitive, and the deposit guidance I give does not cover them. Speak to a lawyer or your DLSA before you move out or sign anything."
  ]
 ],
 "out_of_scope": [],
 "scores": {
  "rent_deposit": 1
 },
 "facts": {
  "amount_rs": null,
  "years_ago": null,
  "memo_age_days": null
 },
 "kb_ids": [
  "RENT-DEPOSIT",
  "RENT-REMEDY",
  "LIMITATION-GEN",
  "LEGAL-AID"
 ],
 "warnings": [],
 "escalate": true,
 "questions": [
  "How much was the deposit, and how did you pay it (bank/UPI/cash)?",
  "Do you have a written rent agreement or any receipt?",
  "Which city/state is the property in? (Rent rules differ by state.)"
 ]
}
```

## Answer shown to user
**⚠️ Eviction rules are state-specific and time-sensitive, and the deposit guidance I give does not cover them. Speak to a lawyer or your DLSA before you move out or sign anything.**

**What I understood:** Security deposit / rent dispute

**Where you stand:**
- There is no single central law fixing deposit rules; they depend mainly on the rent agreement and the rent law of your state. The Model Tenancy Act, 2021 (a model law that applies only in states that have adopted it) caps a residential security deposit at two months' rent and expects it to be returned when the tenant hands back possession, less genuine dues or damage beyond normal wear and tear. Check whether your state has adopted it. [RENT-DEPOSIT]
- The usual steps for an unreturned deposit are: (1) ask in writing, (2) send a legal notice giving a deadline (15 days is customary), (3) if unpaid, file a civil suit for recovery of money; where the claim rests on a written agreement, a summary suit under Order XXXVII of the Code of Civil Procedure, 1908 may be available. A consumer commission is generally not the right forum for a landlord-tenant deposit dispute. A local lawyer should confirm the forum before filing. [RENT-REMEDY]
- Under the Limitation Act, 1963, the general period to sue for recovery of money or on a contract is three years. A claim filed after the limitation period can be dismissed, so old claims need urgent attention. [LIMITATION-GEN]

**What to do next:**
1. Send a polite but firm written demand (WhatsApp/email) asking for the refund by a date; keep the screenshot.
2. If ignored, send a legal notice with a 15-day deadline (a draft is generated below; have a lawyer or the DLSA check it).
3. If still unpaid, a civil recovery suit is the usual route; a local lawyer should confirm the forum for your state.
4. Check whether your state has adopted the Model Tenancy Act, 2021 and what your agreement says about deductions.

**Proof to gather:**
- Rent agreement (even unregistered/ on stamp paper)
- Proof you paid the deposit (bank/UPI statement, receipt)
- Proof you vacated and handed over keys (messages, handover photos, move-out date)
- Messages/emails where you asked for the deposit and the landlord's replies or excuses
- Photos/video of the flat's condition at move-out

**When you need a real lawyer:** see one if the other side hires a lawyer, a court summons arrives, the amount is large, or you are unsure about forum or deadlines. Free help: NALSA 15100 / your District Legal Services Authority [LEGAL-AID].

**To help you better, tell me:**
- How much was the deposit, and how did you pay it (bank/UPI/cash)?
- Do you have a written rent agreement or any receipt?
- Which city/state is the property in? (Rent rules differ by state.)

_I am an AI, not a lawyer. This is general information, not legal advice. Verify before acting._

## Checks
- PASS: language got en
- PASS: escalate got True
- PASS: flag eviction 
- PASS: no notice drafted 
- PASS: no unsupported citation survived 
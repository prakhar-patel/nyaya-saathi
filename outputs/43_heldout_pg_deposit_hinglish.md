# 43_heldout_pg_deposit_hinglish
**Mode:** offline  |  **Run:** 2026-11-08 12:51

## Input
Sir mera pg wale ne 20000 advance nahi lautaya, 3 mahine ho gaye

## Analysis (deterministic layer)
```json
{
 "lang": "hinglish",
 "category": "rent_deposit",
 "flags": [],
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
 "escalate": false,
 "questions": [
  "Do you have a written rent agreement or any receipt?",
  "Which city/state is the property in? (Rent rules differ by state.)",
  "When did you vacate and hand over the keys?"
 ]
}
```

## Answer shown to user
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
- Do you have a written rent agreement or any receipt?
- Which city/state is the property in? (Rent rules differ by state.)
- When did you vacate and hand over the keys?

_I am an AI, not a lawyer. This is general information, not legal advice. Verify before acting._

## Draft notice
```
DRAFT LEGAL NOTICE: NOT REVIEWED BY A LAWYER. Fill every [BRACKET]; get it checked by an advocate or the DLSA before sending (by registered post AD + email).

Date: [DATE]
To: [OTHER PARTY NAME], [ADDRESS]
From: [YOUR NAME], [YOUR ADDRESS], [PHONE]
Subject: Demand for refund of security deposit of Rs [AMOUNT]

1. I was your tenant at [PROPERTY ADDRESS] under [a rent agreement dated DATE / an oral arrangement].
2. I paid you a refundable security deposit of Rs [AMOUNT] on [DATE] by [MODE OF PAYMENT].
3. I vacated and handed over possession to you on [DATE].
4. Despite my requests on [DATES AND MODES], you have not refunded the deposit [and have given no valid reason / have claimed deductions of Rs ___ which are unjustified because ___].
5. You are called upon to pay Rs [AMOUNT] within 15 days of receiving this notice. Failing this, I will be compelled to take legal proceedings for recovery, with interest as permissible by law and costs, entirely at your risk.

Yours faithfully,
[YOUR NAME]
[SIGNATURE]

Enclosures: [copies of the proof listed above]
```

## Checks
- PASS: category got rent_deposit
- PASS: no unsupported citation survived 
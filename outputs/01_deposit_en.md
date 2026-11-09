# 01_deposit_en
**Mode:** offline  |  **Run:** 2026-11-08 12:51

## Input
My landlord in Pune is not returning my security deposit of Rs 60,000. I vacated on 1 September, I have a rent agreement and paid by bank transfer. He keeps saying he will pay next week.

## Analysis (deterministic layer)
```json
{
 "lang": "en",
 "category": "rent_deposit",
 "flags": [],
 "out_of_scope": [],
 "scores": {
  "rent_deposit": 8
 },
 "facts": {
  "amount_rs": 60000,
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
 "questions": []
}
```

## Answer shown to user
**What I understood:** Security deposit / rent dispute; amount mentioned: Rs 60,000

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

_I am an AI, not a lawyer. This is general information, not legal advice. Verify before acting._

## Draft notice
```
DRAFT LEGAL NOTICE: NOT REVIEWED BY A LAWYER. Fill every [BRACKET]; get it checked by an advocate or the DLSA before sending (by registered post AD + email).

Date: [DATE]
To: [OTHER PARTY NAME], [ADDRESS]
From: [YOUR NAME], [YOUR ADDRESS], [PHONE]
Subject: Demand for refund of security deposit of Rs 60,000

1. I was your tenant at [PROPERTY ADDRESS] under [a rent agreement dated DATE / an oral arrangement].
2. I paid you a refundable security deposit of Rs 60,000 on [DATE] by [MODE OF PAYMENT].
3. I vacated and handed over possession to you on [DATE].
4. Despite my requests on [DATES AND MODES], you have not refunded the deposit [and have given no valid reason / have claimed deductions of Rs ___ which are unjustified because ___].
5. You are called upon to pay Rs 60,000 within 15 days of receiving this notice. Failing this, I will be compelled to take legal proceedings for recovery, with interest as permissible by law and costs, entirely at your risk.

Yours faithfully,
[YOUR NAME]
[SIGNATURE]

Enclosures: [copies of the proof listed above]
```

## Checks
- PASS: category got rent_deposit
- PASS: language got en
- PASS: escalate got False
- PASS: amount got 60000
- PASS: retrieved RENT-DEPOSIT 
- PASS: retrieved RENT-REMEDY 
- PASS: notice drafted 
- PASS: no unsupported citation survived 
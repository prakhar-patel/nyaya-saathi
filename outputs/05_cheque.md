# 05_cheque
**Mode:** offline  |  **Run:** 2026-11-08 12:51

## Input
A friend gave me a cheque for Rs 2 lakh which bounced. The bank return memo is dated 10 October 2026. I have not sent any notice yet.

## Analysis (deterministic layer)
```json
{
 "lang": "en",
 "category": "cheque_bounce",
 "flags": [],
 "out_of_scope": [],
 "scores": {
  "consumer_refund": 1,
  "cheque_bounce": 5
 },
 "facts": {
  "amount_rs": 200000,
  "years_ago": null,
  "memo_age_days": 29
 },
 "kb_ids": [
  "NI-138",
  "LEGAL-AID"
 ],
 "warnings": [
  "URGENT DEADLINE: about 1 day(s) are left (to about 09 Nov 2026, counting from the day you received the memo) to send the demand notice. Have a lawyer send it now."
 ],
 "escalate": true,
 "questions": []
}
```

## Answer shown to user
**What I understood:** Dishonoured (bounced) cheque; amount mentioned: Rs 200,000

**Where you stand:**
- Section 138 of the Negotiable Instruments Act, 1881 (cheque dishonour) has strict deadlines: (1) send a written demand notice within 30 days of receiving the bank's cheque-return memo; (2) the person who issued the cheque gets 15 days from receiving the notice to pay; (3) if they do not pay, the complaint must be filed before a Magistrate within one month after that 15-day period ends. Missing a deadline can end the case. This is a criminal complaint; use a lawyer. [NI-138]

**What to do next:**
1. Find the date you received the bank's return memo. The 30-day clock to send the demand notice starts then.
2. Do not wait: have a lawyer prepare and send the notice (a draft is generated below for them to check).
3. After the notice, the cheque issuer has 15 days to pay; then you have one month to file the complaint.

**Proof to gather:**
- The original cheque
- The bank's cheque return memo (with the date you received it)
- Proof of the debt (agreement, invoice, messages, bank transfer)
- Any notice already sent, with postal proof

**When you need a real lawyer:** see one if the other side hires a lawyer, a court summons arrives, the amount is large, or you are unsure about forum or deadlines. Free help: NALSA 15100 / your District Legal Services Authority [LEGAL-AID].

**Warnings:**
- URGENT DEADLINE: about 1 day(s) are left (to about 09 Nov 2026, counting from the day you received the memo) to send the demand notice. Have a lawyer send it now.

_I am an AI, not a lawyer. This is general information, not legal advice. Verify before acting._

## Draft notice
```
DRAFT LEGAL NOTICE: NOT REVIEWED BY A LAWYER. Fill every [BRACKET]; get it checked by an advocate or the DLSA before sending (by registered post AD + email).

Date: [DATE]
To: [OTHER PARTY NAME], [ADDRESS]
From: [YOUR NAME], [YOUR ADDRESS], [PHONE]
Subject: Demand notice for dishonoured cheque

WARNING: strict deadlines apply (notice must go within 30 days of receiving the bank's return memo). Have a lawyer send this.

1. You issued cheque no. [NUMBER] dated [DATE] for Rs [AMOUNT] drawn on [BANK] towards [LIABILITY/DEBT].
2. On presentation, the cheque was returned unpaid on [DATE] with the remark '[REASON ON MEMO]'.
3. I call upon you to pay Rs [AMOUNT] within 15 days of receiving this notice, failing which I will file a complaint under Section 138 of the Negotiable Instruments Act, 1881.

Yours faithfully,
[YOUR NAME]
[SIGNATURE]

Enclosures: [copies of the proof listed above]
```

## Checks
- PASS: category got cheque_bounce
- PASS: language got en
- PASS: escalate got True
- PASS: amount got 200000
- PASS: retrieved NI-138 
- PASS: notice drafted 
- PASS: warning URGENT DEADLINE 
- PASS: no unsupported citation survived 
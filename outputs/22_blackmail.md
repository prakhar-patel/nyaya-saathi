# 22_blackmail
**Mode:** offline  |  **Run:** 2026-11-08 12:51

## Input
someone is blackmailing me with my photos and asking for money on whatsapp

## Analysis (deterministic layer)
```json
{
 "lang": "en",
 "category": "cyber_fraud",
 "flags": [
  [
   "blackmail",
   "Someone may be blackmailing you. Do not pay, do not delete the chats, take screenshots, and report it quickly: call 1930 or use cybercrime.gov.in."
  ]
 ],
 "out_of_scope": [],
 "scores": {
  "cyber_fraud": 1
 },
 "facts": {
  "amount_rs": null,
  "years_ago": null,
  "memo_age_days": null
 },
 "kb_ids": [
  "CYBER",
  "FIR",
  "LEGAL-AID"
 ],
 "warnings": [],
 "escalate": true,
 "questions": [
  "When did it happen (date and time)?",
  "How much money was taken?",
  "Have you already called 1930 or told your bank?"
 ]
}
```

## Answer shown to user
**⚠️ Someone may be blackmailing you. Do not pay, do not delete the chats, take screenshots, and report it quickly: call 1930 or use cybercrime.gov.in.**

**What I understood:** Online / UPI fraud

**Where you stand:**
- For online or UPI fraud, act within hours: call 1930 (National Cyber Crime Helpline), report at cybercrime.gov.in, and inform your bank in writing. Quick reporting improves the chance of the receiving account being frozen. Keep screenshots, transaction IDs and the scammer's number or ID. [CYBER]
- Police must register an FIR when told of a cognizable offence. Under the Bharatiya Nagarik Suraksha Sanhita, 2023 (which replaced the CrPC from 1 July 2024), information can be given orally or electronically. If the station refuses, a written complaint can be sent to the Superintendent of Police, and a Magistrate can be approached. [FIR]

**What to do next:**
1. Call 1930 now and report on cybercrime.gov.in; the first hours matter most.
2. Inform your bank in writing/by their fraud line and ask them to block the transaction and your card/UPI.
3. Keep all evidence; ask for the complaint acknowledgement number.
4. If police refuse to take a complaint, escalate in writing to the Superintendent of Police.

**Proof to gather:**
- Screenshots of messages/calls, scammer's number or ID
- Bank/UPI transaction IDs and statement
- Time of the fraud
- Acknowledgement number from 1930 / cybercrime.gov.in

**When you need a real lawyer:** see one if the other side hires a lawyer, a court summons arrives, the amount is large, or you are unsure about forum or deadlines. Free help: NALSA 15100 / your District Legal Services Authority [LEGAL-AID].

**To help you better, tell me:**
- When did it happen (date and time)?
- How much money was taken?
- Have you already called 1930 or told your bank?

_I am an AI, not a lawyer. This is general information, not legal advice. Verify before acting._

## Checks
- PASS: category got cyber_fraud
- PASS: escalate got True
- PASS: flag blackmail 
- PASS: answer mentions '1930' 
- PASS: no unsupported citation survived 
# 31_legal_threat_not_violence
**Mode:** offline  |  **Run:** 2026-11-08 12:51

## Input
My employer has not paid me for 4 months and the company is threatening to file a case against me if I complain

## Analysis (deterministic layer)
```json
{
 "lang": "en",
 "category": "unpaid_salary",
 "flags": [
  [
   "case_against",
   "A case, complaint or court date against you is involved or has been threatened. Please see a lawyer before replying to anything."
  ]
 ],
 "out_of_scope": [],
 "scores": {
  "unpaid_salary": 1
 },
 "facts": {
  "amount_rs": null,
  "years_ago": null,
  "memo_age_days": null
 },
 "kb_ids": [
  "WAGES",
  "WAGES-PROOF",
  "GRATUITY",
  "LIMITATION-GEN",
  "LEGAL-AID"
 ],
 "warnings": [],
 "escalate": true,
 "questions": [
  "Do you have an offer letter, payslips or bank statements?",
  "Are you still working there, or have you resigned/been terminated?"
 ]
}
```

## Answer shown to user
**⚠️ A case, complaint or court date against you is involved or has been threatened. Please see a lawyer before replying to anything.**

**What I understood:** Unpaid salary / wages / dues

**Where you stand:**
- Employers must pay wages on time and may deduct only what the law allows. Wage law is now the Code on Wages, 2019, which came into force on 21 November 2025 and replaced the Payment of Wages Act, 1936 and other older wage laws. For monthly-paid employees wages are generally due by the 7th day of the next month. Rules and the complaint office can differ by state and by whether your employer falls under the central or the state government's sphere, so confirm locally. The usual first remedy is a written demand to the employer, then a complaint to the state Labour Commissioner or local labour office, which is free. [WAGES]
- Useful proof for unpaid salary: offer or appointment letter, payslips, bank statements showing past salary credits, emails or WhatsApp messages about the dues or the promise to pay, attendance records, and any resignation or termination letter. [WAGES-PROOF]
- Gratuity is now governed by the Code on Social Security, 2020, in force from 21 November 2025, which replaced the Payment of Gratuity Act, 1972. It is generally payable after five years of continuous service (the Code also gives fixed-term employees gratuity after one year) and is due within 30 days once payable. Whether your employer is covered depends on establishment size and the rules; confirm this. [GRATUITY]
- Under the Limitation Act, 1963, the general period to sue for recovery of money or on a contract is three years. A claim filed after the limitation period can be dismissed, so old claims need urgent attention. [LIMITATION-GEN]

**What to do next:**
1. Send a written demand (email) listing months and amount due, with a short deadline (7 days).
2. Complain to the state Labour Commissioner / local labour office; it is free and does not need a lawyer.
3. If the dues are large or the employer denies the job, take a lawyer's or DLSA's help.
4. Act quickly: some wage claims have short time limits.

**Proof to gather:**
- Useful proof for unpaid salary: offer or appointment letter, payslips, bank statements showing past salary credits, emails or WhatsApp messages about the dues or the promise to pay, attendance records, and any resignation or termination letter.

**When you need a real lawyer:** see one if the other side hires a lawyer, a court summons arrives, the amount is large, or you are unsure about forum or deadlines. Free help: NALSA 15100 / your District Legal Services Authority [LEGAL-AID].

**To help you better, tell me:**
- Do you have an offer letter, payslips or bank statements?
- Are you still working there, or have you resigned/been terminated?

_I am an AI, not a lawyer. This is general information, not legal advice. Verify before acting._

## Checks
- PASS: category got unpaid_salary
- PASS: escalate got True
- PASS: flag case_against 
- PASS: answer lacks /violence or threats/ 
- PASS: no unsupported citation survived 
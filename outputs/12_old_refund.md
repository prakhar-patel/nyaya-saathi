# 12_old_refund
**Mode:** offline  |  **Run:** 2026-11-08 12:51

## Input
I bought a washing machine 3 years ago for Rs 30,000, it never worked properly and the shop refuses a refund.

## Analysis (deterministic layer)
```json
{
 "lang": "en",
 "category": "consumer_refund",
 "flags": [],
 "out_of_scope": [],
 "scores": {
  "consumer_refund": 1
 },
 "facts": {
  "amount_rs": 30000,
  "years_ago": 3.0,
  "memo_age_days": null
 },
 "kb_ids": [
  "CPA-JURIS",
  "CPA-LIMIT",
  "CPA-FILE",
  "NCH",
  "ECOM-RULES",
  "CPA-DEFICIENCY",
  "LEGAL-AID"
 ],
 "warnings": [
  "LIMITATION: consumer complaints normally must be filed within 2 years (Section 69). Yours may be late or close: get urgent advice."
 ],
 "escalate": false,
 "questions": [
  "Have you already complained to them? If yes, how and when?"
 ]
}
```

## Answer shown to user
**What I understood:** Consumer refund / defective product or service; amount mentioned: Rs 30,000

**Where you stand:**
- Consumer Protection Act, 2019: a complaint goes to the District Consumer Disputes Redressal Commission if the price paid for the goods/service is up to Rs 50 lakh, to the State Commission if it is above Rs 50 lakh and up to Rs 2 crore, and to the National Commission above Rs 2 crore (Consumer Protection (Jurisdiction of the District Commission, the State Commission and the National Commission) Rules, 2021). Most everyday refund problems are District Commission matters. A lawyer is not compulsory to file. [CPA-JURIS]
- Under Section 69 of the Consumer Protection Act, 2019, a complaint must normally be filed within two years from the date the cause of action arose. A Commission may accept a later complaint only if the person shows sufficient cause for the delay. [CPA-LIMIT]
- A consumer complaint can be filed online on the e-Jagriti portal (e-jagriti.gov.in), which replaced e-Daakhil from 1 January 2025, or in person at the District Commission. No fee is payable for District Commission claims up to Rs 5 lakh. Attach: proof of payment, order/invoice, messages or emails with the seller, and a copy of your written complaint to them. [CPA-FILE]
- The National Consumer Helpline (call 1915, or WhatsApp 8800001915) registers complaints against companies and tries to get them resolved before you go to a Commission. Registering also creates a dated record of your complaint. Online: consumerhelpline.gov.in. [NCH]
- Under the Consumer Protection (E-Commerce) Rules, 2020, an e-commerce platform must publish a grievance officer's details, acknowledge a complaint within 48 hours and resolve it within one month. A platform must also process refunds for returned or cancelled orders within a reasonable period. [ECOM-RULES]
- The Consumer Protection Act, 2019 covers defective goods (Section 2(10)) and deficiency in service (Section 2(11)). Non-delivery after payment, refusal to refund a valid return, or a product materially different from what was promised can fall under these. [CPA-DEFICIENCY]

**What to do next:**
1. Complain in writing to the seller/platform's grievance officer and note the ticket number; they must acknowledge within 48 hours (e-commerce).
2. Register the complaint on the National Consumer Helpline (1915 / consumerhelpline.gov.in) to create an official record and push for settlement.
3. Send a final written demand with a 15-day deadline (draft below).
4. If still unresolved, file a complaint online with the District Consumer Commission, within 2 years of the problem.

**Proof to gather:**
- Order confirmation / invoice / payment proof
- Screenshots of the product page, promised delivery date or terms
- All chats, emails and complaint ticket numbers with the seller/company
- Photos/videos of the defective or wrong product
- Return/cancellation confirmation, if any

**When you need a real lawyer:** see one if the other side hires a lawyer, a court summons arrives, the amount is large, or you are unsure about forum or deadlines. Free help: NALSA 15100 / your District Legal Services Authority [LEGAL-AID].

**Warnings:**
- LIMITATION: consumer complaints normally must be filed within 2 years (Section 69). Yours may be late or close: get urgent advice.

**To help you better, tell me:**
- Have you already complained to them? If yes, how and when?

_I am an AI, not a lawyer. This is general information, not legal advice. Verify before acting._

## Draft notice
```
DRAFT LEGAL NOTICE: NOT REVIEWED BY A LAWYER. Fill every [BRACKET]; get it checked by an advocate or the DLSA before sending (by registered post AD + email).

Date: [DATE]
To: [OTHER PARTY NAME], [ADDRESS]
From: [YOUR NAME], [YOUR ADDRESS], [PHONE]
Subject: Demand for refund of Rs 30,000 for [PRODUCT/SERVICE]

1. On [DATE] I paid Rs 30,000 to you for [PRODUCT/SERVICE] (Order/Invoice No. [NUMBER]).
2. [Describe the problem: not delivered / defective / different from what was promised / refund not processed after return].
3. I complained on [DATES] (ticket numbers [NUMBERS]) but the issue is unresolved.
4. Please refund Rs 30,000 [with compensation of Rs ___ for the inconvenience] within 15 days of receiving this notice. Failing this, I will file a complaint before the Consumer Disputes Redressal Commission and the National Consumer Helpline, at your cost and risk.

Yours faithfully,
[YOUR NAME]
[SIGNATURE]

Enclosures: [copies of the proof listed above]
```

## Checks
- PASS: category got consumer_refund
- PASS: language got en
- PASS: retrieved CPA-LIMIT 
- PASS: warning LIMITATION 
- PASS: no unsupported citation survived 
# Audit log: what was wrong in v1, what changed

v1 passed its own 20 tests. Those tests were written by the same author, so they proved little. This audit used inputs and attacks v1 had never seen.

| # | Found in v1 | Evidence | Fix |
|---|---|---|---|
| 1 | Guard caught only 3 of 15 adversarial sentences | `IPC 420`, `BNS 318`, `u/s 420`, Hindi Act name, `Rent Control Act`, `Article 21`, `NI Act`, court case without "v.", "within 7 days by law", "six months' rent", `Order 7 Rule 11 CPC` all passed | Guard rewritten: 6 checks (statutes w/ or w/o year, section numbers + Section<->Act pairing, abbreviations, courts/cases, Hindi statute words, duration figures). 18/18 caught, 6/6 legit kept |
| 2 | Self-harm message got full salary advice + "do you have an offer letter?" (doc claimed "fixed safe text") | outputs/15_self_harm.md (v1) | Crisis-only response (EN/HI), no case advice |
| 3 | Labour law out of date | Payment of Wages Act 1936 and Gratuity Act 1972 repealed 21 Nov 2025 (Code on Wages 2019, Code on Social Security 2020) | KB entries rewritten, `checked` field records what was and was not verified |
| 4 | e-Daakhil presented as "being moved" | e-Jagriti replaced it 1 Jan 2025 | KB updated |
| 5 | No deadline arithmetic for cheques | memo 45 days old -> no warning | Date / "N days ago" parsing, 30-day window computed; URGENT / MISSED warnings escalate |
| 6 | "years 8" parsed as Rs 8 | "4 years 8 months" -> amount 8 | amount regex requires a non-letter before Rs/INR |
| 7 | Substring keyword matching | "depositing" -> deposit flow (PF case); "three" contains "hr" | whole-word matching |
| 8 | Wrong side not detected | "tenant has not paid rent", "I am the HR" got tenant/employee advice | broadened other_side flag |
| 9 | Legal threat labelled violence | "threatening to file a case" -> "may involve violence" | violence regex excludes legal threats |
| 10 | Out-of-scope + violence had no 181/112 | "husband beats me" -> only NALSA | EMERGENCY added on that path |
| 11 | Blackmail/sextortion not routed or escalated | category None | new red flag + cyber category |
| 12 | Misroutes | loan to friend -> UPI fraud; fired -> unpaid salary; income-tax notice -> generic notice; rent hike -> deposit advice; criminal threat in notice not escalated | out-of-scope terms, termination rule, notice+oos rule, criminal-threat flag |
| 13 | `k\b` matched "bank" and suppressed the "how much?" question | | regex fixed |

## Honest limits of this audit
- Tests 21-43 were written *after* seeing failures: regression safety, not a generalisation score.
- Held-out round (12 inputs written before fixing): ~6 fine, 3 failed safe (asked for more detail), 3 unsafe (now fixed).
- LLM mode was never run end to end here (no API key); only a mock model. Run it yourself and record the result.
- KB: only WAGES, GRATUITY, CPA-FILE were re-verified on the web. All other entries are from memory.

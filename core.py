"""Nyaya Saathi core: everything here is plain code (no LLM), so it is testable and cheap.
The LLM (llm.py) is only used to *phrase* answers from the verified context this module selects."""
import json, os, re, datetime
from pathlib import Path

KB = json.loads((Path(__file__).parent / "data" / "kb.json").read_text(encoding="utf-8"))
KB_BY_ID = {e["id"]: e for e in KB}

# ---------------------------------------------------------------- scope & triage
CATEGORIES = {
    "rent_deposit": dict(
        label="Security deposit / rent dispute", label_hi="सिक्योरिटी डिपॉजिट / किराया विवाद",
        kw=["deposit", "landlord", "tenant", "rent agreement", "vacate", "vacated", "house owner", "flat owner", "pg", "paying guest",
            "makan malik", "malik", "मकान मालिक", "किराया", "डिपॉजिट", "किरायेदार", "security deposit"],
        kb=["RENT-DEPOSIT", "RENT-REMEDY", "LIMITATION-GEN", "LEGAL-AID"],
        proof=["Rent agreement (even unregistered/ on stamp paper)", "Proof you paid the deposit (bank/UPI statement, receipt)",
               "Proof you vacated and handed over keys (messages, handover photos, move-out date)",
               "Messages/emails where you asked for the deposit and the landlord's replies or excuses",
               "Photos/video of the flat's condition at move-out"],
        steps=["Send a polite but firm written demand (WhatsApp/email) asking for the refund by a date; keep the screenshot.",
               "If ignored, send a legal notice with a 15-day deadline (a draft is generated below; have a lawyer or the DLSA check it).",
               "If still unpaid, a civil recovery suit is the usual route; a local lawyer should confirm the forum for your state.",
               "Check whether your state has adopted the Model Tenancy Act, 2021 and what your agreement says about deductions."],
        ask=[("amount", r"(?:₹|\brs\.?|\binr\b|rupees|lakh|\d\s?k\b)|\d{4,}", "How much was the deposit, and how did you pay it (bank/UPI/cash)?"),
             ("agreement", r"agreement|written|stamp|contract|एग्रीमेंट|receipt", "Do you have a written rent agreement or any receipt?"),
             ("state", r"delhi|mumbai|bengal|bangalore|bengaluru|chennai|hyderabad|pune|kanpur|lucknow|noida|gurgaon|gurugram|jaipur|kolkata|ahmedabad|state|city|uttar pradesh|maharashtra|karnataka|tamil", "Which city/state is the property in? (Rent rules differ by state.)"),
             ("vacated", r"vacat|moved out|left the|handed over|खाली", "When did you vacate and hand over the keys?")]),
    "consumer_refund": dict(
        label="Consumer refund / defective product or service", label_hi="उपभोक्ता रिफंड / खराब सामान या सेवा",
        kw=["refund", "order", "product", "delivered", "defective", "amazon", "flipkart", "myntra", "seller", "return",
            "courier", "warranty", "paisa wapas", "paise wapas", "रिफंड", "पैसे वापस", "ऑर्डर", "सामान", "cancelled", "cancel"],
        kb=["CPA-JURIS", "CPA-LIMIT", "CPA-FILE", "NCH", "ECOM-RULES", "CPA-DEFICIENCY", "LEGAL-AID"],
        proof=["Order confirmation / invoice / payment proof", "Screenshots of the product page, promised delivery date or terms",
               "All chats, emails and complaint ticket numbers with the seller/company",
               "Photos/videos of the defective or wrong product", "Return/cancellation confirmation, if any"],
        steps=["Complain in writing to the seller/platform's grievance officer and note the ticket number; they must acknowledge within 48 hours (e-commerce).",
               "Register the complaint on the National Consumer Helpline (1915 / consumerhelpline.gov.in) to create an official record and push for settlement.",
               "Send a final written demand with a 15-day deadline (draft below).",
               "If still unresolved, file a complaint online with the District Consumer Commission, within 2 years of the problem."],
        ask=[("amount", r"(?:₹|\brs\.?|\binr\b|rupees|lakh|\d\s?k\b)|\d{3,}", "How much did you pay?"),
             ("who", r"amazon|flipkart|myntra|meesho|seller|shop|company|store|app|website|online|dealer", "Who is the seller/company, and was it bought online or in a shop?"),
             ("when", r"ago|20\d\d|january|february|march|april|may|june|july|august|september|october|november|december|week|month|yesterday|saal|महीने|दिन", "When did you buy it and when did the problem start?"),
             ("complained", r"complain|ticket|emailed|wrote|called|customer care|शिकायत", "Have you already complained to them? If yes, how and when?")]),
    "unpaid_salary": dict(
        label="Unpaid salary / wages / dues", label_hi="बकाया वेतन / सैलरी",
        kw=["salary", "wages", "unpaid", "employer", "paycheck", "gratuity", "full and final", "fnf", "notice period",
            "सैलरी", "तनख्वाह", "वेतन", "salary nahi", "salary nahin", "boss", "hr", "offer letter", "withheld"],
        kb=["WAGES", "WAGES-PROOF", "GRATUITY", "LIMITATION-GEN", "LEGAL-AID"],
        proof=None, steps=["Send a written demand (email) listing months and amount due, with a short deadline (7 days).",
                           "Complain to the state Labour Commissioner / local labour office; it is free and does not need a lawyer.",
                           "If the dues are large or the employer denies the job, take a lawyer's or DLSA's help.",
                           "Act quickly: some wage claims have short time limits."],
        ask=[("months", r"month|months|mahine|महीने|since|from", "For how many months is salary unpaid, and what is the monthly amount?"),
             ("proof", r"offer|appointment|payslip|bank|statement|email|whatsapp|letter", "Do you have an offer letter, payslips or bank statements?"),
             ("status", r"resign|quit|terminat|fired|still working|working|left|नौकरी", "Are you still working there, or have you resigned/been terminated?"),
             ("size", r"employees|startup|company|pvt|ltd|firm|factory|shop", "What kind of employer is it (company, small shop, factory) and in which state?")]),
    "cheque_bounce": dict(
        label="Dishonoured (bounced) cheque", label_hi="चेक बाउंस",
        kw=["cheque", "check bounced", "bounced", "bounce", "dishonour", "dishonoured", "चेक", "बाउंस", "return memo"],
        kb=["NI-138", "LEGAL-AID"], proof=["The original cheque", "The bank's cheque return memo (with the date you received it)",
                                           "Proof of the debt (agreement, invoice, messages, bank transfer)", "Any notice already sent, with postal proof"],
        steps=["Find the date you received the bank's return memo. The 30-day clock to send the demand notice starts then.",
               "Do not wait: have a lawyer prepare and send the notice (a draft is generated below for them to check).",
               "After the notice, the cheque issuer has 15 days to pay; then you have one month to file the complaint."],
        ask=[("memo", r"memo|returned|dishonou?red on|bounced on|\d{1,2}[/-]\d{1,2}|january|february|march|april|may|june|july|august|september|october|november|december", "What is the date on the bank's cheque-return memo, and when did you receive it?"),
             ("amount", r"(?:₹|\brs\.?|\binr\b|rupees|lakh|\d\s?k\b)|\d{4,}", "What is the cheque amount?"),
             ("notice", r"notice", "Have you already sent a demand notice? When?")]),
    "cyber_fraud": dict(
        label="Online / UPI fraud", label_hi="ऑनलाइन / UPI धोखाधड़ी",
        kw=["upi fraud", "upi scam", "upi account", "scam", "fraud", "otp", "hacked", "cyber", "phishing", "ठगी", "धोखाधड़ी", "paise kat", "kat gaye", "kat gaya", "money debited", "scammer", "fake call", "pretending to be", "blackmail", "blackmailing", "blackmailed", "sextortion", "ब्लैकमेल"],
        kb=["CYBER", "FIR", "LEGAL-AID"], proof=["Screenshots of messages/calls, scammer's number or ID", "Bank/UPI transaction IDs and statement",
                                                "Time of the fraud", "Acknowledgement number from 1930 / cybercrime.gov.in"],
        steps=["Call 1930 now and report on cybercrime.gov.in; the first hours matter most.",
               "Inform your bank in writing/by their fraud line and ask them to block the transaction and your card/UPI.",
               "Keep all evidence; ask for the complaint acknowledgement number.",
               "If police refuse to take a complaint, escalate in writing to the Superintendent of Police."],
        ask=[("when", r"today|yesterday|hours|minutes|ago|\d{1,2}[/-]\d{1,2}|आज|कल", "When did it happen (date and time)?"),
             ("amount", r"(?:₹|\brs\.?|\binr\b|rupees|lakh|\d\s?k\b)|\d{3,}", "How much money was taken?"),
             ("reported", r"1930|cybercrime|reported|bank|called|informed", "Have you already called 1930 or told your bank?")]),
    "notice_received": dict(
        label="You received a legal notice", label_hi="आपको कानूनी नोटिस मिला है",
        kw=["received a notice", "got a notice", "received a legal notice", "got a legal notice", "legal notice", "notice aaya", "notice mila", "नोटिस", "notice from", "demand notice", "sent me a notice"],
        kb=["LEGAL-NOTICE-RECEIVED", "LIMITATION-GEN", "LEGAL-AID"], proof=["The notice itself (all pages, envelope/email)", "Date and mode of receipt",
                                                                            "Any agreement, payment proof or messages relevant to what is claimed"],
        steps=["Note today's date, the deadline in the notice and who sent it.", "Do not ignore it; do not sign or pay in panic.",
               "Reply in writing before the deadline, sticking to facts (a lawyer should review the reply).",
               "If it is a court summons with a hearing date, see a lawyer immediately."],
        ask=[("who", r"from|by|sent|bank|landlord|company|lawyer|advocate|employer", "Who sent the notice and on whose behalf?"),
             ("claim", r"claim|demand|pay|asks|rs\.?|₹|lakh|vacate|evict", "What does the notice demand, and what is the deadline?"),
             ("true", r"true|false|wrong|agree|dispute|owe", "Is what they say right, wrong, or partly right?")]),
}
CAT_PRIORITY = ["notice_received", "cheque_bounce", "cyber_fraud", "rent_deposit", "unpaid_salary", "consumer_refund"]

OUT_OF_SCOPE = ["divorce", "custody", "alimony", "maintenance", "inheritance", "probate", "last will", "will deed", "partition", "property title", "bail", "builder", "rera", "sale deed", "ancestral", "hissa", "zameen", "possession of the flat",
                "visa", "immigration", "income tax", "gst", "patent", "trademark", "talaq", "तलाक", "वसीयत", "dowry", "dahej", "दहेज",
                "murder", "rape", "molest", "pocso", "defamation", "adoption",
                "insurance", "passed away", "legal heir", "death certificate", "sexual harassment", "posh", "rent increase", "rent hike", "increased the rent", "increased rent", "provident fund", "epf", "pf", "498a", "lent", "udhaar", "udhar", "borrowed", "cheated", "cheating", "ran away"]

RED_FLAGS = [  # (id, regex, message); ASCII terms use word boundaries (an earlier version matched 'warrant' inside 'warranty')
    ("arrest", r"\barrest|\bjail\b|\bcustody\b|\bremand\b|police (?:took|picked)|गिरफ्तार|जेल",
     "Someone may be arrested or in custody. This needs a criminal lawyer or DLSA legal aid today, not an AI chat."),
    ("case_against", r"\b(?:fir|case|complaint|chargesheet)\b (?:has been |was |is )?(?:filed|registered|lodged)? ?against me|\bsummons\b|\bcourt date\b|\bhearing on\b|\bnon-?bailable\b|\bwarrants?\b|\bcriminal (?:case|complaint|proceedings?)\b|\b(?:report|complain about|send) me (?:to|about)? ?(?:to )?(?:the )?police\b|\bgo(?:ing)? to (?:the )?police\b",
     "A case, complaint or court date against you is involved or has been threatened. Please see a lawyer before replying to anything."),
    # physical violence / threats to the person; 'threatening to file a case' is a LEGAL threat and is handled by case_against
    ("violence", r"\bbeat(?:ing|en|s)?\b|\bhit me\b|\bthreaten\w*\s+(?:me|us|my family)\b(?!\s+(?:to|with)\s+(?:file|complain|report|sue|legal|police|court|case|take))|\bthreat\s+to\s+(?:kill|hurt|harm)|domestic violence|\babuse|\bharass|\bmolest|\brape\b|\bdowry\b|\bdahej\b|मारपीट|धमकी|हिंसा|दहेज",
     "This may involve violence or threats. Your safety comes first; see the helplines below."),
    ("blackmail", r"\bblackmail\w*|\bsextortion|\bmorphed\b|\bleak(?:ing)? my (?:photos?|videos?|pictures?)|ब्लैकमेल",
     "Someone may be blackmailing you. Do not pay, do not delete the chats, take screenshots, and report it quickly: call 1930 or use cybercrime.gov.in."),
    ("self_harm", r"\bsuicide|end(?:ing)? my life|kill myself|jaan de|मरना चाहता|आत्महत्या",
     "You sound very distressed. Please talk to someone right now (Tele-MANAS 14416, or 112 in an emergency)."),
    ("eviction", r"\bevict|throw(?:ing)? me out|ghar se nikal|घर से निकाल",
     "Eviction rules are state-specific and time-sensitive, and the deposit guidance I give does not cover them. Speak to a lawyer or your DLSA before you move out or sign anything."),
    ("other_side", r"\bmy (?:tenant|employee|customer|buyer|worker)s?\b|\bi am (?:the |a |an )?(?:landlord|employer|owner|hr|manager|seller|shopkeeper)\b|\bi (?:own|run) (?:a|the) (?:shop|company|business|flat|house)\b|\b(?:tenant|employee|customer|buyer)s? (?:has|have|is|are|did|does|will) (?:not|n't|refus\w*|stop\w*|left|asking|demand\w*)\b|\bnot paid (?:the |my )?rent\b|\brent (?:is )?(?:pending|unpaid|overdue)\b|\bemployee is asking\b",
     "It looks like you are the landlord/employer/seller. My guidance is written for the tenant/employee/consumer and may not fit your side. Please consult a lawyer."),
]
BIG_AMOUNT = 10_00_000  # Rs 10 lakh: above this we nudge toward a real lawyer

# ---------------------------------------------------------------- language & facts
def detect_lang(text):
    if re.search(r"[\u0900-\u097F]", text):
        return "hi"
    hinglish = r"\b(mujhe|mera|meri|nahi|nahin|hai|hain|kya|kaise|paisa|paise|malik|wapas|aaya|mila|kar|raha|rahi|bhai|sir|dedo|kab)\b"
    return "hinglish" if len(re.findall(hinglish, text.lower())) >= 2 else "en"


def parse_amount(text):
    t = text.lower().replace(",", "")
    best = None
    for m in re.finditer(r"(?:₹|(?<![a-z])rs\.?|(?<![a-z])inr|(?<![a-z])rupees?)\s*(\d+(?:\.\d+)?)\s*(lakh|lac|crore|cr|k|thousand)?|(\d+(?:\.\d+)?)\s*(lakh|lac|crore|cr|k|thousand|rupees|rupee|rs|रुपये|रुपए|रु)(?![a-z])", t):
        num = float(m.group(1) or m.group(3)); unit = (m.group(2) or m.group(4) or "")
        mult = {"lakh": 1e5, "lac": 1e5, "crore": 1e7, "cr": 1e7, "k": 1e3, "thousand": 1e3}.get(unit, 1)
        val = int(num * mult)
        best = val if best is None or val > best else best
    return best


def parse_years_ago(text):
    t = text.lower()
    m = re.search(r"(\d+(?:\.\d+)?)\s*(?:years?|yrs?|saal|साल)(?:\s*(?:and\s*)?(\d+)\s*(?:months?|mahine|महीने))?\s*(?:ago|back|pehle|पहले)", t)
    if m: return float(m.group(1)) + (int(m.group(2)) / 12 if m.group(2) else 0)
    m = re.search(r"(\d+)\s*(?:months?|mahine|महीने)\s*(?:ago|back|pehle|पहले)", t)
    return int(m.group(1)) / 12 if m else None


MONTHS = {m: i + 1 for i, m in enumerate(["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"])}


def today():
    """Overridable (NYAYA_TODAY=YYYY-MM-DD) so deadline tests are reproducible."""
    v = os.getenv("NYAYA_TODAY")
    return datetime.date.fromisoformat(v) if v else datetime.date.today()


def _dates_in(t):
    out = []
    for m in re.finditer(r"(\d{1,2})(?:st|nd|rd|th)?\s+(" + "|".join(MONTHS) + r")[a-z]*,?\s+(\d{4})", t):
        try: out.append((m.start(), datetime.date(int(m.group(3)), MONTHS[m.group(2)], int(m.group(1)))))
        except ValueError: pass
    for m in re.finditer(r"\b(\d{1,2})[/-](\d{1,2})[/-](\d{4})\b", t):          # Indian order: dd/mm/yyyy
        try: out.append((m.start(), datetime.date(int(m.group(3)), int(m.group(2)), int(m.group(1)))))
        except ValueError: pass
    return out


def parse_memo_age_days(text):
    """Days since the cheque-return memo, from an explicit date or a '40 days ago' / '3 hafte pehle' phrase near the word 'memo'."""
    t = text.lower(); memos = [m.start() for m in re.finditer(r"memo", t)]
    if not memos: return None
    cands = []
    for pos, d in _dates_in(t):
        cands.append((min(abs(pos - p) for p in memos), (today() - d).days))
    for m in re.finditer(r"(\d+)\s*(day|days|din|week|weeks|hafte|hafta|month|months|mahine)\s*(?:ago|pehle|back)", t):
        n, u = int(m.group(1)), m.group(2)
        days = n * (7 if u.startswith(("week", "haft")) else 30 if u.startswith(("month", "mahin")) else 1)
        cands.append((min(abs(m.start() - p) for p in memos), days))
    cands = [c for c in cands if c[0] <= 60 and c[1] >= 0]
    return min(cands)[1] if cands else None


def extract_facts(text):
    return {"amount_rs": parse_amount(text), "years_ago": parse_years_ago(text), "memo_age_days": parse_memo_age_days(text)}

# ---------------------------------------------------------------- triage
def kw_in(k, t):
    """Whole-word keyword match (optional plural / -ed). Devanagari keywords use plain substring."""
    if not k.isascii(): return k in t
    return re.search(r"(?<![a-z0-9])" + re.escape(k) + r"(?:s|es|ed|d)?(?![a-z0-9])", t) is not None


TERMINATION = r"\b(?:fired|laid off|terminated|sacked|dismissed|retrench\w*)\b|removed from (?:the )?job|नौकरी से निकाल"
SALARY_CUES = r"\b(?:salary|wages?|unpaid|not paid|dues|full and final|fnf|gratuity|payslips?)\b|सैलरी|वेतन|तनख्वाह"


def triage(text):
    t = text.lower()
    flags = [(i, msg) for i, rx, msg in RED_FLAGS if re.search(rx, t)]
    scores = {}
    for c, d in CATEGORIES.items():
        s = sum(2 if " " in k else 1 for k in d["kw"] if kw_in(k, t))
        if s: scores[c] = s
    oos = [k for k in OUT_OF_SCOPE if kw_in(k, t)]
    if re.search(TERMINATION, t) and not re.search(SALARY_CUES, t): oos.append("termination")   # wrongful termination is not unpaid salary
    cat = None
    if scores:
        top = max(scores.values())
        cat = next(c for c in CAT_PRIORITY if scores.get(c) == top)
    # an out-of-scope topic wins when nothing in scope is strong, or when the in-scope hit is only 'you got a notice' (e.g. a tax notice)
    if oos and (cat is None or scores[cat] <= 1 or cat == "notice_received"):
        cat = "out_of_scope"
    return cat, flags, oos, scores


def retrieve(cat, text, flags):
    ids = list(CATEGORIES[cat]["kb"]) if cat in CATEGORIES else []
    toks = set(re.findall(r"[a-z0-9]+", text.lower()))
    extra = sorted(((len(toks & set(e["tags"])), e["id"]) for e in KB if e["id"] not in ids), reverse=True)
    ids += [i for s, i in extra[:2] if s >= 2 and i not in ("EMERGENCY",)]
    if any(f[0] in ("violence", "self_harm") for f in flags) and "EMERGENCY" not in ids:
        ids.append("EMERGENCY")
    if not ids or flags:
        if "LEGAL-AID" not in ids: ids.append("LEGAL-AID")
    return ids

# ---------------------------------------------------------------- hallucination guard
# Everything the model says about law must be traceable to the retrieved KB entries. Six independent checks, all deterministic:
#  1 named statutes (with or without year; wrong year caught)   2 section/article/rule/order numbers and Section<->Act pairing
#  3 bare abbreviations (IPC, BNS, CrPC, NI Act ...)             4 courts / judgments / case names
#  5 Hindi statute words must map to an Act that is in context    6 duration figures ('7 days', 'six months') must appear in context or the user's own text
STOP = {"the", "this", "that", "these", "under", "an", "a", "any", "each", "such", "your", "our", "its", "see", "per", "also", "same", "and", "or",
        "as", "by", "for", "with", "if", "on", "in", "of", "check", "confirm", "whether", "but", "however", "note", "use", "file", "to", "at"}
STAT_RE = re.compile(r"(?:\b(?:[A-Z][\w&'-]*[)]?\s+){1,6}(?:Act|Rules|Sanhita|Code)\b|\bCode (?:on|of) (?:[A-Z][\w&'-]*\s*){1,4})(?:,?\s*(?:of\s+)?(\d{4}))?")
SEC_RE = re.compile(r"(?:\bSection|\bSec\.|\bs\.|\bu/s|\bArticle|\bRule|\bOrder|धारा|\bdhara|\bdhaara)\s*(\d+[A-Za-z]?)", re.I)
SEC_ACT_RE = re.compile(r"(?:Section|Sec\.|s\.)\s*(\d+[A-Za-z]?)(?:\(\d+\))?\s*(?:of|,)?\s*(?:the\s+)?((?:[A-Z][\w&'-]*\s+){1,6}Act)")
ABBR_RE = re.compile(r"\b(?:IPC|BNSS?|CrPC|CPC|POCSO|PMLA|NI Act|IT Act|RTI Act|FEMA|Indian Penal Code|Penal Code|Bharatiya Nyaya Sanhita|Constitution)\b")
COURT_RE = re.compile(r"\b(?:Supreme Court|High Court|Hon'ble|landmark|precedent|judg(?:e)?ments?|Tribunal|NCDRC|SCDRC)\b", re.I)
CASE_RE = re.compile(r"\b[A-Z][\w.&' ]{2,40}\s+v(?:s)?\.?\s+[A-Z][\w.&' ]{2,40}|\bAIR\s*\d{4}|\b\d{4}\s*SCC\b|\bSCC\s*\(", re.U)
HI_STAT_RE = re.compile(r"अधिनियम|संहिता|एक्ट")
HI_ALIAS = {"उपभोक्ता संरक्षण": "consumer protection", "परिसीमा": "limitation act", "परक्राम्य लिखत": "negotiable instruments", "आदर्श किरायेदारी": "model tenancy",
            "मॉडल टेनेंसी": "model tenancy", "भारतीय नागरिक सुरक्षा": "nagarik suraksha", "ई-कॉमर्स": "e-commerce", "विधिक सेवा": "legal services",
            "ग्रेच्युटी": "gratuity", "वेतन संहिता": "code on wages", "मजदूरी संहिता": "code on wages", "सामाजिक सुरक्षा": "social security", "सिविल प्रक्रिया": "civil procedure"}
NUMW = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "fifteen": 15,
        "thirty": 30, "sixty": 60, "ninety": 90}
UNITS = {"दिन": "day", "महीने": "month", "महीना": "month", "साल": "year", "घंटे": "hour", "हफ्ते": "week"}
FIG_RE = re.compile(r"(\d+(?:\.\d+)?|" + "|".join(NUMW) + r")[\s-]*(?:calendar\s+)?(days?|weeks?|months?|years?|hours?)(?![a-z])|(\d+)\s*(दिन|महीने|महीना|साल|घंटे|हफ्ते)", re.I)


def _norm(x):
    return re.sub(r"\s+", " ", x.replace("(", " ").replace(")", " ")).strip().lower()


def figures(text):
    out = set()
    for m in FIG_RE.finditer(text.lower().replace(",", "")):
        n, u = (m.group(1), m.group(2)) if m.group(1) else (m.group(3), UNITS[m.group(4)])
        n = float(NUMW.get(n, n)); u = u.rstrip("s") if u.isascii() else u
        out.add((n, u))
    return out


def _ctx(ids):
    return " ".join(KB_BY_ID[i]["text"] + " " + KB_BY_ID[i]["source"] for i in ids if i in KB_BY_ID)


def trusted_text(user_text, a):
    """Text whose figures are allowed to be repeated: the user's own words, the system's own step lists, warnings and flag messages."""
    d = CATEGORIES.get(a["category"], {})
    return " ".join([user_text, " ".join(d.get("steps") or []), " ".join(d.get("proof") or []), " ".join(a["warnings"]), " ".join(m for _, m in a["flags"])])


def _stat_phrase(m, line_start):
    toks = m.group(0).split(); year = m.group(1)
    body = re.sub(r",?\s*(?:of\s+)?\d{4}$", "", m.group(0)).split()
    variants = []
    for start in (0, 1):                                    # also try without a sentence-initial word ('Check Model Tenancy Act')
        t = body[start:]
        while t and t[0].lower() in STOP: t = t[1:]
        if len(t) >= 2 or (t and t[0] == "Code"): variants.append(_norm(" ".join(t)))
        if not (line_start and start == 0): break
    return variants, year


def guard(text, ids, trusted=""):
    """Remove sentences that cite law not present in the retrieved verified context (see the six checks above).
    Line-aware so markdown survives; abbreviation-aware so 'v.' / 'Rs.' do not split sentences."""
    ctx = _ctx(ids); ctxn = _norm(ctx); ctx_l = ctx.lower()
    secs = {m.group(1).lower() for m in SEC_RE.finditer(ctx)}
    allowed_figs = figures(ctx + " " + trusted)
    bad, out_lines = [], []
    for line in text.split("\n"):
        kept = []
        for sent in SENT_SPLIT.split(line):
            r = []
            for m in STAT_RE.finditer(sent):
                variants, year = _stat_phrase(m, m.start() <= 1)
                if not variants: continue
                if not any(v in ctxn for v in variants): r.append("unverified statute: " + m.group(0).strip())
                elif year and not any((v + ", " + year) in ctxn or (v + " " + year) in ctxn for v in variants): r.append("wrong year: " + m.group(0).strip())
            for m in SEC_RE.finditer(sent):
                if m.group(1).lower() not in secs: r.append("unverified section: " + m.group(0).strip())
            for m in SEC_ACT_RE.finditer(sent):                 # Section N of <Act> must co-occur in one KB entry
                act = _norm(m.group(2)); sec = m.group(1).lower()
                ok = any(re.search(r"(?:section|sec\.|s\.)\s*" + re.escape(sec) + r"\b", (KB_BY_ID[i]["text"] + KB_BY_ID[i]["source"]).lower())
                         and act.split(" ", 1)[-1] in _norm(KB_BY_ID[i]["text"] + KB_BY_ID[i]["source"]) for i in ids if i in KB_BY_ID)
                if not ok: r.append("section/act mismatch: " + m.group(0).strip())
            for rx in (ABBR_RE, COURT_RE):
                r += ["unverified reference: " + m.group(0) for m in rx.finditer(sent) if m.group(0).lower() not in ctx_l]
            r += ["case name: " + m.group(0).strip() for m in CASE_RE.finditer(sent)]
            if HI_STAT_RE.search(sent) and not any(h in sent and e in ctx_l for h, e in HI_ALIAS.items()): r.append("unverified Hindi statute reference")
            r += [f"unverified figure: {n:g} {u}" for n, u in figures(sent) if (n, u) not in allowed_figs]
            if r: bad.append({"sentence": sent, "unsupported": r})
            else: kept.append(sent)
        out_lines.append(" ".join(kept))
    return "\n".join(out_lines), bad


SENT_SPLIT = re.compile(r"(?<=[.!?])(?<!\bv\.)(?<!\bvs\.)(?<!\bs\.)(?<!\bSec\.)(?<!\bNo\.)(?<!\bRs\.)(?<!\bno\.)\s+(?=[A-Z0-9\[(])")

# ---------------------------------------------------------------- drafts
def build_notice(cat, facts):
    amt = f"Rs {facts['amount_rs']:,}" if facts.get("amount_rs") else "Rs [AMOUNT]"
    head = ("DRAFT LEGAL NOTICE: NOT REVIEWED BY A LAWYER. Fill every [BRACKET]; get it checked by an advocate or the DLSA before sending "
            "(by registered post AD + email).\n\nDate: [DATE]\nTo: [OTHER PARTY NAME], [ADDRESS]\nFrom: [YOUR NAME], [YOUR ADDRESS], [PHONE]\n")
    tail = "\n\nYours faithfully,\n[YOUR NAME]\n[SIGNATURE]\n\nEnclosures: [copies of the proof listed above]"
    if cat == "rent_deposit":
        body = (f"Subject: Demand for refund of security deposit of {amt}\n\n"
                f"1. I was your tenant at [PROPERTY ADDRESS] under [a rent agreement dated DATE / an oral arrangement].\n"
                f"2. I paid you a refundable security deposit of {amt} on [DATE] by [MODE OF PAYMENT].\n"
                f"3. I vacated and handed over possession to you on [DATE].\n"
                f"4. Despite my requests on [DATES AND MODES], you have not refunded the deposit [and have given no valid reason / have claimed deductions of Rs ___ which are unjustified because ___].\n"
                f"5. You are called upon to pay {amt} within 15 days of receiving this notice. Failing this, I will be compelled to take legal proceedings for recovery, with interest as permissible by law and costs, entirely at your risk.")
    elif cat == "consumer_refund":
        body = (f"Subject: Demand for refund of {amt} for [PRODUCT/SERVICE]\n\n"
                f"1. On [DATE] I paid {amt} to you for [PRODUCT/SERVICE] (Order/Invoice No. [NUMBER]).\n"
                f"2. [Describe the problem: not delivered / defective / different from what was promised / refund not processed after return].\n"
                f"3. I complained on [DATES] (ticket numbers [NUMBERS]) but the issue is unresolved.\n"
                f"4. Please refund {amt} [with compensation of Rs ___ for the inconvenience] within 15 days of receiving this notice. Failing this, I will file a complaint before the Consumer Disputes Redressal Commission and the National Consumer Helpline, at your cost and risk.")
    elif cat == "unpaid_salary":
        body = (f"Subject: Demand for unpaid salary for [MONTHS]\n\n"
                f"1. I have been employed with you as [DESIGNATION] since [DATE] at a monthly salary of Rs [AMOUNT] (Offer letter dated [DATE]).\n"
                f"2. Salary for [MONTHS] totalling {amt if facts.get('amount_rs') else 'Rs [TOTAL]'} has not been paid despite my requests on [DATES].\n"
                f"3. Please pay the entire outstanding amount within 7 days of this notice. Failing this, I will approach the Labour Commissioner and other competent authorities for recovery.")
    elif cat == "cheque_bounce":
        body = ("Subject: Demand notice for dishonoured cheque\n\n"
                "WARNING: strict deadlines apply (notice must go within 30 days of receiving the bank's return memo). Have a lawyer send this.\n\n"
                "1. You issued cheque no. [NUMBER] dated [DATE] for Rs [AMOUNT] drawn on [BANK] towards [LIABILITY/DEBT].\n"
                "2. On presentation, the cheque was returned unpaid on [DATE] with the remark '[REASON ON MEMO]'.\n"
                "3. I call upon you to pay Rs [AMOUNT] within 15 days of receiving this notice, failing which I will file a complaint under Section 138 of the Negotiable Instruments Act, 1881.")
    else:
        return None
    return head + body + tail


ROLEPLAY_PROMPT = ("You are role-playing the OTHER side in a dispute so the user can practise. Case: {case}. Play a realistic, firm but "
                   "non-abusive {other} who gives typical excuses. After 4 exchanges, stop and give the user feedback: what they said well, "
                   "what proof they should have mentioned, and one thing to avoid. Never state any law or section; stay in character as a layperson.")
OTHERS = {"rent_deposit": "landlord", "consumer_refund": "customer-care executive", "unpaid_salary": "HR manager",
          "cheque_bounce": "debtor", "notice_received": "claimant's representative", "cyber_fraud": "bank officer"}

# ---------------------------------------------------------------- offline responder
HEAD = {"en": dict(u="What I understood", s="Where you stand", n="What to do next", p="Proof to gather", q="To help you better, tell me",
                   l="When you need a real lawyer", d="I am an AI, not a lawyer. This is general information, not legal advice. Verify before acting."),
        "hi": dict(u="मैंने क्या समझा", s="आपकी स्थिति", n="आगे क्या करें", p="जमा करने लायक सबूत", q="बेहतर मदद के लिए बताइए",
                   l="कब असली वकील चाहिए", d="मैं AI हूँ, वकील नहीं। यह सामान्य जानकारी है, कानूनी सलाह नहीं। कदम उठाने से पहले जाँच लें।")}


def clarifying(cat, text, n=3):
    if cat not in CATEGORIES: return []
    return [q for _, rx, q in CATEGORIES[cat]["ask"] if not re.search(rx, text.lower())][:n]


def analyse(text, lang=None):
    """Deterministic analysis shared by offline and LLM modes."""
    lang = lang or detect_lang(text)
    cat, flags, oos, scores = triage(text)
    facts = extract_facts(text)
    ids = retrieve(cat, text, flags) if cat != "out_of_scope" else ["LEGAL-AID"]
    if cat == "out_of_scope" and any(f[0] in ("violence", "self_harm") for f in flags): ids.append("EMERGENCY")
    warnings = []
    ya = facts["years_ago"]
    if ya is not None and cat == "consumer_refund" and ya >= 2:
        warnings.append("LIMITATION: consumer complaints normally must be filed within 2 years (Section 69). Yours may be late or close: get urgent advice.")
    if ya is not None and cat in ("rent_deposit", "unpaid_salary") and ya >= 2.5:
        warnings.append("LIMITATION: money claims generally expire after about 3 years under the Limitation Act, 1963. Act urgently.")
    if facts["amount_rs"] and facts["amount_rs"] >= BIG_AMOUNT:
        warnings.append(f"HIGH VALUE: Rs {facts['amount_rs']:,} is a large claim; please engage a lawyer rather than self-filing.")
    if re.search(r"\b(ipc|bns|bnss|crpc|section number|which section|case law|supreme court|high court|judg(?:e)?ments?|precedent)\b|\bsection\s*\d+|\b\d{2,3}\s?[a-z]\b(?=.*\b(?:section|ipc|bns)\b)|\b498\s?a\b", text.lower()):
        warnings.append("CITATION REQUEST: I only cite law from my verified list and never invent section numbers or case names. For exact sections or past cases to quote, ask a lawyer or the DLSA.")
    age = facts.get("memo_age_days")
    if cat == "cheque_bounce" and age is not None:
        left, due = 30 - age, today() - datetime.timedelta(days=age) + datetime.timedelta(days=30)
        if left < 0:
            warnings.append(f"MISSED DEADLINE?: you indicate the bank's return memo is about {age} days old. The demand notice has to be sent within 30 days of receiving the memo, so this window may already have passed. See a lawyer today; only a lawyer can tell you whether anything can still be done.")
        elif left <= 7:
            warnings.append(f"URGENT DEADLINE: about {left} day(s) are left (to about {due:%d %b %Y}, counting from the day you received the memo) to send the demand notice. Have a lawyer send it now.")
        else:
            warnings.append(f"DEADLINE: send the demand notice by about {due:%d %b %Y} ({left} days left, counting from the day you received the memo). Do not wait.")
    escalate = bool(flags) or cat == "out_of_scope" or any(w.startswith(("HIGH", "URGENT", "MISSED")) for w in warnings)
    return dict(lang=lang, category=cat, flags=flags, out_of_scope=oos, scores=scores, facts=facts, kb_ids=ids,
                warnings=warnings, escalate=escalate, questions=clarifying(cat, text))


CRISIS = {"en": ("I'm really sorry you are going through this. Please reach out to someone right now: Tele-MANAS on 14416, or call 112 if you are in immediate danger. "
                 "If someone you trust is nearby, please tell them how you feel.\n\nMoney and legal problems can feel unbearable, but they can be handled one step at a time, "
                 "and I will help with the legal side whenever you want to come back to it."),
          "hi": ("मुझे बहुत अफ़सोस है कि आप इससे गुज़र रहे हैं। कृपया अभी किसी से बात करें: Tele-MANAS 14416, या तुरंत ख़तरे में हों तो 112 पर कॉल करें। "
                 "अगर कोई भरोसेमंद व्यक्ति पास में है, तो उसे बताइए कि आप कैसा महसूस कर रहे हैं।\n\nपैसे और कानूनी परेशानियाँ बहुत भारी लगती हैं, पर उन्हें एक-एक कदम में सुलझाया जा सकता है। "
                 "जब आप चाहें, मैं कानूनी हिस्से में मदद करूँगा/करूँगी।")}


def offline_answer(text, a):
    L = HEAD["hi" if a["lang"] == "hi" else "en"]
    cat, out = a["category"], []
    if any(f[0] == "self_harm" for f in a["flags"]):      # never mix a crisis message with case advice
        return CRISIS["hi" if a["lang"] == "hi" else "en"]
    if a["flags"]:
        out += ["**⚠️ " + m + "**" for _, m in a["flags"]] + [""]
    if cat == "out_of_scope":
        out += ["This looks like a matter outside what I can safely handle (e.g. family, criminal, inheritance, tax, insurance, job termination or immigration law). "
                "I would only be guessing, and mistakes here can cost you a lot.",
                "", f"**{L['l']}:** now. Free option: " + KB_BY_ID["LEGAL-AID"]["text"]]
    elif cat is None:
        out += ["I could not tell yet what your problem is. I can help with: security-deposit/rent disputes, consumer refunds, unpaid salary, "
                "bounced cheques, online/UPI fraud and legal notices you have received.",
                "", "Please tell me in your own words: what happened, when, with whom, how much money is involved, and what proof you have."]
    else:
        d = CATEGORIES[cat]
        out += [f"**{L['u']}:** {d['label_hi'] if a['lang']=='hi' else d['label']}" + (f"; amount mentioned: Rs {a['facts']['amount_rs']:,}" if a['facts']['amount_rs'] else ""), ""]
        out += [f"**{L['s']}:**"] + [f"- {KB_BY_ID[i]['text']} [{i}]" for i in a["kb_ids"] if i not in ("LEGAL-AID", "EMERGENCY")] + [""]
        out += [f"**{L['n']}:**"] + [f"{k+1}. {s}" for k, s in enumerate(d["steps"])] + [""]
        proof = d["proof"] or [KB_BY_ID["WAGES-PROOF"]["text"]]
        out += [f"**{L['p']}:**"] + [f"- {p}" for p in proof] + [""]
        out += [f"**{L['l']}:** "
                + ("see one if the other side hires a lawyer, a court summons arrives, the amount is large, or you are unsure about forum or deadlines. Free help: NALSA 15100 / your District Legal Services Authority [LEGAL-AID]."), ""]
    if "EMERGENCY" in a["kb_ids"]:
        out += [KB_BY_ID["EMERGENCY"]["text"] + " [EMERGENCY]", ""]
    if a["warnings"]:
        out += ["**Warnings:**"] + [f"- {w}" for w in a["warnings"]] + [""]
    if a["questions"] and cat not in ("out_of_scope",):
        out += [f"**{L['q']}:**"] + [f"- {q}" for q in a["questions"]] + [""]
    out += [f"_{L['d']}_"]
    return "\n".join(out)


def respond_offline(text, lang=None):
    a = analyse(text, lang)
    ans = offline_answer(text, a)
    clean, removed = guard(ans, a["kb_ids"], trusted_text(text, a))
    notice = build_notice(a["category"], a["facts"]) if a["category"] in CATEGORIES and not a["flags"] else None
    return dict(analysis=a, answer=clean, removed=removed, notice=notice, mode="offline")

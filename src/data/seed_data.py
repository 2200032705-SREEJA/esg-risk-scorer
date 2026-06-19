"""
Realistic offline ESG seed dataset.
Used when NEWS_API_KEY is absent so the dashboard runs on real scored data
instead of numpy.random.

Each entry: (company, published_date_offset_days_ago, headline, esg_label_hint, sentiment_hint)
We let the actual classifier/sentiment modules score them — no hardcoding.
"""

from datetime import date, timedelta

def _d(n: int) -> str:
    return (date.today() - timedelta(days=n)).isoformat()

SEED_ARTICLES: list[dict] = [
    # ── Apple ─────────────────────────────────────────────────────────────────
    {"company": "Apple", "publishedAt": _d(1),  "title": "Apple commits to 100% recycled aluminium in Mac lineup by 2025", "source": "Reuters"},
    {"company": "Apple", "publishedAt": _d(3),  "title": "Workers at Apple supplier in China allege excessive overtime violations", "source": "FT"},
    {"company": "Apple", "publishedAt": _d(6),  "title": "Apple fined €1.8bn by EU for App Store anticompetitive practices", "source": "BBC"},
    {"company": "Apple", "publishedAt": _d(10), "title": "Apple achieves carbon-neutral operations across all global offices", "source": "Bloomberg"},
    {"company": "Apple", "publishedAt": _d(14), "title": "SEC probes Apple executive stock compensation disclosure practices", "source": "WSJ"},
    {"company": "Apple", "publishedAt": _d(20), "title": "Apple expands renewable energy partnerships in Southeast Asia", "source": "Reuters"},
    {"company": "Apple", "publishedAt": _d(25), "title": "Apple diversity report shows 3% improvement in underrepresented hiring", "source": "CNBC"},

    # ── Microsoft ─────────────────────────────────────────────────────────────
    {"company": "Microsoft", "publishedAt": _d(2),  "title": "Microsoft pledges to remove all historical carbon emissions by 2050", "source": "Bloomberg"},
    {"company": "Microsoft", "publishedAt": _d(5),  "title": "Microsoft faces employee backlash over AI military contract renewal", "source": "Guardian"},
    {"company": "Microsoft", "publishedAt": _d(8),  "title": "Regulatory scrutiny intensifies over Microsoft Activision deal governance", "source": "FT"},
    {"company": "Microsoft", "publishedAt": _d(12), "title": "Microsoft data centres exceed water usage targets in drought regions", "source": "Reuters"},
    {"company": "Microsoft", "publishedAt": _d(18), "title": "Microsoft ranked top employer for disability inclusion for third year", "source": "CNBC"},
    {"company": "Microsoft", "publishedAt": _d(22), "title": "Microsoft board approves independent AI ethics oversight committee", "source": "WSJ"},

    # ── Amazon ────────────────────────────────────────────────────────────────
    {"company": "Amazon", "publishedAt": _d(1),  "title": "Amazon warehouse injury rates still double industry average, report finds", "source": "Reuters"},
    {"company": "Amazon", "publishedAt": _d(4),  "title": "Amazon delivery vans emit more per mile than rivals, study shows", "source": "Guardian"},
    {"company": "Amazon", "publishedAt": _d(7),  "title": "Amazon faces antitrust lawsuit over third-party seller pricing practices", "source": "FT"},
    {"company": "Amazon", "publishedAt": _d(11), "title": "Amazon launches 100,000 electric delivery vehicles from Rivian fleet", "source": "Bloomberg"},
    {"company": "Amazon", "publishedAt": _d(16), "title": "Amazon union drive in Alabama faces new legal challenges", "source": "WSJ"},
    {"company": "Amazon", "publishedAt": _d(21), "title": "Amazon commits $1bn to affordable housing near distribution hubs", "source": "CNBC"},

    # ── Tesla ─────────────────────────────────────────────────────────────────
    {"company": "Tesla", "publishedAt": _d(2),  "title": "Tesla Autopilot investigated by NHTSA after fatal highway crash", "source": "Reuters"},
    {"company": "Tesla", "publishedAt": _d(5),  "title": "Tesla battery recycling programme recovers 92% of lithium from old packs", "source": "Bloomberg"},
    {"company": "Tesla", "publishedAt": _d(9),  "title": "Tesla board under fire for excessive CEO compensation package", "source": "FT"},
    {"company": "Tesla", "publishedAt": _d(13), "title": "Tesla factory in Germany faces protests over water extraction permits", "source": "Guardian"},
    {"company": "Tesla", "publishedAt": _d(17), "title": "Tesla diversity lawsuit settled for $3.2m over racial discrimination claims", "source": "WSJ"},
    {"company": "Tesla", "publishedAt": _d(23), "title": "Tesla Gigafactory achieves net-zero water usage certification", "source": "CNBC"},

    # ── Google ────────────────────────────────────────────────────────────────
    {"company": "Google", "publishedAt": _d(3),  "title": "Google data centre energy consumption rises 48% amid AI expansion", "source": "FT"},
    {"company": "Google", "publishedAt": _d(6),  "title": "Google agrees to $391m settlement over deceptive location tracking", "source": "Reuters"},
    {"company": "Google", "publishedAt": _d(10), "title": "Google employees protest Project Nimbus military cloud contract", "source": "Guardian"},
    {"company": "Google", "publishedAt": _d(15), "title": "Google achieves 24/7 carbon-free energy milestone at 10 campuses", "source": "Bloomberg"},
    {"company": "Google", "publishedAt": _d(19), "title": "EU fines Google €2.4bn for Shopping search result manipulation", "source": "BBC"},
    {"company": "Google", "publishedAt": _d(24), "title": "Google launches $200m fund to retrain workers displaced by AI automation", "source": "CNBC"},

    # ── Meta ──────────────────────────────────────────────────────────────────
    {"company": "Meta", "publishedAt": _d(1),  "title": "Meta fined $1.3bn over illegal transfer of EU user data to US", "source": "Reuters"},
    {"company": "Meta", "publishedAt": _d(4),  "title": "Meta accused of fuelling misinformation around climate denial content", "source": "Guardian"},
    {"company": "Meta", "publishedAt": _d(8),  "title": "Meta lays off 11,000 employees in second round of cuts this year", "source": "FT"},
    {"company": "Meta", "publishedAt": _d(12), "title": "Meta announces new teen safety restrictions across Instagram platform", "source": "BBC"},
    {"company": "Meta", "publishedAt": _d(17), "title": "Meta board resists calls for independent audit on content moderation", "source": "WSJ"},
    {"company": "Meta", "publishedAt": _d(22), "title": "Meta data centres powered by 100% renewable energy in Europe", "source": "Bloomberg"},

    # ── ExxonMobil ────────────────────────────────────────────────────────────
    {"company": "ExxonMobil", "publishedAt": _d(2),  "title": "ExxonMobil sued by California for decades of climate change deception", "source": "Reuters"},
    {"company": "ExxonMobil", "publishedAt": _d(5),  "title": "ExxonMobil methane emissions found 70% higher than self-reported", "source": "Science"},
    {"company": "ExxonMobil", "publishedAt": _d(9),  "title": "ExxonMobil shareholder vote rejects climate-aligned board nominees", "source": "FT"},
    {"company": "ExxonMobil", "publishedAt": _d(14), "title": "ExxonMobil announces carbon capture facility in Texas Gulf Coast", "source": "Bloomberg"},
    {"company": "ExxonMobil", "publishedAt": _d(20), "title": "ExxonMobil workers in refinery strike over safety conditions", "source": "Reuters"},
    {"company": "ExxonMobil", "publishedAt": _d(27), "title": "ExxonMobil reports 22% rise in offshore spill incidents this quarter", "source": "Guardian"},

    # ── JPMorgan ──────────────────────────────────────────────────────────────
    {"company": "JPMorgan", "publishedAt": _d(3),  "title": "JPMorgan still largest funder of fossil fuel expansion globally in 2024", "source": "Guardian"},
    {"company": "JPMorgan", "publishedAt": _d(7),  "title": "JPMorgan agrees to $290m settlement in Epstein victim lawsuit", "source": "Reuters"},
    {"company": "JPMorgan", "publishedAt": _d(11), "title": "JPMorgan board votes to retain CEO Jamie Dimon after shareholder pressure", "source": "FT"},
    {"company": "JPMorgan", "publishedAt": _d(16), "title": "JPMorgan pledges $2.5 trillion in sustainable development financing by 2030", "source": "Bloomberg"},
    {"company": "JPMorgan", "publishedAt": _d(21), "title": "JPMorgan accused of discriminatory mortgage lending practices in report", "source": "WSJ"},

    # ── Walmart ───────────────────────────────────────────────────────────────
    {"company": "Walmart", "publishedAt": _d(2),  "title": "Walmart supply chain audit reveals child labour at three Asian factories", "source": "Reuters"},
    {"company": "Walmart", "publishedAt": _d(6),  "title": "Walmart achieves zero waste to landfill goal at 75% of US stores", "source": "Bloomberg"},
    {"company": "Walmart", "publishedAt": _d(10), "title": "Walmart workers demand union recognition at Southern distribution centres", "source": "Guardian"},
    {"company": "Walmart", "publishedAt": _d(15), "title": "Walmart commits to electric truck fleet for last-mile delivery by 2035", "source": "CNBC"},
    {"company": "Walmart", "publishedAt": _d(20), "title": "Walmart board member resigns over executive pay governance dispute", "source": "FT"},

    # ── Nike ──────────────────────────────────────────────────────────────────
    {"company": "Nike", "publishedAt": _d(1),  "title": "Nike sued for greenwashing over 'Move to Zero' sustainability claims", "source": "Reuters"},
    {"company": "Nike", "publishedAt": _d(5),  "title": "Nike supplier in Vietnam faces wage theft allegations from workers", "source": "Guardian"},
    {"company": "Nike", "publishedAt": _d(9),  "title": "Nike releases most transparent supply chain audit in company history", "source": "Bloomberg"},
    {"company": "Nike", "publishedAt": _d(14), "title": "Nike recycled material line diverts 9 million plastic bottles from landfill", "source": "CNBC"},
    {"company": "Nike", "publishedAt": _d(19), "title": "Nike gender pay gap report shows 18% disparity at executive level", "source": "FT"},
    {"company": "Nike", "publishedAt": _d(25), "title": "Nike co-founder faces insider trading probe from SEC", "source": "WSJ"},

    # ── Goldman Sachs ─────────────────────────────────────────────────────────
    {"company": "Goldman Sachs", "publishedAt": _d(3),  "title": "Goldman Sachs accused of misleading investors in ESG fund disclosures", "source": "FT"},
    {"company": "Goldman Sachs", "publishedAt": _d(7),  "title": "Goldman Sachs 1MDB scandal settlement totals $2.9bn in new filings", "source": "Reuters"},
    {"company": "Goldman Sachs", "publishedAt": _d(12), "title": "Goldman Sachs launches $1bn clean energy transition fund for emerging markets", "source": "Bloomberg"},
    {"company": "Goldman Sachs", "publishedAt": _d(18), "title": "Goldman Sachs gender diversity targets missed for third consecutive year", "source": "WSJ"},
    {"company": "Goldman Sachs", "publishedAt": _d(24), "title": "Goldman Sachs board rejects shareholder proposal for CEO pay cap", "source": "CNBC"},

    # ── Chevron ───────────────────────────────────────────────────────────────
    {"company": "Chevron", "publishedAt": _d(2),  "title": "Chevron loses appeal in $9.5bn Ecuador environmental liability case", "source": "Reuters"},
    {"company": "Chevron", "publishedAt": _d(6),  "title": "Chevron methane flaring increases 35% year-on-year in Permian Basin", "source": "Guardian"},
    {"company": "Chevron", "publishedAt": _d(11), "title": "Chevron unveils hydrogen energy investment plan worth $5bn", "source": "Bloomberg"},
    {"company": "Chevron", "publishedAt": _d(17), "title": "Chevron safety record shows 12% reduction in recordable incidents", "source": "CNBC"},

    # ── Bank of America ───────────────────────────────────────────────────────
    {"company": "Bank of America", "publishedAt": _d(4),  "title": "Bank of America commits to net-zero financed emissions by 2050", "source": "Bloomberg"},
    {"company": "Bank of America", "publishedAt": _d(9),  "title": "Bank of America fined $250m for junk fees and misuse of customer funds", "source": "Reuters"},
    {"company": "Bank of America", "publishedAt": _d(15), "title": "Bank of America diversity programme doubles minority-owned supplier spend", "source": "CNBC"},
    {"company": "Bank of America", "publishedAt": _d(22), "title": "Bank of America board faces pressure over fossil fuel lending portfolio", "source": "Guardian"},

    # ── Coca-Cola ─────────────────────────────────────────────────────────────
    {"company": "Coca-Cola", "publishedAt": _d(3),  "title": "Coca-Cola named world's largest plastic polluter for sixth year running", "source": "Guardian"},
    {"company": "Coca-Cola", "publishedAt": _d(8),  "title": "Coca-Cola water replenishment targets missed in water-stressed regions", "source": "Reuters"},
    {"company": "Coca-Cola", "publishedAt": _d(13), "title": "Coca-Cola pledges 25% recycled material in all packaging by 2025", "source": "Bloomberg"},
    {"company": "Coca-Cola", "publishedAt": _d(19), "title": "Coca-Cola workers in Philippines strike over collective bargaining violation", "source": "FT"},
    {"company": "Coca-Cola", "publishedAt": _d(25), "title": "Coca-Cola executive pay ratio reaches 1,300:1 against median worker salary", "source": "WSJ"},

    # ── Boeing ────────────────────────────────────────────────────────────────
    {"company": "Boeing", "publishedAt": _d(1),  "title": "Boeing 737 MAX production halted after door plug safety failures found", "source": "Reuters"},
    {"company": "Boeing", "publishedAt": _d(5),  "title": "Boeing whistleblower alleges systematic suppression of safety complaints", "source": "Guardian"},
    {"company": "Boeing", "publishedAt": _d(10), "title": "Boeing CEO testifies before Senate on quality control failure culture", "source": "FT"},
    {"company": "Boeing", "publishedAt": _d(16), "title": "Boeing reaches $2.5bn DOJ settlement over 737 MAX fraud charges", "source": "Bloomberg"},
    {"company": "Boeing", "publishedAt": _d(22), "title": "Boeing Sustainable Aviation Fuel investment reaches $100m milestone", "source": "CNBC"},

    # ── Ford ──────────────────────────────────────────────────────────────────
    {"company": "Ford", "publishedAt": _d(2),  "title": "Ford recalls 870,000 F-150 pickups over fuel system fire risk", "source": "Reuters"},
    {"company": "Ford", "publishedAt": _d(7),  "title": "Ford EV transition reduces lifecycle emissions by 40% vs ICE models", "source": "Bloomberg"},
    {"company": "Ford", "publishedAt": _d(13), "title": "Ford union contract guarantees 11% pay rise for 45,000 workers", "source": "CNBC"},
    {"company": "Ford", "publishedAt": _d(19), "title": "Ford battery plant partnership raises concerns over labour conditions", "source": "Guardian"},
    {"company": "Ford", "publishedAt": _d(26), "title": "Ford board approves $50bn EV investment plan with independent oversight", "source": "FT"},

    # ── General Motors ────────────────────────────────────────────────────────
    {"company": "General Motors", "publishedAt": _d(3),  "title": "General Motors delays EV production targets amid battery supply issues", "source": "Reuters"},
    {"company": "General Motors", "publishedAt": _d(8),  "title": "General Motors achieves carbon-neutral manufacturing in three plants", "source": "Bloomberg"},
    {"company": "General Motors", "publishedAt": _d(14), "title": "General Motors sued over Chevrolet Bolt battery fire safety failures", "source": "FT"},
    {"company": "General Motors", "publishedAt": _d(20), "title": "General Motors workers ratify contract with 15% wage increase over 4 years", "source": "CNBC"},

    # ── McDonald's ────────────────────────────────────────────────────────────
    {"company": "McDonald's", "publishedAt": _d(4),  "title": "McDonald's sued for misleading packaging claims on sustainability", "source": "Reuters"},
    {"company": "McDonald's", "publishedAt": _d(9),  "title": "McDonald's franchise workers allege widespread sexual harassment", "source": "Guardian"},
    {"company": "McDonald's", "publishedAt": _d(15), "title": "McDonald's switches to 100% sustainably sourced beef in EU markets", "source": "Bloomberg"},
    {"company": "McDonald's", "publishedAt": _d(21), "title": "McDonald's raises minimum wage to $15 for all US company-owned stores", "source": "CNBC"},
    {"company": "McDonald's", "publishedAt": _d(27), "title": "McDonald's CEO exits amid board investigation into undisclosed relationships", "source": "FT"},

    # ── Starbucks ─────────────────────────────────────────────────────────────
    {"company": "Starbucks", "publishedAt": _d(2),  "title": "Starbucks illegally fired union organisers in New York, NLRB rules", "source": "Reuters"},
    {"company": "Starbucks", "publishedAt": _d(6),  "title": "Starbucks single-use cup waste increases 8% despite reusable programme", "source": "Guardian"},
    {"company": "Starbucks", "publishedAt": _d(11), "title": "Starbucks coffee sourcing certified 100% ethical under C.A.F.E Practices", "source": "Bloomberg"},
    {"company": "Starbucks", "publishedAt": _d(17), "title": "Starbucks CEO compensation rises 40% while barista wages stagnate", "source": "FT"},
    {"company": "Starbucks", "publishedAt": _d(23), "title": "Starbucks pledges to halve water use in manufacturing by 2030", "source": "CNBC"},

    # ── Pfizer ────────────────────────────────────────────────────────────────
    {"company": "Pfizer", "publishedAt": _d(3),  "title": "Pfizer vaccine pricing practices under Senate antitrust investigation", "source": "Reuters"},
    {"company": "Pfizer", "publishedAt": _d(8),  "title": "Pfizer achieves zero manufacturing waste to landfill at 12 global sites", "source": "Bloomberg"},
    {"company": "Pfizer", "publishedAt": _d(14), "title": "Pfizer accused of clinical trial misconduct in developing nations", "source": "Guardian"},
    {"company": "Pfizer", "publishedAt": _d(20), "title": "Pfizer commits $1bn to improve access to medicines in low-income countries", "source": "CNBC"},
    {"company": "Pfizer", "publishedAt": _d(26), "title": "Pfizer board elects first majority-independent director slate in history", "source": "FT"},

    # ── Shell ─────────────────────────────────────────────────────────────────
    {"company": "Shell", "publishedAt": _d(1),  "title": "Shell ordered by Dutch court to cut emissions 45% by 2030", "source": "Reuters"},
    {"company": "Shell", "publishedAt": _d(5),  "title": "Shell scraps short-term carbon emissions targets under investor pressure", "source": "FT"},
    {"company": "Shell", "publishedAt": _d(10), "title": "Shell Nigeria oil spill affects 50,000 residents in Delta communities", "source": "Guardian"},
    {"company": "Shell", "publishedAt": _d(16), "title": "Shell invests $5bn in offshore wind and hydrogen transition projects", "source": "Bloomberg"},
    {"company": "Shell", "publishedAt": _d(22), "title": "Shell CEO pay package draws shareholder revolt at AGM", "source": "FT"},
]

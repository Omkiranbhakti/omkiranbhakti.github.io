# Panchang + festival pages. Executed inside build.py's namespace (uses page, add, band, sec_head, video_cards, V, e, SITE ...).
import datetime as dt, json, os
from panchang import day_panchang, tithi_spans, tithi_name, lunar_month, moonrise, sunrise_sunset, to_ist, from_ist, EKADASHI_NAME, tithi_index
from fest_info import INFO, EKA_RULES, KATHA_FOR, AARTI_FOR
from festivals import find_dates, MONTHS_HI, RULES, tithi_at, MINOR_KEYS

IST_NOW = (dt.datetime.fromisoformat(os.environ["OKB_TODAY"] + "T06:00") if os.environ.get("OKB_TODAY") else dt.datetime.now(dt.timezone.utc).replace(tzinfo=None) + dt.timedelta(hours=5, minutes=30))
TODAY_D = IST_NOW.date()
R_START, R_END = dt.date(2026, 10, 1), dt.date(2027, 12, 31)
if TODAY_D < R_START: TODAY_D = R_START
WD = ["सोमवार","मंगलवार","बुधवार","गुरुवार","शुक्रवार","शनिवार","रविवार"]

def hdate(d): return f"{d.day} {MONTHS_HI[d.month]} {d.year}"
def hdate_w(d): return f"{d.day} {MONTHS_HI[d.month]} {d.year}, {WD[d.weekday()]}"
def t12(s):  # "HH:MM" -> "सुबह 6:21"
    h, m = map(int, s.split(":")); return hhmm(dt.datetime(2000,1,1,h,m))
def hhmm(t):
    h = t.hour
    part = "रात" if h < 4 else "सुबह" if h < 12 else "दोपहर" if h < 16 else "शाम" if h < 19 else "रात"
    return f"{part} {h % 12 or 12}:{t.minute:02d}"
def round5(t):
    m = (t.minute + 2) // 5 * 5
    return t.replace(second=0, microsecond=0, minute=0) + dt.timedelta(minutes=m)

# ---------- compute days ----------
DAYS = {}
d = R_START
while d <= R_END:
    DAYS[d] = day_panchang(d); d += dt.timedelta(days=1)

FEST = find_dates(R_START, R_END)
SPANS = tithi_spans(R_START - dt.timedelta(days=2), R_END + dt.timedelta(days=3))

WHEN = {"sunrise":"पूरे दिन — सुबह से","madhyahna":"पूजा: दोपहर में","aparahna":"पूजा: दोपहर बाद",
        "pradosh":"पूजा: शाम को","night":"पूजा: रात में, चाँद निकलने पर","nishita":"पूजा: आधी रात को"}

WHEN_S = {"sunrise":"सुबह से","madhyahna":"दोपहर में","aparahna":"दोपहर बाद","pradosh":"शाम को","night":"रात को चंद्रोदय पर","nishita":"आधी रात को"}

def kaal_window(day, kaal):
    p = DAYS.get(day) or day_panchang(day)
    sr = dt.datetime.combine(day, dt.time(*map(int, p["sunrise"].split(":"))))
    ss = dt.datetime.combine(day, dt.time(*map(int, p["sunset"].split(":"))))
    dl = ss - sr
    if kaal == "pradosh": return f"प्रदोष काल: {hhmm(ss)} से {hhmm(ss + dt.timedelta(minutes=144))} तक"
    if kaal == "madhyahna": return f"मध्याह्न: {hhmm(sr + dl*2/5)} से {hhmm(sr + dl*3/5)} तक"
    if kaal == "aparahna": return f"अपराह्न: {hhmm(sr + dl*3/5)} से {hhmm(sr + dl*4/5)} तक"
    if kaal == "sunrise": return f"सूर्योदय: {hhmm(sr)}"
    if kaal == "night":
        mr = moonrise(day)
        if not mr: return ""
        lo = mr.replace(second=0, microsecond=0, minute=mr.minute // 5 * 5)
        return f"चंद्रोदय: {hhmm(lo)} से {hhmm(lo + dt.timedelta(minutes=10))} के बीच (दिल्ली)"
    if kaal == "nishita":
        nxt = DAYS.get(day + dt.timedelta(days=1)) or day_panchang(day + dt.timedelta(days=1))
        sr2 = dt.datetime.combine(day + dt.timedelta(days=1), dt.time(*map(int, nxt["sunrise"].split(":"))))
        mid = ss + (sr2 - ss) / 2
        return f"निशीथ काल: {hhmm(mid - dt.timedelta(minutes=24))} से {hhmm(mid + dt.timedelta(minutes=24))} तक"
    return ""

# Ekadashi / Purnima / Amavasya observance days
def observance(tgt, kaal="sunrise"):
    out = []
    for i, s0, e0 in SPANS:
        if i != tgt: continue
        day, pick = s0.date(), None
        while day <= e0.date():
            if R_START <= day <= R_END and tithi_at(day, kaal)[0] == tgt: pick = day; break
            day += dt.timedelta(days=1)
        if pick is None: pick = s0.date() if s0.hour < 18 else s0.date() + dt.timedelta(days=1)
        if R_START <= pick <= R_END:
            am, pu, adhik = lunar_month(from_ist(s0 + (e0 - s0)/2))
            out.append((pick, s0, e0, pu, adhik))
    return out

EKA = []
for tgt, pk in ((10, "S"), (25, "K")):
    for pick, s0, e0, pu, adhik in observance(tgt):
        name = ("पद्मिनी" if pk == "S" else "परमा") if adhik else EKADASHI_NAME.get((pu, pk), "")
        nx = pick + dt.timedelta(days=1)
        EKA.append({"date": pick, "name": f"{name} एकादशी", "month": pu, "paksha": "शुक्ल" if pk=="S" else "कृष्ण",
                    "start": s0, "end": e0, "parana_from": DAYS.get(nx, day_panchang(nx))["sunrise"]})
EKA_KEY = {(m, pk): k for k, nm, m, pk, n, kl, off, mean in EKA_RULES}
EKA_KEY.update({("मार्गशीर्ष","S"): "gita-jayanti", ("कार्तिक","S"): "dev-uthani-ekadashi"})
EKA_RULE = {r[0]: r for r in EKA_RULES}
for x in EKA:
    x["key"] = EKA_KEY.get((x["month"], "S" if x["paksha"] == "शुक्ल" else "K")) if x["name"] not in ("पद्मिनी एकादशी", "परमा एकादशी") else None
    if x["key"] in EKA_RULE: x["name"] = EKA_RULE[x["key"]][1].split(" (")[0]
EKA.sort(key=lambda x: x["date"])
# Parana should end with dwadashi
for x in EKA:
    for i, s0, e0 in SPANS:
        if s0 >= x["end"] - dt.timedelta(minutes=1) and i in (11, 26): x["dwadashi_end"] = e0; break
PURNIMA = [(p, s0, e0, pu) for p, s0, e0, pu, a in observance(14)]
AMAVASYA = [(p, s0, e0, pu) for p, s0, e0, pu, a in observance(29)]

# day -> list of (name, when, url)
DAYFEST = {}
def addf(day, name, when, url):
    DAYFEST.setdefault(day, []).append((name, when, url))
for key, occ in FEST.items():
    for x in occ: addf(x["date"], x["name"], WHEN[x["kaal"]], f"{key}-kab-hai.html")
for x in EKA: addf(x["date"], x["name"], "सुबह से (व्रत)", f"{x['key']}-kab-hai.html" if x.get("key") else "ekadashi-2026-2027.html")
for p, s0, e0, pu in PURNIMA: addf(p, f"{pu} पूर्णिमा", "दिन भर", "purnima-amavasya-2026-2027.html")
for p, s0, e0, pu in AMAVASYA: addf(p, f"{pu} अमावस्या", "दिन भर", "purnima-amavasya-2026-2027.html")
for i, (yd, dd, nn, gg, vv) in enumerate(NDAYS):
    for y in yd.split(","):
        day = dt.date(int(y[:4]), int(y[4:6]), int(y[6:]))
        addf(day, f"नवरात्रि — {gg}", "दिन भर", "navratri-2026.html")

# ---------- month JSON for the live "today" card ----------
os.makedirs(os.path.join(ROOT, "panchang"), exist_ok=True)
by_month = {}
for day, p in DAYS.items():
    m = day.strftime("%Y-%m")
    q = dict(p); q["fest"] = DAYFEST.get(day, [])
    by_month.setdefault(m, {})[day.isoformat()] = q
for m, data in by_month.items():
    with open(os.path.join(ROOT, "panchang", f"{m}.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))

# ---------- shared today-card HTML ----------
def tithi_end_txt(p):
    if not p["tithi_end"]: return ""
    t = dt.datetime.strptime(p["tithi_end"], "%Y-%m-%d %H:%M")
    day = dt.date.fromisoformat(p["date"])
    when = "आज" if t.date() == day else "कल"
    return f"{when} {hhmm(t)} तक, फिर {p['next_tithi']}"

def today_card(p, compact=False):
    day = dt.date.fromisoformat(p["date"])
    fest = DAYFEST.get(day, [])
    fhtml = "".join(f'<li><a href="{u}">{e(n)}</a> <span>{e(w)}</span></li>' for n, w, u in fest) or '<li class="muted">आज कोई बड़ा त्योहार नहीं है</li>'
    adhik = " (अधिक मास)" if p["adhik"] else ""
    return f'''<div class="pcard" id="pcard" data-date="{p['date']}">
<div class="pc-head"><div><p class="pc-date"><span data-k="gdate">{hdate_w(day)}</span></p>
<h3 class="pc-tithi"><span data-k="tithi">{p['paksha']} पक्ष {p['tithi']}</span></h3>
<p class="pc-sub"><span data-k="month">{p['month_purnimanta']} मास{adhik}</span>, विक्रम संवत <span data-k="vs">{p['vs']}</span> · <span data-k="tend">{tithi_end_txt(p)}</span></p></div>
<button class="chip share" type="button" data-share>WhatsApp पर भेजें</button></div>
<dl class="pc-grid">
<div><dt>सूर्योदय / सूर्यास्त</dt><dd><span data-k="sunrise">{t12(p['sunrise'])}</span> / <span data-k="sunset">{t12(p['sunset'])}</span></dd></div>
<div><dt>नक्षत्र</dt><dd data-k="nak">{p['nakshatra']}</dd></div>
<div class="good"><dt>ब्रह्म मुहूर्त <small>ध्यान, जप, पढ़ाई के लिए सबसे अच्छा</small></dt><dd><span data-k="brahma">{t12(p['brahma'][0])} – {t12(p['brahma'][1])}</span></dd></div>
<div class="good"><dt>अभिजीत मुहूर्त <small>नया काम शुरू करने का शुभ समय</small></dt><dd><span data-k="abhijit">{t12(p['abhijit'][0])} – {t12(p['abhijit'][1])}{'' if p['abhijit_ok'] else ' (बुधवार को नहीं माना जाता)'}</span></dd></div>
<div class="bad"><dt>राहु काल <small>इस समय नया शुभ काम शुरू न करें</small></dt><dd><span data-k="rahu">{t12(p['rahu'][0])} – {t12(p['rahu'][1])}</span></dd></div>
<div><dt>प्रदोष काल <small>शाम की पूजा, दीपदान</small></dt><dd><span data-k="pradosh">{t12(p['pradosh'][0])} – {t12(p['pradosh'][1])}</span></dd></div>
</dl>
<div class="pc-fest"><h4>आज के व्रत और त्योहार</h4><ul data-k="fest">{fhtml}</ul></div>
<p class="pc-note">समय नई दिल्ली के हिसाब से हैं; दूसरे शहरों में कुछ मिनट का अंतर हो सकता है। <a href="aaj-ka-panchang.html">पूरा पंचांग और शब्दों का मतलब</a></p>
</div>'''

TODAY_P = DAYS[TODAY_D]

# ---------- upcoming festivals ----------
def upcoming(n=10, from_day=TODAY_D, majors_only=True):
    items = []
    for key, occ in FEST.items():
        if majors_only and key in MINOR_KEYS: continue
        for x in occ:
            if x["date"] >= from_day: items.append((x["date"], x["name"], f"{key}-kab-hai.html", WHEN[x["kaal"]]))
    if not majors_only:
        for x in EKA:
            if x["date"] >= from_day: items.append((x["date"], x["name"], f"{x['key']}-kab-hai.html" if x.get("key") else "ekadashi-2026-2027.html", "सुबह से (व्रत)"))
    items.sort()
    return items[:n]

MON_SHORT = {1:"जन",2:"फ़र",3:"मार्च",4:"अप्रै",5:"मई",6:"जून",7:"जुला",8:"अग",9:"सितं",10:"अक्टू",11:"नवं",12:"दिसं"}
def up_list(items):
    return '<ul class="ulist">' + "".join(
        f'<li><time datetime="{dd.isoformat()}"><b>{dd.day}</b><span>{MON_SHORT[dd.month]}</span></time><a href="{u}"><strong>{e(n)}</strong><span>{WD[dd.weekday()]} · {w}</span></a></li>'
        for dd, n, u, w in items) + '</ul>'

# ---------- Aaj ka panchang page ----------
week_rows = ""
for k in range(7):
    dd = TODAY_D + dt.timedelta(days=k)
    if dd > R_END: break
    p = DAYS[dd]; fs = ", ".join(n for n, w, u in DAYFEST.get(dd, []))
    week_rows += f"<tr><th scope=\"row\">{dd.day} {MONTHS_HI[dd.month]}<small>{WD[dd.weekday()]}</small></th><td>{p['paksha']} {p['tithi']}</td><td>{p['nakshatra']}</td><td>{e(fs) or '—'}</td></tr>"

GLOSS = [("तिथि","चंद्रमा के घटने-बढ़ने से बना हिंदू कैलेंडर का दिन। एक महीने में 30 तिथियाँ होती हैं, 15 शुक्ल पक्ष (चाँद बढ़ता है) और 15 कृष्ण पक्ष (चाँद घटता है) में। व्रत-त्योहार तिथि से तय होते हैं, तारीख़ से नहीं।"),
 ("उदया तिथि","सूर्योदय के समय जो तिथि चल रही हो, वही उस दिन की तिथि मानी जाती है। इसीलिए कभी-कभी एक तिथि दो दिन या एक भी दिन नहीं पड़ती।"),
 ("नक्षत्र","आकाश को 27 हिस्सों में बाँटा गया है, जिन्हें नक्षत्र कहते हैं। चंद्रमा जिस हिस्से में होता है, वह उस दिन का नक्षत्र है।"),
 ("ब्रह्म मुहूर्त","सूर्योदय से लगभग डेढ़ घंटा पहले का 48 मिनट का समय। ध्यान, जाप, पूजा और पढ़ाई के लिए सबसे उत्तम माना जाता है।"),
 ("अभिजीत मुहूर्त","दोपहर के बीच का लगभग 48 मिनट का समय, जिसे दिन का सबसे शुभ मुहूर्त माना जाता है। कोई नया काम शुरू करना हो और दूसरा मुहूर्त न मिले, तो यह लिया जाता है। बुधवार को इसे नहीं माना जाता।"),
 ("राहु काल","दिन का लगभग डेढ़ घंटे का हिस्सा, जो हर वार अलग समय पर आता है। इसमें नया या शुभ काम शुरू करने से बचा जाता है; रोज़ के काम चलते रहते हैं।"),
 ("प्रदोष काल","सूर्यास्त के बाद लगभग ढाई घंटे का समय। शिव पूजा, दीपदान और दिवाली-धनतेरस की पूजा इसी समय होती है।"),
 ("पूर्णिमांत मास","उत्तर भारत में महीना पूर्णिमा के अगले दिन से शुरू होता है। इसलिए कृष्ण पक्ष में उत्तर भारत का महीना, गुजरात-महाराष्ट्र के महीने से एक आगे होता है।")]
gloss_html = "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in GLOSS)
pfaq = [("आज कौन सी तिथि है?", f"{hdate_w(TODAY_D)} को सूर्योदय के समय {TODAY_P['paksha']} पक्ष की {TODAY_P['tithi']} तिथि है ({TODAY_P['month_purnimanta']} मास)। यह पेज हर दिन अपने आप बदल जाता है।"),
        ("राहु काल में क्या नहीं करना चाहिए?","राहु काल में नया काम, सौदा, यात्रा की शुरुआत या शुभ संस्कार शुरू करने से बचा जाता है। पहले से चल रहे काम इसमें किए जा सकते हैं।"),
        ("पंचांग किस शहर का है?","सभी समय नई दिल्ली के सूर्योदय-सूर्यास्त पर आधारित हैं। उत्तर भारत के दूसरे शहरों में कुछ मिनट का अंतर हो सकता है।")]
add("aaj-ka-panchang.html", f"आज का पंचांग — तिथि, शुभ मुहूर्त, राहु काल और त्योहार | OmKiran Bhakti",
 "आज का हिंदू पंचांग सरल हिंदी में: आज की तिथि, नक्षत्र, ब्रह्म मुहूर्त, अभिजीत मुहूर्त, राहु काल, सूर्योदय-सूर्यास्त और आज के व्रत-त्योहार। हर दिन अपने आप अपडेट।",
 f'''{band("आज का पंचांग", "आज की तिथि, शुभ मुहूर्त, राहु काल और व्रत-त्योहार, सरल भाषा में। यह पेज हर दिन अपने आप बदल जाता है।", "आज का पंचांग", *ART["vishnu"], "आज का पंचांग")}
<section><div class="wrap">{today_card(TODAY_P)}</div></section>
<section class="band"><div class="wrap">{sec_head("अगले 7 दिन")}<div class="tbl"><table class="ptable"><thead><tr><th>तारीख़</th><th>तिथि</th><th>नक्षत्र</th><th>व्रत / त्योहार</th></tr></thead><tbody>{week_rows}</tbody></table></div>
<p style="text-align:center;margin-top:1.5rem"><a class="btn" href="panchang-{TODAY_D.strftime('%Y-%m')}.html">{MONTHS_HI[TODAY_D.month]} {TODAY_D.year} का पूरा पंचांग</a></p></div></section>
<section><div class="wrap">{sec_head("आने वाले त्योहार")}{up_list(upcoming(8))}<p style="text-align:center;margin-top:1.5rem"><a class="btn ghost" href="tyohar-calendar.html">पूरा त्योहार कैलेंडर</a></p></div></section>
<section class="band"><div class="wrap prose">{sec_head("पंचांग के शब्दों का आसान मतलब")}<dl class="gloss">{gloss_html}</dl></div></section>
{faq_html(pfaq)}''', crumbs="आज का पंचांग", active="aaj-ka-panchang.html", ld=[faq_ld(pfaq)])

# ---------- Monthly pages ----------
months = sorted(by_month)
for idx, m in enumerate(months):
    y, mo = map(int, m.split("-"))
    rows = ""
    for day in sorted(dt.date.fromisoformat(k) for k in by_month[m]):
        p = DAYS[day]; fs = DAYFEST.get(day, [])
        fl = ", ".join(f'<a href="{u}">{e(n)}</a>' for n, w, u in fs)
        cls = ' class="has-f"' if fs else ""
        rows += f"<tr{cls}><th scope=\"row\">{day.day}<small>{WD[day.weekday()][:-1] if False else WD[day.weekday()]}</small></th><td>{p['paksha']} {p['tithi']}<small>{p['month_purnimanta']}</small></td><td>{p['nakshatra']}</td><td>{t12(p['sunrise'])}</td><td>{fl or '—'}</td></tr>"
    flist = [(dd, n, u, w) for dd in sorted(DAYFEST) if dd.year == y and dd.month == mo for n, w, u in DAYFEST[dd] if "कब-है" in u or u.endswith("kab-hai.html")]
    prev_l = f'<a href="panchang-{months[idx-1]}.html">← {MONTHS_HI[int(months[idx-1][5:])]} {months[idx-1][:4]}</a>' if idx > 0 else "<span></span>"
    next_l = f'<a href="panchang-{months[idx+1]}.html">{MONTHS_HI[int(months[idx+1][5:])]} {months[idx+1][:4]} →</a>' if idx < len(months)-1 else "<span></span>"
    mname = f"{MONTHS_HI[mo]} {y}"
    eks = [x for x in EKA if x["date"].year == y and x["date"].month == mo]
    ans = f"{mname} में " + (", ".join(f"{n} ({dd.day} {MONTHS_HI[mo]})" for dd, n, u, w in flist[:6]) + " प्रमुख त्योहार हैं।" if flist else "कोई बड़ा त्योहार नहीं है।")
    if eks: ans += " एकादशी: " + ", ".join(f"{x['date'].day} {MONTHS_HI[mo]} ({x['name']})" for x in eks) + "।"
    add(f"panchang-{m}.html", f"{mname} पंचांग — रोज़ की तिथि, व्रत और त्योहार | OmKiran Bhakti",
        f"{mname} का पूरा हिंदू पंचांग: हर दिन की तिथि, नक्षत्र, सूर्योदय और व्रत-त्योहार। {('प्रमुख: ' + ', '.join(n for _, n, _, _ in flist[:4])) if flist else ''}"[:158],
        f'''{band(f"{mname} का पंचांग", ans, f"{mname} पंचांग", *ART["vishnu"], mname)}
<section><div class="wrap"><nav class="mnav">{prev_l}<a href="aaj-ka-panchang.html">आज का पंचांग</a>{next_l}</nav>
<div class="tbl"><table class="ptable"><thead><tr><th>तारीख़</th><th>तिथि (मास)</th><th>नक्षत्र</th><th>सूर्योदय</th><th>व्रत / त्योहार</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="pc-note">तिथि सूर्योदय के समय की है (उदया तिथि), नई दिल्ली के अनुसार।</p></div></section>''',
        crumbs=f"{mname} पंचांग", active="aaj-ka-panchang.html")

def info_html(key, base):
    inf = INFO.get(key)
    aar = "".join(f'<p class="lede">🪔 <a href="{h}"><strong>{t}</strong></a> — {sb}</p>' for h, t, sb in AARTI_FOR.get(key, []))
    if not inf:
        kat = (f'<p class="lede">📖 <a href="{KATHA_FOR[key]}"><strong>{base} की कथा पढ़ें</strong></a> — सरल हिंदी में</p>') if key in KATHA_FOR else ""
        return f'<section><div class="wrap">{kat}{aar}</div></section>' if (kat or aar) else ""
    out = '<section><div class="wrap">' + sec_head(f"{base} का महत्व")
    if key in KATHA_FOR: out += f'<p class="lede">📖 <a href="{KATHA_FOR[key]}"><strong>{base} की कथा पढ़ें</strong></a> — सरल हिंदी में</p>'
    out += aar
    if inf.get("region"): out += f'<p class="lede"><strong>कहाँ मनाया जाता है:</strong> {e(inf["region"])}</p>'
    out += "".join(f'<p class="answer">{e(t)}</p>' for t in inf.get("mahatva", []))
    if inf.get("vidhi"):
        out += sec_head(f"{base} की पूजा विधि") + '<ol class="steps">' + "".join(f"<li>{e(v)}</li>" for v in inf["vidhi"]) + "</ol>"
    return out + "</div></section>"

# ---------- Festival 'kab hai' pages ----------
FVID = {"karwa-chauth":["oQl6-dRDfWU","w8pxctA2998"],"diwali":["F95csn49Rq0","KPZbsWemcIg"],"dhanteras":["F95csn49Rq0"],
 "ganesh-chaturthi":["ZswQ9qUMDTs","NGI-JiRiwSc","Qpe4rrfzWhk"],"anant-chaturdashi":["lMHZDM-RRb4","5WeumLCpi5w"],
 "janmashtami":["vy6ucthmxmk","ZIhDdYk6Gus","ZQ_OBR-596M"],"holi":["3ChBJC1Vigk","Potbxr2V0jI","oXTPb9esaQ8"],"holika-dahan":["3ChBJC1Vigk"],
 "chhath-puja":["M5_SEzyH_b4"],"dev-uthani-ekadashi":["hwoEYtPy7Qw"],"maha-shivratri":["sllSUVgfjnw","rxeMNQ48yWU","ZqFztNyxSgU"],
 "sharadiya-navratri":["G99-49Pfs6U","woNhYRu376g"],"chaitra-navratri":["G99-49Pfs6U","Fxfm-eadkTY"],"ram-navami":["pCixItfj5Vo","sLQF1nm_RqU"],
 "hanuman-jayanti":["707iS1Iyv-E","W__UjJxgK_o"],"dussehra":["pCixItfj5Vo","ZqOnkb7zElU"],"guru-purnima":["96GJOWJFJgA"],
 "vivah-panchami":["sLQF1nm_RqU"],"govardhan-puja":["TVdX5XbbjHs"],"kartik-purnima":["ZqFztNyxSgU"],"gita-jayanti":["uCUR842niAU"],
 "sharad-purnima":["KPZbsWemcIg"],"akshaya-tritiya":["F95csn49Rq0"],"narak-chaturdashi":["KPZbsWemcIg"],"vasant-panchami":["Fxfm-eadkTY"]}
_K, _M, _S, _G, _V, _N = ("uCUR842niAU",12), ("2yVR5zSaKpc",76), ("Kbe3pbLsg1U",80), ("NGI-JiRiwSc",80), ("pCixItfj5Vo",80), ("G99-49Pfs6U",50)
FART_MINOR = {"govatsa-dwadashi":_K,"gopashtami":_K,"jagannath-rath-yatra":_K,"hal-shashthi":_K,"rang-panchami":("3ChBJC1Vigk",50),
 "chhath-nahay-khay":("ktQUU5Y3tPE",50),"chhath-kharna":("ktQUU5Y3tPE",50),"chhath-usha-arghya":("ktQUU5Y3tPE",50),"ratha-saptami":("ktQUU5Y3tPE",50),
 "tulsi-vivah":("hwoEYtPy7Qw",50),"vaikunth-chaturdashi":_S,"sawan-start":_S,"nag-panchami":_S,"kaal-bhairav-jayanti":("unfGUJz6D8U",78),
 "sakat-chauth":_G,"shani-jayanti":("gZ7DoH6ZOa4",50),"radha-ashtami":("R1PiCmntXIM",50),"sita-navami":_V,
 "sheetala-ashtami":_M,"gangaur":_M,"vat-savitri":_M,"hariyali-teej":_M,"kajari-teej":_M,"hartalika-teej":_M,
 "hindu-nav-varsh":_N,"mauni-amavasya":_N,"magh-purnima":_N,"ganga-dussehra":_N}
FART = {"karwa-chauth":("oQl6-dRDfWU",36),"diwali":("F95csn49Rq0",72),"dhanteras":("F95csn49Rq0",72),"sharad-purnima":("F95csn49Rq0",72),"ganesh-chaturthi":ART["ganesh"],"janmashtami":ART["krishna"],
 "holi":("3ChBJC1Vigk",50),"maha-shivratri":ART["shiv"],"ram-navami":ART["ram"],"hanuman-jayanti":ART["hanuman"],"dussehra":ART["ram"],
 "sharadiya-navratri":ART["navdurga"],"chaitra-navratri":ART["navdurga"]}

# ---------- extra blocks on every festival page (why this date, year table, do/don't, wishes, series) ----------
from fest_extra import DOS, wishes_for, SERIES, YEARS_SKIP
from festivals import target_index
import urllib.parse as _up
try: FYEARS = json.load(open(os.path.join(os.path.dirname(__file__), "fest_years.json")))
except Exception: FYEARS = {}
KAAL_W = {"sunrise": "सूर्योदय", "pradosh": "प्रदोष काल (शाम)", "night": "चंद्रोदय (रात)", "nishita": "आधी रात (निशीथ काल)",
          "madhyahna": "दोपहर (मध्याह्न)", "aparahna": "अपराह्न (दोपहर बाद)"}
def _dm(t): return f"{t.day} {MONTHS_HI[t.month]}, {hhmm(t)}"
def why_date_html(key, base, x, kaal, off, paksha, n, tname, rule_txt):
    if off or x.get("note"): return ""
    tgt = target_index(paksha, n); s0, e0, D = x["tithi_start"], x["tithi_end"], x["date"]
    lines = [f"{tname} तिथि {_dm(s0)} से {_dm(e0)} तक है।", rule_txt]
    day = s0.date(); kw = KAAL_W[kaal]
    while day <= e0.date():
        ti, mo = tithi_at(day, kaal); mt = to_ist(mo)
        if day == D:
            if ti == tgt: lines.append(f"{hdate_w(D)} को {kw} के समय ({hhmm(mt)}) यही तिथि है — इसलिए {base} इसी दिन है।")
            else: lines.append(f"इस बार {kw} के समय यह तिथि किसी भी दिन नहीं पड़ती (तिथि का क्षय), इसलिए जिस दिन तिथि शुरू होती है, वही दिन लिया गया है।")
        elif ti == tgt:
            lines.append(f"{hdate(day)} को भी {kw} के समय यह तिथि है, लेकिन नियम के अनुसार पहला दिन लिया जाता है।")
        else:
            lines.append(f"{hdate(day)} को {kw} के समय ({hhmm(mt)}) यह तिथि " + ("अभी शुरू नहीं हुई होती" if mt < s0 else "खत्म हो चुकी होती है") + "।")
        day += dt.timedelta(days=1)
    return (f'<section><div class="wrap">{sec_head(f"{base} {D.year} इसी तारीख़ को क्यों?", "तिथि का नियम, आसान भाषा में")}'
            + "".join(f'<p class="answer">{e(l)}</p>' for l in lines) + '</div></section>')
def years_html(key, base):
    ys = FYEARS.get(key)
    if not ys or key in YEARS_SKIP: return ""
    rows = "".join(f'<tr><th scope="row">{d[:4]}</th><td>{hdate_w(dt.date.fromisoformat(d))}</td></tr>' for d in ys)
    return (f'<section><div class="wrap">{sec_head(f"{base} {ys[0][:4]} से {ys[-1][:4]} तक — हर साल की तारीख़", "नई दिल्ली के पंचांग से निकाली गई")}'
            f'<div class="tbl"><table class="ptable"><thead><tr><th>साल</th><th>तारीख़</th></tr></thead><tbody>{rows}</tbody></table></div></div></section>')
def years_faq(key, base, nyear):
    ys = {int(d[:4]): dt.date.fromisoformat(d) for d in FYEARS.get(key, [])} if key not in YEARS_SKIP else {}
    out = []
    if nyear - 1 in ys: out.append((f"{base} {nyear-1} की तारीख़ क्या थी?", f"{hdate_w(ys[nyear-1])}।"))
    if nyear + 2 in ys: out.append((f"{base} {nyear+2} की तारीख़ क्या है?", f"{hdate_w(ys[nyear+2])}।"))
    return out
def dos_html(key, base):
    if key not in DOS: return ""
    do, dont = DOS[key]; li = lambda a: '<ul class="chk">' + "".join(f"<li>{e(v)}</li>" for v in a) + "</ul>"
    return (f'<section data-hi-only><div class="wrap">{sec_head(f"{base} पर क्या करें, क्या न करें")}<div class="dd-grid">'
            f'<div class="dd do"><h2>✅ क्या करें</h2>{li(do)}</div><div class="dd dont"><h2>❌ क्या न करें</h2>{li(dont)}</div></div></div></section>')
def wishes_html(key, base, url):
    cards = ""
    for w in wishes_for(key, base):
        wa = "https://wa.me/?text=" + _up.quote(w + "\n\n" + url)
        cards += (f'<div class="sg wish"><p>{e(w)}</p><p class="wish-b"><button type="button" class="btn ghost wcp" data-t="{e(w)}">📋 कॉपी करें</button> '
                  f'<a class="btn ghost" href="{wa}" target="_blank" rel="noopener nofollow">WhatsApp पर भेजें</a></p></div>')
    return (f'<section class="band" data-hi-only><div class="wrap">{sec_head(f"{base} की शुभकामनाएँ", "कॉपी करें या सीधे WhatsApp पर भेजें")}<div class="sg-grid">{cards}</div></div>'
            '<script>document.addEventListener("click",function(ev){var b=ev.target.closest&&ev.target.closest(".wcp");if(!b)return;'
            'var t=b.getAttribute("data-t");(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){b.textContent="✓ कॉपी हो गया"},function(){b.textContent="✕ दोबारा कोशिश करें"});});</script></section>')
_RNAME = {r[0]: r[1].split(" (")[0] for r in RULES}
def series_html(key):
    for title, keys in SERIES:
        if key not in keys: continue
        items = []
        for k in keys:
            if k.startswith("@"):
                u, nm = k[1:].split("|"); d = None
            else:
                u, nm = f"{k}-kab-hai.html", _RNAME.get(k, k)
                x = next((y for y in FEST.get(k, []) if y["date"] >= TODAY_D - dt.timedelta(days=3)), None); d = x["date"] if x else None
            cur = ' aria-current="page" class="cur"' if k == key else ""
            items.append(f'<li><a href="{u}"{cur}><strong>{e(nm)}</strong>{("<span>" + hdate_w(d) + "</span>") if d else ""}</a></li>')
        return f'<section><div class="wrap">{sec_head(title)}<ol class="fseries">{"".join(items)}</ol></div></section>'
    return ""

TODAY_KEYS = []
for key, name, month, paksha, n, kaal, off, meaning in RULES:
    occ = FEST.get(key, [])
    if not occ: continue
    nxt = next((x for x in occ if x["date"] >= TODAY_D), occ[-1])
    base = name.split(" (")[0]
    alias = name.split(" (")[1].rstrip(")") if " (" in name else ""
    yrs = " / ".join(str(y) for y in sorted({x["date"].year for x in occ}))
    rows = ""
    for x in occ:
        obs_day = x["date"] - dt.timedelta(days=off)
        rows += (f"<tr><th scope=\"row\">{x['date'].year}</th><td><strong>{hdate_w(x['date'])}</strong>{('<small>'+e(x['note'])+'</small>') if x['note'] else ''}</td>"
                 f"<td>{hhmm(x['tithi_start'])}, {x['tithi_start'].day} {MONTHS_HI[x['tithi_start'].month]} से<br>{hhmm(x['tithi_end'])}, {x['tithi_end'].day} {MONTHS_HI[x['tithi_end'].month]} तक</td>"
                 f"<td>{kaal_window(obs_day, kaal) if not off else 'होलिका दहन के अगले दिन'}</td></tr>")
    pk = "शुक्ल" if paksha == "S" else "कृष्ण"
    tname = "पूर्णिमा" if n == 15 else "अमावस्या" if n == 30 else TITHI_HI[n-1]
    _ek = next((x for x in EKA if x.get("key") == key and x["date"] == nxt["date"]), None)
    ans = (f"{base} {nxt['date'].year} में <strong>{hdate_w(nxt['date'])}</strong> को है"
           + (f" ({e(nxt['note'])})" if nxt['note'] else "") + (f"। यह {month} मास के {pk} पक्ष की एकादशी है। व्रत का पारण {(nxt['date']+dt.timedelta(days=1)).day} {MONTHS_HI[(nxt['date']+dt.timedelta(days=1)).month]} को {t12(_ek['parana_from'])} के बाद करें।" if _ek else f"। यह {month} मास के {pk} पक्ष की {tname} तिथि को {WHEN_S[kaal]} मनाया जाता है।"))
    why = {"sunrise":"जिस दिन सूर्योदय के समय यह तिथि हो, उसी दिन त्योहार मनाया जाता है।",
           "pradosh":"इसकी पूजा प्रदोष काल (सूर्यास्त के बाद) में होती है, इसलिए वह दिन लिया जाता है जिस शाम यह तिथि हो।",
           "night":"इसमें चंद्रमा का महत्व है, इसलिए वह दिन लिया जाता है जिस रात चंद्रोदय के समय यह तिथि हो।",
           "nishita":"इसकी मुख्य पूजा आधी रात (निशीथ काल) में होती है, इसलिए वह रात ली जाती है जिसमें यह तिथि हो।",
           "madhyahna":"इसकी पूजा दोपहर (मध्याह्न) में होती है, इसलिए वह दिन लिया जाता है जिसकी दोपहर में यह तिथि हो।",
           "aparahna":"इसकी पूजा दोपहर बाद (अपराह्न) में होती है।"}[kaal]
    vids = [v for v in FVID.get(key, []) if v in V]
    ffaq = [(f"{base} {nxt['date'].year} कब है?", re.sub('<[^>]+>','',ans)),
            (f"{base} किस तिथि को मनाया जाता है?", f"{month} मास, {pk} पक्ष, {tname}। {why}"),
            (f"{base} का महत्व क्या है?", meaning + "।")] + list(INFO.get(key, {}).get("faq", []))
    ffaq += years_faq(key, base, nxt["date"].year)
    _en = INFO.get(key, {}).get("en", "")
    if _en: ffaq.append((f"{_en.split(' / ')[0]} {nxt['date'].year} date?", f"{_en.split(' / ')[0]} {nxt['date'].year}: {nxt['date'].strftime('%d %B %Y')} ({hdate_w(nxt['date'])})."))
    fart = FART.get(key) or FART_MINOR.get(key, ART["vishnu"])
    _t = f"{base} ({alias}) {yrs} कब है? तारीख़, तिथि और शुभ समय | OmKiran Bhakti" if alias else ""
    if _t and len(_t) > 95: _t = f"{base} ({alias}) {yrs} कब है? तारीख़ और तिथि | OmKiran Bhakti"
    if not _t or len(_t) > 95: _t = f"{base} {yrs} कब है? तारीख़, तिथि और शुभ समय | OmKiran Bhakti"
    if _en and len(_t) + len(_en.split(" / ")[0]) < 105: _t = _t.replace(" | OmKiran", f" ({_en.split(' / ')[0]}) | OmKiran")
    add(f"{key}-kab-hai.html", _t,
        f"{base} {nxt['date'].year}: {hdate_w(nxt['date'])}। {month} {pk} {tname} — तिथि शुरू और समाप्त होने का समय, पूजा का समय (दिल्ली) और महत्व।"[:160],
        f'''{band(f"{base} कब है?", ans, base, *fart, base)}
<section><div class="wrap">{sec_head(f"{base}: तारीख़ और समय")}<div class="tbl"><table class="ptable"><thead><tr><th>साल</th><th>तारीख़</th><th>तिथि ({pk} {tname})</th><th>पूजा का समय (नई दिल्ली)</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="answer" style="margin-top:1.5rem">{e(meaning)}। {why}</p></div></section>
{why_date_html(key, base, nxt, kaal, off, paksha, n, tname, why)}
{series_html(key)}
{info_html(key, base)}
{dos_html(key, base)}
{wishes_html(key, base, SITE + key + "-kab-hai.html")}
{years_html(key, base)}
{('<section class="band"><div class="wrap">' + sec_head("सुनें और साथ गाएँ") + video_cards(vids) + '</div></section>') if vids else ''}
<section><div class="wrap">{sec_head("और त्योहार")}{up_list([u for u in upcoming(7) if u[2] != f"{key}-kab-hai.html"][:6])}</div></section>
{faq_html(ffaq)}''', crumbs=f"{base} कब है", active="tyohar-calendar.html",
        ld=[{"@type":"Event","name":f"{base} {x['date'].year}","startDate":x["date"].isoformat(),"endDate":x["date"].isoformat(),
             "eventAttendanceMode":"https://schema.org/OfflineEventAttendanceMode","eventStatus":"https://schema.org/EventScheduled",
             "location":{"@type":"Place","name":"भारत","address":{"@type":"PostalAddress","addressCountry":"IN"}},
             "description":meaning,"organizer":{"@id":SITE+"#organization"}} for x in occ] + [faq_ld(ffaq)])
    TODAY_KEYS.append((key, base))

# ---------- Festival calendar ----------
cal = ""
allf = sorted((x["date"], x["name"], f"{k}-kab-hai.html", WHEN[x["kaal"]]) for k, occ in FEST.items() for x in occ)
cur = None
for dd, n, u, w in allf:
    mk = (dd.year, dd.month)
    if mk != cur:
        if cur: cal += "</ul>"
        cal += f'<h3 class="cal-m">{MONTHS_HI[dd.month]} {dd.year}</h3><ul class="ulist">'; cur = mk
    cal += f'<li><time datetime="{dd.isoformat()}"><b>{dd.day}</b><span>{WD[dd.weekday()][:3]}</span></time><a href="{u}"><strong>{e(n)}</strong><span>{w}</span></a></li>'
cal += "</ul>"
add("tyohar-calendar.html", "हिंदू त्योहार कैलेंडर 2026–2027 — व्रत और त्योहारों की तारीख़ें | OmKiran Bhakti",
    "2026 और 2027 के सभी बड़े हिंदू व्रत-त्योहारों की तारीख़ें: दिवाली, करवा चौथ, छठ, होली, महाशिवरात्रि, रामनवमी, जन्माष्टमी, गणेश चतुर्थी, नवरात्रि और दशहरा।",
    f'''{band("त्योहार कैलेंडर 2026–2027","हर बड़े व्रत-त्योहार की तारीख़, और वह सुबह से मनाया जाएगा या शाम/रात को। हर त्योहार पर क्लिक करके तिथि का समय और पूजा मुहूर्त देखें।","त्योहार कैलेंडर",*ART["navdurga"],"त्योहार")}
<section><div class="wrap"><p style="text-align:center"><a class="btn ghost" href="ekadashi-2026-2027.html">सभी एकादशी</a> <a class="btn ghost" href="purnima-amavasya-2026-2027.html">पूर्णिमा और अमावस्या</a> <a class="btn ghost" href="lok-parv.html">राज्य के अनुसार लोक पर्व</a> <a class="btn ghost" href="vrat-katha.html">व्रत कथाएँ</a></p>{cal}</div></section>''',
    crumbs="त्योहार कैलेंडर", active="tyohar-calendar.html",
    ld=[{"@type":"ItemList","name":"हिंदू त्योहार 2026–2027","itemListElement":[{"@type":"ListItem","position":i+1,"url":SITE+u,"name":f"{n} — {dd.isoformat()}"} for i,(dd,n,u,w) in enumerate(allf)]}])

# ---------- Ekadashi list ----------
erows = ""
for x in EKA:
    dw = x.get("dwadashi_end")
    nx = x["date"] + dt.timedelta(days=1)
    par = f"{nx.day} {MONTHS_HI[nx.month]}: {t12(x['parana_from'])} के बाद" + (f", {hhmm(dw)} से पहले" if dw and dw.date() == nx else "")
    erows += (f"<tr><th scope=\"row\">{hdate_w(x['date'])}</th><td><strong>{('<a href="'+x['key']+'-kab-hai.html">'+e(x['name'])+'</a>') if x.get('key') else e(x['name'])}</strong><small>{x['month']} {x['paksha']} पक्ष</small></td>"
              f"<td>{hhmm(x['start'])}, {x['start'].day} {MONTHS_HI[x['start'].month]} से {hhmm(x['end'])}, {x['end'].day} {MONTHS_HI[x['end'].month]} तक</td><td>{par}</td></tr>")
nek = next((x for x in EKA if x["date"] >= TODAY_D), EKA[-1])
efaq = [("अगली एकादशी कब है?", f"अगली एकादशी {nek['name']} है, जो {hdate_w(nek['date'])} को है।"),
        ("एकादशी व्रत का पारण कब करें?","पारण अगले दिन (द्वादशी को) सूर्योदय के बाद और द्वादशी तिथि खत्म होने से पहले किया जाता है। हर एकादशी का पारण समय तालिका में दिया है।"),
        ("साल में कितनी एकादशी होती हैं?","हर महीने दो, यानी साल में 24 एकादशी। अधिक मास वाले साल में 26 होती हैं।")]
add("ekadashi-2026-2027.html", "एकादशी 2026–2027 — सभी एकादशी की तारीख़, नाम और पारण समय | OmKiran Bhakti",
    f"एकादशी व्रत 2026–2027 की पूरी सूची: हर एकादशी का नाम, तारीख़, तिथि शुरू-समाप्त होने का समय और पारण का समय (नई दिल्ली)। अगली एकादशी: {nek['name']}, {hdate(nek['date'])}।"[:160],
    f'''{band("एकादशी 2026–2027", f"अगली एकादशी <strong>{e(nek['name'])}</strong> है, जो <strong>{hdate_w(nek['date'])}</strong> को है। नीचे हर एकादशी का नाम, तिथि का समय और व्रत खोलने (पारण) का समय है।", "एकादशी", *ART["vishnu"], "एकादशी")}
<section><div class="wrap"><div class="tbl"><table class="ptable"><thead><tr><th>तारीख़</th><th>एकादशी</th><th>तिथि</th><th>पारण (व्रत खोलना)</th></tr></thead><tbody>{erows}</tbody></table></div>
<p class="pc-note">उदया तिथि के नियम से, नई दिल्ली के अनुसार। वैष्णव (इस्कॉन) परंपरा में कभी-कभी एकादशी अगले दिन मानी जाती है।</p></div></section>
<section class="band"><div class="wrap">{sec_head("एकादशी के भजन")}{video_cards([v for v in ["EE2zjTPyHaI","A-vFduFpIHg","GtRRHlLc5gQ","uCUR842niAU"] if v in V])}</div></section>
{faq_html(efaq)}''', crumbs="एकादशी", active="tyohar-calendar.html", ld=[faq_ld(efaq)])

# ---------- One page per named Ekadashi ----------
for key, name, month, paksha, n, kaal, off, meaning in EKA_RULES:
    occ = [x for x in EKA if x.get("key") == key]
    if not occ: continue
    base = name.split(" (")[0]; alias = name.split(" (")[1].rstrip(")") if " (" in name else ""
    nxt = next((x for x in occ if x["date"] >= TODAY_D), occ[-1])
    yrs = " / ".join(str(y) for y in sorted({x["date"].year for x in occ}))
    pk = "शुक्ल" if paksha == "S" else "कृष्ण"
    def _par(x):
        dw = x.get("dwadashi_end"); nx = x["date"] + dt.timedelta(days=1)
        return f"{nx.day} {MONTHS_HI[nx.month]}: {t12(x['parana_from'])} के बाद" + (f", {hhmm(dw)} से पहले" if dw and dw.date() == nx else "")
    rows = "".join(f"<tr><th scope=\"row\">{x['date'].year}</th><td><strong>{hdate_w(x['date'])}</strong></td>"
                   f"<td>{hhmm(x['start'])}, {x['start'].day} {MONTHS_HI[x['start'].month]} से<br>{hhmm(x['end'])}, {x['end'].day} {MONTHS_HI[x['end'].month]} तक</td><td>{_par(x)}</td></tr>" for x in occ)
    ans = (f"{base} {nxt['date'].year} में <strong>{hdate_w(nxt['date'])}</strong> को है। यह {month} मास के {pk} पक्ष की एकादशी है"
           + (f", जिसे {alias} भी कहते हैं" if alias else "") + f"। व्रत का पारण {_par(nxt)} करें।")
    inf = INFO.get(key, {}); en = inf.get("en", "").split(" / ")[0]
    others = [x for x in EKA if x["date"] >= TODAY_D and x.get("key") and x["key"] != key][:6]
    ffaq = [(f"{base} {nxt['date'].year} कब है?", re.sub("<[^>]+>", "", ans)),
            (f"{base} का पारण कब है?", f"{_par(nxt)} (नई दिल्ली)।"),
            (f"{base} का महत्व क्या है?", meaning + "। " + (inf.get("mahatva") or [""])[0])] + list(inf.get("faq", []))
    if en: ffaq.append((f"{en} {nxt['date'].year} date and parana time?", f"{en} {nxt['date'].year}: {nxt['date'].strftime('%d %B %Y')}. Parana (vrat kholna): {_par(nxt)} (New Delhi)."))
    _t = f"{base} {yrs} कब है? तारीख़, पारण समय और व्रत विधि ({en}) | OmKiran Bhakti"
    if len(_t) > 105: _t = f"{base} {yrs} कब है? तारीख़ और पारण समय ({en}) | OmKiran Bhakti"
    add(f"{key}-kab-hai.html", _t,
        f"{base} {nxt['date'].year}: {hdate_w(nxt['date'])}। पारण {_par(nxt)}। {meaning}, व्रत विधि, कथा और नियम।"[:160],
        f'''{band(f"{base} कब है?", ans, base, *ART["vishnu"], base)}
<section><div class="wrap">{sec_head(f"{base}: तारीख़ और पारण समय")}<div class="tbl"><table class="ptable"><thead><tr><th>साल</th><th>तारीख़</th><th>एकादशी तिथि</th><th>पारण (व्रत खोलना)</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="pc-note">उदया तिथि के नियम से, नई दिल्ली के अनुसार।</p></div></section>
{info_html(key, base)}
<section class="band"><div class="wrap">{sec_head("आगे आने वाली एकादशी")}{up_list([(x["date"], x["name"], x["key"] + "-kab-hai.html", "सुबह से (व्रत)") for x in others])}
<p style="text-align:center;margin-top:1rem"><a class="btn ghost" href="ekadashi-2026-2027.html">सभी एकादशी की सूची</a> <a class="btn ghost" href="vishnu-chalisa.html">विष्णु चालीसा</a> <a class="btn ghost" href="om-jai-jagdish-hare-aarti.html">ॐ जय जगदीश हरे</a></p></div></section>
{faq_html(ffaq)}''', crumbs=f"{base} कब है", active="tyohar-calendar.html",
        ld=[{"@type":"Event","name":f"{base} {x['date'].year}","startDate":x["date"].isoformat(),"endDate":x["date"].isoformat(),
             "eventAttendanceMode":"https://schema.org/OfflineEventAttendanceMode","eventStatus":"https://schema.org/EventScheduled",
             "location":{"@type":"Place","name":"भारत","address":{"@type":"PostalAddress","addressCountry":"IN"}},
             "description":meaning,"organizer":{"@id":SITE+"#organization"}} for x in occ] + [faq_ld(ffaq)])

# ---------- Purnima / Amavasya ----------
def pa_rows(lst):
    return "".join(f"<tr><th scope=\"row\">{hdate_w(p)}</th><td>{pu}</td><td>{hhmm(s0)}, {s0.day} {MONTHS_HI[s0.month]} से {hhmm(e0)}, {e0.day} {MONTHS_HI[e0.month]} तक</td></tr>" for p, s0, e0, pu in lst)
npu = next((x for x in PURNIMA if x[0] >= TODAY_D), PURNIMA[-1]); nam = next((x for x in AMAVASYA if x[0] >= TODAY_D), AMAVASYA[-1])
add("purnima-amavasya-2026-2027.html", "पूर्णिमा और अमावस्या 2026–2027 — तारीख़ और तिथि समय | OmKiran Bhakti",
    f"2026–2027 की सभी पूर्णिमा और अमावस्या की तारीख़ें, तिथि शुरू-समाप्त होने का समय (नई दिल्ली)। अगली पूर्णिमा {hdate(npu[0])}, अगली अमावस्या {hdate(nam[0])}।"[:160],
    f'''{band("पूर्णिमा और अमावस्या", f"अगली पूर्णिमा <strong>{hdate_w(npu[0])}</strong> ({npu[3]}) और अगली अमावस्या <strong>{hdate_w(nam[0])}</strong> ({nam[3]}) को है।", "पूर्णिमा-अमावस्या", *ART["shivaarti"], "पूर्णिमा")}
<section><div class="wrap">{sec_head("पूर्णिमा")}<div class="tbl"><table class="ptable"><thead><tr><th>तारीख़</th><th>मास</th><th>तिथि</th></tr></thead><tbody>{pa_rows(PURNIMA)}</tbody></table></div></div></section>
<section class="band"><div class="wrap">{sec_head("अमावस्या")}<div class="tbl"><table class="ptable"><thead><tr><th>तारीख़</th><th>मास</th><th>तिथि</th></tr></thead><tbody>{pa_rows(AMAVASYA)}</tbody></table></div>
<p class="pc-note">उदया तिथि के नियम से, नई दिल्ली के अनुसार। पूर्णिमा व्रत कभी-कभी एक दिन पहले (चंद्रोदय के समय पूर्णिमा होने पर) रखा जाता है।</p></div></section>''',
    crumbs="पूर्णिमा-अमावस्या", active="tyohar-calendar.html")

# ---------- daily share message (WhatsApp / Telegram) ----------
fest_today = DAYFEST.get(TODAY_D, [])
msg = (f"🙏 आज का पंचांग — {hdate_w(TODAY_D)}\n"
       f"🌙 तिथि: {TODAY_P['paksha']} {TODAY_P['tithi']} ({TODAY_P['month_purnimanta']} मास)\n"
       f"⭐ नक्षत्र: {TODAY_P['nakshatra']}\n"
       f"🌅 सूर्योदय {t12(TODAY_P['sunrise'])} | सूर्यास्त {t12(TODAY_P['sunset'])}\n"
       f"✨ अभिजीत मुहूर्त: {t12(TODAY_P['abhijit'][0])} – {t12(TODAY_P['abhijit'][1])}\n"
       f"⚠️ राहु काल: {t12(TODAY_P['rahu'][0])} – {t12(TODAY_P['rahu'][1])}\n"
       + (f"🪔 आज: {', '.join(n for n,w,u in fest_today)}\n" if fest_today else "")
       + f"\nपूरा पंचांग: {SITE}aaj-ka-panchang.html\n— OmKiran Bhakti")
open(os.path.join(ROOT, "panchang", "today.txt"), "w", encoding="utf-8").write(msg)

# ---------- compact card for the home hero ----------
def hero_card(p):
    day = dt.date.fromisoformat(p["date"])
    fest = DAYFEST.get(day, [])
    fhtml = "".join(f'<li><a href="{u}">{e(n)}</a> <span>{e(w)}</span></li>' for n, w, u in fest) or '<li class="muted">आज कोई बड़ा त्योहार नहीं है</li>'
    adhik = " (अधिक मास)" if p["adhik"] else ""
    return f'''<div class="pcard hero-pc" id="pcard" data-date="{p['date']}">
<div class="pc-head"><div><h2 class="pc-h1">आज का पंचांग</h2><p class="pc-date"><span data-k="gdate">{hdate_w(day)}</span></p></div>
<button class="chip share" type="button" data-share>WhatsApp पर भेजें</button></div>
<p class="pc-tithi"><span data-k="tithi">{p['paksha']} पक्ष {p['tithi']}</span></p>
<p class="pc-sub"><span data-k="month">{p['month_purnimanta']} मास{adhik}</span>, विक्रम संवत <span data-k="vs">{p['vs']}</span> · <span data-k="tend">{tithi_end_txt(p)}</span></p>
<dl class="pc-grid">
<div><dt>सूर्योदय / सूर्यास्त</dt><dd><span data-k="sunrise">{t12(p['sunrise'])}</span> / <span data-k="sunset">{t12(p['sunset'])}</span></dd></div>
<div><dt>नक्षत्र</dt><dd data-k="nak">{p['nakshatra']}</dd></div>
<div class="good"><dt>अभिजीत मुहूर्त <small>नया काम शुरू करने का शुभ समय</small></dt><dd><span data-k="abhijit">{t12(p['abhijit'][0])} – {t12(p['abhijit'][1])}{'' if p['abhijit_ok'] else ' (बुधवार को नहीं माना जाता)'}</span></dd></div>
<div class="bad"><dt>राहु काल <small>इसमें नया शुभ काम शुरू न करें</small></dt><dd><span data-k="rahu">{t12(p['rahu'][0])} – {t12(p['rahu'][1])}</span></dd></div>
<div class="good"><dt>ब्रह्म मुहूर्त <small>ध्यान, जप और पढ़ाई के लिए</small></dt><dd><span data-k="brahma">{t12(p['brahma'][0])} – {t12(p['brahma'][1])}</span></dd></div>
<div><dt>प्रदोष काल <small>शाम की पूजा, दीपदान</small></dt><dd><span data-k="pradosh">{t12(p['pradosh'][0])} – {t12(p['pradosh'][1])}</span></dd></div>
</dl>
<div class="pc-fest"><h2 class="pc-fh">आज के व्रत-त्योहार</h2><ul data-k="fest">{fhtml}</ul></div>
<p class="pc-note">नई दिल्ली के अनुसार · <a href="aaj-ka-panchang.html">पूरा पंचांग और शब्दों का मतलब</a></p>
</div>'''

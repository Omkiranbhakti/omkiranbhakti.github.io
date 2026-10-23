# Panchak / Bhadra / Kharmas / Gandmool / Sankranti pages. Executed after library_section, before vrat_section.
import datetime as _dt
from kaalcalc import panchak as k_panchak, bhadra as k_bhadra, kharmas as k_kharmas, gandmool as k_gandmool, bhadra_vaas, PANCHAK_TYPE
from panchang import sid_sun as _sid_sun
_now = _dt.datetime.combine(TODAY_D, _dt.time(0, 0))
_far = _dt.datetime.combine(R_END, _dt.time(23, 59))
def _tm2(t): return f"{t.day} {MONTHS_HI[t.month]} {t.year}, {WD[t.weekday()]} — {ct12(t)}" if t else "—"
def _dur(a, b):
    m = int((b - a).total_seconds() // 60); return f"{m // 1440} दिन {m % 1440 // 60} घंटे" if m >= 1440 else f"{m // 60} घंटे {m % 60} मिनट"
KAAL_PAGES = []

# ---------- Panchak ----------
PK = [p for p in k_panchak(_now - _dt.timedelta(days=6), _far) if p[1] and p[1] >= _now]
if PK:
    rows = []
    for a, b in PK:
        tname, tnote = PANCHAK_TYPE[a.weekday()]
        rows.append(f'<tr><td><strong>{_tm2(a)}</strong></td><td>{_tm2(b)}</td><td>{tname}</td><td>{_dur(a, b)}</td></tr>')
    a0, b0 = PK[0]; t0 = PANCHAK_TYPE[a0.weekday()]
    live = a0 <= _now
    ans = ((f"अभी पंचक चल रहा है — यह <strong>{_tm2(b0)}</strong> पर खत्म होगा।" if live else
            f"अगला पंचक <strong>{_tm2(a0)}</strong> से शुरू होकर <strong>{_tm2(b0)}</strong> तक रहेगा।") +
           f" यह <strong>{t0[0]}</strong> है ({t0[1]})। नीचे {R_END.year} तक के सभी पंचक हैं।")
    faqs = [("अगला पंचक कब से कब तक है?", re.sub("<[^>]+>", "", ans)),
            ("पंचक क्या होता है?", "जब चंद्रमा कुंभ और मीन राशि में (धनिष्ठा के तीसरे चरण से रेवती नक्षत्र तक) रहता है, तो लगभग पाँच दिन का यह समय पंचक कहलाता है। यह हर महीने आता है।"),
            ("पंचक में कौन से काम नहीं करने चाहिए?", "परंपरा के अनुसार पंचक में लकड़ी या घास इकट्ठा करना, घर की छत डलवाना, चारपाई या पलंग बनवाना, दक्षिण दिशा की यात्रा और शव का अंतिम संस्कार बिना विधि (कुश के पाँच पुतले) के नहीं करना चाहिए।"),
            ("पंचक कितने प्रकार के होते हैं?", "पंचक जिस दिन से शुरू हो, उसी से उसका नाम होता है: रविवार — रोग पंचक, सोमवार — राज पंचक, मंगलवार — अग्नि पंचक, शुक्रवार — चोर पंचक, शनिवार — मृत्यु पंचक। बुधवार और गुरुवार से शुरू होने वाले पंचक को कम दोष वाला माना जाता है।"),
            ("क्या पंचक में शुभ काम कर सकते हैं?", "विवाह, मुंडन, गृह प्रवेश जैसे शुभ काम पंचक में सामान्यतः टाले जाते हैं, पर राज पंचक को शुभ माना जाता है। पूजा-पाठ, जप और व्रत पर पंचक का कोई दोष नहीं है।")]
    body = (band("पंचक कब है?", ans, "पंचक कब है", ("unfGUJz6D8U", 78), "पंचक") +
            f'<section><div class="wrap">{sec_head("पंचक की पूरी सूची","शुरू और खत्म होने का समय, नई दिल्ली (IST)")}'
            f'<div class="tbl"><table class="ptable"><thead><tr><th>शुरू</th><th>खत्म</th><th>प्रकार</th><th>अवधि</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
            '<p class="note">समय चंद्रमा के कुंभ राशि (300°, लाहिड़ी अयनांश) में प्रवेश और मीन राशि से निकलने का है। सारे भारत में पंचक एक ही क्षण शुरू होता है; केवल घड़ी का समय IST में दिया है।</p></div></section>'
            + faq_html(faqs))
    add("panchak-kab-hai.html", f"पंचक कब है? {TODAY_D.year}–{R_END.year} पंचक की पूरी लिस्ट, प्रकार और समय | OmKiran Bhakti",
        (f"अगला पंचक: {hdate(a0)} से {hdate(b0)} ({t0[0]})। रोग, राज, अग्नि, चोर, मृत्यु पंचक — सभी पंचक की तारीख़, समय और क्या न करें।")[:160],
        body, crumbs="पंचक कब है", ld=[faq_ld(faqs)], active="tyohar-calendar.html")
    KAAL_PAGES.append(("panchak-kab-hai.html", "पंचक कब है?", f"{hdate(a0)} से {hdate(b0)}" if not live else f"अभी चल रहा है, {hdate(b0)} तक"))
    QA.insert(0, ("अगला पंचक कब से है?", f"{_tm2(a0)} से {_tm2(b0)} तक ({t0[0]})।" if not live else f"अभी पंचक चल रहा है, {_tm2(b0)} तक।", "panchak-kab-hai.html"))

# ---------- Bhadra ----------
BH = [b for b in k_bhadra(_now - _dt.timedelta(days=1), _now + _dt.timedelta(days=75)) if b[1] and b[1] >= _now]
if BH:
    rows = [f'<tr><td><strong>{_tm2(a)}</strong></td><td>{_tm2(b)}</td><td>{bhadra_vaas(a)}{" — अशुभ" if bhadra_vaas(a) == "पृथ्वी लोक" else ""}</td></tr>' for a, b in BH]
    today_bh = [x for x in BH if x[0].date() <= TODAY_D <= x[1].date()]
    nxt = next((x for x in BH if x[0].date() > TODAY_D), BH[-1]); a0, b0 = nxt
    def _bt(a, b):
        s_ = f"{ct12(a)}" if a.date() == TODAY_D else f"{a.day} {MONTHS_HI[a.month]} {ct12(a)}"
        e_ = f"{ct12(b)}" if b.date() == TODAY_D else f"{b.day} {MONTHS_HI[b.month]} {ct12(b)}"
        return f"{s_} से {e_}"
    ans = ((f"आज ({hdate_w(TODAY_D)}) भद्रा है: <strong>{'; '.join(_bt(a, b) for a, b in today_bh)}</strong> तक।" if today_bh else f"आज ({hdate_w(TODAY_D)}) भद्रा नहीं है।") +
           f" अगली भद्रा <strong>{_tm2(a0)}</strong> से <strong>{_tm2(b0)}</strong> तक है।")
    faqs = [("आज भद्रा कब तक है?", re.sub("<[^>]+>", "", ans)),
            ("भद्रा क्या है?", "पंचांग के 11 करणों में से ‘विष्टि’ करण को भद्रा कहते हैं। यह हर महीने लगभग 8 बार, लगभग 12–13 घंटे के लिए आती है और इसमें शुभ काम, खासकर राखी बाँधना और होलिका दहन, वर्जित माने जाते हैं।"),
            ("भद्रा का वास कहाँ होता है?", "चंद्रमा कर्क, सिंह, कुंभ या मीन राशि में हो तो भद्रा पृथ्वी लोक पर (अशुभ); मेष, वृषभ, मिथुन, वृश्चिक में स्वर्ग लोक पर; और कन्या, तुला, धनु, मकर में पाताल लोक पर मानी जाती है। स्वर्ग और पाताल की भद्रा का दोष कम माना जाता है।")]
    body = (band("भद्रा कब है? आज की भद्रा", ans, "भद्रा काल", ("unfGUJz6D8U", 78), "भद्रा") +
            f'<section><div class="wrap">{sec_head("अगले ढाई महीने की भद्रा","शुरू, खत्म और भद्रा का वास — नई दिल्ली (IST)")}'
            f'<div class="tbl"><table class="ptable"><thead><tr><th>शुरू</th><th>खत्म</th><th>भद्रा का वास</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
            '<p class="note">यह पेज हर दिन अपने-आप अपडेट होता है। भद्रा तिथि और करण पर आधारित है, इसलिए पूरे भारत में एक ही क्षण शुरू होती है।</p></div></section>' + faq_html(faqs))
    add("bhadra-kaal.html", "भद्रा कब है? आज की भद्रा, भद्रा का वास और पूरी लिस्ट | OmKiran Bhakti",
        (f"आज भद्रा {'है' if today_bh else 'नहीं है'}। अगली भद्रा {hdate(a0)} को {ct12(a0)} से। अगले 75 दिन की भद्रा, शुरू-खत्म का समय और भद्रा का वास।")[:160],
        body, crumbs="भद्रा काल", ld=[faq_ld(faqs)], active="tyohar-calendar.html")
    KAAL_PAGES.append(("bhadra-kaal.html", "भद्रा कब है?", "आज और अगले 75 दिन"))
    QA.insert(1, ("आज भद्रा है या नहीं?", re.sub("<[^>]+>", "", ans), "bhadra-kaal.html"))

# ---------- Kharmas + Sankranti (solar) ----------
KH = [k for k in k_kharmas(_now - _dt.timedelta(days=40), _far) if not k[1] or k[1] >= _now]
def sankranti_at(deg, start, end):
    """IST moment the Sun (sidereal) enters `deg`."""
    t = start; step = _dt.timedelta(hours=6)
    f = lambda x: (_sid_sun(from_ist(x)) - deg + 360) % 360
    while t < end:
        if f(t) > 300 and f(t + step) < 60:
            a, b = t, t + step
            while b - a > _dt.timedelta(seconds=30):
                m = a + (b - a) / 2
                if f(m) > 300: a = m
                else: b = m
            return b
        t += step
    return None
def sankranti_day(t):
    """Punya kaal day: same day if the Sun enters before sunset, otherwise next day."""
    ss = to_ist(sunrise_sunset(t.date())[1])
    return t.date() if t < ss else t.date() + _dt.timedelta(days=1)
if KH:
    rows = [f'<tr><td>{n} संक्रांति से (सूर्य {n} राशि में)</td><td><strong>{_tm2(a)}</strong></td><td>{_tm2(b) if b else "—"}</td></tr>' for a, b, n in KH]
    a0, b0, n0 = KH[0]; live = a0 <= _now
    ans = ((f"अभी खरमास चल रहा है — यह <strong>{_tm2(b0)}</strong> को खत्म होगा।" if live else f"अगला खरमास <strong>{_tm2(a0)}</strong> से <strong>{_tm2(b0)}</strong> तक है।") +
           " खरमास में विवाह, गृह प्रवेश, मुंडन जैसे मांगलिक काम नहीं किए जाते।")
    faqs = [("खरमास कब से कब तक है?", re.sub("<[^>]+>", "", ans)),
            ("खरमास क्या है?", "जब सूर्य धनु या मीन राशि (गुरु की राशियाँ) में होते हैं, तब का लगभग एक महीना खरमास या मलमास कहलाता है। साल में दो बार — मध्य दिसंबर से मकर संक्रांति तक, और मध्य मार्च से मध्य अप्रैल तक।"),
            ("खरमास में क्या करें?", "दान, जप, सूर्य को अर्घ्य, विष्णु और सूर्य की पूजा और तीर्थ स्नान को इस महीने में बहुत पुण्य वाला माना जाता है; केवल नए मांगलिक काम टाले जाते हैं।")]
    body = (band("खरमास कब है?", ans, "खरमास", ("ktQUU5Y3tPE", 50), "खरमास") +
            f'<section><div class="wrap">{sec_head("खरमास की तारीख़ें","सूर्य के धनु/मीन राशि में प्रवेश और निकलने का समय (IST)")}'
            f'<div class="tbl"><table class="ptable"><thead><tr><th>खरमास</th><th>शुरू</th><th>खत्म</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div></div></section>' + faq_html(faqs))
    add("kharmas-kab-hai.html", f"खरमास कब से है? {TODAY_D.year}–{R_END.year} खरमास (मलमास) की तारीख़ें | OmKiran Bhakti",
        (f"खरमास: {hdate(a0)} से {hdate(b0)}। सूर्य के धनु और मीन राशि में रहने का समय, क्या करें और क्या न करें।")[:160],
        body, crumbs="खरमास", ld=[faq_ld(faqs)], active="tyohar-calendar.html")
    KAAL_PAGES.append(("kharmas-kab-hai.html", "खरमास कब है?", f"{hdate(a0)} से"))
    QA.insert(2, ("खरमास कब से शुरू है?", re.sub("<[^>]+>", "", ans).split(" खरमास में")[0], "kharmas-kab-hai.html"))

# Makar Sankranti / Lohri / Pongal and Baisakhi (Mesh Sankranti)
SOLAR = []
for deg, key, name in ((270, "makar-sankranti", "मकर संक्रांति"), (0, "baisakhi", "बैसाखी (मेष संक्रांति)")):
    t = sankranti_at(deg, _now - _dt.timedelta(days=2), _far)
    while t:
        SOLAR.append((key, name, t, sankranti_day(t)))
        t = sankranti_at(deg, t + _dt.timedelta(days=300), _far)
for key, name in (("makar-sankranti", "मकर संक्रांति"), ("baisakhi", "बैसाखी (मेष संक्रांति)")):
    occ = [x for x in SOLAR if x[0] == key and x[3] >= TODAY_D]
    if not occ: continue
    k, n, t, d = occ[0]; Y = d.year
    ss = to_ist(sunrise_sunset(d)[1])
    if key == "makar-sankranti":
        h1 = f"मकर संक्रांति {Y} कब है? लोहड़ी और पोंगल की तारीख़"
        ans = (f"मकर संक्रांति {Y} <strong>{hdate_w(d)}</strong> को है। सूर्य {_tm2(t)} पर मकर राशि में प्रवेश करेंगे"
               + (", जो सूर्यास्त के बाद है, इसलिए स्नान-दान अगले दिन होगा।" if d != t.date() else "।")
               + f" लोहड़ी <strong>{hdate_w(d - _dt.timedelta(days=1))}</strong> को और पोंगल {hdate(d)} को है।")
        faqs = [(f"मकर संक्रांति {Y} कब है?", f"{hdate_w(d)} को।"), (f"लोहड़ी {Y} कब है?", f"{hdate_w(d - _dt.timedelta(days=1))} को, मकर संक्रांति से एक दिन पहले।"),
                (f"मकर संक्रांति {Y} में सूर्य मकर राशि में कब जाएँगे?", f"{_tm2(t)} पर (IST)।"),
                ("मकर संक्रांति कभी 14 और कभी 15 जनवरी को क्यों होती है?", "संक्रांति उस क्षण होती है जब सूर्य मकर राशि में प्रवेश करते हैं। यह क्षण हर साल लगभग 6 घंटे आगे खिसकता है; अगर प्रवेश सूर्यास्त के बाद हो, तो पुण्य काल और त्योहार अगले दिन माना जाता है।")]
        slug = "makar-sankranti-kab-hai.html"; art = ("ktQUU5Y3tPE", 50)
        rel = '<p class="lede"><a href="surya-chalisa.html">सूर्य चालीसा</a>, <a href="aditya-hridaya-stotra.html">आदित्य हृदय स्तोत्र</a> और <a href="surya-12-naam-mantra.html">सूर्य के 12 नाम</a></p>'
    else:
        h1 = f"बैसाखी {Y} कब है? मेष संक्रांति की तारीख़"
        ans = f"बैसाखी (मेष संक्रांति) {Y} <strong>{hdate_w(d)}</strong> को है। सूर्य {_tm2(t)} पर मेष राशि में प्रवेश करेंगे — इसी दिन से सौर नववर्ष शुरू होता है।"
        faqs = [(f"बैसाखी {Y} कब है?", f"{hdate_w(d)} को।"), ("बैसाखी क्यों मनाई जाती है?", "यह रबी की फ़सल कटने का उत्सव और सौर नववर्ष है; 1699 में इसी दिन गुरु गोबिंद सिंह जी ने खालसा पंथ की स्थापना की थी।")]
        slug = "baisakhi-kab-hai.html"; art = ("ktQUU5Y3tPE", 50); rel = ""
    body = band(h1, ans, h1.split(" कब")[0], *art, h1.split(" कब")[0], extra=rel) + faq_html(faqs)
    add(slug, f"{h1} | OmKiran Bhakti" if len(h1) < 80 else f"{h1.split('?')[0]}? | OmKiran Bhakti", re.sub("<[^>]+>", "", ans)[:160], body,
        crumbs=h1.split(" कब")[0], ld=[faq_ld(faqs), {"@type":"Event","name":f"{n} {Y}","startDate":d.isoformat(),"eventAttendanceMode":"https://schema.org/OfflineEventAttendanceMode",
        "location":{"@type":"Place","name":"भारत","address":{"@type":"PostalAddress","addressCountry":"IN"}}}], active="tyohar-calendar.html")
    KAAL_PAGES.append((slug, h1.split("?")[0] + "?", hdate(d)))
    QA.append((f"{n.split(' (')[0]} {Y} कब है?", f"{hdate_w(d)}।", slug))
    if key == "makar-sankranti": QA.append((f"लोहड़ी {Y} कब है?", f"{hdate_w(d - _dt.timedelta(days=1))}।", slug))

# ---------- Gandmool ----------
_gm = k_gandmool(_now - _dt.timedelta(days=2), _now + _dt.timedelta(days=75))
_gm = [g for g in _gm if g[1] is not None]  # drop the open-ended tail at the scan edge
GM = []
for a, b, n in _gm:
    if GM and abs((GM[-1][1] - a).total_seconds()) < 120: GM[-1] = (GM[-1][0], b, GM[-1][2] + "–" + n)
    else: GM.append((a, b, n))
GM = [g for g in GM if g[1] >= _now]
if GM:
    rows = [f'<tr><td><strong>{_tm2(a)}</strong></td><td>{_tm2(b)}</td><td>{n}</td></tr>' for a, b, n in GM]
    a0, b0, n0 = GM[0]; live = a0 <= _now
    ans = (f"अभी गंडमूल नक्षत्र ({n0}) चल रहा है — {_tm2(b0)} तक।" if live else f"अगला गंडमूल <strong>{_tm2(a0)}</strong> से <strong>{_tm2(b0)}</strong> तक ({n0}) है।") + " नीचे अगले 75 दिन के सभी गंडमूल हैं।"
    faqs = [("आज गंडमूल नक्षत्र है क्या?", re.sub("<[^>]+>", "", ans).split(" नीचे")[0]),
            ("गंडमूल नक्षत्र कौन से हैं?", "अश्विनी, आश्लेषा, मघा, ज्येष्ठा, मूल और रेवती — ये छह नक्षत्र गंडमूल कहलाते हैं, क्योंकि ये राशि और नक्षत्र दोनों के जोड़ (संधि) पर पड़ते हैं।"),
            ("गंडमूल में जन्मे बच्चे के लिए क्या करते हैं?", "परंपरा में जन्म के 27वें दिन, जब वही नक्षत्र दोबारा आता है, गंडमूल शांति पूजा कराई जाती है। यह कोई डरने की बात नहीं है; पूजा के बाद इसे दोष-रहित माना जाता है।")]
    body = (band("गंडमूल नक्षत्र कब है?", ans, "गंडमूल नक्षत्र", ("unfGUJz6D8U", 78), "गंडमूल") +
            f'<section><div class="wrap">{sec_head("अगले 75 दिन के गंडमूल","नई दिल्ली (IST)")}'
            f'<div class="tbl"><table class="ptable"><thead><tr><th>शुरू</th><th>खत्म</th><th>नक्षत्र</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
            '<p class="note">अपने बच्चे का जन्म-नक्षत्र जानने के लिए <a href="janm-tithi-rashi-calculator.html">जन्म तिथि और राशि कैलकुलेटर</a> का उपयोग करें।</p></div></section>' + faq_html(faqs))
    add("gandmool-nakshatra.html", "गंडमूल नक्षत्र कब है? आज और अगले 75 दिन के गंडमूल | OmKiran Bhakti",
        (f"अगला गंडमूल: {hdate(a0)} से {hdate(b0)} ({n0})। गंडमूल नक्षत्रों की लिस्ट, समय और शांति पूजा की जानकारी।")[:160],
        body, crumbs="गंडमूल नक्षत्र", ld=[faq_ld(faqs)], active="tyohar-calendar.html")
    KAAL_PAGES.append(("gandmool-nakshatra.html", "गंडमूल नक्षत्र कब है?", "आज और अगले 75 दिन"))

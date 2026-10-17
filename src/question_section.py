# Answer-first pages for the most-searched "कब है" questions + a Q&A hub.
# Executed after city_section (uses SPANS, FEST, EKA, PURNIMA, AMAVASYA, TODAY_D, add, band, sec_head, faq_html, faq_ld, hdate_w, hdate, e, ct12, c_sun, IN_CITIES, IN_TZ, CITY_JS, city_search, nxt_fest, ART, FART, CITY_PAGES, MONTHS_HI).
import datetime as _dt
HOT_DATES = {}
def _sr(day): return c_sun(28.6139, 77.2090, day, IN_TZ)

# ---------- Navratri: Ashtami / Navami ----------
def navratri_info(start_day, label):
    """From the Pratipada (ghatasthapana) day, find Shukla Ashtami/Navami spans and observance days (New Delhi)."""
    sp = [x for x in SPANS if start_day - _dt.timedelta(days=1) <= x[1].date() <= start_day + _dt.timedelta(days=12)]
    ash = next((x for x in sp if x[0] == 7), None); nav = next((x for x in sp if x[0] == 8), None)
    if not ash or not nav: return None
    # Durga Ashtami: day on which Ashtami prevails at sunrise
    d = ash[1].date(); ad = None
    while d <= ash[2].date():
        sr, _ = _sr(d)
        if ash[1] <= sr.replace(tzinfo=None) < ash[2]: ad = d; break
        d += _dt.timedelta(days=1)
    ad = ad or ash[1].date()
    # Maha Navami: the day Navami begins, if it begins before sunset; otherwise next day
    _, ssn = _sr(nav[1].date())
    nd = nav[1].date() if nav[1] < ssn.replace(tzinfo=None) else nav[1].date() + _dt.timedelta(days=1)
    if label.startswith("चैत्र"):  # Chaitra Navami = Ram Navami (madhyahna rule)
        rn = next((x["date"] for x in FEST.get("ram-navami", []) if abs((x["date"] - start_day).days) < 14), None)
        if rn: nd = rn
    sandhi = (ash[2] - _dt.timedelta(minutes=24), ash[2] + _dt.timedelta(minutes=24))
    return {"label": label, "start": start_day, "ash": ash, "nav": nav, "ad": ad, "nd": nd, "sandhi": sandhi, "same": ad == nd}

def _tm(t): return f"{t.day} {MONTHS_HI[t.month]}, {ct12(t)}"
NAVS = []
for key, label in (("sharadiya-navratri", "शारदीय नवरात्रि"), ("chaitra-navratri", "चैत्र नवरात्रि")):
    for x in FEST.get(key, []):
        info = navratri_info(x["date"], label)
        if info and info["nd"] >= TODAY_D: NAVS.append(info)
NAVS.sort(key=lambda i: i["start"])
if NAVS:
    n0 = NAVS[0]; Y0 = n0["ad"].year
    same_txt = ("हाँ — इस बार अष्टमी और नवमी <strong>एक ही दिन</strong> हैं।" if n0["same"] else "नहीं — अष्टमी और नवमी अलग-अलग दिन हैं।")
    ans = (f"{n0['label']} {Y0} में <strong>दुर्गा अष्टमी {hdate_w(n0['ad'])}</strong> और <strong>महानवमी {hdate_w(n0['nd'])}</strong> को है। {same_txt} "
           f"संधि पूजा {ct12(n0['sandhi'][0])} से {ct12(n0['sandhi'][1])} तक होगी (नई दिल्ली)।")
    blocks = []
    for n in NAVS[:3]:
        Y = n["ad"].year
        why = ""
        if n["same"]:
            why = (f"<p>अष्टमी तिथि {_tm(n['ash'][2])} पर समाप्त होकर उसी दिन नवमी शुरू हो रही है। इसलिए {hdate(n['ad'])} को सुबह अष्टमी का और {ct12(n['nav'][1])} के बाद नवमी का पूजन होगा। "
                   f"नवमी तिथि {_tm(n['nav'][2])} तक है, इसलिए कई परिवार अगले दिन सुबह भी नवमी का कन्या पूजन करते हैं।</p>")
        blocks.append(
            f'<div class="nv-card"><h3>{n["label"]} {Y}</h3><table class="ptable"><tbody>'
            f'<tr><th>दुर्गा अष्टमी</th><td class="big">{hdate_w(n["ad"])}</td></tr>'
            f'<tr><th>महानवमी</th><td class="big">{hdate_w(n["nd"])}</td></tr>'
            f'<tr><th>अष्टमी तिथि</th><td>{_tm(n["ash"][1])} से {_tm(n["ash"][2])} तक</td></tr>'
            f'<tr><th>नवमी तिथि</th><td>{_tm(n["nav"][1])} से {_tm(n["nav"][2])} तक</td></tr>'
            f'<tr><th>संधि पूजा</th><td>{_tm(n["sandhi"][0])} – {ct12(n["sandhi"][1])}</td></tr>'
            f'<tr><th>अष्टमी-नवमी एक साथ?</th><td>{"हाँ, एक ही दिन" if n["same"] else "नहीं, अलग-अलग दिन"}</td></tr>'
            f'</tbody></table>{why}</div>')
    faqs = [(f"{n0['label']} {Y0} में अष्टमी कब है?", f"दुर्गा अष्टमी {hdate_w(n0['ad'])} को है। अष्टमी तिथि {_tm(n0['ash'][1])} से {_tm(n0['ash'][2])} तक है।"),
            (f"{n0['label']} {Y0} में नवमी कब है?", f"महानवमी {hdate_w(n0['nd'])} को है। नवमी तिथि {_tm(n0['nav'][1])} से {_tm(n0['nav'][2])} तक है।"),
            (f"क्या {Y0} में अष्टमी और नवमी एक साथ हैं?", re.sub("<[^>]+>", "", same_txt) + (f" अष्टमी तिथि {_tm(n0['ash'][2])} पर खत्म होकर नवमी शुरू हो जाती है।" if n0["same"] else "")),
            (f"{n0['label']} {Y0} में कन्या पूजन कब करें?", f"अष्टमी का कन्या पूजन {hdate(n0['ad'])} की सुबह ({ct12(n0['ash'][2])} से पहले) और नवमी का कन्या पूजन {ct12(n0['nav'][1])} के बाद करें।" if n0["same"]
                 else f"अष्टमी का कन्या पूजन {hdate_w(n0['ad'])} को और नवमी का {hdate_w(n0['nd'])} को सुबह किया जाता है।"),
            ("संधि पूजा क्या है और कब होती है?", "अष्टमी तिथि के आखिरी 24 मिनट और नवमी के पहले 24 मिनट को संधि काल कहते हैं। माना जाता है कि इसी समय माँ चामुंडा ने चंड-मुंड का वध किया था; इस समय 108 दीपक और 108 कमल से पूजा की जाती है।")]
    body = (band(f"{n0['label']} {Y0}: अष्टमी और नवमी कब है?", ans, "अष्टमी-नवमी कब है", *ART["navdurga"], "माँ दुर्गा",
                 extra='<p class="lede"><a href="navratri-2026.html">नवरात्रि के नौ दिन</a>, <a href="durga-chalisa.html">दुर्गा चालीसा</a> और <a href="jai-ambe-gauri-aarti.html">जय अम्बे गौरी आरती</a></p>') +
            f'<section><div class="wrap">{sec_head("तारीख़, तिथि और संधि पूजा का समय","नई दिल्ली के पंचांग के अनुसार")}<div class="nv-grid">{"".join(blocks)}</div>'
            '<p class="note">दुर्गा अष्टमी उस दिन मानी जाती है जिस दिन सूर्योदय के समय अष्टमी तिथि हो। नवमी उस दिन मानी जाती है जिस दिन (सूर्यास्त से पहले) नवमी तिथि शुरू हो। अपने शहर में तिथि का समय कुछ मिनट अलग हो सकता है।</p></div></section>'
            + faq_html(faqs))
    add("navratri-ashtami-navami-kab-hai.html", f"नवरात्रि {Y0} अष्टमी-नवमी कब है? क्या एक साथ हैं, संधि पूजा का समय | OmKiran Bhakti",
        f"{n0['label']} {Y0}: दुर्गा अष्टमी {hdate(n0['ad'])}, महानवमी {hdate(n0['nd'])}। अष्टमी-नवमी एक साथ हैं या नहीं, तिथि समय, संधि पूजा और कन्या पूजन।"[:160],
        body, crumbs="अष्टमी-नवमी कब है", ld=[faq_ld(faqs)], active="tyohar-calendar.html")
    CITY_PAGES.append(("navratri-ashtami-navami-kab-hai.html", f"नवरात्रि {Y0}: अष्टमी-नवमी कब है?", "durga-ashtami"))
    HOT_DATES["durga-ashtami"] = n0["ad"]

    # ---- exact-match pages: "अष्टमी कब है" / "नवमी कब है"
    _rel = ('<p class="lede"><a href="navratri-ashtami-navami-kab-hai.html">अष्टमी-नवमी एक साथ?</a> · <a href="navratri-vrat-ke-niyam.html">नवरात्रि के नियम</a> · '
            '<a href="durga-chalisa.html">दुर्गा चालीसा</a> · <a href="jai-ambe-gauri-aarti.html">जय अम्बे गौरी</a> · <a href="dussehra-kab-hai.html">दशहरा कब है</a></p>')
    _same = " इस बार अष्टमी और नवमी एक ही दिन हैं।" if n0["same"] else ""
    a_ans = (f"{n0['label']} {Y0} में दुर्गा अष्टमी (महाअष्टमी) <strong>{hdate_w(n0['ad'])}</strong> को है। अष्टमी तिथि {_tm(n0['ash'][1])} से {_tm(n0['ash'][2])} तक है।"
             f"{_same} संधि पूजा {_tm(n0['sandhi'][0])} से {ct12(n0['sandhi'][1])} तक होगी (नई दिल्ली)।")
    a_faq = [(f"अष्टमी {Y0} कब है?", re.sub("<[^>]+>", "", a_ans)),
             (f"अष्टमी का कन्या पूजन कब करें?", f"{hdate_w(n0['ad'])} की सुबह, अष्टमी तिथि रहते हुए ({ct12(n0['ash'][2])} से पहले)।"),
             ("महाअष्टमी पर किस देवी की पूजा होती है?", "माँ महागौरी की — नवदुर्गा का आठवाँ रूप। इसी दिन संधि पूजा और कई घरों में हवन होता है।"),
             ("कन्या पूजन में कितनी कन्याएँ बुलाएँ?", "2 से 10 साल की 9 कन्याएँ और एक बालक (लांगुर/भैरव)। उन्हें पूरी, हलवा और काले चने खिलाकर उपहार दिए जाते हैं।"),
             (f"Durga Ashtami {Y0} date?", f"Durga Ashtami {Y0}: {n0['ad'].strftime('%d %B %Y')}. Sandhi puja (New Delhi): {ct12(n0['sandhi'][0])}–{ct12(n0['sandhi'][1])}.")]
    add("durga-ashtami-kab-hai.html", f"अष्टमी कब है {Y0}? दुर्गा अष्टमी की तारीख़, कन्या पूजन और संधि पूजा का समय (Durga Ashtami) | OmKiran Bhakti",
        f"दुर्गा अष्टमी {Y0}: {hdate(n0['ad'])}। अष्टमी तिथि का समय, कन्या पूजन मुहूर्त, संधि पूजा का समय और महागौरी पूजा।"[:160],
        band(f"अष्टमी कब है? दुर्गा अष्टमी {Y0}", a_ans, "अष्टमी कब है", *ART["navdurga"], "दुर्गा अष्टमी", extra=_rel)
        + f'<section><div class="wrap">{sec_head("महाअष्टमी पर क्या करें")}<ol class="steps"><li>सुबह स्नान करके माँ महागौरी की पूजा करें, लाल चुनरी और नारियल चढ़ाएँ।</li><li>अष्टमी तिथि रहते हुए कन्या पूजन करें: 9 कन्याओं और एक बालक के पैर धोकर, तिलक लगाकर पूरी-हलवा-चने का भोग।</li><li>संधि काल में 108 दीपक और 108 कमल (या फूल) से संधि पूजा करें।</li><li>दुर्गा सप्तशती या दुर्गा चालीसा का पाठ और जय अम्बे गौरी की आरती करें।</li></ol></div></section>'
        + faq_html(a_faq), crumbs="अष्टमी कब है", ld=[faq_ld(a_faq)], active="tyohar-calendar.html")
    n_ans = (f"{n0['label']} {Y0} में महानवमी <strong>{hdate_w(n0['nd'])}</strong> को है। नवमी तिथि {_tm(n0['nav'][1])} से {_tm(n0['nav'][2])} तक है।{_same}"
             f" अगले दिन दशहरा (विजयादशमी) है।")
    n_faq = [(f"नवमी {Y0} कब है?", re.sub("<[^>]+>", "", n_ans)),
             ("नवमी का कन्या पूजन कब करें?", f"नवमी तिथि में, {ct12(n0['nav'][1])} के बाद" + (f"; कई परिवार अगले दिन सुबह भी नवमी का कन्या पूजन करते हैं क्योंकि नवमी तिथि {_tm(n0['nav'][2])} तक है।" if n0["same"] else "।")),
             ("महानवमी पर किस देवी की पूजा होती है?", "माँ सिद्धिदात्री की — नवदुर्गा का नौवाँ रूप। इसी दिन हवन करके नवरात्रि का समापन होता है।"),
             ("नवरात्रि का व्रत कब खोलें (पारण)?", "जो पूरे नौ दिन व्रत रखते हैं, वे नवमी तिथि समाप्त होने के बाद या दशमी (दशहरे) की सुबह पारण करते हैं; कई परिवार नवमी के हवन और कन्या पूजन के बाद व्रत खोलते हैं।"),
             (f"Maha Navami {Y0} date?", f"Maha Navami {Y0}: {n0['nd'].strftime('%d %B %Y')}. Navami tithi: {_tm(n0['nav'][1])} to {_tm(n0['nav'][2])}.")]
    add("maha-navami-kab-hai.html", f"नवमी कब है {Y0}? महानवमी की तारीख़, कन्या पूजन, हवन और पारण (Maha Navami) | OmKiran Bhakti",
        f"महानवमी {Y0}: {hdate(n0['nd'])}। नवमी तिथि का समय, कन्या पूजन, हवन, सिद्धिदात्री पूजा और नवरात्रि व्रत का पारण।"[:160],
        band(f"नवमी कब है? महानवमी {Y0}", n_ans, "नवमी कब है", *ART["navdurga"], "महानवमी", extra=_rel)
        + f'<section><div class="wrap">{sec_head("महानवमी पर क्या करें")}<ol class="steps"><li>माँ सिद्धिदात्री की पूजा करें, तिल और मौसमी फल चढ़ाएँ।</li><li>नवमी तिथि में कन्या पूजन करें, अगर अष्टमी को नहीं किया है।</li><li>हवन करके नवरात्रि का समापन करें: दुर्गा सप्तशती के मंत्रों या ‘ॐ दुं दुर्गायै नमः’ से आहुति दें।</li><li>जौ (खेतरी) और कलश को अगले दिन दशहरे पर सम्मान से विसर्जित करें।</li></ol></div></section>'
        + faq_html(n_faq), crumbs="नवमी कब है", ld=[faq_ld(n_faq)], active="tyohar-calendar.html")
    CITY_PAGES.append(("durga-ashtami-kab-hai.html", f"अष्टमी कब है {Y0}?", "durga-ashtami"))
    CITY_PAGES.append(("maha-navami-kab-hai.html", f"नवमी कब है {Y0}?", "maha-navami"))
    HOT_DATES["maha-navami"] = n0["nd"]

# ---------- Dussehra: city-wise Vijay muhurat & Ravan dahan ----------
ds = nxt_fest("dussehra")
if ds:
    D = ds["date"]; Y = D.year
    rows, data = [], {}
    for hi, en, la, lo in IN_CITIES:
        sr, ss = c_sun(la, lo, D, IN_TZ); day = (ss - sr)
        mu = day / 15; vs, ve = sr + mu * 10, sr + mu * 11
        ap_s, ap_e = sr + day / 5 * 3, sr + day / 5 * 4
        data[en] = (vs, ve, ap_s, ap_e, ss)
        rows.append(f'<tr><td><strong>{hi}</strong> <span class="en">{en}</span></td><td class="big">{ct12(vs)} – {ct12(ve)}</td><td>{ct12(ap_s)} – {ct12(ap_e)}</td><td>{ct12(ss)} के बाद</td></tr>')
    dv = data["Delhi"]; mv = data["Mumbai"]
    dash = next((x for x in SPANS if x[0] == 9 and x[1].date() <= D <= x[2].date()), None)
    ans = (f"दशहरा (विजयादशमी) {Y} <strong>{hdate_w(D)}</strong> को है। दिल्ली में विजय मुहूर्त <strong>{ct12(dv[0])} से {ct12(dv[1])}</strong> तक और रावण दहन सूर्यास्त ({ct12(dv[4])}) के बाद होगा। "
           "नीचे 65+ शहरों का विजय मुहूर्त, अपराह्न पूजा और रावण दहन का समय है।")
    faqs = [(f"दशहरा {Y} कब है?", f"{hdate_w(D)} को।" + (f" दशमी तिथि {_tm(dash[1])} से {_tm(dash[2])} तक है।" if dash else "")),
            (f"दशहरा {Y} में विजय मुहूर्त क्या है?", f"दिल्ली में {ct12(dv[0])} से {ct12(dv[1])} तक; मुंबई में {ct12(mv[0])} से {ct12(mv[1])} तक।"),
            (f"दशहरा {Y} में रावण दहन कितने बजे होगा?", f"रावण दहन प्रदोष काल में, सूर्यास्त के बाद होता है — दिल्ली में {ct12(dv[4])} के बाद, मुंबई में {ct12(mv[4])} के बाद। स्थानीय समिति का समय भी देख लें।"),
            ("विजय मुहूर्त क्या होता है?", "दिन (सूर्योदय से सूर्यास्त) को 15 बराबर भागों में बाँटने पर 11वाँ भाग विजय मुहूर्त कहलाता है। दशहरे पर शमी पूजा, शस्त्र पूजा और नए काम की शुरुआत के लिए इसे सबसे शुभ माना जाता है।")]
    body = (band(f"दशहरा {Y}: विजय मुहूर्त और रावण दहन का समय", ans, "दशहरा मुहूर्त", *FART.get("dussehra", ART["ram"]), "दशहरा",
                 extra='<p class="lede"><a href="dussehra-kab-hai.html">दशहरा कब है</a>, <a href="ram-raksha-stotra.html">राम रक्षा स्तोत्र</a> और <a href="ram-chalisa.html">राम चालीसा</a></p>') +
            f'<section><div class="wrap">{sec_head(f"शहरवार दशहरा मुहूर्त — {hdate_w(D)}")}{city_search("अपना शहर लिखें — जैसे Delhi, कोटा, Kolkata…")}'
            f'<div class="tbl"><table class="ptable city-table"><thead><tr><th>शहर</th><th>विजय मुहूर्त</th><th>अपराह्न पूजा</th><th>रावण दहन</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
            '<p class="note">विजय मुहूर्त दिन का 11वाँ मुहूर्त है; अपराह्न दिन का चौथा पंचमांश। समय स्थानीय सूर्योदय-सूर्यास्त से निकाला गया है।</p></div></section>'
            + faq_html(faqs) + CITY_JS)
    ld = [{"@type":"Event","name":f"दशहरा {Y}","startDate":D.isoformat(),"eventAttendanceMode":"https://schema.org/OfflineEventAttendanceMode",
           "location":{"@type":"Place","name":"भारत","address":{"@type":"PostalAddress","addressCountry":"IN"}},"description":f"दशहरा {Y}: शहरवार विजय मुहूर्त और रावण दहन"}, faq_ld(faqs)]
    add("dussehra-vijay-muhurat-ravan-dahan.html", f"दशहरा {Y} विजय मुहूर्त, रावण दहन का समय — शहरवार | OmKiran Bhakti",
        f"दशहरा {Y} ({hdate_w(D)}): दिल्ली में विजय मुहूर्त {ct12(dv[0])}–{ct12(dv[1])}, रावण दहन {ct12(dv[4])} के बाद। 65+ शहरों का समय।"[:160],
        body, crumbs="दशहरा मुहूर्त", ld=ld, active="tyohar-calendar.html")
    CITY_ANS["dussehra"] = f"दिल्ली में विजय मुहूर्त {ct12(dv[0])}–{ct12(dv[1])}, रावण दहन {ct12(dv[4])} के बाद।"
    CITY_PAGES.append(("dussehra-vijay-muhurat-ravan-dahan.html", f"दशहरा {Y}: विजय मुहूर्त और रावण दहन", "dussehra"))
    _fp = "dussehra-kab-hai.html"
    if _fp in PAGES:
        PAGES[_fp] = PAGES[_fp].replace('<section><div class="wrap">',
            f'<section class="hot"><div class="wrap"><ul class="hot-list"><li><a href="dussehra-vijay-muhurat-ravan-dahan.html"><strong>दशहरा {Y}: विजय मुहूर्त और रावण दहन</strong><span>अपने शहर का समय देखें</span></a></li></ul></div></section><section><div class="wrap">', 1)

# ---------- Q&A hub: every "कब है" question with a direct answer ----------
QA = []
if NAVS:
    QA.append((f"नवरात्रि {Y0} में अष्टमी-नवमी कब है?", f"दुर्गा अष्टमी {hdate_w(n0['ad'])}, महानवमी {hdate_w(n0['nd'])}।", "navratri-ashtami-navami-kab-hai.html"))
    QA.append((f"क्या {Y0} में अष्टमी और नवमी एक साथ हैं?", "हाँ, दोनों एक ही दिन हैं।" if n0["same"] else "नहीं, दोनों अलग-अलग दिन हैं।", "navratri-ashtami-navami-kab-hai.html"))
nek = next((x for x in EKA if x["date"] >= TODAY_D), None)
if nek: QA.append(("अगली एकादशी कब है?", f"{nek['name']} — {hdate_w(nek['date'])}।", "ekadashi-2026-2027.html"))
npu = next((p for p in PURNIMA if p[0] >= TODAY_D), None); nam = next((p for p in AMAVASYA if p[0] >= TODAY_D), None)
if npu: QA.append(("अगली पूर्णिमा कब है?", f"{npu[3]} पूर्णिमा — {hdate_w(npu[0])}।", "purnima-amavasya-2026-2027.html"))
if nam: QA.append(("अगली अमावस्या कब है?", f"{nam[3]} अमावस्या — {hdate_w(nam[0])}।", "purnima-amavasya-2026-2027.html"))
for k, occ in sorted(FEST.items(), key=lambda kv: (nxt_fest(kv[0]) or {"date": _dt.date(2100,1,1)})["date"]):
    x = nxt_fest(k)
    if not x or x["date"] < TODAY_D or not (k + "-kab-hai.html") in PAGES: continue
    nm = re.sub(r"\s*\(.*?\)", "", x["name"])
    QA.append((f"{nm} {x['date'].year} कब है?", f"{hdate_w(x['date'])}।", f"{k}-kab-hai.html"))
for h, t, k in CITY_PAGES:
    if h == "navratri-ashtami-navami-kab-hai.html": continue
    QA.append((t.split(":")[0] + " में " + {"karwa-chauth":"चाँद कब निकलेगा?","diwali":"लक्ष्मी पूजा का मुहूर्त क्या है?","chhath-puja":"अर्घ्य का समय क्या है?","dussehra":"विजय मुहूर्त और रावण दहन कब है?"}.get(k, "समय क्या है?"),
               CITY_ANS.get(k, "") + " दूसरे शहरों का समय पेज पर।", h))
def build_hub():
    qa_html = "".join(f'<details class="qa" open><summary>{e(q)}</summary><p><strong>{e(a)}</strong> <a href="{u}">पूरी जानकारी</a></p></details>' for q, a, u in QA)
    add("tyohar-kab-hai.html", "त्योहार कब है? — एकादशी, पूर्णिमा, दशहरा, दिवाली के सीधे जवाब | OmKiran Bhakti",
        f"अगली एकादशी, पूर्णिमा, अमावस्या, अष्टमी-नवमी, दशहरा, करवा चौथ, दिवाली, छठ — हर ‘कब है’ सवाल का सीधा जवाब, रोज़ अपडेट।"[:160],
        band("त्योहार कब है? सीधे जवाब", f"हर ‘कब है’ सवाल का सीधा जवाब — नई दिल्ली के पंचांग से, हर दिन अपने-आप अपडेट। ({hdate_w(TODAY_D)} तक की जानकारी)", "त्योहार कब है", *ART["navdurga"], "त्योहार") +
        f'<section><div class="wrap faq">{qa_html}</div></section>',
        crumbs="त्योहार कब है", ld=[faq_ld([(q, a) for q, a, u in QA])], active="tyohar-calendar.html")


# surface the answer pages from the calendar and Navratri pages
_strip = ('<section class="hot"><div class="wrap"><ul class="hot-list"><li><a href="tyohar-kab-hai.html"><strong>त्योहार कब है? सीधे जवाब</strong><span>एकादशी, पूर्णिमा, अमावस्या और हर त्योहार</span></a></li>' +
          "".join(f'<li><a href="{h}"><strong>{e(t)}</strong><span>शहरवार समय</span></a></li>' for h, t, k in CITY_PAGES if (HOT_DATES.get(k) or (nxt_fest(k) or {"date": TODAY_D})["date"]) >= TODAY_D) +
          '</ul></div></section><section><div class="wrap">')
for _fp in ("tyohar-calendar.html", "navratri-2026.html", "aaj-ka-panchang.html"):
    if _fp in PAGES: PAGES[_fp] = PAGES[_fp].replace('<section><div class="wrap">', _strip, 1)

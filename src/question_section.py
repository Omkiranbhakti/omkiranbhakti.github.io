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

# ---------- Viral question: "नरक चतुर्दशी और दिवाली एक ही दिन क्यों?" ----------
_nc, _dw = nxt_fest("narak-chaturdashi"), nxt_fest("diwali")
if _nc and _dw:
    from festivals import find_dates as _fd
    ND, DD = _nc["date"], _dw["date"]; Y = DD.year; SAME = ND == DD
    _ch = next((x for x in SPANS if x[0] == 28 and abs((x[2].date() - ND).days) <= 1), None)
    _am = next((x for x in SPANS if x[0] == 29 and abs((x[1].date() - DD).days) <= 1), None)
    _srN, _ = _sr(ND); _, _ssD = _sr(DD)
    _aru = _srN - _dt.timedelta(minutes=96)
    def _fd1(k):
        x = nxt_fest(k); return x["date"] if x and abs((x["date"] - DD).days) < 6 else None
    _dh, _gv, _bd = _fd1("dhanteras"), _fd1("govardhan-puja"), _fd1("bhai-dooj")
    # same-day years (computed, a few back and ahead)
    _yrs = []
    for yy in range(Y - 4, Y + 4):
        try:
            r = _fd(_dt.date(yy, 10, 1), _dt.date(yy, 11, 30))
            a = [x["date"] for x in r.get("narak-chaturdashi", [])]; b = [x["date"] for x in r.get("diwali", [])]
            if a and b: _yrs.append((yy, a[0], b[0]))
        except Exception: pass
    _yr_rows = "".join(f'<tr><td><strong>{yy}</strong></td><td>{hdate(a)}</td><td>{hdate(b)}</td><td>{"हाँ, एक ही दिन" if a == b else "अलग-अलग दिन"}</td></tr>' for yy, a, b in _yrs)
    _same_yrs = [str(yy) for yy, a, b in _yrs if a == b]
    _dmu = CITY_ANS.get("diwali", "")
    if SAME:
        ans = (f"{Y} में नरक चतुर्दशी (रूप चौदस) और दिवाली दोनों <strong>{hdate_w(DD)}</strong> को हैं। "
               f"वजह तिथि का समय है: चतुर्दशी तिथि {_tm(_ch[1])} से {_tm(_ch[2])} तक है और उसके बाद अमावस्या {_tm(_am[2])} तक। "
               f"नरक चतुर्दशी का स्नान <strong>सूर्योदय से पहले</strong> होता है, जब चतुर्दशी हो — यह {hdate(ND)} की सुबह है। "
               f"दिवाली की लक्ष्मी पूजा <strong>प्रदोष काल (शाम)</strong> में होती है, जब अमावस्या हो — यह भी {hdate(DD)} की शाम है, क्योंकि अगले दिन शाम से पहले अमावस्या खत्म हो जाती है। "
               "इसलिए सुबह नरक चतुर्दशी और शाम को दिवाली — दोनों एक ही तारीख़ पर।")
    else:
        ans = (f"{Y} में नरक चतुर्दशी <strong>{hdate_w(ND)}</strong> को और दिवाली <strong>{hdate_w(DD)}</strong> को है — इस साल दोनों अलग-अलग दिन हैं। "
               "नीचे बताया गया है कि कुछ सालों में ये दोनों एक ही दिन क्यों पड़ते हैं।")
    tl = []
    if _dh: tl.append((_dh, "धनतेरस", "शाम को धन्वंतरि-कुबेर पूजा, ख़रीदारी और यम दीपदान (दक्षिण दिशा में दीया)।", "dhanteras-kab-hai.html"))
    if SAME and _ch and _ch[1].date() < ND:
        tl.append((_ch[1].date(), "चतुर्दशी की शाम (छोटी दिवाली के दीये)", f"इस शाम चतुर्दशी तिथि लगी रहती है ({ct12(_ch[1])} से)। जिन घरों में छोटी दिवाली की शाम दीये जलाने का रिवाज़ है, वे इसी शाम जलाते हैं।", None))
    tl.append((ND, "नरक चतुर्दशी — सुबह", f"सूर्योदय ({ct12(_srN)}) से पहले, अरुणोदय (लगभग {ct12(_aru)}) से तिल के तेल की मालिश, उबटन और अभ्यंग स्नान; यम तर्पण।", "narak-chaturdashi-kab-hai.html"))
    tl.append((DD, "दिवाली — शाम", f"प्रदोष काल में लक्ष्मी-गणेश पूजा। {_dmu} आधी रात को बंगाल में काली पूजा।", "diwali-lakshmi-puja-muhurat.html"))
    if SAME and _am and _am[2].date() > DD:
        tl.append((_am[2].date(), "कार्तिक अमावस्या (खाली दिन)", f"अमावस्या {ct12(_am[2])} तक है — सुबह स्नान-दान का दिन। लक्ष्मी पूजा इस शाम नहीं होती क्योंकि शाम तक अमावस्या खत्म हो जाती है।", None))
    if _gv: tl.append((_gv, "गोवर्धन पूजा / अन्नकूट", "प्रतिपदा तिथि में गोवर्धन पूजा और अन्नकूट का भोग।", "govardhan-puja-kab-hai.html"))
    if _bd: tl.append((_bd, "भाई दूज", "बहनें भाई को तिलक लगाती हैं।", "bhai-dooj-kab-hai.html"))
    tl.sort(key=lambda r: r[0])
    tl_rows = "".join(f'<tr><td class="big">{hdate_w(d)}</td><td><strong>{(f"<a href={chr(34)}{u}{chr(34)}>{t}</a>" if u else t)}</strong><br>{w}</td></tr>' for d, t, w, u in tl)
    faqs = [(f"{Y} में नरक चतुर्दशी और दिवाली एक ही दिन क्यों हैं?", re.sub("<[^>]+>", "", ans)),
            (f"{Y} में छोटी दिवाली कब है?",
             (f"नरक चतुर्दशी (रूप चौदस) का स्नान {hdate_w(ND)} की सुबह है और उसी शाम बड़ी दिवाली है। "
              + (f"जो लोग छोटी दिवाली की शाम दीये जलाते हैं, वे {hdate(_ch[1].date())} की शाम जलाते हैं, क्योंकि उस शाम चतुर्दशी तिथि लगी है।" if SAME and _ch and _ch[1].date() < ND else ""))
             if SAME else f"नरक चतुर्दशी / छोटी दिवाली {hdate_w(ND)} को है।"),
            ("नरक चतुर्दशी और दिवाली की तारीख़ कैसे तय होती है?", "नरक चतुर्दशी उस दिन मानी जाती है जिस दिन सूर्योदय से पहले (अरुणोदय में) चतुर्दशी तिथि हो, क्योंकि इसका मुख्य काम सुबह का अभ्यंग स्नान है। दिवाली उस दिन मनाई जाती है जिस दिन प्रदोष काल (सूर्यास्त के बाद लगभग ढाई घंटे) में अमावस्या तिथि हो। जब चतुर्दशी सुबह खत्म होकर दोपहर से अमावस्या लग जाती है, तो दोनों एक ही तारीख़ पर आ जाते हैं।"),
            ("क्या एक ही दिन नरक चतुर्दशी और लक्ष्मी पूजा दोनों कर सकते हैं?", "हाँ। सुबह सूर्योदय से पहले अभ्यंग स्नान और यम तर्पण करें, दिन में घर की सफ़ाई-सजावट, और शाम को शुभ मुहूर्त में लक्ष्मी-गणेश पूजा। दोनों के समय अलग हैं, इसलिए कोई टकराव नहीं।"),
            ("क्या ऐसा पहली बार हो रहा है?", (f"नहीं। नई दिल्ली के पंचांग के हिसाब से {', '.join(_same_yrs)} में भी दोनों एक ही दिन रहे या रहेंगे। यह तिथियों के घटने-बढ़ने से होता है, कोई दुर्लभ संयोग नहीं।" if _same_yrs else "नहीं, यह तिथियों के घटने-बढ़ने से कई सालों में होता है।")),
            ("दिवाली के अगले दिन गोवर्धन पूजा क्यों नहीं है?", (f"क्योंकि {hdate(DD)} के बाद वाले दिन सुबह भी अमावस्या है ({ct12(_am[2])} तक)। गोवर्धन पूजा प्रतिपदा तिथि में होती है, इसलिए वह {hdate_w(_gv)} को है। बीच का दिन कार्तिक अमावस्या (स्नान-दान) का है।" if SAME and _am and _gv and _am[2].date() > DD else "गोवर्धन पूजा प्रतिपदा तिथि में होती है; जिस साल दिवाली के अगले दिन सुबह तक अमावस्या रहती है, उस साल बीच में एक दिन का अंतर आ जाता है।")),
            (f"Why are Narak Chaturdashi and Diwali on the same day in {Y}?", (f"In {Y} Chaturdashi tithi prevails before sunrise on {DD.strftime('%d %B')} (Abhyanga Snan in the morning) and Amavasya prevails during Pradosh that same evening (Lakshmi Puja), so both fall on {DD.strftime('%d %B %Y')}." if SAME else f"In {Y} they fall on different days: Narak Chaturdashi {ND.strftime('%d %B')}, Diwali {DD.strftime('%d %B')}."))]
    _rel = ('<p class="lede"><a href="diwali-kab-hai.html">दिवाली कब है</a> · <a href="narak-chaturdashi-kab-hai.html">नरक चतुर्दशी कब है</a> · '
            '<a href="diwali-lakshmi-puja-muhurat.html">शहरवार लक्ष्मी पूजा मुहूर्त</a> · <a href="narak-chaturdashi-katha.html">नरक चतुर्दशी की कथा</a> · <a href="diwali-calendar.html">दिवाली के पाँच दिन</a></p>')
    body = (band(f"नरक चतुर्दशी और दिवाली एक ही दिन क्यों? ({Y})", ans, "नरक चतुर्दशी और दिवाली एक ही दिन", *FART.get("diwali", ART["navdurga"]), "दिवाली", extra=_rel)
            + f'<section><div class="wrap">{sec_head(f"दिवाली {Y}: किस दिन क्या करें", "नई दिल्ली के पंचांग के अनुसार")}'
            f'<div class="tbl"><table class="ptable"><tbody>{tl_rows}</tbody></table></div>'
            + (f'<table class="ptable"><tbody><tr><th>चतुर्दशी तिथि</th><td>{_tm(_ch[1])} से {_tm(_ch[2])} तक</td></tr><tr><th>अमावस्या तिथि</th><td>{_tm(_am[1])} से {_tm(_am[2])} तक</td></tr>'
               f'<tr><th>{hdate(ND)} सूर्योदय</th><td>{ct12(_srN)} (नरक चतुर्दशी का स्नान इससे पहले)</td></tr><tr><th>{hdate(DD)} सूर्यास्त</th><td>{ct12(_ssD)} (इसके बाद प्रदोष काल में लक्ष्मी पूजा)</td></tr></tbody></table>' if _ch and _am else "")
            + '<p class="note">नियम: नरक चतुर्दशी = सूर्योदय से पहले चतुर्दशी तिथि; दिवाली = प्रदोष काल में अमावस्या तिथि। आपके शहर में तिथि का समय कुछ मिनट अलग हो सकता है, लेकिन तारीख़ पूरे भारत में यही रहती है।</p></div></section>'
            + (f'<section><div class="wrap">{sec_head("किन सालों में दोनों एक ही दिन?", "नई दिल्ली के पंचांग से निकाला गया")}<div class="tbl"><table class="ptable"><thead><tr><th>साल</th><th>नरक चतुर्दशी</th><th>दिवाली</th><th>एक ही दिन?</th></tr></thead><tbody>{_yr_rows}</tbody></table></div></div></section>' if _yr_rows else "")
            + faq_html(faqs))
    add("narak-chaturdashi-aur-diwali-ek-hi-din-kyon.html",
        f"नरक चतुर्दशी और दिवाली एक ही दिन क्यों? {Y} में छोटी दिवाली कब है | OmKiran Bhakti",
        (f"{Y} में नरक चतुर्दशी और दिवाली दोनों {hdate(DD)} को क्यों हैं? तिथि का समय, सुबह अभ्यंग स्नान और शाम लक्ष्मी पूजा, छोटी दिवाली कब मनाएँ।" if SAME
         else f"नरक चतुर्दशी {hdate(ND)}, दिवाली {hdate(DD)}। ये दोनों कभी-कभी एक ही दिन क्यों पड़ते हैं — तिथि का नियम आसान भाषा में।")[:160],
        body, crumbs="नरक चतुर्दशी और दिवाली एक ही दिन", ld=[faq_ld(faqs)], active="tyohar-calendar.html")
    _hot = (f'<section class="hot"><div class="wrap"><ul class="hot-list"><li><a href="narak-chaturdashi-aur-diwali-ek-hi-din-kyon.html"><strong>नरक चतुर्दशी और दिवाली एक ही दिन क्यों?</strong>'
            f'<span>{Y} में छोटी दिवाली कब है — आसान जवाब</span></a></li></ul></div></section><section><div class="wrap">')
    for _fp in ("narak-chaturdashi-kab-hai.html", "diwali-kab-hai.html", "diwali-calendar.html", "diwali-lakshmi-puja-muhurat.html", "narak-chaturdashi-katha.html"):
        if _fp in PAGES: PAGES[_fp] = PAGES[_fp].replace('<section><div class="wrap">', _hot, 1)
    HOT_DATES["narak-diwali"] = DD

# ---------- Karwa Chauth: puja muhurat + "भद्रा है क्या?" box on the existing pages ----------
_kc = nxt_fest("karwa-chauth")
if _kc and _kc["date"] >= TODAY_D:
    try:
        from kaalcalc import bhadra as _bh
        KD = _kc["date"]; KY = KD.year
        _ksr, _kss = _sr(KD)
        _kp0, _kp1 = _kss, _kss + _dt.timedelta(minutes=76)
        _b = [(a, b) for a, b in _bh(_dt.datetime.combine(KD, _dt.time()) - _dt.timedelta(days=1), _dt.datetime.combine(KD, _dt.time()) + _dt.timedelta(days=2)) if b]
        _sr_n, _ss_n = _ksr.replace(tzinfo=None), _kss.replace(tzinfo=None)
        _night_end = _ss_n + _dt.timedelta(hours=5)
        _bday = [(a, b) for a, b in _b if a < _night_end and b > _sr_n - _dt.timedelta(hours=6)]
        _bclash = [(a, b) for a, b in _bday if a < _night_end and b > _ss_n]
        if _bclash:
            bh_txt = "हाँ — " + "; ".join(f"भद्रा {_tm(a)} से {_tm(b)} तक" for a, b in _bclash) + "। पूजा का समय अपने पंडित जी या स्थानीय पंचांग से पक्का कर लें।"
        elif _bday:
            a, b = _bday[0]
            bh_txt = f"नहीं। भद्रा {_tm(a)} से {_tm(b)} तक है — यानी व्रत के दिन सूर्योदय से पहले ही खत्म हो जाती है। शाम की पूजा और चंद्रोदय के समय भद्रा नहीं है।" if b <= _sr_n else f"भद्रा {_tm(a)} से {_tm(b)} तक है; शाम की पूजा और चंद्रोदय के समय भद्रा नहीं है।"
        else:
            bh_txt = "नहीं, करवा चौथ के दिन शाम की पूजा और चंद्रोदय के समय भद्रा नहीं है।"
        _kca = CITY_ANS.get("karwa-chauth", "")
        _kbox = (f'<section class="hot"><div class="wrap"><div class="faq">'
                 f'<details class="qa" open><summary>करवा चौथ {KY} पूजा का शुभ मुहूर्त क्या है?</summary><p><strong>{hdate_w(KD)} — {ct12(_kp0)} से {ct12(_kp1)} तक (नई दिल्ली)।</strong> ज़्यादातर पंचांग सूर्यास्त के बाद का लगभग सवा घंटा करवा माता की पूजा के लिए देते हैं। {("चाँद: " + _kca) if _kca else ""} <a href="karwa-chauth-chand-kab-niklega.html">अपने शहर का चंद्रोदय</a></p></details>'
                 f'<details class="qa" open><summary>करवा चौथ {KY} पर भद्रा है क्या?</summary><p><strong>{e(bh_txt)}</strong></p></details>'
                 f'</div></div></section><section><div class="wrap">')
        for _fp in ("karwa-chauth-kab-hai.html", "karwa-chauth-chand-kab-niklega.html", "karwa-chauth-vrat-katha.html"):
            if _fp in PAGES: PAGES[_fp] = PAGES[_fp].replace('<section><div class="wrap">', _kbox, 1)
        KC_QA = [(f"करवा चौथ {KY} पूजा मुहूर्त क्या है?", f"{hdate_w(KD)}, {ct12(_kp0)} से {ct12(_kp1)} तक (नई दिल्ली)।", "karwa-chauth-kab-hai.html"),
                 (f"करवा चौथ {KY} पर भद्रा है क्या?", bh_txt, "karwa-chauth-kab-hai.html")]
    except Exception as _ex:
        print("karwa box skipped:", _ex); KC_QA = []
else:
    KC_QA = []

# ---------- Q&A hub: every "कब है" question with a direct answer ----------
QA = list(KC_QA)
if NAVS:
    QA.append((f"नवरात्रि {Y0} में अष्टमी-नवमी कब है?", f"दुर्गा अष्टमी {hdate_w(n0['ad'])}, महानवमी {hdate_w(n0['nd'])}।", "navratri-ashtami-navami-kab-hai.html"))
    QA.append((f"क्या {Y0} में अष्टमी और नवमी एक साथ हैं?", "हाँ, दोनों एक ही दिन हैं।" if n0["same"] else "नहीं, दोनों अलग-अलग दिन हैं।", "navratri-ashtami-navami-kab-hai.html"))
if _nc and _dw and DD >= TODAY_D:
    QA.append((f"{Y} में नरक चतुर्दशी और दिवाली एक ही दिन क्यों?", (f"सुबह (सूर्योदय से पहले) चतुर्दशी और शाम (प्रदोष) में अमावस्या — दोनों {hdate_w(DD)} को।" if SAME else f"इस साल दोनों अलग दिन हैं: {hdate(ND)} और {hdate(DD)}।"), "narak-chaturdashi-aur-diwali-ek-hi-din-kyon.html"))
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

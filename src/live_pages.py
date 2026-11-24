# One page per temple for "<temple> live darshan today" searches (Google suggest, 27 Oct 2026: every temple has
# "live darshan today / aaj ke darshan / time / app / official channel"). live-darshan.html uses #hash links,
# which Google does not index separately, so each temple gets its own URL. Executed after darshan_section.py
# (uses LIVE, LIVE_KW, DARSHAN, _dg_player, DG_JS, lyrics_body, add, band, sec_head, faq_html, faq_ld, e, SITE, PAGES).

# live slug -> (short Hindi name used in headings/questions, page slug)
LP = {
 "ram-mandir-ayodhya": ("राम मंदिर अयोध्या", "ram-mandir-live-darshan.html"),
 "mahakaleshwar-ujjain": ("महाकाल उज्जैन", "mahakal-live-darshan.html"),
 "kashi-vishwanath-varanasi": ("काशी विश्वनाथ", "kashi-vishwanath-live-darshan.html"),
 "somnath": ("सोमनाथ", "somnath-live-darshan.html"),
 "omkareshwar": ("ओंकारेश्वर", "omkareshwar-live-darshan.html"),
 "trimbakeshwar": ("त्र्यंबकेश्वर", "trimbakeshwar-live-darshan.html"),
 "kedarnath-badrinath": ("केदारनाथ और बद्रीनाथ", "kedarnath-live-darshan.html"),
 "siddhivinayak-mumbai": ("सिद्धिविनायक", "siddhivinayak-live-darshan.html"),
 "vaishno-devi": ("वैष्णो देवी", "vaishno-devi-live-darshan.html"),
 "banke-bihari-vrindavan": ("बांके बिहारी", "banke-bihari-live-darshan.html"),
 "tirupati-balaji": ("तिरुपति बालाजी", "tirupati-live-darshan.html"),
 "shirdi-sai-baba": ("शिरडी साईं बाबा", "shirdi-sai-baba-live-darshan.html"),
 "khatu-shyam": ("खाटू श्याम", "khatu-shyam-live-darshan.html"),
 "dagdusheth-ganpati-pune": ("दगडूशेठ गणपति", "dagdusheth-ganpati-live-darshan.html"),
 "iskcon-vrindavan": ("इस्कॉन वृंदावन", "iskcon-vrindavan-live-darshan.html"),
 "iskcon-mayapur": ("इस्कॉन मायापुर", "iskcon-mayapur-live-darshan.html"),
 "ambaji-mata": ("अम्बाजी माता", "ambaji-live-darshan.html"),
 "naina-devi": ("नैना देवी", "naina-devi-live-darshan.html"),
 "pavagadh-mahakali": ("पावागढ़ महाकाली", "pavagadh-live-darshan.html"),
 "srisailam-mallikarjuna": ("मल्लिकार्जुन श्रीशैलम", "mallikarjuna-live-darshan.html"),
 "haridwar-ganga-aarti": ("हरिद्वार गंगा आरती", "haridwar-ganga-aarti-live.html"),
 "varanasi-ganga-aarti": ("वाराणसी गंगा आरती", "varanasi-ganga-aarti-live.html"),
 "golden-temple-amritsar": ("स्वर्ण मंदिर अमृतसर", "golden-temple-live-darshan.html"),
 "sabarimala-ayyappa": ("सबरीमला", "sabarimala-live-darshan.html"),
 "guruvayur": ("गुरुवायुर", "guruvayur-live-darshan.html"),
 "dwarkadhish": ("द्वारकाधीश", "dwarkadhish-live-darshan.html"),
 "shrinathji-nathdwara": ("श्रीनाथजी नाथद्वारा", "shrinathji-live-darshan.html"),
 "salasar-balaji": ("सालासर बालाजी", "salasar-balaji-live-darshan.html"),
 "pandharpur-vitthal": ("पंढरपुर विट्ठल", "pandharpur-live-darshan.html"),
 "dakshineswar-kali": ("दक्षिणेश्वर काली", "dakshineswar-live-darshan.html"),
 "sanwaliya-seth": ("सांवलिया सेठ", "sanwaliya-seth-live-darshan.html"),
 "govind-dev-ji-jaipur": ("गोविंद देव जी जयपुर", "govind-dev-ji-live-darshan.html"),
 "radha-rani-barsana": ("राधा रानी बरसाना", "barsana-radha-rani-live-darshan.html"),
 "jagannath-puri": ("जगन्नाथ पुरी", "jagannath-puri-live-darshan.html"),
 "kanaka-durga-vijayawada": ("कनक दुर्गा विजयवाड़ा", "kanaka-durga-live-darshan.html"),
 "annavaram-satyanarayan": ("अन्नवरम सत्यनारायण", "annavaram-live-darshan.html"),
 "simhachalam-narasimha": ("सिंहाचलम नरसिंह", "simhachalam-live-darshan.html"),
 "mahalakshmi-mumbai": ("महालक्ष्मी मुंबई", "mahalakshmi-mumbai-live-darshan.html"),
 "sankat-mochan-varanasi": ("संकट मोचन वाराणसी", "sankat-mochan-live-darshan.html"),
 "iskcon-juhu": ("इस्कॉन जुहू", "iskcon-juhu-live-darshan.html"),
 "iskcon-bangalore": ("इस्कॉन बेंगलुरु", "iskcon-bangalore-live-darshan.html"),
 "iskcon-delhi": ("इस्कॉन दिल्ली", "iskcon-delhi-live-darshan.html"),
}
_GUIDE_OF = {g["live"]: g for g in DARSHAN if g.get("live")}
_lp_rows = [d for d in LIVE if d[0] in LP]

def _lp_name(r):
    import re as _x
    m = _x.search(r"<title>([^<]+)</title>", PAGES.get(r, ""))
    return _x.split(r" — | \| | – |: ", m.group(1))[0].strip() if m else r


def _lp_en(slug):
    import re as _x
    for k in LIVE_KW.get(slug, []):
        if _x.search(r"[A-Za-z]", k) and "live" in k.lower():
            return _x.split(r"(?i) live\b", k)[0].strip()
    return ""

def _lp_glance(slug, g):
    """Short facts for the top of the page: from live_info.LI, else from the temple's guide (DARSHAN)."""
    d = dict(LI.get(slug) or {})
    if not d and g:
        for sec in g["sections"]:
            if sec[1] == "{T}" and len(sec) > 3 and "समय" in sec[0] and "aarti" not in d:
                d["aarti"] = " · ".join(f"{r[0]} {r[1]}" for r in sec[3][:5])
                if len(sec) > 4 and sec[4]: d["darshan"] = sec[4]
            elif sec[1] == "{T}" and len(sec) > 3 and "टिकट" in sec[0] and "ticket" not in d:
                d["ticket"] = " · ".join(f"{r[0]}: {r[1]}" for r in sec[3][:4])
        if g.get("official"): d["official"] = (g["official"], g["official"].split("//", 1)[-1].strip("/"))
    if not d: return "", {}
    rows = []
    if d.get("darshan"): rows.append(("दर्शन का समय", e(d["darshan"])))
    if d.get("aarti"): rows.append(("आरती का समय", e(d["aarti"])))
    if d.get("ticket"): rows.append(("टिकट / VIP दर्शन", e(d["ticket"])))
    if d.get("book"): rows.append(("ऑनलाइन बुकिंग", _ext(*d["book"])))
    if g: rows.append(("पूरी गाइड", f'<a href="{g["slug"]}">टिकट, बुकिंग, नियम और कैसे पहुँचें</a>'))
    if d.get("official"): rows.append(("आधिकारिक वेबसाइट", _ext(*d["official"])))
    if d.get("tip"): rows.append(("ध्यान दें", e(d["tip"])))
    tr = "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in rows)
    html = (f'<div class="tbl"><table class="ptable lp-glance"><tbody>{tr}</tbody></table></div>'
            f'<p class="small">समय मौसम और त्योहारों पर बदल जाता है। जानकारी की जाँच: {LI_CHECKED if slug in LI else DG_CHECKED}।</p>')
    return html, d

for slug, name, place, cid, cname, note, art, aarti, rel in _lp_rows:
    short, ps = LP[slug]
    g = _GUIDE_OF.get(slug)
    kws = LIVE_KW.get(slug, [])
    ans = (f"{e(name)}, {e(place)} के <strong>आज के लाइव दर्शन</strong> इसी पेज पर देखें — सीधे मंदिर के आधिकारिक YouTube चैनल “{e(cname)}” से। "
           "प्रसारण आरती और विशेष अवसरों पर लाइव आता है; उस समय लाइव न हो तो ‘दर्शन और आरती’ दबाएँ, मंदिर के सबसे नए दर्शन चलेंगे।")
    secs = ['<h2 class="k-h">आज के लाइव दर्शन</h2>' + _dg_player(slug, name)]
    gl, gd = _lp_glance(slug, g)
    if gl:
        secs.append(f'<h2 class="k-h">{e(short)} दर्शन का समय, आरती और टिकट — एक नज़र में</h2>' + gl)
    en = _lp_en(slug)
    kws = kws + [f"आज के {short} दर्शन", f"{short} दर्शन का समय", f"{short} आरती का समय", f"{short} VIP दर्शन टिकट बुकिंग", f"{short} आधिकारिक वेबसाइट"]
    if en:
        kws += [f"{en} darshan timings", f"{en} aarti time today", f"{en} VIP darshan ticket booking", f"{en} official website"]
    if g:
        secs.append(f'<p><a class="btn" href="{g["slug"]}">{e(short)}: टिकट, बुकिंग, समय और नियम</a></p>')
    if aarti:
        at, verses, au = aarti
        secs.append(f'<h2 class="k-h">साथ में पढ़ें: {e(at)}</h2><div class="lyrics">{lyrics_body(verses)}</div>'
                    f'<p><a class="btn ghost" href="{au}">अर्थ सहित पढ़ें</a></p>')
    if kws:
        secs.append('<h2 class="k-h">लोग ये भी खोजते हैं</h2><p>' + " · ".join(e(k) for k in kws) + "</p>")
    others = [d for d in _lp_rows if d[0] != slug]
    more = ('<ul class="library">' + "".join(f'<li><a href="{LP[d[0]][1]}"><strong>{e(LP[d[0]][0])}</strong><span>लाइव दर्शन</span></a></li>' for d in others)
            + '<li><a href="live-darshan.html"><strong>सभी मंदिर एक जगह</strong><span>लाइव दर्शन</span></a></li></ul>')
    rel = [r for r in rel if r in PAGES]
    read = ('<ul class="library">' + "".join(f'<li><a href="{r}"><strong>{e(_lp_name(r))}</strong><span>पढ़ें और सुनें</span></a></li>' for r in rel) + "</ul>") if rel else ""
    faqs = [(f"{short} के आज के लाइव दर्शन कहाँ देखें?", f"इसी पेज पर ऊपर ‘दर्शन शुरू करें’ दबाएँ। प्रसारण मंदिर के आधिकारिक YouTube चैनल “{cname}” से चलता है — {note}।"),
            (f"{short} लाइव दर्शन किस समय होता है?", (f"आरती के समय ({gd['aarti']}) प्रसारण सबसे ज़्यादा आता है। " if gd.get("aarti") else "") + "मंदिर आमतौर पर सुबह-शाम की आरती और विशेष उत्सवों पर लाइव प्रसारण करते हैं। बाकी समय ‘दर्शन और आरती’ दबाने पर मंदिर के हाल के दर्शन चलते हैं।"),
            (f"{short} लाइव दर्शन का आधिकारिक चैनल कौन सा है?", f"“{cname}” — {note}।"),
            (f"क्या {short} के लाइव दर्शन देखने के लिए कोई app चाहिए?", "नहीं। यह पेज मोबाइल के ब्राउज़र में ही खुलता है; कोई app या लॉग-इन नहीं चाहिए।"),
            ("लाइव प्रसारण न दिखे तो क्या करें?", "हो सकता है मंदिर उस समय लाइव न हो। ‘दर्शन और आरती’ दबाएँ, या आरती के समय दोबारा पेज खोलें।")]
    if gd.get("darshan"):
        faqs.insert(1, (f"{short} में दर्शन का समय क्या है?", gd["darshan"] + "। त्योहारों पर समय बदल सकता है।"))
    if gd.get("ticket"):
        faqs.append((f"{short} में VIP या शीघ्र दर्शन का टिकट कितने का है?", gd["ticket"] + (f"। बुकिंग: {gd['book'][1]}" if gd.get("book") else "") + "।"))
    if gd.get("official"):
        faqs.append((f"{short} मंदिर की आधिकारिक वेबसाइट कौन सी है?", f"{gd['official'][1]} — बुकिंग और दान सिर्फ़ आधिकारिक वेबसाइट से करें, किसी एजेंट या WhatsApp नंबर को पैसे न भेजें।"))
    if g:
        faqs.append((f"{short} में दर्शन की बुकिंग कैसे करें?", f"टिकट, बुकिंग, समय और नियम की पूरी जानकारी हमारी <a href=\"{g['slug']}\">{short} दर्शन गाइड</a> में है।"))
    body = (band(f"{short} लाइव दर्शन: आज के दर्शन और आरती", ans, f"{short} लाइव दर्शन") +
            '<article><section><div class="wrap prose katha dg-page">' + "".join(secs) + "</div></section></article>" +
            (('<section class="no-print"><div class="wrap">' + sec_head("साथ में पढ़ें") + read + "</div></section>") if read else "") +
            '<section class="band no-print"><div class="wrap">' + sec_head("दूसरे मंदिरों के लाइव दर्शन") + more + "</div></section>" +
            faq_html(faqs) + DG_JS)
    temple = {"@type": "HinduTemple", "name": name, "address": {"@type": "PostalAddress", "addressLocality": place, "addressCountry": "IN"}}
    if gd.get("official"): temple["sameAs"] = gd["official"][0]
    ld = [{"@type": "WebPage", "name": f"{short} लाइव दर्शन", "about": temple}, faq_ld(faqs)]
    add(ps, (f"{short} लाइव दर्शन आज — दर्शन का समय, आरती टाइम" + (", VIP टिकट बुकिंग" if gd.get("book") or gd.get("ticket") else "") + " | OmKiran Bhakti") if gd else f"{short} लाइव दर्शन आज — आधिकारिक प्रसारण, आरती और आज के दर्शन | OmKiran Bhakti",
        f"{name} ({place}) के आज के लाइव दर्शन, सीधे आधिकारिक चैनल से।" + (f" दर्शन का समय: {gd['darshan']}।" if gd.get("darshan") else "") + " आरती टाइम, टिकट, बुकिंग और आधिकारिक वेबसाइट एक नज़र में।",
        body, crumbs=f"{short} लाइव दर्शन", ld=ld, active="live-darshan.html")

# guide pages -> their live page; live-darshan hub -> every temple page
for slug, g in _GUIDE_OF.items():
    if g["slug"] in PAGES and slug in LP:
        PAGES[g["slug"]] = PAGES[g["slug"]].replace('<h2 class="k-h">आज के लाइव दर्शन</h2>',
            f'<h2 class="k-h">आज के लाइव दर्शन</h2><p><a href="{LP[slug][1]}">{e(LP[slug][0])} लाइव दर्शन का अलग पेज</a></p>', 1)
if "live-darshan.html" in PAGES:
    _row = ('<section class="no-print"><div class="wrap">' + sec_head("हर मंदिर का अलग लाइव दर्शन पेज") + '<ul class="library">' +
            "".join(f'<li><a href="{LP[d[0]][1]}"><strong>{e(LP[d[0]][0])}</strong><span>लाइव दर्शन</span></a></li>' for d in _lp_rows) + "</ul></div></section>")
    PAGES["live-darshan.html"] = PAGES["live-darshan.html"].replace('<section class="faq">', _row + '<section class="faq">', 1)

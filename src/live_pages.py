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

for slug, name, place, cid, cname, note, art, aarti, rel in _lp_rows:
    short, ps = LP[slug]
    g = _GUIDE_OF.get(slug)
    kws = LIVE_KW.get(slug, [])
    ans = (f"{e(name)}, {e(place)} के <strong>आज के लाइव दर्शन</strong> इसी पेज पर देखें — सीधे मंदिर के आधिकारिक YouTube चैनल “{e(cname)}” से। "
           "प्रसारण आरती और विशेष अवसरों पर लाइव आता है; उस समय लाइव न हो तो ‘दर्शन और आरती’ दबाएँ, मंदिर के सबसे नए दर्शन चलेंगे।")
    secs = ['<h2 class="k-h">आज के लाइव दर्शन</h2>' + _dg_player(slug, name)]
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
            (f"{short} लाइव दर्शन किस समय होता है?", "मंदिर आमतौर पर सुबह-शाम की आरती और विशेष उत्सवों पर लाइव प्रसारण करते हैं। बाकी समय ‘दर्शन और आरती’ दबाने पर मंदिर के हाल के दर्शन चलते हैं।"),
            (f"{short} लाइव दर्शन का आधिकारिक चैनल कौन सा है?", f"“{cname}” — {note}।"),
            (f"क्या {short} के लाइव दर्शन देखने के लिए कोई app चाहिए?", "नहीं। यह पेज मोबाइल के ब्राउज़र में ही खुलता है; कोई app या लॉग-इन नहीं चाहिए।"),
            ("लाइव प्रसारण न दिखे तो क्या करें?", "हो सकता है मंदिर उस समय लाइव न हो। ‘दर्शन और आरती’ दबाएँ, या आरती के समय दोबारा पेज खोलें।")]
    if g:
        faqs.append((f"{short} में दर्शन की बुकिंग कैसे करें?", f"टिकट, बुकिंग, समय और नियम की पूरी जानकारी हमारी <a href=\"{g['slug']}\">{short} दर्शन गाइड</a> में है।"))
    body = (band(f"{short} लाइव दर्शन: आज के दर्शन और आरती", ans, f"{short} लाइव दर्शन") +
            '<article><section><div class="wrap prose katha dg-page">' + "".join(secs) + "</div></section></article>" +
            (('<section class="no-print"><div class="wrap">' + sec_head("साथ में पढ़ें") + read + "</div></section>") if read else "") +
            '<section class="band no-print"><div class="wrap">' + sec_head("दूसरे मंदिरों के लाइव दर्शन") + more + "</div></section>" +
            faq_html(faqs) + DG_JS)
    temple = {"@type": "HinduTemple", "name": name, "address": {"@type": "PostalAddress", "addressLocality": place, "addressCountry": "IN"}}
    ld = [{"@type": "WebPage", "name": f"{short} लाइव दर्शन", "about": temple}, faq_ld(faqs)]
    add(ps, f"{short} लाइव दर्शन आज — आधिकारिक प्रसारण, आरती और आज के दर्शन | OmKiran Bhakti",
        f"{name} ({place}) के आज के लाइव दर्शन और आरती, सीधे मंदिर के आधिकारिक YouTube चैनल से। कोई app नहीं चाहिए — मोबाइल पर यहीं देखें।",
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

"""SEO landing page for the 3D Kaal-Chakra (kaal-chakra/index.html).
Reads the event rows and katha straight from the wheel, so both stay in sync."""
import os, re, json, html

def _e(s): return html.escape(s, quote=True)

def _slug(r): return re.sub(r'[^a-z0-9]+', '-', r.lower()).strip('-')

ROW = re.compile(r"^\[(-?[\d.]+|NOW),'(\w+)','([^']*)','([^']*)','([^']*)','([^']*)','([^']*)',\"([^\"]*)\"\],?$", re.M)

def _rows(root):
    h = open(os.path.join(root, "kaal-chakra/index.html"), encoding="utf8").read()
    out = []
    for m in ROW.finditer(h):
        y, c, t, p, d, kw, r, w = m.groups()
        out.append(dict(y=y, c=c, t=t, p=p, d=d, slug=_slug(r)))
    imgs = set(json.load(open(os.path.join(root, "kaal-chakra/img/pick.json"), encoding="utf8")))
    k = open(os.path.join(root, "kaal-chakra/katha.js"), encoding="utf8").read()
    K = json.loads(k[k.index("{"):k.rindex("}") + 1])
    return out, imgs, K

def _ylabel(y):
    if y == "NOW": return "आज"
    v = float(y)
    if v < -3102: return "प्राचीन काल (पुराण-काल)"
    if v < 0: return f"ई.पू. {int(-v)}"
    return f"{int(v)} ई."

FAQS = [
 ("हिंदू काल-चक्र क्या है?", "सनातन धर्म में समय को एक सीधी रेखा नहीं, घूमता हुआ चक्र माना गया है। सृष्टि बनती है, चार युग — सत्ययुग, त्रेता, द्वापर और कलियुग — आते-जाते हैं, और फिर नई सृष्टि होती है। इसी को काल-चक्र कहते हैं। हमारा 3D काल-चक्र इसी विचार पर बनी एक इंटरैक्टिव टाइमलाइन है।"),
 ("चार युग कितने लंबे होते हैं?", "पुराणों के अनुसार सत्ययुग 17,28,000 वर्ष, त्रेतायुग 12,96,000 वर्ष, द्वापरयुग 8,64,000 वर्ष और कलियुग 4,32,000 वर्ष का होता है। चारों मिलकर एक महायुग (43,20,000 वर्ष) बनाते हैं।"),
 ("अभी कौन सा युग चल रहा है?", "परंपरागत गणना के अनुसार अभी कलियुग चल रहा है, जो ईसा पूर्व 3102 में श्रीकृष्ण के स्वधाम जाने के साथ शुरू हुआ। अब तक लगभग 5,128 वर्ष बीते हैं; हम कलियुग के पहले चरण में हैं।"),
 ("Hindu Time Machine क्या है?", "यह सनातन धर्म का इंटरैक्टिव काल-चक्र है — एक ‘टाइम मशीन’ जिसमें आप पहिया घुमाकर सृष्टि से कल्कि अवतार तक किसी भी युग की घटना पर पहुँच सकते हैं। यह हिंदी में है और मोबाइल पर भी चलता है।"),
 ("कल्प और मन्वंतर क्या हैं?", "ब्रह्मा जी का एक दिन एक कल्प है, जिसमें एक हज़ार महायुग और चौदह मन्वंतर होते हैं। हमारा कल्प श्वेत वराह कल्प है और मन्वंतर सातवाँ — वैवस्वत मन्वंतर।"),
 ("सनातन धर्म की टाइम मशीन कैसे चलाएँ?", "<a href=\"kaal-chakra/\">3D काल-चक्र</a> खोलें, ‘प्रवेश करें’ दबाएँ और पहिये को उँगली से घुमाएँ। हर बिंदु एक घटना है — कार्ड पर चित्र और छोटा परिचय आता है, ‘पूरी कथा’ में विस्तार से कथा, महत्व, तीर्थ और स्रोत मिलते हैं।"),
 ("कल्कि अवतार कब होगा?", "भागवत पुराण के अनुसार कलियुग के अंत में, जब धर्म लगभग मिट जाएगा, भगवान विष्णु शंभल ग्राम में विष्णुयश के घर कल्कि रूप में जन्म लेंगे और फिर सत्ययुग लौटेगा।"),
 ("इस काल-चक्र में कौन-कौन सी घटनाएँ हैं?", "सृष्टि और वराह अवतार से लेकर ध्रुव, समुद्र मंथन, नृसिंह, वामन, परशुराम, पूरी रामायण, महाभारत और गीता, बड़े आचार्य-संत (शंकराचार्य से विवेकानंद तक), ज्योतिर्लिंग और चार धाम जैसे तीर्थ, और कलियुग की भविष्यवाणियाँ व कल्कि अवतार — 150 से ज़्यादा घटनाएँ, और लगातार नई जुड़ रही हैं।"),
]

INTRO = """<p class="lede"><b>हिंदू काल-चक्र</b> — यानी <b>सनातन धर्म की टाइम मशीन</b>। यहाँ आप सृष्टि के आरंभ से लेकर श्रीराम, श्रीकृष्ण, महाभारत, गीता, संतों और तीर्थों से होते हुए कल्कि अवतार और सत्ययुग की वापसी तक की यात्रा कर सकते हैं — एक घूमते हुए 3D चक्र पर, कथा और चित्रों के साथ।</p>
<p>सनातन परंपरा में समय गोल घूमता है। एक <b>महायुग</b> में चार युग होते हैं — <b>सत्ययुग, त्रेतायुग, द्वापरयुग और कलियुग</b>। एक हज़ार महायुग मिलकर ब्रह्मा जी का एक दिन, यानी एक <b>कल्प</b> बनाते हैं, और एक कल्प में चौदह <b>मनु</b> होते हैं। हमारा कल्प श्वेत वराह कल्प है, मन्वंतर वैवस्वत है, और अभी 28वें महायुग का कलियुग चल रहा है — यही बात हर पूजा के संकल्प में बोली जाती है।</p>
<p>नीचे हर युग की घटनाएँ क्रम से दी गई हैं। किसी भी घटना पर ‘काल-चक्र में देखें’ दबाएँगे तो 3D चक्र सीधे उसी घटना पर रुकेगा। <span lang="en"><b>Hindu Time Machine</b> (Sanatan Time Machine / Hindu Kaal Chakra) — an interactive 3D timeline of Hindu (Sanatan) Dharma in Hindi, from creation to the Kalki avatar. Works on mobile.</span></p>"""

def build(root):
    rows, imgs, K = _rows(root)
    # group by yuga markers
    marks = {"सत्ययुग का आरंभ": "सत्ययुग", "त्रेतायुग का आरंभ": "त्रेतायुग", "द्वापरयुग का आरंभ": "द्वापरयुग", "कलियुग का आरंभ": "कलियुग"}
    groups, cur = [], ("सृष्टि, कल्प और मन्वंतर", [])
    groups.append(cur)
    for r in rows:
        if r["t"] in marks:
            cur = (marks[r["t"]], []); groups.append(cur)
        if r["y"] == "NOW":
            cur = ("आप यहाँ हैं — आगे की भविष्यवाणियाँ (कलियुग का भविष्य और कल्कि)", []); groups.append(cur); continue
        cur[1].append(r)
    toc, secs, n = [], [], 0
    for gi, (g, items) in enumerate(groups):
        if not items: continue
        gid = f"y{gi}"
        toc.append(f'<li><a href="#{gid}">{_e(g)}</a> <small>({len(items)})</small></li>')
        lis = []
        for r in items:
            n += 1
            k = K.get(r["t"])
            first = k[0].split("\n\n")[0] if k else r["d"]
            img = (f'<img src="kaal-chakra/img/{r["slug"]}.webp" alt="{_e(r["t"])}" loading="lazy" width="120" height="120">' if r["slug"] in imgs else "")
            lis.append(f'<li class="kc-ev" id="{r["slug"]}">{img}<div><h3>{_e(r["t"])}</h3>'
                       f'<p class="kc-meta">{_e(_ylabel(r["y"]))} · {_e(r["p"])}</p><p>{_e(first)}</p>'
                       f'<a class="kc-go" href="kaal-chakra/#{r["slug"]}">काल-चक्र में देखें →</a></div></li>')
        secs.append(f'<section id="{gid}"><h2>{_e(g)}</h2><ul class="kc-list">{"".join(lis)}</ul></section>')
    faq_h = "".join(f"<details><summary>{_e(q)}</summary><p>{a}</p></details>" for q, a in FAQS)
    css = """<style>.kc-cta{display:inline-block;margin:.6rem 0 1rem;padding:.8rem 1.3rem;border-radius:999px;background:#f0c25e;color:#1a0f05!important;font-weight:600;text-decoration:none}
.kc-toc{columns:2;padding-left:1.1rem}.kc-list{list-style:none;padding:0;margin:0}.kc-ev{display:flex;gap:14px;padding:14px 0;border-bottom:1px solid #8884}
.kc-ev img{width:96px;height:96px;object-fit:cover;border-radius:12px;flex:none}.kc-ev h3{margin:0 0 .2rem;font-size:1.08rem}.kc-meta{margin:0;opacity:.75;font-size:.88rem}.kc-ev p{margin:.25rem 0}
.kc-go{font-size:.92rem;font-weight:600}@media(max-width:560px){.kc-toc{columns:1}.kc-ev img{width:72px;height:72px}}</style>"""
    body = (f'{css}<section class="night scallop page-band"><div class="wrap"><div><nav class="crumbs-in" aria-label="breadcrumb"><a href="index.html">होम</a> / हिंदू काल-चक्र</nav>'
            f'<h1 class="gold-type">हिंदू काल-चक्र — सनातन धर्म की टाइम मशीन</h1>'
            f'<p class="answer">सृष्टि से कल्कि अवतार तक {n} घटनाएँ — युगों के क्रम में, कथा और चित्रों के साथ। 3D चक्र को घुमाइए और सनातन इतिहास की यात्रा कीजिए।</p>'
            f'<a class="kc-cta" href="kaal-chakra/">🕉️ 3D काल-चक्र खोलें</a></div>'
            f'<a href="kaal-chakra/"><img src="assets/og-kaal-chakra.jpg" alt="हिंदू काल-चक्र — सनातन धर्म की टाइम मशीन" width="600" height="315" style="width:100%;height:auto;border-radius:16px"></a></div></section>'
            f'<section><div class="wrap prose">{INTRO}<h2>युगों के क्रम में</h2><ul class="kc-toc">{"".join(toc)}</ul>'
            f'{"".join(secs)}<p><a class="kc-cta" href="kaal-chakra/">🕉️ 3D काल-चक्र खोलें</a> <a href="kaal-chakra/credits.html">चित्र-श्रेय</a></p></div></section>'
            f'<section class="faq"><div class="wrap"><h2>अक्सर पूछे जाने वाले सवाल</h2>{faq_h}</div></section>')
    title = "हिंदू काल-चक्र (Hindu Time Machine) — सनातन धर्म की टाइम मशीन"
    desc = f"हिंदू काल-चक्र (सनातन काल-चक्र): सत्ययुग, त्रेता, द्वापर और कलियुग की {n} घटनाएँ — वराह, समुद्र मंथन, रामायण, महाभारत, गीता, संत, तीर्थ और कल्कि अवतार। 3D टाइम मशीन में घुमाकर देखें।"
    item_ld = {"@type": "ItemList", "name": "हिंदू काल-चक्र की घटनाएँ", "numberOfItems": n,
               "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": r["t"], "url": f"https://omkiranbhakti.com/hindu-kaal-chakra.html#{r['slug']}"}
                                   for i, r in enumerate([r for g in groups for r in g[1]][:200])]}
    faq_ld = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in FAQS]}
    return title, desc, body, [item_ld, faq_ld]

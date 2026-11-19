"""English edition of the Kaal-Chakra (19 Nov 2026).
A: en/kaal-chakra/index.html — the same 3D wheel, built from kaal-chakra/index.html with English UI
   and English event text from src/kc_en.json ({slug: [title, place, short description]}).
   Assets stay in /kaal-chakra/ (a <base> tag points there). Full English katha can be added later
   as kaal-chakra/katha-en.js (window.KATHA_EN = {slug: [katha, message, tirtha, source]}).
B: en/hindu-kaal-chakra.html — English landing page body (wrapped and finished by build.py).
Events missing from kc_en.json fall back to Roman letters, so new Hindi batches never break the build."""
import os, re, json, html
import kaal_chakra_page as KP

SITE = "https://omkiranbhakti.com/"
WHEEL_EN = SITE + "en/kaal-chakra/"
LAND_EN = SITE + "en/hindu-kaal-chakra.html"

def load(root):
    p = os.path.join(root, "src", "kc_en.json")
    return json.load(open(p, encoding="utf8")) if os.path.exists(p) else {}

def _js(s): return s.replace("\\", "\\\\").replace("'", "\\'")

def ev_en(r, T, roman):
    v = T.get(r["slug"])
    if v: return v
    ro = lambda s: roman(s).rstrip(" ।॥") if s else s
    return [ro(r["t"]), ro(r["p"]), ro(r["d"])]

DESC = ("Spin the Hindu Kaal Chakra — the time machine of Sanatan Dharma. Creation, the Varaha avatar, Samudra Manthan, "
        "the Ramayana, the Mahabharata, the Gita, saints, temples and tirthas, up to the Kalki avatar: 150+ events with pictures.")

HEAD = f'''<title>Hindu Time Machine — Hindu Kaal Chakra | 3D Timeline of Sanatan Dharma</title>
<meta name="description" content="{DESC}">
<meta name="theme-color" content="#0d0805">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{WHEEL_EN}">
<link rel="alternate" hreflang="en" href="{WHEEL_EN}"><link rel="alternate" hreflang="hi" href="{SITE}kaal-chakra/"><link rel="alternate" hreflang="x-default" href="{SITE}kaal-chakra/">
<meta name="keywords" content="Hindu Time Machine, Sanatan Time Machine, Hindu Kaal Chakra, Sanatan Kaal Chakra, Hindu timeline, Hindu dharma timeline, yuga cycle, Satya Yuga Treta Dvapara Kali Yuga, four yugas, time machine of Hindu dharma, Kalki avatar">
<meta property="og:type" content="website"><meta property="og:site_name" content="OmKiran Bhakti"><meta property="og:locale" content="en_IN">
<meta property="og:title" content="Hindu Kaal Chakra — the Time Machine of Sanatan Dharma | 3D Interactive Timeline"><meta property="og:description" content="{DESC}"><meta property="og:url" content="{WHEEL_EN}">
<meta property="og:image" content="{SITE}assets/og-kaal-chakra.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{SITE}assets/og-kaal-chakra.jpg">
<link rel="icon" href="../assets/favicon-48.png" type="image/png" sizes="48x48">
<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": [
 {"@type": "WebApplication", "@id": WHEEL_EN + "#app", "name": "Hindu Kaal Chakra — the Time Machine of Sanatan Dharma",
  "alternateName": ["Hindu Time Machine", "Sanatan Time Machine", "Sanatan Kaal Chakra", "Hindu Dharma Timeline"], "url": WHEEL_EN,
  "description": DESC, "inLanguage": "en-IN", "applicationCategory": "EducationalApplication", "operatingSystem": "Any (web browser)",
  "offers": {"@type": "Offer", "price": "0", "priceCurrency": "INR"}, "isPartOf": {"@id": SITE + "#website"},
  "publisher": {"@type": "Organization", "name": "OmKiran Bhakti", "url": SITE}, "image": SITE + "assets/og-kaal-chakra.jpg"},
 {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "en/"},
  {"@type": "ListItem", "position": 2, "name": "Hindu Kaal Chakra", "item": LAND_EN},
  {"@type": "ListItem", "position": 3, "name": "3D Kaal Chakra", "item": WHEEL_EN}]}]}, ensure_ascii=False)}</script>'''

# exact Hindi → English swaps in the page shell and its script (UI is frozen: text only)
UI = [
 ('<html lang="hi">', '<html lang="en">'),
 ('<small>ॐ ओमकिरण भक्ति</small><div class="serif">काल-चक्र</div>', '<small>ॐ OmKiran Bhakti</small><div class="serif">Kaal Chakra</div>'),
 ('title="आवाज़"', 'title="Sound"'), ('title="तानपुरा"', 'title="Tanpura"'), ('title="सभी कथाएँ"', 'title="All events"'),
 ('📖 पूरी कथा', '📖 Read more'), ('📲 भेजें', '📲 Share'),
 ('👆 चक्र को उँगली से घुमाइए', '👆 Spin the wheel with your finger'),
 ('title="शुरुआत (Home)"', 'title="Start (Home)"'), ('title="आज"', 'title="Today"'), ('title="कोई भी कथा (R)"', 'title="Random event (R)"'),
 ('title="अंत (End)"', 'title="End (End)"'), ('title="ज़ूम (+)"', 'title="Zoom in (+)"'), ('title="ज़ूम कम (−)"', 'title="Zoom out (−)"'),
 ('aria-label="पिछली कथा"', 'aria-label="Previous event"'), ('aria-label="अगली कथा"', 'aria-label="Next event"'),
 ('placeholder="खोजें — राम, कृष्ण, shiv, kumbh…"', 'placeholder="Search — Ram, Krishna, Shiv, Kumbh…"'),
 ('<a href="method.html">📐 यह काल-चक्र कैसे बना?</a> · <a href="credits.html">चित्र-श्रेय</a> · <a href="../en/kaal-chakra/" lang="en" hreflang="en">English</a>',
  '<a href="method.html">📐 How this wheel was made (Hindi)</a> · <a href="credits.html">Image credits</a> · <a href="./" lang="hi" hreflang="hi">हिंदी</a>'),
 ('<h1>काल-चक्र</h1>', '<h1>Kaal Chakra</h1>'),
 ('<p>सृष्टि के आरंभ से कल्कि अवतार और सत्ययुग की वापसी तक — सनातन की हर कथा, एक घूमते चक्र पर।</p>',
  '<p>From the dawn of creation to the Kalki avatar and the return of Satya Yuga — the story of Sanatan Dharma on one turning wheel.</p>'),
 ('🙏 प्रवेश करें', '🙏 Enter'), ('🎧 हेडफ़ोन के साथ सबसे सुंदर अनुभव', '🎧 Best with headphones'),
 ("c:['युग-काल'", "c:['Yugas & time'"), ("a:['अवतार'", "a:['Avatars'"), ("sh:['शिव-शक्ति'", "sh:['Shiva & Shakti'"),
 ("r:['राम कथा'", "r:['Ram katha'"), ("k:['कृष्ण कथा'", "k:['Krishna katha'"), ("m:['महाभारत'", "m:['Mahabharata'"),
 ("s:['ऋषि-भक्त'", "s:['Rishis & saints'"), ("v:['राजवंश'", "v:['Dynasties'"), ("t:['तीर्थ-मंदिर'", "t:['Temples & tirthas'"),
 ("u:['पर्व-कुंभ'", "u:['Festivals & Kumbh'"), ("b:['भविष्यवाणी'", "b:['Prophecies'"), ("n:['आज'", "n:['Today'"),
 ("'आदि काल','#d6b27a','#2e2010','कल्प और मन्वंतरों का आरंभ'", "'Beginning','#d6b27a','#2e2010','Start of the kalpa and manvantaras'"),
 ("'सत्ययुग','#ffd24d','#4a3508','17,28,000 वर्ष • धर्म चारों चरणों पर'", "'Satya Yuga','#ffd24d','#4a3508','1,728,000 years • dharma on all four legs'"),
 ("'त्रेतायुग','#ff8a3d','#4a2008','12,96,000 वर्ष • धर्म तीन चरणों पर'", "'Treta Yuga','#ff8a3d','#4a2008','1,296,000 years • dharma on three legs'"),
 ("'द्वापरयुग','#5aa8ff','#0c1f40','8,64,000 वर्ष • धर्म दो चरणों पर'", "'Dvapara Yuga','#5aa8ff','#0c1f40','864,000 years • dharma on two legs'"),
 ("'कलियुग','#ff5a5f','#3a0d10','4,32,000 वर्ष • धर्म एक चरण पर'", "'Kali Yuga','#ff5a5f','#3a0d10','432,000 years • dharma on one leg'"),
 ("'आज','#ff4d6d','#3a0d18','आप यहाँ हैं'", "'Today','#ff4d6d','#3a0d18','You are here'"),
 ("'भविष्य','#b77cff','#1f0f3a','पुराणों की भविष्यवाणियाँ'", "'Future','#b77cff','#1f0f3a','Prophecies of the Puranas'"),
 ("'पुनः सत्ययुग','#ffd24d','#4a3508','काल-चक्र फिर से घूमता है'", "'New Satya Yuga','#ffd24d','#4a3508','The wheel of time turns again'"),
 ("return'2026 ई.'", "return'2026 CE'"),
 ("return'लगभग '+(+(a/1e7).toFixed(1))+' करोड़ वर्ष पूर्व'", "return'about '+(+(a/1e7).toFixed(1))+' crore years ago'"),
 ("return'लगभग '+(+(a/1e5).toFixed(1))+' लाख वर्ष पूर्व'", "return'about '+(+(a/1e5).toFixed(1))+' lakh years ago'"),
 ("return'ई.पू. '+fmt(-y)}", "return fmt(-y)+' BCE'}"), ("return fmt(y)+' ई.'}", "return fmt(y)+' CE'}"),
 ("['n','आज']", "['n','Today']"), ("['u','निर्धारित']", "['u','Scheduled']"), ("['b','भविष्यवाणी']", "['b','Prophecy']"),
 ("['h','ऐतिहासिक']", "['h','Historical']"), ("['p','पारंपरिक']", "['p','Traditional']"),
 ("'चित्र: Wikimedia Commons'", "'Image: Wikimedia Commons'"),
 ("काल-चक्र घुमाइए, सृष्टि से कल्कि तक की हर कथा 👇\\nhttps://omkiranbhakti.com/kaal-chakra/#", "Spin the Hindu Kaal Chakra — from creation to Kalki 👇\\nhttps://omkiranbhakti.com/en/kaal-chakra/#"),
 ("target=\"_blank\" rel=\"noopener\">▶️ ${kw} भजन</a>", "target=\"_blank\" rel=\"noopener\">▶️ Bhajans</a>"),
 ("rel=\"noopener sponsored\">🪔 पूजा सामग्री</a>", "rel=\"noopener sponsored\">🪔 Puja items</a>"),
 ("📲 WhatsApp पर भेजें", "📲 Share on WhatsApp"), ("📚 विकिपीडिया", "📚 Wikipedia"),
 ("const k=K&&K[e.t]", "const k=K&&K[slug(e)]"),
 ("<h3 class=\"ks\">🙏 महत्व / संदेश</h3>", "<h3 class=\"ks\">🙏 Meaning / message</h3>"),
 ("<h3 class=\"ks\">📍 तीर्थ / कहाँ मनाया जाता है</h3>", "<h3 class=\"ks\">📍 Where it is honoured</h3>"),
 ("<h3 class=\"ks\">📜 स्रोत</h3>", "<h3 class=\"ks\">📜 Sources</h3>"),
 ("if(window.KATHA)return r(window.KATHA);const s=document.createElement('script');s.src='katha.js?v=3';s.onload=()=>r(window.KATHA)",
  "if(window.KATHA_EN)return r(window.KATHA_EN);const s=document.createElement('script');s.src='katha-en.js?v=1';s.onload=()=>r(window.KATHA_EN)"),
 ("कुछ नहीं मिला 🙏", "Nothing found 🙏"), (">सभी ${N}</button>", ">All ${N}</button>"),
 ("${C[FC][1]} सिर्फ़ ${C[FC][0]}", "${C[FC][1]} Only ${C[FC][0]}"),
 ("`कलियुग: <b>${fmt(el)}</b> वर्ष बीते • <b>${fmt(KL-el)}</b> वर्ष शेष`", "`Kali Yuga: <b>${fmt(el)}</b> years passed • <b>${fmt(KL-el)}</b> years left`"),
]

def wheel(root, roman):
    """English 3D wheel HTML, or raises if the Hindi page changed so much that a swap no longer matches."""
    T = load(root)
    h = open(os.path.join(root, "kaal-chakra/index.html"), encoding="utf8").read()
    a = h.index("<title>"); b = h.index("</script>", h.index('application/ld+json')) + len("</script>")
    h = h[:a] + '<base href="/kaal-chakra/">\n' + HEAD + h[b:]
    for hi, en in UI:
        if hi not in h: raise ValueError("kaal_chakra_en: text not found: " + hi[:60])
        h = h.replace(hi, en)
    def row(m):
        y, c, t, p, d, kw, r, w = m.groups()
        tt, pp, dd = ev_en(dict(t=t, p=p, d=d, slug=KP._slug(r)), T, roman)
        return f"[{y},'{c}','{_js(tt)}','{_js(pp)}','{_js(dd)}','{kw}','{r}',\"{w}\"]" + ("," if m.group(0).endswith(",") else "")
    if not os.path.exists(os.path.join(root, "kaal-chakra/katha-en.js")):   # no English katha yet: the sheet shows the short text only
        h = h.replace("function loadKatha(){return kP||", "function loadKatha(){return Promise.resolve(null);return kP||", 1)
    h, n = KP.ROW.subn(row, h)
    if n < 100: raise ValueError("kaal_chakra_en: event rows not found")
    return h

FAQS = [
 ("What is the Hindu Kaal Chakra?", "In Sanatan Dharma, time is not a straight line but a turning wheel. Creation arises, the four yugas — Satya, Treta, Dvapara and Kali — come and go, and then creation begins anew. This is the Kaal Chakra, the wheel of time. Our 3D Kaal Chakra is an interactive timeline built on this idea."),
 ("How long are the four yugas?", "According to the Puranas, Satya Yuga lasts 1,728,000 years, Treta Yuga 1,296,000 years, Dvapara Yuga 864,000 years and Kali Yuga 432,000 years. Together they make one mahayuga of 4,320,000 years."),
 ("Which yuga is running now?", "By the traditional reckoning we live in Kali Yuga, which began in 3102 BCE when Shri Krishna left the world. About 5,128 years have passed; we are in the first quarter of Kali Yuga."),
 ("What is the Hindu Time Machine?", "It is an interactive Kaal Chakra of Sanatan Dharma — a ‘time machine’ where you spin the wheel to reach any event of any yuga, from creation to the Kalki avatar. It works on mobile too."),
 ("What are a kalpa and a manvantara?", "One day of Lord Brahma is a kalpa, made of a thousand mahayugas and fourteen manvantaras. Our kalpa is the Shveta Varaha Kalpa, and the manvantara is the seventh — the Vaivasvata Manvantara."),
 ("How do I use the time machine of Sanatan Dharma?", "Open the <a href=\"" + WHEEL_EN + "\">3D Kaal Chakra</a>, tap ‘Enter’ and spin the wheel with your finger. Every point is an event; its card shows a picture and a short introduction."),
 ("When will the Kalki avatar come?", "According to the Bhagavata Purana, at the end of Kali Yuga, when dharma has almost vanished, Lord Vishnu will be born as Kalki in the village of Shambhala, in the home of Vishnuyasha, and Satya Yuga will return."),
 ("Which events are in this Kaal Chakra?", "From creation and the Varaha avatar to Dhruva, the Samudra Manthan, Narasimha, Vamana, Parashurama, the whole Ramayana, the Mahabharata and the Gita, the great acharyas and saints (from Shankaracharya to Vivekananda), tirthas such as the Jyotirlingas and the Char Dham, and the prophecies of Kali Yuga and the Kalki avatar — more than 150 events, with more being added."),
]
GROUPS = {"start": "Creation, Kalpa and Manvantara", "सत्ययुग": "Satya Yuga", "त्रेतायुग": "Treta Yuga", "द्वापरयुग": "Dvapara Yuga",
          "कलियुग": "Kali Yuga", "now": "You are here — the prophecies ahead (the future of Kali Yuga and Kalki)"}

def _ylabel(y):
    if y == "NOW": return "Today"
    v = float(y)
    if v < -3102: return "Ancient (Puranic age)"
    if v < 0: return f"{int(-v)} BCE"
    return f"{int(v)} CE"

def landing(root, roman):
    """Body, title, description and JSON-LD for en/hindu-kaal-chakra.html (links are absolute: finish() leaves them alone)."""
    rows, imgs, _ = KP._rows(root)
    T = load(root)
    e = lambda s: html.escape(s, quote=True)
    marks = {"सत्ययुग का आरंभ": "सत्ययुग", "त्रेतायुग का आरंभ": "त्रेतायुग", "द्वापरयुग का आरंभ": "द्वापरयुग", "कलियुग का आरंभ": "कलियुग"}
    groups, cur = [], (GROUPS["start"], []); groups.append(cur)
    for r in rows:
        if r["t"] in marks: cur = (GROUPS[marks[r["t"]]], []); groups.append(cur)
        if r["y"] == "NOW": cur = (GROUPS["now"], []); groups.append(cur); continue
        cur[1].append(r)
    toc, secs, n, flat = [], [], 0, []
    for gi, (g, items) in enumerate(groups):
        if not items: continue
        toc.append(f'<li><a href="#y{gi}">{e(g)}</a> <small>({len(items)})</small></li>')
        lis = []
        for r in items:
            n += 1; t, p, d = ev_en(r, T, roman); flat.append((t, r["slug"]))
            img = (f'<img src="{SITE}kaal-chakra/img/{r["slug"]}.webp" alt="{e(t)}" loading="lazy" width="120" height="120">' if r["slug"] in imgs else "")
            lis.append(f'<li class="kc-ev" id="{r["slug"]}">{img}<div><h3>{e(t)}</h3><p class="kc-meta">{e(_ylabel(r["y"]))} · {e(p)}</p>'
                       f'<p>{e(d)}</p><a class="kc-go" href="{WHEEL_EN}#{r["slug"]}">See it on the Kaal Chakra →</a></div></li>')
        secs.append(f'<section id="y{gi}"><h2>{e(g)}</h2><ul class="kc-list">{"".join(lis)}</ul></section>')
    css = """<style>.kc-cta{display:inline-block;margin:.6rem 0 1rem;padding:.8rem 1.3rem;border-radius:999px;background:#f0c25e;color:#1a0f05!important;font-weight:600;text-decoration:none}
.kc-toc{columns:2;padding-left:1.1rem}.kc-list{list-style:none;padding:0;margin:0}.kc-ev{display:flex;gap:14px;padding:14px 0;border-bottom:1px solid #8884}
.kc-ev img{width:96px;height:96px;object-fit:cover;border-radius:12px;flex:none}.kc-ev h3{margin:0 0 .2rem;font-size:1.08rem}.kc-meta{margin:0;opacity:.75;font-size:.88rem}.kc-ev p{margin:.25rem 0}
.kc-go{font-size:.92rem;font-weight:600}@media(max-width:560px){.kc-toc{columns:1}.kc-ev img{width:72px;height:72px}}</style>"""
    intro = f"""<p class="lede">The <b>Hindu Kaal Chakra</b> — the <b>time machine of Sanatan Dharma</b>. Travel from the beginning of creation through Shri Ram, Shri Krishna, the Mahabharata, the Gita, the saints and the tirthas, all the way to the Kalki avatar and the return of Satya Yuga — on a turning 3D wheel, with pictures.</p>
<p>In the Sanatan tradition time moves in circles. One <b>mahayuga</b> holds four yugas — <b>Satya, Treta, Dvapara and Kali Yuga</b>. A thousand mahayugas make one day of Lord Brahma, a <b>kalpa</b>, and each kalpa has fourteen <b>Manus</b>. Our kalpa is the Shveta Varaha Kalpa, the manvantara is the Vaivasvata, and the Kali Yuga of the 28th mahayuga is running now — the very words spoken in the sankalpa of every puja.</p>
<p>Below, the events of each yuga are listed in order. Tap ‘See it on the Kaal Chakra’ on any event and the 3D wheel stops right on it. Holy names are written in Roman letters.</p>"""
    faq_h = "".join(f"<details><summary>{e(q)}</summary><p>{a}</p></details>" for q, a in FAQS)
    body = (f'{css}<section class="night scallop page-band"><div class="wrap"><div><nav class="crumbs-in" aria-label="breadcrumb"><a href="{SITE}en/">Home</a> / Hindu Kaal Chakra</nav>'
            f'<h1 class="gold-type">Hindu Kaal Chakra — the Time Machine of Sanatan Dharma</h1>'
            f'<p class="answer">{n} events from creation to the Kalki avatar — in the order of the yugas, with pictures. Spin the 3D wheel and travel through Sanatan history.</p>'
            f'<a class="kc-cta" href="{WHEEL_EN}">🕉️ Open the 3D Kaal Chakra</a></div>'
            f'<a href="{WHEEL_EN}"><img src="{SITE}assets/og-kaal-chakra.jpg" alt="Hindu Kaal Chakra — the time machine of Sanatan Dharma" width="600" height="315" style="width:100%;height:auto;border-radius:16px"></a></div></section>'
            f'<section><div class="wrap prose">{intro}<h2>In the order of the yugas</h2><ul class="kc-toc">{"".join(toc)}</ul>'
            f'{"".join(secs)}<p><a class="kc-cta" href="{WHEEL_EN}">🕉️ Open the 3D Kaal Chakra</a> <a href="{SITE}kaal-chakra/credits.html">Image credits</a></p></div></section>'
            f'<section class="faq"><div class="wrap"><h2>Frequently asked questions</h2>{faq_h}</div></section>')
    title = "Hindu Kaal Chakra (Hindu Time Machine) — the Time Machine of Sanatan Dharma"
    desc = (f"Hindu Kaal Chakra (Sanatan Kaal Chakra): {n} events of Satya, Treta, Dvapara and Kali Yuga — Varaha, Samudra Manthan, "
            "Ramayana, Mahabharata, Gita, saints, tirthas and the Kalki avatar. Spin the 3D time machine.")
    item_ld = {"@type": "ItemList", "name": "Events of the Hindu Kaal Chakra", "numberOfItems": n,
               "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": t, "url": f"{LAND_EN}#{s}"} for i, (t, s) in enumerate(flat[:200])]}
    faq_ld = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in FAQS]}
    return title, desc, body, [item_ld, faq_ld]

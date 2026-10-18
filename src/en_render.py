# English edition renderer. Executed inside build.py (uses e, SITE, YT, WA_CH, CSSV, JSV, OG_DEFAULT, _roman, json).
EN_KIND = {"doha": "Doha", "chaupai": "Chaupai", "shloka": "Shloka"}

def en_head(title, desc, url, hi_url, ld):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{url}"><link rel="alternate" hreflang="hi" href="{hi_url}"><link rel="alternate" hreflang="x-default" href="{hi_url}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#1C2350">
<meta property="og:type" content="website"><meta property="og:site_name" content="OmKiran Bhakti">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{OG_DEFAULT}"><meta property="og:locale" content="en_IN">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="../assets/favicon-48.png" type="image/png" sizes="48x48"><link rel="apple-touch-icon" href="../assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Mukta:wght@400;500;600&family=Tiro+Devanagari+Hindi&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../styles.css?v={CSSV}">
<script>try{{var t=localStorage.getItem('okb-theme');if(t)document.documentElement.setAttribute('data-theme',t)}}catch(e){{}}</script>
<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@graph":ld},ensure_ascii=False)}</script>
</head>
<body class="en">
<a class="skip" href="#main">Skip to content</a>
<header class="site-head"><div class="toran" aria-hidden="true"></div>
<div class="wrap head-row">
<a class="brand" href="index.html"><img src="../assets/mark-168.webp" alt="OmKiran Bhakti" width="120" height="82"><span><b>OmKiran Bhakti</b><small>Aarti, Chalisa &amp; Mantra — in English</small></span></a>
<nav class="nav" aria-label="Main"><a href="index.html">All prayers</a><a href="{YT}">YouTube</a></nav>
<div class="lang-sw" role="group" aria-label="Language / भाषा"><a href="{hi_url}?lang=hi" lang="hi" hreflang="hi">हिंदी</a><a class="on" lang="en" aria-current="true">EN</a></div>
<button class="theme-btn" aria-label="Switch day / night colours">◐</button>
<button class="menu-btn" aria-label="Menu" aria-expanded="false">☰</button>
</div></header>'''

def en_foot():
    return f'''<footer class="site-foot"><div class="wrap foot-grid">
<div><h2>OmKiran Bhakti</h2><p>Hindu devotional music and prayers — aartis, chalisas and mantras with lyrics and meaning. Watch and sing along on our <a href="{YT}">YouTube channel</a>.</p></div>
<div><h2>Prayers in English</h2><ul>{"".join(f'<li><a href="{s}">{e(EN[s]["name"])}</a></li>' for s in EN)}</ul></div>
</div><div class="wrap join-strip"><span>🙏 Daily panchang, festivals and new bhajans on your phone</span><a class="wa-join" href="{WA_CH}" target="_blank" rel="noopener">WhatsApp channel</a><a class="yt-join" href="https://www.youtube.com/@OmKiranBhakti?sub_confirmation=1" target="_blank" rel="noopener">▶ YouTube Subscribe</a></div>
<div class="wrap fine">© {datetime.date.today().year} OmKiran Bhakti. Traditional texts are public heritage; meanings and music are by OmKiran Bhakti.</div></footer>
<script src="../script.js?v={JSV}" defer></script>
</body></html>'''

def en_lyrics_page(slug, verses, vid_ids):
    d = EN[slug]
    assert len(d["m"]) == len(verses), f"{slug}: {len(d['m'])} meanings for {len(verses)} verses"
    url, hi_url = SITE + "en/" + slug, SITE + slug
    out, n, last = [], 0, None
    for (kind, text, _), mean in zip(verses, d["m"]):
        if kind != last and kind in EN_KIND:
            out.append(f'<p class="section-label">{EN_KIND[kind]}</p>'); last = kind
        if kind in ("mantra", "dhyan"):
            head, body = text.split("\n", 1)
            out.append(f'<div class="verse mantra"><h3 class="m-name">{e(_roman(head))}</h3><p class="line ro" lang="hi-Latn" translate="no">{e(_roman(body)).replace(chr(10),"<br>")}</p>'
                       f'<p class="line-dev" lang="hi" translate="no">{e(body)}</p><p class="mean">{e(mean)}</p></div>'); continue
        no = ""
        if kind in ("chaupai", "shloka"): n += 1; no = str(n)
        out.append(f'<div class="verse {kind}"><span class="no">{no}</span><p class="line ro" lang="hi-Latn" translate="no">{e(_roman(text)).replace(chr(10),"<br>")}</p>'
                   f'<p class="line-dev" lang="hi" translate="no">{e(text)}</p><p class="mean">{e(mean)}</p></div>')
    faqs = d.get("faqs", [])
    faq = ("<section><div class=\"wrap\"><h2>Frequently asked questions</h2>" +
           "".join(f"<details class=\"faq\"><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in faqs) + "</div></section>") if faqs else ""
    vids = (f'<section class="no-print"><div class="wrap"><h2>Sing along — videos</h2>{video_cards(vid_ids)}</div></section>') if vid_ids else ""
    ld = [{"@type":"WebPage","@id":url+"#page","url":url,"name":d["title"],"description":d["desc"],"inLanguage":"en"},
          {"@type":"CreativeWork","name":d["name"],"inLanguage":"hi","text":"\n".join(v[1] for v in verses),
           **({"author":{"@type":"Person","name":d["author"]}} if d.get("author") else {}),"isAccessibleForFree":True},
          {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Prayers in English","item":SITE+"en/"},
                                                       {"@type":"ListItem","position":2,"name":d["name"],"item":url}]}]
    if faqs: ld.append({"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q, a in faqs]})
    body = f'''<nav class="crumbs wrap" aria-label="breadcrumb"><a href="index.html">Prayers in English</a> / {e(d["name"])}</nav>
<main id="main"><article>
<section class="band"><div class="wrap"><h1>{e(d["name"])} — Lyrics in English with Meaning</h1><p class="answer">{e(d["answer"])}</p><p class="lede">{e(d.get("intro",""))}</p></div></section>
<section class="paath-sec"><div class="wrap"><div class="paath-main">
<div class="reader-tools no-print" role="toolbar" aria-label="Reading options">
<button class="chip" data-meaning aria-pressed="true">Show meaning</button>
<button class="chip" data-dev aria-pressed="true">Show Hindi script</button>
<button class="chip" data-size="0.15" aria-label="Bigger text">A+</button><button class="chip" data-size="-0.15" aria-label="Smaller text">A−</button>
<button class="chip" data-print>Print / PDF</button></div>
<div class="lyrics en-lyrics">{"".join(out)}</div>
<p class="note no-print">The text is traditional and wording varies slightly by region. The English meanings are written by OmKiran Bhakti. <a href="{hi_url}?lang=hi">Read this page in Hindi</a>.</p>
</div></div></section></article>
{vids}
{faq}
</main>'''
    EN_OUT[slug] = en_head(d["title"], d["desc"], url, hi_url, ld) + body + en_foot()

def en_index():
    url = SITE + "en/"
    items = "".join(f'<li><a href="{s}"><div><strong>{e(EN[s]["name"])}</strong><span>{e(EN[s]["sub"])}</span></div></a></li>' for s in EN)
    ld = [{"@type":"CollectionPage","@id":url+"#page","url":url,"name":"Hindu prayers in English — OmKiran Bhakti","inLanguage":"en"}]
    body = f'''<main id="main"><section class="band"><div class="wrap"><h1>Hindu Prayers in English — Lyrics with Meaning</h1>
<p class="answer">Aartis, chalisas and mantras with the lyrics in English letters, the original Hindi script, and a simple English meaning of every line. More prayers are added regularly.</p></div></section>
<section><div class="wrap"><ul class="paath">{items}</ul>
<p class="note">Looking for something else? Our full library is in Hindi — <a href="../aarti-mantra.html?lang=hi">open the Hindi site</a>.</p></div></section></main>'''
    EN_OUT["index.html"] = en_head("Hindu Prayers in English — Aarti, Chalisa & Mantra Lyrics with Meaning | OmKiran Bhakti",
        "Hanuman Chalisa, Om Jai Jagdish Hare, Ganesh, Shiv and Durga aartis with lyrics in English and line-by-line English meaning.",
        url, SITE, ld) + body + en_foot()

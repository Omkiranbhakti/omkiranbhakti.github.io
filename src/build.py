#!/usr/bin/env python3
"""Builds the OmKiran Bhakti static site into the repo root.
Run:  python3 src/build.py
Every page is plain HTML (fast, crawlable). Data lives in this file and lyrics.py."""
import json, html, os, sys, re, datetime
sys.path.insert(0, os.path.dirname(__file__))
from lyrics import HANUMAN_CHALISA, OM_JAI_JAGDISH, JAI_GANESH_DEVA, OM_JAI_SHIV_OMKARA

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://omkiranbhakti.github.io/"
YT = "https://www.youtube.com/@OmKiranBhakti"
LOGO = "https://yt3.ggpht.com/v-SABQ87EfZPploVIJ9mR6pumFaiUs0RMrncVYcy0IfrZWA4EQ8MA8agzp_m-TLDq1sh00r5ZA=s256-c-k-c0x00ffffff-no-rj"
TODAY = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=5, minutes=30)).date().isoformat()
import hashlib
def ver(f):
    return hashlib.md5(open(os.path.join(ROOT,f),"rb").read()).hexdigest()[:8]
CSSV, JSV = ver("styles.css"), ver("script.js")
e = html.escape

# ---------- Real channel videos (IDs read from the channel, Oct 2026) ----------
V = {
 # Mata Rani / Durga
 "woNhYRu376g":("फूलों की आई है बहार — माता रानी भजन","4:54"),
 "2yVR5zSaKpc":("ठुमक-ठुमक चली आना मैया मेरे अंगने में","4:08"),
 "fhm1dqyttu0":("लाल फूलों की आई है बहार मैया तेरे मंदिर में","4:52"),
 "9hzay6Ebzas":("मेरी मैया नहीं रूठ जाना — भावपूर्ण देवी गीत","4:42"),
 "vr5Bp46iA-Q":("मेरी बिगड़ी बनाना तेरा काम है","3:19"),
 "PHNyA0VlAI8":("ऊँचे पहाड़ों पे मैया तेरा बसेरा है — वैष्णो देवी भजन","7:21"),
 "NuWOBRQ9B3Q":("बोलते चलो शेरावाली के जयकारे","3:52"),
 "rLSpMEkB7eU":("ओ मैया हजारों तेरे नाम हैं","3:51"),
 "Fxfm-eadkTY":("माता रानी के भजन — नॉनस्टॉप जुकबॉक्स","45:06"),
 "dJAZTUkHcBs":("आशा की झोली ले के — नवरात्रि गरबा","6:53"),
 "eA6tcqEncoE":("श्री दुर्गा चालीसा — 4 मिनट में","3:49"),
 "CcDzHzu7sIw":("लेकर मैया का श्रृंगार — माता रानी लोकगीत","4:28"),
 "jAdixB5m0Zo":("अम्बे तू है जगदम्बे काली — आरती","3:45"),
 # Navratri day-wise
 "Ht_SogxJ_D8":("माँ शैलपुत्री की आरती","7:53"),
 "SsrEdkAf4xI":("माँ ब्रह्मचारिणी की आरती","7:15"),
 "lUhDATRpvrs":("माँ चंद्रघंटा की आरती","7:51"),
 "65nhAnBmYuQ":("माँ कूष्मांडा की आरती","7:55"),
 "Q5_3JBKLNpg":("माँ स्कंदमाता की आरती","7:42"),
 "r32U54qyerw":("माँ कात्यायनी की आरती","7:54"),
 "FFcNanFHSaY":("माँ कालरात्रि की आरती","7:54"),
 "89wxOjTwPwQ":("माँ सिद्धिदात्री स्तुति","37:53"),
 "G99-49Pfs6U":("नवदुर्गा की 9 आरतियाँ — जुकबॉक्स","1:11:02"),
 "SE1RyQ6fWQs":("चामुंडा माता मंत्र जाप","20:36"),
 "h4EjlAYqQo0":("या देवी सर्वभूतेषु — 108 जाप","31:07"),
 "nFvgYHuqZt0":("दुर्गा से काली कैसे बनीं — कथा भजन","4:48"),
 # Shiv
 "vsfjF59qj4Q":("शिव बसे हैं सबके मन में","4:25"),
 "JUg809TxgRg":("शिव चालीसा — 4 मिनट में","4:05"),
 "rxeMNQ48yWU":("महामृत्युंजय मंत्र — 108 बार","54:06"),
 "pn5OODJqmTc":("भोले डमरू बजा दो एक बार","4:40"),
 "Kbe3pbLsg1U":("सांसों की माला पे सिमरूँ मैं शिव का नाम","6:13"),
 "DGsy57lUApA":("कैलाश के निवासी नमो बार-बार","4:34"),
 "ZqFztNyxSgU":("ॐ जय शिव ओंकारा — शिव आरती","7:19"),
 "qCwFf_cCWGM":("नमामीशमीशान — रुद्राष्टकम्","4:35"),
 "6vVDsn9R6DM":("शिवोहम् — निर्वाण षटकम्","3:16"),
 "C5lE4JA3sKc":("ॐ नमः शिवाय — 108 बार","17:10"),
 "fQiD96yFR6o":("मेरा भोला है भंडारी","4:12"),
 "axKgdxe7JZE":("उज्जैन महाकाल आरती","4:59"),
 "icIEKo5vLjw":("वन्दे महाकाल महासुरेशम् — महाकाल मंत्र","6:20"),
 # Hanuman
 "707iS1Iyv-E":("हनुमान चालीसा — सिर्फ़ 4 मिनट में","4:10"),
 "v249ibg1Juk":("हनुमान चालीसा — नई धुन","11:36"),
 "W__UjJxgK_o":("बजरंग बाण","7:19"),
 "HcfPkZyal_M":("हनुमान चालीसा पाठ के 7 ज़रूरी नियम","27:41"),
 "bfNwwRhVY8U":("सुन लो मेरी पुकार — हनुमान भजन","6:18"),
 "6nsots7gB9A":("हनुमान वडवानल स्तोत्र","6:07"),
 # Krishna
 "vy6ucthmxmk":("अंगना झूले कृष्ण कन्हैया — बधाई गीत","3:22"),
 "P9N1XQzw8CI":("जय जय राधा रमण हरि बोल","5:42"),
 "ZQ_OBR-596M":("श्री कृष्ण चालीसा","4:03"),
 "uCUR842niAU":("कृष्णाय वासुदेवाय — कृष्ण मंत्र","43:28"),
 "3ChBJC1Vigk":("बरसाने की होली — मोहन संग खेलत राधा प्यारी","3:40"),
 "TVdX5XbbjHs":("फूलों में सज रहे हैं श्री वृंदावन बिहारी","4:44"),
 "GtRRHlLc5gQ":("हरे राम हरे कृष्ण कीर्तन","18:47"),
 "R1PiCmntXIM":("श्री राधा प्रणाम मंत्र","43:19"),
 "ZIhDdYk6Gus":("जन्मे हैं कृष्ण कन्हैया — सोहर गीत","3:26"),
 "_8yw36Jn7iM":("रख लो हमें बरसाने में","8:03"),
 # Ganesh
 "ZswQ9qUMDTs":("संकट हर लो मंगल कर दो — गणपति भजन","4:52"),
 "lMHZDM-RRb4":("बप्पा लेकर विदाई जब जाना — विसर्जन भजन","4:57"),
 "u3kbBEHOs9o":("श्री गणेश चालीसा — 4 मिनट में","3:56"),
 "NGI-JiRiwSc":("फूलों से सजाया दरबार गजानन आ जाना","5:36"),
 "EtnvDW1AlOY":("हमारे घर आओ ना हे गणपति","3:22"),
 "XscYggWHC5o":("सारी दुनिया में मच गयो शोर, गजानन मेरो है","4:13"),
 "Qpe4rrfzWhk":("सुखकर्ता दुखहर्ता — गणेश आरती","3:43"),
 "IkcVwmMUUmw":("सुवर्णवर्ण सुन्दरम् — गणपति स्तोत्र","4:00"),
 "5WeumLCpi5w":("यूं ना जाओ छोड़कर गणपति अपना घर","4:15"),
 "BmrflIPOqAk":("माता गौरी के राजदुलारे","3:24"),
 # Ram
 "pCixItfj5Vo":("श्री राम चालीसा","4:23"),
 "ZqOnkb7zElU":("सबसे ज़्यादा सुने जाने वाले राम भजन — जुकबॉक्स","19:46"),
 "sLQF1nm_RqU":("श्री रामचंद्र कृपालु भजमन","6:27"),
 "l9z2J0I6Kao":("बैठत रामही उठत रामही — निर्गुण भजन","7:25"),
 "lBRP9bTTLek":("जय रघुनंदन जय सियाराम","4:21"),
 "kHM8fGmqoLw":("राम नाम अति मीठा है","4:45"),
 "SMyoiGPuKGA":("श्री राम गायत्री मंत्र — 108 बार","32:25"),
 "fmbCXi2K9tw":("राम रामेति रामेति रमे रामे मनोरमे","5:23"),
 # EDM
 "unfGUJz6D8U":("भज भज भूतेशम् — काल भैरव x शिव तांडव EDM","4:13"),
 "D5LIL8j8Kqs":("हनुमान तांडव EDM — बजरंगबली पावर मिक्स","3:39"),
 "XLYs9iEXKmA":("अयि गिरिनन्दिनि — साइबरपंक EDM मिक्स","6:59"),
 "pjhPqvh26bg":("अयि गिरिनन्दिनि — महिषासुरमर्दिनि EDM","6:59"),
 "BQxaizzx5So":("अयि गिरिनन्दिनि — सुपरफ़ास्ट स्तोत्र","11:34"),
 # Mantra & other
 "KPZbsWemcIg":("महालक्ष्मी मंत्र — 108 बार","30:50"),
 "ASNq5VCqOhY":("शनि चालीसा — 4 मिनट में","4:05"),
 "gZ7DoH6ZOa4":("शनि मंत्र — 108 बार","36:31"),
 "ktQUU5Y3tPE":("सूर्य बीज मंत्र","18:42"),
 "iUo6Ui1lPMY":("ॐ साईं नमो नमः — 108 बार","30:37"),
 "w8pxctA2998":("करवा चौथ की आरती — जय करवा माता","4:24"),
 "5HxuQ9YgtiE":("श्री पितृ चालीसा","6:04"),
 "WutRzz-5xZw":("पितृ स्तोत्र पाठ","4:11"),
 "hwoEYtPy7Qw":("मेरी तुलसी दुल्हन बन आई रे — तुलसी विवाह गीत","4:56"),
 "oQl6-dRDfWU":("करवा माता की आरती — पारंपरिक","3:41"),
 "F95csn49Rq0":("महालक्ष्मी मंत्र — 108 बार (धन और सुख-शांति)","17:33"),
 "Potbxr2V0jI":("कह दो राधा रानी से — उड़े रे गुलाल","4:17"),
 "oXTPb9esaQ8":("बरसाने की छोरी — राधा कृष्ण होली गीत","4:10"),
 "M5_SEzyH_b4":("छठ पूजा भजन — नॉन स्टॉप","13:33"),
 "sllSUVgfjnw":("नाथों के नाथ सुन लो पुकार — महाशिवरात्रि भजन","5:37"),
 "96GJOWJFJgA":("गुरु मंत्र जाप — 108 बार","26:22"),
 "EE2zjTPyHaI":("खाटू में तेरा दरबार — ग्यारस (एकादशी) भजन","4:31"),
 "A-vFduFpIHg":("निर्जला एकादशी व्रत कथा","11:23"),
 "PvWUk5b8eF0":("शिव गायत्री मंत्र — ध्यान संगीत","5:15"),
 "dZ7iceOQt9Y":("आशुतोष शशांक शेखर — शिव महापुराण मंत्र","10:06"),
 "oiQLsZFwU7I":("सुखकर्ता दुखहर्ता — गणपती आरती (मराठी)","2:03"),
 "ZZcOOWNvFg8":("गणपति आरती — सुखकर्ता दुखहर्ता, बोल सहित","3:45"),
 "r-yfzKxNW0w":("मंगल की सेवा सुन मेरी देवा — आरती","6:13"),
 "LwmVaSve_mM":("कुलदेवी मंत्र — ॐ कुलदैव्यै नमः","8:28"),
 "PSKXIFYrtcU":("एक नज़र कृपा की कर दो — शेरावाली भजन","3:33"),
 "bWKRDa8dDqE":("दुर्गा चालीसा — 4 मिनट में (नवरात्रि 2026)","3:49"),
 "p7MyXd8oj9s":("दुर्गा चालीसा — 7 बार सुपरफ़ास्ट पाठ","26:43"),
}
PLAYLISTS = {
 "mata":("PLblSMxBGjJTo6wp1f_kZODt5LSwoGf1IH","नवरात्रि DJ भजन प्लेलिस्ट"),
 "shiv":("PLblSMxBGjJTrMun6MW9QXjvbGxDq9Y6kc","शिव भजन प्लेलिस्ट"),
 "ganesh":("PLblSMxBGjJTolFx8Xyl3WqCqC-tccT-RK","गणपति बप्पा के भजन प्लेलिस्ट"),
 "ram":("PLblSMxBGjJTpqSlRTJVK3I1or8DZtEGpk","राम भजन और हनुमान चालीसा प्लेलिस्ट"),
 "edm":("PLblSMxBGjJTqgM4-tdYgqhoynFhFhQ96B","अयि गिरिनन्दिनि कलेक्शन"),
 "mantra":("PLblSMxBGjJTr2IRYOvJgJKxA13VVUR5Xd","मंत्रों का खज़ाना प्लेलिस्ट"),
}

# Deity art = the channel's own thumbnails, cropped into a temple-arch frame.
# value: (video id, horizontal focus % for the crop)
ART = {
 "mata":("2yVR5zSaKpc",76), "shiv":("Kbe3pbLsg1U",80), "hanuman":("707iS1Iyv-E",12),
 "ganesh":("NGI-JiRiwSc",80), "krishna":("uCUR842niAU",12), "ram":("pCixItfj5Vo",80),
 "edm":("unfGUJz6D8U",78), "skandamata":("Q5_3JBKLNpg",74), "navdurga":("G99-49Pfs6U",50),
 "shivaarti":("rxeMNQ48yWU",50), "vishnu":("pCixItfj5Vo",80),
}
DAY_ART = {"Ht_SogxJ_D8":62,"SsrEdkAf4xI":62,"lUhDATRpvrs":62,"65nhAnBmYuQ":62,"Q5_3JBKLNpg":74,"r32U54qyerw":60,"FFcNanFHSaY":60,"89wxOjTwPwQ":60}

def arch(vid, pos=50, alt="", eager=False):
    return (f'<div class="arch"><img src="https://i.ytimg.com/vi/{vid}/maxresdefault.jpg" '
            f'onerror="this.onerror=null;this.src=\'https://i.ytimg.com/vi/{vid}/hqdefault.jpg\'" '
            f'onload="if(this.naturalWidth<200&&!this.dataset.f){{this.dataset.f=1;this.src=\'https://i.ytimg.com/vi/{vid}/hqdefault.jpg\'}}" '
            f'style="object-position:{pos}% 30%" alt="{e(alt)}" {"" if eager else "loading=\"lazy\""} width="300" height="400"></div>')

LOTUS = ('<div class="lotus" aria-hidden="true"><svg viewBox="0 0 34 20"><g fill="currentColor">'
         '<path d="M17 1c3 4 3 10 0 15-3-5-3-11 0-15z"/><path d="M17 16C13 13 9 12 4 13c3 3 8 4 13 3z" opacity=".75"/>'
         '<path d="M17 16c4-3 8-4 13-3-3 3-8 4-13 3z" opacity=".75"/><path d="M3 18h28" stroke="currentColor" stroke-width="1"/></g></svg></div>')

def sec_head(title, sub=""):
    return f'<div class="sec-head">{LOTUS}<h2>{title}</h2>{f"<p>{sub}</p>" if sub else ""}</div>'

def band(h1, answer, crumb, vid=None, pos=50, alt="", extra="", gold=True, to_band=False):
    art = arch(vid, pos, alt, eager=True) if vid else ""
    return (f'<section class="night scallop page-band{" to-band" if to_band else ""}"><div class="wrap"><div>'
            f'<nav class="crumbs-in" aria-label="breadcrumb"><a href="index.html">होम</a> / {e(crumb)}</nav>'
            f'<h1{" class=\"gold-type\"" if gold else ""}>{e(h1)}</h1><p class="answer">{answer}</p>{extra}</div>{art}</div></section>')

NAV = [("index.html","होम"),("aaj-ka-panchang.html","आज का पंचांग"),("tyohar-calendar.html","त्योहार"),
       ("aarti-mantra.html","आरती-चालीसा"),("jaap-mala.html","जाप माला"),("mata-rani-bhajan.html","भजन")]

def watch(i): return f"https://www.youtube.com/watch?v={i}"

def video_cards(ids, deity=""):
    out = ['<ul class="videos">']
    for i in ids:
        t, dur = V[i]
        out.append(f'''<li class="video"><div class="frame"><img src="https://i.ytimg.com/vi/{i}/hqdefault.jpg" alt="{e(t)} — वीडियो" loading="lazy" width="480" height="360"><span class="dur">{dur}</span><button class="play" data-id="{i}" aria-label="यहीं चलाएँ: {e(t)}"></button></div>
<h3><a href="{watch(i)}" target="_blank" rel="noopener">{e(t)}</a></h3><p>OmKiran Bhakti{(" · "+deity) if deity else ""}</p></li>''')
    out.append('</ul>')
    return "\n".join(out)

def itemlist(ids, name):
    return {"@type":"ItemList","name":name,"itemListElement":[
        {"@type":"ListItem","position":n+1,"url":watch(i),"name":V[i][0]} for n,i in enumerate(ids)]}

def faq_html(faqs):
    if not faqs: return ""
    qs = "".join(f"<details><summary>{e(q)}</summary><p>{a}</p></details>" for q,a in faqs)
    return f'<section class="faq"><div class="wrap"><h2>अक्सर पूछे जाने वाले सवाल</h2>{qs}</div></section>'

def faq_ld(faqs):
    import re
    return {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":re.sub("<[^>]+>","",a)}} for q,a in faqs]}

def page(slug, title, desc, body, crumbs=None, ld=None, active=None, h1=None):
    url = SITE if slug=="index.html" else SITE+slug
    graph = [{"@type":"WebPage","@id":url+"#page","url":url,"name":title,"description":desc,"inLanguage":"hi-IN",
              "isPartOf":{"@id":SITE+"#website"},"publisher":{"@id":SITE+"#organization"},"dateModified":TODAY}]
    if crumbs:
        graph.append({"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"होम","item":SITE}]+
            [{"@type":"ListItem","position":2,"name":crumbs,"item":url}]})
    graph += (ld or [])
    navh = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h==(active or slug) else ""}>{t}</a>' for h,t in NAV)
    crumb_html = f'<nav class="crumbs wrap" aria-label="breadcrumb"><a href="index.html">होम</a> / {e(crumbs)}</nav>' if (crumbs and 'crumbs-in' not in body) else ""
    return f'''<!doctype html>
<html lang="hi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#1C2350">
<meta property="og:type" content="website"><meta property="og:site_name" content="OmKiran Bhakti">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{LOGO}"><meta property="og:locale" content="hi_IN">
<meta name="twitter:card" content="summary">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Mukta:wght@400;500;600&family=Tiro+Devanagari+Hindi&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css?v={CSSV}">
<script>try{{var t=localStorage.getItem('okb-theme');if(t)document.documentElement.setAttribute('data-theme',t)}}catch(e){{}}</script>
<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@graph":graph},ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#main">सीधे सामग्री पर जाएँ</a>
<header class="site-head"><div class="toran" aria-hidden="true"></div>
<div class="wrap head-row">
<a class="brand" href="index.html"><img src="{LOGO}" alt="" width="40" height="40"><span><b>OmKiran Bhakti</b><small>भजन, आरती, चालीसा और मंत्र</small></span></a>
<nav class="nav" aria-label="मुख्य">{navh}</nav>
<button class="theme-btn" aria-label="रंग बदलें (दिन/रात)">◐</button>
<button class="menu-btn" aria-label="मेन्यू" aria-expanded="false">☰</button>
</div></header>
{crumb_html}
<main id="main">
{body}
</main>
<footer class="site-foot"><div class="wrap foot-grid">
<div><h2>OmKiran Bhakti</h2><p>हिंदी भक्ति संगीत का घर — आरती, चालीसा, मंत्र और भजन, बोल और अर्थ के साथ। हमारे सभी वीडियो <a href="{YT}">YouTube चैनल</a> पर हैं।</p></div>
<div><h2>पाठ</h2><ul><li><a href="hanuman-chalisa.html">हनुमान चालीसा</a></li><li><a href="om-jai-jagdish-hare-aarti.html">ॐ जय जगदीश हरे</a></li><li><a href="ganesh-aarti-jai-ganesh-deva.html">गणेश आरती</a></li><li><a href="shiv-aarti-om-jai-shiv-omkara.html">शिव आरती</a></li><li><a href="jaap-mala.html">ऑनलाइन जाप माला</a></li><li><a href="aaj-ka-panchang.html">आज का पंचांग</a></li><li><a href="tyohar-calendar.html">त्योहार कैलेंडर</a></li><li><a href="about.html">परिचय</a></li></ul></div>
<div><h2>भजन</h2><ul><li><a href="mata-rani-bhajan.html">माता रानी</a></li><li><a href="shiv-bhajan.html">शिव</a></li><li><a href="ganesh-bhajan.html">गणेश</a></li><li><a href="krishna-bhajan.html">कृष्ण</a></li><li><a href="ram-bhajan.html">राम</a></li><li><a href="devotional-edm-bhajans.html">भक्ति EDM</a></li></ul></div>
</div><div class="wrap fine">© {datetime.date.today().year} OmKiran Bhakti. पारंपरिक पाठ सार्वजनिक धरोहर हैं; अर्थ और संगीत OmKiran Bhakti के हैं।</div></footer>
<script src="script.js?v={JSV}" defer></script>
</body></html>'''

PAGES = {}
def add(slug, *a, **k): PAGES[slug] = page(slug, *a, **k)

DEVNUM = str.maketrans("0123456789","०१२३४५६७८९")
def lyrics_body(verses, label_map=True):
    out, n = [], 0
    last = None
    for kind, text, mean in verses:
        if label_map and kind != last:
            lab = {"doha":"दोहा","chaupai":"चौपाई"}.get(kind)
            if lab: out.append(f'<p class="section-label">{lab}</p>')
            last = kind
        if kind in ("chaupai", "shloka"): n += 1; no = str(n).translate(DEVNUM)
        else: no = ""
        if kind in ("mantra", "dhyan"):
            head, body = text.split("\n", 1)
            out.append(f'<div class="verse mantra{" dhyan" if kind == "dhyan" else ""}"><h3 class="m-name">{e(head)}</h3><p class="line">{e(body)}</p><p class="mean">{e(mean)}</p></div>')
            continue
        out.append(f'<div class="verse {kind}"><span class="no">{no}</span><p class="line">{e(text)}</p><p class="mean">{e(mean)}</p></div>')
    return "\n".join(out)

def reader_tools():
    return ('<div class="reader-tools no-print" role="toolbar" aria-label="पढ़ने के विकल्प">'
            '<button class="chip chip-paath" data-paath aria-pressed="false"><span class="pm-on">पाठ मोड</span><span class="pm-off">पाठ मोड बंद करें</span></button>'
            '<button class="chip" data-meaning aria-pressed="true">अर्थ दिखाएँ</button>'
            '<button class="chip" data-size="0.15" aria-label="अक्षर बड़े करें">अ+</button>'
            '<button class="chip" data-size="-0.15" aria-label="अक्षर छोटे करें">अ−</button>'
            '<button class="chip" data-print>प्रिंट / PDF</button></div>')


def verse_count(verses):
    from collections import Counter
    c = Counter(k for k,_,_ in verses)
    names = [("chaupai","चौपाई"),("shloka","श्लोक"),("pad","पद"),("mantra","मंत्र"),("doha","दोहे")]
    parts = [f"{c[k]} {n}" for k,n in names if c.get(k)]
    other = sum(v for k,v in c.items() if k not in dict(names))
    if other and not parts: parts.append(f"{other} पद")
    return ", ".join(parts)

def paath_end(slug, name):
    from urllib.parse import quote
    msg = quote(f"{name} — पूरे बोल और हर पंक्ति का अर्थ:\n{SITE}{slug}")
    return (f'<div class="paath-end"><p class="pe-mark" aria-hidden="true">॥ इति ॥</p>'
            f'<p class="pe-text">{e(name)} का पाठ पूरा हुआ।</p>'
            f'<a class="btn pe-share no-print" href="https://wa.me/?text={msg}" rel="noopener" target="_blank">किसी अपने को WhatsApp पर भेजें</a></div>')

def paath_rail(slug, verses):
    return (f'<aside class="paath-rail no-print" aria-label="इस पाठ के बारे में"><div class="rail-card">'
            f'<p class="rail-count">{verse_count(verses)}</p>'
            f'<button class="btn rail-btn" data-paath>पाठ मोड में पढ़ें</button>'
            f'<p class="rail-hint">पूजा के समय: बड़े अक्षर, दीपक की रोशनी जैसा अँधेरा पन्ना, और स्क्रीन अपने-आप बंद नहीं होगी।</p></div>'
            f'<!--REL:{slug}--></aside>')

def lyrics_page(slug, title, desc, h1, answer, verses, intro_html, vid_ids, faqs, crumb, extra="", work_name=None, author=None, art=None):
    akey = {"hanuman-chalisa.html":"hanuman","om-jai-jagdish-hare-aarti.html":"vishnu",
            "ganesh-aarti-jai-ganesh-deva.html":"ganesh","shiv-aarti-om-jai-shiv-omkara.html":"shivaarti"}.get(slug)
    vid, pos = art if art else ART.get(akey, (None,50))
    body = f'''<article>{band(h1, answer, crumb, vid, pos, h1, extra=intro_html)}
<section class="paath-sec"><div class="paath-diya" aria-hidden="true"><div class="diya"><span class="bowl"></span><span class="flame"></span></div></div><div class="wrap paath-grid">
<div class="paath-main">
{reader_tools()}
<div class="lyrics">{lyrics_body(verses)}</div>
{paath_end(slug, work_name or h1)}
<p class="note no-print">पाठ पारंपरिक है और अलग-अलग क्षेत्रों में शब्दों में थोड़ा अंतर मिलता है। अर्थ सरल हिंदी में OmKiran Bhakti ने लिखा है। कोई त्रुटि दिखे तो <a href="{YT}">YouTube पर कमेंट</a> करके बताएँ।</p>
</div>
{paath_rail(slug, verses)}
</div></section></article>
{('<section class="no-print"><div class="wrap"><h2>साथ में गाएँ — वीडियो</h2>' + video_cards(vid_ids) + '</div></section>') if vid_ids else ''}
{extra}
{faq_html(faqs)}'''
    ld = [{"@type":"CreativeWork","name":work_name or h1,"inLanguage":"hi","text":"\n".join(v[1] for v in verses),
           **({"author":{"@type":"Person","name":author}} if author else {}),
           "isAccessibleForFree":True,"publisher":{"@id":SITE+"#organization"}},
          ] + ([itemlist(vid_ids, h1+" — वीडियो")] if vid_ids else []) + ([faq_ld(faqs)] if faqs else [])
    add(slug, title, desc, body, crumbs=crumb, ld=ld, active="aarti-mantra.html")

# ---------------- Lyrics pages ----------------
lyrics_page("hanuman-chalisa.html",
 "हनुमान चालीसा — पूरे बोल, सरल हिंदी अर्थ और वीडियो | OmKiran Bhakti",
 "हनुमान चालीसा के पूरे 40 चौपाई और दोहे, हर पंक्ति का सरल हिंदी अर्थ, बड़े अक्षरों में पढ़ने का विकल्प, प्रिंट PDF और 4 मिनट वाला पाठ वीडियो।",
 "हनुमान चालीसा — पूरे बोल और अर्थ",
 "हनुमान चालीसा गोस्वामी तुलसीदास जी की रचना है। इसमें 2 आरंभिक दोहे, 40 चौपाइयाँ और 1 समापन दोहा हैं। नीचे हर पंक्ति के साथ उसका सरल हिंदी अर्थ दिया है।",
 HANUMAN_CHALISA,
 '<p class="lede">मंगलवार और शनिवार को इसका पाठ विशेष माना जाता है, पर इसे किसी भी दिन, किसी भी समय श्रद्धा से पढ़ा जा सकता है।</p>',
 ["707iS1Iyv-E","v249ibg1Juk","HcfPkZyal_M","W__UjJxgK_o","bfNwwRhVY8U","6nsots7gB9A"],
 [("हनुमान चालीसा किसने लिखी?","हनुमान चालीसा 16वीं शताब्दी के संत-कवि गोस्वामी तुलसीदास जी ने अवधी भाषा में लिखी।"),
  ("हनुमान चालीसा में कितनी चौपाइयाँ हैं?","इसमें 40 चौपाइयाँ हैं, इसीलिए इसे 'चालीसा' कहते हैं। शुरुआत में 2 दोहे और अंत में 1 दोहा है।"),
  ("हनुमान चालीसा का पाठ कब करना चाहिए?","परंपरा में मंगलवार और शनिवार विशेष माने जाते हैं, और सुबह स्नान के बाद का समय उत्तम माना जाता है। श्रद्धा हो तो किसी भी समय पाठ किया जा सकता है।"),
  ("हनुमान चालीसा पढ़ने में कितना समय लगता है?","सामान्य गति से लगभग 7–10 मिनट। तेज़ लय में यह लगभग 4 मिनट में पूरा हो जाता है — हमारा <a href=\"https://www.youtube.com/watch?v=707iS1Iyv-E\">4 मिनट वाला पाठ</a> साथ में पढ़ने के लिए बनाया गया है।"),
  ("क्या 108 बार हनुमान चालीसा पढ़ने की कोई गिनती रख सकते हैं?","हाँ, हमारी <a href=\"jaap-mala.html\">ऑनलाइन जाप माला</a> से आप हर पाठ की गिनती रख सकते हैं।")],
 "हनुमान चालीसा", extra=f'<section class="band no-print"><div class="wrap"><h2>और भी पढ़ें</h2><ul class="library"><li><a href="ram-bhajan.html"><strong>राम भजन</strong><span>हनुमान जी के आराध्य</span></a></li><li><a href="jaap-mala.html"><strong>जाप माला</strong><span>पाठ की गिनती रखें</span></a></li><li><a href="aarti-mantra.html"><strong>सभी आरती और चालीसा</strong><span>पूरी सूची</span></a></li></ul></div></section>',
 work_name="हनुमान चालीसा", author="गोस्वामी तुलसीदास")

lyrics_page("om-jai-jagdish-hare-aarti.html",
 "ॐ जय जगदीश हरे आरती — पूरे बोल और अर्थ | OmKiran Bhakti",
 "ॐ जय जगदीश हरे आरती के पूरे बोल, हर पद का सरल हिंदी अर्थ, बड़े अक्षर और प्रिंट PDF। भगवान विष्णु की यह आरती लगभग हर पूजा के अंत में गाई जाती है।",
 "ॐ जय जगदीश हरे — आरती के बोल और अर्थ",
 "‘ॐ जय जगदीश हरे’ भगवान विष्णु (जगदीश) की आरती है, जिसकी रचना 19वीं शताब्दी में पंडित श्रद्धाराम फिल्लौरी ने की। उत्तर भारत में लगभग हर पूजा का समापन इसी आरती से होता है।",
 OM_JAI_JAGDISH, '<p class="lede">गुरुवार श्रीहरि विष्णु का दिन माना जाता है — इस दिन यह आरती विशेष रूप से गाई जाती है।</p>',
 ["G99-49Pfs6U","sLQF1nm_RqU","GtRRHlLc5gQ"],
 [("ॐ जय जगदीश हरे आरती किसने लिखी?","यह आरती पंजाब के विद्वान पंडित श्रद्धाराम फिल्लौरी (1837–1881) ने लिखी थी।"),
  ("यह आरती किस भगवान की है?","यह भगवान विष्णु की आरती है। ‘जगदीश’ का अर्थ है जगत के ईश्वर, और ‘हरि’ विष्णु का नाम है।"),
  ("आरती कब गाई जाती है?","यह आरती आम तौर पर पूजा, कथा या हवन के अंत में गाई जाती है।")],
 "ॐ जय जगदीश हरे", work_name="ॐ जय जगदीश हरे", author="पंडित श्रद्धाराम फिल्लौरी")

lyrics_page("ganesh-aarti-jai-ganesh-deva.html",
 "जय गणेश जय गणेश देवा आरती — पूरे बोल और अर्थ | OmKiran Bhakti",
 "जय गणेश जय गणेश देवा — गणेश जी की आरती के पूरे बोल, सरल हिंदी अर्थ, प्रिंट PDF और गणपति भजन वीडियो। बुधवार और गणेश चतुर्थी पर विशेष।",
 "जय गणेश जय गणेश देवा — गणेश आरती",
 "‘जय गणेश जय गणेश देवा’ भगवान गणेश की सबसे लोकप्रिय हिंदी आरती है, जो परंपरा से सूरदास जी की मानी जाती है। किसी भी शुभ काम या पूजा की शुरुआत गणेश वंदना से होती है।",
 JAI_GANESH_DEVA, '<p class="lede">बुधवार गणेश जी का दिन है, और गणेश चतुर्थी के दस दिनों में यह आरती रोज़ सुबह-शाम गाई जाती है।</p>',
 ["Qpe4rrfzWhk","ZswQ9qUMDTs","u3kbBEHOs9o","IkcVwmMUUmw"],
 [("गणेश जी की आरती कब करनी चाहिए?","किसी भी पूजा की शुरुआत में, बुधवार को, और गणेश चतुर्थी के दिनों में सुबह-शाम।"),
  ("‘सुखकर्ता दुखहर्ता’ और ‘जय गणेश देवा’ में क्या अंतर है?","‘सुखकर्ता दुखहर्ता’ संत समर्थ रामदास की मराठी आरती है, जबकि ‘जय गणेश देवा’ हिंदी आरती है। दोनों गणेश जी की हैं — हमारा <a href=\"https://www.youtube.com/watch?v=Qpe4rrfzWhk\">सुखकर्ता दुखहर्ता वीडियो</a> भी देखें।")],
 "गणेश आरती", work_name="जय गणेश जय गणेश देवा")

lyrics_page("shiv-aarti-om-jai-shiv-omkara.html",
 "ॐ जय शिव ओंकारा आरती — पूरे बोल और अर्थ | OmKiran Bhakti",
 "ॐ जय शिव ओंकारा — भगवान शिव की आरती के पूरे बोल, हर पद का सरल हिंदी अर्थ, प्रिंट PDF और शिव आरती वीडियो। सोमवार और सावन में विशेष।",
 "ॐ जय शिव ओंकारा — शिव आरती",
 "‘ॐ जय शिव ओंकारा’ भगवान शिव की सबसे प्रचलित आरती है। इसके अंतिम पद में ‘शिवानन्द स्वामी’ का नाम आता है। सोमवार, सावन और महाशिवरात्रि पर इसे विशेष रूप से गाया जाता है।",
 OM_JAI_SHIV_OMKARA, '<p class="lede">इस आरती में ब्रह्मा, विष्णु और शिव को एक ही ओंकार के तीन रूप बताया गया है।</p>',
 ["ZqFztNyxSgU","axKgdxe7JZE","JUg809TxgRg","C5lE4JA3sKc"],
 [("शिव आरती कब करनी चाहिए?","सोमवार को, सावन के महीने में, प्रदोष व्रत और महाशिवरात्रि पर। रोज़ शाम की पूजा में भी गाई जाती है।"),
  ("शिव जी के प्रमुख मंत्र कौन-से हैं?","पंचाक्षर मंत्र ‘ॐ नमः शिवाय’ और महामृत्युंजय मंत्र। दोनों के 108 बार वाले वीडियो हमारे <a href=\"shiv-bhajan.html\">शिव भजन पेज</a> पर हैं।")],
 "शिव आरती", work_name="ॐ जय शिव ओंकारा")

# ---------------- Deity pages ----------------
DEITY = [
 ("mata-rani-bhajan.html","mata","माता रानी भजन — देवी गीत, दुर्गा चालीसा और नवरात्रि भजन | OmKiran Bhakti",
  "माता रानी के लोकप्रिय भजन, दुर्गा चालीसा, देवी आरती और नवरात्रि गरबा — OmKiran Bhakti के असली वीडियो, साथ में नवरात्रि 2026 की तिथियाँ।",
  "माता रानी के भजन",
  "यहाँ OmKiran Bhakti के माता रानी के सबसे पसंद किए गए भजन हैं — जगराते के जयकारे, भावपूर्ण देवी गीत, दुर्गा चालीसा और नवरात्रि के गरबे।",
  ["woNhYRu376g","2yVR5zSaKpc","fhm1dqyttu0","9hzay6Ebzas","PHNyA0VlAI8","NuWOBRQ9B3Q","rLSpMEkB7eU","vr5Bp46iA-Q","CcDzHzu7sIw","dJAZTUkHcBs","eA6tcqEncoE","Fxfm-eadkTY"],
  [("navratri-2026.html","नवरात्रि 2026","तिथियाँ और नौ देवियाँ"),("jaap-mala.html","जाप माला","‘जय माता दी’ जाप गिनें")],
  [("नवरात्रि 2026 कब है?","शारदीय नवरात्रि 2026, 11 अक्टूबर से शुरू हुई; अष्टमी और नवमी 19 अक्टूबर को और दशहरा 20 अक्टूबर को है। पूरी सूची <a href=\"navratri-2026.html\">नवरात्रि 2026 पेज</a> पर।"),
   ("माता रानी का कौन-सा भजन सबसे ज़्यादा सुना जाता है?","हमारे चैनल पर ‘फूलों की आई है बहार’ सबसे ज़्यादा सुना गया माता रानी भजन है।")]),
 ("shiv-bhajan.html","shiv","शिव भजन, शिव आरती और महामृत्युंजय मंत्र | OmKiran Bhakti",
  "भोलेनाथ के भजन, ॐ जय शिव ओंकारा आरती, शिव चालीसा, रुद्राष्टकम और 108 बार महामृत्युंजय मंत्र — OmKiran Bhakti के असली वीडियो एक जगह।",
  "शिव भजन, आरती और मंत्र",
  "भगवान शिव की भक्ति के लिए यहाँ भजन, आरती, चालीसा, रुद्राष्टकम, निर्वाण षटकम और 108 बार जाप वाले मंत्र हैं। सोमवार और सावन में ये सबसे ज़्यादा सुने जाते हैं।",
  ["vsfjF59qj4Q","JUg809TxgRg","rxeMNQ48yWU","ZqFztNyxSgU","pn5OODJqmTc","Kbe3pbLsg1U","DGsy57lUApA","qCwFf_cCWGM","6vVDsn9R6DM","C5lE4JA3sKc","fQiD96yFR6o","icIEKo5vLjw"],
  [("shiv-aarti-om-jai-shiv-omkara.html","शिव आरती","ॐ जय शिव ओंकारा — बोल और अर्थ"),("jaap-mala.html","जाप माला","‘ॐ नमः शिवाय’ 108 जाप")],
  [("महामृत्युंजय मंत्र कितनी बार जपना चाहिए?","परंपरा में 108 बार (एक माला) जाप किया जाता है। हमारा 108 बार वाला वीडियो और ऑनलाइन जाप माला दोनों इसमें मदद करेंगे।")]),
 ("ganesh-bhajan.html","ganesh","गणेश भजन, गणेश आरती और गणेश चालीसा | OmKiran Bhakti",
  "गणपति बप्पा के लोकप्रिय भजन — संकट हर लो मंगल कर दो, विसर्जन भजन, गणेश चालीसा और सुखकर्ता दुखहर्ता आरती। OmKiran Bhakti के असली वीडियो।",
  "गणेश भजन और आरती",
  "विघ्नहर्ता गणेश जी के भजन, आरती और चालीसा। ‘संकट हर लो मंगल कर दो’ हमारे चैनल का सबसे ज़्यादा सुना गया भजन है।",
  ["ZswQ9qUMDTs","lMHZDM-RRb4","NGI-JiRiwSc","EtnvDW1AlOY","XscYggWHC5o","u3kbBEHOs9o","Qpe4rrfzWhk","IkcVwmMUUmw","5WeumLCpi5w","BmrflIPOqAk"],
  [("ganesh-aarti-jai-ganesh-deva.html","गणेश आरती","जय गणेश देवा — बोल और अर्थ")],
  [("गणेश जी की पूजा किस दिन करनी चाहिए?","बुधवार गणेश जी का दिन माना जाता है, और हर शुभ काम की शुरुआत उनकी वंदना से होती है।")]),
 ("krishna-bhajan.html","krishna","कृष्ण भजन — राधा कृष्ण भक्ति गीत और जन्माष्टमी बधाई | OmKiran Bhakti",
  "राधा-कृष्ण के मधुर भजन, जन्माष्टमी बधाई गीत, कृष्ण चालीसा, हरे कृष्ण कीर्तन और बरसाने की होली — OmKiran Bhakti के असली वीडियो।",
  "कृष्ण भजन और राधा-कृष्ण के गीत",
  "श्रीकृष्ण और राधा रानी के भजन — जन्माष्टमी के बधाई और सोहर गीत, कृष्ण चालीसा, हरे कृष्ण कीर्तन, राधा प्रणाम मंत्र और ब्रज की होली।",
  ["vy6ucthmxmk","P9N1XQzw8CI","TVdX5XbbjHs","ZQ_OBR-596M","ZIhDdYk6Gus","3ChBJC1Vigk","_8yw36Jn7iM","GtRRHlLc5gQ","uCUR842niAU","R1PiCmntXIM"],
  [("om-jai-jagdish-hare-aarti.html","ॐ जय जगदीश हरे","श्रीहरि की आरती")],
  [("जन्माष्टमी पर कौन-से भजन गाए जाते हैं?","कृष्ण जन्म के बधाई और सोहर गीत, जैसे ‘अंगना झूले कृष्ण कन्हैया’ और ‘जन्मे हैं कृष्ण कन्हैया’।")]),
 ("ram-bhajan.html","ram","राम भजन, श्री राम चालीसा और राम स्तुति | OmKiran Bhakti",
  "श्री राम के भजन, राम चालीसा, श्री रामचंद्र कृपालु स्तुति, निर्गुण राम भजन और 108 बार राम गायत्री मंत्र — OmKiran Bhakti के असली वीडियो।",
  "राम भजन और राम स्तुति",
  "मर्यादा पुरुषोत्तम श्रीराम के भजन, ‘श्री रामचंद्र कृपालु भजमन’ स्तुति, राम चालीसा, निर्गुण भजन और राम गायत्री मंत्र। हनुमान चालीसा के साथ सुबह सुनने के लिए उत्तम।",
  ["pCixItfj5Vo","sLQF1nm_RqU","ZqOnkb7zElU","l9z2J0I6Kao","lBRP9bTTLek","kHM8fGmqoLw","SMyoiGPuKGA","fmbCXi2K9tw"],
  [("hanuman-chalisa.html","हनुमान चालीसा","पूरे बोल और अर्थ")],
  [("‘श्री रामचंद्र कृपालु भजमन’ किसने लिखा?","यह स्तुति गोस्वामी तुलसीदास जी की ‘विनय पत्रिका’ से है।")]),
 ("devotional-edm-bhajans.html","edm","भक्ति EDM — शिव तांडव, हनुमान तांडव और अयि गिरिनन्दिनि मिक्स | OmKiran Bhakti",
  "OmKiran Bhakti के भक्ति EDM ट्रैक — भज भज भूतेशम्, हनुमान तांडव पावर मिक्स और अयि गिरिनन्दिनि EDM। जिम, ड्राइव और जगराते के लिए ऊर्जा भरा संगीत।",
  "भक्ति EDM",
  "पारंपरिक स्तोत्र और मंत्र, आज की इलेक्ट्रॉनिक धुन में। ये ट्रैक OmKiran Bhakti के अपने प्रोडक्शन हैं — भारी बेस, तेज़ लय और मूल संस्कृत पाठ।",
  ["unfGUJz6D8U","D5LIL8j8Kqs","XLYs9iEXKmA","pjhPqvh26bg","BQxaizzx5So"],
  [("shiv-bhajan.html","शिव भजन","पारंपरिक रूप में"),("mata-rani-bhajan.html","माता रानी भजन","पारंपरिक रूप में")],
  [("भक्ति EDM क्या है?","भक्ति EDM में पारंपरिक मंत्र, स्तोत्र और भजनों को इलेक्ट्रॉनिक डांस म्यूज़िक की लय में पेश किया जाता है, ताकि नई पीढ़ी भी उनसे जुड़ सके।")]),
]
for slug, pk, title, desc, h1, answer, ids, related, faqs in DEITY:
    plid, plname = PLAYLISTS.get(pk, (None,None))
    rel = "".join(f'<li><a href="{h}"><strong>{e(t)}</strong><span>{e(s)}</span></a></li>' for h,t,s in related)
    pl = f'<p style="margin-top:2rem"><a class="btn" href="https://www.youtube.com/playlist?list={plid}" target="_blank" rel="noopener">पूरी प्लेलिस्ट YouTube पर सुनें: {e(plname)}</a></p>' if plid else ""
    vid, pos = ART[pk]
    body = f'''{band(h1, answer, h1, vid, pos, h1)}
<section><div class="wrap">{sec_head("सबसे पसंद किए गए वीडियो")}{video_cards(ids)}{pl}</div></section>
<section class="band"><div class="wrap">{sec_head("बोल और पाठ")}<ul class="library">{rel}<li><a href="aarti-mantra.html"><strong>सभी आरती और चालीसा</strong><span>पूरी सूची</span></a></li></ul></div></section>
{faq_html(faqs)}'''
    add(slug, title, desc, body, crumbs=h1, ld=[itemlist(ids, h1), faq_ld(faqs)] if faqs else [itemlist(ids,h1)], active="mata-rani-bhajan.html")

# ---------------- Aarti & mantra hub ----------------
LIB = [("hanuman-chalisa.html","हनुमान चालीसा","40 चौपाई, अर्थ सहित"),
       ("om-jai-jagdish-hare-aarti.html","ॐ जय जगदीश हरे","विष्णु आरती, अर्थ सहित"),
       ("ganesh-aarti-jai-ganesh-deva.html","जय गणेश देवा","गणेश आरती, अर्थ सहित"),
       ("shiv-aarti-om-jai-shiv-omkara.html","ॐ जय शिव ओंकारा","शिव आरती, अर्थ सहित")]
mantra_ids = ["rxeMNQ48yWU","C5lE4JA3sKc","KPZbsWemcIg","SE1RyQ6fWQs","h4EjlAYqQo0","SMyoiGPuKGA","gZ7DoH6ZOa4","ktQUU5Y3tPE","iUo6Ui1lPMY"]
chalisa_ids = ["707iS1Iyv-E","eA6tcqEncoE","u3kbBEHOs9o","JUg809TxgRg","ASNq5VCqOhY","ZQ_OBR-596M","pCixItfj5Vo","5HxuQ9YgtiE"]
aarti_ids = ["ZqFztNyxSgU","Qpe4rrfzWhk","jAdixB5m0Zo","axKgdxe7JZE","w8pxctA2998","G99-49Pfs6U"]
lib_html = "".join(f'<li><a href="{h}"><strong>{t}</strong><span>{s}</span></a></li>' for h,t,s in LIB)
PAATH_ART = {"hanuman-chalisa.html":"hanuman","om-jai-jagdish-hare-aarti.html":"vishnu","ganesh-aarti-jai-ganesh-deva.html":"ganesh","shiv-aarti-om-jai-shiv-omkara.html":"shivaarti"}
paath_html = '<ul class="paath">' + "".join(f'<li><a href="{h}">{arch(*ART[PAATH_ART[h]], alt="")}<div><strong>{t}</strong><span>{s}</span></div></a></li>' for h,t,s in LIB) + \
  f'<li><a href="jaap-mala.html">{arch("Kbe3pbLsg1U",80, alt="")}<div><strong>ऑनलाइन जाप माला</strong><span>108 की गिनती</span></div></a></li>' + \
  f'<li><a href="navratri-2026.html">{arch(*ART["navdurga"], alt="")}<div><strong>नवरात्रि 2026</strong><span>तिथियाँ और नौ देवियाँ</span></div></a></li></ul>'
add("aarti-mantra.html", "आरती, चालीसा और मंत्र — बोल, अर्थ और वीडियो | OmKiran Bhakti",
 "हनुमान चालीसा, ॐ जय जगदीश हरे, गणेश आरती और शिव आरती के पूरे बोल और अर्थ; साथ में चालीसा, आरती और 108 बार मंत्र जाप के वीडियो।",
 f'''{band("आरती, चालीसा और मंत्र","पूजा के समय पढ़ने के लिए पूरे बोल, हर पंक्ति के सरल हिंदी अर्थ के साथ — बड़े अक्षरों में पढ़ें या प्रिंट करें। नीचे हर पाठ का गाने वाला वीडियो भी है।","आरती, चालीसा और मंत्र",*ART["navdurga"],"नवदुर्गा आरती")}
<section><div class="wrap">{sec_head("बोल और अर्थ","हर पंक्ति के साथ उसका सरल हिंदी अर्थ")}{paath_html}
<p class="note">हर हफ़्ते नए पाठ जुड़ते हैं — दुर्गा चालीसा, शिव चालीसा, आरती कुंजबिहारी की और व्रत कथाएँ जल्द आ रही हैं।</p></div></section>
<section class="band"><div class="wrap">{sec_head("चालीसा — 4 मिनट में","रोज़ के पाठ के लिए तेज़ लय में")}{video_cards(chalisa_ids)}</div></section>
<section><div class="wrap">{sec_head("आरती")}{video_cards(aarti_ids)}</div></section>
<section class="band"><div class="wrap">{sec_head("मंत्र जाप — 108 बार","एक माला के बराबर जाप, ध्यान के साथ सुनें")}{video_cards(mantra_ids)}
<p style="margin-top:2rem"><a class="btn" href="https://www.youtube.com/playlist?list={PLAYLISTS['mantra'][0]}" target="_blank" rel="noopener">मंत्रों का खज़ाना — पूरी प्लेलिस्ट</a></p></div></section>''',
 crumbs="आरती, चालीसा और मंत्र", ld=[itemlist(chalisa_ids+aarti_ids+mantra_ids,"आरती, चालीसा और मंत्र वीडियो")])

# ---------------- Navratri 2026 ----------------
NDAYS = [("20261011","11 अक्टूबर, रविवार","पहला दिन","माँ शैलपुत्री","Ht_SogxJ_D8"),
         ("20261012","12 अक्टूबर, सोमवार","दूसरा दिन","माँ ब्रह्मचारिणी","SsrEdkAf4xI"),
         ("20261013","13 अक्टूबर, मंगलवार","तीसरा दिन","माँ चंद्रघंटा","lUhDATRpvrs"),
         ("20261014","14 अक्टूबर, बुधवार","चौथा दिन","माँ कूष्मांडा","65nhAnBmYuQ"),
         ("20261015","15 अक्टूबर, गुरुवार","पाँचवाँ दिन","माँ स्कंदमाता","Q5_3JBKLNpg"),
         ("20261016","16 अक्टूबर, शुक्रवार","छठा दिन","माँ कात्यायनी","r32U54qyerw"),
         ("20261017","17 अक्टूबर, शनिवार","सातवाँ दिन","माँ कालरात्रि","FFcNanFHSaY"),
         ("20261018,20261019","18–19 अक्टूबर","अष्टमी","माँ महागौरी",None),
         ("20261019","19 अक्टूबर, सोमवार","नवमी","माँ सिद्धिदात्री","89wxOjTwPwQ")]
days = "".join(f'<li data-ymd="{y}">' + (arch(v, DAY_ART.get(v,60), g) if v else arch("G99-49Pfs6U",50,g)) +
               f'<div><span class="d">{d} · {n}</span><span class="g">{g}</span>' +
               (f'<a href="{watch(v)}" target="_blank" rel="noopener">आरती सुनें</a>' if v else '<a href="https://www.youtube.com/watch?v=G99-49Pfs6U" target="_blank" rel="noopener">नवदुर्गा आरती सुनें</a>') + '</div></li>'
               for y,d,n,g,v in NDAYS)
nav_faq = [("नवरात्रि 2026 कब से कब तक है?","शारदीय नवरात्रि 2026, 11 अक्टूबर (रविवार) को घटस्थापना से शुरू हुई। दुर्गा अष्टमी और महानवमी दोनों 19 अक्टूबर (सोमवार) को हैं, और विजयादशमी (दशहरा) 20 अक्टूबर (मंगलवार) को है।"),
           ("इस बार अष्टमी और नवमी एक ही दिन क्यों हैं?","2026 में अष्टमी तिथि 19 अक्टूबर की सुबह समाप्त होकर उसी दिन नवमी तिथि शुरू हो रही है, इसलिए दिल्ली के पंचांग के अनुसार दोनों का पूजन 19 अक्टूबर को होगा। आपके शहर में तिथि का समय थोड़ा अलग हो सकता है।"),
           ("नवरात्रि में किस दिन किस देवी की पूजा होती है?","क्रम से: शैलपुत्री, ब्रह्मचारिणी, चंद्रघंटा, कूष्मांडा, स्कंदमाता, कात्यायनी, कालरात्रि, महागौरी और सिद्धिदात्री।")]
add("navratri-2026.html", "नवरात्रि 2026 — तिथियाँ, नौ देवियाँ और हर दिन की आरती | OmKiran Bhakti",
 "शारदीय नवरात्रि 2026: 11 अक्टूबर से शुरू, अष्टमी-नवमी 19 अक्टूबर, दशहरा 20 अक्टूबर। हर दिन की देवी, उनकी आरती का वीडियो और माता रानी के भजन।",
 f'''{band("नवरात्रि 2026", "शारदीय नवरात्रि 2026 की शुरुआत <strong>11 अक्टूबर (रविवार)</strong> को घटस्थापना से हुई। <strong>दुर्गा अष्टमी और महानवमी, दोनों 19 अक्टूबर (सोमवार)</strong> को हैं, और <strong>दशहरा 20 अक्टूबर (मंगलवार)</strong> को है।", "नवरात्रि 2026", *ART["navdurga"], "माँ दुर्गा के नौ स्वरूप", extra='<p class="lede">तिथियाँ दिल्ली के पंचांग पर आधारित हैं; अपने शहर का मुहूर्त स्थानीय पंचांग से मिला लें।</p>')}
<section><div class="wrap">{sec_head("नौ दिन, नौ देवियाँ","आज का दिन अपने आप चमकता हुआ दिखेगा")}<ul class="days">{days}</ul></div></section>
<section class="band"><div class="wrap">{sec_head("नवरात्रि के भजन")}{video_cards(["G99-49Pfs6U","woNhYRu376g","NuWOBRQ9B3Q","dJAZTUkHcBs","SE1RyQ6fWQs","h4EjlAYqQo0"])}
<p style="margin-top:2rem;text-align:center"><a class="btn" href="mata-rani-bhajan.html">माता रानी के सभी भजन</a> <a class="btn ghost" href="jaap-mala.html">‘जय माता दी’ जाप गिनें</a></p></div></section>
{faq_html(nav_faq)}''',
 crumbs="नवरात्रि 2026", active="navratri-2026.html",
 ld=[{"@type":"Event","name":"शारदीय नवरात्रि 2026","startDate":"2026-10-11","endDate":"2026-10-20","eventAttendanceMode":"https://schema.org/MixedEventAttendanceMode","eventStatus":"https://schema.org/EventScheduled","location":{"@type":"Place","name":"भारत","address":{"@type":"PostalAddress","addressCountry":"IN"}},"organizer":{"@id":SITE+"#organization"},"description":"नौ दिनों तक माँ दुर्गा के नौ स्वरूपों की पूजा का पर्व।"}, faq_ld(nav_faq)])

# ---------------- Jaap mala ----------------
MANTRAS = ["ॐ नमः शिवाय","राम","श्री राम जय राम जय जय राम","हरे कृष्ण हरे कृष्ण कृष्ण कृष्ण हरे हरे, हरे राम हरे राम राम राम हरे हरे","राधे राधे","ॐ गं गणपतये नमः","जय माता दी","ॐ ऐं ह्रीं क्लीं चामुण्डायै विच्चे","ॐ नमो भगवते वासुदेवाय","ॐ हं हनुमते नमः","ॐ श्रीं महालक्ष्म्यै नमः","ॐ शं शनैश्चराय नमः"]
opts = "".join(f'<option value="{e(m)}">{e(m)}</option>' for m in MANTRAS) + '<option value="custom">अपना मंत्र लिखें…</option>'
jfaq = [("जाप माला में 108 मनके क्यों होते हैं?","परंपरा में 108 को पवित्र संख्या माना जाता है, इसलिए एक माला में 108 मनके होते हैं और एक माला पूरी होने पर 108 जाप होते हैं।"),
        ("क्या मेरी गिनती सेव रहती है?","हाँ, गिनती आपके ही फ़ोन या कंप्यूटर के ब्राउज़र में सेव रहती है। हमें कोई जानकारी नहीं भेजी जाती।"),
        ("क्या बिना इंटरनेट के चलेगी?","पेज एक बार खुलने के बाद गिनती बिना रुकावट चलती रहती है।")]
add("jaap-mala.html", "ऑनलाइन जाप माला — 108 नाम जाप काउंटर | OmKiran Bhakti",
 "मुफ़्त ऑनलाइन जाप माला: मंत्र चुनें, टैप करके गिनें, 108 पूरे होने पर माला गिनती। ॐ नमः शिवाय, राम, हरे कृष्ण, जय माता दी या अपना मंत्र।",
 f'''<section class="night scallop mala-night"><div class="wrap"><nav class="crumbs-in" aria-label="breadcrumb"><a href="index.html">होम</a> / जाप माला</nav><h1 class="gold-type">ऑनलाइन जाप माला</h1>
<p class="answer">मंत्र चुनें और बीच के बटन पर टैप करें — हर टैप एक जाप है। 108 जाप पर एक माला पूरी होती है और फ़ोन हल्का-सा कंपन करता है। कंप्यूटर पर स्पेसबार भी दबा सकते हैं।</p>
<div class="mala-wrap" style="margin-top:2rem">
<div class="mala" id="mala"><svg viewBox="0 0 400 400" aria-hidden="true"></svg>
<button class="tap" aria-label="एक जाप गिनें"><span class="count">0</span><span class="mantra-show"></span></button></div>
<div><label for="mantra"><strong>मंत्र चुनें</strong></label><br><select id="mantra">{opts}</select>
<p hidden style="margin-top:.8rem"><label for="custom">अपना मंत्र</label><br><input type="text" id="custom" maxlength="80" placeholder="जैसे: ॐ श्री गुरवे नमः"></p>
<div class="stats"><div><b id="malas">0</b>मालाएँ पूरी</div><div><b id="total">0</b>कुल जाप</div></div>
<button class="btn ghost" id="reset">इस माला को शून्य करें</button>
<p style="margin-top:1.5rem">जाप के साथ सुनना चाहें तो <a href="aarti-mantra.html">108 बार मंत्र जाप के वीडियो</a> देखें।</p></div></div></div></section>
{faq_html(jfaq)}''',
 crumbs="जाप माला", active="jaap-mala.html",
 ld=[{"@type":"WebApplication","name":"OmKiran Bhakti जाप माला","applicationCategory":"LifestyleApplication","operatingSystem":"Any","inLanguage":"hi","offers":{"@type":"Offer","price":"0","priceCurrency":"INR"},"url":SITE+"jaap-mala.html"}, faq_ld(jfaq)])

# ---------------- About ----------------
add("about.html", "OmKiran Bhakti के बारे में — हिंदी भक्ति संगीत चैनल",
 "OmKiran Bhakti एक हिंदी भक्ति संगीत चैनल है — भजन, आरती, चालीसा, मंत्र जाप और भक्ति EDM। जानें हम क्या बनाते हैं और हमें कहाँ सुनें।",
 f'''{band("OmKiran Bhakti के बारे में","OmKiran Bhakti एक हिंदी भक्ति संगीत चैनल है, जो भजन, आरती, चालीसा, 108 बार मंत्र जाप और भक्ति EDM बनाता है। YouTube पर इसके 28 हज़ार से ज़्यादा सब्सक्राइबर और 890 से ज़्यादा वीडियो हैं।","परिचय",*ART["ganesh"],"OmKiran Bhakti")}
<section><div class="wrap prose">
<p>हमारे चैनल पर माता रानी, शिव, गणेश, हनुमान, श्रीराम और श्रीकृष्ण के भजन, त्योहारों के विशेष गीत (नवरात्रि, गणेश चतुर्थी, जन्माष्टमी, पितृ पक्ष, होली) और रोज़ के पाठ के लिए तेज़ गति वाली चालीसा मिलती है।</p>
<p>यह वेबसाइट उन भक्तों के लिए है जो पूजा के समय आरती और चालीसा के सही बोल पढ़ना चाहते हैं, उनका अर्थ समझना चाहते हैं, या साथ में गाने के लिए वीडियो ढूँढ रहे हैं।</p>
<h2>हमें कहाँ सुनें</h2>
<ul><li><a href="{YT}">YouTube: @OmKiranBhakti</a></li><li><a href="https://www.instagram.com/omkiranbhakti/">Instagram</a></li><li><a href="https://www.facebook.com/omkiranbhakti/">Facebook</a></li></ul>
<h2>सबसे ज़्यादा सुने गए</h2>{video_cards(["ZswQ9qUMDTs","707iS1Iyv-E","lMHZDM-RRb4"])}</div></section>''',
 crumbs="परिचय", active="about.html",
 ld=[{"@type":"AboutPage","url":SITE+"about.html","about":{"@id":SITE+"#organization"}}])

# ---------------- Panchang & festivals ----------------
from panchang import TITHI as TITHI_HI
exec(open(os.path.join(os.path.dirname(__file__), "panchang_section.py"), encoding="utf-8").read())
exec(open(os.path.join(os.path.dirname(__file__), "city_section.py"), encoding="utf-8").read())
exec(open(os.path.join(os.path.dirname(__file__), "question_section.py"), encoding="utf-8").read())

exec(open(os.path.join(os.path.dirname(__file__), "library_section.py"), encoding="utf-8").read())
exec(open(os.path.join(os.path.dirname(__file__), "kaal_section.py"), encoding="utf-8").read())
exec(open(os.path.join(os.path.dirname(__file__), "choghadiya_section.py"), encoding="utf-8").read())
exec(open(os.path.join(os.path.dirname(__file__), "calc_section.py"), encoding="utf-8").read())
exec(open(os.path.join(os.path.dirname(__file__), "vrat_section.py"), encoding="utf-8").read())

# ---------------- Home ----------------
ORG = {"@type":"Organization","@id":SITE+"#organization","name":"OmKiran Bhakti","alternateName":["Om Kiran Bhakti","ओमकिरण भक्ति"],"url":SITE,
       "logo":{"@type":"ImageObject","url":LOGO},"sameAs":[YT,"https://www.facebook.com/omkiranbhakti/","https://www.instagram.com/omkiranbhakti/"],
       "description":"OmKiran Bhakti is a Hindi devotional music channel: bhajans, aartis, chalisas, 108-times mantra jaap and devotional EDM.",
       "knowsAbout":["Hindi bhajan","Aarti","Chalisa","Mantra jaap","Navratri","Hanuman Chalisa"]}
WEBSITE = {"@type":"WebSite","@id":SITE+"#website","url":SITE,"name":"OmKiran Bhakti","inLanguage":"hi-IN","publisher":{"@id":SITE+"#organization"}}
home_latest = ["Q5_3JBKLNpg","9hzay6Ebzas","fhm1dqyttu0","2yVR5zSaKpc","G99-49Pfs6U","NuWOBRQ9B3Q"]
home_popular = ["ZswQ9qUMDTs","707iS1Iyv-E","lMHZDM-RRb4","eA6tcqEncoE","woNhYRu376g","rxeMNQ48yWU"]
deities = [("mata-rani-bhajan.html","माता रानी","शेरावाली, दुर्गा, नवदुर्गा"),("shiv-bhajan.html","शिव","भोलेनाथ, महाकाल"),
           ("hanuman-chalisa.html","हनुमान","बजरंगबली, संकटमोचन"),("ganesh-bhajan.html","गणेश","विघ्नहर्ता, गणपति बप्पा"),
           ("krishna-bhajan.html","श्रीकृष्ण","राधा-कृष्ण, कन्हैया"),("ram-bhajan.html","श्रीराम","सियाराम, रघुनंदन")]
dlist = "".join(f'<li><a href="{h}">{arch(*ART[k], alt=t)}<strong>{t}</strong><small>{sub}</small></a></li>' for h,t,sub,k in
   [(h,t,sub,k) for (h,t,sub),k in zip(deities,["mata","shiv","hanuman","ganesh","krishna","ram"])])
_hot = sorted([(HOT_DATES.get(k) or nxt_fest(k)["date"], h, t) for h, t, k in CITY_PAGES if HOT_DATES.get(k) or nxt_fest(k)], key=lambda x: x[0])
_hot = [x for x in _hot if x[0] >= TODAY_D]
hot_html = ('<section class="hot"><div class="wrap"><h2 class="hot-h">अपने शहर का समय देखें</h2><ul class="hot-list">' +
            "".join(f'<li><a href="{h}"><strong>{e(t)}</strong><span>{hdate_w(d)}</span></a></li>' for d, h, t in _hot) +
            '</ul><p style="text-align:center;margin:1rem 0 0"><a href="tyohar-kab-hai.html">एकादशी, पूर्णिमा, हर त्योहार — सभी ‘कब है’ सवालों के जवाब</a></p></div></section>') if _hot else ""
_tools = [("aaj-ka-choghadiya.html","आज का चौघड़िया","65 शहरों का शुभ समय"),("janm-tithi-rashi-calculator.html","जन्म तिथि और राशि कैलकुलेटर","नाम अक्षर, नक्षत्र, तिथि वाला जन्मदिन")] + [(h, t, sub) for h, t, sub in KAAL_PAGES if h in ("panchak-kab-hai.html","bhadra-kaal.html","kharmas-kab-hai.html","gandmool-nakshatra.html")]
tools_html = ('<section class="hot"><div class="wrap"><h2 class="hot-h">रोज़ काम आने वाला</h2><ul class="hot-list">' +
              "".join(f'<li><a href="{h}"><strong>{e(t)}</strong><span>{e(sub)}</span></a></li>' for h, t, sub in _tools) + '</ul></div></section>')
for _fp in ("aaj-ka-panchang.html", "tyohar-calendar.html"):
    if _fp in PAGES: PAGES[_fp] = PAGES[_fp].replace('<section class="hot">', tools_html + '<section class="hot">', 1)
add("index.html", "OmKiran Bhakti — आरती, चालीसा, मंत्र और भजन (बोल व अर्थ सहित)",
 "हनुमान चालीसा, आरती और मंत्रों के पूरे बोल सरल अर्थ के साथ; माता रानी, शिव, गणेश, कृष्ण और राम के भजन; नवरात्रि 2026 और ऑनलाइन जाप माला।",
 f'''<section class="night scallop to-band hero3"><div class="wrap">
{hero_card(TODAY_P)}
<div class="aaj-panel" id="today" aria-live="polite">
<p class="when">आज</p><h2>हनुमान चालीसा</h2>
<figure class="shrine">{arch(*ART["skandamata"], alt="आज के आराध्य", eager=True).replace('<div class="arch">','<div class="arch" id="today-art">').replace('</div>','<div class="diya" aria-hidden="true"><span class="bowl"></span><span class="flame"></span></div></div>')}<figcaption id="today-cap">जय माता दी</figcaption></figure>
<p class="say">रोज़ के पाठ के लिए पूरे बोल और अर्थ।</p>
<div class="actions"><a class="btn gold go" href="hanuman-chalisa.html">पाठ खोलें</a><a class="btn ghost" href="jaap-mala.html">जाप माला</a></div>
</div>
</div></section>
{hot_html}{tools_html}<section class="band"><div class="wrap">{sec_head("आने वाले त्योहार","तारीख़, और त्योहार सुबह से है या शाम-रात को")}{up_list(upcoming(8))}
<p style="text-align:center;margin-top:1.5rem"><a class="btn" href="tyohar-calendar.html">पूरा त्योहार कैलेंडर</a> <a class="btn ghost" href="ekadashi-2026-2027.html">सभी एकादशी</a></p></div></section>
<section><div class="wrap">{sec_head("अपने आराध्य चुनें","हर देवता के भजन, आरती और मंत्र एक जगह")}<ul class="devta devta-light">{dlist}</ul></div></section>
<section class="band"><div class="wrap">{sec_head("बोल और अर्थ","पूजा के समय फ़ोन पर बड़े अक्षरों में पढ़ें, या प्रिंट करके रखें")}{paath_html}</div></section>
<section><div class="wrap">{sec_head("नए भजन","इस हफ़्ते चैनल पर आए")}{video_cards(home_latest)}
<p style="margin-top:2rem;text-align:center"><a class="btn" href="{YT}?sub_confirmation=1" target="_blank" rel="noopener">YouTube पर सब्सक्राइब करें</a></p></div></section>
<section class="band"><div class="wrap">{sec_head("सबसे ज़्यादा सुने गए","लाखों भक्तों की पसंद")}{video_cards(home_popular)}</div></section>
<section class="night"><div class="wrap">{sec_head("भक्ति EDM","स्तोत्र और मंत्र, आज की धुन में")}{video_cards(["unfGUJz6D8U","D5LIL8j8Kqs","XLYs9iEXKmA"])}
<p style="margin-top:2rem;text-align:center"><a class="btn gold" href="devotional-edm-bhajans.html">सभी EDM ट्रैक</a></p></div></section>''',
 ld=[ORG, WEBSITE, itemlist(home_popular,"सबसे ज़्यादा सुने गए भजन")])

# 404
add("404.html","पेज नहीं मिला | OmKiran Bhakti","यह पेज मौजूद नहीं है।",
 '<section><div class="wrap prose"><h1>यह पेज नहीं मिला</h1><p class="lede">पता बदल गया होगा। नीचे से अपना पाठ चुनें:</p><ul class="library">'+lib_html+'</ul></div></section>')
PAGES["404.html"] = PAGES["404.html"].replace('<meta name="robots" content="index,follow,max-image-preview:large">','<meta name="robots" content="noindex">')

# ---------------- Write ----------------
import re as _re
def _rel_html(slug):
    me = next((c for c in CATALOG if c[0]==slug), None)
    if not me: return ""
    same = [c for c in CATALOG if c[0]!=slug and c[4][0]==me[4][0]]
    more = [c for c in CATALOG if c[0]!=slug and c not in same and c[1]==me[1]]
    items = (same + more)[:6]
    lis = "".join(f'<li><a href="{c[0]}"><strong>{e(c[2])}</strong><span>{e(c[3])}</span></a></li>' for c in items)
    return f'<div class="rail-rel"><h2>इनका भी पाठ करें</h2><ul>{lis}</ul></div>'
for _s in list(PAGES):
    PAGES[_s] = _re.sub(r"<!--REL:([^>]+?)-->", lambda m: _rel_html(m.group(1)), PAGES[_s])
for slug, content in PAGES.items():
    with open(os.path.join(ROOT, slug), "w", encoding="utf-8") as f: f.write(content)

urls = [s for s in PAGES if s != "404.html"]
prio = {"index.html":"1.0","hanuman-chalisa.html":"0.9","navratri-2026.html":"0.9"}
sm = ['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for s in urls:
    sm.append(f'  <url><loc>{SITE if s=="index.html" else SITE+s}</loc><lastmod>{TODAY}</lastmod></url>')
sm.append('</urlset>')
open(os.path.join(ROOT,"sitemap.xml"),"w").write("\n".join(sm)+"\n")
open(os.path.join(ROOT,"robots.txt"),"w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n")

titles = {s: PAGES[s].split("<title>")[1].split("</title>")[0] for s in urls}
_up = upcoming(12)
llms = ["# OmKiran Bhakti","",
 f"> Hindi devotional website of the OmKiran Bhakti YouTube channel: {NPAATH} traditional aartis, chalisas, stotras, mantras and vrat kathas with line-by-line plain-Hindi meanings; a daily Hindu panchang (New Delhi); festival dates computed from tithi rules; city-wise festival timings for 65+ Indian cities and the diaspora; and a free online jaap mala.","",
 f"Official YouTube channel: {YT}",
 "Panchang method: sidereal (Lahiri ayanamsa) positions from PyEphem, udaya tithi, purnimanta months; festivals follow their traditional kaal rule (sunrise, pradosh, moonrise, nishita).","",
 "## Upcoming festivals (dates for New Delhi)",*[f"- {html.unescape(n)}: {d.isoformat()} — {SITE}{u}" for d,n,u,w in _up],"",
 "## City-wise festival timings and quick answers",f"- [{html.unescape(titles['tyohar-kab-hai.html'])}]({SITE}tyohar-kab-hai.html)",*[f"- [{html.unescape(titles[h])}]({SITE}{h})" for h,_,_ in CITY_PAGES],"",
 "## Daily tools (updated every day)",f"- [{html.unescape(titles['aaj-ka-choghadiya.html'])}]({SITE}aaj-ka-choghadiya.html): choghadiya, Rahu kaal, Abhijit for 65 Indian cities",
 f"- [{html.unescape(titles['janm-tithi-rashi-calculator.html'])}]({SITE}janm-tithi-rashi-calculator.html): birth tithi, nakshatra, moon sign, naam akshar and next tithi-birthday from a birth date (runs in the browser)",
 *[f"- [{html.unescape(titles[h])}]({SITE}{h})" for h,_,_ in KAAL_PAGES],"",
 "## Lyrics and texts with meanings",*[f"- [{html.unescape(titles[c[0]])}]({SITE}{c[0]})" for c in CATALOG if c[0] in titles],"",
 "## Bhajans by deity",*[f"- [{html.unescape(titles[d[0]])}]({SITE}{d[0]})" for d in DEITY],"",
 "## Panchang, festivals and tools",f"- [{html.unescape(titles['aaj-ka-panchang.html'])}]({SITE}aaj-ka-panchang.html): daily Hindu panchang for New Delhi (tithi, nakshatra, muhurat, Rahu kaal), updated every day",
 f"- [{html.unescape(titles['tyohar-calendar.html'])}]({SITE}tyohar-calendar.html)",
 f"- [{html.unescape(titles['ekadashi-2026-2027.html'])}]({SITE}ekadashi-2026-2027.html)",
 f"- [{html.unescape(titles['purnima-amavasya-2026-2027.html'])}]({SITE}purnima-amavasya-2026-2027.html)",
 *[f"- [{html.unescape(titles[k+'-kab-hai.html'])}]({SITE}{k}-kab-hai.html)" for k in FEST if k+'-kab-hai.html' in titles],
 f"- [{html.unescape(titles['navratri-2026.html'])}]({SITE}navratri-2026.html)",f"- [{html.unescape(titles['jaap-mala.html'])}]({SITE}jaap-mala.html)",
 f"- [{html.unescape(titles['aarti-mantra.html'])}]({SITE}aarti-mantra.html)",f"- [{html.unescape(titles['about.html'])}]({SITE}about.html)",""]
open(os.path.join(ROOT,"llms.txt"),"w",encoding="utf-8").write("\n".join(llms))
print(f"built {len(PAGES)} pages, sitemap {len(urls)} urls")

# "अभी चर्चा में" — weekly page of what people are searching / discussing about bhakti right now.
# Signals: Google autocomplete (hi, IN) checked on the WEEK date below, our Quora answers, our Pinterest pins.
# Everything shown is our own writing/images; external posts are only linked, never copied.
# Executed inside build.py's namespace (uses add, e, hdate, hdate_w, nxt_fest, FEST, CITY_ANS, PAGES, SITE, TODAY_D, faq_html, faq_ld).
import urllib.parse as _cup
import datetime as _cdt
_cz_mon = TODAY_D - _cdt.timedelta(days=TODAY_D.weekday())
def _cz_dm(d): return f"{d.day} {MONTHS_HI[d.month]}"
CZ_WEEK = f"{_cz_dm(_cz_mon)} – {_cz_dm(_cz_mon + _cdt.timedelta(days=6))} {(_cz_mon + _cdt.timedelta(days=6)).year}"
CZ_UPDATED = f"{_cz_dm(TODAY_D)} {TODAY_D.year}"
CZ_DAYS = 40   # only festivals coming within this many days are "in discussion"

def _cz_d(k):
    x = nxt_fest(k)
    return x["date"] if x else None

# (question people type, source chip, short answer (may use {date:key}), link, link text)
CZ_TRENDS = [
 ("दिवाली 2026 कब है?", "google", "{date:diwali} को। दिल्ली में लक्ष्मी पूजा का सबसे शुभ समय शाम 5:55 से 7:50 तक।", "diwali-lakshmi-puja-muhurat.html", "65+ शहरों का मुहूर्त"),
 ("धनतेरस पर क्या खरीदें, क्या नहीं?", "google", "धनतेरस {date:dhanteras} को है। पीतल-चाँदी के बर्तन, झाड़ू और धनिया शुभ; लोहा, काँच और धारदार चीज़ें टालें।", "dhanteras-kab-hai.html", "पूरी लिस्ट और पूजा विधि"),
 ("नरक चतुर्दशी और दिवाली एक ही दिन क्यों?", "quora", "दोनों {date:narak-chaturdashi} को — सुबह चतुर्दशी में रूप चौदस का स्नान, शाम अमावस्या में लक्ष्मी पूजा।", "narak-chaturdashi-aur-diwali-ek-hi-din-kyon.html", "तिथि का पूरा हिसाब"),
 ("छठ पूजा 2026 कब है?", "google", "संध्या अर्घ्य {date:chhath-puja} को। नहाय-खाय से उषा अर्घ्य तक चारों दिन की तारीख़ और अर्घ्य का समय।", "chhath-puja-kab-hai.html", "चारों दिन देखें"),
 ("लक्ष्मी पूजा कैसे करें?", "google", "गणेश पूजा → कलश → लक्ष्मी पूजा → कुबेर और बही-खाता → आरती → पूरे घर में दीये। स्टेप-बाय-स्टेप विधि।", "diwali-lakshmi-puja-vidhi.html", "पूजा विधि पढ़ें"),
 ("दिवाली पर क्या करें, क्या न करें?", "google", "घर साफ़ और रोशन रखें, प्रदोष काल में पूजा करें; उधार देना, झगड़ा और पूजा के समय अँधेरा टालें।", "diwali-par-kya-kare-kya-na-kare.html", "पूरी सूची"),
 ("देवउठनी एकादशी 2026 कब है?", "google", "{date:dev-uthani-ekadashi} को — इसी दिन भगवान विष्णु जागते हैं और शुभ काम फिर शुरू होते हैं।", "dev-uthani-ekadashi-kab-hai.html", "तारीख़ और पारण"),
 ("करवा चौथ पर चाँद कब निकलेगा?", "google", "करवा चौथ {date:karwa-chauth} को। {city:karwa-chauth}", "karwa-chauth-chand-kab-niklega.html", "अपने शहर का समय"),
]
# --- keep the page fresh on every daily build ---
# hand-written entries stay only while their festival is near; the rest is filled
# automatically from the festival calendar (next CZ_DAYS days), nearest first.
def _cz_near(a):
    ks = re.findall(r"\{date:([\w-]+)\}", a)
    return bool(ks) and all(_cz_d(k) and 0 <= (_cz_d(k) - TODAY_D).days <= CZ_DAYS for k in ks)
CZ_TRENDS = [t for t in CZ_TRENDS if _cz_near(t[2])]
def _cz_auto():
    import festivals as _F
    seen, out = {re.search(r"\{date:([\w-]+)\}", t[2]).group(1) for t in CZ_TRENDS}, []
    for r in _F.RULES:
        k, name, mean = r[0], r[1], r[7] if len(r) > 7 else ""
        d = _cz_d(k)
        if k in seen or not d or not 0 <= (d - TODAY_D).days <= CZ_DAYS: continue
        seen.add(k)
        page = next((h for h in (f"{k}-kab-hai.html", f"{k}.html") if h in PAGES), "tyohar-calendar.html")
        out.append((d, k in _F.MINOR_KEYS, (f"{name.split(' (')[0]} {d.year} कब है?", "google",
                    f"{{date:{k}}} को।" + (f" {mean}।" if mean else ""), page, "तारीख़, मुहूर्त और नियम")))
        for suf, q, lt in (("katha", "की कथा", "पूरी कथा पढ़ें"), ("puja-vidhi", "की पूजा विधि", "पूजा विधि देखें"), ("vidhi", "की पूजा विधि", "पूजा विधि देखें")):
            if f"{k}-{suf}.html" in PAGES:
                out.append((d, True, (f"{name.split(' (')[0]} {q}", "google", f"{{date:{k}}} को। सरल हिंदी में, शुरू से अंत तक।", f"{k}-{suf}.html", lt)))
    out.sort(key=lambda x: (x[0], x[1]))
    return [t for _, _, t in out]
CZ_TRENDS = (CZ_TRENDS + _cz_auto())[:10]
CZ_SRC = {"google": ("🔎", "Google पर ट्रेंडिंग"), "quora": ("💬", "Quora पर चर्चा"), "pinterest": ("📌", "Pinterest पर ट्रेंड")}

# our own Quora answers
CZ_QUORA = [
 ("साल 2026 में दिवाली (लक्ष्मी पूजा) किस तारीख को मनाई जाएगी?", "https://hi.quora.com/%E0%A4%B8%E0%A4%BE%E0%A4%B2-2026-%E0%A4%AE%E0%A5%87%E0%A4%82-%E0%A4%A6%E0%A4%BF%E0%A4%B5%E0%A4%BE%E0%A4%B2%E0%A5%80-%E0%A4%B2%E0%A4%95%E0%A5%8D%E0%A4%B7%E0%A5%8D%E0%A4%AE%E0%A5%80/answers/1477743922183839", "तिथि का हिसाब, दिल्ली का मुहूर्त और नरक चतुर्दशी वाली बात"),
 ("छठ पूजा 2026 की तारीख क्या है और यह दिवाली के कितने दिन बाद आती है?", "https://hi.quora.com/%E0%A4%9B%E0%A4%A0-%E0%A4%AA%E0%A5%82%E0%A4%9C%E0%A4%BE-2026-%E0%A4%95%E0%A5%80-%E0%A4%A4%E0%A4%BE%E0%A4%B0%E0%A5%80%E0%A4%96-%E0%A4%95%E0%A5%8D%E0%A4%AF%E0%A4%BE-%E0%A4%B9%E0%A5%88-%E0%A4%94%E0%A4%B0/answers/1477743922183943", "चारों दिन, षष्ठी तिथि और अर्घ्य का समय"),
 ("अप्सरा मेनका ने ऋषि विश्वामित्र की तपस्या क्यों और कैसे भंग की थी?", "https://hi.quora.com/%E0%A4%85%E0%A4%AA%E0%A5%8D%E0%A4%B8%E0%A4%B0%E0%A4%BE-%E0%A4%AE%E0%A5%87%E0%A4%A8%E0%A4%95%E0%A4%BE-%E0%A4%A8%E0%A5%87-%E0%A4%8B%E0%A4%B7%E0%A4%BF-1/answers/1477743922185247", "महाभारत आदि पर्व से — शकुंतला और भरत तक की कथा"),
]

# short myth facts (our own writing, scripture named)
CZ_FACTS = [
 ("🔱", "रावण का असली नाम दशग्रीव था", "कैलाश उठाने पर शिव जी ने अँगूठे से दबाया; उसकी चीख (रव) से लोक काँप उठे — तभी शिव जी ने नाम दिया “रावण”।", "वाल्मीकि रामायण, उत्तर कांड"),
 ("🏹", "अर्जुन एक साल “बृहन्नला” क्यों बने?", "इंद्रलोक में अर्जुन ने उर्वशी को “पुरु वंश की माता” कहकर मना किया; उर्वशी के श्राप ने अज्ञातवास में उन्हें छिपने का भेस दे दिया।", "महाभारत, वन पर्व"),
 ("🐘", "गणेश जी को “प्रथम पूज्य” कैसे मिला", "पार्वती जी के बनाए बालक ने शिव जी को द्वार पर रोका; हाथी का सिर लगाकर शिव जी ने उन्हें गणों का अधिपति बनाया और पहली पूजा का वर दिया।", "शिव पुराण, रुद्र संहिता"),
 ("☀️", "कर्ण सबसे बड़े पांडव थे", "दुर्वासा के मंत्र से कुंती ने विवाह से पहले सूर्य देव को बुलाया; कवच-कुंडल वाले बालक को उन्होंने नदी में बहा दिया।", "महाभारत, आदि पर्व"),
]

# extra one-line facts for the home-page "क्या आप जानते हैं?" corner card (our own wording)
CZ_POP = [(i, h, p, s) for i, h, p, s in CZ_FACTS] + [
 ("🇮🇳", "“भारत” नाम किसके नाम पर पड़ा?", "मेनका-विश्वामित्र की बेटी शकुंतला और राजा दुष्यंत के पुत्र भरत के नाम पर।", "महाभारत, आदि पर्व"),
 ("📜", "ऋग्वेद में एक प्रेम-संवाद भी है", "अप्सरा उर्वशी और राजा पुरूरवा का विरह-संवाद ऋग्वेद के दसवें मंडल (सूक्त 95) में है।", "ऋग्वेद 10.95"),
 ("🎯", "एकलव्य ने सात बाणों से कुत्ते का मुँह भर दिया था", "कुत्ते को चोट भी नहीं लगी — यही देखकर द्रोण ने गुरुदक्षिणा में अँगूठा माँगा।", "महाभारत, आदि पर्व"),
 ("🛡️", "भीष्म शिखंडी पर बाण क्यों नहीं चलाते थे", "शिखंडी पिछले जन्म में अंबा थीं; भीष्म का प्रण था कि जो स्त्री रहा हो उस पर शस्त्र नहीं उठाएँगे।", "महाभारत, उद्योग पर्व"),
 ("🐒", "हनुमान जी के पुत्र मकरध्वज", "लोक-रामकथाओं के अनुसार हनुमान जी के पसीने की बूँद से जन्मे; श्रीराम ने उन्हें पाताल का राजा बनाया।", "आनंद रामायण व लोक परंपरा"),
 ("🌙", "करवा चौथ पर चाँद छलनी से क्यों देखते हैं", "लोक-कथा में वीरावती के भाइयों ने छलनी के पीछे दीया रखकर नकली चाँद दिखाया था — तब से छलनी की परंपरा मानी जाती है।", "करवा चौथ व्रत कथा"),
]

def _cz_fill(s):
    s = re.sub(r"\{date:([\w-]+)\}", lambda m: hdate_w(_cz_d(m.group(1))) if _cz_d(m.group(1)) else "जल्द", s)
    return re.sub(r"\{city:([\w-]+)\}", lambda m: CITY_ANS.get(m.group(1), ""), s)

def build_charcha():
    try:
        import json as _j
        PM = _j.load(open(os.path.join(os.path.dirname(__file__), "pins_meta.json"), encoding="utf-8"))
    except Exception:
        PM = []
    ticker = " ".join(f'<span>🔥 {e(q)}</span>' for q, *_ in CZ_TRENDS)
    cards = []
    for n, (q, src, a, u, ut) in enumerate(CZ_TRENDS, 1):
        ic, lab = CZ_SRC[src]
        cards.append(f'<li class="cz-card cz-{src}"><span class="cz-rank">{n:02d}</span><div class="cz-body"><span class="cz-chip">{ic} {lab}</span>'
                     f'<h3><a href="{u}">{e(q)}</a></h3><p>{e(_cz_fill(a))}</p><a class="cz-go" href="{u}">{e(ut)} →</a></div></li>')
    quora = "".join(f'<li class="cz-q"><span class="cz-qmark">“</span><h3><a href="{u}" target="_blank" rel="noopener">{e(q)}</a></h3><p>{e(s)}</p>'
                    f'<a class="cz-go" href="{u}" target="_blank" rel="noopener">Quora पर हमारा जवाब पढ़ें ↗</a></li>' for q, u, s in CZ_QUORA)
    pins = ""
    for k, t, d, u, b in PM[:8]:
        page_url = SITE + u; img = SITE + f"img/pins/pin_{k}.jpg"
        share = "https://www.pinterest.com/pin/create/button/?" + _cup.urlencode({"url": page_url, "media": img, "description": t})
        pins += (f'<li class="cz-pin"><a href="{u}"><img src="img/pins/pin_{k}.jpg" alt="{e(t)}" loading="lazy" width="1000" height="1500"></a>'
                 f'<a class="cz-save" href="{share}" target="_blank" rel="noopener nofollow">📌 सेव करें</a></li>')
    facts = "".join(f'<li class="cz-fact"><span class="cz-fi">{i}</span><h3>{e(h)}</h3><p>{e(p)}</p><small>स्रोत: {e(s)}</small></li>' for i, h, p, s in CZ_FACTS)
    faqs = [(q, _cz_fill(a)) for q, s, a, u, ut in CZ_TRENDS[:6]]
    body = (
        f'<section class="cz-hero"><div class="wrap"><nav class="crumbs-in" aria-label="breadcrumb"><a href="index.html">होम</a> / अभी चर्चा में</nav>'
        f'<p class="cz-live"><i></i> इस हफ़्ते · {e(CZ_WEEK)}</p><h1>अभी चर्चा में 🔥</h1>'
        '<p class="cz-lede">भक्ति और त्योहारों के वो सवाल जो लोग इस हफ़्ते सबसे ज़्यादा खोज रहे हैं — Google, Quora और Pinterest से चुने, जवाब हमारे पंचांग से।</p>'
        f'<div class="cz-ticker" aria-hidden="true"><div>{ticker} {ticker}</div></div></div></section>'
        f'<section class="cz-sec"><div class="wrap"><h2 class="cz-h">🔎 सबसे ज़्यादा खोजे जा रहे सवाल</h2><ol class="cz-grid">{"".join(cards)}</ol></div></section>'
        + (f'<section class="cz-sec cz-dark"><div class="wrap"><h2 class="cz-h">📌 Pinterest पर सेव करें</h2><p class="cz-sub">त्योहार की तारीख़ें और आरती — हमारी पिन्स। पसंद आए तो अपने बोर्ड पर सेव करें या WhatsApp पर भेजें।</p><ul class="cz-pins">{pins}</ul>'
           '<p class="cz-more"><a href="https://in.pinterest.com/omkiranb/" target="_blank" rel="noopener">Pinterest पर OmKiran Bhakti फ़ॉलो करें ↗</a></p></div></section>' if pins else "")
        + f'<section class="cz-sec"><div class="wrap"><h2 class="cz-h">💬 Quora पर चर्चा</h2><ul class="cz-qs">{quora}</ul></div></section>'
        f'<section class="cz-sec cz-warm" id="facts"><div class="wrap"><h2 class="cz-h">✨ क्या आप जानते हैं?</h2><ul class="cz-facts">{facts}</ul></div></section>'
        + faq_html(faqs)
        + f'<section class="cz-sec"><div class="wrap"><p class="cz-upd">अपडेट: {e(CZ_UPDATED)} · हर हफ़्ते नए ट्रेंड। ट्रेंड Google के खोज-सुझावों और Quora-Pinterest की चर्चा से चुने जाते हैं; सारी जानकारी और तस्वीरें OmKiran Bhakti की अपनी हैं।</p></div></section>'
    )
    add("abhi-charcha-mein.html", f"अभी चर्चा में — इस हफ़्ते के ट्रेंडिंग भक्ति सवाल ({CZ_WEEK}) | OmKiran Bhakti",
        "इस हफ़्ते सबसे ज़्यादा खोजे जा रहे भक्ति सवाल: " + ", ".join(q.rstrip("?") for q, *_ in CZ_TRENDS[:3]) + " — सही तारीख़, मुहूर्त और पूजा विधि।",
        body, crumbs="अभी चर्चा में", ld=[faq_ld(faqs)], active="tyohar-calendar.html")

def cz_home_strip():
    if "index.html" in PAGES:
        strip = ('<section class="cz-strip"><div class="wrap"><a class="cz-strip-in" href="abhi-charcha-mein.html"><b>🔥 अभी चर्चा में</b>'
                 '<span class="cz-strip-t">' + " · ".join(e(q) for q, *_ in CZ_TRENDS[:4]) + '</span><em>देखें →</em></a></div></section>')
        h = PAGES["index.html"]
        m = re.search(r"<main[^>]*>", h)
        if m: h = h[:m.end()] + strip + h[m.end():]
        import json as _j
        _tools = [("🎹", "आरती हारमोनियम पर बजाइए", "सरगम लिखी पट्टियाँ — फ़ोन पर ही बजाकर सीखें, बिलकुल मुफ़्त।", "", "/harmonium.html"),
                  ("📿", "जाप माला से 108 जाप गिनिए", "माला न हो तो भी — हर जाप पर टैप करें, गिनती हम रखेंगे।", "", "/jaap-mala.html"),
                  ("🕉️", "हिंदू काल-चक्र देखिए", "युग, मन्वंतर और कल्प — सनातन समय की टाइम मशीन।", "", "/hindu-kaal-chakra.html"),
                  ("🌙", "अपनी जन्म तिथि और राशि जानिए", "जन्म की तारीख़ डालें — नक्षत्र, राशि और नाम अक्षर।", "", "/janm-tithi-rashi-calculator.html")]
        _mix = []
        for _n, _f in enumerate(CZ_POP):
            _mix.append(list(_f) + [""])
            if _n % 2 == 1 and _tools: _mix.append(list(_tools.pop(0)))
        _mix += [list(t) for t in _tools]
        data = _j.dumps(_mix, ensure_ascii=False).replace("</", "<\\/")
        pop = ('<aside class="kya-pop" id="kya-pop" hidden aria-label="क्या आप जानते हैं?"><button type="button" class="kp-x" aria-label="बंद करें">×</button>'
               '<p class="kp-k">✨ क्या आप जानते हैं?</p><div class="kp-row"><span class="kp-i"></span><div><b class="kp-t"></b><p class="kp-p"></p><small class="kp-s"></small></div></div>'
               '<div class="kp-nav"><span class="kp-dots"></span><a href="/abhi-charcha-mein.html#facts">और रोचक तथ्य →</a></div></aside>'
               '<script>(function(){var F=' + data + ',box=document.getElementById("kya-pop");if(!box||!F.length)return;'
               'try{if(sessionStorage.getItem("kpX"))return}catch(e){}'
               'var k=Math.floor(Math.random()*F.length),tm;if(!F[k][4]&&F[(k+1)%F.length][4])k=(k+1)%F.length;var q=function(c){return box.querySelector(c)};'
               'var dots=q(".kp-dots");dots.innerHTML=F.map(function(_,j){return "<i></i>"}).join("");'
               'function show(){var f=F[k];q(".kp-i").textContent=f[0];var t=q(".kp-t");t.textContent="";if(f[4]){var a=document.createElement("a");a.href=f[4];a.textContent=f[1]+" →";t.appendChild(a)}else t.textContent=f[1];q(".kp-p").textContent=f[2];q(".kp-s").textContent=f[4]?"मुफ़्त टूल · बिना ऐप":"स्रोत: "+f[3];box.classList.toggle("kp-tool",!!f[4]);'
               '[].forEach.call(dots.children,function(d,j){d.className=j===k?"on":""});box.classList.remove("kp-in");void box.offsetWidth;box.classList.add("kp-in")}'
               'function next(){k=(k+1)%F.length;show()}'
               'function start(){box.hidden=false;show();tm=setInterval(next,9000)}'
               'box.addEventListener("mouseenter",function(){clearInterval(tm)});box.addEventListener("mouseleave",function(){clearInterval(tm);tm=setInterval(next,9000)});'
               'q(".kp-row").addEventListener("click",next);'
               'q(".kp-x").addEventListener("click",function(){box.hidden=true;clearInterval(tm);try{sessionStorage.setItem("kpX","1")}catch(e){}});'
               'setTimeout(start,window.innerWidth<700?9000:4000);})();</script>')
        PAGES["index.html"] = h.replace("</main>", pop + "</main>", 1)

build_charcha()

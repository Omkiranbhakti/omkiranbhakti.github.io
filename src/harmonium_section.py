# Online harmonium + harmonium learning pages. Executed inside build.py (after whatsapp_section).
# Uses add, band, sec_head, faq_html, faq_ld, e, SITE, TODAY, ver, PAGES.
# Player code: /harmonium.js. Notation: S r R g G M m P d D n N (r g d n komal, m tivra),
# "." before = mandra, "'" after = taar, "-" = hold one more beat.
# bpm = syllables (note units) per minute at the song's real singing speed; the player's speed slider scales it.
# Tunes: traditional melodies as commonly taught; regional tunes differ slightly — fix a line in HM_SONGS and rebuild.

HM_SONGS = [
 dict(id="om-jai-jagdish-hare", bpm=150, slug="om-jai-jagdish-hare-harmonium-notes.html", name="ॐ जय जगदीश हरे",
  lyric_page="om-jai-jagdish-hare-aarti.html", kw="Om Jai Jagdish Hare",
  lines=[("ॐ जय जगदीश हरे", "S - S - S S S - .N S R -"),
         ("स्वामी जय जगदीश हरे", "R G M - P P D P M G R -"),
         ("भक्त जनों के संकट", "R G R G M - M G R G R S"),
         ("दास जनों के संकट", "R G R G M - M G R G R S"),
         ("क्षण में दूर करे", "S S R - G R S .N .D -"),
         ("ॐ जय जगदीश हरे", "S - S - S S S - .N S R -")],
  about="यह आरती पंडित श्रद्धाराम फिल्लौरी ने 1870 के आसपास लिखी थी और आज लगभग हर घर में संध्या आरती में गाई जाती है। धुन मध्य सप्तक में ही चलती है, बस \"क्षण में दूर करे\" पर मंद्र नि और ध तक उतरती है — इसलिए यह हारमोनियम सीखने वालों का सबसे अच्छा पहला गाना है।"),
 dict(id="jai-ganesh-deva", bpm=170, slug="jai-ganesh-deva-harmonium-notes.html", name="जय गणेश जय गणेश देवा",
  lyric_page="ganesh-aarti-jai-ganesh-deva.html", kw="Jai Ganesh Deva",
  lines=[("जय गणेश जय गणेश जय गणेश देवा", "S S R R G G G G G G M G M G R R"),
         ("माता जाकी पार्वती पिता महादेवा", ".N .N S .N R R R R G G R S S -"),
         ("एक दंत दयावंत चार भुजा धारी", "S S G M P P P P M P M P M G G -"),
         ("माथे सिंदूर सोहे मूसे की सवारी", "S G M G P P P P M P M P M G G -"),
         ("जय गणेश जय गणेश जय गणेश देवा", "S S R R G G G G G G M G M G R R"),
         ("माता जाकी पार्वती पिता महादेवा", ".N .N S .N R R R R G G R S S -")],
  about="गणेश जी की यह आरती हर पूजा की शुरुआत में गाई जाती है। स्थायी (जय गणेश…) सा से ग तक घूमती है और अंतरा (एक दंत…) प तक ऊपर जाता है। केवल शुद्ध सुर हैं, कोई कोमल-तीव्र नहीं — शुरुआत के लिए आसान।"),
 dict(id="aarti-kunj-bihari", bpm=160, slug="aarti-kunj-bihari-ki-harmonium-notes.html", name="आरती कुंजबिहारी की",
  lyric_page="aarti-kunj-bihari-ki.html", kw="Aarti Kunj Bihari Ki",
  lines=[("आरती कुंजबिहारी की", "P - P P M P n n D P - M G R"),
         ("श्री गिरिधर कृष्णमुरारी की", "S R P M M G G S R S .N S -"),
         ("गले में बैजंती माला", "G G G R - R G R S .N S -"),
         ("बजावै मुरली मधुर बाला", "G G - G R - R R G R R S .N S -"),
         ("श्रवण में कुण्डल झलकाला", "G G - G R - R G R R S .N S -"),
         ("नंद के आनंद नंदलाला", "G - G G R - R G R R S .N S -")],
  about="जन्माष्टमी और रोज़ की कृष्ण आरती। पहली पंक्ति में कोमल नि (नि॒) आता है — काली पट्टी, जो ध के ठीक ऊपर है। बाक़ी आरती सा-रे-ग के आसपास और मंद्र नि पर लौटती है।"),
 dict(id="hanuman-chalisa", bpm=170, slug="hanuman-chalisa-harmonium-notes.html", name="हनुमान चालीसा",
  lyric_page="hanuman-chalisa.html", kw="Hanuman Chalisa",
  lines=[("श्रीगुरु चरन सरोज रज", "S - S S S S R R G - R G G"),
         ("निज मनु मुकुरु सुधारि", "P P P M M R R S S - S -"),
         ("जय हनुमान ज्ञान गुन सागर", "S R R P - P P D P M G G R R"),
         ("जय कपीस तिहुँ लोक उजागर", "P - M G R R S .N .N .D R R R S S -")],
  about="चालीसा की हर चौपाई इसी धुन पर चलती है — दो पंक्तियाँ सीख लीं तो पूरी चालीसा बजा सकते हैं। ऊपर दोहा और पहली चौपाई की धुन है; आगे की चौपाइयाँ (राम दूत अतुलित बल धामा…) पहली चौपाई वाली धुन पर ही गाई जाती हैं।"),
 dict(id="raghupati-raghav", bpm=140, slug="raghupati-raghav-raja-ram-harmonium-notes.html", name="रघुपति राघव राजाराम",
  lyric_page="raghupati-raghav-raja-ram.html", kw="Raghupati Raghav Raja Ram",
  lines=[("रघुपति राघव राजा राम", "S S S S S S .N .D .N R S R M G M -"),
         ("पतित पावन सीताराम", "R g R S .N .D .N G R R S -"),
         ("सीताराम सीताराम", "G G G M G R S R M G M -"),
         ("भज प्यारे तू सीताराम", "R R M P d P M G R R -"),
         ("रघुपति राघव राजा राम", "S S S S S S .N .D .N R S R M G M -"),
         ("पतित पावन सीताराम", "R g R S .N .D .N G R R S -")],
  about="गांधी जी की प्रार्थना सभाओं से घर-घर पहुँची यह राम धुन। इसमें कोमल ग (ग॒) और कोमल ध (ध॒) भी आते हैं — दोनों काली पट्टियाँ। शुरुआत में रफ़्तार 60–70% रखें।"),
]

HM_ALANKAR = [
 dict(id="sargam", bpm=100, name="अभ्यास 1: सरगम ऊपर-नीचे (आरोह-अवरोह)",
  lines=[("आरोह — सा से तार सा तक", "S R G M P D N S' -"), ("अवरोह — तार सा से सा तक", "S' N D P M G R S -")]),
 dict(id="alankar-1", bpm=110, name="अभ्यास 2: अलंकार — सारेग, रेगम…",
  lines=[("आरोह", "S R G R G M G M P M P D P D N D N S' -"), ("अवरोह", "S' N D N D P D P M P M G M G R G R S -")]),
 dict(id="alankar-2", bpm=120, name="अभ्यास 3: अलंकार — सासा रेरे गग…",
  lines=[("आरोह", "S S R R G G M M P P D D N N S' S'"), ("अवरोह", "S' S' N N D D P P M M G G R R S S")]),
 dict(id="alankar-3", bpm=110, name="अभ्यास 4: अलंकार — साग, रेम, गप…",
  lines=[("आरोह", "S G R M G P M D P N D S' -"), ("अवरोह", "S' D N P D M P G M R G S -")]),
 dict(id="komal", bpm=90, name="अभ्यास 5: कोमल-तीव्र पहचान (सारे 12 सुर)",
  lines=[("ऊपर", "S r R g G M m P d D n N S' -"), ("नीचे", "S' N n D d P m M G g R r S -")]),
]

_HM_SEMI = dict(S=0, r=1, R=2, g=3, G=4, M=5, m=6, P=7, d=8, D=9, n=10, N=11)
_HM_NAME = ["सा", "रे", "रे", "ग", "ग", "म", "म", "प", "ध", "ध", "नि", "नि"]

def _hm_sargam_html(notation):
    """Static sargam (same look as the player) for the notes table — readable by Google and printable."""
    out = []
    for t in notation.split():
        if t == "-":
            out.append('<i class="hold">–</i>'); continue
        low = len(t) - len(t.lstrip(".")); t = t.lstrip(".")
        high = len(t) - len(t.rstrip("'")); t = t.rstrip("'")
        pc = _HM_SEMI[t]
        cls = (" komal" if pc in (1, 3, 8, 10) else "") + (" tivra" if pc == 6 else "") + (" low" if low else " high" if high else "")
        out.append(f'<span class="sw{cls}">{_HM_NAME[pc]}</span>')
    return " ".join(out)

def _hm_text(notation):
    """Plain-text sargam for descriptions/FAQ: मंद्र = ़ prefix-free words."""
    words = []
    for t in notation.split():
        if t == "-": continue
        low = t.startswith("."); high = t.endswith("'"); t = t.strip(".'")
        pc = _HM_SEMI[t]
        w = _HM_NAME[pc] + ("(को)" if pc in (1, 3, 8, 10) else "(ती)" if pc == 6 else "")
        words.append(("मं." if low else "तार " if high else "") + w)
    return " ".join(words)

def _hm_json(items):
    return json.dumps({"songs": [{"id": s["id"], "title": s["name"], "bpm": s["bpm"], "lines": [{"t": a, "n": b} for a, b in s["lines"]]} for s in items]},
                      ensure_ascii=False)

HMV = ver("harmonium.js")
def _hm_player(items, start=""):
    d = json.loads(_hm_json(items)); d["start"] = start
    blob = json.dumps(d, ensure_ascii=False).replace("</", "<\\/")
    return ('<div class="hm" id="hm"><noscript><p>हारमोनियम चलाने के लिए ब्राउज़र में JavaScript चालू करें।</p></noscript></div>'
            f'<script type="application/json" id="hm-data">{blob}</script>'
            f'<script src="harmonium.js?v={HMV}" defer></script>')

def _hm_table(s):
    rows = "".join(f'<tr><td>{e(a)}</td><td>{_hm_sargam_html(b)}</td></tr>' for a, b in s["lines"])
    return (f'<div class="tbl"><table class="ptable sargam-tbl"><thead><tr><th>बोल</th><th>सरगम (हारमोनियम नोट्स)</th></tr></thead><tbody>{rows}</tbody></table></div>')

_HM_LEGEND = ('<p class="pc-note"><strong>संकेत कैसे पढ़ें:</strong> सुर के नीचे बिंदु = मंद्र सप्तक (नीचे वाला), ऊपर बिंदु = तार सप्तक (ऊपर वाला), '
              'नीचे लकीर = कोमल सुर (काली पट्टी), ऊपर लकीर = तीव्र म, – = पिछला सुर एक मात्रा और खींचें। '
              'नोट्स सबसे प्रचलित धुन के हिसाब से हैं; आपके इलाक़े या मंडली की धुन थोड़ी अलग हो सकती है।</p>')

def _hm_ul(items):
    return '<ul class="library">' + "".join(f'<li><a href="{h}"><strong>{e(t)}</strong><span>{e(s)}</span></a></li>' for h, t, s in items) + "</ul>"

_HM_SONG_LINKS = [(s["slug"], s["name"] + " — हारमोनियम नोट्स", "सरगम + बजाकर सीखें") for s in HM_SONGS]

# ---------- 1. Hub: ऑनलाइन हारमोनियम ----------
_hub_faq = [
 ("ऑनलाइन हारमोनियम कैसे बजाएँ?", "पट्टियों पर उँगली या माउस रखें — जब तक दबाए रखेंगे, सुर बजता रहेगा। कंप्यूटर पर A S D F G H J K बटन सा रे ग म प ध नि सां बजाते हैं और W E T Y U काली पट्टियाँ।"),
 ("क्या यह मोबाइल पर चलता है?", "हाँ। पट्टियाँ छूकर बजाएँ; कीबोर्ड चौड़ा हो तो उसे बाएँ-दाएँ खिसका सकते हैं। फ़ोन साइलेंट मोड में हो तो कुछ फ़ोनों पर आवाज़ नहीं आती — साइलेंट हटाकर देखें।"),
 ("सफ़ेद 1, काली 1 का क्या मतलब है?", "हारमोनियम पर 'सा' किस पट्टी से शुरू करें, उसे सफ़ेद 1 (C), काली 1 (C#), सफ़ेद 2 (D)… कहते हैं। पुरुष आम तौर पर सफ़ेद 1 से काली 2 के बीच और महिलाएँ सफ़ेद 4 से सफ़ेद 5 के बीच गाती हैं। यहाँ 'सा का सुर' बदलने से पूरा कीबोर्ड और सभी गाने उसी सुर में चले जाते हैं।"),
 ("ड्रोन क्या है?", "ड्रोन में नीचे का सा और प लगातार बजता है, जैसे हारमोनियम की धौंकनी चलाते हुए एक पट्टी दबाए रखना। इससे गाते समय सुर पकड़ने में मदद मिलती है।"),
 ("क्या यह मुफ़्त है?", "हाँ, पूरी तरह मुफ़्त। न ऐप डाउनलोड करना है, न साइन-अप।"),
]
add("harmonium.html",
    "ऑनलाइन हारमोनियम — फ़्री में बजाएँ, सरगम और आरती के नोट्स के साथ | OmKiran Bhakti",
    "मोबाइल और कंप्यूटर पर ऑनलाइन हारमोनियम बजाएँ — सा रे ग म लिखी पट्टियाँ, सफ़ेद-काली स्केल बदलें, सा-प ड्रोन, और ॐ जय जगदीश हरे, हनुमान चालीसा जैसी आरतियाँ धुन के साथ बजाकर सीखें। पूरी तरह मुफ़्त।",
    band("ऑनलाइन हारमोनियम — सरगम के साथ बजाएँ",
         "नीचे की पट्टियाँ छूकर बजाएँ। हर पट्टी पर सा रे ग म लिखा है, सुर (सफ़ेद 1, काली 1…) बदल सकते हैं, और किसी आरती को चुनकर उसकी धुन सुन सकते हैं या <b>अभ्यास मोड</b> में ख़ुद बजाना सीख सकते हैं।",
         "ऑनलाइन हारमोनियम") +
    '<section><div class="wrap">' + _hm_player(HM_SONGS) + "</div></section>" +
    '<section class="band"><div class="wrap">' + sec_head("आरतियों के हारमोनियम नोट्स", "हर गाने का अलग पेज — सरगम लिखी हुई, और बजाकर सीखने वाला प्लेयर") +
    _hm_ul(_HM_SONG_LINKS) + "</div></section>" +
    '<section><div class="wrap prose">' + sec_head("नए हैं? यहाँ से शुरू करें") +
    '<p>अगर हारमोनियम पहली बार बजा रहे हैं, तो <a href="harmonium-sikhen.html">हारमोनियम सीखें</a> पेज पर सा पहचानने से लेकर अलंकार तक छोटे-छोटे पाठ हैं — हर पाठ यहीं बजाकर अभ्यास कर सकते हैं।</p>'
    '<h2 class="k-h">इस हारमोनियम में क्या-क्या है</h2><ul>'
    '<li><strong>सरगम लिखी पट्टियाँ:</strong> हर पट्टी पर सा, रे, ग… लिखा है। नीचे बिंदु = मंद्र सप्तक, ऊपर बिंदु = तार सप्तक।</li>'
    '<li><strong>सा का सुर:</strong> सफ़ेद 1 से सफ़ेद 7 तक कोई भी — अपनी आवाज़ के हिसाब से।</li>'
    '<li><strong>सा-प ड्रोन:</strong> गाते समय सुर पकड़ने के लिए।</li>'
    '<li><strong>धुन प्लेयर:</strong> चमकती पट्टी देखकर साथ-साथ बजाएँ; रफ़्तार कम करें; एक पंक्ति को बार-बार दोहराएँ।</li>'
    '<li><strong>अभ्यास मोड:</strong> गाना तभी आगे बढ़ता है जब आप सही पट्टी दबाते हैं — जैसे गुरु जी साथ बैठे हों।</li></ul></div></section>' +
    faq_html(_hub_faq),
    crumbs="ऑनलाइन हारमोनियम",
    ld=[{"@type": "WebApplication", "name": "OmKiran Bhakti ऑनलाइन हारमोनियम", "applicationCategory": "MusicApplication",
         "operatingSystem": "Any (browser)", "inLanguage": "hi", "isAccessibleForFree": True,
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "INR"}, "url": SITE + "harmonium.html"}, faq_ld(_hub_faq)],
    active="harmonium.html")

# ---------- 2. हारमोनियम सीखें (lessons) ----------
_learn_faq = [
 ("हारमोनियम सीखने में कितना समय लगता है?", "रोज़ 20–30 मिनट अभ्यास करें तो 2–3 हफ़्ते में सरल आरती (ॐ जय जगदीश हरे, जय गणेश देवा) बजने लगती है। अलंकार रोज़ करने से उँगलियाँ जल्दी सधती हैं।"),
 ("हारमोनियम में सा कहाँ होता है?", "सा कोई तय पट्टी नहीं है — आप जिस पट्टी को सा मानें, बाक़ी सुर उसी से गिने जाते हैं। शुरुआत में सफ़ेद 1 (C) को सा मानना सबसे आसान है, क्योंकि तब सातों शुद्ध सुर सफ़ेद पट्टियों पर ही आते हैं।"),
 ("कोमल और तीव्र सुर क्या होते हैं?", "रे, ग, ध, नि के आधा सुर नीचे वाले रूप को कोमल कहते हैं (काली पट्टी), और म के आधा सुर ऊपर वाले रूप को तीव्र म कहते हैं। सा और प कभी नहीं बदलते — इन्हें अचल सुर कहते हैं।"),
 ("उँगलियाँ कैसे रखें?", "दाएँ हाथ से पट्टियाँ और बाएँ हाथ से धौंकनी। शुरुआत में सा-रे-ग पर तर्जनी, मध्यमा, अनामिका रखें; म के लिए अंगूठा नीचे से निकालें या हाथ थोड़ा खिसकाएँ। जल्दी के चक्कर में एक ही उँगली से न बजाएँ।"),
]
_steps = lambda xs: '<ol class="steps">' + "".join(f"<li>{x}</li>" for x in xs) + "</ol>"
add("harmonium-sikhen.html",
    "हारमोनियम कैसे बजाएँ — शुरुआत से आसान पाठ, सरगम और अलंकार (ऑनलाइन अभ्यास) | OmKiran Bhakti",
    "हारमोनियम सीखना शुरू करें: पट्टियों की पहचान, सा कहाँ है, सप्तक, कोमल-तीव्र सुर, उँगलियाँ, धौंकनी, और 5 अलंकार — सब कुछ यहीं ऑनलाइन हारमोनियम पर बजाकर अभ्यास करें। फिर आरती के नोट्स से पहला गाना।",
    band("हारमोनियम कैसे बजाएँ — शुरुआत से",
         "हारमोनियम सीखने का क्रम है: पहले पट्टियों में सा पहचानें, फिर सातों सुर (सा रे ग म प ध नि) ऊपर-नीचे बजाएँ, फिर अलंकार से उँगलियाँ साधें, और आख़िर में एक आसान आरती। नीचे हर पाठ के साथ अभ्यास का प्लेयर है।",
         "हारमोनियम सीखें") +
    '<article><section><div class="wrap prose katha">' +
    '<h2 class="k-h">पाठ 1: हारमोनियम को जानें</h2>'
    '<p>हारमोनियम में दो हिस्से हैं — आगे पट्टियाँ (सफ़ेद और काली) और पीछे धौंकनी। बाएँ हाथ से धौंकनी चलाते हैं, जिससे हवा भरती है, और दाएँ हाथ से पट्टियाँ दबाते हैं। ऊपर लगे बटन (स्टॉप) खोलने पर आवाज़ निकलती है; पहले \"ड्रोन\" स्टॉप खोल लें तो सा लगातार गूँजता है।</p>'
    '<p>धौंकनी हल्के, बराबर दबाव से चलाएँ — झटके से नहीं। आवाज़ एक-सी रहनी चाहिए, लहर जैसी नहीं।</p>'
    '<h2 class="k-h">पाठ 2: सा कहाँ है — सफ़ेद 1, काली 1</h2>'
    '<p>पट्टियों में दो और तीन काली पट्टियों के गुच्छे बार-बार आते हैं। <strong>दो काली पट्टियों वाले गुच्छे के ठीक बाएँ की सफ़ेद पट्टी</strong> को सफ़ेद 1 (C) कहते हैं। शुरुआत में इसी को सा मानें — तब सा रे ग म प ध नि सातों सफ़ेद पट्टियों पर आते हैं।</p>'
    '<p>गाते समय अपनी आवाज़ के हिसाब से सा बदला जाता है (काली 1, सफ़ेद 2…)। नीचे प्लेयर में \"सा का सुर\" बदलकर देखें — सा वाली पट्टी पीली दिखती है।</p>'
    '<h2 class="k-h">पाठ 3: सात सुर और तीन सप्तक</h2>'
    '<p>सात सुर हैं: <strong>सा, रे, ग, म, प, ध, नि</strong>। नि के बाद फिर सा आता है, पर ऊँचा — उसे तार सा कहते हैं। सा से नीचे वाले सुर मंद्र सप्तक कहलाते हैं (लिखते समय नीचे बिंदु), बीच वाले मध्य सप्तक और ऊपर वाले तार सप्तक (ऊपर बिंदु)।</p>' +
    _steps(["प्लेयर में \"अभ्यास 1: सरगम ऊपर-नीचे\" चुनें।", "▶ बजाएँ दबाकर एक बार सुनें, चमकती पट्टियाँ देखें।",
            "अब ✋ अभ्यास मोड दबाएँ और ख़ुद बजाएँ — सही पट्टी दबाने पर ही आगे बढ़ेगा।", "साथ-साथ \"सा रे ग म…\" गाते भी जाएँ, इससे कान और गला दोनों सधते हैं।"]) +
    '<h2 class="k-h">पाठ 4: कोमल और तीव्र सुर</h2>'
    '<p>रे, ग, ध, नि के कोमल रूप (आधा सुर नीचे) काली पट्टियों पर होते हैं — लिखते समय नीचे लकीर: रे॒ ग॒ ध॒ नि॒। म का तीव्र रूप (आधा सुर ऊपर) भी काली पट्टी पर है — ऊपर लकीर। सा और प कभी कोमल-तीव्र नहीं होते। \"अभ्यास 5\" में सारे 12 सुर एक के बाद एक बजते हैं।</p>'
    '<h2 class="k-h">पाठ 5: उँगलियाँ और अलंकार</h2>'
    '<p>अलंकार सुरों के छोटे-छोटे पैटर्न हैं — जैसे व्यायाम। रोज़ 10 मिनट अलंकार करने से उँगलियाँ अपने-आप सही पट्टी पर जाने लगती हैं। पहले धीमी रफ़्तार (50–60%) पर बजाएँ, बिना गलती बजने लगे तब रफ़्तार बढ़ाएँ।</p>' +
    _steps(["दाएँ हाथ की तर्जनी सा पर, मध्यमा रे पर, अनामिका ग पर रखें।", "म के लिए अंगूठा तर्जनी के नीचे से निकालकर रखें, फिर तर्जनी प पर — इसी तरह आगे बढ़ें।",
            "हर अलंकार पहले आरोह (ऊपर), फिर अवरोह (नीचे)।", "\"चुनी पंक्ति दोहराएँ\" लगाकर एक ही पंक्ति कई बार बजाएँ।"]) +
    "</div></section>"
    '<section><div class="wrap">' + sec_head("अभ्यास का हारमोनियम", "ऊपर गाना/अभ्यास चुनें — अलंकार और आरतियाँ दोनों यहीं हैं") +
    _hm_player(HM_ALANKAR + HM_SONGS, "sargam") + "</div></section>"
    '<section class="band"><div class="wrap">' + sec_head("पाठ 6: पहला गाना", "सबसे आसान से शुरू करें — ॐ जय जगदीश हरे, फिर जय गणेश देवा") +
    _hm_ul(_HM_SONG_LINKS) + "</div></section></article>" +
    faq_html(_learn_faq),
    crumbs="हारमोनियम सीखें",
    ld=[{"@type": "HowTo", "name": "हारमोनियम कैसे बजाएँ — शुरुआत से", "inLanguage": "hi",
         "step": [{"@type": "HowToStep", "name": n} for n in ["हारमोनियम को जानें", "सा पहचानें", "सात सुर और सप्तक", "कोमल-तीव्र सुर", "उँगलियाँ और अलंकार", "पहला गाना"]]},
        faq_ld(_learn_faq)],
    active="harmonium-sikhen.html")

# ---------- 3. Song notes pages ----------
for _s in HM_SONGS:
    _first = _s["lines"][0]
    _faq = [
     (f"{_s['name']} के हारमोनियम नोट्स क्या हैं?",
      f"पहली पंक्ति \"{_first[0]}\" के सुर हैं: {_hm_text(_first[1])}। पूरी आरती के सरगम ऊपर की तालिका में हैं, और प्लेयर में बजाकर सुन सकते हैं।"),
     (f"{_s['name']} किस सुर (स्केल) में बजाएँ?",
      "नोट्स सा के हिसाब से लिखे हैं, इसलिए किसी भी स्केल में बजा सकते हैं। सीखते समय सफ़ेद 1 (C) सबसे आसान है; गाते समय अपनी आवाज़ के हिसाब से 'सा का सुर' बदल लें — पूरी धुन अपने-आप उसी सुर में चली जाएगी।"),
     ("धुन मेरी मंडली वाली से थोड़ी अलग क्यों लग रही है?",
      "पारंपरिक आरतियों की धुन इलाक़े और परिवार के हिसाब से थोड़ी बदलती है। यहाँ सबसे प्रचलित धुन दी है। आप किसी पंक्ति को अलग तरह गाते हैं तो हमें WhatsApp चैनल पर बताएँ।"),
    ]
    _rel = [(x["slug"], x["name"] + " — नोट्स", "हारमोनियम") for x in HM_SONGS if x["id"] != _s["id"]][:3]
    _rel = [(_s["lyric_page"], _s["name"] + " — पूरे बोल", "अर्थ सहित")] + _rel + [("harmonium-sikhen.html", "हारमोनियम सीखें", "शुरुआत से पाठ")]
    add(_s["slug"],
        f"{_s['name']} हारमोनियम नोट्स (सरगम) — बजाकर सीखें | {_s['kw']} Harmonium Notes",
        f"{_s['name']} के हारमोनियम नोट्स सरगम में — हर पंक्ति के सुर, आसान संकेत, और ऑनलाइन हारमोनियम पर धुन सुनकर व अभ्यास मोड में ख़ुद बजाकर सीखें। {_s['kw']} harmonium notes in Hindi.",
        band(f"{_s['name']} — हारमोनियम नोट्स (सरगम)",
             f"{_s['name']} की पहली पंक्ति \"{e(_first[0])}\" के सुर हैं: <b>{e(_hm_text(_first[1]))}</b>। पूरी धुन नीचे सरगम में लिखी है — प्लेयर में ▶ दबाकर सुनें, या ✋ अभ्यास मोड में ख़ुद बजाएँ।",
             _s["name"] + " नोट्स") +
        '<section><div class="wrap">' + _hm_player(HM_SONGS, _s["id"]) + "</div></section>" +
        '<article><section><div class="wrap prose katha">' +
        f'<h2 class="k-h">{e(_s["name"])} — सरगम नोट्स</h2>' + _hm_table(_s) + _HM_LEGEND +
        f'<h2 class="k-h">धुन के बारे में</h2><p>{e(_s["about"])}</p>' +
        '<h2 class="k-h">कैसे सीखें</h2>' +
        _steps(["▶ बजाएँ से पूरी धुन असली रफ़्तार पर एक-दो बार सुनें।",
                "रफ़्तार 60–70% पर लाएँ, किसी एक पंक्ति पर टैप करें, \"चुनी पंक्ति दोहराएँ\" लगाएँ और ✋ अभ्यास मोड में बजाएँ।",
                "एक पंक्ति बिना रुके बजने लगे, तब अगली पंक्ति पर जाएँ।",
                "आख़िर में रफ़्तार धीरे-धीरे 100% तक लाएँ और पूरी आरती गाते हुए बजाएँ।"]) +
        f'<p>पूरी आरती के बोल और अर्थ: <a href="{_s["lyric_page"]}">{e(_s["name"])}</a>।</p>' +
        "</div></section></article>" +
        '<section class="no-print"><div class="wrap">' + sec_head("साथ में देखें") + _hm_ul(_rel) + "</div></section>" +
        faq_html(_faq),
        crumbs=_s["name"] + " नोट्स",
        ld=[{"@type": "MusicComposition", "name": _s["name"], "inLanguage": "hi", "description": "हारमोनियम सरगम नोट्स"},
            {"@type": "HowTo", "name": f"{_s['name']} हारमोनियम पर कैसे बजाएँ", "inLanguage": "hi",
             "step": [{"@type": "HowToStep", "name": a, "text": _hm_text(b)} for a, b in _s["lines"]]},
            faq_ld(_faq)],
        active="harmonium.html")

# ---------- 4. Link the existing lyrics pages to their notes ----------
for _s in HM_SONGS:
    _p = PAGES.get(_s["lyric_page"])
    if not _p or "harmonium-notes" in _p: continue
    _strip = (f'<section class="no-print"><div class="wrap"><p class="pc-note">🎹 <strong>हारमोनियम पर बजाना सीखें:</strong> '
              f'<a href="{_s["slug"]}">{e(_s["name"])} के हारमोनियम नोट्स (सरगम)</a> — '
              f'<a href="harmonium.html">ऑनलाइन हारमोनियम</a> पर बजाकर अभ्यास करें।</p></div></section>')
    _i = _p.find('<section class="faq">')
    if _i < 0: _i = _p.find("</main>")
    if _i > 0: PAGES[_s["lyric_page"]] = _p[:_i] + _strip + _p[_i:]

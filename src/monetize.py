# Monetisation switches. Both stay OFF (nothing is shown) until the IDs are filled in.
AMAZON_TAG = "omkiranbhakti-21"      # Amazon Associates India store ID, e.g. "omkiran-21"
ADSENSE_PUB = "ca-pub-2329005702942940"     # AdSense publisher ID, e.g. "ca-pub-1234567890123456"

# Puja items per deity: (label shown in Hindi, Amazon.in search words). Links are plain Amazon searches with our tag —
# no prices are shown (Amazon rule), and every box carries an affiliate disclosure.
COMMON = [("पीतल का दीया", "brass diya for puja"), ("कपूर", "pure camphor for puja"), ("अगरबत्ती और धूप", "agarbatti dhoop sticks"), ("पूजा थाली सेट", "puja thali set")]
ITEMS = {
 "hanuman": [("हनुमान जी का चोला (सिंदूर)", "hanuman ji chola sindoor"), ("हनुमान चालीसा (गीता प्रेस)", "hanuman chalisa gita press"), ("लाल पूजा वस्त्र", "red puja cloth")],
 "shiv":    [("रुद्राक्ष माला", "rudraksha mala 108"), ("पीतल का शिवलिंग", "brass shivling for home"), ("भस्म / विभूति", "vibhuti bhasma")],
 "devi":    [("माता की चुनरी", "mata ki chunri"), ("रोली-कुमकुम", "roli kumkum for puja"), ("दुर्गा सप्तशती (गीता प्रेस)", "durga saptashati gita press")],
 "lakshmi": [("कमल गट्टा माला", "kamal gatta mala"), ("श्री यंत्र", "shri yantra"), ("लक्ष्मी-गणेश मूर्ति", "lakshmi ganesh murti")],
 "ganesh":  [("गणेश मूर्ति", "ganesh murti for home"), ("दूर्वा / पूजा फूल माला", "artificial flower garland for puja"), ("मोदक साँचा", "modak mould")],
 "krishna": [("लड्डू गोपाल पोशाक", "laddu gopal dress"), ("तुलसी माला", "tulsi mala"), ("बाँसुरी (पूजा सज्जा)", "bansuri for laddu gopal")],
 "vishnu":  [("तुलसी माला", "tulsi mala"), ("रामचरितमानस (गीता प्रेस)", "ramcharitmanas gita press"), ("पीला पूजा वस्त्र", "yellow puja cloth")],
 "shani":   [("तिल के तेल का दीया", "til oil for diya"), ("शनि यंत्र", "shani yantra"), ("काले तिल", "black til for puja")],
 "surya":   [("ताँबे का लोटा (अर्घ्य)", "copper lota for surya arghya"), ("लाल चंदन", "lal chandan"), ("सूर्य यंत्र", "surya yantra")],
}
KEYS = [("hanuman","hanuman"),("bajrang","hanuman"),("sankatmochan","hanuman"),("shiv","shiv"),("rudra","shiv"),("linga","shiv"),("mahamrityunjay","shiv"),
        ("jyotirlinga","shiv"),("bhairav","shiv"),("lakshmi","lakshmi"),("shri-suktam","lakshmi"),("ganesh","ganesh"),("ganpati","ganesh"),("sukhkarta","ganesh"),
        ("krishna","krishna"),("kunj","krishna"),("radha","krishna"),("madhurashtakam","krishna"),("damodar","krishna"),("govardhan","krishna"),("khatu","krishna"),
        ("ram","vishnu"),("vishnu","vishnu"),("jagdish","vishnu"),("hari","vishnu"),("satyanarayan","vishnu"),("dashavatar","vishnu"),("ekadashi","vishnu"),
        ("shani","shani"),("surya","surya"),("aditya","surya"),
        ("durga","devi"),("ambe","devi"),("kali","devi"),("mata","devi"),("devi","devi"),("bhavani","devi"),("argala","devi"),("mahishasura","devi"),
        ("saraswati","devi"),("parvati","devi"),("santoshi","devi"),("vindhy","devi"),("gayatri","devi"),("ganga","devi"),("annapurna","devi"),("ahoi","devi"),("kuber","lakshmi"),("diwali","lakshmi"),("yam-deepdaan","lakshmi"),("dhanvantari","vishnu"),("narak","krishna")]

def deity(slug):
    for k, d in KEYS:
        if k in slug: return d
    return None

def samagri_box(slug, esc):
    if not AMAZON_TAG: return ""
    from urllib.parse import quote_plus
    d = deity(slug)
    items = (ITEMS.get(d, []) + COMMON)[:6]
    lis = "".join(f'<li><a href="https://www.amazon.in/s?k={quote_plus(q)}&amp;tag={AMAZON_TAG}" target="_blank" rel="sponsored noopener">{esc(n)}</a></li>' for n, q in items)
    return (f'<aside class="samagri-box no-print" aria-label="इस पूजा की सामग्री"><h2>इस पूजा की सामग्री</h2><ul>{lis}</ul>'
            f'<p class="aff-note">ये Amazon के affiliate links हैं — इनसे ख़रीदारी पर OmKiran Bhakti को छोटा-सा कमीशन मिलता है, आपके लिए दाम वही रहता है।</p></aside>')

GA_ID = ""  # Google Analytics 4 measurement ID (G-XXXXXXX); empty = off

def ga_head():
    if not GA_ID: return ""
    return (f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>'
            f"<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{GA_ID}');</script>")

def adsense_head():
    if not ADSENSE_PUB: return ga_head()
    return ga_head() + f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_PUB}" crossorigin="anonymous"></script>'

def ads_txt():
    return f"google.com, {ADSENSE_PUB.replace('ca-', '')}, DIRECT, f08c47fec0942fa0\n" if ADSENSE_PUB else ""

# ---- Festival pages: (slug keyword, heading, items)
FEST = [
 ("diwali", "दिवाली लक्ष्मी पूजा की सामग्री", [("लक्ष्मी-गणेश मूर्ति", "lakshmi ganesh murti diwali"), ("मिट्टी के दीये", "clay diya for diwali"), ("खील-बताशे / पूजा प्रसाद", "kheel batasha diwali puja"), ("कलश और नारियल", "brass kalash for puja"), ("रंगोली रंग", "rangoli colours"), ("दिवाली तोरण / बंदनवार", "diwali toran door hanging"), ("श्री यंत्र", "shri yantra"), ("कमल गट्टा", "kamal gatta")]),
 ("dhanteras", "धनतेरस की ख़रीदारी और पूजा", [("पीतल / चाँदी के बर्तन", "brass utensils for dhanteras"), ("धन्वंतरि-कुबेर मूर्ति", "kuber murti"), ("मिट्टी के दीये", "clay diya for diwali"), ("झाड़ू (शुभ)", "broom for home"), ("श्री यंत्र", "shri yantra"), ("कुबेर यंत्र", "kuber yantra")]),
 ("narak-chaturdashi", "रूप चौदस की सामग्री", [("मिट्टी के दीये", "clay diya for diwali"), ("उबटन", "ubtan for bath"), ("तिल का तेल", "til oil")]),
 ("govardhan", "गोवर्धन पूजा की सामग्री", [("लड्डू गोपाल / कृष्ण मूर्ति", "laddu gopal murti"), ("मिट्टी के दीये", "clay diya for diwali"), ("पूजा थाली सेट", "puja thali set")]),
 ("bhai-dooj", "भाई दूज की सामग्री", [("रोली-चावल तिलक सेट", "roli chawal tilak set"), ("पूजा थाली सेट", "puja thali set"), ("नारियल गोला", "dry coconut gola")]),
 ("chhath", "छठ पूजा की सामग्री", [("बाँस का सूप", "bamboo soop for chhath"), ("बाँस की टोकरी (दउरा)", "bamboo basket for chhath"), ("पीतल का लोटा (अर्घ्य)", "brass lota for arghya"), ("ठेकुआ साँचा", "thekua mould"), ("पीला-लाल सिंदूर", "chhath sindoor"), ("मिट्टी के दीये", "clay diya")]),
 ("karwa-chauth", "करवा चौथ की सामग्री", [("करवा चौथ थाली सेट", "karwa chauth thali set"), ("मिट्टी का करवा", "karwa chauth karwa"), ("छलनी", "karwa chauth channi"), ("सुहाग / श्रृंगार सामग्री", "suhag shringar kit"), ("करवा चौथ व्रत कथा पुस्तक", "karwa chauth vrat katha book")]),
 ("ahoi", "अहोई अष्टमी की सामग्री", [("अहोई माता कैलेंडर / चित्र", "ahoi mata photo"), ("करवा", "karwa chauth karwa"), ("पूजा थाली सेट", "puja thali set")]),
 ("navratri", "नवरात्रि कलश स्थापना की सामग्री", [("कलश (पीतल)", "brass kalash for puja"), ("जौ बोने का मिट्टी का पात्र", "clay pot for jau navratri"), ("माता की चुनरी", "mata ki chunri"), ("दुर्गा सप्तशती (गीता प्रेस)", "durga saptashati gita press"), ("अखंड ज्योत दीया", "akhand jyot diya brass"), ("दुर्गा माँ की मूर्ति", "durga maa murti")]),
 ("durga", "दुर्गा पूजा की सामग्री", [("माता की चुनरी", "mata ki chunri"), ("दुर्गा सप्तशती (गीता प्रेस)", "durga saptashati gita press"), ("अखंड ज्योत दीया", "akhand jyot diya brass")]),
 ("dussehra", "दशहरा पूजा की सामग्री", [("शस्त्र पूजा थाली", "puja thali set"), ("रामचरितमानस (गीता प्रेस)", "ramcharitmanas gita press"), ("राम दरबार मूर्ति", "ram darbar murti")]),
 ("tulsi", "तुलसी विवाह की सामग्री", [("तुलसी का गमला", "tulsi plant pot"), ("शालिग्राम", "shaligram"), ("लाल चुनरी", "mata ki chunri"), ("पूजा थाली सेट", "puja thali set")]),
 ("janmashtami", "जन्माष्टमी की सामग्री", [("लड्डू गोपाल मूर्ति", "laddu gopal murti"), ("लड्डू गोपाल पोशाक", "laddu gopal dress"), ("झूला / पालना", "laddu gopal jhula"), ("बाँसुरी और मोर-मुकुट", "laddu gopal mukut bansuri")]),
 ("ganesh-chaturthi", "गणेश चतुर्थी की सामग्री", [("गणेश मूर्ति (इको-फ्रेंडली)", "eco friendly ganesh murti"), ("गणेश चौकी / आसन", "ganesh chowki"), ("मोदक साँचा", "modak mould"), ("दूर्वा माला / फूल माला", "artificial flower garland for puja")]),
 ("shivratri", "महाशिवरात्रि की सामग्री", [("पीतल का शिवलिंग", "brass shivling for home"), ("रुद्राक्ष माला", "rudraksha mala 108"), ("ताँबे का लोटा (जलाभिषेक)", "copper lota"), ("भस्म / विभूति", "vibhuti bhasma")]),
 ("sawan", "सावन पूजा की सामग्री", [("पीतल का शिवलिंग", "brass shivling for home"), ("रुद्राक्ष माला", "rudraksha mala 108"), ("ताँबे का लोटा (जलाभिषेक)", "copper lota")]),
 ("holi", "होली की ख़रीदारी", [("हर्बल गुलाल", "herbal gulal"), ("पिचकारी", "pichkari"), ("होलिका पूजा थाली", "puja thali set")]),
 ("raksha-bandhan", "रक्षाबंधन की सामग्री", [("राखी (भाई के लिए)", "rakhi for brother"), ("रक्षाबंधन थाली", "rakhi thali set"), ("रोली-चावल तिलक", "roli chawal tilak set")]),
 ("ekadashi", "एकादशी व्रत-पूजा की सामग्री", [("तुलसी माला", "tulsi mala"), ("विष्णु सहस्रनाम (गीता प्रेस)", "vishnu sahasranamam gita press"), ("पीला पूजा वस्त्र", "yellow puja cloth")]),
 ("satyanarayan", "सत्यनारायण पूजा की सामग्री", [("सत्यनारायण कथा पुस्तक", "satyanarayan katha book"), ("केले के पत्ते / चौकी", "puja chowki"), ("पंचामृत पात्र", "panchamrit bowl brass")]),
 ("ram-navami", "राम नवमी की सामग्री", [("राम दरबार मूर्ति", "ram darbar murti"), ("रामचरितमानस (गीता प्रेस)", "ramcharitmanas gita press")]),
 ("hanuman-jayanti", "हनुमान जयंती की सामग्री", [("हनुमान जी का चोला (सिंदूर)", "hanuman ji chola sindoor"), ("सुंदरकांड (गीता प्रेस)", "sundarkand gita press")]),
 ("vasant-panchami", "वसंत पंचमी की सामग्री", [("सरस्वती माँ की मूर्ति", "saraswati murti"), ("पीला पूजा वस्त्र", "yellow puja cloth")]),
 ("makar-sankranti", "मकर संक्रांति की सामग्री", [("तिल-गुड़", "til gud"), ("पतंग और माँझा", "kite and manjha"), ("ताँबे का लोटा (अर्घ्य)", "copper lota for surya arghya")]),
 ("pitru", "श्राद्ध / तर्पण की सामग्री", [("ताँबे का लोटा", "copper lota"), ("काले तिल", "black til for puja"), ("कुशा आसन", "kusha asan")]),
 ("sharad-purnima", "शरद पूर्णिमा की सामग्री", [("चाँदी / पीतल की कटोरी (खीर के लिए)", "brass bowl for kheer"), ("लक्ष्मी-गणेश मूर्ति", "lakshmi ganesh murti")]),
 ("teej", "तीज की सामग्री", [("सुहाग / श्रृंगार सामग्री", "suhag shringar kit"), ("मेहंदी", "natural mehndi cone"), ("शिव-पार्वती मूर्ति", "shiv parvati murti")]),
 ("vat-", "वट सावित्री की सामग्री", [("कच्चा सूत / कलावा", "kalawa mauli"), ("सुहाग / श्रृंगार सामग्री", "suhag shringar kit"), ("बाँस का पंखा", "bamboo hand fan")]),
]

def _link(n, q):
    from urllib.parse import quote_plus
    return f'<li><a href="https://www.amazon.in/s?k={quote_plus(q)}&amp;tag={AMAZON_TAG}" target="_blank" rel="sponsored noopener">{n}</a></li>'

NOTE = '<p class="aff-note">ये Amazon के affiliate links हैं — इनसे ख़रीदारी पर OmKiran Bhakti को छोटा-सा कमीशन मिलता है, आपके लिए दाम वही रहता है।</p>'

def festival_box(slug):
    if not AMAZON_TAG: return ""
    for k, head, items in FEST:
        if k in slug:
            lis = "".join(_link(n, q) for n, q in (items + [x for x in COMMON if x not in items])[:8])
            return (f'<section class="no-print"><div class="wrap"><aside class="samagri-box fest" aria-label="{head}"><h2>{head}</h2><ul>{lis}</ul>'
                    f'<p><a href="puja-samagri-kharidein.html">सभी पूजा सामग्री, मूर्तियाँ और किताबें →</a></p>{NOTE}</aside></div></section>')
    return ""

SHOP = [
 ("मूर्तियाँ", [("गणेश मूर्ति", "ganesh murti for home"), ("लक्ष्मी-गणेश मूर्ति", "lakshmi ganesh murti"), ("पीतल का शिवलिंग", "brass shivling for home"), ("लड्डू गोपाल", "laddu gopal murti"), ("हनुमान मूर्ति", "hanuman murti"), ("दुर्गा माँ की मूर्ति", "durga maa murti"), ("राम दरबार", "ram darbar murti"), ("सरस्वती माँ", "saraswati murti")]),
 ("पूजा का सामान", [("पूजा थाली सेट", "puja thali set"), ("पीतल का दीया", "brass diya for puja"), ("अखंड ज्योत दीया", "akhand jyot diya brass"), ("कलश", "brass kalash for puja"), ("पूजा की घंटी", "puja bell brass"), ("पूजा चौकी", "puja chowki"), ("आसन", "puja asan"), ("कपूर", "pure camphor for puja"), ("अगरबत्ती और धूप", "agarbatti dhoop sticks"), ("रोली-कुमकुम", "roli kumkum for puja"), ("कलावा", "kalawa mauli")]),
 ("माला और यंत्र", [("रुद्राक्ष माला", "rudraksha mala 108"), ("तुलसी माला", "tulsi mala"), ("कमल गट्टा माला", "kamal gatta mala"), ("स्फटिक माला", "sphatik mala"), ("श्री यंत्र", "shri yantra"), ("कुबेर यंत्र", "kuber yantra")]),
 ("धार्मिक पुस्तकें (गीता प्रेस)", [("श्रीमद्भगवद्गीता", "bhagavad gita gita press hindi"), ("रामचरितमानस", "ramcharitmanas gita press"), ("सुंदरकांड", "sundarkand gita press"), ("दुर्गा सप्तशती", "durga saptashati gita press"), ("हनुमान चालीसा", "hanuman chalisa gita press"), ("व्रत कथा संग्रह", "vrat katha sangrah gita press"), ("नित्य कर्म पूजा प्रकाश", "nitya karm puja prakash gita press")]),
 ("घर का मंदिर", [("लकड़ी का मंदिर", "wooden mandir for home"), ("मंदिर की लाइट / दीपमाला", "mandir light"), ("भगवान की पोशाक", "god dress for murti"), ("पूजा के फूल-माला (कृत्रिम)", "artificial flower garland for puja")]),
]

ICON = {"लक्ष्मी":"🪷","गणेश":"🐘","शिवलिंग":"🔱","लड्डू":"🦚","हनुमान":"🚩","दुर्गा":"🦁","राम दरबार":"🏹","सरस्वती":"🎶",
 "थाली":"🍽️","दीया":"🪔","कलश":"🏺","घंटी":"🔔","चौकी":"🪑","आसन":"🧘","कपूर":"🔥","अगरबत्ती":"🌫️","रोली":"🔴","कलावा":"🧶",
 "रुद्राक्ष":"📿","तुलसी":"🌿","कमल":"🪷","स्फटिक":"💎","श्री यंत्र":"🔺","कुबेर":"💰",
 "गीता":"📖","रामचरितमानस":"📕","सुंदरकांड":"📗","सप्तशती":"📘","चालीसा":"📙","व्रत कथा":"📚","नित्य":"📜",
 "मंदिर":"🛕","लाइट":"✨","पोशाक":"👘","फूल":"🌼"}
CAT = {"मूर्तियाँ":("🕉️","घर के मंदिर के लिए सुंदर मूर्तियाँ"),"पूजा का सामान":("🪔","रोज़ की पूजा का ज़रूरी सामान"),
       "माला और यंत्र":("📿","जाप के लिए माला, सिद्ध यंत्र"),"धार्मिक पुस्तकें (गीता प्रेस)":("📚","गीता प्रेस की असली किताबें"),
       "घर का मंदिर":("🛕","मंदिर, रोशनी और सजावट")}

def _ico(n):
    return next((v for k, v in ICON.items() if k in n), "🙏")

def _url(q):
    from urllib.parse import quote_plus
    return f"https://www.amazon.in/s?k={quote_plus(q)}&amp;tag={AMAZON_TAG}"

def _card(n, q):
    return (f'<li><a href="{_url(q)}" target="_blank" rel="sponsored noopener"><span class="pc-ico" aria-hidden="true">{_ico(n)}</span>'
            f'<span class="pc-nm">{n}</span><span class="pc-cta">Amazon पर देखें</span></a></li>')

def shop_body():
    nav = '<nav class="shop-nav" aria-label="श्रेणियाँ">' + "".join(f'<a href="#c{i}">{CAT[t][0]} {t.split(" (")[0]}</a>' for i, (t, _) in enumerate(SHOP)) + '</nav>'
    secs = "".join(f'<section id="c{i}" class="shop-sec{" alt" if i % 2 else ""}"><div class="wrap"><div class="shop-head"><span class="sh-ico" aria-hidden="true">{CAT[t][0]}</span>'
                   f'<div><h2>{t}</h2><p>{CAT[t][1]}</p></div></div><ul class="pc-grid">{"".join(_card(n, q) for n, q in items)}</ul></div></section>'
                   for i, (t, items) in enumerate(SHOP))
    fest = "".join(f'<li><a href="{s}"><span class="fc-ico" aria-hidden="true">{ic}</span><strong>{h}</strong><span class="fc-go">लिस्ट देखें →</span></a></li>' for s, h, ic in [
        ("diwali-puja-samagri-list.html","दिवाली पूजा सामग्री","🪔"),("chhath-puja-samagri-list.html","छठ पूजा सामग्री","🌅"),
        ("karwa-chauth-puja-samagri-list.html","करवा चौथ सामग्री","🌕"),("navratri-kalash-sthapana-samagri-list.html","नवरात्रि कलश स्थापना","🏺"),
        ("puja-samagri.html","सभी लिस्ट (प्रिंट करें)","🖨️")])
    return (f'<section class="shop-sec"><div class="wrap">{nav}</div></section>' + secs +
            f'<section class="shop-sec"><div class="wrap"><div class="shop-head"><span class="sh-ico" aria-hidden="true">🎉</span><div><h2>त्योहार के हिसाब से लिस्ट</h2><p>बाज़ार जाने से पहले पूरी लिस्ट देख लें</p></div></div><ul class="fest-cards">{fest}</ul>{NOTE}</div></section>')

def shop_teaser():
    pick = [("गणेश मूर्ति","ganesh murti for home"),("पूजा थाली सेट","puja thali set"),("पीतल का दीया","brass diya for puja"),("कलश","brass kalash for puja"),
            ("रुद्राक्ष माला","rudraksha mala 108"),("श्री यंत्र","shri yantra"),("श्रीमद्भगवद्गीता","bhagavad gita gita press hindi"),("लकड़ी का मंदिर","wooden mandir for home")]
    return (f'<section class="shop-sec alt no-print"><div class="wrap"><div class="shop-head"><span class="sh-ico" aria-hidden="true">🛍️</span><div><h2>घर बैठे मँगाएँ</h2>'
            f'<p>पूजा का सामान, मूर्तियाँ, माला और गीता प्रेस की किताबें — Amazon पर</p></div></div><ul class="pc-grid">{"".join(_card(n, q) for n, q in pick)}</ul>'
            f'<p class="shop-more"><a class="btn" href="puja-samagri-kharidein.html">पूरी पूजा सामग्री देखें →</a></p>{NOTE}</div></section>')

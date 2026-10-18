# Monetisation switches. Both stay OFF (nothing is shown) until the IDs are filled in.
AMAZON_TAG = ""      # Amazon Associates India store ID, e.g. "omkiran-21"
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
        ("saraswati","devi"),("parvati","devi"),("santoshi","devi"),("vindhy","devi"),("gayatri","devi"),("ganga","devi"),("annapurna","devi"),("ahoi","devi")]

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

def adsense_head():
    if not ADSENSE_PUB: return ""
    return f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_PUB}" crossorigin="anonymous"></script>'

def ads_txt():
    return f"google.com, {ADSENSE_PUB.replace('ca-', '')}, DIRECT, f08c47fec0942fa0\n" if ADSENSE_PUB else ""

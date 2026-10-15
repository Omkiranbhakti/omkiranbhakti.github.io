# Monthly vrat lists (Pradosh, Sankashti, Masik Shivratri, Vinayaka Chaturthi), Diwali 5-day calendar,
# Sawan Somvar list, and related-paath links on festival pages.
# Executed after library_section (uses observance, SPANS, FEST, TODAY_D, moonrise, day_panchang, DAYS, add, band, sec_head,
# faq_html, faq_ld, hdate_w, hdate, e, ct12, nxt_fest, ART, PAGES, MONTHS_HI, WD, CITY_PAGES).
import datetime as _dt
def _sun(d):
    p = DAYS.get(d) or day_panchang(d)
    return p
def _row_tbl(head, rows):
    return f'<div class="tbl"><table class="ptable"><thead><tr>{"".join(f"<th>{h}</th>" for h in head)}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
VRAT_PAGES = []
def vrat_page(slug, title, desc, h1, ans, art, head, rows, faqs, extra_html="", crumb=None):
    body = (band(h1, ans, crumb or h1, *art, h1) +
            f'<section><div class="wrap">{_row_tbl(head, rows)}'
            '<p class="note">तारीख़ें नई दिल्ली के पंचांग पर आधारित हैं; तिथि का समय दूसरे शहरों में कुछ मिनट अलग हो सकता है।</p>'
            f'{extra_html}</div></section>' + faq_html(faqs))
    add(slug, title, desc[:160], body, crumbs=crumb or h1, ld=[faq_ld(faqs)], active="tyohar-calendar.html")
    VRAT_PAGES.append((slug, h1))

def _fut(lst): return [x for x in lst if x[0] >= TODAY_D]
def _upto(): return TODAY_D + _dt.timedelta(days=400)

# ---------- Pradosh vrat ----------
PRAD = sorted([(d, s0, e0, "शुक्ल") for d, s0, e0, pu, a in observance(12, "pradosh")] + [(d, s0, e0, "कृष्ण") for d, s0, e0, pu, a in observance(27, "pradosh")])
PRAD = [x for x in _fut(PRAD) if x[0] <= _upto()]
PNAME = {0:"सोम प्रदोष",1:"भौम प्रदोष",2:"बुध प्रदोष",3:"गुरु प्रदोष",4:"शुक्र प्रदोष",5:"शनि प्रदोष",6:"रवि प्रदोष"}
if PRAD:
    rows = []
    for d, s0, e0, pk in PRAD:
        _ss = to_ist(sunrise_sunset(d)[1])
        rows.append(f'<tr><td><strong>{hdate_w(d)}</strong></td><td>{PNAME[d.weekday()]} ({pk})</td><td>{ct12(_ss)} – {ct12(_ss + _dt.timedelta(minutes=144))}</td><td>{ct12(s0)}, {s0.day} {MONTHS_HI[s0.month][:3]} – {ct12(e0)}, {e0.day} {MONTHS_HI[e0.month][:3]}</td></tr>')
    n = PRAD[0]
    ans = f"अगला प्रदोष व्रत <strong>{PNAME[n[0].weekday()]}</strong> है, जो <strong>{hdate_w(n[0])}</strong> को है। नीचे अगले 13 महीनों के सभी प्रदोष व्रत की तारीख़ और त्रयोदशी तिथि का समय है।"
    faqs = [("अगला प्रदोष व्रत कब है?", f"{PNAME[n[0].weekday()]} — {hdate_w(n[0])}।"),
            ("प्रदोष व्रत किस तिथि को होता है?", "हर महीने दोनों पक्षों की त्रयोदशी को — उस दिन, जिसकी शाम (प्रदोष काल) में त्रयोदशी तिथि हो। महीने में दो बार।"),
            ("सोम प्रदोष और शनि प्रदोष क्या है?", "सोमवार को पड़ने वाला प्रदोष सोम प्रदोष और शनिवार वाला शनि प्रदोष कहलाता है; दोनों को विशेष फलदायी माना जाता है।"),
            ("प्रदोष व्रत में पूजा कब करें?", "सूर्यास्त के बाद के लगभग ढाई घंटे (प्रदोष काल) में शिव जी का अभिषेक और पूजा की जाती है; तालिका में हर प्रदोष का यह समय दिया है।")]
    vrat_page("pradosh-vrat-list.html", f"प्रदोष व्रत {TODAY_D.year}–{TODAY_D.year+1} लिस्ट — अगला प्रदोष कब है? | OmKiran Bhakti",
              f"अगला प्रदोष व्रत: {PNAME[n[0].weekday()]}, {hdate(n[0])}। सभी प्रदोष व्रत (सोम, भौम, शनि प्रदोष) की तारीख़, त्रयोदशी तिथि का समय और पूजा का प्रदोष काल।",
              "प्रदोष व्रत कब है?", ans, ART["shiv"], ["तारीख़","प्रदोष","प्रदोष काल (पूजा)","त्रयोदशी तिथि"], rows, faqs,
              '<p style="margin-top:1rem">पूजा में पढ़ें: <a href="shiv-chalisa.html">शिव चालीसा</a>, <a href="shiv-aarti-om-jai-shiv-omkara.html">शिव आरती</a>, <a href="rudrashtakam.html">रुद्राष्टकम्</a></p>')

# ---------- Sankashti chaturthi (with moonrise) ----------
SANK = [x for x in _fut([(d, s0, e0, pu) for d, s0, e0, pu, a in observance(18, "night")]) if x[0] <= _upto()]
if SANK:
    rows = []
    for d, s0, e0, pu in SANK:
        mr = moonrise(d)
        tag = " (अंगारकी)" if d.weekday() == 1 else ""
        extra = {"माघ":" — सकट चौथ","कार्तिक":" — करवा चौथ"}.get(pu, "")
        rows.append(f'<tr><td><strong>{hdate_w(d)}</strong></td><td>{pu} संकष्टी{tag}{extra}</td><td class="big">{ct12(mr) if mr else "—"}</td></tr>')
    n = SANK[0]; nmr = moonrise(n[0])
    ans = f"अगली संकष्टी चतुर्थी <strong>{hdate_w(n[0])}</strong> को है; दिल्ली में चंद्रोदय लगभग <strong>{ct12(nmr) if nmr else '—'}</strong> बजे होगा। नीचे सभी संकष्टी चतुर्थी और चाँद निकलने का समय है।"
    faqs = [("अगली संकष्टी चतुर्थी कब है?", f"{hdate_w(n[0])} — चंद्रोदय लगभग {ct12(nmr) if nmr else '—'} (दिल्ली)।"),
            ("संकष्टी चतुर्थी का व्रत कैसे खोलते हैं?", "दिन भर व्रत रखकर रात को चाँद निकलने पर उसे अर्घ्य देकर और गणेश जी की पूजा करके व्रत खोला जाता है।"),
            ("अंगारकी चतुर्थी क्या है?", "जब संकष्टी चतुर्थी मंगलवार को पड़े, तो उसे अंगारकी चतुर्थी कहते हैं; इसे सबसे शुभ संकष्टी माना जाता है।")]
    vrat_page("sankashti-chaturthi-list.html", f"संकष्टी चतुर्थी {TODAY_D.year}–{TODAY_D.year+1} — तारीख़ और चाँद निकलने का समय | OmKiran Bhakti",
              f"अगली संकष्टी चतुर्थी: {hdate(n[0])}। सभी संकष्टी (अंगारकी, सकट चौथ, करवा चौथ सहित) की तारीख़ और दिल्ली में चंद्रोदय समय।",
              "संकष्टी चतुर्थी कब है?", ans, ART["ganesh"], ["तारीख़","संकष्टी","चंद्रोदय (दिल्ली)"], rows, faqs,
              '<p style="margin-top:1rem">पूजा में पढ़ें: <a href="ganesh-chalisa.html">गणेश चालीसा</a>, <a href="sankatnashan-ganesh-stotra.html">संकटनाशन गणेश स्तोत्र</a>, <a href="ganesh-aarti-jai-ganesh-deva.html">गणेश आरती</a></p>')

# ---------- Vinayaka chaturthi ----------
VIN = [x for x in _fut([(d, s0, e0, pu) for d, s0, e0, pu, a in observance(3, "madhyahna")]) if x[0] <= _upto()]
if VIN:
    rows = [f'<tr><td><strong>{hdate_w(d)}</strong></td><td>{pu} विनायक चतुर्थी{" (गणेश चतुर्थी)" if pu=="भाद्रपद" else ""}</td><td>{ct12(s0)}, {s0.day} {MONTHS_HI[s0.month][:3]} – {ct12(e0)}, {e0.day} {MONTHS_HI[e0.month][:3]}</td></tr>' for d, s0, e0, pu in VIN]
    n = VIN[0]
    faqs = [("अगली विनायक चतुर्थी कब है?", f"{hdate_w(n[0])}।"),
            ("विनायक चतुर्थी और संकष्टी चतुर्थी में क्या अंतर है?", "विनायक चतुर्थी शुक्ल पक्ष की चतुर्थी है (पूजा दोपहर में), संकष्टी कृष्ण पक्ष की चतुर्थी है (व्रत चाँद को अर्घ्य देकर खुलता है)।"),
            ("विनायक चतुर्थी पर चाँद क्यों नहीं देखते?", "मान्यता है कि शुक्ल चतुर्थी की रात चाँद देखने से झूठा कलंक लगता है, इसलिए इस दिन चंद्र-दर्शन से बचा जाता है।")]
    vrat_page("vinayaka-chaturthi-list.html", f"विनायक चतुर्थी {TODAY_D.year}–{TODAY_D.year+1} — सभी तारीख़ें | OmKiran Bhakti",
              f"अगली विनायक चतुर्थी: {hdate(n[0])}। हर महीने की विनायक (शुक्ल) चतुर्थी की तारीख़ और तिथि का समय।",
              "विनायक चतुर्थी कब है?", f"अगली विनायक चतुर्थी <strong>{hdate_w(n[0])}</strong> को है। नीचे हर महीने की विनायक चतुर्थी की तारीख़ है।", ART["ganesh"],
              ["तारीख़","चतुर्थी","चतुर्थी तिथि"], rows, faqs)

# ---------- Masik Shivratri ----------
MSR = [x for x in _fut([(d, s0, e0, pu) for d, s0, e0, pu, a in observance(28, "nishita")]) if x[0] <= _upto()]
if MSR:
    rows = [f'<tr><td><strong>{hdate_w(d)}</strong></td><td>{pu} मासिक शिवरात्रि{" (महाशिवरात्रि)" if pu=="फाल्गुन" else ""}</td><td>{ct12(s0)}, {s0.day} {MONTHS_HI[s0.month][:3]} – {ct12(e0)}, {e0.day} {MONTHS_HI[e0.month][:3]}</td></tr>' for d, s0, e0, pu in MSR]
    n = MSR[0]
    faqs = [("अगली मासिक शिवरात्रि कब है?", f"{hdate_w(n[0])}।"),
            ("मासिक शिवरात्रि किस तिथि को होती है?", "हर महीने कृष्ण पक्ष की चतुर्दशी को — उस रात, जिसमें आधी रात (निशीथ काल) के समय चतुर्दशी हो।"),
            ("महाशिवरात्रि और मासिक शिवरात्रि में क्या अंतर है?", "फाल्गुन मास की मासिक शिवरात्रि ही महाशिवरात्रि कहलाती है; बाकी 11 मासिक शिवरात्रि हैं।")]
    vrat_page("masik-shivratri-list.html", f"मासिक शिवरात्रि {TODAY_D.year}–{TODAY_D.year+1} — सभी तारीख़ें | OmKiran Bhakti",
              f"अगली मासिक शिवरात्रि: {hdate(n[0])}। हर महीने की शिवरात्रि की तारीख़ और चतुर्दशी तिथि का समय।",
              "मासिक शिवरात्रि कब है?", f"अगली मासिक शिवरात्रि <strong>{hdate_w(n[0])}</strong> को है। नीचे हर महीने की शिवरात्रि है।", ART["shiv"],
              ["तारीख़","शिवरात्रि","चतुर्दशी तिथि"], rows, faqs,
              '<p style="margin-top:1rem">पूजा में पढ़ें: <a href="om-namah-shivaya.html">ॐ नमः शिवाय</a>, <a href="shiv-tandav-stotram.html">शिव तांडव</a>, <a href="lingashtakam.html">लिंगाष्टकम्</a></p>')

# ---------- Diwali 5 days ----------
_d5 = [("govatsa-dwadashi","वसु बारस / गोवत्स द्वादशी"),("dhanteras","धनतेरस"),("narak-chaturdashi","नरक चतुर्दशी (रूप चौदस)"),("diwali","दिवाली — लक्ष्मी पूजा"),
       ("govardhan-puja","गोवर्धन पूजा (अन्नकूट)"),("bhai-dooj","भाई दूज"),("chitragupt-puja","चित्रगुप्त पूजा")]
dwn = nxt_fest("diwali")
if dwn:
    Y = dwn["date"].year
    items = []
    for k, label in _d5:
        x = next((o for o in FEST.get(k, []) if abs((o["date"] - dwn["date"]).days) <= 5), None)
        if x: items.append((x["date"], label, f"{k}-kab-hai.html"))
    items.sort(key=lambda x: x[0])
    rows = [f'<tr><td><strong>{hdate_w(d)}</strong></td><td><a href="{u}">{e(l)}</a></td></tr>' for d, l, u in items]
    same = [l for d, l, u in items if d == dwn["date"] and "दिवाली" not in l]
    ans = (f"दिवाली {Y} का पाँच दिन का उत्सव <strong>{hdate(items[0][0])}</strong> से <strong>{hdate(items[-1][0])}</strong> तक है। लक्ष्मी पूजा <strong>{hdate_w(dwn['date'])}</strong> को है।"
           + (f" इस बार {', '.join(same)} भी उसी दिन है।" if same else ""))
    faqs = [(f"दिवाली {Y} कब है?", f"लक्ष्मी पूजा {hdate_w(dwn['date'])} को।"),
            (f"धनतेरस {Y} कब है?", next((hdate_w(d) for d, l, u in items if l == "धनतेरस"), "")),
            (f"छोटी दिवाली (रूप चौदस) {Y} कब है?", next((hdate_w(d) for d, l, u in items if l.startswith("नरक")), "")),
            (f"भाई दूज {Y} कब है?", next((hdate_w(d) for d, l, u in items if l == "भाई दूज"), ""))]
    vrat_page("diwali-calendar.html", f"दिवाली {Y} कैलेंडर — धनतेरस से भाई दूज तक पाँचों दिन | OmKiran Bhakti",
              f"दिवाली {Y}: वसु बारस, धनतेरस, रूप चौदस, लक्ष्मी पूजा ({hdate(dwn['date'])}), गोवर्धन पूजा, भाई दूज — हर दिन की तारीख़ और पूजा का समय।",
              f"दिवाली {Y}: पाँचों दिन की तारीख़ें", ans, ("F95csn49Rq0",72), ["तारीख़","पर्व"], rows, faqs,
              '<p style="margin-top:1rem"><a href="diwali-lakshmi-puja-muhurat.html">अपने शहर का लक्ष्मी पूजा मुहूर्त</a> · <a href="lakshmi-aarti.html">लक्ष्मी आरती</a> · <a href="shri-suktam.html">श्री सूक्त</a></p>',
              crumb="दिवाली कैलेंडर")

# ---------- Chhath 4 days ----------
chn = nxt_fest("chhath-puja")
if chn:
    Y = chn["date"].year
    seq = [("chhath-nahay-khay","पहला दिन — नहाय-खाय"),("chhath-kharna","दूसरा दिन — खरना"),("chhath-puja","तीसरा दिन — संध्या अर्घ्य"),("chhath-usha-arghya","चौथा दिन — उषा अर्घ्य और पारण")]
    items = []
    for k, l in seq:
        x = next((o for o in FEST.get(k, []) if abs((o["date"] - chn["date"]).days) <= 3), None)
        if x: items.append((x["date"], l, f"{k}-kab-hai.html"))
    rows = [f'<tr><td><strong>{hdate_w(d)}</strong></td><td><a href="{u}">{e(l)}</a></td></tr>' for d, l, u in items]
    faqs = [(f"छठ पूजा {Y} कब से शुरू है?", f"नहाय-खाय {hdate_w(items[0][0])} से।"),
            (f"छठ {Y} में संध्या अर्घ्य कब है?", hdate_w(chn["date"])),
            ("छठ में खरना क्या होता है?", "दूसरे दिन व्रती दिन भर निर्जला रहकर शाम को गुड़ की खीर और रोटी का प्रसाद बनाते हैं; इसके बाद 36 घंटे का निर्जला व्रत शुरू होता है।")]
    vrat_page("chhath-puja-calendar.html", f"छठ पूजा {Y} कैलेंडर — नहाय-खाय, खरना, संध्या और उषा अर्घ्य | OmKiran Bhakti",
              f"छठ महापर्व {Y}: नहाय-खाय {hdate(items[0][0])}, खरना, संध्या अर्घ्य {hdate(chn['date'])} और उषा अर्घ्य — चारों दिन की तारीख़।",
              f"छठ पूजा {Y}: चारों दिन की तारीख़ें", f"छठ महापर्व {Y} <strong>{hdate(items[0][0])}</strong> को नहाय-खाय से शुरू होकर <strong>{hdate(items[-1][0])}</strong> को उषा अर्घ्य के साथ पूरा होगा।",
              ("ktQUU5Y3tPE",50), ["तारीख़","दिन"], rows, faqs,
              '<p style="margin-top:1rem"><a href="chhath-puja-arghya-time.html">अपने शहर का अर्घ्य का समय</a> · <a href="surya-dev-aarti.html">सूर्य देव की आरती</a></p>', crumb="छठ कैलेंडर")

# ---------- Sawan Somvar ----------
sw = nxt_fest("sawan-start")
if sw:
    st = sw["date"]
    end = next((x[2].date() for x in SPANS if x[0] == 14 and x[1].date() > st), st + _dt.timedelta(days=30))
    mons = [st + _dt.timedelta(days=i) for i in range((end - st).days + 1) if (st + _dt.timedelta(days=i)).weekday() == 0]
    Y = st.year
    _ord = ['पहला','दूसरा','तीसरा','चौथा','पाँचवाँ','छठा']
    rows = [f'<tr><td><strong>{_ord[i]} सोमवार</strong></td><td>{hdate_w(d)}</td></tr>' for i, d in enumerate(mons)]
    faqs = [(f"सावन {Y} कब से शुरू है?", f"{hdate_w(st)} से; सावन {hdate(end)} (श्रावण पूर्णिमा) तक है।"),
            (f"सावन {Y} में कितने सोमवार हैं?", f"{len(mons)} सोमवार — पहला {hdate(mons[0])} को।" if mons else ""),
            ("सावन सोमवार व्रत कैसे करें?", "सुबह स्नान के बाद शिवलिंग पर जल, दूध, बेलपत्र चढ़ाएँ, ‘ॐ नमः शिवाय’ का जप करें और शाम को शिव आरती करके फलाहार लें।")]
    vrat_page("sawan-somvar.html", f"सावन सोमवार {Y} — सावन कब से शुरू, सभी सोमवार की तारीख़ | OmKiran Bhakti",
              f"सावन {Y}: {hdate(st)} से {hdate(end)} तक। सभी {len(mons)} सावन सोमवार की तारीख़ और व्रत विधि (उत्तर भारत, पूर्णिमांत)।",
              f"सावन सोमवार {Y}", f"सावन {Y} <strong>{hdate_w(st)}</strong> से शुरू होकर <strong>{hdate(end)}</strong> तक है। इसमें <strong>{len(mons)} सोमवार</strong> हैं।",
              ART["shiv"], ["सोमवार","तारीख़"], rows, faqs,
              '<p class="note">यह उत्तर भारत (पूर्णिमांत पंचांग) की तारीख़ है; महाराष्ट्र, गुजरात, दक्षिण भारत (अमांत) में सावन 15 दिन बाद शुरू होता है।</p>'
              '<p style="margin-top:1rem">पूजा में पढ़ें: <a href="shiv-chalisa.html">शिव चालीसा</a>, <a href="om-namah-shivaya.html">ॐ नमः शिवाय</a>, <a href="somvar-vrat-katha.html">सोमवार व्रत कथा</a></p>')

# ---------- related paath on festival pages ----------
RELP = {"tulsi-vivah":["tulsi-mata-aarti.html","vishnu-chalisa.html"],"dev-uthani-ekadashi":["tulsi-mata-aarti.html","ekadashi-mata-aarti.html","vishnu-chalisa.html"],
 "kaal-bhairav-jayanti":["bhairav-chalisa.html","bhairav-aarti.html"],"shani-jayanti":["shani-chalisa.html","shani-dev-aarti.html","dashrath-krit-shani-stotra.html"],
 "ganga-dussehra":["ganga-chalisa.html","ganga-aarti.html"],"radha-ashtami":["radha-chalisa.html","radha-kripa-kataksh-stotra.html","aarti-kunj-bihari-ki.html"],
 "sawan-start":["sawan-somvar.html","shiv-chalisa.html","om-namah-shivaya.html"],"hariyali-teej":["parvati-chalisa.html","parvati-aarti.html"],
 "hartalika-teej":["parvati-chalisa.html","parvati-aarti.html"],"kajari-teej":["parvati-aarti.html"],"gangaur":["parvati-aarti.html","parvati-chalisa.html"],
 "sakat-chauth":["sankashti-chaturthi-list.html","ganesh-chalisa.html","sankatnashan-ganesh-stotra.html"],"ratha-saptami":["surya-chalisa.html","aditya-hridaya-stotra.html","surya-dev-aarti.html"],
 "sita-navami":["ram-chalisa.html","ram-raksha-stotra.html"],"govatsa-dwadashi":["diwali-calendar.html","krishna-chalisa.html"],"gopashtami":["krishna-chalisa.html","aarti-kunj-bihari-ki.html"],
 "dhanteras":["diwali-calendar.html","lakshmi-aarti.html"],"narak-chaturdashi":["diwali-calendar.html","hanuman-chalisa.html"],"diwali":["diwali-calendar.html","diwali-lakshmi-puja-muhurat.html","lakshmi-chalisa.html","shri-suktam.html"],
 "govardhan-puja":["diwali-calendar.html","krishna-chalisa.html"],"bhai-dooj":["diwali-calendar.html"],"chitragupt-puja":["diwali-calendar.html"],
 "chhath-puja":["chhath-puja-calendar.html","chhath-puja-arghya-time.html","surya-dev-aarti.html"],"chhath-nahay-khay":["chhath-puja-calendar.html","chhath-puja-arghya-time.html"],
 "chhath-kharna":["chhath-puja-calendar.html","chhath-puja-arghya-time.html"],"chhath-usha-arghya":["chhath-puja-calendar.html","chhath-puja-arghya-time.html"],
 "maha-shivratri":["masik-shivratri-list.html","shiv-chalisa.html","shiv-tandav-stotram.html"],"vaikunth-chaturdashi":["vishnu-chalisa.html","shiv-chalisa.html"],
 "akshay-navami":["vishnu-chalisa.html"],"sheetala-ashtami":["durga-chalisa.html"],"vat-savitri":["parvati-aarti.html"],"nag-panchami":["shiv-chalisa.html"],
 "narasimha-jayanti":["dashavatar-stotram.html","vishnu-chalisa.html"],"dattatreya-jayanti":["om-jai-jagdish-hare-aarti.html"],"jagannath-rath-yatra":["krishnashtakam.html","om-jai-jagdish-hare-aarti.html"],
 "sharadiya-navratri":["navratri-ashtami-navami-kab-hai.html","durga-chalisa.html"],"chaitra-navratri":["navratri-ashtami-navami-kab-hai.html","durga-chalisa.html"]}
def _ttl(slug):
    if slug not in PAGES: return None
    t = PAGES[slug].split("<title>")[1].split("</title>")[0]
    return html.unescape(t.split(" | ")[0])
_more = sec_head("और त्योहार")
for k, lst in RELP.items():
    fp = f"{k}-kab-hai.html"
    if fp not in PAGES: continue
    lis = "".join(f'<li><a href="{u}"><strong>{e(_ttl(u).split(" — ")[0])}</strong><span>{e(" — ".join(_ttl(u).split(" — ")[1:]) or "पढ़ें")}</span></a></li>' for u in lst if _ttl(u))
    if not lis: continue
    PAGES[fp] = PAGES[fp].replace(f'<section><div class="wrap">{_more}', f'<section class="band"><div class="wrap">{sec_head("पूजा में पढ़ें")}<ul class="library">{lis}</ul></div></section><section><div class="wrap">{_more}', 1)

# add the vrat lists to the Q&A hub, then build it
_vq = {"pradosh-vrat-list.html":("अगला प्रदोष व्रत कब है?", PRAD), "sankashti-chaturthi-list.html":("अगली संकष्टी चतुर्थी कब है?", SANK),
       "vinayaka-chaturthi-list.html":("अगली विनायक चतुर्थी कब है?", VIN), "masik-shivratri-list.html":("अगली मासिक शिवरात्रि कब है?", MSR)}
for _u, (_q, _l) in _vq.items():
    if _l: QA.insert(2, (_q, f"{hdate_w(_l[0][0])}।", _u))
for _u, _h in VRAT_PAGES:
    if _u in ("diwali-calendar.html", "chhath-puja-calendar.html", "sawan-somvar.html"):
        QA.append((_h.replace(": ", " — ") + " कब हैं?" if "तारीख़ें" in _h else _h + " कब है?", "सभी तारीख़ें इस पेज पर।", _u))
build_hub()

_vl = "".join(f'<li><a href="{u}"><strong>{e(h)}</strong><span>पूरी सूची</span></a></li>' for u, h in VRAT_PAGES)
for _fp in ("tyohar-calendar.html",):
    if _fp in PAGES: PAGES[_fp] = PAGES[_fp].replace('<ul class="hot-list"><li><a href="tyohar-kab-hai.html">', '<ul class="hot-list">' + _vl + '<li><a href="tyohar-kab-hai.html">', 1)

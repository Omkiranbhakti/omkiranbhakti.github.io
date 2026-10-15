# City-wise festival timings (Karwa Chauth moonrise, Diwali Lakshmi puja, Chhath arghya).
# Executed inside build.py after panchang_section (uses add, band, sec_head, faq_html, faq_ld, FEST, TODAY_D, hdate_w, e, FART, ART, SITE).
import datetime as _dt
from citycalc import moonrise as c_moonrise, sun_times as c_sun, lagna_window as c_lagna_win, chandrodaya_day as c_chandro
IN_TZ = "Asia/Kolkata"
# (hindi, english, lat, lon) — grouped roughly north -> south
IN_CITIES = [
 ("दिल्ली","Delhi",28.6139,77.2090),("नोएडा","Noida",28.5355,77.3910),("गुरुग्राम","Gurugram",28.4595,77.0266),
 ("गाज़ियाबाद","Ghaziabad",28.6692,77.4538),("फ़रीदाबाद","Faridabad",28.4089,77.3178),("मेरठ","Meerut",28.9845,77.7064),
 ("चंडीगढ़","Chandigarh",30.7333,76.7794),("लुधियाना","Ludhiana",30.9010,75.8573),("अमृतसर","Amritsar",31.6340,74.8723),
 ("जालंधर","Jalandhar",31.3260,75.5762),("पटियाला","Patiala",30.3398,76.3869),("अंबाला","Ambala",30.3782,76.7767),
 ("पानीपत","Panipat",29.3909,76.9635),("करनाल","Karnal",29.6857,76.9905),("रोहतक","Rohtak",28.8955,76.6066),
 ("हिसार","Hisar",29.1492,75.7217),("जम्मू","Jammu",32.7266,74.8570),("श्रीनगर","Srinagar",34.0837,74.7973),
 ("शिमला","Shimla",31.1048,77.1734),("देहरादून","Dehradun",30.3165,78.0322),("हरिद्वार","Haridwar",29.9457,78.1642),
 ("जयपुर","Jaipur",26.9124,75.7873),("जोधपुर","Jodhpur",26.2389,73.0243),("उदयपुर","Udaipur",24.5854,73.7125),
 ("बीकानेर","Bikaner",28.0229,73.3119),("कोटा","Kota",25.2138,75.8648),("अजमेर","Ajmer",26.4499,74.6399),
 ("आगरा","Agra",27.1767,78.0081),("मथुरा","Mathura",27.4924,77.6737),("अलीगढ़","Aligarh",27.8974,78.0880),
 ("बरेली","Bareilly",28.3670,79.4304),("मुरादाबाद","Moradabad",28.8386,78.7733),("लखनऊ","Lucknow",26.8467,80.9462),
 ("कानपुर","Kanpur",26.4499,80.3319),("अयोध्या","Ayodhya",26.7922,82.1998),("प्रयागराज","Prayagraj",25.4358,81.8463),
 ("वाराणसी","Varanasi",25.3176,82.9739),("गोरखपुर","Gorakhpur",26.7606,83.3732),("पटना","Patna",25.5941,85.1376),
 ("गया","Gaya",24.7914,85.0002),("मुज़फ़्फ़रपुर","Muzaffarpur",26.1209,85.3647),("भागलपुर","Bhagalpur",25.2425,86.9842),
 ("रांची","Ranchi",23.3441,85.3096),("जमशेदपुर","Jamshedpur",22.8046,86.2029),("धनबाद","Dhanbad",23.7957,86.4304),
 ("कोलकाता","Kolkata",22.5726,88.3639),("भुवनेश्वर","Bhubaneswar",20.2961,85.8245),("गुवाहाटी","Guwahati",26.1445,91.7362),
 ("भोपाल","Bhopal",23.2599,77.4126),("इंदौर","Indore",22.7196,75.8577),("ग्वालियर","Gwalior",26.2183,78.1828),
 ("जबलपुर","Jabalpur",23.1815,79.9864),("उज्जैन","Ujjain",23.1765,75.7885),("रायपुर","Raipur",21.2514,81.6296),
 ("अहमदाबाद","Ahmedabad",23.0225,72.5714),("सूरत","Surat",21.1702,72.8311),("वडोदरा","Vadodara",22.3072,73.1812),
 ("मुंबई","Mumbai",19.0760,72.8777),("पुणे","Pune",18.5204,73.8567),("नागपुर","Nagpur",21.1458,79.0882),
 ("नासिक","Nashik",19.9975,73.7898),("हैदराबाद","Hyderabad",17.3850,78.4867),("बेंगलुरु","Bengaluru",12.9716,77.5946),
 ("चेन्नई","Chennai",13.0827,80.2707),("कोच्चि","Kochi",9.9312,76.2673),("गोवा (पणजी)","Goa",15.4909,73.8278),
]
ABROAD = [  # (hindi, english, lat, lon, tz)
 ("न्यूयॉर्क","New York, USA",40.7128,-74.0060,"America/New_York"),("न्यू जर्सी","New Jersey, USA",40.7357,-74.1724,"America/New_York"),
 ("शिकागो","Chicago, USA",41.8781,-87.6298,"America/Chicago"),("ह्यूस्टन","Houston, USA",29.7604,-95.3698,"America/Chicago"),
 ("डलास","Dallas, USA",32.7767,-96.7970,"America/Chicago"),("सैन फ़्रांसिस्को","San Francisco, USA",37.7749,-122.4194,"America/Los_Angeles"),
 ("लॉस एंजेलिस","Los Angeles, USA",34.0522,-118.2437,"America/Los_Angeles"),("सिएटल","Seattle, USA",47.6062,-122.3321,"America/Los_Angeles"),
 ("टोरंटो","Toronto, Canada",43.6532,-79.3832,"America/Toronto"),("ब्रैम्पटन","Brampton, Canada",43.7315,-79.7624,"America/Toronto"),
 ("वैंकूवर","Vancouver, Canada",49.2827,-123.1207,"America/Vancouver"),("कैलगरी","Calgary, Canada",51.0447,-114.0719,"America/Edmonton"),
 ("लंदन","London, UK",51.5074,-0.1278,"Europe/London"),("बर्मिंघम","Birmingham, UK",52.4862,-1.8904,"Europe/London"),
 ("लेस्टर","Leicester, UK",52.6369,-1.1398,"Europe/London"),("दुबई","Dubai, UAE",25.2048,55.2708,"Asia/Dubai"),
 ("सिंगापुर","Singapore",1.3521,103.8198,"Asia/Singapore"),("सिडनी","Sydney, Australia",-33.8688,151.2093,"Australia/Sydney"),
 ("मेलबर्न","Melbourne, Australia",-37.8136,144.9631,"Australia/Melbourne"),("ऑकलैंड","Auckland, NZ",-36.8485,174.7633,"Pacific/Auckland"),
 ("काठमांडू","Kathmandu, Nepal",27.7172,85.3240,"Asia/Kathmandu"),
]
def ct12(t):
    h, m = t.hour, t.minute
    part = "सुबह" if h < 12 else ("दोपहर" if h < 16 else ("शाम" if h < 19 else "रात"))
    if h < 4: part = "रात"
    return f"{part} {(h % 12) or 12}:{m:02d}"
def chm(t): return f"{(t.hour % 12) or 12}:{t.minute:02d} {'AM' if t.hour < 12 else 'PM'}"
def nxt_fest(key):
    occ = FEST.get(key, [])
    return next((x for x in occ if x["date"] >= TODAY_D), occ[-1] if occ else None)
CITY_JS = ('<script>(function(){var q=document.getElementById("city-q");if(!q)return;var rows=[].slice.call(document.querySelectorAll(".city-table tbody tr"));'
           'q.addEventListener("input",function(){var v=q.value.trim().toLowerCase();rows.forEach(function(r){r.hidden=v&&r.textContent.toLowerCase().indexOf(v)<0;});});})();</script>')
def city_search(ph):
    return f'<div class="lib-search no-print"><label for="city-q" class="sr">शहर खोजें</label><input type="search" id="city-q" placeholder="{ph}" autocomplete="off"></div>'
CITY_PAGES = []

# ---------- Karwa Chauth: moonrise city-wise ----------
kc = nxt_fest("karwa-chauth")
if kc:
    D = kc["date"]; Y = D.year
    rows_in, data_in = [], {}
    for hi, en, la, lo in IN_CITIES:
        mr = c_moonrise(la, lo, D, IN_TZ); sr, ss = c_sun(la, lo, D, IN_TZ)
        data_in[en] = mr
        rows_in.append(f'<tr><td><strong>{hi}</strong> <span class="en">{en}</span></td><td class="big">{ct12(mr) if mr else "—"}</td><td>{ct12(ss)}</td></tr>')
    rows_ab = []
    for hi, en, la, lo, tz in ABROAD:
        d2, mr = c_chandro(la, lo, tz, D, 18)
        rows_ab.append(f'<tr><td><strong>{hi}</strong> <span class="en">{en}</span></td><td>{hdate_w(d2)}</td><td class="big">{chm(mr) if mr else "—"}</td></tr>')
    dl, mb = data_in["Delhi"], data_in["Mumbai"]
    ans = (f"करवा चौथ {Y} <strong>{hdate_w(D)}</strong> को है। दिल्ली में चाँद लगभग <strong>{ct12(dl)}</strong> और मुंबई में लगभग <strong>{ct12(mb)}</strong> बजे निकलेगा। "
           "नीचे भारत के 65+ शहरों और अमेरिका, कनाडा, ब्रिटेन, दुबई, ऑस्ट्रेलिया के शहरों का चंद्रोदय समय दिया है।")
    faqs = [(f"करवा चौथ {Y} में दिल्ली में चाँद कब निकलेगा?", f"{hdate_w(D)} को दिल्ली में चंद्रोदय लगभग {ct12(dl)} बजे होगा। ऊँची इमारतों या धुंध के कारण चाँद 5–10 मिनट देर से दिख सकता है।"),
            (f"करवा चौथ {Y} में मुंबई में चाँद कब निकलेगा?", f"मुंबई में चंद्रोदय लगभग {ct12(mb)} बजे होगा।"),
            (f"अमेरिका और कनाडा में करवा चौथ {Y} कब है?", "अमेरिका और कनाडा में स्थानीय चंद्रोदय के समय चतुर्थी तिथि एक दिन पहले पड़ रही है, इसलिए वहाँ व्रत की तारीख़ नीचे की विदेश वाली तालिका में देखें।"),
            ("करवा चौथ का चाँद देर से क्यों दिखता है?", "पंचांग में दिया समय वह है जब चाँद क्षितिज (आसमान के किनारे) पर आता है। ऊँची इमारतें, पेड़ या बादल हों तो चाँद 5–15 मिनट बाद दिखाई देता है।")]
    body = (band(f"करवा चौथ {Y}: आपके शहर में चाँद कब निकलेगा?", ans, "करवा चौथ चाँद का समय", *FART["karwa-chauth"], "करवा चौथ",
                 extra=f'<p class="lede"><a href="karwa-chauth-vrat-katha.html">करवा चौथ व्रत कथा</a> और <a href="karwa-chauth-kab-hai.html">तिथि व पूजा का समय</a></p>') +
            f'<section><div class="wrap">{sec_head(f"भारत के शहरों में चंद्रोदय — {hdate_w(D)}")}{city_search("अपना शहर लिखें — जैसे Delhi, पटना, Pune…")}'
            f'<div class="tbl"><table class="ptable city-table"><thead><tr><th>शहर</th><th>चाँद निकलने का समय</th><th>सूर्यास्त (पूजा शुरू)</th></tr></thead><tbody>{"".join(rows_in)}</tbody></table></div>'
            '<p class="note">समय खगोलीय गणना से निकाला गया है (चाँद का क्षितिज पर आना)। ऊँची इमारतों, पेड़ों या बादलों के कारण चाँद 5–15 मिनट देर से दिख सकता है — छत से पूर्व दिशा में देखें।</p></div></section>'
            f'<section class="band"><div class="wrap">{sec_head("विदेश में करवा चौथ — स्थानीय तारीख़ और समय")}'
            f'<div class="tbl"><table class="ptable city-table"><thead><tr><th>शहर</th><th>व्रत की तारीख़ (स्थानीय)</th><th>चंद्रोदय (स्थानीय समय)</th></tr></thead><tbody>{"".join(rows_ab)}</tbody></table></div>'
            '<p class="note">विदेश में व्रत उसी दिन रखा जाता है जिस दिन वहाँ चंद्रोदय के समय कार्तिक कृष्ण चतुर्थी हो — इसलिए कुछ देशों में तारीख़ भारत से एक दिन पहले होती है।</p></div></section>'
            + faq_html(faqs) + CITY_JS)
    ld = [{"@type":"Event","name":f"करवा चौथ {Y}","startDate":D.isoformat(),"eventAttendanceMode":"https://schema.org/OfflineEventAttendanceMode",
           "location":{"@type":"Place","name":"भारत","address":{"@type":"PostalAddress","addressCountry":"IN"}},"description":f"करवा चौथ {Y}: शहरवार चंद्रोदय समय"}, faq_ld(faqs)]
    add("karwa-chauth-chand-kab-niklega.html", f"करवा चौथ {Y} चाँद कब निकलेगा? शहरवार चंद्रोदय समय | OmKiran Bhakti",
        f"करवा चौथ {Y} ({hdate_w(D)}): दिल्ली में चाँद {ct12(dl)}, मुंबई {ct12(mb)}। भारत के 65+ शहरों और USA, कनाडा, UK, दुबई का चंद्रोदय समय।"[:160],
        body, crumbs="करवा चौथ चाँद का समय", ld=ld, active="tyohar-calendar.html")
    CITY_PAGES.append(("karwa-chauth-chand-kab-niklega.html", f"करवा चौथ {Y}: शहरवार चाँद निकलने का समय", "karwa-chauth"))

# ---------- Diwali: Lakshmi puja muhurat city-wise ----------
dw = nxt_fest("diwali")
if dw:
    D = dw["date"]; Y = D.year
    rows, data = [], {}
    for hi, en, la, lo in IN_CITIES:
        sr, ss = c_sun(la, lo, D, IN_TZ)
        pe = ss + _dt.timedelta(minutes=144)
        vr = c_lagna_win(la, lo, ss - _dt.timedelta(minutes=30), ss + _dt.timedelta(hours=5), 1)
        best = None
        if vr:
            s, e2 = max(ss, vr[0]), min(pe, vr[1])
            best = (s, e2) if s < e2 else vr
        data[en] = (ss, pe, vr, best)
        rows.append(f'<tr><td><strong>{hi}</strong> <span class="en">{en}</span></td><td class="big">{(ct12(best[0])+" – "+ct12(best[1])) if best else "—"}</td>'
                    f'<td>{ct12(ss)} – {ct12(pe)}</td><td>{(ct12(vr[0])+" – "+ct12(vr[1])) if vr else "—"}</td></tr>')
    ds, dp, dv, db = data["Delhi"]
    ans = (f"दीपावली {Y} <strong>{hdate_w(D)}</strong> को है। दिल्ली में लक्ष्मी पूजा का सबसे शुभ समय <strong>{ct12(db[0])} से {ct12(db[1])}</strong> तक है — "
           "जब प्रदोष काल और स्थिर वृषभ लग्न एक साथ हों। नीचे 65+ शहरों का अलग-अलग समय है।")
    mb = data["Mumbai"][3]; pt = data["Patna"][3]
    faqs = [(f"दिवाली {Y} में लक्ष्मी पूजा का शुभ मुहूर्त क्या है?", f"दिल्ली में {ct12(db[0])} से {ct12(db[1])} तक (प्रदोष काल में वृषभ लग्न)। दूसरे शहरों का समय तालिका में देखें।"),
            (f"मुंबई में दिवाली {Y} लक्ष्मी पूजा का समय?", f"मुंबई में {ct12(mb[0])} से {ct12(mb[1])} तक।" if mb else "तालिका देखें।"),
            (f"पटना में दिवाली {Y} लक्ष्मी पूजा का समय?", f"पटना में {ct12(pt[0])} से {ct12(pt[1])} तक।" if pt else "तालिका देखें।"),
            ("लक्ष्मी पूजा प्रदोष काल और वृषभ लग्न में क्यों होती है?", "प्रदोष काल सूर्यास्त के बाद के लगभग ढाई घंटे हैं, जो लक्ष्मी पूजा के लिए श्रेष्ठ माने जाते हैं। वृषभ ‘स्थिर लग्न’ है — मान्यता है कि स्थिर लग्न में पूजा करने से लक्ष्मी घर में स्थिर रहती हैं।")]
    body = (band(f"दिवाली {Y}: आपके शहर में लक्ष्मी पूजा का शुभ मुहूर्त", ans, "दिवाली लक्ष्मी पूजा मुहूर्त", *FART["diwali"], "दिवाली",
                 extra=f'<p class="lede"><a href="lakshmi-aarti.html">लक्ष्मी जी की आरती</a>, <a href="lakshmi-chalisa.html">लक्ष्मी चालीसा</a> और <a href="shri-suktam.html">श्री सूक्त</a> — पूजा में साथ पढ़ें।</p>') +
            f'<section><div class="wrap">{sec_head(f"शहरवार लक्ष्मी पूजा मुहूर्त — {hdate_w(D)}")}{city_search("अपना शहर लिखें — जैसे Delhi, लखनऊ, Surat…")}'
            f'<div class="tbl"><table class="ptable city-table"><thead><tr><th>शहर</th><th>सबसे शुभ समय</th><th>प्रदोष काल</th><th>वृषभ लग्न</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
            '<p class="note">‘सबसे शुभ समय’ वह है जब प्रदोष काल (सूर्यास्त से लगभग 2 घंटे 24 मिनट) और स्थिर वृषभ लग्न दोनों एक साथ हों। समय लाहिड़ी अयनांश के साथ खगोलीय गणना से निकाला गया है; अपने पुरोहित या स्थानीय पंचांग से मिलान कर लें।</p></div></section>'
            + faq_html(faqs) + CITY_JS)
    ld = [{"@type":"Event","name":f"दीपावली {Y} लक्ष्मी पूजा","startDate":D.isoformat(),"eventAttendanceMode":"https://schema.org/OfflineEventAttendanceMode",
           "location":{"@type":"Place","name":"भारत","address":{"@type":"PostalAddress","addressCountry":"IN"}},"description":f"दीपावली {Y}: शहरवार लक्ष्मी पूजा मुहूर्त"}, faq_ld(faqs)]
    add("diwali-lakshmi-puja-muhurat.html", f"दिवाली {Y} लक्ष्मी पूजा मुहूर्त — आपके शहर का शुभ समय | OmKiran Bhakti",
        f"दिवाली {Y} ({hdate_w(D)}): दिल्ली में लक्ष्मी पूजा {ct12(db[0])}–{ct12(db[1])}। 65+ शहरों का प्रदोष काल, वृषभ लग्न और सबसे शुभ समय।"[:160],
        body, crumbs="दिवाली लक्ष्मी पूजा मुहूर्त", ld=ld, active="tyohar-calendar.html")
    CITY_PAGES.append(("diwali-lakshmi-puja-muhurat.html", f"दिवाली {Y}: शहरवार लक्ष्मी पूजा मुहूर्त", "diwali"))

# ---------- Chhath: sandhya arghya (sunset) and usha arghya (sunrise) ----------
ch = nxt_fest("chhath-puja")
if ch:
    D = ch["date"]; D2 = D + _dt.timedelta(days=1); Y = D.year
    CH_CITIES = [c for c in IN_CITIES if c[1] in ("Patna","Gaya","Muzaffarpur","Bhagalpur","Ranchi","Jamshedpur","Dhanbad","Varanasi","Gorakhpur",
                 "Prayagraj","Lucknow","Kanpur","Ayodhya","Kolkata","Delhi","Noida","Gurugram","Ghaziabad","Faridabad","Mumbai","Pune","Surat",
                 "Ahmedabad","Bengaluru","Hyderabad","Chennai","Chandigarh","Ludhiana","Jaipur","Bhopal","Indore","Raipur","Guwahati","Bhubaneswar")]
    rows, data = [], {}
    for hi, en, la, lo in CH_CITIES:
        _, ss = c_sun(la, lo, D, IN_TZ); sr2, _ = c_sun(la, lo, D2, IN_TZ)
        data[en] = (ss, sr2)
        rows.append(f'<tr><td><strong>{hi}</strong> <span class="en">{en}</span></td><td class="big">{ct12(ss)}</td><td class="big">{ct12(sr2)}</td></tr>')
    ps, pr = data["Patna"]; dls, dlr = data["Delhi"]
    ans = (f"छठ पूजा {Y} में संध्या अर्घ्य <strong>{hdate_w(D)}</strong> को और उषा अर्घ्य <strong>{hdate_w(D2)}</strong> को है। "
           f"पटना में डूबते सूर्य को अर्घ्य {ct12(ps)} और उगते सूर्य को अर्घ्य {ct12(pr)} बजे; दिल्ली में {ct12(dls)} और {ct12(dlr)} बजे।")
    faqs = [(f"छठ पूजा {Y} में पटना में अर्घ्य का समय क्या है?", f"संध्या अर्घ्य ({hdate_w(D)}) सूर्यास्त {ct12(ps)}; उषा अर्घ्य ({hdate_w(D2)}) सूर्योदय {ct12(pr)}।"),
            (f"छठ पूजा {Y} में दिल्ली में अर्घ्य का समय क्या है?", f"संध्या अर्घ्य सूर्यास्त {ct12(dls)}; उषा अर्घ्य सूर्योदय {ct12(dlr)}।"),
            ("छठ में अर्घ्य किस समय देना चाहिए?", "संध्या अर्घ्य डूबते सूर्य को सूर्यास्त से ठीक पहले और उषा अर्घ्य उगते सूर्य को सूर्योदय के समय दिया जाता है। घाट पर 15–20 मिनट पहले पहुँचना अच्छा रहता है।")]
    body = (band(f"छठ पूजा {Y}: आपके शहर में अर्घ्य का समय", ans, "छठ अर्घ्य का समय", *FART.get("chhath-puja", ART["vishnu"]), "छठ पूजा",
                 extra='<p class="lede"><a href="chhath-puja-kab-hai.html">छठ पूजा की तारीख़ें</a>, <a href="surya-dev-aarti.html">सूर्य देव की आरती</a> और <a href="aditya-hridaya-stotra.html">आदित्य हृदय स्तोत्र</a></p>') +
            f'<section><div class="wrap">{sec_head("शहरवार अर्घ्य का समय")}{city_search("अपना शहर लिखें — जैसे Patna, गया, Delhi…")}'
            f'<div class="tbl"><table class="ptable city-table"><thead><tr><th>शहर</th><th>संध्या अर्घ्य (सूर्यास्त), {D.day} {MONTHS_HI[D.month]}</th><th>उषा अर्घ्य (सूर्योदय), {D2.day} {MONTHS_HI[D2.month]}</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
            '<p class="note">सूर्योदय और सूर्यास्त का समय समतल क्षितिज के लिए है; नदी किनारे पेड़ या इमारतें हों तो सूर्य कुछ मिनट पहले छिप या बाद में दिख सकता है।</p></div></section>'
            + faq_html(faqs) + CITY_JS)
    ld = [{"@type":"Event","name":f"छठ पूजा {Y}","startDate":D.isoformat(),"endDate":D2.isoformat(),"eventAttendanceMode":"https://schema.org/OfflineEventAttendanceMode",
           "location":{"@type":"Place","name":"भारत","address":{"@type":"PostalAddress","addressCountry":"IN"}},"description":f"छठ पूजा {Y}: शहरवार अर्घ्य समय"}, faq_ld(faqs)]
    add("chhath-puja-arghya-time.html", f"छठ पूजा {Y} अर्घ्य का समय — पटना, दिल्ली और शहरवार | OmKiran Bhakti",
        f"छठ पूजा {Y}: संध्या अर्घ्य {hdate_w(D)}, उषा अर्घ्य {hdate_w(D2)}। पटना में सूर्यास्त {ct12(ps)}, सूर्योदय {ct12(pr)} — 34 शहरों का अर्घ्य समय।"[:160],
        body, crumbs="छठ अर्घ्य का समय", ld=ld, active="tyohar-calendar.html")
    CITY_PAGES.append(("chhath-puja-arghya-time.html", f"छठ पूजा {Y}: शहरवार अर्घ्य का समय", "chhath-puja"))

# link each festival page to its city-wise page
for _h, _t, _k in CITY_PAGES:
    _fp = f"{_k}-kab-hai.html"
    if _fp in PAGES:
        PAGES[_fp] = PAGES[_fp].replace('<section><div class="wrap">',
            f'<section class="hot"><div class="wrap"><ul class="hot-list"><li><a href="{_h}"><strong>{e(_t)}</strong><span>अपने शहर का समय देखें</span></a></li></ul></div></section><section><div class="wrap">', 1)

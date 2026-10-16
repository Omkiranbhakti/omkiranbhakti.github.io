# Live darshan: official temple YouTube streams shown inside YouTube's own player on our pages (views/ads stay with the temple).
# Channel IDs verified on 16 Oct 2026: each is linked or embedded by the temple's own website, or carries the temple trust's name
# with live darshan uploads (see src/live_probe.py results).
import library as _L
LIVE = [
 # slug, name, place, channel_id, channel_name, verified_note, art, aarti (title, verses, page), related paath
 ("ram-mandir-ayodhya","श्री राम जन्मभूमि मंदिर","अयोध्या","UCIbhcJEGjI7fRfKiG_p0Mqg","Shri Ram Janmbhoomi Teerth Kshetra","ट्रस्ट की आधिकारिक वेबसाइट srjbtkshetra.org इसी चैनल से जुड़ी है",
  ART["ram"],("श्री रामचंद्र कृपालु भजु मन",_L.RAMCHANDRA_KRIPALU,"shri-ramchandra-kripalu.html"),["ram-raksha-stotra.html","ram-chalisa.html","ramayan-ji-ki-aarti.html"]),
 ("mahakaleshwar-ujjain","श्री महाकालेश्वर ज्योतिर्लिंग","उज्जैन","UCEUuwXHmHckwmdANSy4c7Sw","Shrimahakaleshwarjyotirlingam","यह चैनल श्री महाकालेश्वर मंदिर प्रबंध समिति के आयोजनों का प्रसारण करता है",
  ART["shiv"],("ॐ जय शिव ओंकारा",OM_JAI_SHIV_OMKARA,"shiv-aarti-om-jai-shiv-omkara.html"),["shiv-chalisa.html","shiv-tandav-stotram.html","rudrashtakam.html"]),
 ("kashi-vishwanath-varanasi","श्री काशी विश्वनाथ धाम","वाराणसी","UCdMj2twWfMHXrWgX5oVdoyA","Shree Kashi Vishwanath Mandir Trust","मंदिर ट्रस्ट के नाम वाला चैनल, जिस पर नियमित ‘लाइव दर्शन’ प्रसारण होता है",
  ART["shivaarti"],("ॐ जय शिव ओंकारा",OM_JAI_SHIV_OMKARA,"shiv-aarti-om-jai-shiv-omkara.html"),["shiv-chalisa.html","lingashtakam.html","om-namah-shivaya.html"]),
 ("somnath","श्री सोमनाथ ज्योतिर्लिंग","गिर सोमनाथ, गुजरात","UCT1egsvA08YcdMLiEu1DTRg","Somnath Temple - Official Channel","श्री सोमनाथ ट्रस्ट की वेबसाइट somnath.org अपने लाइव दर्शन पेज पर यही चैनल दिखाती है",
  ART["shiv"],("ॐ जय शिव ओंकारा",OM_JAI_SHIV_OMKARA,"shiv-aarti-om-jai-shiv-omkara.html"),["dwadash-jyotirlinga-stotram.html","shiv-chalisa.html","shiv-panchakshar-stotram.html"]),
 ("omkareshwar","श्री ओंकारेश्वर ज्योतिर्लिंग","खंडवा, मध्य प्रदेश","UCsIZ3yYwCW4316fPX3V-4lg","Shri Omkareshwar Jyotirlinga Official","मंदिर की वेबसाइट shriomkareshwar.org इसी चैनल का लाइव दिखाती है",
  ART["shiv"],("ॐ जय शिव ओंकारा",OM_JAI_SHIV_OMKARA,"shiv-aarti-om-jai-shiv-omkara.html"),["dwadash-jyotirlinga-stotram.html","shiv-chalisa.html"]),
 ("trimbakeshwar","श्री त्र्यंबकेश्वर ज्योतिर्लिंग","नासिक, महाराष्ट्र","UCX08UrvqI86jJpTvRMQhGQg","Trimbakeshwar Trust","त्र्यंबकेश्वर देवस्थान ट्रस्ट की वेबसाइट इसी चैनल से जुड़ी है",
  ART["shiv"],("ॐ जय शिव ओंकारा",OM_JAI_SHIV_OMKARA,"shiv-aarti-om-jai-shiv-omkara.html"),["mahamrityunjay-mantra.html","shiv-chalisa.html"]),
 ("kedarnath-badrinath","श्री केदारनाथ और बद्रीनाथ धाम","उत्तराखंड","UCfBDZKKj8GmkCSB7b8zNl_A","BKTC Official","श्री बद्रीनाथ-केदारनाथ मंदिर समिति (BKTC) की सरकारी वेबसाइट इसी चैनल से जुड़ी है",
  ART["shiv"],("ॐ जय शिव ओंकारा",OM_JAI_SHIV_OMKARA,"shiv-aarti-om-jai-shiv-omkara.html"),["shiv-chalisa.html","om-jai-jagdish-hare-aarti.html"]),
 ("siddhivinayak-mumbai","श्री सिद्धिविनायक मंदिर","मुंबई","UCF9FdiMBENIbM6jb44zWmCQ","Shree Siddhivinayak Ganapati Temple Trust","मंदिर ट्रस्ट की वेबसाइट siddhivinayak.org अपने लाइव दर्शन पेज पर यही चैनल दिखाती है",
  ART["ganesh"],("जय गणेश देवा",JAI_GANESH_DEVA,"ganesh-aarti-jai-ganesh-deva.html"),["sukhkarta-dukhharta-aarti.html","ganesh-chalisa.html","sankatnashan-ganesh-stotra.html"]),
 ("vaishno-devi","माता वैष्णो देवी","कटरा, जम्मू-कश्मीर","UCFYQr1l7ereS27SrLJ8bBtw","Shri Mata Vaishno Devi Shrine Board","श्राइन बोर्ड की आधिकारिक वेबसाइट maavaishnodevi.org इसी चैनल से जुड़ी है",
  ART["mata"],("जय अम्बे गौरी",_L.JAI_AMBE_GAURI,"jai-ambe-gauri-aarti.html"),["vaishno-mata-aarti.html","durga-chalisa.html","durga-mantra.html"]),
 ("banke-bihari-vrindavan","श्री बांके बिहारी मंदिर","वृंदावन","UCwh96MUAk0m81vEXaHVm6Ng","Thakurji Shri Banke Bihari ji","मंदिर की वेबसाइट bihariji.org अपने पेज पर इसी चैनल का लाइव दिखाती है",
  ART["krishna"],("आरती कुंजबिहारी की",_L.KUNJ_BIHARI,"aarti-kunj-bihari-ki.html"),["radha-chalisa.html","madhurashtakam.html","krishna-chalisa.html"]),
 ("tirupati-balaji","श्री वेंकटेश्वर (तिरुपति बालाजी)","तिरुमला, आंध्र प्रदेश","UCS2Y83GD-fc7qqgNW5uj41g","SVBC TTD","तिरुमला तिरुपति देवस्थानम (TTD) का अपना भक्ति चैनल SVBC",
  ART["vishnu"],("ॐ जय जगदीश हरे",OM_JAI_JAGDISH,"om-jai-jagdish-hare-aarti.html"),["vishnu-chalisa.html","shri-hari-stotram.html"]),
 ("shirdi-sai-baba","श्री साईबाबा समाधि मंदिर","शिर्डी","UCKGvJDh7g_Kzocbwy7aKicA","Shree Saibaba Sansthan Trust","साईबाबा संस्थान की आधिकारिक वेबसाइट sai.org.in इसी चैनल के वीडियो दिखाती है",
  ART["vishnu"],None,["om-jai-jagdish-hare-aarti.html","hanuman-chalisa.html"]),
 ("khatu-shyam","श्री खाटू श्याम जी","खाटू, सीकर (राजस्थान)","UCT-3fEwrrxlwMrWgMvoqt-w","श्री श्याम दर्शन - खाटूश्यामजी","श्री श्याम मंदिर की वेबसाइट shrishyammandir.com इसी चैनल का लिंक और रोज़ की लाइव आरती दिखाती है",
  ART["krishna"],("आरती कुंजबिहारी की",_L.KUNJ_BIHARI,"aarti-kunj-bihari-ki.html"),["krishna-chalisa.html","madhurashtakam.html"]),
 ("dagdusheth-ganpati-pune","श्रीमंत दगडूशेठ हलवाई गणपति","पुणे","UCFUYpQptYcTT_IKWf2GlESg","Official Shrimant Dagdusheth Halwai Ganpati Trust","ट्रस्ट की वेबसाइट dagdushethganpati.com अपने लाइव दर्शन पेज पर यही चैनल देती है",
  ART["ganesh"],("जय गणेश देवा",JAI_GANESH_DEVA,"ganesh-aarti-jai-ganesh-deva.html"),["sukhkarta-dukhharta-aarti.html","ganesh-chalisa.html"]),
 ("iskcon-vrindavan","इस्कॉन श्री कृष्ण बलराम मंदिर","वृंदावन","UCAA6IsLVfbHrP1I_lzxv09Q","ISKCON Vrindavan","iskconvrindavan.com का लाइव पेज इसी चैनल का प्रसारण दिखाता है",
  ART["krishna"],("आरती कुंजबिहारी की",_L.KUNJ_BIHARI,"aarti-kunj-bihari-ki.html"),["hare-krishna-mahamantra.html","damodarashtakam.html"]),
 ("iskcon-mayapur","इस्कॉन मायापुर (श्री राधा माधव)","मायापुर, पश्चिम बंगाल","UCypj9Vvizo4cCERfDFIG3zw","Mayapur TV","इस्कॉन मायापुर का अपना चैनल, जिस पर रोज़ की आरतियाँ लाइव आती हैं",
  ART["radha"] if "radha" in ART else ART["krishna"],("आरती कुंजबिहारी की",_L.KUNJ_BIHARI,"aarti-kunj-bihari-ki.html"),["hare-krishna-mahamantra.html","radha-kripa-kataksh-stotra.html"]),
 ("ambaji-mata","अम्बाजी माता मंदिर","बनासकांठा, गुजरात","UCUge9PCf1By7w1DEP95xXoA","Ambaji Temple Official","मंदिर की वेबसाइट ambajitemple.in अपने लाइव दर्शन पेज पर यही चैनल देती है",
  ART["mata"],("जय अम्बे गौरी",_L.JAI_AMBE_GAURI,"jai-ambe-gauri-aarti.html"),["durga-chalisa.html","durga-mantra.html"]),
 ("naina-devi","माता श्री नैना देवी जी","बिलासपुर, हिमाचल प्रदेश","UCeHrvDbvedJ6b_RPJWmQJFw","Temple Trust Shri Naina Devi Ji Official","मंदिर ट्रस्ट की वेबसाइट srinainadevi.com इसी चैनल का लाइव प्रसारण दिखाती है",
  ART["mata"],("जय अम्बे गौरी",_L.JAI_AMBE_GAURI,"jai-ambe-gauri-aarti.html"),["durga-chalisa.html","saptashloki-durga.html"]),
 ("pavagadh-mahakali","महाकाली माता मंदिर, पावागढ़","पंचमहाल, गुजरात","UCyxo14WjnjBLdCZ1k7YGRbg","Pavagadh Temple","मंदिर की वेबसाइट pavagadhtemple.in इसी चैनल से जुड़ी है",
  ART["mata"],("जय अम्बे गौरी",_L.JAI_AMBE_GAURI,"jai-ambe-gauri-aarti.html"),["kali-chalisa.html","durga-chalisa.html"]),
 ("srisailam-mallikarjuna","श्री मल्लिकार्जुन ज्योतिर्लिंग","श्रीशैलम, आंध्र प्रदेश","UCNIzL2dT2gZxQae2LHXvl0A","Srisaila Tv","श्रीशैलम देवस्थानम का अपना चैनल ‘श्रीशैल टीवी’, जिस पर रोज़ की सेवाएँ आती हैं",
  ART["shivaarti"],("ॐ जय शिव ओंकारा",OM_JAI_SHIV_OMKARA,"shiv-aarti-om-jai-shiv-omkara.html"),["dwadash-jyotirlinga-stotram.html","shiv-chalisa.html"]),
 ("haridwar-ganga-aarti","हर की पौड़ी गंगा आरती","हरिद्वार","UCKi6NnIyqlz3jBqcCQJ4b0A","Shri Ganga Sabha Reg. Haridwar","हर की पौड़ी पर गंगा आरती कराने वाली श्री गंगा सभा का अपना चैनल",
  ART["shivaarti"],("ॐ जय गंगे माता",__import__("library3").GANGA_AARTI,"ganga-aarti.html"),["ganga-chalisa.html"]),
 ("varanasi-ganga-aarti","दशाश्वमेध घाट गंगा आरती","वाराणसी","UCNDyYxUskLujzM6X3XVtXXw","Ganga Seva Nidhi","दशाश्वमेध घाट की आरती कराने वाली गंगा सेवा निधि का अपना चैनल",
  ART["shivaarti"],("ॐ जय गंगे माता",__import__("library3").GANGA_AARTI,"ganga-aarti.html"),["ganga-chalisa.html"]),
 ("golden-temple-amritsar","श्री हरमंदिर साहिब (स्वर्ण मंदिर)","अमृतसर","UCYn6UEtQ771a_OWSiNBoG8w","SGPC, Sri Amritsar","SGPC की आधिकारिक वेबसाइट sgpc.net इसी चैनल का लिंक देती है",
  ART["shivaarti"],None,[]),
]
def _uu(cid): return "UU" + cid[2:]
LIVE_JS = '''<script>(function(){[].slice.call(document.querySelectorAll(".ld-player")).forEach(function(p){
var cid=p.dataset.ch, box=p.querySelector(".ld-frame"), bts=p.querySelectorAll("[data-mode]");
function load(m){var src=m==="live"?"https://www.youtube.com/embed/live_stream?channel="+cid+"&autoplay=1&rel=0":"https://www.youtube.com/embed/videoseries?list=UU"+cid.slice(2)+"&autoplay=1&rel=0";
box.innerHTML='<iframe src="'+src+'" title="'+p.dataset.t+'" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen loading="lazy"></iframe>';
[].forEach.call(bts,function(b){b.setAttribute("aria-pressed",b.dataset.mode===m?"true":"false")});}
[].forEach.call(bts,function(b){b.addEventListener("click",function(){load(b.dataset.mode)})});
var st=p.querySelector(".ld-start"); if(st) st.addEventListener("click",function(){load("recent")});
});})();</script>'''
def ld_player(cid, title, art):
    return (f'<div class="ld-player" data-ch="{cid}" data-t="{e(title)}"><div class="ld-frame">'
            f'<img src="https://i.ytimg.com/vi/{art[0]}/hqdefault.jpg" alt="" width="480" height="360" loading="lazy">'
            f'<button class="ld-start" aria-label="{e(title)} — लाइव दर्शन शुरू करें"><span>▶ लाइव दर्शन शुरू करें</span></button></div>'
            '<div class="ld-modes" role="group" aria-label="क्या देखें"><button class="chip" data-mode="live" aria-pressed="false">अभी लाइव</button>'
            '<button class="chip" data-mode="recent" aria-pressed="false">हाल के दर्शन और आरती</button></div>'
            '<p class="ld-hint">अगर मंदिर से अभी प्रसारण नहीं हो रहा है, तो ‘हाल के दर्शन और आरती’ दबाएँ — मंदिर के चैनल के सबसे नए वीडियो चलेंगे।</p></div>')

# ---- one page for all temples: picker on top, a single player, the matching aarti below ----
_BH = {d[1]: [v for v in d[6] if v in V] for d in DEITY}
_TEMPLE_BH = {"khatu-shyam":"krishna","dagdusheth-ganpati-pune":"ganesh","iskcon-vrindavan":"krishna","iskcon-mayapur":"krishna","ambaji-mata":"mata","naina-devi":"mata","pavagadh-mahakali":"mata","ram-mandir-ayodhya":"ram","siddhivinayak-mumbai":"ganesh","vaishno-devi":"mata","banke-bihari-vrindavan":"krishna","tirupati-balaji":"krishna","shirdi-sai-baba":"ram"}
import json as _json, os as _os
# Our own bhajan MP3s (no ads): {"shiv":[{"t":"title","f":"url"}], "ram":[...], ...}. Empty -> YouTube player fallback.
AUD = next((_json.load(open(_p, encoding="utf-8")) for _p in ("audio_bhajan.json", "src/audio_bhajan.json") if _os.path.exists(_p)), {})
def _aud(slug):
    if slug == "golden-temple-amritsar": return ""
    l = AUD.get("_temples", {}).get(slug) or AUD.get(_TEMPLE_BH.get(slug, "shiv")) or AUD.get("_all", [])
    return e(_json.dumps(l, ensure_ascii=False)) if l else ""
_SHIV = ["vsfjF59qj4Q","Kbe3pbLsg1U","DGsy57lUApA","pn5OODJqmTc","fQiD96yFR6o","sllSUVgfjnw","ZqFztNyxSgU","qCwFf_cCWGM","6vVDsn9R6DM","dZ7iceOQt9Y","JUg809TxgRg","icIEKo5vLjw"]
_RAM = ["sLQF1nm_RqU","lBRP9bTTLek","kHM8fGmqoLw","l9z2J0I6Kao","fmbCXi2K9tw","pCixItfj5Vo","ZqOnkb7zElU"]
_GAN = ["ZswQ9qUMDTs","NGI-JiRiwSc","XscYggWHC5o","EtnvDW1AlOY","Qpe4rrfzWhk","IkcVwmMUUmw","BmrflIPOqAk","r-yfzKxNW0w","u3kbBEHOs9o"]
_MATA = ["NuWOBRQ9B3Q","woNhYRu376g","fhm1dqyttu0","2yVR5zSaKpc","9hzay6Ebzas","rLSpMEkB7eU","vr5Bp46iA-Q","PSKXIFYrtcU","CcDzHzu7sIw","jAdixB5m0Zo"]
_KRI = ["TVdX5XbbjHs","_8yw36Jn7iM","P9N1XQzw8CI","vy6ucthmxmk","ZIhDdYk6Gus","ZQ_OBR-596M","GtRRHlLc5gQ"]
def _first(lead, base): return lead + [x for x in base if x not in lead]
# Hand-picked OmKiran Bhakti tracks for each temple: the temple's own song first, then that deity's bhajans.
TEMPLE_TRACKS = {
 "mahakaleshwar-ujjain": _first(["axKgdxe7JZE","icIEKo5vLjw"], _SHIV), "kashi-vishwanath-varanasi": _first(["dZ7iceOQt9Y","Kbe3pbLsg1U"], _SHIV),
 "srisailam-mallikarjuna": _first(["DGsy57lUApA"], _SHIV), "haridwar-ganga-aarti": _SHIV, "varanasi-ganga-aarti": _first(["dZ7iceOQt9Y"], _SHIV), "golden-temple-amritsar": [],
 "kal-bhairav-ujjain": _first(["unfGUJz6D8U","axKgdxe7JZE"], _SHIV), "somnath": _SHIV, "omkareshwar": _first(["C5lE4JA3sKc"], _SHIV),
 "trimbakeshwar": _SHIV, "kedarnath-badrinath": _first(["DGsy57lUApA"], _SHIV),
 "ram-mandir-ayodhya": _RAM, "shirdi-sai-baba": _first(["iUo6Ui1lPMY","96GJOWJFJgA"], _RAM),
 "siddhivinayak-mumbai": _GAN, "dagdusheth-ganpati-pune": _first(["oiQLsZFwU7I","ZZcOOWNvFg8","Qpe4rrfzWhk"], _GAN),
 "vaishno-devi": _first(["PHNyA0VlAI8"], _MATA), "ambaji-mata": _first(["dJAZTUkHcBs"], _MATA), "naina-devi": _first(["PSKXIFYrtcU","PHNyA0VlAI8"], _MATA),
 "pavagadh-mahakali": _first(["jAdixB5m0Zo","nFvgYHuqZt0"], _MATA),
 "banke-bihari-vrindavan": _KRI, "khatu-shyam": _first(["EE2zjTPyHaI"], _KRI), "iskcon-vrindavan": _first(["GtRRHlLc5gQ","P9N1XQzw8CI"], _KRI),
 "iskcon-mayapur": _first(["GtRRHlLc5gQ","P9N1XQzw8CI"], _KRI), "tirupati-balaji": _first(["P9N1XQzw8CI","GtRRHlLc5gQ"], _KRI),
}
def _bh(slug):
    if slug in TEMPLE_TRACKS and not TEMPLE_TRACKS[slug]: return ""
    if slug in TEMPLE_TRACKS: return ",".join(x for x in TEMPLE_TRACKS[slug] if x in V)
    ids = _BH.get(_TEMPLE_BH.get(slug, "shiv"), []) or home_popular
    return ",".join(ids[:12])
_cards, _aartis, _seen = [], [], {}
for i, (slug, name, place, cid, cname, note, art, aarti, rel) in enumerate(LIVE):
    akey = aarti[2] if aarti else ""
    if aarti and akey not in _seen:
        _seen[akey] = len(_seen)
        at, verses, au = aarti
        _aartis.append(f'<div class="ld-aarti" data-a="{akey}" data-t="{e(at)}" hidden><div class="lyrics">{lyrics_body(verses)}</div>'
                       f'<p style="margin-top:.6rem"><a class="btn ghost" href="{au}">अर्थ सहित पढ़ें</a></p></div>')
    _cards.append(f'<li><button type="button" class="ld-pick" data-slug="{slug}" data-ch="{cid}" data-name="{e(name)}" data-place="{e(place)}" '
                  f'data-src="{e(cname)}" data-note="{e(note)}" data-a="{akey}" data-bh="{_bh(slug)}" data-aud="{_aud(slug)}" aria-pressed="{"true" if i == 0 else "false"}">'
                  f'<span class="ld-thumb"><img src="img/live/sm/{slug}.webp" alt="" loading="lazy" width="300" height="300"></span>'
                  f'<strong>{e(name)}</strong><small>{e(place)}</small></button></li>')
_first = LIVE[0]
LIVE_ONE_JS = r"""<script>document.addEventListener("DOMContentLoaded",function(){
var picks=[].slice.call(document.querySelectorAll(".ld-pick")),box=document.querySelector(".ld-frame"),mode="live",cur=null;
var bh=document.getElementById("ld-bh"),bhw={};
var nm=document.getElementById("ld-name"),src=document.getElementById("ld-src"),aar=[].slice.call(document.querySelectorAll(".ld-aarti"));
function play(m){mode=m;if(!cur)return;var cid=cur.dataset.ch;
 var u=m==="live"?"https://www.youtube.com/embed/live_stream?channel="+cid+"&autoplay=1&mute=1&rel=0&cc_load_policy=0&iv_load_policy=3":"https://www.youtube.com/embed/videoseries?list=UU"+cid.slice(2)+"&autoplay=1&mute=1&rel=0&cc_load_policy=0&iv_load_policy=3";
 box.innerHTML='<iframe src="'+u+'" title="'+cur.dataset.name+' लाइव दर्शन" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>';
 [].forEach.call(document.querySelectorAll("[data-mode]"),function(b){b.setAttribute("aria-pressed",b.dataset.mode===m?"true":"false")});
 bhajan();}
function bhajan(){var au=document.getElementById("ld-aud");if(cur.dataset.aud&&window.okbAudio&&au){okbAudio(au,JSON.parse(cur.dataset.aud));}var ids=(cur.dataset.bh||"").split(",").filter(Boolean);if(!ids.length){bhw.hidden=false;return;}
 bh.innerHTML='<iframe src="https://www.youtube.com/embed/'+ids[0]+'?autoplay=1&mute=1&rel=0&cc_load_policy=0&iv_load_policy=3&playlist='+ids.slice(1).join(",")+'" title="OmKiran Bhakti भजन" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>';
 bhw.hidden=false;}
function pick(b,start){cur=b;picks.forEach(function(x){x.setAttribute("aria-pressed",x===b?"true":"false")});
 nm.textContent=b.dataset.name+", "+b.dataset.place;src.textContent="स्रोत: मंदिर का आधिकारिक YouTube चैनल “"+b.dataset.src+"” — "+b.dataset.note+"। वीडियो के सभी अधिकार उन्हीं के हैं।";
 var ta="";aar.forEach(function(a){var on=a.dataset.a===b.dataset.a;a.hidden=!on;if(on)ta=a.dataset.t});var al=document.getElementById("ld-aline");al.hidden=!ta;document.getElementById("ld-atitle").textContent=ta;
 try{history.replaceState(null,"","#"+b.dataset.slug)}catch(e){}
 if(start)play("recent");else{box.innerHTML='<button class="ld-start" type="button"><span>▶ '+b.dataset.name+' — दर्शन शुरू करें</span></button>';box.querySelector(".ld-start").addEventListener("click",function(){play("recent")});}}
picks.forEach(function(b){b.addEventListener("click",function(){pick(b,true);document.querySelector(".ld-player").scrollIntoView({behavior:"smooth",block:"start"})})});
[].forEach.call(document.querySelectorAll("[data-mode]"),function(b){b.addEventListener("click",function(){play(b.dataset.mode)})});
var h=(location.hash||"").slice(1),hit=picks.filter(function(p){return p.dataset.slug===h})[0],first=hit||picks[0];pick(first,!!hit);if(hit)document.querySelector(".ld-player").scrollIntoView({block:"start"});
});</script>"""
_faqs = [("मंदिरों के लाइव दर्शन कहाँ देखें?", "इसी पेज पर ऊपर से मंदिर चुनें — राम मंदिर अयोध्या, महाकाल उज्जैन, काशी विश्वनाथ, सोमनाथ, ओंकारेश्वर, त्र्यंबकेश्वर, केदारनाथ-बद्रीनाथ, सिद्धिविनायक, वैष्णो देवी, बांके बिहारी, तिरुपति, शिर्डी, खाटू श्याम, दगडूशेठ गणपति, इस्कॉन वृंदावन, इस्कॉन मायापुर, अम्बाजी, नैना देवी, पावागढ़ महाकाली, श्रीशैलम मल्लिकार्जुन, हरिद्वार और काशी की गंगा आरती तथा स्वर्ण मंदिर अमृतसर का आधिकारिक प्रसारण यहीं चलता है।"),
         ("लाइव प्रसारण न दिखे तो क्या करें?", "मंदिर आरती और विशेष अवसरों पर लाइव आते हैं। इसलिए पेज खुलते ही उसी मंदिर के चैनल के सबसे नए दर्शन-आरती वीडियो चलते हैं; प्रसारण चल रहा हो तो ‘अभी लाइव देखें’ दबाएँ।"),
         ("क्या ये प्रसारण आधिकारिक हैं?", "हाँ। केवल वही YouTube चैनल लिए गए हैं जिन्हें मंदिर की अपनी वेबसाइट दिखाती है या जो मंदिर ट्रस्ट के नाम से चलते हैं। वीडियो और प्रसारण पूरी तरह मंदिरों के हैं; OmKiran Bhakti उन्हें YouTube के प्लेयर से यहाँ दिखाता है।")]
add("live-darshan.html", f"लाइव दर्शन — राम मंदिर, महाकाल, खाटू श्याम समेत {len(LIVE)} मंदिर | OmKiran Bhakti",
    f"राम मंदिर, महाकाल, काशी विश्वनाथ, खाटू श्याम, दगडूशेठ, वैष्णो देवी, बांके बिहारी, इस्कॉन वृंदावन, तिरुपति — {len(LIVE)} मंदिरों के आधिकारिक लाइव दर्शन एक ही पेज पर, साथ में आरती।",
    band("मंदिरों के लाइव दर्शन", f"भारत के {len(LIVE)} प्रमुख मंदिरों का <strong>आधिकारिक</strong> लाइव प्रसारण एक ही जगह। मंदिर चुनें — दर्शन यहीं चलेगा, साथ में आरती पढ़ें और भजन सुनें।", "लाइव दर्शन", *ART["shivaarti"], "लाइव दर्शन") +
    f'<section><div class="wrap"><ul class="ld-picks" role="list">{"".join(_cards)}</ul>'
    f'<div class="ld-player"><h2 id="ld-name" class="ld-name">{e(_first[1])}, {e(_first[2])}</h2><div class="ld-frame"></div>'
    '<div class="ld-modes" role="group" aria-label="क्या देखें"><button class="chip" data-mode="recent" aria-pressed="false">दर्शन और आरती</button>'
    '<button class="chip live-chip" data-mode="live" aria-pressed="false"><span class="lv-dot" aria-hidden="true"></span>अभी लाइव देखें</button></div>'
    f'<details class="ld-aline" id="ld-aline"><summary>📖 साथ में पढ़ें: <b id="ld-atitle"></b></summary>{"".join(_aartis)}</details>'
    '<div class="ok-card"><div class="ok-yt" id="ld-bh"></div><div class="ok-msg"><b>🙏 OmKiran Bhakti में आपका स्वागत है</b><p>दर्शन के साथ हमारे भजन सुनिए। रोज़ नए भजन, आरती और मंत्र के लिए चैनल से जुड़िए।</p><a class="ok-sub" href="https://www.youtube.com/@OmKiranBhakti?sub_confirmation=1" target="_blank" rel="noopener">▶ Subscribe करें</a></div></div>'
    '<div class="bh-aud" id="ld-aud"></div>'
    '<p class="note" id="ld-src"></p></div></div></section>'
    + faq_html(_faqs) + LIVE_ONE_JS,
    crumbs="लाइव दर्शन", ld=[faq_ld(_faqs)], active="aarti-mantra.html")

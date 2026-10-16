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
]
def _uu(cid): return "UU" + cid[2:]
LIVE_JS = '''<script>(function(){[].slice.call(document.querySelectorAll(".ld-player")).forEach(function(p){
var cid=p.dataset.ch, box=p.querySelector(".ld-frame"), bts=p.querySelectorAll("[data-mode]");
function load(m){var src=m==="live"?"https://www.youtube.com/embed/live_stream?channel="+cid+"&autoplay=1&rel=0":"https://www.youtube.com/embed/videoseries?list=UU"+cid.slice(2)+"&autoplay=1&rel=0";
box.innerHTML='<iframe src="'+src+'" title="'+p.dataset.t+'" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen loading="lazy"></iframe>';
[].forEach.call(bts,function(b){b.setAttribute("aria-pressed",b.dataset.mode===m?"true":"false")});}
[].forEach.call(bts,function(b){b.addEventListener("click",function(){load(b.dataset.mode)})});
var st=p.querySelector(".ld-start"); if(st) st.addEventListener("click",function(){load("live")});
});})();</script>'''
def ld_player(cid, title, art):
    return (f'<div class="ld-player" data-ch="{cid}" data-t="{e(title)}"><div class="ld-frame">'
            f'<img src="https://i.ytimg.com/vi/{art[0]}/hqdefault.jpg" alt="" width="480" height="360" loading="lazy">'
            f'<button class="ld-start" aria-label="{e(title)} — लाइव दर्शन शुरू करें"><span>▶ लाइव दर्शन शुरू करें</span></button></div>'
            '<div class="ld-modes" role="group" aria-label="क्या देखें"><button class="chip" data-mode="live" aria-pressed="false">अभी लाइव</button>'
            '<button class="chip" data-mode="recent" aria-pressed="false">हाल के दर्शन और आरती</button></div>'
            '<p class="ld-hint">अगर मंदिर से अभी प्रसारण नहीं हो रहा है, तो ‘हाल के दर्शन और आरती’ दबाएँ — मंदिर के चैनल के सबसे नए वीडियो चलेंगे।</p></div>')
def _ttl2(slug):
    t = PAGES[slug].split("<title>")[1].split("</title>")[0] if slug in PAGES else None
    return html.unescape(t.split(" | ")[0]) if t else None
LIVE_PAGES = []
for slug, name, place, cid, cname, note, art, aarti, rel in LIVE:
    page_slug = f"live-darshan-{slug}.html"
    ans = (f"{name}, {place} के <strong>लाइव दर्शन</strong> यहीं देखें। प्रसारण मंदिर के अपने YouTube चैनल <strong>“{e(cname)}”</strong> से है, जो YouTube के प्लेयर में चलता है — "
           "दर्शन मंदिर का है और व्यू भी उन्हीं के चैनल पर गिने जाते हैं।")
    rel_li = "".join(f'<li><a href="{u}"><strong>{e(_ttl2(u).split(" — ")[0])}</strong><span>{e(" — ".join(_ttl2(u).split(" — ")[1:]) or "पढ़ें")}</span></a></li>' for u in rel if _ttl2(u))
    aarti_html = ""
    if aarti:
        at, verses, au = aarti
        aarti_html = (f'<section class="band"><div class="wrap">{sec_head(f"दर्शन के साथ पढ़ें — {at}","आरती के समय वीडियो चलाकर साथ में गाएँ")}'
                      f'<details class="ld-aarti" open><summary>{e(at)} — पूरे बोल</summary><div class="lyrics">{lyrics_body(verses)}</div></details>'
                      f'<p style="margin-top:1rem"><a class="btn ghost" href="{au}">अर्थ सहित पढ़ें (पाठ मोड)</a></p></div></section>')
    faqs = [(f"{name} के लाइव दर्शन कहाँ देखें?", f"इसी पेज पर — मंदिर के आधिकारिक YouTube चैनल “{cname}” का प्रसारण यहाँ चलता है। {note}।"),
            ("लाइव प्रसारण न दिखे तो क्या करें?", "मंदिर हर समय प्रसारण नहीं करता; आरती और विशेष अवसरों पर लाइव आता है। उस समय ‘हाल के दर्शन और आरती’ दबाएँ — चैनल के सबसे नए वीडियो चलेंगे।"),
            ("क्या यह प्रसारण OmKiran Bhakti का है?", f"नहीं। वीडियो और प्रसारण पूरी तरह मंदिर के चैनल “{cname}” का है; OmKiran Bhakti सिर्फ़ YouTube के प्लेयर से उसे इस पेज पर दिखाता है ताकि भक्त दर्शन के साथ आरती भी पढ़ सकें।")]
    body = (band(f"{name} लाइव दर्शन", ans, f"{name} लाइव दर्शन", *art, name,
                 extra='<p class="lede"><a href="live-darshan.html">दूसरे मंदिरों के लाइव दर्शन</a></p>') +
            f'<section><div class="wrap">{ld_player(cid, name + " लाइव दर्शन", art)}'
            f'<p class="note">स्रोत: मंदिर का आधिकारिक YouTube चैनल “{e(cname)}” — {e(note)}। वीडियो के सभी अधिकार उन्हीं के हैं।</p></div></section>'
            + aarti_html +
            (f'<section><div class="wrap">{sec_head("और पाठ")}<ul class="library">{rel_li}</ul></div></section>' if rel_li else "")
            + faq_html(faqs) + LIVE_JS)
    add(page_slug, f"{name} लाइव दर्शन — {place} | OmKiran Bhakti" if len(f"{name} लाइव दर्शन — {place} | OmKiran Bhakti") <= 95 else f"{name} लाइव दर्शन | OmKiran Bhakti",
        f"{name} ({place}) के लाइव दर्शन और आरती — मंदिर के आधिकारिक YouTube चैनल से, साथ में आरती के पूरे बोल पढ़ें।"[:160],
        body, crumbs=f"{name} लाइव दर्शन", ld=[faq_ld(faqs)], active="aarti-mantra.html")
    LIVE_PAGES.append((page_slug, name, place, art))
grid = "".join(f'<li><a href="{s}">{arch(*a, alt="")}<div><strong>{e(n)}</strong><span>{e(p)}</span></div></a></li>' for s, n, p, a in LIVE_PAGES)
_faqs = [("मंदिरों के लाइव दर्शन कहाँ देखें?", "इस पेज से मंदिर चुनें — राम मंदिर अयोध्या, महाकाल उज्जैन, काशी विश्वनाथ, सोमनाथ, सिद्धिविनायक, वैष्णो देवी, बांके बिहारी, तिरुपति और शिर्डी समेत 12 मंदिरों का आधिकारिक प्रसारण यहीं चलता है।"),
         ("क्या ये प्रसारण आधिकारिक हैं?", "हाँ, हमने केवल वही YouTube चैनल लिए हैं जिन्हें मंदिर की अपनी वेबसाइट दिखाती है या जो मंदिर ट्रस्ट के नाम से चलते हैं। नकली ‘लाइव’ चैनल शामिल नहीं किए गए।")]
add("live-darshan.html", "लाइव दर्शन — राम मंदिर, महाकाल, काशी विश्वनाथ, सोमनाथ और 12 मंदिर | OmKiran Bhakti",
    "राम मंदिर अयोध्या, महाकाल उज्जैन, काशी विश्वनाथ, सोमनाथ, सिद्धिविनायक, वैष्णो देवी, बांके बिहारी, तिरुपति, शिर्डी — 12 मंदिरों के आधिकारिक लाइव दर्शन एक जगह, साथ में आरती।",
    band("मंदिरों के लाइव दर्शन", "भारत के प्रमुख मंदिरों का <strong>आधिकारिक</strong> लाइव प्रसारण एक जगह। हर प्रसारण मंदिर के अपने YouTube चैनल से है; मंदिर चुनें और दर्शन के साथ आरती भी पढ़ें।", "लाइव दर्शन", *ART["shivaarti"], "लाइव दर्शन") +
    f'<section><div class="wrap"><ul class="paath">{grid}</ul>'
    '<p class="note">केवल आधिकारिक चैनल शामिल हैं — जिनसे मंदिर की अपनी वेबसाइट जुड़ी है या जो मंदिर ट्रस्ट के नाम से चलते हैं। प्रसारण का समय मंदिर तय करता है।</p></div></section>' + faq_html(_faqs),
    crumbs="लाइव दर्शन", ld=[faq_ld(_faqs)], active="aarti-mantra.html")

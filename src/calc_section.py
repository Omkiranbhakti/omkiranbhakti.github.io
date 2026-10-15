# जन्म तिथि / राशि / नाम अक्षर calculator page (client-side, janm.js + astronomy-engine).
_AK = [["चु","चे","चो","ला"],["ली","लू","ले","लो"],["अ","ई","उ","ए"],["ओ","वा","वी","वू"],["वे","वो","का","की"],["कु","घ","ङ","छ"],["के","को","हा","ही"],["हु","हे","हो","डा"],["डी","डू","डे","डो"],["मा","मी","मू","मे"],["मो","टा","टी","टू"],["टे","टो","पा","पी"],["पू","ष","ण","ठ"],["पे","पो","रा","री"],["रू","रे","रो","ता"],["ती","तू","ते","तो"],["ना","नी","नू","ने"],["नो","या","यी","यू"],["ये","यो","भा","भी"],["भू","धा","फा","ढा"],["भे","भो","जा","जी"],["खी","खू","खे","खो"],["गा","गी","गू","गे"],["गो","सा","सी","सू"],["से","सो","दा","दी"],["दू","थ","झ","ञ"],["दे","दो","चा","ची"]]
_NK = ["अश्विनी","भरणी","कृत्तिका","रोहिणी","मृगशिरा","आर्द्रा","पुनर्वसु","पुष्य","आश्लेषा","मघा","पूर्वा फाल्गुनी","उत्तरा फाल्गुनी","हस्त","चित्रा","स्वाति","विशाखा","अनुराधा","ज्येष्ठा","मूल","पूर्वाषाढ़ा","उत्तराषाढ़ा","श्रवण","धनिष्ठा","शतभिषा","पूर्वा भाद्रपद","उत्तरा भाद्रपद","रेवती"]
_RS = ["मेष","वृषभ","मिथुन","कर्क","सिंह","कन्या","तुला","वृश्चिक","धनु","मकर","कुंभ","मीन"]
def _pr(n, p): return _RS[int(((n * 4 + p) * (360 / 108) + 0.001) // 30)]
ak_rows = "".join(f'<tr><td><strong>{_NK[n]}</strong></td><td>{" ".join(_AK[n])}</td><td>{" / ".join(dict.fromkeys(_pr(n, p) for p in range(4)))}</td></tr>' for n in range(27))
rs_rows = "".join(f'<tr><td><strong>{r}</strong></td><td>{", ".join(_AK[n][p] for n in range(27) for p in range(4) if _pr(n, p) == r)}</td></tr>' for r in _RS)
_jv = hashlib.md5(open(os.path.join(ROOT, "janm.js"), "rb").read()).hexdigest()[:8]
TZ_OPTS = [("5.5","भारत (IST)"),("5.75","नेपाल"),("4","दुबई (UAE)"),("3","सऊदी/क़तर"),("8","सिंगापुर/मलेशिया"),("0","UK — सर्दी (GMT)"),("1","UK — गर्मी (BST)"),
           ("-4","USA पूर्वी — गर्मी (EDT)"),("-5","USA पूर्वी — सर्दी (EST)"),("-6","USA मध्य — सर्दी (CST)"),("-7","USA पश्चिमी — गर्मी (PDT)"),("-8","USA पश्चिमी — सर्दी (PST)"),
           ("10","ऑस्ट्रेलिया (सिडनी) — सर्दी"),("11","ऑस्ट्रेलिया (सिडनी) — गर्मी"),("12","न्यूज़ीलैंड"),("-3","कनाडा/ब्राज़ील (-3)")]
tz_html = "".join(f'<option value="{v}">{l}</option>' for v, l in TZ_OPTS)
form = f'''<form class="jcalc no-print" id="jcalc" onsubmit="return false">
<div class="jrow"><label>जन्म की तारीख़<input type="date" id="j-date" required min="1900-01-01" max="2100-12-31"></label>
<label>जन्म का समय<input type="time" id="j-time" value="12:00"></label>
<label>कहाँ जन्म हुआ<select id="j-tz">{tz_html}</select></label></div>
<label class="jchk"><input type="checkbox" id="j-notime"> जन्म का समय नहीं पता</label>
<button class="btn" id="j-go" type="submit">तिथि और राशि निकालें</button>
</form>
<div id="j-out" class="jout" aria-live="polite" hidden></div>'''
name_form = '''<form class="jcalc no-print" id="ncalc" onsubmit="return false"><div class="jrow"><label>नाम (हिंदी में)<input type="text" id="n-name" placeholder="जैसे राहुल, प्रिया, श्रेया" autocomplete="off"></label></div>
<button class="btn ghost" id="n-go" type="submit">नाम से राशि देखें</button></form><div id="n-out" class="jout" aria-live="polite" hidden></div>'''
JS = f'''<script src="https://cdn.jsdelivr.net/npm/astronomy-engine@2.1.19/astronomy.browser.min.js"></script><script src="janm.js?v={_jv}"></script>
<script>(function(){{
var $=function(i){{return document.getElementById(i)}}, MON=["जनवरी","फ़रवरी","मार्च","अप्रैल","मई","जून","जुलाई","अगस्त","सितंबर","अक्टूबर","नवंबर","दिसंबर"], WD=["रविवार","सोमवार","मंगलवार","बुधवार","गुरुवार","शुक्रवार","शनिवार"];
function hd(d){{return d.getUTCDate()+" "+MON[d.getUTCMonth()]+" "+d.getUTCFullYear()+", "+WD[d.getUTCDay()]}}
function row(k,v){{return "<tr><th>"+k+"</th><td>"+v+"</td></tr>"}}
$("j-notime").addEventListener("change",function(){{$("j-time").disabled=this.checked}});
$("jcalc").addEventListener("submit",function(){{
  var dv=$("j-date").value; if(!dv){{$("j-date").focus();return}}
  if(!window.Janm||!window.Astronomy){{$("j-out").hidden=false;$("j-out").textContent="कैलकुलेटर लोड नहीं हुआ — इंटरनेट जाँचकर पेज दोबारा खोलें।";return}}
  var tm=$("j-notime").checked?"12:00":($("j-time").value||"12:00"), off=parseFloat($("j-tz").value);
  var p=dv.split("-"), q=tm.split(":"), t=new Date(Date.UTC(+p[0],+p[1]-1,+p[2],+q[0],+q[1])-off*3600e3);
  var b=Janm.birth(t), nx=Janm.nextTithiBirthday(b,new Date(),2);
  var ak=b.allAkshar.map(function(s,i){{return i===b.pada-1?"<mark>"+s+"</mark>":s}}).join(" ");
  var h="<h3>आपका जन्म "+b.paksha+" पक्ष की "+b.tithi+" को हुआ</h3><table class=\\"ptable jt\\"><tbody>"+
   row("हिंदू तिथि",b.purnimanta+" मास, "+b.paksha+" पक्ष, "+b.tithi+(b.adhik?" (अधिक मास)":"")+(b.purnimanta!==b.amanta?" <small>(अमांत पंचांग में: "+b.amanta+")</small>":""))+
   row("विक्रम संवत",b.vikram)+row("जन्म नक्षत्र",b.nakshatra+", "+["पहला","दूसरा","तीसरा","चौथा"][b.pada-1]+" चरण"+(b.gandmool?" <small>— गंडमूल नक्षत्र (<a href=\\"gandmool-nakshatra.html\\">जानें</a>)</small>":""))+
   row("राशि (चंद्र राशि)",b.rashi+" <small>— स्वामी ग्रह "+b.rashiLord+"</small>")+row("नाम के शुभ अक्षर",ak+" <small>— चरण के अनुसार पहला अक्षर: <strong>"+b.akshar+"</strong></small>")+
   row("सूर्य राशि",b.suryaRashi)+row("गण / नाड़ी",b.gan+" गण, "+b.nadi+" नाड़ी")+
   (nx.length?row("आपका तिथि वाला जन्मदिन",nx.map(hd).join("<br>")):"")+"</tbody></table>"+
   ($("j-notime").checked?"<p class=\\"note\\">समय न पता होने पर दोपहर 12 बजे का हिसाब लगाया है। नक्षत्र और कभी-कभी तिथि दिन में बदल सकती है — सही नतीजे के लिए जन्म का समय डालें।</p>":"")+
   "<p><a class=\\"btn pe-share\\" target=\\"_blank\\" rel=\\"noopener\\" href=\\"https://wa.me/?text="+encodeURIComponent("मेरा जन्म "+b.purnimanta+" "+b.paksha+" "+b.tithi+" को, "+b.nakshatra+" नक्षत्र, "+b.rashi+" राशि में हुआ। आप भी अपनी जन्म तिथि और राशि जानें: "+location.href.split("#")[0])+"\\">WhatsApp पर भेजें</a></p>";
  $("j-out").innerHTML=h;$("j-out").hidden=false;$("j-out").scrollIntoView({{behavior:"smooth",block:"start"}});
}});
$("ncalc").addEventListener("submit",function(){{
  var r=window.Janm&&Janm.nameRashi($("n-name").value);$("n-out").hidden=false;
  $("n-out").innerHTML=r?("<p class=\\"answer\\"><strong>"+$("n-name").value.trim()+"</strong> नाम का पहला अक्षर <strong>‘"+r.syllable+"’</strong> है: "+r.nakshatra+" नक्षत्र का "+["पहला","दूसरा","तीसरा","चौथा"][r.pada-1]+" चरण — <strong>"+r.rashi+" राशि</strong> (स्वामी "+r.rashiLord+")।</p><p class=\\"note\\">नाम से निकली राशि केवल अनुमान है; असली राशि जन्म के समय चंद्रमा की स्थिति से तय होती है — ऊपर का कैलकुलेटर देखें।</p>"):"<p>नाम हिंदी (देवनागरी) में लिखें, जैसे ‘राहुल’।</p>";
}});
}})();</script>'''
_ans = ("अपनी जन्म की तारीख़ और समय डालें — यह टूल बताएगा कि आपका जन्म किस <strong>हिंदू तिथि</strong> (पक्ष और महीने सहित) को हुआ, आपका <strong>जन्म नक्षत्र</strong>, "
        "<strong>चंद्र राशि</strong>, नाम के <strong>शुभ अक्षर</strong>, गण-नाड़ी, और इस साल आपका <strong>तिथि वाला जन्मदिन</strong> किस तारीख़ को पड़ेगा।")
_faqs = [("जन्म तिथि कैसे पता करें?", "जन्म की अंग्रेज़ी तारीख़ और समय ऊपर के कैलकुलेटर में डालें; यह उसी पल के सूर्य और चंद्रमा की स्थिति से हिंदू तिथि, पक्ष और महीना निकालता है।"),
         ("जन्म तारीख़ से राशि कैसे जानें?", "वैदिक ज्योतिष में राशि वह है जिसमें जन्म के समय चंद्रमा था (चंद्र राशि)। कैलकुलेटर लाहिड़ी अयनांश से चंद्रमा की स्थिति निकालकर राशि और नक्षत्र बताता है।"),
         ("नक्षत्र से नाम का अक्षर कैसे निकालते हैं?", "हर नक्षत्र के चार चरण होते हैं और हर चरण का एक अक्षर तय है (जैसे रोहिणी: ओ, वा, वी, वू)। जन्म जिस चरण में हुआ, उसी अक्षर से नाम रखना शुभ माना जाता है। पूरी सूची नीचे तालिका में है।"),
         ("तिथि वाला जन्मदिन क्या है?", "बहुत से परिवार जन्मदिन अंग्रेज़ी तारीख़ की जगह हिंदू तिथि पर मनाते हैं — उसी महीने, उसी पक्ष की उसी तिथि को। यह हर साल अलग अंग्रेज़ी तारीख़ पर पड़ता है; कैलकुलेटर अगले दो साल की तारीख़ बताता है।"),
         ("नाम से राशि कैसे पता करें?", "नाम के पहले अक्षर को नक्षत्र-चरण की सूची से मिलाया जाता है — जैसे ‘रा’ चित्रा नक्षत्र में आता है, इसलिए राहुल की नाम-राशि तुला है। यह केवल अनुमान है; असली राशि जन्म-समय से तय होती है।"),
         ("क्या यह कैलकुलेटर मुफ़्त है और मेरी जानकारी कहीं जाती है?", "हाँ, पूरी तरह मुफ़्त है। सारी गणना आपके फ़ोन या कंप्यूटर पर ही होती है; तारीख़ या नाम कहीं भेजा या सेव नहीं किया जाता।")]
_body = (band("जन्म तिथि, राशि और नाम अक्षर कैलकुलेटर", _ans, "जन्म तिथि कैलकुलेटर", *ART["krishna"], "जन्म तिथि") +
         f'<section><div class="wrap">{sec_head("अपनी जन्म तिथि और राशि जानें","सारी गणना आपके फ़ोन पर ही होती है — कुछ भी सेव नहीं होता")}{form}</div></section>'
         f'<section class="band"><div class="wrap">{sec_head("नाम से राशि जानें")}{name_form}</div></section>'
         f'<section><div class="wrap">{sec_head("नक्षत्र के अनुसार नाम के अक्षर","27 नक्षत्र, हर चरण का एक अक्षर")}<div class="tbl"><table class="ptable"><thead><tr><th>नक्षत्र</th><th>चरण 1–4 के अक्षर</th><th>राशि</th></tr></thead><tbody>{ak_rows}</tbody></table></div></div></section>'
         f'<section class="band"><div class="wrap">{sec_head("राशि के अनुसार नाम के अक्षर")}<div class="tbl"><table class="ptable"><thead><tr><th>राशि</th><th>नाम के अक्षर</th></tr></thead><tbody>{rs_rows}</tbody></table></div>'
         '<p class="note">गणना का तरीका: सूर्य और चंद्रमा की स्थिति (astronomy-engine), लाहिड़ी अयनांश, अमांत/पूर्णिमांत महीना — यही तरीका इस साइट के रोज़ के पंचांग में है।</p></div></section>'
         + faq_html(_faqs) + JS)
add("janm-tithi-rashi-calculator.html", "जन्म तिथि, राशि और नाम अक्षर कैलकुलेटर — जन्म तारीख़ से हिंदू तिथि जानें | OmKiran Bhakti",
    "जन्म की तारीख़ और समय डालकर जानें: हिंदू जन्म तिथि, पक्ष, महीना, नक्षत्र, चंद्र राशि, नाम के शुभ अक्षर और इस साल का तिथि वाला जन्मदिन। नाम से राशि भी — मुफ़्त।",
    _body, crumbs="जन्म तिथि कैलकुलेटर",
    ld=[{"@type":"WebApplication","name":"जन्म तिथि, राशि और नाम अक्षर कैलकुलेटर","applicationCategory":"LifestyleApplication","operatingSystem":"Any","inLanguage":"hi",
         "offers":{"@type":"Offer","price":"0","priceCurrency":"INR"},"url":SITE+"janm-tithi-rashi-calculator.html","publisher":{"@id":SITE+"#organization"}}, faq_ld(_faqs)],
    active="aaj-ka-panchang.html")
QA.insert(3, ("मेरी जन्म तिथि और राशि क्या है?", "जन्म की तारीख़ और समय डालकर कैलकुलेटर से तुरंत जानें — तिथि, नक्षत्र, राशि और नाम अक्षर।", "janm-tithi-rashi-calculator.html"))

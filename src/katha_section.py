# Vrat katha pages. Executed inside build.py after library_section (uses band, add, FEST, TODAY_D, hdate_w...).
KATHA_CAT = []
_REL = {
 "karwa-chauth-vrat-katha.html":[("karwa-chauth-kab-hai.html","करवा चौथ 2026 कब है","चंद्रोदय का समय"),("aarti-mantra.html","आरती संग्रह","सभी आरतियाँ")],
 "ahoi-ashtami-vrat-katha.html":[("ahoi-mata-aarti.html","अहोई माता की आरती","जय अहोई माता"),("ahoi-ashtami-kab-hai.html","अहोई अष्टमी 2026 कब है","तारीख़ और समय")],
 "somvar-vrat-katha.html":[("shiv-aarti-om-jai-shiv-omkara.html","शिव आरती","ॐ जय शिव ओंकारा"),("shiv-chalisa.html","शिव चालीसा","अर्थ सहित"),("om-namah-shivaya.html","ॐ नमः शिवाय","जाप विधि")],
 "satyanarayan-vrat-katha.html":[("satyanarayan-aarti.html","सत्यनारायण आरती","ॐ जय लक्ष्मी रमणा"),("purnima-amavasya-2026-2027.html","पूर्णिमा 2026–27","कथा का शुभ दिन")],
}
NOTE = "यह कथा पारंपरिक कथा का OmKiran Bhakti द्वारा सरल हिंदी में किया गया पुनर्कथन है; अलग-अलग क्षेत्रों में कथा के विवरण में थोड़ा अंतर मिलता है।"
for k in KATHAS:
    dline = ""
    if k["fest"] and FEST.get(k["fest"]):
        nxt = next((x for x in FEST[k["fest"]] if x["date"] >= TODAY_D), FEST[k["fest"]][-1])
        dline = ('<p class="lede">' + e(nxt["name"]) + " " + str(nxt["date"].year) + ": <strong>" + hdate_w(nxt["date"]) +
                 '</strong> — <a href="' + k["fest"] + '-kab-hai.html">तिथि और पूजा का समय देखें</a></p>')
    secs = "".join('<h2 class="k-h">' + e(h) + "</h2>" + "".join("<p>" + e(par) + "</p>" for par in paras) for h, paras in k["sections"])
    vids = [v for v in k["vids"] if v in V]
    relh = "".join('<li><a href="' + h + '"><strong>' + e(t) + "</strong><span>" + e(sb) + "</span></a></li>" for h, t, sb in _REL[k["slug"]])
    body = (band(k["h1"], k["answer"], k["h1"], *k["art"], k["h1"], extra=dline) +
            '<article><section><div class="wrap prose katha">' + secs + '<p class="note">' + NOTE + "</p></div></section></article>" +
            (('<section class="band no-print"><div class="wrap">' + sec_head("सुनें") + video_cards(vids) + "</div></section>") if vids else "") +
            '<section class="no-print"><div class="wrap">' + sec_head("साथ में पढ़ें") + '<ul class="library">' + relh + "</ul></div></section>" +
            faq_html(k["faqs"]))
    ld = [{"@type":"Article","headline":k["h1"],"inLanguage":"hi","author":{"@id":SITE+"#organization"},
           "publisher":{"@id":SITE+"#organization"},"dateModified":TODAY,"description":k["desc"]}] + ([faq_ld(k["faqs"])] if k["faqs"] else [])
    add(k["slug"], k["title"], k["desc"], body, crumbs=k["h1"], ld=ld, active="aarti-mantra.html")
    KATHA_CAT.append((k["slug"], "katha", k["h1"], "सरल हिंदी में", k["art"]))

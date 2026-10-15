# Daily city-wise Choghadiya, Rahu kaal, Yamaganda, Gulika, Abhijit. Rebuilt every day by the deploy cron.
import datetime as _dt
CH_NAMES = ["उद्वेग", "चर", "लाभ", "अमृत", "काल", "शुभ", "रोग"]
CH_KIND = {"अमृत": ("good", "सबसे शुभ"), "शुभ": ("good", "शुभ"), "लाभ": ("good", "शुभ — व्यापार/लाभ"), "चर": ("mid", "सामान्य — यात्रा के लिए अच्छा"),
           "उद्वेग": ("bad", "अशुभ"), "रोग": ("bad", "अशुभ"), "काल": ("bad", "अशुभ")}
DAY_START = {6: 0, 0: 3, 1: 6, 2: 2, 3: 5, 4: 1, 5: 4}     # python weekday -> first day choghadiya index
NIGHT_START = {6: 5, 0: 1, 1: 4, 2: 0, 3: 3, 4: 6, 5: 2}
RAHU = {0: 2, 1: 7, 2: 5, 3: 6, 4: 4, 5: 3, 6: 8}; YAMA = {0: 4, 1: 3, 2: 2, 3: 1, 4: 7, 5: 6, 6: 5}; GULI = {0: 6, 1: 5, 2: 4, 3: 3, 4: 2, 5: 1, 6: 7}

def chogh(la, lo, day):
    sr, ss = c_sun(la, lo, day, IN_TZ); sr2, _ = c_sun(la, lo, day + _dt.timedelta(days=1), IN_TZ)
    dl, nl = (ss - sr) / 8, (sr2 - ss) / 8
    i0, j0 = DAY_START[day.weekday()], NIGHT_START[day.weekday()]
    dayc = [(CH_NAMES[(i0 + k) % 7], sr + dl * k, sr + dl * (k + 1)) for k in range(8)]
    nightc = [(CH_NAMES[(j0 + 5 * k) % 7], ss + nl * k, ss + nl * (k + 1)) for k in range(8)]
    seg = lambda n: (sr + dl * (n - 1), sr + dl * n)
    mu = (ss - sr) / 15
    return {"sr": sr, "ss": ss, "day": dayc, "night": nightc, "rahu": seg(RAHU[day.weekday()]), "yama": seg(YAMA[day.weekday()]),
            "guli": seg(GULI[day.weekday()]), "abhijit": (sr + mu * 7, sr + mu * 8)}

def _ctbl(rows, cap):
    tr = "".join(f'<tr class="ch-{CH_KIND[n][0]}" data-s="{a.isoformat()}" data-e="{b.isoformat()}"><td><strong>{n}</strong></td><td>{ct12(a)} – {ct12(b)}</td><td>{CH_KIND[n][1]}</td></tr>' for n, a, b in rows)
    return f'<div class="tbl"><table class="ptable chogh"><caption>{cap}</caption><thead><tr><th>चौघड़िया</th><th>समय</th><th>फल</th></tr></thead><tbody>{tr}</tbody></table></div>'
CH_JS = ('<script>(function(){var n=Date.now();[].slice.call(document.querySelectorAll(".chogh tr[data-s]")).forEach(function(r){'
         'if(Date.parse(r.dataset.s)<=n&&n<Date.parse(r.dataset.e)){r.classList.add("now");var c=r.cells[2];c.textContent+=" — अभी चल रहा है";}});})();</script>')
def _slug(en): return "choghadiya-" + re.sub(r"[^a-z]+", "-", en.lower()).strip("-") + ".html"
CHOGH_PAGES = []
_D, _T = TODAY_D, TODAY_D + _dt.timedelta(days=1)
for hi, en, la, lo in IN_CITIES:
    c, t = chogh(la, lo, _D), chogh(la, lo, _T)
    good = [x for x in c["day"] if CH_KIND[x[0]][0] == "good"]
    ans = (f"आज {hdate_w(_D)} को {hi} में सूर्योदय {ct12(c['sr'])} और सूर्यास्त {ct12(c['ss'])} है। "
           f"दिन का सबसे शुभ चौघड़िया <strong>{', '.join(f'{n} ({ct12(a)}–{ct12(b)})' for n, a, b in good[:3])}</strong> है। "
           f"राहु काल <strong>{ct12(c['rahu'][0])} – {ct12(c['rahu'][1])}</strong> तक रहेगा।")
    extra = (f'<div class="kaal-grid"><div><b>राहु काल</b><span>{ct12(c["rahu"][0])} – {ct12(c["rahu"][1])}</span><small>नया काम शुरू न करें</small></div>'
             f'<div><b>अभिजीत मुहूर्त</b><span>{ct12(c["abhijit"][0])} – {ct12(c["abhijit"][1])}</span><small>{"बुधवार को अभिजीत नहीं लिया जाता" if _D.weekday()==2 else "दिन का सबसे शुभ समय"}</small></div>'
             f'<div><b>यमगंड</b><span>{ct12(c["yama"][0])} – {ct12(c["yama"][1])}</span><small>अशुभ</small></div>'
             f'<div><b>गुलिक काल</b><span>{ct12(c["guli"][0])} – {ct12(c["guli"][1])}</span><small>इसमें किया काम दोहराया जाता है</small></div></div>')
    faqs = [(f"आज {hi} में शुभ चौघड़िया कब है?", re.sub("<[^>]+>", "", ans)),
            ("चौघड़िया क्या होता है?", "दिन (सूर्योदय से सूर्यास्त) और रात (सूर्यास्त से अगले सूर्योदय) को आठ-आठ बराबर भागों में बाँटा जाता है; हर भाग एक चौघड़िया है। अमृत, शुभ और लाभ शुभ हैं, चर सामान्य है, और रोग, काल, उद्वेग अशुभ माने जाते हैं।"),
            ("चौघड़िया हर शहर में अलग क्यों होता है?", "क्योंकि यह स्थानीय सूर्योदय और सूर्यास्त से निकलता है; दिल्ली और मुंबई के सूर्योदय में लगभग आधे घंटे का अंतर होता है।")]
    body = (band(f"आज का चौघड़िया — {hi}", ans, f"चौघड़िया {hi}", ("ktQUU5Y3tPE", 50), "चौघड़िया", extra='<p class="lede"><a href="aaj-ka-choghadiya.html">दूसरा शहर चुनें</a> · <a href="aaj-ka-panchang.html">आज का पंचांग</a></p>') +
            f'<section><div class="wrap">{extra}<div class="ch-cols">{_ctbl(c["day"], f"दिन का चौघड़िया — {hdate_w(_D)}")}{_ctbl(c["night"], "रात का चौघड़िया")}</div>'
            f'<h2 class="ch-tom">कल — {hdate_w(_T)}</h2><div class="ch-cols">{_ctbl(t["day"], "दिन का चौघड़िया")}{_ctbl(t["night"], "रात का चौघड़िया")}</div>'
            f'<p class="note">{hi} ({en}) के अक्षांश-देशांतर से गणना। यह पेज हर रात 12 बजे अपने-आप अपडेट होता है।</p></div></section>' + faq_html(faqs) + CH_JS)
    slug = _slug(en)
    add(slug, f"आज का चौघड़िया {hi} ({en}) — शुभ मुहूर्त, राहु काल | OmKiran Bhakti",
        f"आज का चौघड़िया {hi}: सूर्योदय {ct12(c['sr'])}, राहु काल {ct12(c['rahu'][0])}–{ct12(c['rahu'][1])}। दिन-रात के अमृत, शुभ, लाभ चौघड़िया का समय, अभिजीत मुहूर्त।"[:160],
        body, crumbs=f"चौघड़िया {hi}", ld=[faq_ld(faqs)], active="aaj-ka-panchang.html")
    CHOGH_PAGES.append((slug, hi, en))
# hub
c = chogh(28.6139, 77.2090, _D)
grid = "".join(f'<li><a href="{s}"><strong>{h}</strong><span>{en}</span></a></li>' for s, h, en in CHOGH_PAGES)
good = [x for x in c["day"] if CH_KIND[x[0]][0] == "good"]
ans = (f"आज {hdate_w(_D)} को दिल्ली में शुभ चौघड़िया <strong>{', '.join(f'{n} {ct12(a)}–{ct12(b)}' for n, a, b in good)}</strong> है; राहु काल {ct12(c['rahu'][0])}–{ct12(c['rahu'][1])}। "
       "अपने शहर का चौघड़िया नीचे चुनें — हर शहर का समय वहाँ के सूर्योदय से अलग होता है।")
faqs = [("आज का शुभ चौघड़िया कब है?", re.sub("<[^>]+>", "", ans).split(" अपने शहर")[0]),
        ("सबसे शुभ चौघड़िया कौन सा है?", "अमृत चौघड़िया सबसे शुभ माना जाता है, फिर शुभ और लाभ। चर यात्रा के लिए अच्छा है। रोग, काल और उद्वेग में नए काम शुरू नहीं किए जाते।")]
add("aaj-ka-choghadiya.html", f"आज का चौघड़िया — {hdate(_D)} शुभ मुहूर्त, राहु काल (65 शहर) | OmKiran Bhakti",
    f"आज का चौघड़िया: दिल्ली में राहु काल {ct12(c['rahu'][0])}–{ct12(c['rahu'][1])}। दिन और रात के अमृत, शुभ, लाभ चौघड़िया — 65 शहरों का अलग समय।"[:160],
    band("आज का चौघड़िया", ans, "आज का चौघड़िया", ("ktQUU5Y3tPE", 50), "चौघड़िया") +
    f'<section><div class="wrap"><div class="ch-cols">{_ctbl(c["day"], "दिल्ली — दिन का चौघड़िया")}{_ctbl(c["night"], "दिल्ली — रात का चौघड़िया")}</div></div></section>'
    f'<section class="band"><div class="wrap">{sec_head("अपना शहर चुनें")}{city_search("शहर का नाम — जैसे Pune, जयपुर…")}<ul class="hot-list city-grid">{grid}</ul></div></section>'
    + faq_html(faqs) + CH_JS +
    '<script>(function(){var q=document.getElementById("city-q");if(!q)return;var li=[].slice.call(document.querySelectorAll(".city-grid li"));q.addEventListener("input",function(){var v=q.value.trim().toLowerCase();li.forEach(function(x){x.hidden=v&&x.textContent.toLowerCase().indexOf(v)<0;});});})();</script>',
    crumbs="आज का चौघड़िया", ld=[faq_ld(faqs)], active="aaj-ka-panchang.html")
QA.insert(0, ("आज का शुभ चौघड़िया कब है?", re.sub("<[^>]+>", "", ans).split(" अपने शहर")[0], "aaj-ka-choghadiya.html"))

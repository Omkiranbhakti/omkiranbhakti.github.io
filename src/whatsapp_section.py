# Daily ready-to-post WhatsApp channel message (today + tomorrow), rebuilt every night by the deploy cron.
import datetime as _dt, json as _j
_WD = [("shiv","ॐ नमः शिवाय","सोमवार — भोलेनाथ का दिन","shiv-chalisa.html","शिव चालीसा"),
       ("hanuman","जय बजरंगबली","मंगलवार — हनुमान जी का दिन","hanuman-chalisa.html","हनुमान चालीसा"),
       ("ganesh","गणपति बप्पा मोरया","बुधवार — श्री गणेश का दिन","ganesh-chalisa.html","गणेश चालीसा"),
       ("vishnu","ॐ नमो भगवते वासुदेवाय","गुरुवार — श्री हरि विष्णु का दिन","om-jai-jagdish-hare-aarti.html","ॐ जय जगदीश हरे"),
       ("mata","जय माता दी","शुक्रवार — माँ दुर्गा और लक्ष्मी का दिन","durga-chalisa.html","दुर्गा चालीसा"),
       ("shani","जय शनिदेव","शनिवार — शनिदेव और हनुमान जी का दिन","shani-chalisa.html","शनि चालीसा"),
       ("surya","ॐ सूर्याय नमः","रविवार — सूर्यदेव का दिन","aditya-hridaya-stotra.html","आदित्य हृदय स्तोत्र")]
def _msg(day):
    p = DAYS.get(day)
    if not p: return None, None
    k, jay, dname, pu, pt = _WD[day.weekday()]
    fest = DAYFEST.get(day, [])
    up, seen = [], set()
    for j in range(1, 20):
        dd = day + _dt.timedelta(days=j)
        for n, w, u in DAYFEST.get(dd, []):
            if 'नवरात्रि —' in n or n in seen: continue
            seen.add(n); up.append((dd, n, u, w))
    up = up[:4]
    L = [f"🙏 *{jay}* 🙏", "", f"📅 *{hdate_w(day)}*", f"🕉️ *आज का पंचांग*",
         f"🌙 तिथि: {p['paksha']} पक्ष {p['tithi']} ({p['month_purnimanta']} मास)",
         f"⭐ नक्षत्र: {p['nakshatra']}",
         f"🌅 सूर्योदय {t12(p['sunrise'])} | 🌇 सूर्यास्त {t12(p['sunset'])}",
         f"✨ अभिजीत मुहूर्त: {t12(p['abhijit'][0])} – {t12(p['abhijit'][1])}" + ("" if p.get('abhijit_ok', True) else " (बुधवार को नहीं)"),
         f"⚠️ राहु काल: {t12(p['rahu'][0])} – {t12(p['rahu'][1])}"]
    if fest:
        L += ["", "🪔 *आज के व्रत-त्योहार*"] + [f"• {n}" for n, w, u in fest[:4]]
    L += ["", f"📿 {dname}", f"आज पढ़ें: *{pt}* (अर्थ सहित)", SITE + pu]
    if up:
        L += ["", "🔔 *आने वाले त्योहार*"] + [f"• {d.day} {MONTHS_HI[d.month]} — {n}" for d, n, u, w in up]
    L += ["", "🛕 मंदिरों के लाइव दर्शन: " + SITE + "live-darshan.html",
          "📖 पूरा पंचांग: " + SITE + "aaj-ka-panchang.html", "", "— *OmKiran Bhakti* 🙏 चैनल को शेयर करें"]
    return "\n".join(L), k
_cards = []
for i, lab in [(0, "आज"), (1, "कल")]:
    d = TODAY_D + _dt.timedelta(days=i)
    txt, k = _msg(d)
    if not txt: continue
    _cards.append(f'''<div class="wa-card"><div class="wa-top"><h2>{lab} — {hdate_w(d)}</h2>
<img src="img/art/wa-{k}.jpg" alt="" width="160" height="214" loading="lazy"></div>
<pre class="wa-txt" id="wa{i}">{e(txt)}</pre>
<div class="wa-btns"><button class="btn gold" type="button" data-copy="wa{i}">📋 मैसेज कॉपी करें</button>
<a class="btn ghost" href="img/art/wa-{k}.jpg" download="omkiran-{d.isoformat()}.jpg">🖼️ फोटो डाउनलोड</a>
<a class="btn ghost" href="{WA_CH}" target="_blank" rel="noopener">चैनल खोलें</a></div></div>''')
_JS = '''<script>document.querySelectorAll("[data-copy]").forEach(function(b){b.addEventListener("click",function(){var t=document.getElementById(b.dataset.copy).textContent;
(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){b.textContent="✅ कॉपी हो गया — अब चैनल में पेस्ट करें"},function(){var r=document.createRange();r.selectNodeContents(document.getElementById(b.dataset.copy));var s=getSelection();s.removeAllRanges();s.addRange(r);document.execCommand("copy");b.textContent="✅ कॉपी हो गया";});});});</script>'''
add("whatsapp-sandesh.html", "आज का WhatsApp संदेश — OmKiran Bhakti",
    "OmKiran Bhakti WhatsApp चैनल के लिए रोज़ का तैयार संदेश।",
    band("आज का WhatsApp संदेश", "हर रात 12 बजे अपने-आप नया संदेश बनता है। <strong>कॉपी करें → फोटो डाउनलोड करें → चैनल में भेजें।</strong>", "WhatsApp संदेश") +
    f'<section><div class="wrap wa-wrap">{"".join(_cards)}</div></section>' + _JS, crumbs="WhatsApp संदेश")
PAGES["whatsapp-sandesh.html"] = PAGES["whatsapp-sandesh.html"].replace('<meta name="robots" content="index,follow,max-image-preview:large">','<meta name="robots" content="noindex">')

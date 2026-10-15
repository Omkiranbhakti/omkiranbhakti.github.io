/* OmKiran Bhakti — जन्म तिथि, नक्षत्र, राशि और नाम अक्षर (Lahiri ayanamsa, same method as the site's panchang).
   Needs astronomy-engine (window.Astronomy in the browser, or require() in Node). */
(function (root) {
  var A = root.Astronomy || (typeof require === "function" ? require("astronomy-engine") : null);
  var TITHI = ["प्रतिपदा","द्वितीया","तृतीया","चतुर्थी","पंचमी","षष्ठी","सप्तमी","अष्टमी","नवमी","दशमी","एकादशी","द्वादशी","त्रयोदशी","चतुर्दशी","पूर्णिमा"];
  var NAK = ["अश्विनी","भरणी","कृत्तिका","रोहिणी","मृगशिरा","आर्द्रा","पुनर्वसु","पुष्य","आश्लेषा","मघा","पूर्वा फाल्गुनी","उत्तरा फाल्गुनी","हस्त","चित्रा","स्वाति","विशाखा","अनुराधा","ज्येष्ठा","मूल","पूर्वाषाढ़ा","उत्तराषाढ़ा","श्रवण","धनिष्ठा","शतभिषा","पूर्वा भाद्रपद","उत्तरा भाद्रपद","रेवती"];
  var AKSHAR = [["चु","चे","चो","ला"],["ली","लू","ले","लो"],["अ","ई","उ","ए"],["ओ","वा","वी","वू"],["वे","वो","का","की"],["कु","घ","ङ","छ"],["के","को","हा","ही"],["हु","हे","हो","डा"],["डी","डू","डे","डो"],["मा","मी","मू","मे"],["मो","टा","टी","टू"],["टे","टो","पा","पी"],["पू","ष","ण","ठ"],["पे","पो","रा","री"],["रू","रे","रो","ता"],["ती","तू","ते","तो"],["ना","नी","नू","ने"],["नो","या","यी","यू"],["ये","यो","भा","भी"],["भू","धा","फा","ढा"],["भे","भो","जा","जी"],["खी","खू","खे","खो"],["गा","गी","गू","गे"],["गो","सा","सी","सू"],["से","सो","दा","दी"],["दू","थ","झ","ञ"],["दे","दो","चा","ची"]];
  var RASHI = ["मेष","वृषभ","मिथुन","कर्क","सिंह","कन्या","तुला","वृश्चिक","धनु","मकर","कुंभ","मीन"];
  var RASHI_LORD = ["मंगल","शुक्र","बुध","चंद्र","सूर्य","बुध","शुक्र","मंगल","गुरु","शनि","शनि","गुरु"];
  var MONTH_BY_SIGN = ["वैशाख","ज्येष्ठ","आषाढ़","श्रावण","भाद्रपद","आश्विन","कार्तिक","मार्गशीर्ष","पौष","माघ","फाल्गुन","चैत्र"];
  var MONTH_ORDER = ["चैत्र","वैशाख","ज्येष्ठ","आषाढ़","श्रावण","भाद्रपद","आश्विन","कार्तिक","मार्गशीर्ष","पौष","माघ","फाल्गुन"];
  var GAN = ["देव","मनुष्य","राक्षस","मनुष्य","देव","मनुष्य","देव","देव","राक्षस","राक्षस","मनुष्य","मनुष्य","देव","राक्षस","देव","राक्षस","देव","राक्षस","राक्षस","मनुष्य","मनुष्य","देव","राक्षस","राक्षस","मनुष्य","मनुष्य","देव"];
  var NADI = ["आदि","मध्य","अंत्य","अंत्य","मध्य","आदि","आदि","मध्य","अंत्य","आदि","मध्य","अंत्य","अंत्य","मध्य","आदि","आदि","मध्य","अंत्य","आदि","मध्य","अंत्य","अंत्य","मध्य","आदि","आदि","मध्य","अंत्य"];
  var GANDMOOL = {0:1, 8:1, 9:1, 17:1, 18:1, 26:1};

  function jd(t) { return t.getTime() / 86400000 + 2440587.5; }
  function ayanamsa(t) { return 23.85307 + ((jd(t) - 2451545.0) / 365.25) * 0.0139694; }
  function moonLon(t) { return A.EclipticGeoMoon(t).lon; }
  function sunLon(t) { return A.SunPosition(t).elon; }
  function norm(x) { return ((x % 360) + 360) % 360; }
  function sidMoon(t) { return norm(moonLon(t) - ayanamsa(t)); }
  function sidSun(t) { return norm(sunLon(t) - ayanamsa(t)); }
  function tithiIndex(t) { return Math.floor(norm(moonLon(t) - sunLon(t)) / 12); }
  function newMoonBefore(t) {
    var s = A.SearchMoonPhase(0, new Date(t.getTime() - 32 * 864e5), 40), last = null;
    while (s && s.date <= t) { last = s.date; s = A.SearchMoonPhase(0, new Date(s.date.getTime() + 864e5), 40); }
    return { prev: last, next: s ? s.date : null };
  }
  function lunarMonth(t) {
    var nm = newMoonBefore(t), s1 = Math.floor(sidSun(nm.prev) / 30), s2 = Math.floor(sidSun(nm.next) / 30);
    var adhik = s1 === s2, amanta = MONTH_BY_SIGN[adhik ? (s1 + 1) % 12 : s1];
    var ti = tithiIndex(t), purni = ti >= 15 ? MONTH_ORDER[(MONTH_ORDER.indexOf(amanta) + 1) % 12] : amanta;
    return { amanta: amanta, purnimanta: purni, adhik: adhik };
  }
  function vikram(t, amanta) {
    var y = t.getUTCFullYear(), m = t.getUTCMonth() + 1;
    if (m >= 5) return y + 57; if (m <= 2) return y + 56;
    return (amanta === "फाल्गुन" || amanta === "माघ") ? y + 56 : y + 57;
  }
  function tithiName(i) { return i === 29 ? ["कृष्ण", "अमावस्या"] : (i < 15 ? ["शुक्ल", TITHI[i]] : ["कृष्ण", TITHI[i - 15]]); }

  function birth(t) {
    var sm = sidMoon(t), ti = tithiIndex(t), nk = Math.floor(sm / (360 / 27)), pada = Math.floor((sm % (360 / 27)) / (360 / 108));
    var lm = lunarMonth(t), tn = tithiName(ti), r = Math.floor(sm / 30), sr = Math.floor(sidSun(t) / 30);
    return { tithiIndex: ti, paksha: tn[0], tithi: tn[1], nakIndex: nk, nakshatra: NAK[nk], pada: pada + 1, akshar: AKSHAR[nk][pada], allAkshar: AKSHAR[nk],
             rashi: RASHI[r], rashiIndex: r, rashiLord: RASHI_LORD[r], suryaRashi: RASHI[sr], amanta: lm.amanta, purnimanta: lm.purnimanta, adhik: lm.adhik,
             vikram: vikram(t, lm.amanta), gan: GAN[nk], nadi: NADI[nk], gandmool: !!GANDMOOL[nk] };
  }
  /* Next date (from `from`) whose sunrise tithi + amanta month match the birth: the "tithi birthday". 06:00 IST used as sunrise. */
  function nextTithiBirthday(b, from, count) {
    var out = [], d = new Date(Date.UTC(from.getUTCFullYear(), from.getUTCMonth(), from.getUTCDate(), 0, 30));
    for (var k = 0; k < 800 && out.length < (count || 1); k++, d = new Date(d.getTime() + 864e5)) {
      if (tithiIndex(d) !== b.tithiIndex) continue;
      var lm = lunarMonth(d);
      if (lm.amanta === b.amanta && !lm.adhik) { out.push(new Date(d.getTime())); d = new Date(d.getTime() + 300 * 864e5); }
    }
    return out;
  }
  /* Name -> nakshatra pada and rashi from the first syllable */
  var MAP = {}; AKSHAR.forEach(function (row, n) { row.forEach(function (s, p) { MAP[s] = { nak: n, pada: p }; }); });
  function syll(name) {
    name = (name || "").trim(); if (!name) return "";
    var c = name.charAt(0);
    if (c === "ऋ") return "री";
    if ("अआइईउऊएऐओऔ".indexOf(c) >= 0) return { "आ": "अ", "इ": "ई", "ऊ": "उ", "ऐ": "ए", "औ": "ओ" }[c] || c;
    var i = 1; while (name.charAt(i) === "्" && i + 1 < name.length) i += 2;   // skip conjuncts: प्रि -> पी
    var m = name.charAt(i); c = { "श": "स", "ब": "व", "ड़": "ड", "ढ़": "ढ" }[c] || c;
    if (m && "ािीुूेैोौ".indexOf(m) >= 0) return c + ({ "ि": "ी", "ु": "ू", "ै": "े", "ौ": "ो" }[m] || m);
    return c;
  }
  function nameRashi(name) {
    var s = syll(name); if (!s) return null;
    var cands = [s, s.replace("ी", "ि").replace("ू", "ु"), s.charAt(0) + "ा", s.charAt(0)];
    if (s.length === 2) { var alt = { "ी": "ि", "ू": "ु" }[s.charAt(1)]; if (alt) cands.splice(1, 0, s.charAt(0) + alt); }
    for (var i = 0; i < cands.length; i++) if (MAP[cands[i]]) {
      var h = MAP[cands[i]], r = Math.floor(((h.nak * 4 + h.pada) * (360 / 108) + 0.001) / 30);
      return { syllable: cands[i], nakshatra: NAK[h.nak], pada: h.pada + 1, rashi: RASHI[r], rashiLord: RASHI_LORD[r] };
    }
    for (var n = 0; n < 27; n++) for (var p = 0; p < 4; p++) if (AKSHAR[n][p].charAt(0) === s.charAt(0)) {
      var r2 = Math.floor(((n * 4 + p) * (360 / 108) + 0.001) / 30); return { syllable: AKSHAR[n][p], nakshatra: NAK[n], pada: p + 1, rashi: RASHI[r2], rashiLord: RASHI_LORD[r2] };
    }
    return null;
  }
  var api = { birth: birth, nextTithiBirthday: nextTithiBirthday, nameRashi: nameRashi, AKSHAR: AKSHAR, NAK: NAK, RASHI: RASHI };
  if (typeof module !== "undefined") module.exports = api; else root.Janm = api;
})(typeof window !== "undefined" ? window : globalThis);

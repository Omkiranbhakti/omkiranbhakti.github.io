/* OmKiran Bhakti — ऑनलाइन हारमोनियम (Web Audio, no samples, no external libraries).
   Page supplies <div class="hm" id="hm"></div> and <script type="application/json" id="hm-data">{"songs":[...],"start":"id"}</script>.
   Notation tokens: S r R g G M m P d D n N  (r g d n = komal, m = tivra Ma), "." before = mandra (low), "'" after = taar (high), "-" = hold one more beat. */
(function () {
  "use strict";
  var root = document.getElementById("hm");
  if (!root) return;
  var data = {};
  try { data = JSON.parse(document.getElementById("hm-data").textContent); } catch (e) {}
  var songs = data.songs || [];

  // ---------- notation ----------
  var SEMI = { S: 0, r: 1, R: 2, g: 3, G: 4, M: 5, m: 6, P: 7, d: 8, D: 9, n: 10, N: 11 };
  var NAME = ["सा", "रे", "रे", "ग", "ग", "म", "म", "प", "ध", "ध", "नि", "नि"];
  var KOMAL = { 1: 1, 3: 1, 8: 1, 10: 1 }, TIVRA = { 6: 1 };
  function parse(str) {
    var out = [];
    str.trim().split(/\s+/).forEach(function (t) {
      if (t === "-") { if (out.length) out[out.length - 1].dur++; return; }
      var low = 0, high = 0;
      while (t.charAt(0) === ".") { low++; t = t.slice(1); }
      while (t.charAt(t.length - 1) === "'") { high++; t = t.slice(0, -1); }
      if (!(t in SEMI)) return;
      out.push({ s: SEMI[t] - 12 * low + 12 * high, dur: 1 });
    });
    return out;
  }
  var WEST = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
  function west(s) { var m = 48 + saPc + s; return WEST[m % 12] + (Math.floor(m / 12) - 1); }
  function label(s) { // sargam and/or western name, per the "पट्टी पर नाम" choice
    var sg = sargamLabel(s);
    if (names === "west") return '<span class="wn only">' + west(s) + "</span>";
    if (names === "both") return sg + '<span class="wn">' + west(s) + "</span>";
    return sg;
  }
  function sargamLabel(s) { // sargam label with octave + komal/tivra classes
    var pc = ((s % 12) + 12) % 12, oct = Math.floor(s / 12);
    var cls = (KOMAL[pc] ? " komal" : "") + (TIVRA[pc] ? " tivra" : "") + (oct < 0 ? " low" : oct > 0 ? " high" : "");
    return '<span class="sw' + cls + '">' + NAME[pc] + "</span>";
  }
  function plain(s) {
    if (names === "west") return west(s);
    return plainSargam(s) + (names === "both" ? " / " + west(s) : "");
  }
  function plainSargam(s) {
    var pc = ((s % 12) + 12) % 12, oct = Math.floor(s / 12);
    return (oct < 0 ? "मंद्र " : oct > 0 ? "तार " : "") + NAME[pc] + (KOMAL[pc] ? " (कोमल)" : TIVRA[pc] ? " (तीव्र)" : "");
  }

  // ---------- settings ----------
  var store = {};
  try { store = JSON.parse(localStorage.getItem("okb-hm") || "{}"); } catch (e) {}
  function save() { try { localStorage.setItem("okb-hm", JSON.stringify(store)); } catch (e) {} }
  var saPc = typeof store.sa === "number" ? store.sa : 0;          // 0 = C (सफ़ेद 1)
  var vol = typeof store.vol === "number" ? store.vol : 0.5;
  var speed = 100; // % of the song's real tempo
  var showKeys = store.keys !== false;
  var names = store.names || "sargam";
  var pumpMode = !!store.pump, airLvl = 1; // "धौंकनी ख़ुद चलाएँ": sound needs air you pump in
  var mech = typeof store.mech === "number" ? store.mech : 0.3; // key clatter + bellows air, 0..1
  var bassOn = store.bass !== false, highOn = !!store.high, coupOn = !!store.coup, echoOn = store.echo !== false;
  var SCALES = ["सफ़ेद 1 (C)", "काली 1 (C#)", "सफ़ेद 2 (D)", "काली 2 (D#)", "सफ़ेद 3 (E)", "सफ़ेद 4 (F)",
    "काली 3 (F#)", "सफ़ेद 5 (G)", "काली 4 (G#)", "सफ़ेद 6 (A)", "काली 5 (A#)", "सफ़ेद 7 (B)"];

  // ---------- sound: two detuned reeds + a soft bass reed, filtered, with gentle bellows tremolo ----------
  // Free-reed model: a narrow-pulse reed spectrum (strong, buzzy upper partials), two middle reeds a few
  // cents apart (the slow "beating" of a real harmonium), a bass reed an octave down, a little air from the
  // reed slot, and a shared body EQ (nasal formants) with a slow bellows swell. No vibrato, no tremolo.
  var ac = null, master = null, bus = null, dry = null, room = null, roomIn = null, roomWet = null, voices = {}, drone = null, waves = {}, noiseBuf = null;
  function reedWave(duty, tilt) {
    var N = 48, re = new Float32Array(N), im = new Float32Array(N);
    for (var n = 1; n < N; n++) im[n] = (Math.abs(Math.sin(Math.PI * n * duty)) + 0.12) / Math.pow(n, tilt);
    return ac.createPeriodicWave(re, im);
  }
  function audio() {
    if (!ac) {
      var AC = window.AudioContext || window.webkitAudioContext;
      if (!AC) return null;
      ac = new AC();
      master = ac.createGain(); master.gain.value = vol * (typeof airGain === "function" ? airGain() : 1);
      bus = ac.createGain(); bus.gain.value = 1;
      var hp = ac.createBiquadFilter(); hp.type = "highpass"; hp.frequency.value = 70;
      var f1 = ac.createBiquadFilter(); f1.type = "peaking"; f1.frequency.value = 1150; f1.Q.value = 1.1; f1.gain.value = 5;
      var f2 = ac.createBiquadFilter(); f2.type = "peaking"; f2.frequency.value = 2700; f2.Q.value = 1.4; f2.gain.value = 3;
      var lp = ac.createBiquadFilter(); lp.type = "lowpass"; lp.frequency.value = 5200; lp.Q.value = 0.5;
      var bellows = ac.createGain(); bellows.gain.value = 1;
      var lfo = ac.createOscillator(), lfoG = ac.createGain();
      lfo.frequency.value = 0.45; lfoG.gain.value = 0.03; lfo.connect(lfoG); lfoG.connect(bellows.gain); lfo.start();
      var comp = ac.createDynamicsCompressor(); comp.threshold.value = -14; comp.ratio.value = 3;
      bus.connect(hp); hp.connect(f1); f1.connect(f2); f2.connect(lp); lp.connect(bellows); bellows.connect(master);
      dry = ac.createGain(); dry.connect(master);
      // a small Indian room: generated impulse response (no files), mixed under the dry reed
      room = ac.createConvolver(); roomIn = ac.createGain(); roomWet = ac.createGain();
      var len = Math.round(ac.sampleRate * 1.5), ir = ac.createBuffer(2, len, ac.sampleRate);
      for (var c = 0; c < 2; c++) { var dd = ir.getChannelData(c); for (var j = 0; j < len; j++) dd[j] = (Math.random() * 2 - 1) * Math.pow(1 - j / len, 3.2) * (j < 400 ? j / 400 : 1); }
      room.buffer = ir; roomWet.gain.value = echoOn ? 0.28 : 0;
      roomIn.connect(room); room.connect(roomWet); roomWet.connect(master);
      master.connect(comp); comp.connect(ac.destination);
      waves.mid = reedWave(0.23, 0.72); waves.bass = reedWave(0.38, 0.95);
      noiseBuf = ac.createBuffer(1, ac.sampleRate, ac.sampleRate);
      var d = noiseBuf.getChannelData(0); for (var i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
    }
    if (ac.state === "suspended") ac.resume();
    loadSamples();
    return ac;
  }
  function freq(s) { return 130.8128 * Math.pow(2, (saPc + s) / 12); } // सा = C3 … B3 (real harmonium middle)

  // ---------- recorded harmonium (CC0 samples, one per key G2–D5) ----------
  var SMP = [36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,67,68,69,70,71,72,73,74];
  var SBASE = (data.samples || "audio/harmonium/"), bufs = {}, loading = false, loadedN = 0;
  var LOOP_A = 1.4, LOOP_B = 4.4, XF = 0.25, START = 0.09;
  function prepLoop(b) { // equal-power crossfade so the sustain loops without a click
    var sr = b.sampleRate, a = Math.round(LOOP_A * sr), e = Math.round(LOOP_B * sr), c = Math.round(XF * sr);
    if (e > b.length) e = b.length - 1;
    for (var ch = 0; ch < b.numberOfChannels; ch++) {
      var d = b.getChannelData(ch);
      for (var i = 0; i < c; i++) {
        var w = i / c, x = e - c + i, y = a - c + i;
        d[x] = d[x] * Math.cos(w * Math.PI / 2) + d[y] * Math.sin(w * Math.PI / 2);
      }
    }
    b._a = a / sr; b._b = e / sr; return b;
  }
  function loadSamples() {
    if (loading || !ac || !window.fetch) return; loading = true;
    var sa = 48 + saPc, order = SMP.slice().sort(function (x, y) { return Math.abs(x - sa - 3) - Math.abs(y - sa - 3); });
    var st = root.querySelector(".hm-load"); if (st) st.hidden = false;
    order.forEach(function (m) {
      fetch(SBASE + "h" + m + ".mp3").then(function (r) { if (!r.ok) throw 0; return r.arrayBuffer(); })
        .then(function (ab) { return new Promise(function (ok, no) { ac.decodeAudioData(ab, ok, no); }); })
        .then(function (b) { bufs[m] = prepLoop(b); })
        .catch(function () {})
        .then(function () { loadedN++; if (st && loadedN >= SMP.length) st.hidden = true; });
    });
  }
  function nearest(m) {
    var best = null;
    SMP.forEach(function (k) { if (bufs[k] && (best === null || Math.abs(k - m) < Math.abs(best - m))) best = k; });
    return best !== null && Math.abs(best - m) <= 4 ? best : null;
  }
  function sampleSrc(m, gain, out, t) { // one looping reed at MIDI note m, or null if no sample is near
    var k = nearest(m); if (k === null) return null;
    var b = bufs[k], src = ac.createBufferSource(), g = ac.createGain();
    src.buffer = b; src.loop = true; src.loopStart = b._a; src.loopEnd = b._b;
    src.playbackRate.value = Math.pow(2, (m - k) / 12);
    g.gain.value = gain; src.connect(g); g.connect(out); src.start(t, START + Math.random() * 0.02);
    return src;
  }
  function reed(f, level, plain) {
    var m = Math.round(12 * Math.log(f / 440) / Math.LN2) + 69;
    if (nearest(m) === null) return synthReed(f, level * 0.9);
    var t = ac.currentTime, out = ac.createGain(), srcs = [];
    out.gain.setValueAtTime(0, t); out.gain.setTargetAtTime(level * 2.2, t, 0.012);
    srcs.push(sampleSrc(m, 1, out, t));
    if (!plain && bassOn) srcs.push(sampleSrc(m - 12, 0.55, out, t));   // खरज — the lower reed set
    if (!plain && highOn) srcs.push(sampleSrc(m + 12, 0.32, out, t));   // ऊँची रीड — octave coupler
    out.connect(dry); if (room) out.connect(roomIn);
    return { out: out, stop: function () {
      var n = ac.currentTime;
      out.gain.cancelScheduledValues(n); out.gain.setValueAtTime(out.gain.value, n);
      out.gain.setTargetAtTime(0, n, 0.05);
      srcs.forEach(function (x) { if (x) try { x.stop(n + 0.4); } catch (e) {} });
    } };
  }
  function synthReed(f, level) {
    var t = ac.currentTime, out = ac.createGain();
    out.gain.setValueAtTime(0, t);
    out.gain.setTargetAtTime(level, t, 0.022);           // reed "speaks" quickly but softly
    var srcs = [[waves.mid, f, 0.5], [waves.mid, f * 1.0032, 0.42], [waves.bass, f / 2, 0.3]].map(function (o) {
      var osc = ac.createOscillator(), g = ac.createGain();
      osc.setPeriodicWave(o[0]); osc.frequency.value = o[1]; g.gain.value = o[2];
      osc.connect(g); g.connect(out); osc.start(t); return osc;
    });
    var air = ac.createBufferSource(); air.buffer = noiseBuf; air.loop = true;
    var bp = ac.createBiquadFilter(); bp.type = "bandpass"; bp.frequency.value = 2600; bp.Q.value = 0.7;
    var ag = ac.createGain(); ag.gain.value = 0.05;
    air.connect(bp); bp.connect(ag); ag.connect(out); air.start(t, Math.random());
    srcs.push(air);
    out.connect(bus);
    return { out: out, stop: function () {
      var n = ac.currentTime;
      out.gain.cancelScheduledValues(n); out.gain.setValueAtTime(out.gain.value, n);
      out.gain.setTargetAtTime(0, n, 0.03);
      srcs.forEach(function (o) { try { o.stop(n + 0.25); } catch (e) {} });
    } };
  }
  // ---------- mechanics: key "khat" on press/release, and air through the reeds while sounding ----------
  var hiss = null, hissG = null;
  function clack(down) {
    if (!ac || mech <= 0 || !noiseBuf) return;
    var t = ac.currentTime, n = ac.createBufferSource(), bp = ac.createBiquadFilter(), g = ac.createGain();
    n.buffer = noiseBuf; bp.type = "bandpass"; bp.frequency.value = down ? 1800 : 2600; bp.Q.value = 1.2;
    g.gain.setValueAtTime((down ? 0.5 : 0.25) * mech, t); g.gain.exponentialRampToValueAtTime(0.0001, t + (down ? 0.035 : 0.025));
    n.connect(bp); bp.connect(g); g.connect(master); n.start(t, Math.random() * 0.5); n.stop(t + 0.05);
    if (down) { // wooden thump of the key hitting its bed
      var o = ac.createOscillator(), og = ac.createGain();
      o.frequency.setValueAtTime(190, t); o.frequency.exponentialRampToValueAtTime(70, t + 0.05);
      og.gain.setValueAtTime(0.35 * mech, t); og.gain.exponentialRampToValueAtTime(0.0001, t + 0.06);
      o.connect(og); og.connect(master); o.start(t); o.stop(t + 0.07);
    }
  }
  function air(on) {
    if (!ac || !noiseBuf) return;
    if (!hiss) {
      hiss = ac.createBufferSource(); hiss.buffer = noiseBuf; hiss.loop = true;
      var bp = ac.createBiquadFilter(); bp.type = "bandpass"; bp.frequency.value = 1400; bp.Q.value = 0.6;
      hissG = ac.createGain(); hissG.gain.value = 0; hiss.connect(bp); bp.connect(hissG); hissG.connect(master); hiss.start();
    }
    hissG.gain.setTargetAtTime(on ? 0.06 * mech : 0, ac.currentTime, 0.12);
  }
  function noteOn(s) {
    if (!audio()) return;
    if (voices[s]) return;
    var v = reed(freq(s), 0.2);
    if (coupOn) { // ऑक्टेव कपलर: the key an octave lower goes down with it
      var c = reed(freq(s - 12), 0.16, true), ck = keyEls[s - 12], st = v.stop;
      if (ck) ck.classList.add("coupled");
      v.stop = function () { st(); c.stop(); if (ck) ck.classList.remove("coupled"); };
    }
    voices[s] = v; clack(true);
    var k = keyEls[s]; if (k) k.classList.add("down");
    breathe(); floatNote(s);
    onPlayed(s);
  }
  function noteOff(s) {
    if (voices[s]) { voices[s].stop(); delete voices[s]; clack(false); }
    var k = keyEls[s]; if (k) k.classList.remove("down");
    breathe();
  }
  // a note rises out of the reed cover above the key that was pressed: ♪ + its name
  var GLYPH = ["♪", "♫", "♩", "♬"], flying = 0;
  function floatNote(s) {
    var air = root.querySelector(".hm-air"), k = keyEls[s];
    if (!air || !k || flying > 14) return;
    var kr = k.getBoundingClientRect(), ar = air.getBoundingClientRect();
    var x = Math.max(24, Math.min(ar.width - 24, kr.left + kr.width / 2 - ar.left)), dx = (25 + Math.random() * 30) + "px"; // always drifts the same way, like air leaving the reeds
    var el = document.createElement("span");
    el.className = "hm-fly" + (k.classList.contains("blk") ? " blk" : "");
    el.style.left = x + "px"; el.style.setProperty("--dx", dx);
    el.innerHTML = '<i class="g">' + GLYPH[Math.floor(Math.random() * 4)] + "</i>" + label(s);
    air.appendChild(el); flying++;
    for (var i = 0; i < 3; i++) {
      var p = document.createElement("i"); p.className = "hm-puff";
      p.style.left = (x + Math.random() * 30 - 15) + "px"; p.style.setProperty("--dx", (20 + Math.random() * 30) + "px");
      p.style.animationDelay = (i * 0.09) + "s"; air.appendChild(p);
      setTimeout(p.remove.bind(p), 1300);
    }
    setTimeout(function () { el.remove(); flying--; }, 2000);
  }
  function breathe() {
    var on = Object.keys(voices).length > 0 || !!drone;
    root.classList.toggle("playing", on); air(on);
    root.style.setProperty("--pump", (1.6 - Math.min(3, Object.keys(voices).length) * 0.3) + "s");
  }
  function allOff() { Object.keys(voices).forEach(function (s) { noteOff(+s); }); }
  function setDrone(on) {
    if (drone) { drone.forEach(function (v) { v.stop(); }); drone = null; }
    if (on && audio()) drone = [reed(freq(-12), 0.06, true), reed(freq(-5), 0.045, true)];
    breathe();
  }

  // ---------- UI ----------
  var LO = -12, HI = 19; // मंद्र सा … तार प
  function isBlack(s) { return [1, 3, 6, 8, 10].indexOf(((saPc + s) % 12 + 12) % 12) >= 0; }
  var KEYMAP = { z: -5, x: -3, c: -1, a: 0, w: 1, s: 2, e: 3, d: 4, f: 5, t: 6, g: 7, y: 8, h: 9, u: 10, j: 11,
    k: 12, o: 13, l: 14, p: 15, ";": 16, "'": 17 };
  var KEYOF = {}; Object.keys(KEYMAP).forEach(function (k) { KEYOF[KEYMAP[k]] = k; });

  var opts = SCALES.map(function (n, i) { return '<option value="' + i + '"' + (i === saPc ? " selected" : "") + ">" + n + "</option>"; }).join("");
  var songOpts = '<option value="">— खुला बजाएँ (कोई गाना नहीं) —</option>' +
    songs.map(function (sg) { return '<option value="' + sg.id + '">' + sg.title + "</option>"; }).join("");
  function stopKnob(cls, text, on) {
    return '<label class="stop"><input type="checkbox" class="' + cls + '"' + (on ? " checked" : "") + '><span class="knob" aria-hidden="true"></span><span class="stop-l">' + text + "</span></label>";
  }
  var kw = typeof store.kw === "number" ? store.kw : (window.innerWidth < 640 ? 46 : 58); // white-key width (zoom)
  function seg(cls, cur, items) {
    return '<div class="seg ' + cls + '" role="group">' + items.map(function (it) {
      return '<button type="button" data-v="' + it[0] + '" aria-pressed="' + (it[0] === cur) + '">' + it[1] + "</button>";
    }).join("") + "</div>";
  }
  root.innerHTML =
    '<div class="hm-inst">' +
    '<div class="hm-bellows" aria-hidden="true"><div class="hm-pleats"></div><span class="hm-pumphint">↕ धौंकनी चलाएँ</span></div>' +
    '<i class="screw tl"></i><i class="screw tr"></i><i class="screw bl"></i><i class="screw br"></i>' +
    '<div class="hm-top wood" aria-hidden="true"><div class="hm-cover"></div><div class="hm-ad" hidden><small>विज्ञापन</small><div class="hm-ad-slot"></div></div><div class="hm-air"></div></div>' +
    '<div class="hm-rail wood">' +
    '<button type="button" class="rbtn hm-menu" aria-label="हारमोनियम सेटिंग्स खोलें" aria-expanded="false"><span class="bars"></span></button>' +
    '<button type="button" class="rbtn hm-dronebtn" aria-pressed="false" title="सा-प ड्रोन">सा·प</button>' +
    '<span class="hm-airmeter" hidden title="धौंकनी में हवा"><i></i></span>' +
    (data.app ? '<button type="button" class="rbtn hm-songsbtn" aria-expanded="false">♪ गाने</button>' : "") +
    '<div class="hm-nav"><input type="range" class="hm-navr" min="0" max="1000" value="0" aria-label="पट्टियाँ खिसकाएँ (सप्तक)"><div class="hm-navnums" aria-hidden="true"></div></div>' +
    '<button type="button" class="rbtn hm-zout" aria-label="पट्टियाँ छोटी करें">−</button>' +
    '<button type="button" class="rbtn hm-zin" aria-label="पट्टियाँ बड़ी करें">+</button>' +
    "</div>" +
    '<div class="hm-felt" aria-hidden="true"></div>' +
    '<div class="hm-keybed"><div class="hm-cheek" aria-hidden="true"><span class="brand-v">OmKiran</span></div>' +
    '<div class="hm-kbd-wrap"><div class="hm-kbd" role="group" aria-label="हारमोनियम की पट्टियाँ"></div></div>' +
    '<div class="hm-cheek" aria-hidden="true"><span class="brand-v">OmKiran</span></div></div>' +
    '<div class="hm-drawer wood" hidden>' +
    '<div class="dr-head"><b>हारमोनियम</b><button type="button" class="rbtn sm hm-close" aria-label="सेटिंग्स बंद करें">×</button></div>' +
    '<div class="dr-grid"><div class="dr-col">' +
    '<label class="dr-row">आवाज़ <input type="range" class="hm-volr" min="0" max="1" step="0.05" value="' + vol + '"></label>' +
    '<div class="dr-row">सा का सुर<div class="dr-scale"><button type="button" class="rbtn sm hm-sdown" aria-label="सुर नीचे">−</button>' +
    '<select class="hm-sa" aria-label="सा किस पट्टी पर">' + opts + '</select><button type="button" class="rbtn sm hm-sup" aria-label="सुर ऊपर">+</button></div></div>' +
    '<div class="dr-row">पट्टी पर नाम' + seg("hm-names", names, [["sargam", "रे ग"], ["west", "C D E"], ["both", "दोनों"]]) + "</div>" +
    '<label class="dr-row" title="पट्टी की खट और धौंकनी की हवा — असली हारमोनियम जैसा एहसास">खटके की आवाज़ <input type="range" class="hm-mech" min="0" max="1" step="0.05" value="' + mech + '" aria-label="खटके की आवाज़"></label>' +
    '</div><div class="dr-col">' +
    '<div class="dr-row">स्टॉप<div class="dr-stops">' +
    stopKnob("hm-bass", "खरज", bassOn) + stopKnob("hm-coup", "कपलर", coupOn) + stopKnob("hm-high", "ऊँची रीड", highOn) +
    stopKnob("hm-echo", "गूँज", echoOn) + stopKnob("hm-drone", "ड्रोन", false) + stopKnob("hm-showkeys", "अक्षर", showKeys) + "</div></div>" +
    '<div class="dr-row dr-adv">एडवांस्ड' +
    '<label class="dr-inline" title="ऊपर की धौंकनी को उँगली/माउस से ऊपर-नीचे खींचें, या कंप्यूटर पर Space दबाते रहें। हवा ख़त्म तो आवाज़ भी बंद।"><input type="checkbox" class="hm-pump"' + (pumpMode ? " checked" : "") + '> धौंकनी ख़ुद चलाएँ</label>' +
    '<div class="dr-inline"><button type="button" class="hm-midi hm-mini">MIDI कीबोर्ड जोड़ें</button><small class="hm-midist">Chrome / Edge में</small></div>' +
    '</div></div></div>' +
    '<p class="dr-note">आवाज़: असली हारमोनियम की रिकॉर्डिंग (CC0)। कपलर: हर पट्टी के साथ एक सप्तक नीचे वाली पट्टी भी बजती है।</p>' +
    "</div>" +
    "</div>" +
    '<p class="hm-rotate">📱 फ़ोन को आड़ा (लैंडस्केप) करें — पट्टियाँ बड़ी दिखेंगी।</p>' +
    '<p class="hm-load" hidden>असली हारमोनियम की आवाज़ लोड हो रही है…</p><p class="hm-hint">पट्टी पर उँगली या माउस रखें। कंप्यूटर पर <b>A S D F G H J K</b> = सा रे ग म प ध नि सां, ऊपर की लाइन (W E T Y U) = काली पट्टियाँ।</p>' +
    (songs.length ?
      '<div class="hm-song">' +
      '<div class="hm-bar"><label class="hm-pick">गाना <select class="hm-songsel" aria-label="गाना चुनें">' + songOpts + "</select></label>" +
      '<button type="button" class="hm-btn hm-play">▶ बजाएँ</button>' +
      '<button type="button" class="hm-btn hm-practice" title="जब तक सही पट्टी न दबाएँ, आगे नहीं बढ़ेगा">✋ अभ्यास मोड</button></div>' +
      '<div class="hm-bar"><label class="hm-tempo">रफ़्तार <input type="range" min="40" max="150" step="5" value="100" aria-label="रफ़्तार (असली का प्रतिशत)"><span class="hm-bpm"></span></label>' +
      '<button type="button" class="hm-mini hm-reset">असली रफ़्तार</button>' +
      '<label class="hm-chk"><input type="checkbox" class="hm-loop"> चुनी पंक्ति दोहराएँ</label></div>' +
      '<p class="hm-status" aria-live="polite"></p><ol class="hm-lines"></ol></div>' : "");

  // ---------- procedural textures: teak grain and ivory (drawn once, no image files) ----------
  (function textures() {
    try {
      function noise(w, h, seed) { var g = [], r = seed; for (var i = 0; i < w * h; i++) { r = (r * 16807) % 2147483647; g.push(r / 2147483647); } return g; }
      function smooth(g, gw, gh, x, y) {
        var x0 = Math.floor(x) % gw, y0 = Math.floor(y) % gh, x1 = (x0 + 1) % gw, y1 = (y0 + 1) % gh, fx = x - Math.floor(x), fy = y - Math.floor(y);
        fx = fx * fx * (3 - 2 * fx); fy = fy * fy * (3 - 2 * fy);
        var a = g[y0 * gw + x0], b = g[y0 * gw + x1], c = g[y1 * gw + x0], d = g[y1 * gw + x1];
        return a + (b - a) * fx + (c - a) * fy + (a - b - c + d) * fx * fy;
      }
      var W = 512, H = 256, cv = document.createElement("canvas"); cv.width = W; cv.height = H;
      var cx = cv.getContext("2d"), im = cx.createImageData(W, H), g1 = noise(32, 32, 7), g2 = noise(64, 64, 11);
      for (var y = 0; y < H; y++) for (var x = 0; x < W; x++) {
        var n = smooth(g1, 32, 32, x / 64, y / 16) * 2 + smooth(g2, 64, 64, x / 9, y / 3) * 0.6;
        var ring = Math.sin((y / H) * 38 + n * 5.5), fine = smooth(g2, 64, 64, x / 2.5, y / 0.9);
        var v = 0.55 + 0.22 * ring + 0.12 * (fine - 0.5) + 0.08 * (n - 1);
        var i = (y * W + x) * 4;
        im.data[i] = 120 + 110 * v; im.data[i + 1] = 58 + 62 * v; im.data[i + 2] = 14 + 26 * v; im.data[i + 3] = 255;
      }
      cx.putImageData(im, 0, 0);
      root.style.setProperty("--wood", "url(" + cv.toDataURL("image/jpeg", 0.85) + ")");
      var iv = document.createElement("canvas"); iv.width = iv.height = 128; var ic = iv.getContext("2d"), ii = ic.createImageData(128, 128);
      for (var k = 0; k < ii.data.length; k += 4) { var q = 236 + Math.random() * 14; ii.data[k] = q + 6; ii.data[k + 1] = q + 1; ii.data[k + 2] = q - 16; ii.data[k + 3] = 255; }
      ic.putImageData(ii, 0, 0);
      root.style.setProperty("--ivory-tex", "url(" + iv.toDataURL("image/jpeg", 0.9) + ")");
    } catch (e) {}
  })();
  var kbd = root.querySelector(".hm-kbd"), keyEls = {};
  function drawKeys() {
    kbd.innerHTML = "";
    keyEls = {};
    var lo = isBlack(LO) ? LO - 1 : LO, hi = isBlack(HI) ? HI + 1 : HI, whites = 0, html = "";
    for (var s = lo; s <= hi; s++) if (!isBlack(s)) whites++;
    var w = 100 / whites, wi = 0;
    for (s = lo; s <= hi; s++) {
      var b = isBlack(s), kb = KEYOF[s] ? '<i class="kk">' + KEYOF[s].toUpperCase() + "</i>" : "";
      var style = b ? "left:" + (wi * w - w * 0.3) + "%;width:" + (w * 0.6) + "%" : "width:" + w + "%";
      html += '<button type="button" tabindex="-1" class="key ' + (b ? "blk" : "wht") + (s === 0 ? " sa" : "") + '" data-s="' + s +
        '" style="' + style + '" aria-label="' + plain(s) + '">' + label(s) + kb + "</button>";
      if (!b) wi++;
    }
    kbd.innerHTML = html;
    kbd.style.width = (whites * kw) + "px";
    Array.prototype.forEach.call(kbd.querySelectorAll(".key"), function (k) { keyEls[+k.dataset.s] = k; });
    root.classList.toggle("nokeys", !showKeys);
    var nums = root.querySelector(".hm-navnums"), total = whites * kw;
    nums.innerHTML = [[-12, "मंद्र"], [0, "मध्य"], [12, "तार"]].map(function (x) {
      var k = keyEls[x[0]]; return k ? '<span style="left:' + (100 * k.offsetLeft / total) + '%">' + x[1] + "</span>" : "";
    }).join("");
    centerSa();
  }
  var wrap = root.querySelector(".hm-kbd-wrap"), navr = root.querySelector(".hm-navr");
  function centerSa() {
    var k = keyEls[0]; if (!k) return;
    wrap.scrollLeft = Math.max(0, k.offsetLeft - kw * 2.5); syncNav();
  }
  function syncNav() {
    var max = wrap.scrollWidth - wrap.clientWidth;
    navr.disabled = max <= 0; navr.value = max > 0 ? Math.round(1000 * wrap.scrollLeft / max) : 0;
  }
  wrap.addEventListener("scroll", syncNav, { passive: true });
  navr.addEventListener("input", function () { wrap.scrollLeft = (wrap.scrollWidth - wrap.clientWidth) * this.value / 1000; });
  window.addEventListener("resize", syncNav);
  function zoom(d) { kw = Math.max(34, Math.min(90, kw + d)); store.kw = kw; save(); drawKeys(); }
  root.querySelector(".hm-zin").addEventListener("click", function () { zoom(8); });
  root.querySelector(".hm-zout").addEventListener("click", function () { zoom(-8); });
  // drawer
  var drawer = root.querySelector(".hm-drawer"), menuBtn = root.querySelector(".hm-menu");
  function openDrawer(on) { drawer.hidden = !on; menuBtn.setAttribute("aria-expanded", on); if (on) root.querySelector(".hm-close").focus(); }
  menuBtn.addEventListener("click", function () { openDrawer(drawer.hidden); });
  root.querySelector(".hm-close").addEventListener("click", function () { openDrawer(false); menuBtn.focus(); });
  drawer.addEventListener("keydown", function (ev) { if (ev.key === "Escape") { openDrawer(false); menuBtn.focus(); } });
  drawKeys();

  // pointer: press, slide across keys, release
  var down = null;
  function sOf(el) { var k = el && el.closest && el.closest(".key"); return k ? +k.dataset.s : null; }
  kbd.addEventListener("pointerdown", function (ev) {
    var s = sOf(ev.target); if (s === null) return;
    ev.preventDefault(); down = s; noteOn(s);
    try { kbd.releasePointerCapture(ev.pointerId); } catch (e) {}
  });
  kbd.addEventListener("pointerover", function (ev) {
    if (down === null) return;
    var s = sOf(ev.target); if (s === null || s === down) return;
    noteOff(down); down = s; noteOn(s);
  });
  function release() { if (down !== null) { noteOff(down); down = null; } }
  window.addEventListener("pointerup", release);
  window.addEventListener("pointercancel", release);
  kbd.addEventListener("contextmenu", function (ev) { ev.preventDefault(); });

  // computer keyboard
  function typing(ev) { var t = ev.target; return t && (t.tagName === "INPUT" && t.type !== "range" && t.type !== "checkbox" || t.tagName === "TEXTAREA" || t.isContentEditable); }
  document.addEventListener("keydown", function (ev) {
    if (ev.repeat || ev.ctrlKey || ev.metaKey || ev.altKey || typing(ev)) return;
    var s = KEYMAP[ev.key.toLowerCase()]; if (s === undefined) return;
    if (ev.target.tagName === "SELECT") return;
    ev.preventDefault(); noteOn(s);
  });
  document.addEventListener("keyup", function (ev) { var s = KEYMAP[ev.key.toLowerCase()]; if (s !== undefined) noteOff(s); });
  window.addEventListener("blur", allOff);

  // controls
  root.querySelector(".hm-sa").addEventListener("change", function () {
    saPc = +this.value; store.sa = saPc; save(); allOff(); drawKeys(); if (window._hmRelabel) window._hmRelabel();
    var d = root.querySelector(".hm-drone"); if (d.checked) setDrone(true);
  });
  root.querySelector(".hm-volr").addEventListener("input", function () {
    vol = +this.value; store.vol = vol; save(); if (master) master.gain.value = vol * airGain();
  });
  root.querySelector(".hm-mech").addEventListener("input", function () {
    mech = +this.value; store.mech = mech; save(); breathe();
  });
  // ---------- MIDI input (Web MIDI: Chrome, Edge, Opera; not Safari/Firefox) ----------
  var midiBtn = root.querySelector(".hm-midi"), midiSt = root.querySelector(".hm-midist"), midiOn = {};
  function midiMsg(ev) {
    var d = ev.data, cmd = d[0] & 0xf0, note = d[1], vel = d[2];
    var s = note - 60 - saPc; // middle C on the controller = मध्य सा when सा is सफ़ेद 1
    if (cmd === 0x90 && vel > 0) { audio(); midiOn[note] = s; noteOn(s); }
    else if (cmd === 0x80 || (cmd === 0x90 && vel === 0)) { if (note in midiOn) { noteOff(midiOn[note]); delete midiOn[note]; } }
  }
  midiBtn.addEventListener("click", function () {
    if (!navigator.requestMIDIAccess) { midiSt.textContent = "यह ब्राउज़र MIDI नहीं चलाता — कंप्यूटर पर Chrome या Edge में खोलें।"; return; }
    audio();
    navigator.requestMIDIAccess().then(function (acc) {
      function hook() {
        var names = [];
        acc.inputs.forEach(function (inp) { inp.onmidimessage = midiMsg; names.push(inp.name); });
        midiSt.textContent = names.length ? "जुड़ा: " + names.join(", ") + " — अब बजाइए।" : "कोई MIDI कीबोर्ड नहीं मिला। केबल लगाकर फिर दबाएँ।";
        midiBtn.textContent = names.length ? "MIDI जुड़ा ✓" : "MIDI कीबोर्ड जोड़ें";
      }
      hook(); acc.onstatechange = hook;
    }, function () { midiSt.textContent = "MIDI की अनुमति नहीं मिली। ब्राउज़र की अनुमति देकर फिर कोशिश करें।"; });
  });
  var droneChk = root.querySelector(".hm-drone"), droneBtn = root.querySelector(".hm-dronebtn");
  function droneTo(on) { droneChk.checked = on; droneBtn.setAttribute("aria-pressed", on); setDrone(on); }
  droneChk.addEventListener("change", function () { droneTo(this.checked); });
  droneBtn.addEventListener("click", function () { droneTo(!droneChk.checked); });
  function stepSa(d) { var sel = root.querySelector(".hm-sa"); sel.value = (saPc + d + 12) % 12; sel.dispatchEvent(new Event("change")); }
  root.querySelector(".hm-sup").addEventListener("click", function () { stepSa(1); });
  root.querySelector(".hm-sdown").addEventListener("click", function () { stepSa(-1); });
  root.querySelector(".hm-names").addEventListener("click", function (ev) {
    var b = ev.target.closest("button"); if (!b) return;
    names = b.dataset.v; store.names = names; save();
    Array.prototype.forEach.call(this.querySelectorAll("button"), function (x) { x.setAttribute("aria-pressed", x === b); });
    drawKeys(); if (window._hmRelabel) window._hmRelabel();
  });
  root.querySelector(".hm-bass").addEventListener("change", function () { bassOn = this.checked; store.bass = bassOn; save(); });
  root.querySelector(".hm-coup").addEventListener("change", function () { coupOn = this.checked; store.coup = coupOn; save(); });
  root.querySelector(".hm-high").addEventListener("change", function () { highOn = this.checked; store.high = highOn; save(); });
  root.querySelector(".hm-echo").addEventListener("change", function () {
    echoOn = this.checked; store.echo = echoOn; save(); if (roomWet) roomWet.gain.value = echoOn ? 0.28 : 0;
  });
  root.querySelector(".hm-showkeys").addEventListener("change", function () {
    showKeys = this.checked; store.keys = showKeys; save(); root.classList.toggle("nokeys", !showKeys);
  });

  // ---------- ad slot (only when the page turns ads on — after AdSense approval) ----------
  var ad = root.querySelector(".hm-ad");
  if (!(data.ads && data.adClient && data.adSlot)) { if (ad) ad.remove(); }
  else {
    ad.hidden = false;
    ad.querySelector(".hm-ad-slot").innerHTML = '<ins class="adsbygoogle" style="display:inline-block;width:320px;height:50px" data-ad-client="' + data.adClient + '" data-ad-slot="' + data.adSlot + '"></ins>';
    try { (window.adsbygoogle = window.adsbygoogle || []).push({}); } catch (e) {}
    root.classList.add("has-ad");
  }

  // ---------- bellows: pump-yourself mode ----------
  var bel = root.querySelector(".hm-bellows"), meter = root.querySelector(".hm-airmeter"), meterBar = meter.querySelector("i");
  function airGain() { return pumpMode ? Math.min(1, airLvl / 0.3) : 1; }
  function applyAir() {
    if (master) master.gain.setTargetAtTime(vol * airGain(), ac.currentTime, 0.05);
    meterBar.style.height = Math.round(airLvl * 100) + "%";
    bel.style.setProperty("--open", pumpMode ? airLvl : 1);
  }
  function pumpIn(x) { airLvl = Math.min(1, airLvl + x); bel.classList.add("pumping"); clearTimeout(bel._t); bel._t = setTimeout(function () { bel.classList.remove("pumping"); }, 180); applyAir(); }
  var last = performance.now();
  (function leak(now) {
    var dt = Math.min(0.1, (now - last) / 1000); last = now;
    if (pumpMode) { var n = Object.keys(voices).length + (drone ? 1 : 0); airLvl = Math.max(0, airLvl - dt * (0.02 + 0.075 * n)); applyAir(); }
    requestAnimationFrame(leak);
  })(last);
  var belY = null;
  bel.addEventListener("pointerdown", function (ev) { if (!pumpMode) return; ev.preventDefault(); audio(); belY = ev.clientY; try { bel.setPointerCapture(ev.pointerId); } catch (e) {} });
  bel.addEventListener("pointermove", function (ev) { if (belY === null) return; var d = Math.abs(ev.clientY - belY); belY = ev.clientY; if (d) pumpIn(d * 0.006); });
  bel.addEventListener("pointerup", function () { belY = null; });
  bel.addEventListener("pointercancel", function () { belY = null; });
  document.addEventListener("keydown", function (ev) {
    if (!pumpMode || ev.code !== "Space" || typing(ev) || ev.target.tagName === "BUTTON" || ev.target.tagName === "SELECT") return;
    ev.preventDefault(); if (!ev.repeat) pumpIn(0.22); else pumpIn(0.05);
  });
  function setPump(on) {
    pumpMode = on; store.pump = on; save(); airLvl = on ? 0.6 : 1;
    root.classList.toggle("pumpmode", on); meter.hidden = !on; applyAir();
  }
  root.querySelector(".hm-pump").addEventListener("change", function () { setPump(this.checked); });
  setPump(pumpMode);

  // start fetching the recorded sound early (the context stays silent until the first tap)
  setTimeout(function () { try { audio(); } catch (e) {} }, 600);

  // ---------- song player ----------
  if (!songs.length) return;
  var sel = root.querySelector(".hm-songsel"), linesEl = root.querySelector(".hm-lines"), status = root.querySelector(".hm-status");
  var playBtn = root.querySelector(".hm-play"), pracBtn = root.querySelector(".hm-practice");
  var tempo = root.querySelector(".hm-tempo input"), bpmEl = root.querySelector(".hm-bpm"), loopEl = root.querySelector(".hm-loop");
  var song = null, lines = [], cur = { l: 0, i: 0 }, timer = null, mode = null, chipEls = [];
  function showSpeed() { bpmEl.textContent = speed + "%" + (speed === 100 ? " (असली)" : ""); tempo.value = speed; }
  showSpeed();

  function loadSong(id) {
    stop();
    song = null; lines = []; linesEl.innerHTML = ""; chipEls = [];
    songs.forEach(function (sg) { if (sg.id === id) song = sg; });
    playBtn.disabled = pracBtn.disabled = !song;
    if (!song) { status.textContent = "ऊपर से कोई गाना चुनें, या पट्टियों पर खुला बजाएँ।"; return; }
    speed = 100; showSpeed();
    lines = song.lines.map(function (ln) { return { t: ln.t, notes: parse(ln.n) }; });
    renderLines();
    cur = { l: 0, i: 0 }; mark();
    status.textContent = "▶ बजाएँ से धुन सुनें, या ✋ अभ्यास मोड में ख़ुद बजाएँ। किसी पंक्ति पर टैप करके वहाँ से शुरू करें।";
  }
  function renderLines() {
    linesEl.innerHTML = lines.map(function (ln, li) {
      return '<li data-l="' + li + '"><p class="hm-lyric">' + ln.t + '</p><p class="hm-notes">' +
        ln.notes.map(function (n, ni) { return '<span class="chip" data-i="' + ni + '">' + label(n.s) + (n.dur > 1 ? '<i class="hold">' + new Array(n.dur).join("–") + "</i>" : "") + "</span>"; }).join("") +
        "</p></li>";
    }).join("");
    chipEls = lines.map(function (ln, li) { return linesEl.querySelectorAll('li[data-l="' + li + '"] .chip'); });
  }
  window._hmRelabel = function () { if (song) { renderLines(); mark(); } };
  function mark() {
    Array.prototype.forEach.call(linesEl.querySelectorAll(".chip.on, li.on"), function (x) { x.classList.remove("on"); });
    Array.prototype.forEach.call(root.querySelectorAll(".key.next"), function (x) { x.classList.remove("next"); });
    var li = linesEl.querySelector('li[data-l="' + cur.l + '"]'); if (li) li.classList.add("on");
    var c = chipEls[cur.l] && chipEls[cur.l][cur.i]; if (c) c.classList.add("on");
    var n = lines[cur.l] && lines[cur.l].notes[cur.i];
    if (n && keyEls[n.s]) keyEls[n.s].classList.add("next");
  }
  function advance() {
    cur.i++;
    if (cur.i >= lines[cur.l].notes.length) {
      cur.i = 0;
      if (!loopEl.checked) cur.l++;
      if (cur.l >= lines.length) { cur.l = 0; mark(); stop(); status.textContent = "🙏 पूरा हुआ! फिर से बजाने के लिए ▶ दबाएँ।"; return false; }
    }
    return true;
  }
  function step() {
    var n = lines[cur.l].notes[cur.i], beat = 60000 / ((song.bpm || 120) * speed / 100);
    mark(); noteOn(n.s);
    var len = n.dur * beat;
    timer = setTimeout(function () {
      noteOff(n.s);
      if (mode !== "play") return;
      if (advance()) timer = setTimeout(step, 30);
    }, len - 30);
  }
  function stop() {
    clearTimeout(timer); timer = null; mode = null; allOff();
    playBtn.textContent = "▶ बजाएँ"; pracBtn.textContent = "✋ अभ्यास मोड";
    playBtn.classList.remove("on"); pracBtn.classList.remove("on");
  }
  function prompt() {
    var n = lines[cur.l].notes[cur.i];
    status.innerHTML = "अब दबाएँ: <b>" + plain(n.s) + "</b>" + (showKeys && KEYOF[n.s] ? " (कीबोर्ड पर " + KEYOF[n.s].toUpperCase() + ")" : "");
  }
  var played = false;
  function onPlayed(s) {
    if (mode !== "practice" || played) return;
    var n = lines[cur.l].notes[cur.i];
    if (s !== n.s) { status.innerHTML = "यह " + plain(s) + " है — <b>" + plain(n.s) + "</b> दबाएँ (चमकती पट्टी)।"; return; }
    played = true;
    setTimeout(function () {
      played = false;
      if (mode !== "practice") return;
      if (advance()) { mark(); prompt(); }
    }, 60);
  }
  playBtn.addEventListener("click", function () {
    if (mode === "play") { stop(); status.textContent = "रुका हुआ। ▶ से वहीं से आगे बजेगा।"; return; }
    stop(); if (!audio()) return;
    mode = "play"; playBtn.textContent = "⏸ रोकें"; playBtn.classList.add("on");
    status.textContent = "धुन बज रही है — चमकती पट्टी देखते रहें।"; step();
  });
  pracBtn.addEventListener("click", function () {
    if (mode === "practice") { stop(); status.textContent = "अभ्यास रोका।"; return; }
    stop(); audio();
    mode = "practice"; pracBtn.textContent = "✋ अभ्यास बंद करें"; pracBtn.classList.add("on");
    mark(); prompt();
  });
  tempo.addEventListener("input", function () { speed = +this.value; showSpeed(); });
  root.querySelector(".hm-reset").addEventListener("click", function () { speed = 100; showSpeed(); });
  linesEl.addEventListener("click", function (ev) {
    var li = ev.target.closest("li"); if (!li) return;
    var chip = ev.target.closest(".chip");
    var wasPlaying = mode;
    stop();
    cur = { l: +li.dataset.l, i: chip ? +chip.dataset.i : 0 }; mark();
    if (wasPlaying === "practice") { mode = "practice"; pracBtn.textContent = "✋ अभ्यास बंद करें"; pracBtn.classList.add("on"); prompt(); }
    else status.textContent = "यहीं से शुरू होगा — ▶ बजाएँ या ✋ अभ्यास मोड दबाएँ।";
  });
  sel.addEventListener("change", function () { loadSong(this.value); });
  var start = data.start || "";
  sel.value = start; loadSong(start);
  window.hmLoadSong = function (id) { sel.value = id; loadSong(id); };
  if (data.app) {
    var sb = root.querySelector(".hm-songsbtn"), sheet = root.querySelector(".hm-song");
    root.classList.add("app");
    sb.addEventListener("click", function () { var o = !root.classList.contains("sheet"); root.classList.toggle("sheet", o); sb.setAttribute("aria-expanded", o); });
  }
})();

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
  var bassOn = store.bass !== false, highOn = !!store.high, echoOn = store.echo !== false;
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
      master = ac.createGain(); master.gain.value = vol;
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
  var SMP = [43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,67,68,69,70,71,72,73,74];
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
  function noteOn(s) {
    if (!audio()) return;
    if (voices[s]) return;
    voices[s] = reed(freq(s), 0.2);
    var k = keyEls[s]; if (k) k.classList.add("down");
    breathe();
    onPlayed(s);
  }
  function noteOff(s) {
    if (voices[s]) { voices[s].stop(); delete voices[s]; }
    var k = keyEls[s]; if (k) k.classList.remove("down");
    breathe();
  }
  function breathe() { root.classList.toggle("playing", Object.keys(voices).length > 0 || !!drone); }
  function allOff() { Object.keys(voices).forEach(function (s) { noteOff(+s); }); }
  function setDrone(on) {
    if (drone) { drone.forEach(function (v) { v.stop(); }); drone = null; }
    if (on && audio()) drone = [reed(freq(-12), 0.06, true), reed(freq(-5), 0.045, true)];
    breathe();
  }

  // ---------- UI ----------
  var LO = -5, HI = 19; // मंद्र प … तार प
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
  root.innerHTML =
    '<div class="hm-case">' +
    '<div class="hm-bellows" aria-hidden="true"><i class="hm-strap"></i></div>' +
    '<div class="hm-stops">' +
    '<label class="plate">सा का सुर <select class="hm-sa" aria-label="सा किस पट्टी पर">' + opts + "</select></label>" +
    '<label class="plate hm-vol">आवाज़ <input type="range" min="0" max="1" step="0.05" value="' + vol + '" aria-label="आवाज़"></label>' +
    '<label class="plate">पट्टी पर नाम <select class="hm-names" aria-label="पट्टी पर कौन से नाम दिखें">' +
    '<option value="sargam"' + (names === "sargam" ? " selected" : "") + '>सा रे ग (सरगम)</option>' +
    '<option value="west"' + (names === "west" ? " selected" : "") + '>C D E (अंग्रेज़ी)</option>' +
    '<option value="both"' + (names === "both" ? " selected" : "") + '>दोनों</option></select></label>' +
    '<span class="hm-knobs">' +
    stopKnob("hm-bass", "खरज", bassOn) + stopKnob("hm-high", "ऊँची रीड", highOn) + stopKnob("hm-echo", "गूँज", echoOn) +
    stopKnob("hm-drone", "सा-प ड्रोन", false) + stopKnob("hm-showkeys", "कीबोर्ड अक्षर", showKeys) + "</span>" +
    "</div>" +
    '<div class="hm-felt" aria-hidden="true"></div>' +
    '<div class="hm-kbd-wrap"><div class="hm-kbd" role="group" aria-label="हारमोनियम की पट्टियाँ"></div></div>' +
    '<div class="hm-grille" aria-hidden="true"><span class="hm-nameplate">OmKiran Bhakti</span></div>' +
    "</div>" +
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
    kbd.style.minWidth = (whites * 36) + "px";
    Array.prototype.forEach.call(kbd.querySelectorAll(".key"), function (k) { keyEls[+k.dataset.s] = k; });
    root.classList.toggle("nokeys", !showKeys);
    var saKey = keyEls[0], wrap = root.querySelector(".hm-kbd-wrap");
    if (saKey && wrap.scrollWidth > wrap.clientWidth) wrap.scrollLeft = saKey.offsetLeft - 40;
  }
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
  root.querySelector(".hm-vol input").addEventListener("input", function () {
    vol = +this.value; store.vol = vol; save(); if (master) master.gain.value = vol;
  });
  root.querySelector(".hm-drone").addEventListener("change", function () { setDrone(this.checked); });
  root.querySelector(".hm-names").addEventListener("change", function () {
    names = this.value; store.names = names; save(); drawKeys(); if (window._hmRelabel) window._hmRelabel();
  });
  root.querySelector(".hm-bass").addEventListener("change", function () { bassOn = this.checked; store.bass = bassOn; save(); });
  root.querySelector(".hm-high").addEventListener("change", function () { highOn = this.checked; store.high = highOn; save(); });
  root.querySelector(".hm-echo").addEventListener("change", function () {
    echoOn = this.checked; store.echo = echoOn; save(); if (roomWet) roomWet.gain.value = echoOn ? 0.28 : 0;
  });
  root.querySelector(".hm-showkeys").addEventListener("change", function () {
    showKeys = this.checked; store.keys = showKeys; save(); root.classList.toggle("nokeys", !showKeys);
  });

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
})();

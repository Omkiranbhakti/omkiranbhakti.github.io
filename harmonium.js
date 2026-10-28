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
  function label(s) { // sargam label with octave + komal/tivra classes
    var pc = ((s % 12) + 12) % 12, oct = Math.floor(s / 12);
    var cls = (KOMAL[pc] ? " komal" : "") + (TIVRA[pc] ? " tivra" : "") + (oct < 0 ? " low" : oct > 0 ? " high" : "");
    return '<span class="sw' + cls + '">' + NAME[pc] + "</span>";
  }
  function plain(s) {
    var pc = ((s % 12) + 12) % 12, oct = Math.floor(s / 12);
    return (oct < 0 ? "मंद्र " : oct > 0 ? "तार " : "") + NAME[pc] + (KOMAL[pc] ? " (कोमल)" : TIVRA[pc] ? " (तीव्र)" : "");
  }

  // ---------- settings ----------
  var store = {};
  try { store = JSON.parse(localStorage.getItem("okb-hm") || "{}"); } catch (e) {}
  function save() { try { localStorage.setItem("okb-hm", JSON.stringify(store)); } catch (e) {} }
  var saPc = typeof store.sa === "number" ? store.sa : 0;          // 0 = C (सफ़ेद 1)
  var vol = typeof store.vol === "number" ? store.vol : 0.5;
  var bpm = typeof store.bpm === "number" ? store.bpm : 70;
  var showKeys = store.keys !== false;
  var SCALES = ["सफ़ेद 1 (C)", "काली 1 (C#)", "सफ़ेद 2 (D)", "काली 2 (D#)", "सफ़ेद 3 (E)", "सफ़ेद 4 (F)",
    "काली 3 (F#)", "सफ़ेद 5 (G)", "काली 4 (G#)", "सफ़ेद 6 (A)", "काली 5 (A#)", "सफ़ेद 7 (B)"];

  // ---------- sound: two detuned reeds + a soft bass reed, filtered, with gentle bellows tremolo ----------
  var ac = null, master = null, voices = {}, drone = null;
  function audio() {
    if (!ac) {
      var AC = window.AudioContext || window.webkitAudioContext;
      if (!AC) return null;
      ac = new AC();
      master = ac.createGain(); master.gain.value = vol;
      var comp = ac.createDynamicsCompressor();
      master.connect(comp); comp.connect(ac.destination);
    }
    if (ac.state === "suspended") ac.resume();
    return ac;
  }
  function freq(s) { return 261.6256 * Math.pow(2, (saPc + s) / 12); } // सा = C4 … B4
  function reed(f, level) {
    var t = ac.currentTime, out = ac.createGain();
    out.gain.setValueAtTime(0, t);
    out.gain.linearRampToValueAtTime(level, t + 0.045);
    var lp = ac.createBiquadFilter(); lp.type = "lowpass"; lp.frequency.value = Math.min(4200, f * 7); lp.Q.value = 0.6;
    var trem = ac.createGain(); trem.gain.value = 1;
    var lfo = ac.createOscillator(), lfoG = ac.createGain();
    lfo.frequency.value = 5.2; lfoG.gain.value = 0.035; lfo.connect(lfoG); lfoG.connect(trem.gain);
    var oscs = [["sawtooth", f, 0.5], ["sawtooth", f * 1.0035, 0.38], ["square", f / 2, 0.16]].map(function (o) {
      var osc = ac.createOscillator(), g = ac.createGain();
      osc.type = o[0]; osc.frequency.value = o[1]; g.gain.value = o[2];
      osc.connect(g); g.connect(lp); osc.start(t); return osc;
    });
    lfo.start(t);
    lp.connect(trem); trem.connect(out); out.connect(master);
    return { out: out, stop: function () {
      var n = ac.currentTime;
      out.gain.cancelScheduledValues(n); out.gain.setValueAtTime(out.gain.value, n);
      out.gain.linearRampToValueAtTime(0, n + 0.16);
      oscs.concat([lfo]).forEach(function (o) { try { o.stop(n + 0.2); } catch (e) {} });
    } };
  }
  function noteOn(s) {
    if (!audio()) return;
    if (voices[s]) return;
    voices[s] = reed(freq(s), 0.22);
    var k = keyEls[s]; if (k) k.classList.add("down");
    onPlayed(s);
  }
  function noteOff(s) {
    if (voices[s]) { voices[s].stop(); delete voices[s]; }
    var k = keyEls[s]; if (k) k.classList.remove("down");
  }
  function allOff() { Object.keys(voices).forEach(function (s) { noteOff(+s); }); }
  function setDrone(on) {
    if (drone) { drone.forEach(function (v) { v.stop(); }); drone = null; }
    if (on && audio()) drone = [reed(freq(-12), 0.07), reed(freq(-5), 0.05)];
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
  root.innerHTML =
    '<div class="hm-bar">' +
    '<label>सा का सुर <select class="hm-sa" aria-label="सा किस पट्टी पर">' + opts + "</select></label>" +
    '<label class="hm-vol">आवाज़ <input type="range" min="0" max="1" step="0.05" value="' + vol + '" aria-label="आवाज़"></label>' +
    '<label class="hm-chk"><input type="checkbox" class="hm-drone"> सा-प ड्रोन</label>' +
    '<label class="hm-chk"><input type="checkbox" class="hm-showkeys"' + (showKeys ? " checked" : "") + "> कीबोर्ड अक्षर</label>" +
    "</div>" +
    '<div class="hm-kbd-wrap"><div class="hm-kbd" role="group" aria-label="हारमोनियम की पट्टियाँ"></div></div>' +
    '<p class="hm-hint">पट्टी पर उँगली या माउस रखें। कंप्यूटर पर <b>A S D F G H J K</b> = सा रे ग म प ध नि सां, ऊपर की लाइन (W E T Y U) = काली पट्टियाँ।</p>' +
    (songs.length ?
      '<div class="hm-song">' +
      '<div class="hm-bar"><label class="hm-pick">गाना <select class="hm-songsel" aria-label="गाना चुनें">' + songOpts + "</select></label>" +
      '<button type="button" class="hm-btn hm-play">▶ बजाएँ</button>' +
      '<button type="button" class="hm-btn hm-practice" title="जब तक सही पट्टी न दबाएँ, आगे नहीं बढ़ेगा">✋ अभ्यास मोड</button>' +
      '<label class="hm-tempo">रफ़्तार <input type="range" min="30" max="140" step="5" value="' + bpm + '" aria-label="रफ़्तार"><span class="hm-bpm"></span></label>' +
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
    saPc = +this.value; store.sa = saPc; save(); allOff(); drawKeys();
    var d = root.querySelector(".hm-drone"); if (d.checked) setDrone(true);
  });
  root.querySelector(".hm-vol input").addEventListener("input", function () {
    vol = +this.value; store.vol = vol; save(); if (master) master.gain.value = vol;
  });
  root.querySelector(".hm-drone").addEventListener("change", function () { setDrone(this.checked); });
  root.querySelector(".hm-showkeys").addEventListener("change", function () {
    showKeys = this.checked; store.keys = showKeys; save(); root.classList.toggle("nokeys", !showKeys);
  });

  // ---------- song player ----------
  if (!songs.length) return;
  var sel = root.querySelector(".hm-songsel"), linesEl = root.querySelector(".hm-lines"), status = root.querySelector(".hm-status");
  var playBtn = root.querySelector(".hm-play"), pracBtn = root.querySelector(".hm-practice");
  var tempo = root.querySelector(".hm-tempo input"), bpmEl = root.querySelector(".hm-bpm"), loopEl = root.querySelector(".hm-loop");
  var song = null, lines = [], cur = { l: 0, i: 0 }, timer = null, mode = null, chipEls = [];
  bpmEl.textContent = bpm;

  function loadSong(id) {
    stop();
    song = null; lines = []; linesEl.innerHTML = ""; chipEls = [];
    songs.forEach(function (sg) { if (sg.id === id) song = sg; });
    playBtn.disabled = pracBtn.disabled = !song;
    if (!song) { status.textContent = "ऊपर से कोई गाना चुनें, या पट्टियों पर खुला बजाएँ।"; return; }
    lines = song.lines.map(function (ln) { return { t: ln.t, notes: parse(ln.n) }; });
    linesEl.innerHTML = lines.map(function (ln, li) {
      return '<li data-l="' + li + '"><p class="hm-lyric">' + ln.t + '</p><p class="hm-notes">' +
        ln.notes.map(function (n, ni) { return '<span class="chip" data-i="' + ni + '">' + label(n.s) + (n.dur > 1 ? '<i class="hold">' + new Array(n.dur).join("–") + "</i>" : "") + "</span>"; }).join("") +
        "</p></li>";
    }).join("");
    chipEls = lines.map(function (ln, li) { return linesEl.querySelectorAll('li[data-l="' + li + '"] .chip'); });
    cur = { l: 0, i: 0 }; mark();
    status.textContent = "▶ बजाएँ से धुन सुनें, या ✋ अभ्यास मोड में ख़ुद बजाएँ। किसी पंक्ति पर टैप करके वहाँ से शुरू करें।";
  }
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
    var n = lines[cur.l].notes[cur.i], beat = 60000 / bpm;
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
  tempo.addEventListener("input", function () { bpm = +this.value; bpmEl.textContent = bpm; store.bpm = bpm; save(); });
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

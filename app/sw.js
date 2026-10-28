/* OmKiran Harmonium — offline cache. Version changes whenever the app, player, styles or sounds change. */
var CACHE = "okb-harmonium-80d52f0536";
var FILES = ["./", "manifest.webmanifest", "icon-192.png", "icon-512.png", "../harmonium.js?v=84265634", "../harmonium.css?v=eb4beea3", "../audio/harmonium/h36.mp3", "../audio/harmonium/h37.mp3", "../audio/harmonium/h38.mp3", "../audio/harmonium/h39.mp3", "../audio/harmonium/h40.mp3", "../audio/harmonium/h41.mp3", "../audio/harmonium/h42.mp3", "../audio/harmonium/h43.mp3", "../audio/harmonium/h44.mp3", "../audio/harmonium/h45.mp3", "../audio/harmonium/h46.mp3", "../audio/harmonium/h47.mp3", "../audio/harmonium/h48.mp3", "../audio/harmonium/h49.mp3", "../audio/harmonium/h50.mp3", "../audio/harmonium/h51.mp3", "../audio/harmonium/h52.mp3", "../audio/harmonium/h53.mp3", "../audio/harmonium/h54.mp3", "../audio/harmonium/h55.mp3", "../audio/harmonium/h56.mp3", "../audio/harmonium/h57.mp3", "../audio/harmonium/h58.mp3", "../audio/harmonium/h59.mp3", "../audio/harmonium/h60.mp3", "../audio/harmonium/h61.mp3", "../audio/harmonium/h62.mp3", "../audio/harmonium/h63.mp3", "../audio/harmonium/h64.mp3", "../audio/harmonium/h65.mp3", "../audio/harmonium/h67.mp3", "../audio/harmonium/h68.mp3", "../audio/harmonium/h69.mp3", "../audio/harmonium/h70.mp3", "../audio/harmonium/h71.mp3", "../audio/harmonium/h72.mp3", "../audio/harmonium/h73.mp3", "../audio/harmonium/h74.mp3"];
self.addEventListener("install", function (e) {
  e.waitUntil(caches.open(CACHE).then(function (c) { return c.addAll(FILES); }).then(function () { return self.skipWaiting(); }));
});
self.addEventListener("activate", function (e) {
  e.waitUntil(caches.keys().then(function (ks) { return Promise.all(ks.filter(function (k) { return k.indexOf("okb-harmonium-") === 0 && k !== CACHE; }).map(function (k) { return caches.delete(k); })); }).then(function () { return self.clients.claim(); }));
});
self.addEventListener("fetch", function (e) {
  var r = e.request; if (r.method !== "GET") return;
  if (r.mode === "navigate") { // the app page: fresh when online, cached when offline
    e.respondWith(fetch(r).then(function (res) { var cp = res.clone(); caches.open(CACHE).then(function (c) { c.put("./", cp); }); return res; }).catch(function () { return caches.match("./"); }));
    return;
  }
  e.respondWith(caches.match(r).then(function (hit) {
    return hit || fetch(r).then(function (res) {
      if (res.ok && (r.url.indexOf("fonts.g") > 0 || r.url.indexOf(self.location.origin) === 0)) { var cp = res.clone(); caches.open(CACHE).then(function (c) { c.put(r, cp); }); }
      return res;
    });
  }));
});

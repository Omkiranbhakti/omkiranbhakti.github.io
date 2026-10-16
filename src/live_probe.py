# Verification of temple live-darshan sources (round 2): which YouTube channels do temples' OFFICIAL websites point to,
# and are those channels' videos embeddable? Runs on GitHub Actions (YouTube reachable there). Writes live_probe.json.
import json, re, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36", "Accept-Language": "en-IN,en;q=0.9"}
def get(url, timeout=20):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e: return e.code, ""
    except Exception as e: return 0, str(e)[:80]
C = {
 "srisailam": {"sites": ["https://www.srisailadevasthanam.org/en-in/home"], "handles": ["srisailatv", "c/srisailatv"], "channels": []},
 "haridwar-ganga-aarti": {"sites": [], "handles": ["c/ShriGangaSabhaRegHaridwar"], "channels": []},
 "varanasi-ganga-aarti": {"sites": [], "handles": [], "channels": ["UCNDyYxUskLujzM6X3XVtXXw"]},
 "golden-temple": {"sites": [], "handles": ["c/SGPCAmritsar-official"], "channels": ["UCYn6UEtQ771a_OWSiNBoG8w"]},
 "dwarkadhish": {"sites": [], "handles": [], "channels": ["UCBAvMHZO3BIfMMhOK9LMOYQ"]},
 "nathdwara": {"sites": [], "handles": [], "channels": ["UCsXwdvZigny0t_d0TBIeHVA"]},
 "guruvayur": {"sites": [], "handles": [], "channels": ["UCgYLLt5Drs2Scd-J--JqDzQ"]},
 "mehandipur": {"sites": [], "handles": [], "channels": ["UCROq4qiZoivt1oZjGFR_EsQ", "UCs3IeKoxt-RFDI2qzp1oGFA"]},
 "mahakal-old": {"sites": [], "handles": [], "channels": []},
}
def site_links(url):
    s, b = get(url)
    return url, {"status": s,
        "channels": sorted(set(re.findall(r'youtube\.com/channel/(UC[\w-]{22})', b)) | set(re.findall(r'live_stream\?channel=(UC[\w-]{22})', b))),
        "handles": sorted(set(h for h in re.findall(r'youtube\.com/(@[\w.\-]+|user/[\w.\-]+|c/[\w.\-]+)', b))),
        "videos": sorted(set(re.findall(r'(?:youtube(?:-nocookie)?\.com/(?:embed/|watch\?v=|live/)|youtu\.be/)([\w-]{11})', b)))[:8]}
def handle_id(h):
    s, b = get("https://www.youtube.com/" + h)
    m = re.search(r'"(?:externalId|channelId)":"(UC[\w-]{22})"', b) or re.search(r'<link rel="canonical" href="https://www.youtube.com/channel/(UC[\w-]{22})"', b)
    return h, (m.group(1) if m else None, s)
def oembed(vid):
    s, b = get("https://www.youtube.com/oembed?format=json&url=" + urllib.parse.quote(f"https://www.youtube.com/watch?v={vid}"))
    if s == 200:
        j = json.loads(b); return {"ok": True, "author": j.get("author_name"), "title": j.get("title")}
    return {"ok": False, "status": s}
def chan(cid):
    s, b = get(f"https://www.youtube.com/channel/{cid}/streams")
    title = re.search(r'<meta property="og:title" content="([^"]+)"', b)
    subs = re.search(r'"subscriberCountText":\{[^}]*?"simpleText":"([^"]+)"', b) or re.search(r'([\d.,]+[KMB]?) subscribers', b)
    vids = list(dict.fromkeys(re.findall(r'"videoId":"([\w-]{11})"', b)))[:4]
    live = re.findall(r'"style":"LIVE"', b)
    s2, b2 = get(f"https://www.youtube.com/channel/{cid}/live")
    lv = re.search(r'<link rel="canonical" href="https://www.youtube.com/watch\?v=([\w-]{11})"', b2)
    return cid, {"status": s, "title": title.group(1) if title else None, "subs": subs.group(1) if subs else None,
                 "streams_found": len(vids), "live_badges": len(live), "live_now": '"isLiveNow":true' in b2, "live_video": lv.group(1) if lv else None,
                 "recent": [{"id": v, **oembed(v)} for v in vids[:4]]}
out = {}
with ThreadPoolExecutor(12) as ex:
    sites = dict(ex.map(site_links, [u for c in C.values() for u in c["sites"]]))
    hs = set(h for c in C.values() for h in c["handles"]) | set(h for r in sites.values() for h in r["handles"])
    hid = dict(ex.map(handle_id, hs))
    for k, c in C.items():
        cs = set(c["channels"])
        for u in c["sites"]: cs |= set(sites[u]["channels"]) | set(hid.get(h, (None,))[0] for h in sites[u]["handles"] if hid.get(h, (None,))[0])
        cs |= set(hid[h][0] for h in c["handles"] if hid.get(h, (None,))[0])
        c["_all"] = sorted(cs)
    info = dict(ex.map(chan, sorted(set(x for c in C.values() for x in c["_all"]))))
    for k, c in C.items():
        site_vids = sorted(set(v for u in c["sites"] for v in sites[u]["videos"]))
        out[k] = {"sites": {u: sites[u] for u in c["sites"]}, "handles": {h: hid.get(h) for h in c["handles"]},
                  "site_video_oembed": {v: oembed(v) for v in site_vids[:4]}, "channels": {x: info[x] for x in c["_all"]}}
        print(k, {u: sites[u]["status"] for u in c["sites"]}, [(x, info[x]["title"], info[x]["subs"]) for x in c["_all"]])
json.dump(out, open("live_probe.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

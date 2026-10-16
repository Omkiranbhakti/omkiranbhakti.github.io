# One-off verification: which YouTube channels do temples' OFFICIAL websites point to, and can their videos be embedded?
# Runs on GitHub Actions (YouTube is reachable there). Writes live_probe.json.
import json, re, urllib.request, urllib.parse, sys
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36", "Accept-Language": "en-IN,en;q=0.9"}
def get(url, timeout=25):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:
        return 0, str(e)[:120]
CANDS = {
 "kashi-vishwanath": {"handles": ["@ShreeKashiVishwanathMandir"], "pages": ["https://utsav.gov.in/view-darshan/kashi-vishwanath-live-darshan-1", "https://shrikashivishwanath.org/en/page/live-darshan", "https://shrikashivishwanath.org/sitemap.xml"]},
 "mahakal": {"channels": ["UCEUuwXHmHckwmdANSy4c7Sw"], "pages": ["https://utsav.gov.in/view-darshan/mahakaleshwar-live-darshan", "https://utsav.gov.in/view-darshan/shri-mahakaleshwar-live-darshan", "https://utsav.gov.in/live-darshan", "https://utsav.gov.in/darshan"]},
 "somnath-utsav": {"handles": [], "pages": ["https://utsav.gov.in/view-darshan/somnath-live-darshan"]},
 "shirdi": {"handles": ["@saibabasansthantrust"], "pages": []},
 "tirupati": {"handles": ["@SVBCTTD"], "pages": ["https://www.tirumala.org/SVBC.aspx", "https://www.svbcttd.com/"]},
}
def oembed(vid):
    s, b = get("https://www.youtube.com/oembed?format=json&url=" + urllib.parse.quote(f"https://www.youtube.com/watch?v={vid}"))
    if s == 200:
        j = json.loads(b); return {"ok": True, "author": j.get("author_name"), "author_url": j.get("author_url"), "title": j.get("title")}
    return {"ok": False, "status": s}
def channel_info(url):
    s, b = get(url)
    cid = re.search(r'"(?:externalId|channelId)":"(UC[\w-]{22})"', b)
    title = re.search(r'<meta property="og:title" content="([^"]+)"', b)
    return {"status": s, "channel_id": cid.group(1) if cid else None, "title": title.group(1) if title else None}
def feed(cid):
    s, b = get(f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}")
    items = re.findall(r"<entry>.*?<yt:videoId>([\w-]{11})</yt:videoId>.*?<title>(.*?)</title>.*?<published>(.*?)</published>", b, re.S)
    return {"status": s, "latest": [{"id": i, "title": t, "published": p} for i, t, p in items[:6]]}
def live_now(cid):
    s, b = get(f"https://www.youtube.com/channel/{cid}/live")
    vid = re.search(r'<link rel="canonical" href="https://www.youtube.com/watch\?v=([\w-]{11})"', b)
    return {"status": s, "is_live": '"isLiveNow":true' in b, "video": vid.group(1) if vid else None}
out = {}
for key, c in CANDS.items():
    r = {"pages": {}, "handles": {}, "channels": {}}
    found_vids, found_ch = set(), set(c.get("channels", []))
    for p in c["pages"]:
        s, b = get(p)
        vids = set(re.findall(r'(?:youtube(?:-nocookie)?\.com/(?:embed/|watch\?v=|live/)|youtu\.be/)([\w-]{11})', b))
        chs = set(re.findall(r'youtube\.com/channel/(UC[\w-]{22})', b)) | set(re.findall(r'live_stream\?channel=(UC[\w-]{22})', b))
        hs = set(re.findall(r'youtube\.com/(@[\w.-]+)', b))
        r["pages"][p] = {"status": s, "video_ids": sorted(vids)[:10], "channel_ids": sorted(chs), "handles": sorted(hs)[:10]}
        found_vids |= vids; found_ch |= chs
        for h in hs: c.setdefault("handles", []).append(h) if h not in c.get("handles", []) else None
    for h in c.get("handles", [])[:5]:
        info = channel_info(f"https://www.youtube.com/{h}")
        r["handles"][h] = info
        if info["channel_id"]: found_ch.add(info["channel_id"])
    r["page_videos"] = {v: oembed(v) for v in list(found_vids)[:6]}
    for cid in list(found_ch)[:5]:
        f = feed(cid)
        lv = live_now(cid)
        s_, b_ = get(f"https://www.youtube.com/channel/{cid}/streams")
        vid_ = re.findall(r'"videoId":"([\w-]{11})"', b_)
        f["latest"] = f["latest"] or [{"id": v, "title": "", "published": ""} for v in list(dict.fromkeys(vid_))[:3]]
        emb = oembed(f["latest"][0]["id"]) if f["latest"] else None
        r["channels"][cid] = {"feed": f, "live": lv, "latest_embed": emb, "live_embed": oembed(lv["video"]) if lv.get("video") else None}
    out[key] = r
    print(key, "pages:", {p: v["status"] for p, v in r["pages"].items()}, "channels:", list(r["channels"]))
json.dump(out, open("live_probe.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# Which temple YouTube channels are live right now? Writes live-now.json: {"t": unix time, "live": {channelId: videoId}}.
# Run by .github/workflows/live-now.yml every 15 minutes; the result goes to branch "live-status" (not main, so no site rebuild).
import json, re, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36",
      "Accept-Language": "en-IN,en;q=0.9", "Cookie": "CONSENT=YES+1; SOCS=CAI"}

def channels():
    src = open("src/live_section.py", encoding="utf-8").read()
    block = src.split("LIVE = [", 1)[1].split("\n]", 1)[0]
    return list(dict.fromkeys(re.findall(r'"(UC[\w-]{22})"', block)))

def player(v):
    """Ask YouTube's own player API whether a video is live now. Returns True/False, or None on failure."""
    body = json.dumps({"videoId": v, "context": {"client": {"clientName": "WEB", "clientVersion": "2.20251120.01.00", "hl": "en", "gl": "IN"}}}).encode()
    req = urllib.request.Request("https://www.youtube.com/youtubei/v1/player?prettyPrint=false", data=body,
                                 headers={**UA, "Content-Type": "application/json", "Origin": "https://www.youtube.com"})
    try:
        j = json.loads(urllib.request.urlopen(req, timeout=25).read())
    except Exception as e:
        return None
    vd = j.get("videoDetails") or {}
    lb = ((j.get("microformat") or {}).get("playerMicroformatRenderer") or {}).get("liveBroadcastDetails") or {}
    if "isLiveNow" in lb: return bool(lb["isLiveNow"])
    if vd: return bool(vd.get("isLive"))
    return None

def check(cid):
    try:
        req = urllib.request.Request(f"https://www.youtube.com/channel/{cid}/live", headers=UA)
        with urllib.request.urlopen(req, timeout=25) as r:
            b = r.read().decode("utf-8", "replace")
    except Exception:
        return cid, None
    # Live: /live opens the stream (page has "isLive":true and the video id). Not live: /live falls back to the channel page,
    # whose canonical link is the channel URL.
    can = re.search(r'<link rel="canonical" href="([^"]+)"', b)
    if '"isLive":true' in b and not (can and "/channel/" in can.group(1)):
        v = re.search(r'"videoId":"([\w-]{11})"', b)
        if v: return cid, v.group(1)
    return cid, ""

if __name__ == "__main__":
    ch = channels()
    # health check: a channel that streams 24x7 (Lofi Girl). If it doesn't show as live, detection is broken -> don't publish.
    if "--debug" in sys.argv:
        for v in ["_tV5LEBDs7w", "wYJYJ61EeQE", "Qzv2g6bkpSc"]:
            print(v, player(v))
        sys.exit(0)
    probe = check("UCSJ4gkVC6NrvII8umztf0Ow")[1]
    print("probe:", repr(probe))
    if not probe:
        sys.exit("detection check failed (24x7 test channel not seen as live); not publishing")
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(check, ch))
    ok = sum(1 for _, v in res if v is not None)
    live = {c: v for c, v in res if v}
    out = {"t": int(time.time()), "checked": ok, "total": len(ch), "live": live}
    json.dump(out, open("live-now.json", "w"), indent=0)
    print(f"{len(live)} live of {ok}/{len(ch)} checked:", live)
    if ok < len(ch) // 2:
        sys.exit("too many fetch failures; not publishing")

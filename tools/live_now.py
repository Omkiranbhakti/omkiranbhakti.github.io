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

def check(cid):
    try:
        req = urllib.request.Request(f"https://www.youtube.com/channel/{cid}/live", headers=UA)
        with urllib.request.urlopen(req, timeout=25) as r:
            b = r.read().decode("utf-8", "replace")
    except Exception:
        return cid, None
    can = re.search(r'<link rel="canonical" href="https://www\.youtube\.com/watch\?v=([\w-]{11})"', b)
    if can and '"isLiveNow":true' in b:
        return cid, can.group(1)
    return cid, ""

if __name__ == "__main__":
    ch = channels()
    # health check: a channel that streams 24x7 (Lofi Girl). If it doesn't show as live, detection is broken -> don't publish.
    if "--debug" in sys.argv:
        for u in ["https://www.youtube.com/channel/UCSJ4gkVC6NrvII8umztf0Ow/live", "https://www.youtube.com/@LofiGirl/live",
                  "https://www.youtube.com/embed/live_stream?channel=UCSJ4gkVC6NrvII8umztf0Ow"]:
            try:
                with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=25) as r:
                    b = r.read().decode("utf-8", "replace"); fu = r.geturl()
            except Exception as e:
                print(u, "ERR", e); continue
            print(u, "->", fu, len(b), "canon:", re.findall(r'<link rel="canonical" href="([^"]+)"', b)[:1],
                  "isLiveNow:", b.count('"isLiveNow":true'), "isLive:", b.count('"isLive":true'), "liveBroadcastDetails:", b.count("liveBroadcastDetails"),
                  "consent:", b.count("consent.youtube"), "videoIds:", re.findall(r'"videoId":"([\w-]{11})"', b)[:2])
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

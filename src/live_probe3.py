# Round 5: final check of chosen channels — title, subscribers, latest uploads (embeddable?), live tab, description.
import json, re, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36", "Accept-Language": "en-IN,en;q=0.9"}
def get(url, timeout=25):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r: return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e: return e.code, ""
    except Exception as e: return 0, str(e)[:80]
CH = ["UCvhUwke3pu_HQHDSP9_IGQg","UCAv-PEL7-tc5_WX5Qj423UQ","UCeYbwWPOnxpJ4oIYKpDO7iQ","UCCunHgsT7Hhogo40FHbhfDg","UCgYLLt5Drs2Scd-J--JqDzQ","UCBAvMHZO3BIfMMhOK9LMOYQ",
      "UCsXwdvZigny0t_d0TBIeHVA","UC82-0zBQho_hyV10fFAAeQA","UCzz1F1BYfBg_D23SpOnsRMw","UCgktEvceTyKnDN3w4F8n9Xg","UCSCMDOZrz_4-1dtnXsp8M7Q","UCse62u7mSlythNVB-X91vsA",
      "UCh82LJ6iwg68CLTHmy4BX1w","UC2m4o6e6TtbEQDj360pqBUw","UC1S9R_iJ4w00yYpivF7nt1Q","UC5iFIulyp-G2hZWHUUSJVSw","UC1vJ4RlWSHP6n0xL2G1tkYQ","UCPXnayBvF7ynbG_I3VOTgIg",
      "UCt8rtuZMlfSCMcb2ZxMgubA","UCqNGTFK0_nHU2Ldj3ZKScYw","UCzZ-P-kj1ByMNkzL4QCQlnw","UCxEk8cJijhNrRNDTkpeX_Zw","UCuk6VIkHtJZAkYZmCB8KVVQ","UCotHxqZyV7edB_gF7TmSnZw",
      "UCvyzcmTRl2y-1k9oeMvt41g","UC4G75x5HdLU77x_GG-byhCg","UCYXVKgcETYbcykzERUaU6ZA","UC0CWlMWRpuLIrp39nelismg","UCET-LB-LgAuDS-Cy8nfH4-w","UCKulZy7GUcfLE8ZaYi5V_kg"]
def oembed(v):
    s, b = get("https://www.youtube.com/oembed?format=json&url=" + urllib.parse.quote(f"https://www.youtube.com/watch?v={v}"))
    return {"id": v, "ok": s == 200, "author": json.loads(b).get("author_name") if s == 200 else None, "title": json.loads(b).get("title")[:80] if s == 200 else None}
def chan(cid):
    s, b = get(f"https://www.youtube.com/channel/{cid}/videos")
    title = re.search(r'<meta property="og:title" content="([^"]+)"', b)
    desc = re.search(r'<meta property="og:description" content="([^"]*)"', b)
    vids = list(dict.fromkeys(re.findall(r'"videoId":"([\w-]{11})"', b)))[:3]
    ages = re.findall(r'"publishedTimeText":\{"simpleText":"([^"]+)"', b)[:3]
    s2, b2 = get(f"https://www.youtube.com/channel/{cid}/streams")
    sv = list(dict.fromkeys(re.findall(r'"videoId":"([\w-]{11})"', b2)))[:2]
    sages = re.findall(r'"publishedTimeText":\{"simpleText":"([^"]+)"', b2)[:2]
    links = sorted(set(re.findall(r'"url":"(https?://(?!www\.youtube|youtube|i\.ytimg|yt3)[^"]{4,80})"', b)))[:6]
    return cid, {"status": s, "title": title.group(1) if title else None, "desc": desc.group(1)[:300] if desc else None, "links": links,
                 "uploads_age": ages, "streams_age": sages, "recent": [oembed(v) for v in vids], "recent_streams": [oembed(v) for v in sv]}
with ThreadPoolExecutor(10) as ex: out = dict(ex.map(chan, CH))
for c, i in out.items(): print(c, i["title"], i["uploads_age"], i["streams_age"], [r["ok"] for r in i["recent"]])
json.dump(out, open("live_probe.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

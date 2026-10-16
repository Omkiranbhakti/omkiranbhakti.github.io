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
 "khatu-shyam": {"sites": ["https://shrishyammandir.com", "https://www.khatushyamji.org", "https://khatushyam.in", "https://www.shrishyammandirkhatu.com"], "handles": ["@ShriShyamMandirKhatuShyamJi", "@khatushyamjisikar", "@ShriShyamDarshan"], "channels": ["UCQHKI4hRBBk6BraL8VGV5fw"]},
 "dwarkadhish": {"sites": ["https://www.dwarkadhish.org", "https://dwarkadhish.org/live-darshan.php", "https://www.dwarkadhishtemple.org"], "handles": ["@shridwarkadhishmandirofficial", "@shreedwarkadhishjagadmandi8285"], "channels": ["UCBAvMHZO3BIfMMhOK9LMOYQ"]},
 "nathdwara": {"sites": ["https://www.nathdwaratemple.org", "https://nathdwaratemple.org/live-darshan"], "handles": ["user/nathdwaratemple", "@SHRIJIDARSHAN_Nathdwara"], "channels": []},
 "dagdusheth": {"sites": ["https://www.dagdushethganpati.com", "https://www.dagdushethganpati.com/live-darshan", "https://www.dagdushethganpati.com/contact"], "handles": ["@DagdushethGanpati", "@dagdushethhalwaiganpati"], "channels": []},
 "mayapur": {"sites": ["https://www.mayapur.com", "https://mayapur.tv"], "handles": ["@mayapurtvofficial", "@MayapurTV"], "channels": ["UCypj9Vvizo4cCERfDFIG3zw"]},
 "iskcon-vrindavan": {"sites": ["https://www.iskconvrindavan.com", "https://iskconvrindavan.com/live"], "handles": ["@ISKCONVrindavan", "@iskconvrindavanofficial"], "channels": []},
 "prem-mandir": {"sites": ["https://www.jkp.org.in", "https://www.jkp.org.in/live"], "handles": ["@JKPOfficial", "@jkpliterature"], "channels": []},
 "salasar": {"sites": ["https://www.salasarbalaji.org", "https://salasarbalajidham.org", "https://www.salasarbalajimandir.com"], "handles": ["@SalasarBalajiDham", "@salasarbalajimandir"], "channels": []},
 "mehandipur": {"sites": ["https://www.mehandipurbalaji.org", "https://mehandipurbalajitrust.org"], "handles": ["@MehandipurBalajiDham"], "channels": []},
 "mahalaxmi-kolhapur": {"sites": ["https://www.mahalaxmikolhapur.com", "https://mahalaxmikolhapur.com/live-darshan"], "handles": ["@ShriMahalaxmiKolhapur"], "channels": []},
 "ambaji": {"sites": ["https://www.ambajitemple.in", "https://ambajitemple.in/live-darshan"], "handles": ["@ambajitemple", "@ShreeArasuriAmbajiMataDevasthanTrust"], "channels": []},
 "kamakhya": {"sites": ["https://www.maakamakhya.org", "https://kamakhyatemple.org"], "handles": ["@KamakhyaTemple"], "channels": []},
 "pashupatinath": {"sites": ["https://pashupatinathtemple.org", "https://www.pashupatiareadevelopmenttrust.org.np"], "handles": ["@PashupatiAreaDevelopmentTrust", "@pashupatinathlive"], "channels": []},
 "srisailam": {"sites": ["https://www.srisailadevasthanam.org", "https://srisailadevasthanam.org/live-darshan"], "handles": ["@SrisailaTVOfficial", "@srisailadevasthanam"], "channels": []},
 "baidyanath": {"sites": ["https://babadham.org", "https://www.babadham.org/live"], "handles": ["@BabaBaidyanathDham"], "channels": []},
 "grishneshwar": {"sites": ["https://www.grishneshwar.org", "https://grishneshwartemple.org"], "handles": [], "channels": []},
 "bhimashankar": {"sites": ["https://www.bhimashankar.org", "https://bhimashankardevasthan.org"], "handles": [], "channels": []},
 "nageshwar": {"sites": ["https://www.nageshwarjyotirlinga.org"], "handles": [], "channels": []},
 "rameshwaram": {"sites": ["https://rameswaramramanathar.hrce.tn.gov.in"], "handles": [], "channels": []},
 "tuljabhavani": {"sites": ["https://www.shrituljabhavani.org", "https://shrituljabhavani.org/live-darshan"], "handles": ["@ShriTuljabhavaniTemple"], "channels": []},
 "shani-shingnapur": {"sites": ["https://www.shanidev.com", "https://shanishingnapur.org", "https://www.shanishinganapur.com"], "handles": ["@ShaniShingnapur"], "channels": []},
 "guruvayur": {"sites": ["https://guruvayurdevaswom.in", "https://www.guruvayurdevaswom.nic.in"], "handles": ["@GuruvayurDevaswomOfficial"], "channels": []},
 "haridwar-ganga-aarti": {"sites": ["https://www.gangasabha.org", "https://shrigangasabha.org", "https://www.shrigangasabhaharidwar.org"], "handles": ["@ShriGangaSabha", "@shrigangasabhaharidwar"], "channels": []},
 "varanasi-ganga-aarti": {"sites": ["https://www.gangasevanidhi.org", "https://gangaaarti.org"], "handles": ["@GangaSevaNidhi", "@gangasevanidhivaranasi"], "channels": []},
 "pavagadh": {"sites": ["https://pavagadhtemple.in", "https://www.pavagadhtemple.org"], "handles": ["@MahakaliMandirPavagadh"], "channels": []},
 "chintpurni": {"sites": ["https://www.chintpurnitemple.org", "https://maachintpurni.org"], "handles": ["@ChintpurniTemple"], "channels": []},
 "naina-devi": {"sites": ["https://www.srinainadevi.com", "https://nainadevi.org"], "handles": [], "channels": []},
 "sanwariya-seth": {"sites": ["https://www.sanwariyaseth.org", "https://sanwaliyaseth.org"], "handles": ["@ShriSanwaliyaSethMandir"], "channels": []},
 "kal-bhairav-ujjain": {"sites": [], "handles": ["@KaalBhairavUjjain"], "channels": []},
 "radha-raman": {"sites": ["https://www.radharamanmandir.com", "https://radharaman.org"], "handles": ["@RadhaRamanMandir"], "channels": []},
 "jagannath-puri": {"sites": ["https://www.shreejagannatha.in", "https://shreejagannatha.in/live"], "handles": ["@ShreeJagannathaTemple"], "channels": []},
 "hanumangarhi": {"sites": ["https://www.hanumangarhi.org"], "handles": [], "channels": []},
 "kainchi-dham": {"sites": [], "handles": ["@KainchiDhamOfficial"], "channels": []},
 "golden-temple": {"sites": ["https://sgpc.net"], "handles": ["@SGPCSriAmritsar"], "channels": []},
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
                 "recent": [{"id": v, **oembed(v)} for v in vids[:2]]}
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

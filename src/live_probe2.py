# Round 4: find official live-darshan YouTube channels for more temples.
# For each temple: links on its official website(s) + top channels from a YouTube search; then channel facts.
# Runs on GitHub Actions (YouTube reachable there). Writes live_probe.json.
import json, re, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36", "Accept-Language": "en-IN,en;q=0.9"}
def get(url, timeout=25):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e: return e.code, ""
    except Exception as e: return 0, str(e)[:80]
T = {
 "sabarimala": (["https://sabarimalaonline.org/", "https://travancoredevaswomboard.org/"], "Sabarimala live darshan"),
 "guruvayur": (["https://guruvayurdevaswom.in/"], "Guruvayur temple live darshan"),
 "dwarkadhish": (["https://www.dwarkadhish.org/"], "Dwarkadhish mandir live darshan"),
 "nathdwara": (["https://www.nathdwaratemple.org/"], "Shrinathji Nathdwara live darshan"),
 "mehandipur": (["https://www.mehandipurbalaji.org/"], "Mehandipur Balaji live darshan"),
 "salasar": (["https://www.salasarbalajitemple.com/", "https://salasarbalaji.org/"], "Salasar Balaji live darshan"),
 "kolhapur-mahalaxmi": (["https://www.mahalaxmikolhapur.com/"], "Kolhapur Mahalaxmi Ambabai live darshan"),
 "pandharpur": (["https://vitthalrukminimandir.org/english/home.html", "https://vitthalrukminimandir.org/"], "Pandharpur Vitthal live darshan"),
 "kamakhya": (["https://maakamakhya.org/", "https://kamakhyatemple.org/"], "Kamakhya temple live darshan"),
 "deoghar": (["https://babadham.org/", "https://www.babadham.org/"], "Baba Baidyanath Dham Deoghar live darshan"),
 "shani-shingnapur": (["https://www.shanishinganapur.com/", "https://shanidev.com/"], "Shani Shingnapur live darshan"),
 "tuljabhavani": (["https://shrituljabhavani.org/"], "Tuljabhavani live darshan"),
 "jagannath-puri": (["https://www.shreejagannatha.in/"], "Jagannath Puri live darshan"),
 "meenakshi": (["https://maduraimeenakshi.hrce.tn.gov.in/", "http://www.maduraimeenakshi.org/"], "Madurai Meenakshi temple live"),
 "kanaka-durga": (["https://kanakadurgamma.org/"], "Kanaka Durga temple Vijayawada live darshan"),
 "mumbadevi": (["https://www.mumbadevi.org.in/"], "Mumbadevi temple live darshan"),
 "shegaon": (["https://www.gajananmaharaj.org/"], "Shegaon Gajanan Maharaj live darshan"),
 "chintpurni": (["https://www.chintpurnitemple.in/", "https://mataschintpurni.com/"], "Chintpurni mata live darshan"),
 "jwalaji": ([], "Jwala Ji mandir live darshan"),
 "sanwaliya-seth": (["https://shrisanwaliyaseth.com/"], "Sanwaliya Seth live darshan"),
 "govind-dev-ji": (["https://govinddevji.net/", "https://www.govinddevji.net/"], "Govind Dev Ji Jaipur live darshan"),
 "prem-mandir": (["https://www.jkp.org.in/"], "Prem Mandir Vrindavan live darshan"),
 "dakshineswar": (["https://www.dakshineswarkalitemple.org/"], "Dakshineswar Kali temple live"),
 "kalighat": ([], "Kalighat temple live darshan"),
 "yadadri": (["https://yadadritemple.telangana.gov.in/"], "Yadadri Lakshmi Narasimha live"),
 "annavaram": (["https://annavaramdevasthanam.nic.in/"], "Annavaram temple live"),
 "simhachalam": (["https://simhachalamdevasthanam.net/"], "Simhachalam temple live"),
 "padmanabhaswamy": (["https://www.sreepadmanabhaswamytemple.org/"], "Padmanabhaswamy temple live"),
 "mansa-devi": (["https://mansadevi.org.in/"], "Mansa Devi Panchkula live darshan"),
 "kal-bhairav-ujjain": ([], "Kal Bhairav Ujjain live darshan"),
 "khajrana": ([], "Khajrana Ganesh Indore live darshan"),
 "sankat-mochan": ([], "Sankat Mochan Varanasi live darshan"),
 "hanumangarhi": ([], "Hanumangarhi Ayodhya live darshan"),
 "bageshwar-dham": ([], "Bageshwar Dham live"),
 "kainchi-dham": ([], "Kainchi Dham live darshan"),
 "mahakal-bhasma": ([], "Mahakaleshwar bhasm aarti live"),
 "chamunda": ([], "Chamunda Devi temple live darshan"),
 "jeen-mata": ([], "Jeen Mata live darshan"),
 "karni-mata": ([], "Karni Mata Deshnoke live darshan"),
 "grishneshwar": ([], "Grishneshwar jyotirlinga live darshan"),
 "bhimashankar": ([], "Bhimashankar jyotirlinga live darshan"),
 "rameswaram": ([], "Rameswaram temple live darshan"),
 "nageshwar": ([], "Nageshwar jyotirlinga live darshan"),
 "ranakpur-ambaji": ([], "Khodiyar mata live darshan"),
 "brahma-pushkar": ([], "Pushkar Brahma temple live"),
 "radha-raman": ([], "Radha Raman mandir Vrindavan live darshan"),
 "radha-rani-barsana": ([], "Barsana Radha Rani mandir live darshan"),
 "iskcon-juhu": ([], "ISKCON Juhu live darshan"),
 "iskcon-bangalore": ([], "ISKCON Bangalore live darshan"),
 "iskcon-delhi": ([], "ISKCON Delhi live darshan"),
}
def site_links(url):
    s, b = get(url)
    return url, {"status": s,
        "channels": sorted(set(re.findall(r'youtube\.com/channel/(UC[\w-]{22})', b)) | set(re.findall(r'live_stream\?channel=(UC[\w-]{22})', b))),
        "handles": sorted(set(re.findall(r'youtube\.com/(@[\w.\-]+|user/[\w.\-]+|c/[\w.\-]+)', b))),
        "videos": sorted(set(re.findall(r'(?:youtube(?:-nocookie)?\.com/(?:embed/|watch\?v=|live/)|youtu\.be/)([\w-]{11})', b)))[:6]}
def handle_id(h):
    s, b = get("https://www.youtube.com/" + h)
    m = re.search(r'"(?:externalId|channelId)":"(UC[\w-]{22})"', b) or re.search(r'<link rel="canonical" href="https://www.youtube.com/channel/(UC[\w-]{22})"', b)
    return h, (m.group(1) if m else None)
def vid_owner(v):
    s, b = get("https://www.youtube.com/oembed?format=json&url=" + urllib.parse.quote(f"https://www.youtube.com/watch?v={v}"))
    if s != 200: return v, None
    j = json.loads(b); u = j.get("author_url", "")
    if "/channel/" in u: return v, u.split("/channel/")[1]
    return v, handle_id(u.split("youtube.com/")[1])[1] if "youtube.com/" in u else None
def search(q):
    s, b = get("https://www.youtube.com/results?search_query=" + urllib.parse.quote(q) + "&sp=EgIQAg%253D%253D")  # channels filter
    chans = list(dict.fromkeys(re.findall(r'"channelId":"(UC[\w-]{22})"', b)))[:6]
    s2, b2 = get("https://www.youtube.com/results?search_query=" + urllib.parse.quote(q))
    owners = list(dict.fromkeys(re.findall(r'"longBylineText":\{"runs":\[\{"text":"[^"]*","navigationEndpoint":\{[^}]*?"browseEndpoint":\{"browseId":"(UC[\w-]{22})"', b2)))[:8]
    return q, {"channel_results": chans, "video_owners": owners}
def chan(cid):
    s, b = get(f"https://www.youtube.com/channel/{cid}/streams")
    title = re.search(r'<meta property="og:title" content="([^"]+)"', b)
    subs = re.search(r'"subscriberCountText":\{[^}]*?"simpleText":"([^"]+)"', b) or re.search(r'"metadataParts":\[\{"text":\{"content":"([^"]*subscribers)"', b)
    vids = list(dict.fromkeys(re.findall(r'"videoId":"([\w-]{11})"', b)))[:5]
    vt = re.findall(r'"title":\{"runs":\[\{"text":"([^"]{5,90})"', b)[:4]
    verified = "BADGE_STYLE_TYPE_VERIFIED" in b[:400000]
    desc = re.search(r'<meta property="og:description" content="([^"]*)"', b)
    s2, b2 = get(f"https://www.youtube.com/channel/{cid}/live")
    return cid, {"title": title.group(1) if title else None, "subs": subs.group(1) if subs else None, "verified": verified,
                 "desc": (desc.group(1)[:220] if desc else None), "streams": len(vids), "stream_titles": vt,
                 "live_now": '"isLiveNow":true' in b2}
out = {}
with ThreadPoolExecutor(10) as ex:
    sites = dict(ex.map(site_links, [u for v in T.values() for u in v[0]]))
    hs = set(h for r in sites.values() for h in r["handles"])
    hid = dict(ex.map(handle_id, hs))
    svids = set(v for r in sites.values() for v in r["videos"])
    vown = dict(ex.map(vid_owner, svids))
    srch = dict(ex.map(search, [v[1] for v in T.values()]))
    allc = set()
    for k, (us, q) in T.items():
        sc = set()
        for u in us:
            sc |= set(sites[u]["channels"]) | {hid[h] for h in sites[u]["handles"] if hid.get(h)} | {vown[v] for v in sites[u]["videos"] if vown.get(v)}
        cands = list(sc) + srch[q]["channel_results"][:4] + srch[q]["video_owners"][:4]
        out[k] = {"sites": {u: sites[u] for u in us}, "site_channels": sorted(sc), "candidates": list(dict.fromkeys(cands))}
        allc |= set(out[k]["candidates"])
    info = dict(ex.map(chan, sorted(allc)))
for k in out:
    out[k]["info"] = {c: info[c] for c in out[k]["candidates"]}
    print(k, "| site:", out[k]["site_channels"], "|", [(c, info[c]["title"], info[c]["subs"], info[c]["verified"], info[c]["streams"]) for c in out[k]["candidates"]])
json.dump(out, open("live_probe.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

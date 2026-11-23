# Index control for a young domain: keep Google's attention on the strongest pages.
# - Small-city choghadiya pages (Hindi and English) are near-duplicates of each other
#   (same table, different times). They stay live and linked, but get "noindex,follow" and stay out of the sitemap.
#   To bring a city back into Google, add its slug to KEEP_CITIES.
# - Sitemap <lastmod> comes from a content hash kept in seo/lastmod.json: the date only moves when a page really changes.
import hashlib, json, os, re

KEEP_CITIES = {  # biggest search demand — these choghadiya pages stay indexed
    "delhi", "noida", "gurugram", "ghaziabad", "faridabad", "mumbai", "pune", "jaipur", "lucknow", "kolkata",
    "patna", "ahmedabad", "bengaluru", "hyderabad", "indore", "varanasi", "chandigarh", "bhopal", "kanpur", "chennai",
}
INDEX_META = '<meta name="robots" content="index,follow,max-image-preview:large">'
NOINDEX_META = '<meta name="robots" content="noindex,follow">'

# AdSense review (4 Nov 2026) flagged "replicated content, low-value content".
# Pages with embedded temple live streams, and thin pages (few words of their own), stay indexed
# but carry no AdSense code, so ads only run on full pages. Decided from Hindi pages, applied to both languages.
THIN_WORDS = 300
KEEP_ADS = {"index.html", "about.html", "contact.html", "privacy-policy.html", "disclaimer.html",
            "jaap-mala.html", "puja-samagri.html", "gayatri-mantra.html", "mahamrityunjay-mantra.html"}  # tools + top mantras
NO_ADS = set()   # filled by mark_no_ads() from the Hindi pages before apply()
_ADS = re.compile(r'<script async src="https://pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js[^"]*"[^>]*></script>')


def _own_words(html):
    m = re.search(r"(?s)<main[^>]*>(.*)</main>", html)
    t = m.group(1) if m else html
    t = re.sub(r"(?s)<(script|style|nav|aside)[^>]*>.*?</\1>", " ", t)
    return len(re.sub(r"<[^>]+>", " ", t).split())


def mark_no_ads(pages):
    NO_ADS.clear()
    for s, h in pages.items():
        if s in KEEP_ADS or not s.endswith(".html"): continue
        if s == "live-darshan.html" or s.endswith("-live-darshan.html") or _own_words(h) < THIN_WORDS: NO_ADS.add(s)
    return len(NO_ADS)


def is_noindex(slug, english=False):
    m = re.fullmatch(r"choghadiya-([a-z-]+)\.html", slug)
    if not m: return False
    return m.group(1) not in KEEP_CITIES   # same rule in both languages, so hreflang pairs stay consistent


_ROBOTS = re.compile(r'<meta (?:name="robots" content="[^"]*"|content="[^"]*" name="robots")\s*/?>')


def apply(pages, english=False):
    if not english:   # Hindi pages are applied first; decide no-ads pages from them
        print(f"ADS: {mark_no_ads(pages)} live-stream/thin pages without AdSense code")
    for s in NO_ADS & set(pages):
        pages[s] = _ADS.sub("", pages[s])
    n = 0
    for s in list(pages):
        if is_noindex(s, english):
            new, k = _ROBOTS.subn(NOINDEX_META, pages[s], count=1)
            if k: pages[s] = new; n += 1
    return n


def _fingerprint(html):
    return hashlib.sha1(html.encode("utf-8")).hexdigest()[:16]


def lastmod_dates(root, files, today):
    """files: {url_path: html}. Returns {url_path: 'YYYY-MM-DD'} and updates seo/lastmod.json."""
    p = os.path.join(root, "seo", "lastmod.json")
    try: old = json.load(open(p, encoding="utf-8"))
    except Exception: old = {}
    new, out = {}, {}
    for k, h in files.items():
        fp = _fingerprint(h)
        prev = old.get(k)
        date = prev[1] if prev and prev[0] == fp else today
        new[k] = [fp, date]; out[k] = date
    with open(p, "w", encoding="utf-8") as f: json.dump(new, f, ensure_ascii=False, indent=0, sort_keys=True)
    return out

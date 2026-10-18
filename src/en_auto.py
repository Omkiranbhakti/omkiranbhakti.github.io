# English edition for every page: converts a finished Hindi page into English.
#  - Lyrics lines (translate="no" + data-ro) are shown in Roman letters only.
#  - Every other Hindi text block is looked up in the translation table (src/en_tr/*.json),
#    written by hand for OmKiran Bhakti. Inline tags become <1>..</1> placeholders and
#    numbers become {0},{1}.. so one translation serves every date, time and count.
#  - A page is published in English only when every one of its blocks has a translation.
import json, os, re, glob, copy, hashlib
from bs4 import BeautifulSoup, NavigableString, Comment, Tag

DEV = re.compile(r"[ऀ-ॿ]")
NUM = re.compile(r"(?<![<\/\d{])\d+(?:[:.,]\d+)*(?![\d/>}])")
TIME_RE = re.compile(r"(सुबह|दोपहर|शाम|रात) (\d{1,2}):(\d{2})")
DEV_DIGITS = str.maketrans("०१२३४५६७८९", "0123456789")
BLOCK = {"p","li","h1","h2","h3","h4","h5","h6","td","th","dt","dd","summary","figcaption","caption",
         "blockquote","button","label","option","legend","title","div","span","a","b","strong","small","em","i","nav","header","section"}
LEAFY = {"p","li","h1","h2","h3","h4","h5","h6","td","th","dt","dd","summary","figcaption","caption","blockquote","button","label","option","legend","title"}
ATTRS = ("alt", "title", "aria-label", "placeholder", "data-label")
TR_DIR = os.path.join(os.path.dirname(__file__), "en_tr")

def load_table():
    t = {}
    for f in sorted(glob.glob(os.path.join(TR_DIR, "*.json"))):
        with open(f, encoding="utf-8") as fh: t.update(json.load(fh))
    return t

def hid(key): return hashlib.sha1(key.encode("utf-8")).hexdigest()[:10]

def norm_space(s): return re.sub(r"\s+", " ", s).strip()

from en_entities import ENT
_ENT_ALL = sorted(((h, c) for c, d in ENT.items() for h in d), key=lambda x: -len(x[0]))
_ALT = "|".join(re.escape(h) for h, _ in _ENT_ALL)
ENT_RE = re.compile(r"(?<![\u0900-\u0963\u0970-\u097F])(" + _ALT + r")(?![\u0900-\u0963\u0970-\u097F])")
_ALT_OLD = "|".join(re.escape(h) for h, c in _ENT_ALL if c != "F")
ENT_RE_OLD = re.compile(r"(?<![\u0900-\u097F])(" + _ALT_OLD + r")(?![\u0900-\u097F])")   # first table batches were keyed with this
_ENT_CLS = {h: c for h, c in _ENT_ALL}
ENMON_RE = re.compile(r"(?<![A-Za-z])(January|February|March|April|May|June|July|August|September|October|November|December)(?![A-Za-z])")
def _qnames():
    names = set(ENT.get("F", {}).values())
    try:
        import fest_info as _I
        for v in _I.INFO.values():
            for p in (v.get("en") or "").split(" / "):
                if p.strip(): names.add(p.strip())
    except Exception: pass
    names |= {"Diwali Lakshmi Puja"}
    return sorted((n for n in names if re.fullmatch(r"[A-Za-z][A-Za-z \-]+", n)), key=len, reverse=True)
_Q = _qnames()
Q_RE = re.compile(r"^(" + "|".join(re.escape(x) for x in _Q) + r")(?= \{)") if _Q else re.compile(r"$^")
CHOG = {"अमृत":"Amrit","शुभ":"Shubh","लाभ":"Labh","चर":"Char","रोग":"Rog","काल":"Kaal","उद्वेग":"Udveg"}
CHOG_RE = re.compile(r"(?<![\u0900-\u097F])(?:(" + "|".join(k for k in CHOG if k != "काल") + r")(?= \(\{| \{\d)|(काल)(?= \(\{))")
_LAT = sorted(set(ENT["C"].values()), key=len, reverse=True)
LAT_RE = re.compile(r"(?:(?<=\()|(?<=>))(" + "|".join(re.escape(x) for x in _LAT) + r")(?=\)|<)")

def num_key(s, old=False):
    """Replace numbers with {0},{1}.. and known names with {D0},{C0}..; return key and values."""
    s = s.translate(DEV_DIGITS)
    _has_dev = bool(DEV.search(s))
    nums, ents = [], []
    def rep(m):
        nums.append(m.group(0)); return "{%d}" % (len(nums) - 1)
    def rep_t(m):
        part, h, mm = m.group(1), int(m.group(2)), m.group(3)
        ap = "am" if part == "सुबह" or (part == "रात" and h in (12, 1, 2, 3)) else "pm"
        nums.append(f"{h}:{mm} {ap}"); return "{%d}" % (len(nums) - 1)
    s = TIME_RE.sub(rep_t, s)
    s = NUM.sub(rep, s)
    cnt = {}
    def rep_e(m):
        c = _ENT_CLS[m.group(1)]; i = cnt.get(c, 0); cnt[c] = i + 1
        ents.append((c, i, ENT[c][m.group(1)])); return "{%s%d}" % (c, i)
    s = (ENT_RE_OLD if old else ENT_RE).sub(rep_e, s)
    def rep_g(m):
        i = cnt.get("G", 0); cnt["G"] = i + 1
        ents.append(("G", i, CHOG[m.group(1) or m.group(2)])); return "{G%d}" % i
    s = CHOG_RE.sub(rep_g, s)
    def rep_en(m):
        i = cnt.get("E", 0); cnt["E"] = i + 1
        ents.append(("E", i, m.group(1))); return "{E%d}" % i
    if _has_dev: s = ENMON_RE.sub(rep_en, s)
    def rep_q(m):
        ents.append(("Q", 0, m.group(1))); return "{Q0}"
    if _has_dev: s = Q_RE.sub(rep_q, s, count=1)
    def rep_l(m):
        i = cnt.get("L", 0); cnt["L"] = i + 1
        ents.append(("L", i, m.group(1))); return "{L%d}" % i
    s = LAT_RE.sub(rep_l, s)
    return s, (nums, {(c, i): v for c, i, v in ents})

def fill(tpl, vals):
    nums, ents = vals
    tpl = re.sub(r"\{([A-Z])(\d+)\}", lambda m: ents.get((m.group(1), int(m.group(2))), m.group(0)), tpl)
    return re.sub(r"\{(\d+)\}", lambda m: nums[int(m.group(1))] if int(m.group(1)) < len(nums) else m.group(0), tpl)

def has_dev(node):
    if isinstance(node, NavigableString): return bool(DEV.search(str(node)))
    return any(has_dev(c) for c in node.children if not isinstance(c, Comment)) if not _skip(node) else False

def _skip(tag):
    return isinstance(tag, Tag) and (tag.name in ("script", "style") or tag.get("translate") == "no")

def _serialize(tag, tags):
    """Inner HTML of a unit with inline child tags as numbered placeholders."""
    out = []
    for c in tag.children:
        if isinstance(c, Comment): continue
        if isinstance(c, NavigableString):
            out.append(str(c).replace("<", "&lt;")); continue
        if c.name == "br": out.append("<br>"); continue
        tags.append(c); n = len(tags)
        if _skip(c) or not c.contents:
            out.append(f"<{n}/>")
        else:
            out.append(f"<{n}>" + _serialize(c, tags) + f"</{n}>")
    return "".join(out)

class Missing(Exception): pass

# Derived forms: translate the inner text once, the wrappers follow automatically.
DERIVE = [(re.compile(r"^(.+) — वीडियो$"), "{} — video"),
          (re.compile(r"^यहीं चलाएँ: (.+)$"), "Play here: {}"),
          (re.compile(r"^<1>(.+)</1>$"), "<1>{}</1>"),
          (re.compile(r"^<1><2>(.+)</2></1>$"), "<1><2>{}</2></1>")]

class Converter:
    def __init__(self, table, roman, en_slugs, site):
        self.t, self.roman, self.en, self.site = table, roman, en_slugs, site
        self.missing = {}   # key -> set(slugs)
        self.ro_seen = {}   # Roman-only headings that could get an English override

    def look(self, key, depth=0):
        v = self.t.get(hid(key))
        if v is not None: return v
        if depth == 0:
            v = self.look_parts(key)
            if v is not None: return v
        if depth > 2: return None
        for rx, fmt in DERIVE:
            m = rx.match(key)
            if m and "<" not in m.group(1).replace("<br>", ""):
                inner = self.look(m.group(1), depth + 1)
                if inner is not None: return fmt.format(inner)
        return None

    @staticmethod
    def parts(key):
        """Sentences of a tag-free text, each renumbered from {0}; with maps back to the original numbers."""
        if "<" in key: return None
        ps = [p for p in re.split(r"(?<=[।?!])\s+", key) if p]
        if len(ps) < 2: return None
        out = []
        for p in ps:
            cnt, fwd = {}, {}
            def rn(m):
                c = m.group(1)
                if m.group(0) not in fwd:
                    i = cnt.get(c, 0); cnt[c] = i + 1; fwd[m.group(0)] = "{%s%d}" % (c, i)
                return fwd[m.group(0)]
            np_ = re.sub(r"\{([A-Z]?)\d+\}", rn, p)
            back = {v: k for k, v in fwd.items()}
            out.append((np_, back))
        return out

    def look_parts(self, key):
        ps = self.parts(key)
        if not ps: return None
        res = []
        for np_, back in ps:
            v = self.look(np_, 9)
            if v is None: return None
            res.append(re.sub(r"\{[A-Z]?\d+\}", lambda m: back.get(m.group(0), m.group(0)), v))
        return " ".join(res)

    def record(self, key, slug):
        ps = self.parts(key)
        if ps:
            for np_, _ in ps:
                if self.look(np_, 9) is None: self.missing.setdefault(self.base(np_), set()).add(slug)
        else:
            self.missing.setdefault(self.base(key), set()).add(slug)

    def base(self, key):
        for _ in range(3):
            for rx, fmt in DERIVE:
                m = rx.match(key)
                if m and "<" not in m.group(1).replace("<br>", ""):
                    key = m.group(1); break
            else:
                break
        return key

    def tr(self, text, slug, ctx=None):
        key, nums = num_key(norm_space(text))
        if not DEV.search(key): return text
        self.n_tot += 1
        v = self.look(key)
        if v is None:
            k2, n2 = num_key(norm_space(text), old=True)
            if k2 != key:
                v = self.look(k2)
                if v is not None: nums = n2
        if v is None:
            self.record(key, slug); self.n_miss += 1; return None
        return fill(v, nums)

    def unit(self, tag, slug):
        tags = []
        inner = _serialize(tag, tags)
        key, nums = num_key(norm_space(inner))
        self.n_tot += 1
        v = self.look(key)
        if v is None:
            k2, n2 = num_key(norm_space(inner), old=True)
            if k2 != key:
                v = self.look(k2)
                if v is not None: nums = n2
        if v is None:
            self.record(key, slug); self.n_miss += 1; return False
        html = fill(v, nums)
        def rebuild(m):
            close, n, selfc = m.group(1), int(m.group(2)), m.group(3)
            t = tags[n - 1]
            if selfc: return str(t)
            if close: return f"</{t.name}>"
            attrs = "".join(f' {k}="{(" ".join(a) if isinstance(a, list) else a)}"' for k, a in t.attrs.items())
            return f"<{t.name}{attrs}>"
        html = re.sub(r"<(/?)(\d+)(/?)>", rebuild, html)
        new = BeautifulSoup(f"<x>{html}</x>", "html.parser").x
        tag.clear()
        for c in list(new.contents): tag.append(c)
        return True

    def convert(self, slug, hindi_html, page_url):
        soup = BeautifulSoup(hindi_html, "html.parser")
        self.n_tot = self.n_miss = 0
        ok = True
        # 1. lyrics / holy names in Roman
        for t in soup.find_all(attrs={"translate": "no"}):
            ro = t.get("data-ro")
            cls = t.get("class") or []
            if ro and "line" not in cls and t.name not in ("p", "div"):
                # heading-style holy names: an English override wins over the Roman spelling
                key, vals = num_key(norm_space(t.get_text()))
                v = self.t.get(hid(key))
                if v is not None:
                    t.clear(); t.append(BeautifulSoup(fill(v, vals), "html.parser")); del t["data-ro"]; t["lang"] = "en"; continue
                self.ro_seen.setdefault(key, set()).add(slug)
            if ro:
                t.clear()
                parts = ro.split("\n")
                for i, p in enumerate(parts):
                    if i: t.append(soup.new_tag("br"))
                    t.append(p)
                del t["data-ro"]
                if t.name != "html": t["lang"] = "hi-Latn"
            elif DEV.search(t.get_text()):
                for s in list(t.find_all(string=DEV)):
                    s.replace_with(self.roman(str(s)))
        # 2. text units
        body_roots = [soup.head.title] if soup.head and soup.head.title else []
        body_roots += [soup.body] if soup.body else []
        for root in body_roots:
            for tag in list(root.find_all(True)) + [root]:
                if tag.name in ("script", "style"): continue
                top = tag
                for p in tag.parents: top = p
                if top is not soup: continue   # replaced by an earlier unit
                if any(_skip(p) for p in [tag] + list(tag.parents)): continue
                direct = any(isinstance(c, NavigableString) and not isinstance(c, Comment) and DEV.search(str(c)) for c in tag.children)
                if not direct: continue
                # translate at the nearest leafy ancestor (or self) so a sentence stays whole
                u = tag
                while u.name not in LEAFY and u.parent is not None and u.parent.name not in ("body", "[document]", "main", "section", "div", "ul", "ol", "nav", "header", "footer", "article", "aside", "details", "head"):
                    u = u.parent
                if getattr(u, "_done", False): continue
                u._done = True
                if not self.unit(u, slug): ok = False
        # 3. attributes
        for t in soup.find_all(True):
            for a in ATTRS:
                if t.has_attr(a) and DEV.search(t[a]):
                    v = self.tr(t[a], slug)
                    if v is None: ok = False
                    else: t[a] = v
        for m in soup.find_all("meta"):
            if m.get("content") and DEV.search(m["content"]):
                v = self.tr(m["content"], slug)
                if v is None: ok = False
                else: m["content"] = v
        # 4. JSON-LD
        for s in soup.find_all("script", type="application/ld+json"):
            try: data = json.loads(s.string)
            except Exception: continue
            def walk(o, k=None):
                nonlocal ok
                if isinstance(o, dict): return {kk: walk(vv, kk) for kk, vv in o.items()}
                if isinstance(o, list): return [walk(x, k) for x in o]
                if isinstance(o, str) and DEV.search(o):
                    if k == "text": return self.roman(o)
                    v = self.tr(o, slug)
                    if v is None: ok = False; return o
                    return v
                return o
            data = walk(data)
            s.string = json.dumps(data, ensure_ascii=False)
        # a page goes out in English when (almost) every block is translated; a few
        # day-to-day texts that are not translated yet may stay in Hindi
        if self.n_miss and (self.n_miss > 3 or self.n_miss > 0.04 * max(self.n_tot, 1)): return None
        return soup

def finish(soup, slug, conv, en_slugs, site, hi_url, en_url):
    """Links, language tags and head for a converted page that lives in /en/."""
    html_t = soup.find("html")
    if html_t: html_t["lang"] = "en"
    for t in soup.find_all(True):
        for a in ("href", "src", "srcset", "poster", "data-src"):
            v = t.get(a)
            if not v or not isinstance(v, str): continue
            if re.match(r"^(https?:|mailto:|tel:|data:|#|//|javascript:)", v): continue
            if a == "srcset":
                t[a] = ", ".join("../" + p.strip() for p in v.split(",")); continue
            path = v.split("#")[0].split("?")[0]
            if a == "href" and (path.endswith(".html") or path == "") and path in en_slugs | {""}:
                continue  # stays inside /en/
            t[a] = "../" + v
    head = soup.head
    if head:
        for l in head.find_all("link", rel=lambda r: r and ("canonical" in r or "alternate" in r)):
            l.decompose()
        for m in head.find_all("meta", property=re.compile("^og:(url|locale)$")): m.decompose()
        for tag in [f'<link rel="canonical" href="{en_url}">',
                    f'<link rel="alternate" hreflang="en" href="{en_url}">',
                    f'<link rel="alternate" hreflang="hi" href="{hi_url}">',
                    f'<link rel="alternate" hreflang="x-default" href="{hi_url}">',
                    f'<meta property="og:url" content="{en_url}">', '<meta property="og:locale" content="en_IN">']:
            head.append(BeautifulSoup(tag, "html.parser"))
    sw = soup.select_one(".lang-sw")
    if sw:
        sw.clear()
        sw.append(BeautifulSoup(f'<a href="../{"" if slug=="index.html" else slug}?lang=hi" lang="hi" hreflang="hi">हिंदी</a><a class="on" lang="en" aria-current="true" data-lang="en">EN</a>', "html.parser"))
        sw["aria-label"] = "Language / भाषा"
    b = soup.body
    if b: b["class"] = (b.get("class") or []) + ["en"]
    return str(soup)

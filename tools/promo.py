"""Show the site's free tools (harmonium, jaap mala, kaal chakra, janm rashi) on every page.

Runs after src/build.py (see .github/workflows/pages.yml). Adds one "भक्ति टूल्स" block
to each built page, with the tool that fits that page first. Safe to run twice.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARK = 'class="okb-tp'

HI = {
    "hm": ("/harmonium.html", "/app/icon-192.png", "", "ऑनलाइन हारमोनियम", "सरगम लिखी पट्टियाँ, आरती की धुनें — फ़ोन पर बजाएँ"),
    "mala": ("/jaap-mala.html", "", "📿", "जाप माला", "108 बार जाप की गिनती, बिना माला के"),
    "kc": ("/hindu-kaal-chakra.html", "", "🕉️", "हिंदू काल-चक्र", "युग, मन्वंतर और कल्प — सनातन समय की यात्रा"),
    "janm": ("/janm-tithi-rashi-calculator.html", "", "🌙", "जन्म तिथि और राशि", "नाम अक्षर, नक्षत्र और तिथि वाला जन्मदिन"),
}
EN = {
    "hm": ("/en/harmonium.html", "/app/icon-192.png", "", "Online Harmonium", "Play aartis with sargam keys on your phone"),
    "mala": ("/jaap-mala.html", "", "📿", "Jaap Mala", "Count 108 chants without a mala"),
    "kc": ("/en/hindu-kaal-chakra.html", "", "🕉️", "Hindu Kaal Chakra", "Yugas, manvantaras and kalpas explained"),
    "janm": ("/janm-tithi-rashi-calculator.html", "", "🌙", "Birth Tithi & Rashi", "Name letter, nakshatra and tithi birthday"),
}
SKIP = {"404.html", "privacy-policy.html", "disclaimer.html", "contact.html", "about.html", "stats.html",
        "harmonium.html", "jaap-mala.html", "hindu-kaal-chakra.html", "janm-tithi-rashi-calculator.html"}
MALA_W = ("chalisa", "mantra", "stotra", "ashtak", "stavan", "suktam", "shatakam", "naam", "kavach", "namah", "mahamantra", "kripal")
KC_W = ("kab-hai", "panchang", "tyohar", "choghadiya", "ekadashi", "purnima", "calendar", "kaal", "list", "maas", "katha", "niyam")


def notes_page(stem):
    for st in (stem, stem.replace("-aarti", ""), stem.replace("aarti-", "")):
        if os.path.exists(os.path.join(ROOT, st + "-harmonium-notes.html")):
            return st + "-harmonium-notes.html"
    return ""


def order(name):
    stem = name[:-5]
    if "harmonium" in name or "aarti" in name or "bhajan" in name or notes_page(stem):
        first = "hm"
    elif any(w in name for w in MALA_W):
        first = "mala"
    elif any(w in name for w in KC_W):
        first = "kc"
    else:
        first = "hm"
    rest = [k for k in ("hm", "mala", "kc", "janm") if k != first]
    return [first] + rest, stem


def block(name, en):
    keys, stem = order(name)
    T = EN if en else HI
    notes = notes_page(stem)
    cards = []
    for i, k in enumerate(keys):
        href, img, emo, title, sub = T[k]
        if k == "hm" and not en and notes and not name.endswith("-harmonium-notes.html"):
            href, sub = "/" + notes, "इसी की धुन हारमोनियम पर बजाकर सीखें"
        ic = (f'<img src="{img}" alt="" width="44" height="44" loading="lazy">' if img
              else f'<span aria-hidden="true">{emo}</span>')
        cards.append(f'<li{" class=okb-tp-1" if i == 0 else ""}><a href="{href}"><i>{ic}</i><b>{title}</b><small>{sub}</small></a></li>')
    head = "🛠️ Free devotional tools" if en else "🛠️ मुफ़्त भक्ति टूल्स"
    note = "No app needed, free" if en else "बिना ऐप, बिलकुल मुफ़्त"
    return (f'<section class="okb-tp no-print"><div class="wrap"><h2>{head} <small>{note}</small></h2>'
            f'<ul>{"".join(cards)}</ul></div></section>')


def insert(html, blk, home):
    if MARK in html:
        html = re.sub(r'<section class="okb-tp.*?</section>', "", html, flags=re.S)
    if home:
        m = re.search(r'<section class="qi-sec">.*?</section>', html, flags=re.S)
        if m:
            return html[:m.end()] + blk + html[m.end():]
    for a in ('<section class="no-print sewa">', "<footer"):
        i = html.find(a)
        if i != -1:
            return html[:i] + blk + html[i:]
    return html


POP_A, POP_B = "<!--okb-pop-->", "<!--/okb-pop-->"


def home_pop():
    """The rotating 'क्या आप जानते हैं?' card (facts + tool glimpses) from the built home page."""
    h = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    m = re.search(r'<aside class="kya-pop".*?</aside><script>.*?</script>', h, flags=re.S)
    return POP_A + m.group() + POP_B if m else ""


def add_pop(html, pop):
    html = re.sub(re.escape(POP_A) + ".*?" + re.escape(POP_B), "", html, flags=re.S)
    if not pop or 'class="kya-pop"' in html:
        return html
    for a in ("</main>", "</body>"):
        i = html.find(a)
        if i != -1:
            return html[:i] + pop + html[i:]
    return html


def main():
    n = 0
    pop = home_pop()
    for d, en in ((ROOT, False), (os.path.join(ROOT, "en"), True)):
        for name in sorted(os.listdir(d)):
            if not name.endswith(".html") or name in SKIP:
                continue
            p = os.path.join(d, name)
            s = open(p, encoding="utf-8").read()
            t = insert(s, block(name, en), name == "index.html")
            if not en and name != "index.html":
                t = add_pop(t, pop)
            if t != s:
                open(p, "w", encoding="utf-8").write(t); n += 1
    print("promo: tools block on", n, "pages")


if __name__ == "__main__":
    sys.exit(main())

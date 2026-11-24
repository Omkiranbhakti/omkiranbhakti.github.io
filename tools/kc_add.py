#!/usr/bin/env python3
"""Add a batch of Kaal-Chakra events from a compact text file.
Usage: python3 tools/kc_add.py tools/batches/b03.txt
One event per line, fields separated by ' | ':
 year | kind | title | place | short | yt_kw | key (English, gives slug) | wiki | katha (paras split by ' // ') | mahatva | tirth ('—' none) | source | en_title | en_place | en_short
Lines starting with # are ignored. Rows are merged into kaal-chakra/index.html sorted by year,
katha into kaal-chakra/katha.js, English into src/kc_en.json, and slugs into tools/kc_query.json (image search)."""
import sys, re, json
NOW = 2026.86
src = open(sys.argv[1], encoding='utf8').read().splitlines()
ev = []
for ln in src:
    ln = ln.strip()
    if not ln or ln.startswith('#'): continue
    f = [x.strip() for x in ln.split(' | ')]
    assert len(f) == 15, (len(f), ln[:80])
    for x in f[:8]:
        assert "'" not in x and '"' not in x, ln[:60]
    ev.append(f)
p = 'kaal-chakra/index.html'; h = open(p, encoding='utf8').read()
L = h.split('\n')
ROW = re.compile(r"^\[(-?[\d.]+|NOW),'(\w+)','([^']*)'")
rows = [i for i, l in enumerate(L) if ROW.match(l)]
titles = {ROW.match(L[i]).group(3) for i in rows}
yv = lambda l: NOW if ROW.match(l).group(1) == 'NOW' else float(ROW.match(l).group(1))
K = open('kaal-chakra/katha.js', encoding='utf8').read(); KD = json.loads(K[K.index('{'):K.rindex('}') + 1])
EN = json.load(open('src/kc_en.json', encoding='utf8'))
Q = {}  # only this batch's slugs, so the image run searches just the new events
slug = lambda r: re.sub(r'[^a-z0-9]+', '-', r.lower()).strip('-')
new = []
for f in ev:
    y, c, t, pl, d, kw, r, w, kt, mh, tr, so, et, ep, ed = f
    if t in titles: print('skip (exists):', t); continue
    assert c in 'c a sh r k m s v t u b n'.split(), c
    new.append((float(y), f"[{y},'{c}','{t}','{pl}','{d}','{kw}','{r}',\"{w}\"],"))
    KD[t] = [kt.replace(' // ', '\n\n'), mh, tr, so]
    EN[slug(r)] = [et, ep, ed]
    Q.setdefault(slug(r), [w or r, (w or r) + ' painting'])
    titles.add(t)
# merge sorted
block = [L[i] for i in rows] + [n[1] for n in new]
block.sort(key=lambda l: yv(l))
block = [b if b.endswith(',') else b + ',' for b in block]
block[-1] = block[-1].rstrip(',')
L = L[:rows[0]] + block + L[rows[-1] + 1:]
open(p, 'w', encoding='utf8').write('\n'.join(L))
open('kaal-chakra/katha.js', 'w', encoding='utf8').write('window.KATHA={\n' + ',\n'.join(json.dumps(k, ensure_ascii=False) + ':' + json.dumps(v, ensure_ascii=False, separators=(',', ':')) for k, v in KD.items()) + '\n};\n')
open('src/kc_en.json', 'w', encoding='utf8').write('{\n' + ',\n'.join(json.dumps(k, ensure_ascii=False) + ': ' + json.dumps(v, ensure_ascii=False) for k, v in EN.items()) + '\n}\n')
json.dump(Q, open('tools/kc_query.json', 'w', encoding='utf8'), ensure_ascii=False, indent=0)
print('added', len(new), 'total', len(block))

# Panchak, Bhadra (Vishti karana), Gandmool and Kharmas periods from the panchang engine (times in IST).
import datetime as dt, ephem
from panchang import sid_moon, sid_sun, elong, from_ist, to_ist

def _scan(fn, start, end, step_h=1.0):
    """Yield (t0, t1) IST intervals where fn(ephem.Date) is True; edges refined to ~1 minute."""
    def f(t): return fn(from_ist(t))
    def edge(a, b, va):
        while (b - a) > dt.timedelta(seconds=40):
            m = a + (b - a) / 2
            if f(m) == va: a = m
            else: b = m
        return b
    out, t, prev, on = [], start, f(start), None
    if prev: on = start
    step = dt.timedelta(hours=step_h)
    while t < end:
        n = t + step; v = f(n)
        if v != prev:
            x = edge(t, n, prev)
            if v: on = x
            else:
                if on is not None: out.append((on, x))
                on = None
        t, prev = n, v
    if on is not None: out.append((on, None))
    return out

def panchak(start, end):
    return _scan(lambda d: sid_moon(d) >= 300.0, start, end)

GANDMOOL_NAK = {0: "अश्विनी", 8: "आश्लेषा", 9: "मघा", 17: "ज्येष्ठा", 18: "मूल", 26: "रेवती"}
def gandmool(start, end):
    res = []
    for i, n in GANDMOOL_NAK.items():
        lo, hi = i * 360 / 27, (i + 1) * 360 / 27
        for a, b in _scan(lambda d, lo=lo, hi=hi: lo <= sid_moon(d) < hi, start, end):
            res.append((a, b, n))
    return sorted(res, key=lambda x: x[0])

def karana_index(d):  # 0..59 half-tithi number
    return int(elong(d) // 6)
def is_vishti(d):
    n = karana_index(d)
    return 1 <= n <= 56 and (n - 1) % 7 == 6
def bhadra(start, end):
    return _scan(is_vishti, start, end, step_h=0.5)

def bhadra_vaas(d_ist):
    r = int(sid_moon(from_ist(d_ist)) // 30)
    if r in (3, 4, 10, 11): return "पृथ्वी लोक"
    if r in (0, 1, 2, 7): return "स्वर्ग लोक"
    return "पाताल लोक"

def kharmas(start, end):
    a = _scan(lambda d: 240 <= sid_sun(d) < 270, start, end, step_h=6)
    b = _scan(lambda d: 330 <= sid_sun(d) < 360, start, end, step_h=6)
    return sorted([(x, y, "धनु") for x, y in a] + [(x, y, "मीन") for x, y in b], key=lambda z: z[0])

PANCHAK_TYPE = {6: ("रोग पंचक", "रविवार से शुरू — सेहत के मामलों में सावधानी"), 0: ("राज पंचक", "सोमवार से शुरू — शुभ माना जाता है, सरकारी कामों में सफलता"),
                1: ("अग्नि पंचक", "मंगलवार से शुरू — आग, निर्माण और औज़ार के कामों से बचें"), 2: ("बुधवार वाला पंचक", "बुधवार से शुरू — इसे कम दोष वाला माना जाता है"),
                3: ("गुरुवार वाला पंचक", "गुरुवार से शुरू — इसे कम दोष वाला माना जाता है"), 4: ("चोर पंचक", "शुक्रवार से शुरू — यात्रा, लेन-देन और व्यापार से बचें"),
                5: ("मृत्यु पंचक", "शनिवार से शुरू — सबसे अशुभ माना जाता है, जोखिम के काम टालें")}

if __name__ == "__main__":
    s, e = dt.datetime(2026, 10, 1), dt.datetime(2027, 1, 31)
    for a, b in panchak(s, e): print("panchak", a.strftime("%d %b %H:%M %a"), "→", b.strftime("%d %b %H:%M") if b else "-")
    for a, b in bhadra(dt.datetime(2026, 10, 15), dt.datetime(2026, 11, 1)): print("bhadra", a.strftime("%d %b %H:%M"), "→", b.strftime("%d %b %H:%M"), bhadra_vaas(a))
    for a, b, n in kharmas(s, dt.datetime(2027, 6, 1)): print("kharmas", n, a, b)
    for a, b, n in gandmool(dt.datetime(2026, 10, 15), dt.datetime(2026, 11, 15)): print("gand", n, a.strftime("%d %b %H:%M"), b.strftime("%d %b %H:%M"))

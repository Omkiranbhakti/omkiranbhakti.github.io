"""Simple Hindu panchang for New Delhi, computed with PyEphem (no network needed).
Rules used (standard, as in common North-Indian panchangs):
- Day's tithi/nakshatra = the one running at local sunrise (udaya tithi).
- Sunrise/sunset = upper limb, standard refraction (-0:34).
- Month names: amanta month from the sun's sidereal sign at the new moon; North India
  (purnimanta) names the krishna paksha after the next month.
- Nakshatra uses Lahiri ayanamsa.
- Brahma muhurat = 96 to 48 min before sunrise; Abhijit = 8th of 15 daytime muhurtas;
  Rahu kaal = weekday-specific 1/8 of daytime.
"""
import ephem, math, datetime as dt

LAT, LON, ELEV = "28.6139", "77.2090", 216
IST = dt.timedelta(hours=5, minutes=30)

TITHI = ["प्रतिपदा","द्वितीया","तृतीया","चतुर्थी","पंचमी","षष्ठी","सप्तमी","अष्टमी","नवमी","दशमी",
         "एकादशी","द्वादशी","त्रयोदशी","चतुर्दशी","पूर्णिमा"]
NAK = ["अश्विनी","भरणी","कृत्तिका","रोहिणी","मृगशिरा","आर्द्रा","पुनर्वसु","पुष्य","आश्लेषा","मघा",
       "पूर्वा फाल्गुनी","उत्तरा फाल्गुनी","हस्त","चित्रा","स्वाति","विशाखा","अनुराधा","ज्येष्ठा","मूल",
       "पूर्वाषाढ़ा","उत्तराषाढ़ा","श्रवण","धनिष्ठा","शतभिषा","पूर्वा भाद्रपद","उत्तरा भाद्रपद","रेवती"]
# amanta month by sun's sidereal sign (0=Mesha) at the opening new moon
MONTH_BY_SIGN = ["वैशाख","ज्येष्ठ","आषाढ़","श्रावण","भाद्रपद","आश्विन","कार्तिक","मार्गशीर्ष","पौष","माघ","फाल्गुन","चैत्र"]
MONTH_ORDER = ["चैत्र","वैशाख","ज्येष्ठ","आषाढ़","श्रावण","भाद्रपद","आश्विन","कार्तिक","मार्गशीर्ष","पौष","माघ","फाल्गुन"]
VAAR = ["सोमवार","मंगलवार","बुधवार","गुरुवार","शुक्रवार","शनिवार","रविवार"]  # Python weekday()
RAHU_SLOT = {0:2,1:7,2:5,3:6,4:4,5:3,6:8}  # weekday() -> 1-based slot of 8

def obs(date=None):
    o = ephem.Observer(); o.lat, o.lon, o.elevation = LAT, LON, ELEV
    o.pressure = 0; o.horizon = "-0:34"
    if date is not None: o.date = date
    return o

def to_ist(d):  # ephem.Date -> naive IST datetime
    return ephem.Date(d).datetime() + IST

def from_ist(t):  # naive IST datetime -> ephem.Date
    return ephem.Date(t - IST)

def ecl_lon(body, d):
    body.compute(d, epoch=d)
    return math.degrees(ephem.Ecliptic(body, epoch=d).lon)

def ayanamsa(d):
    y = 2000 + (ephem.Date(d) - ephem.Date("2000/1/1 12:00")) / 365.25
    return 23.85307 + (y - 2000) * 0.0139694

def elong(d):
    return (ecl_lon(ephem.Moon(), d) - ecl_lon(ephem.Sun(), d)) % 360

def sid_moon(d): return (ecl_lon(ephem.Moon(), d) - ayanamsa(d)) % 360
def sid_sun(d):  return (ecl_lon(ephem.Sun(), d) - ayanamsa(d)) % 360

def tithi_index(d):  # 0..29
    return int(elong(d) // 12)

def nak_index(d):
    return int(sid_moon(d) // (360/27))

def _end(fn, idx, start):
    """Find when fn(d) stops equalling idx, searching forward from start (max 2 days)."""
    lo = ephem.Date(start); hi = ephem.Date(lo + 1/24)
    while fn(hi) == idx:
        lo, hi = hi, ephem.Date(hi + 1/24)
        if hi - start > 2.2: return None
    for _ in range(30):
        mid = ephem.Date((lo + hi) / 2)
        if fn(mid) == idx: lo = mid
        else: hi = mid
    return ephem.Date(hi)

def sunrise_sunset(day):  # day: date (IST calendar day)
    o = obs(from_ist(dt.datetime(day.year, day.month, day.day, 0, 0)))
    sr = o.next_rising(ephem.Sun(), use_center=False)
    o.date = sr
    ss = o.next_setting(ephem.Sun(), use_center=False)
    return sr, ss

def tithi_name(i):
    paksha = "शुक्ल" if i < 15 else "कृष्ण"
    n = i % 15
    name = TITHI[n] if not (i == 29) else "अमावस्या"
    if i == 14: name = "पूर्णिमा"
    return paksha, name

def lunar_month(d):
    """Return (amanta_month, purnimanta_month, is_adhik) for moment d."""
    nm = ephem.previous_new_moon(d)
    nxt = ephem.next_new_moon(d)
    s1 = int(sid_sun(nm) // 30); s2 = int(sid_sun(nxt) // 30)
    amanta = MONTH_BY_SIGN[s1]
    adhik = (s1 == s2)
    if adhik:  # adhik maas takes the name of the following month
        amanta = MONTH_BY_SIGN[(s1 + 1) % 12]
    i = tithi_index(d)
    if i >= 15:  # krishna paksha -> purnimanta month is the next one
        purni = MONTH_ORDER[(MONTH_ORDER.index(amanta) + 1) % 12]
    else:
        purni = amanta
    return amanta, purni, adhik

def vikram_samvat(day):
    # VS increments at Chaitra shukla pratipada (new moon with sun in sidereal Meena, Mar/Apr)
    d = from_ist(dt.datetime(day.year, 3, 1))
    for _ in range(3):
        nm = ephem.next_new_moon(d)
        if int(sid_sun(nm) // 30) == 11:
            start = to_ist(nm).date(); break
        d = ephem.Date(nm + 1)
    else:
        start = dt.date(day.year, 4, 1)
    return day.year + 57 if day >= start else day.year + 56

def fmt(t):  # datetime -> "06:21"
    return t.strftime("%H:%M").lstrip("0") if False else t.strftime("%H:%M")

def hhmm12(t):
    h = t.hour % 12 or 12
    part = "सुबह" if t.hour < 12 else ("दोपहर" if t.hour < 16 else ("शाम" if t.hour < 19 else "रात"))
    if t.hour < 4: part = "रात"
    return f"{part} {h}:{t.minute:02d}"

def day_panchang(day):
    sr, ss = sunrise_sunset(day)
    sr_i, ss_i = to_ist(sr), to_ist(ss)
    ti = tithi_index(sr)
    paksha, tname = tithi_name(ti)
    t_end = _end(tithi_index, ti, sr)
    ni = nak_index(sr); n_end = _end(nak_index, ni, sr)
    amanta, purni, adhik = lunar_month(sr)
    daylen = (ss_i - sr_i)
    mu = daylen / 15
    abhijit = (sr_i + 7*mu, sr_i + 8*mu)
    slot = RAHU_SLOT[day.weekday()]
    rahu = (sr_i + (slot-1)*daylen/8, sr_i + slot*daylen/8)
    brahma = (sr_i - dt.timedelta(minutes=96), sr_i - dt.timedelta(minutes=48))
    # next tithi (to tell what comes after)
    nxt = (ti + 1) % 30
    np_, nname = tithi_name(nxt)
    return {
        "date": day.isoformat(), "vaar": VAAR[day.weekday()],
        "sunrise": fmt(sr_i), "sunset": fmt(ss_i),
        "paksha": paksha, "tithi": tname, "tithi_i": ti,
        "tithi_end": to_ist(t_end).strftime("%Y-%m-%d %H:%M") if t_end else None,
        "next_tithi": nname, "next_paksha": np_,
        "nakshatra": NAK[ni], "nak_end": to_ist(n_end).strftime("%Y-%m-%d %H:%M") if n_end else None,
        "month_purnimanta": purni, "month_amanta": amanta, "adhik": adhik,
        "vs": vikram_samvat(day),
        "brahma": [fmt(brahma[0]), fmt(brahma[1])],
        "abhijit": [fmt(abhijit[0]), fmt(abhijit[1])], "abhijit_ok": day.weekday() != 2,
        "rahu": [fmt(rahu[0]), fmt(rahu[1])],
        "pradosh": [fmt(ss_i), fmt(ss_i + dt.timedelta(minutes=144))],
    }

def tithi_spans(start_day, end_day):
    """Every tithi between two dates with exact IST start/end (for festival checks)."""
    d = from_ist(dt.datetime(start_day.year, start_day.month, start_day.day))
    stop = from_ist(dt.datetime(end_day.year, end_day.month, end_day.day))
    out = []
    i = tithi_index(d); s = d
    while d < stop:
        e = _end(tithi_index, i, d)
        out.append((i, to_ist(s), to_ist(e))); s = d = ephem.Date(e + 1/86400); i = tithi_index(d)
    return out

if __name__ == "__main__":
    for day in [dt.date(2026,10,15), dt.date(2026,10,18), dt.date(2026,10,19), dt.date(2026,10,20)]:
        p = day_panchang(day)
        print(p["date"], p["vaar"], p["month_purnimanta"], p["paksha"], p["tithi"], "→ ends", p["tithi_end"],
              "|", p["nakshatra"], "| sun", p["sunrise"], p["sunset"], "| rahu", p["rahu"], "| VS", p["vs"])
    for i, s, e in tithi_spans(dt.date(2026,10,17), dt.date(2026,10,21)):
        print(tithi_name(i), s.strftime("%d %H:%M"), "→", e.strftime("%d %H:%M"))

def moonrise(day):
    """Moonrise (IST) on a calendar day in Delhi, or None."""
    o = obs(from_ist(dt.datetime(day.year, day.month, day.day, 0, 0)))
    try:
        r = to_ist(o.next_rising(ephem.Moon()))
    except Exception:
        return None
    return r if r.date() == day else None

EKADASHI_NAME = {("चैत्र","K"):"पापमोचिनी",("चैत्र","S"):"कामदा",("वैशाख","K"):"वरूथिनी",("वैशाख","S"):"मोहिनी",
 ("ज्येष्ठ","K"):"अपरा",("ज्येष्ठ","S"):"निर्जला",("आषाढ़","K"):"योगिनी",("आषाढ़","S"):"देवशयनी",
 ("श्रावण","K"):"कामिका",("श्रावण","S"):"श्रावण पुत्रदा",("भाद्रपद","K"):"अजा",("भाद्रपद","S"):"परिवर्तिनी",
 ("आश्विन","K"):"इंदिरा",("आश्विन","S"):"पापांकुशा",("कार्तिक","K"):"रमा",("कार्तिक","S"):"देवउठनी (प्रबोधिनी)",
 ("मार्गशीर्ष","K"):"उत्पन्ना",("मार्गशीर्ष","S"):"मोक्षदा",("पौष","K"):"सफला",("पौष","S"):"पौष पुत्रदा",
 ("माघ","K"):"षटतिला",("माघ","S"):"जया",("फाल्गुन","K"):"विजया",("फाल्गुन","S"):"आमलकी"}

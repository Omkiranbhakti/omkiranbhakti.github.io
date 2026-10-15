# City-level astronomy: moonrise, sunset, sidereal ascendant (lagna) for any lat/lon + IANA timezone.
import datetime as dt, math
from zoneinfo import ZoneInfo
import ephem
from panchang import ayanamsa, tithi_index

def _obs(lat, lon, utc_dt):
    o = ephem.Observer(); o.lat, o.lon = str(lat), str(lon); o.elevation = 0
    o.pressure = 0; o.horizon = "-0:34"; o.date = ephem.Date(utc_dt)
    return o

def _utc(local_naive, tz):
    return local_naive.replace(tzinfo=ZoneInfo(tz)).astimezone(dt.timezone.utc).replace(tzinfo=None)

def _local(ed, tz):
    return ephem.Date(ed).datetime().replace(tzinfo=dt.timezone.utc).astimezone(ZoneInfo(tz))

def moonrise(lat, lon, day, tz):
    """Local aware datetime of moonrise on local calendar `day`, or None."""
    o = _obs(lat, lon, _utc(dt.datetime(day.year, day.month, day.day), tz))
    try: r = _local(o.next_rising(ephem.Moon()), tz)
    except Exception: return None
    return r if r.date() == day else None

def sun_times(lat, lon, day, tz):
    o = _obs(lat, lon, _utc(dt.datetime(day.year, day.month, day.day), tz))
    sr = o.next_rising(ephem.Sun(), use_center=False); o.date = sr
    ss = o.next_setting(ephem.Sun(), use_center=False)
    return _local(sr, tz), _local(ss, tz)

def tithi_at(aware):
    return tithi_index(ephem.Date(aware.astimezone(dt.timezone.utc).replace(tzinfo=None)))

def lagna(lat, lon, aware):
    """Sidereal (Lahiri) ascendant sign index 0=Mesh..11=Meen at a moment."""
    ed = ephem.Date(aware.astimezone(dt.timezone.utc).replace(tzinfo=None))
    o = _obs(lat, lon, ephem.Date(ed).datetime())
    ramc = float(o.sidereal_time())                 # radians, local apparent sidereal time
    eps = math.radians(23.4393 - 0.0130 * ((ed - ephem.Date("2000/1/1 12:00")) / 36525))
    phi = math.radians(lat)
    asc = math.degrees(math.atan2(math.cos(ramc), -(math.sin(ramc) * math.cos(eps) + math.tan(phi) * math.sin(eps)))) % 360
    return int(((asc - ayanamsa(ed)) % 360) // 30)

def lagna_window(lat, lon, start, end, sign, step_min=1):
    """First continuous window within [start,end] where lagna == sign -> (s,e) or None."""
    t, s, e = start, None, None
    while t <= end:
        if lagna(lat, lon, t) == sign:
            if s is None: s = t
            e = t
        elif s is not None: break
        t += dt.timedelta(minutes=step_min)
    return (s, e) if s else None

def chandrodaya_day(lat, lon, tz, near_day, tithi_idx):
    """Local date (near near_day) on which `tithi_idx` prevails at moonrise."""
    for k in (-1, 0, 1):
        d = near_day + dt.timedelta(days=k)
        mr = moonrise(lat, lon, d, tz)
        if mr and tithi_at(mr) == tithi_idx: return d, mr
    return near_day, moonrise(lat, lon, near_day, tz)

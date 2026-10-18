"""Devanagari -> readable Roman Hindi (Hinglish style) for 'lyrics in English' sections."""
import re
from aksharamukha import transliterate as _t
_MAP = [("jñ", "gy"), ("ā", "a"), ("ī", "i"), ("ū", "u"), ("ṛ", "ri"), ("ṝ", "ri"), ("ē", "e"), ("ō", "o"),
        ("ñ", "n"), ("ṅ", "n"), ("ṇ", "n"), ("ṃ", "n"), ("m̐", "n"), ("̐", "n"), ("ś", "sh"), ("ṣ", "sh"),
        ("ṭ", "t"), ("ḍ", "d"), ("ḥ", "h"), ("ḷ", "l"), ("ḻ", "l"), ("ṟ", "r"), ("q", "k"), ("ġ", "g"), ("ḳ", "k"), ("ẖ", "kh"), ("ü", "u"), ("ï", "i"), ("_", ""), ("ë", "e")]
def roman_line(s):
    s = s.replace("ॐ", "Om").replace("॥", " ||").replace("।", " |")
    r = _t.process("Devanagari", "IAST", s, pre_options=["RemoveSchwaHindi"])
    for a, b in _MAP: r = r.replace(a, b)
    r = r.replace("ch", "\x01").replace("c", "ch").replace("\x01", "chh").replace("sv", "sw").replace("dv", "dw")
    r = re.sub(r"[̀-ͯ]", "", r)          # leftover combining marks
    r = re.sub(r"\bjay\b", "jai", r)
    r = re.sub(r"(\w)\|", r"\1 |", r).replace("||", "॥").replace("|", "।")
    r = re.sub(r"\s+", " ", r).strip()
    return r[:1].upper() + r[1:]
def roman(text):
    return "\n".join(roman_line(l) for l in text.split("\n") if l.strip())

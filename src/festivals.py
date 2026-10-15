"""Festival dates for New Delhi, derived from tithi rules with the panchang engine.
Each rule: (key, Hindi name, purnimanta month, paksha 'S'/'K', tithi 1-15 (15=purnima, 30=amavasya), kaal, offset_days)
kaal = the moment of day at which the tithi must prevail:
  sunrise (udaya), pradosh (sunset+48m), night (moonrise approx, 20:30 IST), aparahna (14:00), madhyahna (12:30), nishita (midnight)
offset_days lets a festival fall on the day after its tithi date (e.g. Holi after Holika Dahan).
"""
import datetime as dt
from panchang import tithi_index, from_ist, sunrise_sunset, to_ist, lunar_month, MONTH_ORDER

def tithi_at(day, kaal):
    sr, ss = sunrise_sunset(day)
    t = {"sunrise": to_ist(sr) + dt.timedelta(minutes=2), "pradosh": to_ist(ss) + dt.timedelta(minutes=48),
         "night": dt.datetime(day.year, day.month, day.day, 20, 30), "aparahna": dt.datetime(day.year, day.month, day.day, 14, 0),
         "madhyahna": dt.datetime(day.year, day.month, day.day, 11, 30),
         "nishita": dt.datetime(day.year, day.month, day.day, 23, 50)}[kaal]
    d = from_ist(t)
    return tithi_index(d), d

def target_index(paksha, n):
    if n == 30: return 29
    return (n - 1) if paksha == "S" else (n - 1 + 15)

RULES = [
 # key, name, month (purnimanta), paksha, tithi, kaal, offset, short meaning
 ("sharad-purnima","शरद पूर्णिमा","आश्विन","S",15,"night",0,"चाँदनी में खीर रखने और माँ लक्ष्मी की पूजा की रात"),
 ("karwa-chauth","करवा चौथ","कार्तिक","K",4,"night",0,"सुहागिन महिलाओं का निर्जला व्रत, चाँद को अर्घ्य देकर पारण"),
 ("ahoi-ashtami","अहोई अष्टमी","कार्तिक","K",8,"pradosh",0,"संतान की लंबी आयु के लिए माताओं का व्रत"),
 ("dhanteras","धनतेरस","कार्तिक","K",13,"pradosh",0,"धन्वंतरि और कुबेर पूजा, बर्तन और सोना खरीदने का दिन"),
 ("narak-chaturdashi","नरक चतुर्दशी (रूप चौदस, छोटी दिवाली)","कार्तिक","K",14,"sunrise",0,"यम दीपदान और अभ्यंग स्नान"),
 ("diwali","दिवाली (लक्ष्मी पूजा)","कार्तिक","K",30,"pradosh",0,"प्रदोष काल में माँ लक्ष्मी और गणेश जी की पूजा"),
 ("govardhan-puja","गोवर्धन पूजा","कार्तिक","S",1,"sunrise",0,"अन्नकूट, श्रीकृष्ण और गोवर्धन पर्वत की पूजा"),
 ("bhai-dooj","भाई दूज","कार्तिक","S",2,"aparahna",0,"बहनें भाई को तिलक लगाकर लंबी आयु की कामना करती हैं"),
 ("chhath-puja","छठ पूजा (संध्या अर्घ्य)","कार्तिक","S",6,"sunrise",0,"डूबते सूर्य को अर्घ्य, अगली सुबह उगते सूर्य को"),
 ("dev-uthani-ekadashi","देवउठनी एकादशी","कार्तिक","S",11,"sunrise",0,"भगवान विष्णु के जागने का दिन, तुलसी विवाह की शुरुआत"),
 ("kartik-purnima","कार्तिक पूर्णिमा (देव दीपावली)","कार्तिक","S",15,"sunrise",0,"गंगा स्नान, दीपदान और गुरु नानक जयंती"),
 ("vivah-panchami","विवाह पंचमी","मार्गशीर्ष","S",5,"sunrise",0,"श्रीराम-सीता विवाह का उत्सव"),
 ("gita-jayanti","गीता जयंती (मोक्षदा एकादशी)","मार्गशीर्ष","S",11,"sunrise",0,"श्रीकृष्ण के गीता उपदेश का दिन"),
 ("vasant-panchami","वसंत पंचमी","माघ","S",5,"sunrise",0,"माँ सरस्वती की पूजा"),
 ("maha-shivratri","महाशिवरात्रि","फाल्गुन","K",14,"nishita",0,"शिव-पार्वती विवाह की रात, निशीथ काल में शिव पूजा"),
 ("holika-dahan","होलिका दहन","फाल्गुन","S",15,"pradosh",0,"बुराई पर अच्छाई की जीत, होली की पहली रात"),
 ("holi","होली (रंगवाली)","फाल्गुन","S",15,"pradosh",1,"रंगों का त्योहार, होलिका दहन के अगले दिन"),
 ("chaitra-navratri","चैत्र नवरात्रि (घटस्थापना)","चैत्र","S",1,"sunrise",0,"हिंदू नववर्ष और चैत्र नवरात्रि का पहला दिन"),
 ("ram-navami","राम नवमी","चैत्र","S",9,"madhyahna",0,"मध्याह्न में श्रीराम का जन्मोत्सव"),
 ("hanuman-jayanti","हनुमान जयंती","चैत्र","S",15,"sunrise",0,"हनुमान जी का जन्मोत्सव (उत्तर भारत)"),
 ("akshaya-tritiya","अक्षय तृतीया","वैशाख","S",3,"sunrise",0,"सोना खरीदने और दान का अक्षय फल देने वाला दिन"),
 ("guru-purnima","गुरु पूर्णिमा","आषाढ़","S",15,"sunrise",0,"गुरु और वेदव्यास जी की पूजा"),
 ("raksha-bandhan","रक्षा बंधन","श्रावण","S",15,"aparahna",0,"बहनें भाई को राखी बाँधती हैं (भद्रा काल से बचें)"),
 ("janmashtami","कृष्ण जन्माष्टमी","भाद्रपद","K",8,"nishita",0,"आधी रात को श्रीकृष्ण का जन्मोत्सव"),
 ("ganesh-chaturthi","गणेश चतुर्थी","भाद्रपद","S",4,"madhyahna",0,"मध्याह्न में गणपति स्थापना"),
 ("anant-chaturdashi","अनंत चतुर्दशी (गणेश विसर्जन)","भाद्रपद","S",14,"sunrise",0,"गणपति विसर्जन का दिन"),
 ("sharadiya-navratri","शारदीय नवरात्रि (घटस्थापना)","आश्विन","S",1,"sunrise",0,"नवरात्रि का पहला दिन, कलश स्थापना"),
 ("dussehra","दशहरा (विजयादशमी)","आश्विन","S",10,"aparahna",0,"रावण दहन, बुराई पर अच्छाई की जीत"),
]

# Smaller festivals and vrats (shown on the calendar and their own pages, not in the home "upcoming" strip)
MINOR_RULES = [
 ("govatsa-dwadashi","गोवत्स द्वादशी (वसु बारस)","कार्तिक","K",12,"pradosh",0,"गाय-बछड़े की पूजा, दिवाली उत्सव की शुरुआत"),
 ("chhath-nahay-khay","छठ नहाय-खाय","कार्तिक","S",4,"sunrise",0,"छठ महापर्व का पहला दिन, शुद्ध सात्विक भोजन"),
 ("chhath-kharna","छठ खरना","कार्तिक","S",5,"sunrise",0,"छठ का दूसरा दिन, शाम को गुड़ की खीर का प्रसाद"),
 ("chhath-usha-arghya","छठ उषा अर्घ्य (पारण)","कार्तिक","S",7,"sunrise",0,"उगते सूर्य को अर्घ्य देकर छठ व्रत का पारण"),
 ("chitragupt-puja","चित्रगुप्त पूजा (कलम-दवात पूजा)","कार्तिक","S",2,"aparahna",0,"कायस्थ समाज में चित्रगुप्त जी और कलम-दवात की पूजा"),
 ("gopashtami","गोपाष्टमी","कार्तिक","S",8,"sunrise",0,"श्रीकृष्ण के गौ-चारण आरंभ का दिन, गौ पूजा"),
 ("akshay-navami","अक्षय नवमी (आंवला नवमी)","कार्तिक","S",9,"sunrise",0,"आंवले के पेड़ की पूजा और उसके नीचे भोजन"),
 ("tulsi-vivah","तुलसी विवाह","कार्तिक","S",12,"pradosh",0,"शालिग्राम (विष्णु) के साथ तुलसी माता का विवाह"),
 ("vaikunth-chaturdashi","बैकुंठ चतुर्दशी","कार्तिक","S",14,"nishita",0,"हरि-हर मिलन, विष्णु और शिव दोनों की पूजा"),
 ("kaal-bhairav-jayanti","काल भैरव जयंती","मार्गशीर्ष","K",8,"nishita",0,"भगवान शिव के काल भैरव रूप का प्राकट्य दिवस"),
 ("dattatreya-jayanti","दत्तात्रेय जयंती","मार्गशीर्ष","S",15,"pradosh",0,"भगवान दत्तात्रेय का जन्मोत्सव"),
 ("sakat-chauth","सकट चौथ (तिलकुटा चौथ)","माघ","K",4,"night",0,"संतान के लिए माताओं का व्रत, चंद्र अर्घ्य और तिलकुट"),
 ("mauni-amavasya","मौनी अमावस्या","माघ","K",30,"sunrise",0,"मौन रहकर गंगा स्नान और दान का दिन"),
 ("ratha-saptami","रथ सप्तमी (सूर्य जयंती)","माघ","S",7,"sunrise",0,"सूर्य देव का प्राकट्य दिवस, अर्घ्य और स्नान"),
 ("magh-purnima","माघ पूर्णिमा","माघ","S",15,"sunrise",0,"माघ स्नान का समापन, गंगा स्नान और दान"),
 ("rang-panchami","रंग पंचमी","चैत्र","K",5,"sunrise",0,"होली के पाँचवें दिन देवताओं के साथ रंग खेलने का पर्व"),
 ("sheetala-ashtami","शीतला अष्टमी (बसौड़ा)","चैत्र","K",8,"sunrise",0,"शीतला माता को बासी भोजन का भोग"),
 ("hindu-nav-varsh","हिंदू नववर्ष (गुड़ी पड़वा, उगादी)","चैत्र","S",1,"sunrise",0,"विक्रम संवत का नया साल"),
 ("gangaur","गणगौर","चैत्र","S",3,"sunrise",0,"शिव-पार्वती (ईसर-गौर) की पूजा, राजस्थान का प्रमुख पर्व"),
 ("parshuram-jayanti","परशुराम जयंती","वैशाख","S",3,"pradosh",0,"भगवान परशुराम का जन्मोत्सव"),
 ("sita-navami","सीता नवमी (जानकी जयंती)","वैशाख","S",9,"madhyahna",0,"माता सीता का प्राकट्य दिवस"),
 ("narasimha-jayanti","नृसिंह जयंती","वैशाख","S",14,"pradosh",0,"भगवान नृसिंह का प्राकट्य, प्रह्लाद की रक्षा"),
 ("buddha-purnima","बुद्ध पूर्णिमा (वैशाख पूर्णिमा)","वैशाख","S",15,"sunrise",0,"भगवान बुद्ध का जन्म, ज्ञान और निर्वाण दिवस"),
 ("vat-savitri","वट सावित्री व्रत","ज्येष्ठ","K",30,"sunrise",0,"सुहागिनों का व्रत, बरगद की पूजा और सावित्री-सत्यवान कथा"),
 ("shani-jayanti","शनि जयंती","ज्येष्ठ","K",30,"sunrise",0,"शनि देव का जन्मोत्सव"),
 ("ganga-dussehra","गंगा दशहरा","ज्येष्ठ","S",10,"sunrise",0,"माँ गंगा के धरती पर अवतरण का दिन"),
 ("jagannath-rath-yatra","जगन्नाथ रथ यात्रा","आषाढ़","S",2,"sunrise",0,"पुरी में भगवान जगन्नाथ, बलभद्र और सुभद्रा की रथ यात्रा"),
 ("sawan-start","सावन शुरू (श्रावण मास आरंभ)","श्रावण","K",1,"sunrise",0,"शिव जी का प्रिय महीना शुरू, सावन सोमवार व्रत"),
 ("hariyali-teej","हरियाली तीज","श्रावण","S",3,"sunrise",0,"सुहागिनों का शिव-पार्वती व्रत, झूले और मेहंदी"),
 ("nag-panchami","नाग पंचमी","श्रावण","S",5,"sunrise",0,"नाग देवता की पूजा"),
 ("kajari-teej","कजरी तीज","भाद्रपद","K",3,"sunrise",0,"सुहागिनों का व्रत, नीम की पूजा और चंद्र अर्घ्य"),
 ("hal-shashthi","हलषष्ठी (ललही छठ)","भाद्रपद","K",6,"sunrise",0,"बलराम जयंती, संतान के लिए माताओं का व्रत"),
 ("hartalika-teej","हरतालिका तीज","भाद्रपद","S",3,"sunrise",0,"निर्जला व्रत, शिव-पार्वती की बालू की प्रतिमा की पूजा"),
 ("rishi-panchami","ऋषि पंचमी","भाद्रपद","S",5,"madhyahna",0,"सप्तऋषियों की पूजा"),
 ("radha-ashtami","राधा अष्टमी","भाद्रपद","S",8,"madhyahna",0,"श्री राधा रानी का जन्मोत्सव"),
 ("pitru-paksha","पितृ पक्ष आरंभ (पूर्णिमा श्राद्ध)","भाद्रपद","S",15,"aparahna",0,"श्राद्ध पक्ष की शुरुआत"),
 ("sarva-pitru-amavasya","सर्वपितृ अमावस्या","आश्विन","K",30,"aparahna",0,"सभी पितरों के श्राद्ध का अंतिम दिन"),
]
MINOR_KEYS = {r[0] for r in MINOR_RULES}
RULES = RULES + MINOR_RULES

def month_of(day, kaal):
    i, d = tithi_at(day, kaal)
    am, pu, adhik = lunar_month(d)
    return i, pu, adhik

def find_dates(start, end):
    """Span-based: every occurrence of each rule's tithi in its month, then pick the observance day.
    Returns {key: [dict(date, name, meaning, tithi_start, tithi_end, note)]}."""
    from panchang import tithi_spans
    spans = tithi_spans(start - dt.timedelta(days=2), end + dt.timedelta(days=2))
    out = {}
    for key, name, month, paksha, n, kaal, off, meaning in RULES:
        tgt = target_index(paksha, n); res = []
        for i, s0, e0 in spans:
            if i != tgt: continue
            mid = s0 + (e0 - s0) / 2
            am, pu, adhik = lunar_month(from_ist(mid))
            if pu != month or adhik: continue
            # candidate days the tithi touches
            day, cand = s0.date(), []
            while day <= e0.date():
                ti, _ = tithi_at(day, kaal)
                if ti == tgt: cand.append(day)
                day += dt.timedelta(days=1)
            note = ""
            if cand:
                pick = cand[0]
            else:  # kshaya at the chosen moment: observe on the day the tithi begins (if it begins in daytime)
                pick = s0.date() if s0.hour < 18 else s0.date() + dt.timedelta(days=1)
            if key == "raksha-bandhan":
                # Bhadra = first half of purnima. If aparahna of pick lies in it and purnima exists at next sunrise, move on.
                half = s0 + (e0 - s0) / 2
                apar = dt.datetime(pick.year, pick.month, pick.day, 14, 0)
                nxt = pick + dt.timedelta(days=1)
                if s0 <= apar < half and tithi_at(nxt, "sunrise")[0] == tgt:
                    pick = nxt; note = f"भद्रा के कारण राखी {e0.strftime('%H:%M')} से पहले बाँधें"
            if key == "janmashtami":
                alt = pick + dt.timedelta(days=1)
                if tithi_at(alt, "sunrise")[0] == tgt:
                    note = f"वैष्णव परंपरा (मथुरा-वृंदावन, ISKCON): {alt.day} {MONTHS_HI[alt.month]}"
            d = pick + dt.timedelta(days=off)
            if start <= d <= end:
                res.append({"date": d, "name": name, "meaning": meaning, "tithi_start": s0, "tithi_end": e0, "note": note, "kaal": kaal})
        out[key] = res
    return out

MONTHS_HI = ["","जनवरी","फ़रवरी","मार्च","अप्रैल","मई","जून","जुलाई","अगस्त","सितंबर","अक्टूबर","नवंबर","दिसंबर"]

if __name__ == "__main__":
    res = find_dates(dt.date(2026,10,1), dt.date(2027,12,31))
    for k, v in res.items():
        print(k.ljust(22), " | ".join(f"{x['date'].isoformat()} {x['date'].strftime('%a')} {x['note']}" for x in v))

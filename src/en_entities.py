# Names that are swapped for typed placeholders before a translation lookup, so one
# translation covers every weekday, month, city, tithi, nakshatra and Hindu month.
# D weekday · M month · C city · T tithi · N nakshatra · H Hindu month
ENT = {
 "D": {"सोमवार":"Monday","मंगलवार":"Tuesday","बुधवार":"Wednesday","गुरुवार":"Thursday","बृहस्पतिवार":"Thursday","शुक्रवार":"Friday","शनिवार":"Saturday","रविवार":"Sunday"},
 "M": {"जनवरी":"January","फ़रवरी":"February","फरवरी":"February","मार्च":"March","अप्रैल":"April","मई":"May","जून":"June","जुलाई":"July","अगस्त":"August","सितंबर":"September","अक्टूबर":"October","नवंबर":"November","दिसंबर":"December",
       "फ़र":"Feb","अप्रै":"Apr","जुला":"Jul","अग":"Aug","सितं":"Sep","अक्टू":"Oct","नवं":"Nov","दिसं":"Dec"},
 "C": {'दिल्ली': 'Delhi', 'नोएडा': 'Noida', 'गुरुग्राम': 'Gurugram', 'गाज़ियाबाद': 'Ghaziabad', 'फ़रीदाबाद': 'Faridabad', 'मेरठ': 'Meerut', 'चंडीगढ़': 'Chandigarh', 'लुधियाना': 'Ludhiana', 'अमृतसर': 'Amritsar', 'जालंधर': 'Jalandhar', 'पटियाला': 'Patiala', 'अंबाला': 'Ambala', 'पानीपत': 'Panipat', 'करनाल': 'Karnal', 'रोहतक': 'Rohtak', 'हिसार': 'Hisar', 'जम्मू': 'Jammu', 'श्रीनगर': 'Srinagar', 'शिमला': 'Shimla', 'देहरादून': 'Dehradun', 'हरिद्वार': 'Haridwar', 'जयपुर': 'Jaipur', 'जोधपुर': 'Jodhpur', 'उदयपुर': 'Udaipur', 'बीकानेर': 'Bikaner', 'कोटा': 'Kota', 'अजमेर': 'Ajmer', 'आगरा': 'Agra', 'मथुरा': 'Mathura', 'अलीगढ़': 'Aligarh', 'बरेली': 'Bareilly', 'मुरादाबाद': 'Moradabad', 'लखनऊ': 'Lucknow', 'कानपुर': 'Kanpur', 'अयोध्या': 'Ayodhya', 'प्रयागराज': 'Prayagraj', 'वाराणसी': 'Varanasi', 'गोरखपुर': 'Gorakhpur', 'पटना': 'Patna', 'मुज़फ़्फ़रपुर': 'Muzaffarpur', 'भागलपुर': 'Bhagalpur', 'रांची': 'Ranchi', 'जमशेदपुर': 'Jamshedpur', 'धनबाद': 'Dhanbad', 'कोलकाता': 'Kolkata', 'भुवनेश्वर': 'Bhubaneswar', 'गुवाहाटी': 'Guwahati', 'भोपाल': 'Bhopal', 'इंदौर': 'Indore', 'ग्वालियर': 'Gwalior', 'जबलपुर': 'Jabalpur', 'उज्जैन': 'Ujjain', 'रायपुर': 'Raipur', 'अहमदाबाद': 'Ahmedabad', 'वडोदरा': 'Vadodara', 'मुंबई': 'Mumbai', 'पुणे': 'Pune', 'नागपुर': 'Nagpur', 'नासिक': 'Nashik', 'हैदराबाद': 'Hyderabad', 'बेंगलुरु': 'Bengaluru', 'चेन्नई': 'Chennai', 'कोच्चि': 'Kochi', 'गोवा (पणजी)': 'Goa', 'न्यूयॉर्क': 'New York, USA', 'न्यू जर्सी': 'New Jersey, USA', 'शिकागो': 'Chicago, USA', 'ह्यूस्टन': 'Houston, USA', 'डलास': 'Dallas, USA', 'सैन फ़्रांसिस्को': 'San Francisco, USA', 'लॉस एंजेलिस': 'Los Angeles, USA', 'सिएटल': 'Seattle, USA', 'टोरंटो': 'Toronto, Canada', 'ब्रैम्पटन': 'Brampton, Canada', 'वैंकूवर': 'Vancouver, Canada', 'कैलगरी': 'Calgary, Canada', 'लंदन': 'London, UK', 'बर्मिंघम': 'Birmingham, UK', 'लेस्टर': 'Leicester, UK', 'दुबई': 'Dubai, UAE', 'सिंगापुर': 'Singapore', 'सिडनी': 'Sydney, Australia', 'मेलबर्न': 'Melbourne, Australia', 'ऑकलैंड': 'Auckland, NZ', 'काठमांडू': 'Kathmandu, Nepal'},
 "T": {"प्रतिपदा":"Pratipada","द्वितीया":"Dwitiya","तृतीया":"Tritiya","चतुर्थी":"Chaturthi","पंचमी":"Panchami","षष्ठी":"Shashthi","सप्तमी":"Saptami","अष्टमी":"Ashtami","नवमी":"Navami","दशमी":"Dashami","एकादशी":"Ekadashi","द्वादशी":"Dwadashi","त्रयोदशी":"Trayodashi","चतुर्दशी":"Chaturdashi","पूर्णिमा":"Purnima","अमावस्या":"Amavasya"},
 "N": {"अश्विनी":"Ashwini","भरणी":"Bharani","कृत्तिका":"Krittika","रोहिणी":"Rohini","मृगशिरा":"Mrigashira","आर्द्रा":"Ardra","पुनर्वसु":"Punarvasu","आश्लेषा":"Ashlesha","मघा":"Magha","पूर्वा फाल्गुनी":"Purva Phalguni","उत्तरा फाल्गुनी":"Uttara Phalguni","चित्रा":"Chitra","स्वाति":"Swati","विशाखा":"Vishakha","अनुराधा":"Anuradha","ज्येष्ठा":"Jyeshtha","पूर्वाषाढ़ा":"Purvashadha","उत्तराषाढ़ा":"Uttarashadha","धनिष्ठा":"Dhanishtha","शतभिषा":"Shatabhisha","पूर्वा भाद्रपद":"Purva Bhadrapada","उत्तरा भाद्रपद":"Uttara Bhadrapada","रेवती":"Revati"},
 "H": {"चैत्र":"Chaitra","वैशाख":"Vaishakh","ज्येष्ठ":"Jyeshtha","आषाढ़":"Ashadh","श्रावण":"Shravan","भाद्रपद":"Bhadrapad","आश्विन":"Ashwin","कार्तिक":"Kartik","मार्गशीर्ष":"Margashirsha","पौष":"Paush","माघ":"Magh","फाल्गुन":"Phalgun"},
}


PAR = {"पवित्रा एकादशी":"Pavitra Ekadashi","सौभाग्य पंचमी":"Saubhagya Panchami","गुड़ी पड़वा, उगादी":"Gudi Padwa, Ugadi","अचला एकादशी":"Achala Ekadashi","वसु बारस":"Vasu Baras","आंवला नवमी":"Amla Navami","देव दीपावली":"Dev Deepawali","श्यामा पूजा":"Shyama Puja","पूर्णिमा श्राद्ध":"Purnima Shraddh","वैशाख पूर्णिमा":"Vaishakh Purnima","हरिशयनी, पद्मा एकादशी":"Harishayani, Padma Ekadashi","रंगभरी एकादशी":"Rangbhari Ekadashi","विजयादशमी":"Vijayadashami","घटस्थापना":"Ghatasthapana","भीमसेनी एकादशी":"Bhimseni Ekadashi","अन्नदा एकादशी":"Annada Ekadashi","पारण":"Parana","मोक्षदा एकादशी":"Mokshada Ekadashi","बसौड़ा":"Basoda","गंगा जयंती":"Ganga Jayanti","तिलकुटा चौथ":"Tilkuta Chauth","सूर्य जयंती":"Surya Jayanti","पार्श्व, जलझूलनी एकादशी":"Parshva, Jaljhulni Ekadashi","संध्या अर्घ्य":"Sandhya Arghya","ललही छठ":"Lalahi Chhath","जानकी जयंती":"Janaki Jayanti","रंगवाली":"Rangwali","जीवित्पुत्रिका":"Jivitputrika","लक्ष्मी पूजा":"Lakshmi Puja","गणेश विसर्जन":"Ganesh Visarjan","रूप चौदस, छोटी दिवाली":"Roop Chaudas, Chhoti Diwali","श्रावण मास आरंभ":"start of Shravan month","कलम-दवात पूजा":"Kalam-Dawat Puja"}

# F: festival names, from the festival rules (Hindi name) and their English search names.
def _festivals():
    try:
        import festivals as _F, fest_info as _I
        from roman import roman_line as _rl
    except Exception:
        return {}
    over = {"janmashtami": "Krishna Janmashtami", "holi": "Holi", "diwali": "Diwali", "chaitra-navratri": "Chaitra Navratri",
            "sharadiya-navratri": "Sharadiya Navratri", "pitru-paksha": "Pitru Paksha begins", "sawan-start": "Sawan begins",
            "vat-savitri": "Vat Savitri Vrat", "hindu-nav-varsh": "Hindu Nav Varsh", "maha-shivratri": "Mahashivratri",
            "chhath-usha-arghya": "Chhath Usha Arghya", "chhath-nahay-khay": "Chhath Nahay-Khay", "holashtak": "Holashtak begins", "hal-shashthi": "Hal Shashthi", "akshay-navami": "Akshay Navami"}
    out = {}
    rules = list(_F.RULES) + list(getattr(_I, "EKA_RULES", []))
    for r in rules:
        key, hi = r[0], r[1]
        en = over.get(key) or (_I.INFO.get(key, {}).get("en") or "").split(" / ")[0].strip() or " ".join(w.capitalize() for w in key.split("-"))
        base = hi.split(" (")[0].strip()
        out.setdefault(base, en)
        if " (" in hi:
            par = hi.split(" (", 1)[1].rstrip(")")
            out.setdefault(hi, f"{en} ({PAR.get(par) or _rl(par).title()})")
    return out
ENT["F"] = _festivals()

# Short "at a glance" facts for each temple's live darshan page (live_pages.py): darshan time, aarti time,
# ticket/VIP, booking link, official site, one tip. Checked 25 Nov 2026 against temple sites and recent guides.
# Temples with a full guide in darshan_section.py (DARSHAN) are filled from that guide; add the rest here in batches.
# Fields: darshan, aarti, ticket, book=(url, label) or None, official=(url, label) or None, tip
LI_CHECKED = "25 नवंबर 2026"
LI = {
 "somnath": dict(
  darshan="रोज़ सुबह 6:00 से रात 10:00 बजे तक", aarti="सुबह 7:00, दोपहर 12:00, शाम 7:00",
  ticket="आम दर्शन मुफ़्त; दर्शन पास, पूजा और कमरे ट्रस्ट की वेबसाइट से", book=("https://somnath.org/", "somnath.org"),
  official=("https://somnath.org/", "somnath.org"),
  tip="रात 8 से 9 बजे ‘जय सोमनाथ’ लाइट एंड साउंड शो होता है। पैसे सिर्फ़ ट्रस्ट की वेबसाइट पर भरें, किसी WhatsApp नंबर या एजेंट को नहीं।"),
 "omkareshwar": dict(
  darshan="सुबह 5:00 से रात लगभग 9:30 बजे तक (बीच में भोग के समय कुछ देर बंद)", aarti="मंगला आरती सुबह 4:30; दोपहर भोग 12:20 के आसपास; शाम शयन आरती",
  ticket="आम दर्शन मुफ़्त; शीघ्र दर्शन ₹300 प्रति व्यक्ति (समय-स्लॉट वाला)", book=("https://shriomkareshwar.org/", "shriomkareshwar.org"),
  official=("https://shriomkareshwar.org/", "shriomkareshwar.org"),
  tip="शीघ्र दर्शन टिकट सिर्फ़ चुने हुए स्लॉट में मान्य है। सावन और सोमवार को भीड़ बहुत रहती है; ममलेश्वर दर्शन भी साथ में करें।"),
 "trimbakeshwar": dict(
  darshan="सुबह लगभग 5:30 से रात 9:00 बजे तक", aarti="सुबह, दोपहर और शाम की आरती; विशेष पूजा का समय बुकिंग के अनुसार",
  ticket="आम दर्शन मुफ़्त; VIP (डोनेशन) दर्शन पास ₹200 प्रति व्यक्ति", book=("https://trimbakeshwartrust.com/", "trimbakeshwartrust.com"),
  official=("https://trimbakeshwartrust.com/", "trimbakeshwartrust.com"),
  tip="VIP पास पर लिखे नाम वाला असली फ़ोटो पहचान पत्र साथ रखें। सावन के सोमवार और महाशिवरात्रि पर घंटों की कतार लगती है।"),
 "banke-bihari-vrindavan": dict(
  darshan="सर्दियाँ: सुबह 8:45 – दोपहर 1:00, शाम 4:30 – रात 8:30 · गर्मियाँ: सुबह 7:45 – 12:00, शाम 5:30 – 9:30", aarti="श्रृंगार आरती सुबह (सर्दियों में लगभग 9:00); राजभोग आरती दोपहर; शयन आरती रात को बंद होने से पहले",
  ticket="दर्शन मुफ़्त; मंगला आरती साल में सिर्फ़ जन्माष्टमी पर होती है", book=None, official=None,
  tip="समय दिवाली के बाद (सर्दी) और होली के बाद (गर्मी) बदलता है। पैसे लेकर ‘VIP दर्शन’ कराने का दावा करने वालों से सावधान रहें।"),
 "shirdi-sai-baba": dict(
  darshan="सुबह लगभग 4:45 से रात 11:00 बजे तक", aarti="काकड़ आरती सुबह ~5:15, मध्यान्ह आरती 12:00, धूप आरती सूर्यास्त पर, शेज आरती रात 10:30",
  ticket="आम दर्शन मुफ़्त; पेड दर्शन और आरती पास सिर्फ़ ऑनलाइन", book=("https://online.sai.org.in/", "online.sai.org.in"),
  official=("https://sai.org.in/", "sai.org.in"),
  tip="गुरुवार को सबसे ज़्यादा भीड़ रहती है। बुक किए गए दर्शन/आरती की तारीख़ और स्लॉट बाद में बदले नहीं जा सकते।"),
 "dagdusheth-ganpati-pune": dict(
  darshan="सुबह 6:00 से रात 11:00 बजे तक", aarti="सुप्रभात आरती 7:30, मध्यान्ह आरती 3:00, महामंगल आरती रात 8:00–9:00, शेज आरती 10:30",
  ticket="दर्शन मुफ़्त, कोई टिकट नहीं", book=None, official=("https://www.dagdushethganpati.com/", "dagdushethganpati.com"),
  tip="संकष्टी चतुर्थी और गणेशोत्सव में समय बढ़ जाता है और बहुत भीड़ रहती है। मंदिर शनिवारवाड़ा के पास बुधवार पेठ में है।"),
 "dwarkadhish": dict(
  darshan="सुबह 6:30 – दोपहर 1:00, शाम 5:00 – रात 9:30", aarti="मंगला आरती 6:30, श्रृंगार आरती 10:30, संध्या आरती 7:30, शयन आरती 8:30",
  ticket="आम दर्शन मुफ़्त", book=None, official=("https://www.dwarkadhish.org/", "dwarkadhish.org"),
  tip="भोग के समय बीच-बीच में कुछ मिनट दर्शन बंद रहते हैं। मंदिर पर ध्वजा दिन में कई बार बदलती है — यह दृश्य ज़रूर देखें।"),
 "jagannath-puri": dict(
  darshan="सुबह लगभग 5–6 बजे से रात 9–10 बजे तक, बीच में भोग-अनुष्ठान के समय दर्शन रुकते हैं", aarti="मंगल आरती सुबह 5:00; संध्या आरती शाम लगभग 5:30–6:00",
  ticket="आम दर्शन मुफ़्त", book=None, official=("https://www.shreejagannatha.in/", "shreejagannatha.in"),
  tip="मंदिर में सिर्फ़ हिंदुओं को प्रवेश है; मोबाइल, कैमरा और चमड़े का सामान अंदर नहीं जाता। महाप्रसाद आनंद बाज़ार में मिलता है।"),
 "shrinathji-nathdwara": dict(
  darshan="सुबह लगभग 5:30 – 12:30, शाम 4:00 – 8:00 (दर्शन ‘झाँकी’ में खुलते हैं, बीच में पट बंद)", aarti="मंगला, श्रृंगार, ग्वाल, राजभोग, उत्थापन, भोग, संध्या आरती, शयन — रोज़ 8 झाँकी",
  ticket="दर्शन मुफ़्त", book=None, official=("https://www.nathdwaratemple.org/", "nathdwaratemple.org"),
  tip="झाँकी का समय मौसम और त्योहार से रोज़ बदलता है; मंदिर अगले दिन का समय पहले घोषित करता है। झाँकी कुछ ही मिनट की होती है, पहले पहुँचें।"),
 "salasar-balaji": dict(
  darshan="सुबह लगभग 5:30 से रात 9:00 बजे तक", aarti="मंगला आरती 5:30, राजभोग 10:15, संध्या आरती शाम, शयन आरती रात (सर्दियाँ); मंगलवार को राजभोग महाप्रसाद आरती",
  ticket="दर्शन मुफ़्त", book=None, official=None,
  tip="मंगलवार, शनिवार और हनुमान जयंती पर बहुत भीड़ रहती है। नारियल चढ़ाने और मनौती का धागा बाँधने की परंपरा है।"),
 "sabarimala-ayyappa": dict(
  darshan="सिर्फ़ तय समय पर खुलता है — मंडल काल 16 नवंबर से 27 दिसंबर 2026; मकरविलक्कु के लिए 30 दिसंबर से (मकरज्योति 14 जनवरी 2027)", aarti="हरिवरासनम रोज़ रात को मंदिर बंद होने से पहले",
  ticket="दर्शन मुफ़्त, पर वर्चुअल क्यू बुकिंग ज़रूरी", book=("https://sabarimalaonline.org/", "sabarimalaonline.org"),
  official=("https://sabarimalaonline.org/", "sabarimalaonline.org"),
  tip="स्पॉट बुकिंग निलक्कल, एरुमेली और वंडीपेरियार में है, पंपा में नहीं। बाकी साल मंदिर हर मलयालम महीने की शुरुआत में कुछ दिन खुलता है।"),
 "haridwar-ganga-aarti": dict(
  darshan="हर की पौड़ी (ब्रह्मकुंड) घाट 24 घंटे खुला", aarti="सुबह सूर्योदय के आसपास (सर्दियों में ~6:30); शाम सूर्यास्त पर (सर्दियों में ~5:30, गर्मियों में ~6:30–7:00)",
  ticket="आरती देखना मुफ़्त, कोई टिकट नहीं", book=None, official=None,
  tip="शाम की आरती का समय सूर्यास्त के साथ खिसकता है; अच्छी जगह के लिए 45–60 मिनट पहले पहुँचें। भीड़ में जेब और बच्चों का ध्यान रखें।"),
 "varanasi-ganga-aarti": dict(
  darshan="दशाश्वमेध घाट 24 घंटे खुला", aarti="शाम सूर्यास्त के बाद — सर्दियों में लगभग 6:00, गर्मियों में लगभग 7:00; करीब 45 मिनट",
  ticket="घाट से आरती देखना मुफ़्त; नाव या छत से देखने का किराया अलग", book=None, official=None,
  tip="गोदौलिया चौराहे से पैदल 10 मिनट। अस्सी घाट पर सुबह की ‘सुबह-ए-बनारस’ आरती भी होती है।"),
}

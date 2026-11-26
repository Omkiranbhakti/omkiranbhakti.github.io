#!/usr/bin/env python3
"""Build tools/master/kc_master.csv: Tryambak cards (facts only) + OKB additions, matched with live Kaal-Chakra events.
Usage: python3 kc_master.py <repo> <tryambak_dir> <okb_extras.txt>"""
import csv, json, re, sys, difflib, unicodedata as U
repo, tdir, extras = sys.argv[1:4]
fold = lambda s: re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9 ]', ' ', U.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower())).strip()
slug = lambda r: re.sub(r'[^a-z0-9]+', '-', r.lower()).strip('-')

# live events
h = open(f'{repo}/kaal-chakra/index.html', encoding='utf8').read()
LIVE = re.findall(r"^\[(-?[\d.]+|NOW),'(\w+)','([^']*)','([^']*)','[^']*','[^']*','([^']*)'", h, re.M)
EN = json.load(open(f'{repo}/src/kc_en.json', encoding='utf8'))
IMG = json.load(open(f'{repo}/kaal-chakra/img/pick.json', encoding='utf8')) if True else {}
live = [dict(y=y, kind=k, hi=t, place=p, slug=slug(r), en=EN.get(slug(r), [''])[0]) for y, k, t, p, r in LIVE]

CAT = {'Itihāsa & Purāṇa tradition': ('c', 1), 'Foretold & scheduled': ('b', 1), 'Temples & tīrthas': ('t', 1),
       'Ācāryas, saints & seers': ('s', 1), 'Scriptures & texts': ('-', 2), 'Darśana & philosophy': ('-', 2),
       'Sampradāyas & institutions': ('-', 2), 'Civilization & archaeology': ('-', 2), 'Arts, sciences & letters': ('-', 3),
       'Kingdoms & rulers': ('v', 3), 'Wars, invasions & resistance': ('-', 3), 'Reform, law & nation': ('-', 3), 'Beyond Bhārata': ('-', 3)}
CORE = re.compile(r'r.?g ?veda|veda\b|upani|g[iī]t[aā]|r[aā]m[aā]ya|mah[aā]bh[aā]rata|bh[aā]gavata|pur[aā][nṇ]a|yoga ?s[uū]tra|brahma ?s[uū]tra|r[aā]macaritam[aā]nas|kumbh', re.I)

rows = []
for x in csv.DictReader(open(f'{tdir}/Cards.csv', encoding='utf8')):
    kind, pr = CAT.get(x['Category'], ('-', 3))
    if pr > 1 and CORE.search(x['Title']): pr = 1
    rows.append(dict(id=x['Card ID'], source='TRY', status='pending', priority=pr, kind=kind, category=x['Category'],
                     region=x['Region'], sort_year=x['Sort year'], date=x['Date'], title_en=x['Title'], title_hi='',
                     n_sources=x['No. of Sources'], slug='', image='', verify='स्रोत Tryambak में', note=''))
n = 0
for ln in open(extras, encoding='utf8'):
    ln = ln.strip()
    if not ln or ln.startswith('#'): continue
    k, y, hi, en, rg, pr = [f.strip() for f in ln.split('|')]
    n += 1
    rows.append(dict(id=f'okb-{n:03d}', source='OKB', status='pending', priority=int(pr), kind=k, category='OKB addition',
                     region=rg, sort_year=y, date='', title_en=en, title_hi=hi, n_sources='0', slug='', image='',
                     verify='स्रोत जोड़ना बाकी' + ('' if y else '; साल बाकी'), note=''))

# OKB additions that Tryambak already has: keep the Tryambak card, give it the Hindi name and priority 1
DUP = {'त्रिपुर सुंदरी, उदयपुर (त्रिपुरा)': 'nb-03', 'पशुपतिनाथ, काठमांडू': '07-107', 'जनकपुर — जानकी मंदिर': 'nb-06', 'गया का विष्णुपद मंदिर': '11-67',
       'शारदा पीठ, कश्मीर': '20-17', 'अष्टविनायक': '11-81', 'दुर्गा पूजा': '11-95', 'पुरी की रथ यात्रा': '20-4', 'ओणम और राजा महाबली': '20-5',
       'गणेश चतुर्थी — सार्वजनिक उत्सव': '12-63', 'माधवदेव और बरगीत': '10-102', 'उनाकोटी के शिव शिल्प': 'na-20', 'जागेश्वर धाम': '07-77'}
byid = {r['id']: r for r in rows}
for r in [r for r in rows if r['title_hi'] in DUP]:
    t = byid[DUP[r['title_hi']]]; t.update(title_hi=r['title_hi'], priority=1, kind=r['kind']); rows.remove(r)
for r in rows:
    if r['id'] == '17-84': r.update(title_hi='मायापुर इस्कॉन', priority=1)
# match live -> rows (same kind family + title similarity, nearby year)
used = set()
STOP = set('the and of at in on to from with born death dies begins begin beginning temple temples mandir shri sri sant saint swami great his her their into for rebuilt built founded a an by its yuga'.split())
def norm(t):
    for a, b in (('sh','s'),('ch','c'),('ee','i'),('oo','u'),('aa','a'),('w','v'),('ph','p'),('th','t'),('dh','d'),('bh','b'),('kh','k'),('gh','g'),('jh','j'),('ri','r'),('y','i')): t = t.replace(a, b)
    return t
def toks(t): return [norm(w) for w in fold(t).split() if len(w) >= 4 and w not in STOP]
def shared(a, b): return sum(1 for x in toks(a) if any(difflib.SequenceMatcher(None, x, y).ratio() >= .8 for y in toks(b)))
FIX = {'सीता हरण': 'Abduction of Sītā', 'वेदव्यास का जन्म': 'Vyāsa born to Satyavatī', 'श्रीकृष्ण का जन्म': 'Birth of Śrī Kṛṣṇa',
       'निंबार्काचार्य और राधा-कृष्ण उपासना': 'Nimbārka and the Dvaitādvaita', 'सोमनाथ मंदिर का पुनर्निर्माण': 'Somanātha reconstruction pledged',
       'अनंत पद्मनाभस्वामी मंदिर': None, 'माँ आनंदमयी': 'Ānandamayī Mā recognised', 'काशी विश्वनाथ मंदिर': 'Kāśī Viśvanātha rebuilt by Ahilyābāī',
       'मदुरै का मीनाक्षी मंदिर': 'Madurai Nāyakas and the Mīnākṣī', 'रामानुजाचार्य — विशिष्टाद्वैत': 'Rāmānuja’s Śrī Bhāṣya',
       'स्वामी विवेकानंद — शिकागो': 'Vivekānanda at the Parliament', 'बेलूर मठ': None, 'श्री अरविंद, पुदुचेरी': 'Aurobindo arrives at Pondicherry',
       'विद्यारण्य और विजयनगर': None,
 'सत्ययुग का आरंभ': 'Satya (Kṛta) Yuga', 'राम सेतु का निर्माण': 'Rāma Setu is built', 'वृंदावन की लीलाएँ': "Kṛṣṇa's Vraja līlā", 'श्रीकृष्ण का स्वधाम गमन': "Kṛṣṇa's departure",
       'कलियुग का आरंभ': 'Kali Yuga begins', 'पांडवों का महाप्रस्थान': 'Mahāprasthāna', 'संत कबीर': 'Kabīr, the weaver', 'सूरदास': 'Sūrdāsa', 'संत रविदास': 'Ravidāsa',
       'लल्लेश्वरी — लल्ल देद': 'Lallā, the Kashmiri', 'संत चोखामेला': 'Cokhāmeḷā', 'स्वामी रामानंद': 'Rāmānanda and the', 'सबरीमला के अयप्पा': 'Śabarimala and the',
       'गुरुवायूर के श्रीकृष्ण': 'Guruvāyūr temple rises', 'कनकदास': 'Kanaka Dāsa', 'श्रीमंत शंकरदेव': 'Śaṅkaradeva born', 'घृष्णेश्वर ज्योतिर्लिंग': 'Ghṛṣṇeśvara and',
       'हर की पौड़ी, हरिद्वार': 'Bathing fairs at Haridvāra', 'महाबलीपुरम का तट मंदिर': 'Narasiṃhavarman II builds', 'कांची का कैलाशनाथर मंदिर': 'Rājasiṃha Pallava builds',
       'केदारनाथ धाम': "Śaṅkara's mahāsamādhi at Kedā",
       'ऋग्वेद — सबसे प्राचीन ग्रंथ': 'Ṛgveda Saṃhitā composed', 'याज्ञवल्क्य-मैत्रेयी संवाद': 'Yājñavalkya and Maitreyī', 'पतंजलि का योगसूत्र': 'Yoga Sūtra of Patañjali',
       'महाशिवरात्रि और एकादशी व्रत': 'Mahāśivarātri and Ekādaśī', 'नवरात्रि और शारदीय दुर्गा उत्सव': 'Navarātri and the autumn', 'अप्पर — तिरुनावुक्करसर': 'Appar (Tirunāvukkarasar)',
       'संबंदर — बाल-संत': 'Tiruñāṉacampantar', 'माणिक्कवाचकर और तिरुवाचकम्': 'Māṇikkavācakar', 'नम्मालवार और तिरुवायमोऴि': 'Nammāḻvār', 'माधवदेव और नामघोषा': 'Mādhavadeva composes',
       'कृत्तिवासी रामायण': 'Kṛttivāsa', 'अक्कलकोट के स्वामी समर्थ': 'Akkalkoṭ', 'बामाखेपा — तारापीठ के संत': 'Bāmākṣepā', 'मोरया गोसावी — गणेश भक्त': 'Morayā Gosāvī',
       'जनाबाई, मुक्ताबाई और सोयराबाई': 'Janābāī', 'अक्का महादेवी': 'Akka Mahādevī', 'गुरु राघवेंद्र स्वामी, मंत्रालयम': 'Raghavendra Tīrtha enters', 'शारदा पीठ, कश्मीर': 'Śāradā Pīṭha',
       'पशुपतिनाथ, काठमांडू': 'Paśupatinātha in Licchavi', 'द्वादश ज्योतिर्लिंग': 'Twelve jyotirliṅgas', '51 शक्तिपीठ': 'Fifty-one Śakti', 'भारत के चार धाम': 'Cār Dhām of Bhārata',
       'गया का विष्णुपद मंदिर': 'Viṣṇupada temple', 'रथ यात्रा': 'Ratha-yātrā festivals'}
FIX.update({'कारैक्काल अम्मैयार': 'Kāraikkāl Ammaiyār, Śaiva poet-saint', 'पहले तीन आळवार — तिरुक्कोवलूर का दीप': 'First three Āḻvārs', 'सुंदरर और तिरुत्तोंडत्तोगै': 'Sundarar and the Tiruttoṇṭattokai', 'पेरियाळवार और कुलशेखर आळवार': 'Periyāḻvār and Kulaśekhara', 'तिरुमंगै आळवार': 'Tirumaṅgai Āḻvār and the Periya Tirumoḻi', 'आदि शंकराचार्य का जन्म': 'Birth of Ādi Śaṅkarācārya', 'शंकर का संन्यास और गुरु गोविंदपाद': 'Śaṅkara takes saṃnyāsa and finds Govindapāda', 'काशी में चांडाल प्रसंग — मनीषा पंचकम्': 'Encounter with the caṇḍāla at Kāśī', 'शंकर-मंडन मिश्र शास्त्रार्थ — उभय भारती निर्णायक': 'Ubhaya Bhāratī challenges Śaṅkara', 'नाथमुनि को मिला दिव्य प्रबंधम्': 'Nāthamuni recovers the Divya Prabandham', 'यामुनाचार्य (आळवंदार)': 'Yāmunācārya (Āḷavandār) of Śrīraṅgam', 'रामानुजाचार्य का जन्म': 'Birth of Rāmānujācārya', 'रामानुज ने सबको सुनाया गुप्त मंत्र': 'Rāmānuja and the open mantra', 'बसवेश्वर का जन्म': 'Birth of Basava (Basaveśvara)', 'मध्वाचार्य का जन्म': 'Birth of Madhvācārya', 'ज्ञानेश्वर की संजीवन समाधि': "Jñāneśvara's sañjīvana samādhi", 'गुरु नानक देव का जन्म': 'Guru Nānak born', 'मीराबाई का जन्म': 'Mīrābāī born in Rajasthan', 'चैतन्य महाप्रभु का संन्यास': 'Caitanya takes saṃnyāsa', 'हरिदास ठाकुर — नामाचार्य': "Haridāsa Ṭhākura, nāmācārya of Caitanya's circle", 'गोस्वामी तुलसीदास का जन्म': 'Tulasīdāsa, poet of the Rāmacaritamānasa, born', 'संत तुकाराम का वैकुंठ गमन': "Tukārāma's departure from Dehū", 'स्वामी विवेकानंद का जन्म': 'Birth of Vivekānanda in Calcutta', 'नरेंद्र की श्रीरामकृष्ण से भेंट': 'Narendra meets Rāmakṛṣṇa', 'रमण महर्षि का आत्म-बोध': "Ramaṇa's death-experience at Madurai", 'खजुराहो का लक्ष्मण मंदिर': 'Lakṣmaṇa temple, Khajurāho', 'बेलूर चेन्नकेशव मंदिर': 'Cennakeśava temple, Belūr', 'हळेबीडु का होयसळेश्वर मंदिर': 'Hoysaḷeśvara temple, Haḷebīḍu', 'मुक्तेश्वर मंदिर, भुवनेश्वर': 'Mukteśvara temple at Bhubaneśvara', 'ऐहोळे — मंदिर स्थापत्य का पालना': 'Aihoḷe temples of the early Cālukyas', 'पट्टदकल के चालुक्य मंदिर': 'Paṭṭadakal temples of the Cālukyas', 'दारासुरम का ऐरावतेश्वर मंदिर': 'Airāvateśvara temple, Dārāsuram', 'गंगैकोंडचोलपुरम मंदिर': 'Gaṅgaikoṇḍacōḻapuram temple', 'रामप्पा मंदिर': 'Rāmappa temple at Pālampeṭ', 'सोमनाथपुर का केशव मंदिर': 'Keśava temple, Somanāthapura', 'भोजेश्वर मंदिर, भोजपुर': 'Bhojeśvara temple at Bhojpur', 'मुंडेश्वरी मंदिर': 'Muṇḍeśvarī temple', 'देवगढ़ का दशावतार मंदिर': 'Daśāvatāra temple, Deogarh', 'जागेश्वर धाम': 'Jageśvara and Baijnāth temple groups', 'शंकराचार्य मंदिर, श्रीनगर': 'Śaṅkarācārya Temple on Gopādri hill', 'कटासराज — शिव के आँसुओं का सरोवर': "Katas Raj, Śiva's tears and the Yakṣa Praśna", 'उनाकोटी — एक कम एक करोड़': "Unakoti's rock-cut Śiva reliefs", 'लेपाक्षी वीरभद्र मंदिर': 'Lepākṣī Vīrabhadra temple', 'ओरछा के राम राजा': "Orchā's Caturbhuja and Rāma Rājā temples", 'डाकोर के रणछोड़राय': 'Raṇachoḍarāya temple built at Ḍākor', 'अष्टविनायक': 'Peśvā patronage of the Aṣṭavināyaka temples', 'मंगेशी मंदिर — गोवा के मंगेश': 'Mangeśa liṅga moved from Kuśasthalī to Priol', 'त्रिपुर सुंदरी मंदिर, उदयपुर (त्रिपुरा)': 'Dhanya Māṇikya builds Tripurā Sundarī temple', 'ओणम': 'Oṇam in Tamil and Kerala sources', 'कार्तिगै दीपम्': 'Kārttikai lamps in Cōḻa temple life'})  # batch 06
for L in live:
    best, score = None, 0
    if L['hi'] in FIX:
        t = FIX[L['hi']]
        for i, r in enumerate(rows):
            if t and i not in used and r['source'] == 'TRY' and r['title_en'].startswith(t): best, score = i, 8; break
        if best is None: score = 0
        else:
            pass
    for i, r in enumerate(rows):
        if i in used: continue
        if L['hi'] in FIX: break
        if r['source'] == 'OKB':
            if r['title_hi'] == L['hi']: best, score = i, 9; break
            continue
        sh = shared(L['en'], r['title_en'])
        if not sh: continue
        s = difflib.SequenceMatcher(None, norm(fold(L['en'])), norm(fold(r['title_en']))).ratio() + .25 * sh
        try:
            if L['y'] != 'NOW' and abs(float(r['sort_year']) - float(L['y'])) < max(80, abs(float(L['y'])) * .05): s += .2
        except ValueError: pass
        if s > score: best, score = i, s
    if best is not None and score >= .95:
        r = rows[best]; used.add(best)
        r.update(status='live', title_hi=L['hi'], slug=L['slug'], image='हाँ' if L['slug'] in IMG else 'नहीं',
                 note=f"match {score:.2f}" + (f"; live: {L['en']}" if score < 9 else ''))
    else:
        rows.append(dict(id=f"okb-live-{L['slug']}", source='OKB', status='live', priority=1, kind=L['kind'], category='OKB (live)',
                         region=L['place'], sort_year=L['y'], date='', title_en=L['en'], title_hi=L['hi'], n_sources='',
                         slug=L['slug'], image='हाँ' if L['slug'] in IMG else 'नहीं', verify='', note='live, Tryambak में मेल नहीं'))

def yk(r):
    try: return float(r['sort_year'])
    except ValueError: return 9e9
rows.sort(key=lambda r: (r['priority'], yk(r)))
F = list(rows[0].keys())
w = csv.DictWriter(open(f'{repo}/tools/master/kc_master.csv', 'w', encoding='utf8', newline=''), F)
w.writeheader(); w.writerows(rows)
import collections as C
print('rows', len(rows), C.Counter(r['status'] for r in rows), C.Counter((r['priority'], r['status']) for r in rows))
print('weak matches:'); [print(' ', r['title_hi'], '<->', r['title_en'], r['note']) for r in rows if r['status'] == 'live' and r['note'].startswith('match 0.')]

# 30-day content roadmap (28 Oct – 27 Nov 2026)

Method: upcoming festivals (src/fest_years.json) × what people search (Google suggest / People also ask pattern) × what the site already has.
Rule: publish each page at least 7–10 days before its festival, link it from the festival's "kab hai" page, and queue it for indexing the same day.
The "kab hai" pages already exist for every festival below. The gaps are the other intents people search: what to buy, the puja vidhi, the katha, rules and wishes.
Competition: Google's results mostly show news sites with 2025 articles or old URLs, so fresh 2026 pages with exact dates have a real chance.
Search Console query data is not used yet (the browser was offline on 27 Oct). Re-rank this list once it is available.

| # | Publish by | Page (slug) | Search intent | Festival date | Status |
|---|---|---|---|---|---|
| 1 | 29 Oct | dhanteras-kya-kharide.html: what to buy and what not to buy, buying muhurat | informational / commercial (Amazon puja items) | Dhanteras 6 Nov | done 27 Oct |
| 2 | 29 Oct | dhanteras-puja-vidhi.html: Dhanvantari, Kuber and Yam deepdaan vidhi | informational | 6 Nov | done 27 Oct |
| 3 | 31 Oct | govardhan-puja-vidhi.html: Annakut, parikrama, vidhi | informational | 10 Nov | todo |
| 4 | 31 Oct | bhai-dooj-tilak-vidhi.html: tilak muhurat and vidhi, what to give | informational | 11 Nov | todo |
| 5 | 2 Nov | chhath-vrat-niyam.html: the 4-day rules | informational | 13–16 Nov | todo |
| 6 | 2 Nov | chhath-geet.html: traditional Chhath songs (traditional lyrics only) + our videos | informational / video | 15 Nov | todo |
| 7 | 5 Nov | dev-uthani-ekadashi-katha.html + puja vidhi (sugarcane mandap, waking Bhagwan) | informational | 20 Nov | todo |
| 8 | 7 Nov | tulsi-vivah-vidhi.html: vidhi + samagri list (Amazon) | informational / commercial | 21 Nov | todo |
| 9 | 10 Nov | dev-deepawali-varanasi.html: date, ghats, Ganga aarti timings, boat/crowd tips, live link | informational / travel | 24 Nov | todo |
| 10 | 10 Nov | guru-nanak-jayanti-kab-hai.html: date, gurpurab, what happens | informational (same day as Kartik Purnima) | 24 Nov | todo |
| 11 | 12 Nov | kartik-purnima-snan-daan.html: snan muhurat, what to donate, deepdaan | informational | 24 Nov | todo |
| 12 | 15 Nov | utpanna-ekadashi-katha.html | informational | Dec (check date) | todo |
| 13 | 18 Nov | kaal-bhairav-jayanti-puja-vidhi.html + katha | informational | 1 Dec | todo |
| 14 | 20 Nov | margashirsha-maas.html: month guide, Margashirsha Guruvar (Lakshmi vrat) | informational | Nov–Dec | todo |
| 15 | 25 Nov | vivah-panchami-katha.html | informational | 14 Dec | todo |
| 16 | ongoing | darshan guide pages: add 5 more temples (Somnath, Omkareshwar, Banke Bihari, Shirdi, Jagannath Puri) | informational / travel | evergreen | todo |

Every new page needs:
- An FAQ (5–8 real questions) with FAQPage schema.
- Internal links to the festival's "kab hai" page, its aarti or katha, and the live darshan page.
- English translations in src/en_tr/ so the English page is published too.
- An entry in seo/index-queue.txt.

Review: after 30 days, use Search Console to see which pages got impressions and build more pages on the topics that worked.

## Search Console findings (27 Oct 2026, omkiranbhakti.com, 497 queries, 5.9k impressions, 47 clicks)
The real questions people typed when our pages appeared. Ordered by opportunity:
| Finding | Data | Action | Status |
|---|---|---|---|
| Bhadra questions are the biggest topic ("bhadra kab se kab tak", "kal bhadra hai kya") | ~400 impressions, position 5–10, almost 0 clicks | bhadra-kaal.html title → "भद्रा कब से कब तक है?", description with end time, new FAQ "क्या कल भद्रा है?" | done 27 Oct |
| Karwa Chauth samagri list (~40 variants) | ~150 impressions, position 9–11 | festival is on 29 Oct; before Karwa Chauth 2027, add the exact phrases ("kya kya saman lagta hai", "saman list") as FAQ | later |
| Purnima / amavasya kab hai | ~50 impressions, position 6–10 | make purnima-amavasya-2026-2027.html answer "अगली पूर्णिमा / अमावस्या कब है" at the top | todo |
| Kharmas / malmas 2027 | ~40 impressions, position 6–9 | kharmas page: add FAQ for the March 2027 kharmas and "मलमास" | todo |
| Sant bhajan meanings (Jau kahan taji charan, Man pachtai hai, Maya maha thagni) | position 2–11 | more Surdas / Kabir / Tulsi bhajan pages with meaning | todo |
| Rahu kaal / choghadiya Faridabad | position 9–11 | fine; the city page is indexed and improving | — |
| Local festival names: Kalam-dawat puja, Jhojhiya, Vasubaras 2027, Jitiya 2027 | 1–5 impressions each | short "kab hai" pages for Jhojhiya and Vasubaras | todo |
| English lyrics queries (Gayatri, Mahamrityunjay, Ganesh chalisa in English) | position 48–90 | English pages are new; wait 4 weeks, then improve titles | later |

## Live darshan (Google suggest, 27 Oct 2026)
Every temple has "<temple> live darshan today / aaj ke darshan / time / app / official channel / youtube" suggestions. live-darshan.html used #hash links, which Google does not index separately, so on 27 Oct each of the 42 temples got its own page (src/live_pages.py, e.g. mahakal-live-darshan.html). The FAQ on each page answers "today", "time", "official channel" and "app". The pages are linked from the hub and the guide pages, and the top 17 are queued for indexing. Temples people search for that we do not have yet: Mehandipur Balaji, Baba Baidyanath Dham, Sundha Mata, Shantikunj Haridwar, Amarnath (yatra season), Lalbaugcha Raja (Ganesh festival) — add them once an official channel is verified.

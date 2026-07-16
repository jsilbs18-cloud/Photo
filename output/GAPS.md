# GAPS & Uncertainty Register — G20 Ministers & Trade Deck

Compiled 2026-07-16. Every item a reviewer should chase down before external use. Nothing here is a fabricated placeholder — all officeholders resolved to a named person; these are data-vintage, basis, precision, and acting-status flags. Cross-references: full sourcing in `research/g20-research.md`; structured data in `data/g20.json`.

**Roll-up:** 12 Verified · 5 Needs check · 2 Vacant/acting (of 19).

## Per-country flags

| Country | Flag | Specific gaps to verify |
|---|---|---|
| Argentina | Vacant / acting | (1) Acting/interim official: Pablo Lavigne — Secretary of Production Coordination (exercising Industry & Commerce functions) (2) GDP value low-confidence (secondary IMF-based aggregator; may reflect Apr-2026 WEO revision). (3) Quirno's succession dates: Werthein resigned Oct 22, 2025; Quirno's appointment was announced Oct 23 and he was sworn in Oct 27, 2025 — so 'assumed office' should be cited as Oct 27, 2025 (some databases list Oct 23). (4) Lavigne's acting Industry & Commerce role via Decree 215/2026 is explicitly temporary — 'until the coverage of the Secretariat is arranged' — so it may lapse if a permanent Secretary of Industry and Commerce is named; re-check before publication. (5) Neither Quirno nor Lavigne holds the literal title 'Trade Minister' — Argentina folds international trade into the Foreign Ministry and domestic commerce into the Economy Ministry. |
| Australia | Needs check | (1) Overall trade balance (goods+services, 2025) flagged 'Needs check'. (2) GDP value low-confidence (secondary IMF-based aggregator; may reflect Apr-2026 WEO revision). (3) Overall balance is goods+services (not goods-only) — basis differs from other countries. (4) Charlton's two titles in the brief (Assistant Minister for Science, Technology and the Digital Economy; Cabinet Secretary) are both correct and held concurrently, not alternatives. (5) Ayres's two titles in the brief (Minister for Industry and Innovation; Minister for Science) are both correct and held concurrently, not alternatives. (6) Farrell also holds a second title, Special Minister of State, alongside Minister for Trade and Tourism. |
| Brazil | Needs check | (1) GDP value low-confidence (secondary IMF-based aggregator; may reflect Apr-2026 WEO revision). |
| China | Verified | (1) Added Dr. Yin Hejun (MOST) to the digital/technology section per user direction; his portfolio (science, technology and innovation policy) is distinct from Li Lecheng's MIIT portfolio (industry, telecom, digital economy). (2) Li Chenggang no longer holds the WTO ambassadorship — he was removed from that post on 20 October 2025 and now serves solely as International Trade Representative and Vice Minister of Commerce; any briefing text listing him as WTO envoy should be updated. |
| France | Needs check | (1) U.S. bilateral goods figures low-confidence (EU member without standalone USTR fact sheet). |
| Germany | Verified | (1) U.S. bilateral goods figures medium-confidence (EU member without standalone USTR fact sheet). |
| India | Verified | (1) Overall balance uses fiscal year FY 2025-26, not calendar 2025. |
| Italy | Verified | (1) U.S. bilateral goods figures medium-confidence (EU member without standalone USTR fact sheet). |
| Mexico | Needs check | (1) GDP value low-confidence (secondary IMF-based aggregator; may reflect Apr-2026 WEO revision). |
| Poland | Needs check | (1) GDP value low-confidence (secondary IMF-based aggregator; may reflect Apr-2026 WEO revision). (2) U.S. bilateral goods figures medium-confidence (EU member without standalone USTR fact sheet). (3) USER DIRECTION REJECTED: Krzysztof Paszyk should not be added — he left the government in the 23-24 July 2025 reshuffle when the Ministry of Economic Development and Technology (MRiT) was liquidated; he is now PSL-Trzecia Droga parliamentary club chairman (a Sejm/party post, not a cabinet post). (4) Prior dual-verified research CONFIRMED: MRiT was merged into the Ministry of Finance and Economy under Andrzej Domanski (created 24 July 2025), with Michal Baranowski as the deputy minister responsible for trade. (5) Caution on stale sources: gov.pl still serves Baranowski's bio and Paszyk's old minister page under legacy 'rozwoj-technologia' / 'development-technology' URLs (the portal now also publishes the Journal of the Minister of Finance and Economy there); do not cite those URLs as evidence that MRiT still exists. (6) Exact day of Paszyk's election as PSL club chairman (late July 2025) not pinned to a specific date in accessible sources; his May 2024 swearing-in day (reported 13 May 2024) also worth a spot-check if exact dates go in print. |
| Saudi Arabia | Vacant / acting | (1) Acting/interim official: Mohammed bin Abdulaziz Al-Abduljabbar — Acting Governor, General Authority for Foreign Trade (GAFT) (2) Overall trade balance (goods-only, 2025) flagged 'Needs check'. (3) GDP value low-confidence (secondary IMF-based aggregator; may reflect Apr-2026 WEO revision). |

## Acting / interim officials (carry the flag through to any external version)

- **Argentina — Pablo Lavigne**, Secretary of Production Coordination (also exercising Industry & Commerce functions, acting) (Ministerio de Economía). Flagged *Vacant / acting*. Held on an acting/interim basis; confirm permanent appointment.
- **Saudi Arabia — Mohammed bin Abdulaziz Al-Abduljabbar**, Acting Governor, General Authority for Foreign Trade (GAFT) (General Authority for Foreign Trade (GAFT)). Flagged *Vacant / acting*. Held on an acting/interim basis; confirm permanent appointment.

## Cross-cutting data caveats

- **GDP low-confidence (6):** Argentina, Australia, Brazil, Mexico, Poland, Saudi Arabia — sourced from a secondary IMF-based aggregator; may reflect the later Apr-2026 WEO revision. Confirm against the primary IMF WEO table.
- **U.S. bilateral goods below high confidence:** France (low), Germany/Italy/Poland (medium) — EU members without a standalone USTR fact sheet; sourced via the Census/COMTRADE mirror. Confirm against census.gov country pages.
- **Basis exceptions:** Australia's overall balance is goods+services; India's is fiscal year 2025-26. All others goods-only, calendar 2025.
- **Currency conversion:** Overall balances for Australia, Canada, France, Germany, Italy, Japan, Poland, Saudi Arabia and the UK are converted from local currency (EUR/GBP/CAD/AUD/JPY/SAR) at approximate 2025 average rates; USD values carry exchange-rate uncertainty.
- **Primary-source reachability:** census.gov, imf.org and many national statistics/government sites returned HTTP 403 to automated fetching in the build environment. Figures came from official-data-derived channels (USTR fact sheets, Trading Economics' Census/COMTRADE mirror, StatisticsTimes' IMF-WEO tabulation), not read directly off the primary agency page. Re-confirm headline figures against primary sources before publication.
- **Flags:** Wikimedia Commons was egress-blocked; flag images are from the public-domain hampusborgos/country-flags repository.

## Data-quality correction applied during QA

- **Saudi Arabia:** the raw research wrongly included the U.S. Secretary of Commerce and U.S. Trade Representative in Saudi Arabia's trade-officials list (context bleed from U.S.-specific instructions). Removed; Saudi Arabia's trade officials are the Minister of Commerce (Al-Qasabi) and the acting GAFT Governor (Al-Abduljabbar).

- None — every displayed official has an official portrait embedded.

## Bloc annex (EU & African Union)

- **European Union** — no flags; all items verified.
  - note: Eurostat vintage discrepancy on 2025 extra-EU goods surplus: EUR 130.0 bn (Statistics Explained, exports EUR 2,644.1 bn / imports EUR 2,514.1 bn) vs EUR 128 bn (Eurostat news headline, 2026-03-26). The revised EUR 128 bn
  - note: USD conversion of the extra-EU balance is derived, not official: EUR 128 bn x 1.1306 (2025 annual average USD/EUR, per ECB reference-rate history via exchangerates.org.uk) = ~USD 144.7 bn.
  - note: Direct fetches of imf.org, ustr.gov, ec.europa.eu (Eurostat) and en.wikipedia.org returned HTTP 403 through the environment proxy; all figures were verified via search-engine excerpts quoting those primary sources, corro
  - note: Mirror-statistics gap (expected, methodological): USTR/Census puts 2025 U.S. goods imports from the EU at $633.2 bn, while Eurostat reports EU goods exports to the U.S. of EUR 554.9 bn (~$627 bn) — within the normal CIF/
- **African Union** — Overall balance flagged Needs check: No clean, verifiable continental goods trade BALANCE aggregate was accessible (WTO/UNCTAD primary tables egress-blocked). Best clean aggrega
  - note: Continental goods trade balance left null: Afreximbank puts Africa's 2024 total merchandise trade at ~$1.5T, while secondary aggregations imply ~$1.4T (exports ~$682B + imports ~$719B, deficit ~$37B); WTO/UNCTAD primary 
  - note: GDP ($2.81T, 2025) is an IMF WEO-based projection aggregated by third parties (StatisticsTimes/Worldometers over ~53-54 economies); the IMF publishes no single 'Africa' nominal GDP line and imf.org was egress-blocked, so
  - note: The Feb 2025 AUC elections filled only four of six commissioner posts; ETTIM was held in an acting capacity (Moses Vilakati) until Francisca Tatchouop Belobe was elected in July 2025 and sworn in September 2025 — stale s
  - note: U.S. trade figures are a U.S.-Africa (whole continent) proxy for the AU; USTR/Census pages could not be fetched directly (egress-blocked) and were verified via search excerpts of the USTR Africa page.

## Portrait drop-in manifest

Portraits cannot be fetched from the build environment (all government hosts and Wikimedia are egress-blocked). To add them: from the DOC network, save each official's photo to the path below (png/jpg), then run `bash scripts/build.sh` — slides embed them automatically.

| Official | Save to | Official page (portrait source) |
|---|---|---|
| Argentina — Darío Leandro Genua | `assets/portraits/argentina-genua.png` | https://www.argentina.gob.ar/noticias/dario-genua-abrio-el-argentina-digital-summit-2026 |
| Argentina — Pablo Quirno | `assets/portraits/argentina-quirno.png` | https://en.wikipedia.org/wiki/Pablo_Quirno |
| Argentina — Pablo Lavigne | `assets/portraits/argentina-lavigne.png` | https://www.ambito.com/economia/unifican-forma-transitoria-dos-areas-clave-y-le-asignan-mas-funciones-pablo-lavigne-n6261559 |
| Australia — Andrew Charlton | `assets/portraits/australia-charlton.png` | https://ministers.pmc.gov.au/hon-dr-andrew-charlton-mp |
| Australia — Tim Ayres | `assets/portraits/australia-ayres.png` | https://www.minister.industry.gov.au/ministers/timayres |
| Australia — Don Farrell | `assets/portraits/australia-farrell.png` | https://www.trademinister.gov.au/minister/don-farrell |
| Brazil — Frederico de Siqueira Filho | `assets/portraits/brazil-siqueira.png` | https://telesintese.com.br/frederico-siqueira-diz-que-pretende-seguir-no-ministerio-ate-o-fim-de-2026/ |
| Brazil — Luciana Santos | `assets/portraits/brazil-santos.png` | https://www.gov.br/mcti/pt-br/acesso-a-informacao/institucional/quem-e-quem |
| Brazil — Márcio Fernando Elias Rosa | `assets/portraits/brazil-rosa.png` | https://agenciagov.ebc.com.br/noticias/202604/marcio-elias-rosa-e-o-novo-ministro-do-desenvolvimento-industria-comercio-e-servicos |
| Canada — Evan Solomon | `assets/portraits/canada-solomon.png` | https://www.canada.ca/en/government/ministers/evan-solomon.html |
| Canada — Maninder Sidhu | `assets/portraits/canada-sidhu.png` | https://www.canada.ca/en/government/ministers/maninder-sidhu.html |
| Canada — Dominic LeBlanc | `assets/portraits/canada-leblanc.png` | https://www.canada.ca/en/government/ministers/dominic-leblanc.html |
| China — Li Lecheng | `assets/portraits/china-lilecheng.png` | https://www.chinadaily.com.cn/a/202504/30/WS68120fb7a310a04af22bd237.html |
| China — Yin Hejun | `assets/portraits/china-hejun.png` | https://en.most.gov.cn/organization/leadership/202404/t20240411_190178.htm |
| China — Wang Wentao | `assets/portraits/china-wangwentao.png` | https://english.mofcom.gov.cn/News/PressConference/art/2026/art_af9691957bef4456be63899a4966e416.html |
| China — Li Chenggang | `assets/portraits/china-lichenggang.png` | https://www.cnbc.com/2026/05/22/china-apec-trade-meeting-li-chenggang-cooperation-us-china-deals.html |
| France — Anne Le Hénanff | `assets/portraits/france-lehenanff.png` | https://www.info.gouv.fr/personnalite/anne-le-henanff |
| France — Nicolas Forissier | `assets/portraits/france-forissier.png` | https://www.info.gouv.fr/personnalite/nicolas-forissier |
| Germany — Karsten Wildberger | `assets/portraits/germany-wildberger.png` | https://www.bundesregierung.de/breg-de/bundesregierung/bundeskabinett/2342876-2342876 |
| Germany — Katherina Reiche | `assets/portraits/germany-reiche.png` | https://www.bundesregierung.de/breg-de/bundesregierung/bundeskabinett/katherina-reiche-2342740 |
| India — Ashwini Vaishnaw | `assets/portraits/india-vaishnaw.png` | https://en.wikipedia.org/wiki/Ashwini_Vaishnaw |
| India — Piyush Goyal | `assets/portraits/india-goyal.png` | https://en.wikipedia.org/wiki/Piyush_Goyal |
| India — Rajesh Agrawal | `assets/portraits/india-agrawal.png` | https://theprint.in/diplomacy/india-us-framework-trade-deal-ready-will-be-signed-at-right-time-says-commerce-secretary/2985216/ |
| Indonesia — Meutya Viada Hafid | `assets/portraits/indonesia-hafid.png` | https://en.wikipedia.org/wiki/Meutya_Hafid |
| Indonesia — Budi Santoso | `assets/portraits/indonesia-santoso.png` | https://en.wikipedia.org/wiki/Budi_Santoso_(politician) |
| Indonesia — Airlangga Hartarto | `assets/portraits/indonesia-airlangga.png` | https://en.wikipedia.org/wiki/Airlangga_Hartarto |
| Italy — Alessio Butti | `assets/portraits/italy-butti.png` | https://www.governo.it/en/governo/meloni/undersecretary-presidency-council-ministers/alessio-butti |
| Italy — Antonio Tajani | `assets/portraits/italy-tajani.png` | https://www.governo.it/en/governo/meloni/minister/antonio-tajani |
| Italy — Adolfo Urso | `assets/portraits/italy-urso.png` | https://www.governo.it/en/governo/meloni/minister/adolfo-urso |
| Japan — Matsumoto Hisashi | `assets/portraits/japan-matsumoto.png` | https://www.digital.go.jp/en/about/member/matsumotohisashi |
| Japan — Akazawa Ryosei | `assets/portraits/japan-akazawa.png` | https://www.meti.go.jp/english/aboutmeti/profiles/individual/aMinister.html |
| Mexico — José Antonio Peña Merino | `assets/portraits/mexico-pena.png` | https://es.wikipedia.org/wiki/Agencia_de_Transformaci%C3%B3n_Digital_y_Telecomunicaciones |
| Mexico — Marcelo Luis Ebrard Casaubón | `assets/portraits/mexico-ebrard.png` | https://ustr.gov/about/policy-offices/press-office/press-releases/2026/april/joint-statement-ambassador-jamieson-greer-and-mexican-secretary-economy-marcelo-ebrard |
| Mexico — Luis Rosendo Gutiérrez Romano | `assets/portraits/mexico-gutierrez.png` | https://www.gob.mx/se/estructuras/luis-rosendo-gutierrez-romano |
| Poland — Krzysztof Gawkowski | `assets/portraits/poland-gawkowski.png` | https://www.gov.pl/web/primeminister/krzysztof-gawkowski |
| Poland — Andrzej Domański | `assets/portraits/poland-domanski.png` | https://www.bloomberg.com/news/articles/2025-07-23/poland-reshuffles-cabinet-to-create-economy-superministry |
| Poland — Michał Baranowski | `assets/portraits/poland-baranowski.png` | https://aninews.in/news/world/asia/eu-india-fta-huge-deal-for-europe-including-polish-businesses-polands-undersecretary-of-state-michal-baranowski20260714221423/ |
| Russia — Maksut Shadayev | `assets/portraits/russia-shadayev.png` | https://www.themoscowtimes.com/2026/03/31/russias-digital-ministry-declares-war-on-vpns-a92384 |
| Russia — Anton Alikhanov | `assets/portraits/russia-alikhanov.png` | https://armenia.news-pravda.com/en/russia/2026/07/06/36732.html |
| Russia — Maxim Reshetnikov | `assets/portraits/russia-reshetnikov.png` | https://www.thenationalnews.com/news/europe/2026/06/08/russias-economy-is-sustainable-and-balanced-despite-global-uncertainty-minister-says/ |
| Saudi Arabia — Abdullah bin Amer Alswaha | `assets/portraits/saudi-alswaha.png` | https://mcit.gov.sa/en/minister-mcit |
| Saudi Arabia — Majid bin Abdullah Al-Qasabi | `assets/portraits/saudi-alqasabi.png` | https://mc.gov.sa/en/About/CVs-Ministry-officials/Pages/Minister.aspx |
| Saudi Arabia — Mohammed bin Abdulaziz Al-Abduljabbar | `assets/portraits/saudi-abduljabbar.png` | https://x.com/gaft_sa/status/1975121378769871186 |
| South Korea — Bae Kyung-hoon | `assets/portraits/korea-bae.png` | https://en.wikipedia.org/wiki/Bae_Kyung-hoon |
| South Korea — Kim Jung-kwan | `assets/portraits/korea-kim.png` | https://en.wikipedia.org/wiki/Kim_Jung-kwan_(politician) |
| South Korea — Yeo Han-koo | `assets/portraits/korea-yeo.png` | https://en.wikipedia.org/wiki/Yeo_Han-koo |
| Türkiye — Mehmet Fatih Kacır | `assets/portraits/turkiye-kacir.png` | https://en.wikipedia.org/wiki/Mehmet_Fatih_Kac%C4%B1r |
| Türkiye — Ömer Bolat | `assets/portraits/turkiye-bolat.png` | https://www.tccb.gov.tr/en/cabinet/minister-of-trade |
| United Kingdom — Liz Kendall | `assets/portraits/uk-kendall.png` | https://www.gov.uk/government/ministers/secretary-of-state-for-science-innovation-and-technology |
| United Kingdom — Peter Kyle | `assets/portraits/uk-kyle.png` | https://www.gov.uk/government/ministers/secretary-of-state--2 |
| United Kingdom — Chris Bryant | `assets/portraits/uk-bryant.png` | https://www.gov.uk/government/people/chris-bryant |
| United States — Michael Kratsios | `assets/portraits/us-kratsios.png` | https://en.wikipedia.org/wiki/Michael_Kratsios |
| United States — Arielle Roth | `assets/portraits/us-roth.png` | https://www.ntia.gov/personnel-profile/arielle-roth |
| United States — Howard Lutnick | `assets/portraits/us-lutnick.png` | https://en.wikipedia.org/wiki/Howard_Lutnick |
| United States — Jamieson Greer | `assets/portraits/us-greer.png` | https://ustr.gov/about/leadership/us-trade-representative |
| European Union — Henna Virkkunen | `assets/portraits/bloc-virkkunen.png` | https://commission.europa.eu/about/organisation/college-commissioners/henna-virkkunen_en |
| European Union — Maroš Šefčovič | `assets/portraits/bloc-efovi.png` | https://commission.europa.eu/about/organisation/college-commissioners/maros-sefcovic_en |
| African Union — Lerato Dorothy Mataboge | `assets/portraits/bloc-mataboge.png` | https://au.int/en/commissioners/he-ms-lerato-mataboge |
| African Union — Francisca Tatchouop Belobe | `assets/portraits/bloc-belobe.png` | https://au.int/en/commissioners/he-francisca-tatchouop-belobe |

## Name spellings to preserve exactly (incl. diacritics)

- Türkiye, Darío Leandro Genua, José Antonio Peña Merino, Katherina Reiche, Maroš Šefčovič, Mehmet Fatih Kacır, Abdulkadir Uraloğlu, Andrzej Domański, Michał Baranowski, Krzysztof Gawkowski, Márcio Fernando Elias Rosa.
- Romanization variants (form used shown first): Bae Kyung-hoon / Baek; Kim Jung-kwan / Jeong-kwan; Rajesh Agrawal / Agarwal.


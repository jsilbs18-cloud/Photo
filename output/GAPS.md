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

## Portraits pending (monogram placeholder shown on the slide)

- **Argentina** — Darío Leandro Genua (Secretary of Innovation, Science and Technology): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **Argentina** — Pablo Quirno (Minister of Foreign Affairs, International Trade and Worship (Canciller)): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **Argentina** — Pablo Lavigne (Secretary of Production Coordination (also exercising Industry & Commerce functions, acting)): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **Australia** — Andrew Charlton (Cabinet Secretary; Assistant Minister for Science, Technology and the Digital Economy): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **Australia** — Tim Ayres (Minister for Industry and Innovation; Minister for Science): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **Australia** — Don Farrell (Minister for Trade and Tourism; Special Minister of State): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **Brazil** — Frederico de Siqueira Filho (Minister of Communications): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **Brazil** — Luciana Santos (Minister of Science, Technology and Innovation): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **Brazil** — Márcio Fernando Elias Rosa (Minister of Development, Industry, Trade and Services): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **Brazil** — Lucas Pedreira do Couto Ferraz (Secretary of Foreign Trade (SECEX)): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **Canada** — Evan Solomon (Minister of Artificial Intelligence and Digital Innovation): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **Canada** — Maninder Sidhu (Minister of International Trade): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **Canada** — Dominic LeBlanc (President of the King's Privy Council for Canada and Minister responsible for Canada-U.S. Trade, Intergovernmental Affairs, Internal Trade and One Canadian Economy): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **China** — Li Lecheng (Minister of Industry and Information Technology): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **China** — Yin Hejun (Minister of Science and Technology): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **China** — Wang Wentao (Minister of Commerce): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **China** — Li Chenggang (China International Trade Representative (full ministerial rank) and Vice Minister of Commerce): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **France** — Anne Le Hénanff (Minister Delegate for Artificial Intelligence and Digital Affairs): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **France** — Nicolas Forissier (Minister Delegate for Foreign Trade and Attractiveness): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **Germany** — Karsten Wildberger (Federal Minister for Digital Transformation and Government Modernisation): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **Germany** — Katherina Reiche (Federal Minister for Economic Affairs and Energy): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **India** — Ashwini Vaishnaw (Union Minister of Electronics and Information Technology (concurrently Minister of Railways and Minister of Information & Broadcasting)): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **India** — Piyush Goyal (Union Minister of Commerce and Industry): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **India** — Rajesh Agrawal (Commerce Secretary (Secretary, Department of Commerce) and India's Chief Negotiator for the India-US Bilateral Trade Agreement): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **Indonesia** — Meutya Viada Hafid (Minister of Communication and Digital Affairs): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **Indonesia** — Budi Santoso (Minister of Trade): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **Indonesia** — Airlangga Hartarto (Coordinating Minister for Economic Affairs): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **Italy** — Alessio Butti (Undersecretary of State to the Presidency of the Council of Ministers with responsibility for Technological Innovation): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **Italy** — Antonio Tajani (Deputy Prime Minister (Vice President of the Council of Ministers) and Minister of Foreign Affairs and International Cooperation): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **Italy** — Adolfo Urso (Minister of Enterprises and Made in Italy): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **Japan** — Matsumoto Hisashi (Minister for Digital Transformation): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **Japan** — Akazawa Ryosei (Minister of Economy, Trade and Industry): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **Mexico** — José Antonio Peña Merino (Head of the Agency for Digital Transformation and Telecommunications): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **Mexico** — Marcelo Luis Ebrard Casaubón (Secretary of Economy): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **Mexico** — Luis Rosendo Gutiérrez Romano (Undersecretary for Foreign Trade): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **Poland** — Krzysztof Gawkowski (Deputy Prime Minister and Minister of Digital Affairs): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **Poland** — Andrzej Domański (Minister of Finance and Economy): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **Poland** — Michał Baranowski (Undersecretary of State (deputy minister) responsible for trade): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **Russia** — Maksut Shadayev (Minister of Digital Development, Communications and Mass Media): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **Russia** — Anton Alikhanov (Minister of Industry and Trade): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **Russia** — Maxim Reshetnikov (Minister of Economic Development): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **Saudi Arabia** — Abdullah bin Amer Alswaha (Minister of Communications and Information Technology): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **Saudi Arabia** — Majid bin Abdullah Al-Qasabi (Minister of Commerce): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **Saudi Arabia** — Mohammed bin Abdulaziz Al-Abduljabbar (Acting Governor, General Authority for Foreign Trade (GAFT)): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **South Korea** — Bae Kyung-hoon (Deputy Prime Minister and Minister of Science and ICT): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **South Korea** — Kim Jung-kwan (Minister of Trade, Industry and Resources): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **South Korea** — Yeo Han-koo (Minister for Trade (Head of the Office of Trade Negotiations)): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **Türkiye** — Mehmet Fatih Kacır (Minister of Industry and Technology): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **Türkiye** — Ömer Bolat (Minister of Trade): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **United Kingdom** — Liz Kendall (Secretary of State for Science, Innovation and Technology): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **United Kingdom** — Peter Kyle (Secretary of State for Business and Trade, and President of the Board of Trade): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **United Kingdom** — Chris Bryant (Minister of State (Minister for Trade Policy and Economic Security)): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **United States** — Michael Kratsios (Director of the Office of Science and Technology Policy (OSTP) and Assistant to the President for Science and Technology): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **United States** — Arielle Roth (Assistant Secretary of Commerce for Communications and Information and Administrator, National Telecommunications and Information Administration (NTIA)): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **United States** — Howard Lutnick (United States Secretary of Commerce): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.
- **United States** — Jamieson Greer (United States Trade Representative (USTR), with rank of Ambassador): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.

## Name spellings to preserve exactly (incl. diacritics)

- Türkiye, Darío Leandro Genua, José Antonio Peña Merino, Katherina Reiche, Maroš Šefčovič, Mehmet Fatih Kacır, Abdulkadir Uraloğlu, Andrzej Domański, Michał Baranowski, Krzysztof Gawkowski, Márcio Fernando Elias Rosa.
- Romanization variants (form used shown first): Bae Kyung-hoon / Baek; Kim Jung-kwan / Jeong-kwan; Rajesh Agrawal / Agarwal.


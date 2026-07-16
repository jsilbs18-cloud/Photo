# GAPS & Uncertainty Register — G20 Ministers & Trade Deck

Compiled 2026-07-16. Every item a reviewer should chase down before external use. Nothing here is a fabricated placeholder — all officeholders resolved to a named person; these are data-vintage, basis, precision, and acting-status flags. Cross-references: full sourcing in `research/g20-research.md`; structured data in `data/g20.json`.

**Roll-up:** 12 Verified · 5 Needs check · 2 Vacant/acting (of 19).

## Per-country flags

| Country | Flag | Specific gaps to verify |
|---|---|---|
| Argentina | Vacant / acting | (1) Acting/interim official: Pablo Lavigne — Secretary of Production Coordination (exercising Industry & Commerce functions) (2) GDP value low-confidence (secondary IMF-based aggregator; may reflect Apr-2026 WEO revision). |
| Australia | Needs check | (1) Overall trade balance (goods+services, 2025) flagged 'Needs check'. (2) GDP value low-confidence (secondary IMF-based aggregator; may reflect Apr-2026 WEO revision). (3) Overall balance is goods+services (not goods-only) — basis differs from other countries. |
| Brazil | Needs check | (1) GDP value low-confidence (secondary IMF-based aggregator; may reflect Apr-2026 WEO revision). |
| France | Needs check | (1) U.S. bilateral goods figures low-confidence (EU member without standalone USTR fact sheet). |
| Germany | Verified | (1) U.S. bilateral goods figures medium-confidence (EU member without standalone USTR fact sheet). |
| India | Verified | (1) Overall balance uses fiscal year FY 2025-26, not calendar 2025. |
| Italy | Verified | (1) U.S. bilateral goods figures medium-confidence (EU member without standalone USTR fact sheet). |
| Mexico | Needs check | (1) GDP value low-confidence (secondary IMF-based aggregator; may reflect Apr-2026 WEO revision). |
| Poland | Needs check | (1) GDP value low-confidence (secondary IMF-based aggregator; may reflect Apr-2026 WEO revision). (2) U.S. bilateral goods figures medium-confidence (EU member without standalone USTR fact sheet). |
| Saudi Arabia | Vacant / acting | (1) Acting/interim official: Mohammed bin Abdulaziz Al-Abduljabbar — Acting Governor, General Authority for Foreign Trade (GAFT) (2) Overall trade balance (goods-only, 2025) flagged 'Needs check'. (3) GDP value low-confidence (secondary IMF-based aggregator; may reflect Apr-2026 WEO revision). |

## Acting / interim officials (carry the flag through to any external version)

- **Argentina — Pablo Lavigne**, Secretary of Production Coordination (exercising Industry & Commerce functions) (Ministry of Economy). Flagged *Vacant / acting*. Held on an acting/interim basis; confirm permanent appointment.
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

## Name spellings to preserve exactly (incl. diacritics)

- Türkiye, Darío Leandro Genua, José Antonio Peña Merino, Katherina Reiche, Maroš Šefčovič, Mehmet Fatih Kacır, Abdulkadir Uraloğlu, Andrzej Domański, Michał Baranowski, Krzysztof Gawkowski, Márcio Fernando Elias Rosa.
- Romanization variants (form used shown first): Bae Kyung-hoon / Baek; Kim Jung-kwan / Jeong-kwan; Rajesh Agrawal / Agarwal.


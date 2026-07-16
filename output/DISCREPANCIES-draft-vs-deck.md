# Draft `G20_Minister_List.docx` vs. deck data — discrepancy log

Compared 2026-07-16. Per instruction, **the deck's figures win everywhere** (they are 2025-vintage,
single-source, and QA-verified); the new ITA-format list is generated from the same `data/g20.json`
as the deck. Items below are what changed relative to your draft, so you can trace every difference.

## 1. Systematic difference: balance vintages
The draft's overall trade balances are **2024** figures; the deck (and the new list) use **2025 full year**.
Every country's overall balance therefore differs. Largest gaps:

| Country | Draft (2024) | Deck/list (2025) |
|---|---|---|
| Mexico | −$26.9B deficit | **+$0.8B surplus** (sign flip — 2025 was a record-export year) |
| Poland | +$0.75B surplus | **−$8.7B deficit** (sign flip) |
| Australia | +$44.5B "merchandise" | **+$4.5B goods+services** (2025; basis differs — flagged in caveats) |
| China | +$991.7B | **+$1,190.0B** |
| South Korea | +$51.8B | **+$78.0B** |
| India | −$275.5B | **−$333.2B** (FY 2025-26) |
| Japan | −$36.5B | **−$17.0B** |
| France | −$111.3B | **−$76.1B** |
| Germany | +$260B | **+$226B** |
| Saudi Arabia | +$72.7B | **+$59.9B** (derived; flagged Needs check) |
| Argentina | +$18.9B | **+$11.3B** |
| Brazil | +$59.1B | **+$68.3B** |
| Indonesia | +$31B | **+$41.1B** |
| Türkiye | −$82.2B | **−$92B** |
| UK | −$303.3B | **−$319.2B** |
| Russia | +$133B | **+$139.3B** |
| Canada | −$5B | **−$22.4B** |
| U.S. | −$1.29T (2024) | **−$1,240.9B (2025)** |

## 2. U.S. bilateral figures that differ (deck values kept)
- **France**: draft $50.6B / $68.1B / −$17.5B → deck **$44.4B / $61.1B / −$16.7B** (largest bilateral gap; draft may use a different year or basis)
- **Italy**: draft $43.1B / $74.4B / −$31.4B → deck **$43.7B / $78.7B / −$35.0B**
- **Germany**: imports $155.8B → **$159.0B**; balance −$73B → **−$76.3B**
- **Japan**: $81.4B / $145.8B / −$64.4B → **$82.1B / $146.0B / −$63.9B**
- **South Korea**: $69.1B / $125.5B / −$56.5B → **$68.8B / $125.2B / −$56.4B**
- **Mexico**: $337.3B / $534.3B / −$197B → **$338.0B / $534.9B / −$196.9B**
- **Poland**: draft exports $14.3B / imports $14.1B (which would be a U.S. *surplus*, though the draft labels
  it a deficit) → deck **$14.1B / $14.5B / −$0.4B deficit**
- Minor roundings: Argentina exports $10B→$9.9B; India $45.4B→$45.6B; Indonesia $10.8B/$34.6B→$11.0B/$34.7B;
  UK exports $97.4B→$97.0B; China $106B/$308.7B→$106.3B/$308.4B; Brazil bilateral $14.4B→$14.5B; Australia
  imports $29B→$29.1B, bilateral $4.7B→$4.6B; Canada intro figures ($333.6B/$381.9B/−$48.3B) disagreed with
  the draft's own bullets — the bullets matched the deck and were kept.

## 3. Internal errors in the draft (corrected in the list)
- **Saudi Arabia**: $14.1B exports vs $10.5B imports is a U.S. **surplus** of $3.6B; the draft calls it a deficit.
- **Poland**: labeled a U.S. "deficit of $251 million" while its own export/import figures imply a surplus;
  deck figures show a −$0.4B deficit.
- **China section**: contains a copy-pasted block of Canada bullets (and a truncated "U.S." bullet).
- **Brazil**: intro says GDP $2.28T, bullets say $2.26T (deck: $2,280.0B). **Canada**: intro $2.32T vs bullets
  $2.28T (deck: $2,284.0B). **Brazil and Italy** both show "+$59.1B" balances — likely a copy artifact.
- "Canda" typo; **United States: Jamieson Greer's entry is empty** (completed in the list).

## 4. GDP differences (deck values kept)
India $3.96T → **$4,125.0B**; Japan $4.44T → **$4,280.0B**; UK $4T → **$3,959.0B**; China $19.5T →
**$19,399.0B**; Germany $5.05T → **$5,014.0B**; US $30.77T → **$30,620.0B**; Russia $2.56T → **$2,541.0B**;
Argentina $683.1B → **$681.5B**; Korea $1.87T → **$1,859.0B**; Türkiye $1.6T → **$1,565.0B**.

## 5. Names / titles corrected to verified officialdom
- Lavigne: draft "Secretary of Production **Coordinating**" → **Coordination** (+ acting marker restored)
- Baranowski: draft "**Michael**" → **Michał**; Domański: "Poland's Minister of Finance" → **Minister of
  Finance and Economy**
- LeBlanc: full official title restored (**President of the King's Privy Council for Canada and Minister
  responsible for Canada-U.S. Trade, Intergovernmental Affairs, Internal Trade and One Canadian Economy**)
- Kyle: "+ **President of the Board of Trade**" restored
- Forissier: draft "Foreign Trade and **Economic** Attractiveness" → **Foreign Trade and Attractiveness**
- Butti: exact title restored (**Undersecretary of State to the Presidency of the Council of Ministers with
  responsibility for Technological Innovation**)
- Ayres: draft "Minister for Industry and Innovation, Science" → **Minister for Industry and Innovation;
  Minister for Science** (two titles held concurrently)
- Japan names kept in Japanese order per the deck (**Akazawa Ryosei**, **Matsumoto Hisashi**); draft used
  Western order — style choice, flag if you prefer Western order
- Heading "Turkey" → **Türkiye**; acting flags restored (Lavigne; Saudi GAFT governor)
- Draft's EU entry was a placeholder note ("we are sending in the Exec. VP…, Henna Virkkunen") — the list
  now carries the full verified EU profile (Virkkunen + Šefčovič) and an African Union profile.

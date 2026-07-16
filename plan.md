# Build Plan — G20 Ministers & Trade Data Deck

**Status:** _Awaiting your approval before I write any build code._
**Date:** 2026-07-16 · **Branch:** `claude/g20-ministers-trade-deck-u00bnw`

---

## 0. What changed before this plan (read first)

Your prompt named `research/g20-research.md` as the primary input, but **no such file existed** in the repo (this is the iOS PhotoApp repo). You chose **"Research it live, cited"**, so I built the research from scratch via live web search on 2026-07-16, with an **independent adversarial verification pass** on every officeholder (each verifier re-searched to *refute* the draft — catching reshuffles since my Jan-2026 cutoff, misspellings, and paraphrased titles).

- The full cited record is now at **`research/g20-research.md`** (970 lines, every figure and minister with a source URL, as-of date, and confidence).
- Machine-readable source: `data/_research.json` (raw workflow output; I will normalize it into `data/g20.json` after you approve).
- **40 research agents, 0 errors, ~1.7M tokens.** Everything traces to a live source; nothing is filled from model memory.

> If you would rather drop in your own vetted research file, say so now and I'll re-extract from it instead — this is the moment to swap the input.

---

## 1. Data model — `data/g20.json` (single source of truth)

Both deliverables generate from this one file so they cannot drift. QA asserts workbook == deck == JSON.

```jsonc
{
  "meta": {
    "compiled": "2026-07-16",
    "scope_note": "19 G20 sovereign members; Poland substituted for South Africa; EU & AU bloc seats excluded.",
    "gdp":      { "source": "IMF WEO Oct 2025 (via StatisticsTimes tabulation)", "reference_year": "2025", "as_of": "2026-07-16", "url": "..." },
    "us_trade": { "source": "U.S. Census Bureau goods trade (via USTR fact sheets / Census-COMTRADE mirror)", "reference_year": "2025", "basis": "goods only", "as_of": "2026-07-16", "url": "..." }
  },
  "countries": [
    {
      "country": "Argentina",
      "flag_file": "assets/flags/argentina.png",

      "gdp_usd_b": 681.5, "gdp_year": "2025", "gdp_confidence": "low",

      "overall_balance_usd_b": 11.3, "overall_balance_basis": "goods-only",
      "overall_balance_year": "2025", "overall_balance_confidence": "Verified",

      "us_exports_usd_b": 9.9, "us_imports_usd_b": 8.3,
      "us_bilateral_usd_b": 1.6,           // = exports - imports; asserted in QA
      "us_trade_year": "2025", "us_trade_confidence": "high",

      "digital_ministers": [
        { "name": "Darío Leandro Genua", "title": "Secretary of Innovation, Science and Technology",
          "ministry": "Chief of Cabinet Office (Jefatura de Gabinete de Ministros)",
          "assumed_office": "2024-06-06", "bio": "…60–100 words…",
          "source_url": "...", "as_of": "2026-07-16", "confidence": "Verified",
          "is_acting": false, "role_label": "…", "is_primary": true }
      ],
      "trade_ministers": [ /* Lavigne (acting, primary), Brun (external trade) */ ],

      "row_confidence": "Vacant / acting",     // roll-up, rule in §4
      "split_note_digital": "",                // one-liner when a portfolio is split
      "split_note_trade": "Domestic commerce/industry (Lavigne, acting) sits under the Economy Ministry; external trade negotiation (Brun) under the Foreign Ministry.",
      "source_notes": "…secondary officials, caveats…",
      "gaps": [ "GDP figure low-confidence (secondary aggregator)", "Commerce secretariat vacant; Lavigne acting" ]
    }
    /* … 18 more … */
  ]
}
```

**United States row:** `gdp_usd_b` and `overall_balance_usd_b` populated; `us_exports_usd_b`, `us_imports_usd_b`, `us_bilateral_usd_b` = `null` → rendered **N/A** (per spec).

---

## 2. Per-country field inventory & confidence roll-up

All 19 have: GDP, overall balance, U.S. bilateral (exc. U.S. itself), ≥1 digital minister, ≥1 trade minister — **no missing officeholders**. `D`/`T` = count of digital/trade officials captured (extras shown on the deck as split-portfolio, listed in workbook Source notes).

| Country | D | T | Row flag | Why flagged |
|---|:-:|:-:|---|---|
| Argentina | 1 | 2 | **Vacant / acting** | Commerce secretariat vacant → Lavigne acting; GDP low-conf |
| Australia | 2 | 1 | **Needs check** | Overall balance is goods+**services** & currency-converted; GDP low-conf |
| Brazil | 2 | 2 | **Needs check** | GDP low-conf (secondary aggregator) |
| Canada | 1 | 2 | Verified | — |
| China | 1 | 2 | Verified | — |
| France | 1 | 1 | **Needs check** | U.S. bilateral goods figure low-conf (EU member, no USTR fact sheet) |
| Germany | 1 | 2 | Verified | (U.S.-trade medium-conf — noted, not downgraded) |
| India | 2 | 2 | Verified | (balance is FY 2025-26, Apr–Mar — noted) |
| Indonesia | 1 | 2 | Verified | — |
| Italy | 1 | 2 | Verified | (U.S.-trade medium-conf — noted) |
| Japan | 1 | 2 | Verified | — |
| Mexico | 1 | 2 | **Needs check** | GDP low-conf |
| Poland | 1 | 2 | **Needs check** | GDP low-conf; U.S.-trade medium-conf |
| Russia | 1 | 2 | Verified | — |
| Saudi Arabia | 1 | 2 | **Vacant / acting** | GAFT governor acting; balance derived/Needs-check; GDP low-conf |
| South Korea | 1 | 2 | Verified | (romanization variants noted) |
| Türkiye | 3 | 1 | Verified | (digital portfolio split 3 ways — see §5) |
| United Kingdom | 3 | 2 | Verified | — |
| United States | 2 | 2 | Verified | (no cabinet digital minister; trade split Commerce+USTR) |

**Roll-up: 12 Verified · 5 Needs check · 2 Vacant/acting.**

---

## 3. Gaps & uncertainty register → `output/GAPS.md`

Every item below is carried into the workbook `Confidence flag`, `Source notes`, `GAPS.md`, and the deck caveats slide. **None are invented placeholders** — all officeholders resolved to a named person; the gaps are data-vintage/precision issues, not missing names.

**A. Acting / vacant officials**
- **Argentina** — Pablo Lavigne exercises the (vacant) Industry & Commerce secretariat functions on an *acting* basis (Decree 215/2026, transitional).
- **Saudi Arabia** — Mohammed Al-Abduljabbar is *Acting* Governor of GAFT; no permanent governor confirmed; assumed-office date not published.

**B. Trade-balance figures flagged _Needs check_**
- **Australia** — figure is **goods+services** (A$6.9b), not goods-only; USD value is a currency conversion (~0.645 AUD/USD). No clean CY2025 goods-only annual figure retrieved.
- **Saudi Arabia** — 2025 goods surplus is **derived** by summing GASTAT quarterly surpluses (Q1/Q2 approximate); no single official annual figure retrieved.

**C. GDP values low-confidence** (secondary IMF-based aggregator, may reflect Apr-2026 WEO revision): **Argentina, Australia, Brazil, Mexico, Poland, Saudi Arabia.** (U.S. = medium.)

**D. U.S. bilateral goods figures below high confidence** (EU members without a standalone USTR fact sheet; sourced via Census/COMTRADE mirror): **France (low), Germany (medium), Italy (medium), Poland (medium).**

**E. Reference-basis exceptions** (must be labeled on-slide): **Australia** = goods+services; **India** = fiscal year 2025-26 (Apr–Mar); all others = goods-only, calendar 2025.

**F. Currency-conversion caveat** (many overall balances converted from EUR/GBP/CAD/AUD/JPY/SAR at approx. 2025 average rates): Australia, Canada, France, Germany, Italy, Japan, Poland, Saudi Arabia, UK. Local-currency originals kept in Source notes.

**G. Primary-source reachability** — `census.gov`, `imf.org`, and many national sites returned HTTP 403 to automated fetching; figures came from official-data-derived channels (USTR fact sheets, Trading Economics' Census/COMTRADE mirror, StatisticsTimes' IMF-WEO tabulation). Faithful to the underlying agencies but not read off the primary page.

**H. Data-quality correction already applied** — Saudi Arabia's raw trade-officials list wrongly contained the **U.S.** Commerce Secretary (Lutnick) and USTR (Greer), leaked from the U.S. record. Removed; Saudi's correct officials are Al-Qasabi (Commerce) and Al-Abduljabbar (GAFT, acting).

**I. Name spellings to preserve exactly** — Türkiye, Darío, Peña, Katherina Reiche, Šefčovič, Kacır, Uraloğlu, Domański, Baranowski, Gawkowski; Bae Kyung-hoon (var. Baek), Kim Jung-kwan (var. Jeong-kwan), Rajesh Agrawal (var. Agarwal).

---

## 4. Design decisions I need you to confirm

These are judgment calls where the research is solid but the *presentation* needs a choice. My default in **bold**; tell me if you disagree.

1. **Confidence roll-up rule (per row):** `Vacant/acting` if any official is acting → else `Needs check` if any minister, or the overall-balance, or the GDP (low) or U.S.-trade (low) figure is uncertain → else `Verified`. *Medium* GDP/U.S.-trade confidence is **noted but not** downgraded (else nearly every EU row flags). **Default: as stated.**

2. **Which official goes in the workbook's single minister columns** (deck shows all): primary = the lead cabinet-level minister. Two genuinely ambiguous picks:
   - **Türkiye digital** — no standalone digital ministry; three officials split it (Cybersecurity Presidency / Industry & Technology / Transport & Infrastructure). **Default primary: Mehmet Fatih Kacır, Minister of Industry and Technology** (closest "technology minister"), with a split-note listing the other two.
   - **Argentina trade** — **Default primary: Pablo Lavigne (acting domestic commerce)**, with Fernando Brun (external-trade negotiator) as the split counterpart. Alternative: make Brun primary since he owns external trade.
   - **Brazil digital** — Communications (Siqueira Filho) vs Science/Tech/Innovation (Santos). **Default primary: Frederico de Siqueira Filho (Communications)**; Santos shown as the science/tech counterpart.

3. **Split portfolios on country slides** — show up to **two** officials prominently with a one-line division-of-responsibility note. Where a portfolio splits **three** ways (Türkiye digital, UK digital), show the primary + a one-line note naming the junior/other ministers rather than three full bios (keeps the layout identical across all 19). **Default: as stated.**

4. **GDP reference year = 2025, U.S. trade year = 2025** for all rows (single consistent vintage). Header labels state the year and the goods-only basis. **Default: as stated.**

---

## 5. Deliverable 1 — workbook `output/g20-ministers-trade-reference.xlsx`

One row per country, 16 columns, alphabetical, `openpyxl`:

`Country` · `GDP (USD bn, nominal — 2025)` · `GDP reference year` · `Overall trade balance (USD bn; goods-only exc. Australia g+s)` · `U.S. goods exports to (USD bn)` · `U.S. goods imports from (USD bn)` · `U.S. bilateral balance (USD bn; − = U.S. deficit)` · `Trade data reference year` · `Digital/technology minister` · `Digital minister title` · `Digital minister ministry` · `Trade/commerce minister` · `Trade minister title` · `Trade minister ministry` · `Confidence flag` · `Source notes`

- Freeze header row; autofit columns; USD figures formatted `$#,##0.0` (billions, 1 decimal).
- **Conditional formatting** on U.S. bilateral balance: red fill = U.S. deficit (negative), green = U.S. surplus (positive).
- U.S. row: GDP + overall balance filled; three bilateral cells = `N/A`.
- Split portfolios: primary in the minister columns; secondary official(s) named in `Source notes`.

## 6. Deliverable 2 — deck `output/g20-ministers-trade-deck.pptx`

16:9, `python-pptx`, government-brief aesthetic (navy/slate + one accent + neutrals; no gradients/clip-art). Slides:

1. **Title** — title, "Prepared for International Trade Administration," date, data-vintage line ("Trade data: 2025 full year, goods basis, unless noted").
2. **Methodology / scope** — 19 countries, Poland-for-South-Africa, EU/AU excluded, sources + vintages + as-of, the 403/conversion caveats in brief.
3. **Summary table** — all 19: country, GDP, U.S. exports to, U.S. imports from, U.S. bilateral balance; right-aligned numbers; **split across 2 slides** (10 + 9) so it breathes; deficit/surplus color-coded.
4. **19 country slides** — identical master layout, elements pinned to the same coordinates:
   - Flag (uniform height) + country name, top-left.
   - Trade block: GDP, overall balance, U.S. exports/imports/bilateral — each labeled with its reference year.
   - Digital minister: name, exact title, ministry, assumed-office, 60–100w bio.
   - Trade minister: same. Split portfolios → both + one-line division note.
   - Small source/as-of footer + a `Needs check` / `Acting` badge where flagged.
5. **Sources & caveats** — datasets + vintages, the low-confidence/needs-check register, acting officials, currency-conversion & 403 sourcing notes, and the Poland-for-SA + EU/AU footnote.

- **Type scale fixed across all 19** country slides; body ≥ 11pt. Bios must fit the box **without shrinking type** — I tighten copy if any overflow, and QA measures rendered text height to prove no overflow.

## 7. Flags
Download Wikimedia Commons PNG renderings to `assets/flags/`, normalize to a uniform display height, embed. Failed download → labeled placeholder rectangle + logged (never silently skipped).

## 8. QA (run before I report done)
Programmatic asserts against `data/g20.json`: exactly 19 country slides; South Africa absent / Poland present; every dollar figure carries a year; **`us_bilateral == us_exports − us_imports`** on every slide; **workbook == deck == JSON** for all 19; no text box overflow (measured); every flag embedded & undistorted; minister names/ministries char-for-char vs research incl. diacritics; titles exact (not paraphrased); `GAPS.md` non-empty. I'll report results + anything internally inconsistent in the sources.

---

### ▶ Approve this plan (or adjust §4) and I'll build `data/g20.json` → workbook + deck → QA.

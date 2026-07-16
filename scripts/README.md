# Build pipeline — G20 Ministers & Trade deliverables

All deliverables are generated from **one source of truth**, `data/g20.json`, so the
workbook and the deck cannot drift. `scripts/qa.py` asserts that programmatically.

## Data lineage

```
(live web research, 2026-07-16, dual-verified)
        │
        ▼
data/_research.json          # raw structured research output (per-country, cited)
        │  scripts/build_json.py   (normalize: primary-minister selection, roll-up,
        ▼                           bilateral = exports − imports, contamination fix)
data/g20.json                # SINGLE SOURCE OF TRUTH
        ├── scripts/build_xlsx.py → output/g20-ministers-trade-reference.xlsx
        ├── scripts/build_pptx.py → output/g20-ministers-trade-deck.pptx
        ├── scripts/build_html.py → output/_deck.html → (Chromium) → output/g20-ministers-trade-deck.pdf
        └── scripts/build_gaps.py → output/GAPS.md
```

`research/g20-research.md` is the human-readable cited record (every figure and
officeholder with a source URL, as-of date, and confidence flag).

## Run

```bash
bash scripts/build.sh          # runs the whole pipeline + QA
```

Requires Python packages `openpyxl python-pptx Pillow cairosvg pymupdf` and a Chromium
binary (set `CHROME=` if not at the default Playwright path). Scripts assume the repo at
`/home/user/Photo`; adjust the `ROOT` constant in each script if cloned elsewhere.

## Notes

- **PDF via Chromium, not LibreOffice.** LibreOffice's headless converter is blocked in
  the build sandbox (exits 81), so the PDF is rendered from an HTML mirror of the deck
  (`build_html.py`) that uses the same coordinates and palette as the PPTX. PPTX and PDF
  are therefore two formats of the same deck.
- **Flags** come from the public-domain `hampusborgos/country-flags` repo (Wikimedia
  Commons was egress-blocked); rasterized to uniform 400px height, true aspect ratios.
- **QA** (`qa.py`) checks: 19 country slides, South Africa absent / Poland present,
  every figure carries a year, bilateral = exports − imports, workbook == pptx == pdf ==
  JSON for all 19, diacritics survive into every format, minister names/titles/ministries
  match the research char-for-char, flags embedded, and a font-metric text-fit measurement
  that proves no PPTX bio/box overflows.

## v2/v3 revisions (2026-07-16)

- `apply_updates.py` merges `data/_updates.json` (live-verified roster changes, US world
  totals, seal) and `data/_trim_output.json` (compressed bios) into `data/g20.json`.
- `normalize_portraits.py` crops portraits to 4:5 and generates monogram placeholders —
  drop official photos into `assets/portraits/<slug>.png` (see GAPS.md) and rerun build.sh.
- Deck styled per the **ITA Visual Style Guide (Jan 2026)**: Trade Navy #0A314D / Trade
  Blue #00558C, Trade Gold rules, Open Sans (Calibri is the approved O365 alternate),
  DOC seal white-line rendering, official document footer signatures. Fonts installed
  from Google Fonts GitHub into /usr/local/share/fonts/ita for the PDF render.

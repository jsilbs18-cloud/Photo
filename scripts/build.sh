#!/usr/bin/env bash
# Reproducible build pipeline for the G20 ministers & trade deliverables.
# Single source of truth: data/g20.json  ->  workbook + deck (pptx & pdf) + GAPS.md
# Assumes the repo at /home/user/Photo (adjust ROOT in the scripts otherwise) and
# Python packages: openpyxl, python-pptx, Pillow, cairosvg, pymupdf.
set -euo pipefail
cd "$(dirname "$0")/.."
CHROME="${CHROME:-/opt/pw-browsers/chromium-1194/chrome-linux/chrome}"

echo "1/7 flags";      python3 scripts/fetch_flags.py      # -> assets/flags/*.png (+ data/_flags_status.json)
echo "2/7 json";       python3 scripts/build_json.py       # data/_research.json -> data/g20.json
echo "     updates";    python3 scripts/apply_updates.py     # merge data/_updates.json (rosters, portraits, seal, US totals)
echo "     blocs";      python3 scripts/apply_blocs.py       # EU & AU annex from data/_bloc_*.json
echo "     portraits";  python3 scripts/normalize_portraits.py  # embeds any photos dropped into assets/portraits/
echo "3/7 workbook";   python3 scripts/build_xlsx.py       # -> output/g20-ministers-trade-reference.xlsx
echo "     list";       python3 scripts/build_docx.py       # -> output/g20-ministers-trade-list.docx (ITA format)
echo "4/7 pptx";       python3 scripts/build_pptx.py       # -> output/g20-ministers-trade-deck.pptx
echo "5/7 html";       python3 scripts/build_html.py       # -> output/_deck.html (intermediate)
echo "6/7 pdf";        "$CHROME" --headless --no-sandbox --disable-gpu --no-pdf-header-footer \
                           --print-to-pdf=output/g20-ministers-trade-deck.pdf output/_deck.html 2>/dev/null
echo "     gaps";      python3 scripts/build_gaps.py       # -> output/GAPS.md
echo "7/7 qa";         python3 scripts/qa.py               # asserts workbook == deck == pdf == json
echo "DONE."

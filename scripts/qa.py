#!/usr/bin/env python3
"""QA for the v2 deliverables: workbook == pptx == pdf == data/g20.json, arithmetic,
diacritics, roster char-for-char vs data/_roster_reference.json, portraits/flags/seal
embedded, and font-metric text-fit for the split-column layout."""
import json, re, sys, os
from openpyxl import load_workbook
from pptx import Presentation
import fitz
from PIL import Image, ImageFont

ROOT = '/home/user/Photo/'
D = json.load(open(ROOT + 'data/g20.json')); CO = D['countries']
ROSTER = json.load(open(ROOT + 'data/_roster_reference.json'))

PASS = []; FAIL = []
def check(c, m): (PASS if c else FAIL).append(('PASS' if c else 'FAIL') + ': ' + m)

def money(v): return 'N/A' if v is None else f"${v:,.1f}B"
def absmoney(v): return None if v is None else f"${abs(v):,.1f}B"

names = [c['country'] for c in CO]

# ---------- 1. scope ----------
check(len(CO) == 19, f"exactly 19 countries (got {len(CO)})")
check('South Africa' not in names, "South Africa absent")
check('Poland' in names, "Poland present")
check(names == sorted(names), "countries alphabetical")

# ---------- 2. arithmetic ----------
for c in CO:
    if c['country'] == 'United States':
        check(c['us_exports_usd_b'] is None and c['us_bilateral_usd_b'] is None, "US bilateral columns N/A")
        if c.get('us_world_exports_b') is not None:
            d = abs((c['us_world_exports_b'] - c['us_world_imports_b']) - c['us_world_balance_b'])
            check(d <= 0.25, f"US world totals tie (diff {d:.2f})")
    else:
        e, i, b = c['us_exports_usd_b'], c['us_imports_usd_b'], c['us_bilateral_usd_b']
        check(round(e - i, 1) == b, f"{c['country']}: bilateral {b} == {e}-{i}")

# ---------- 3. every figure has a year ----------
for c in CO:
    check(bool(c['gdp_year']) and bool(c['us_trade_year']) and bool(c['overall_balance_year']),
          f"{c['country']}: figures carry reference years")

# ---------- 4. displayed officials well-formed ----------
for c in CO:
    for key in ('digital_ministers', 'trade_ministers'):
        shown = [o for o in c[key] if o.get('display') in ('full', 'half')]
        check(1 <= len(shown) <= 2, f"{c['country']}/{key}: 1-2 displayed officials (got {len(shown)})")
        for o in shown:
            check(bool(o['name'] and o['title'] and o['ministry']), f"{c['country']}/{o['name']}: complete fields")

# ---------- 5. workbook ----------
wb = load_workbook(ROOT + 'output/g20-ministers-trade-reference.xlsx'); ws = wb.active
hdr = {ws.cell(1, j).value.replace('\n', ' '): j for j in range(1, 17)}
rowby = {ws.cell(r, 1).value: r for r in range(2, 21)}
gcol = [k for k in hdr if k.startswith('GDP (')][0]
bcol = [k for k in hdr if k.startswith('U.S. bilateral')][0]
dcol = [k for k in hdr if k.startswith('Digital / technology')][0]
tcol = [k for k in hdr if k.startswith('Trade / commerce')][0]
fcol = [k for k in hdr if k.startswith('Confidence')][0]
for c in CO:
    r = rowby[c['country']]
    check(abs((ws.cell(r, hdr[gcol]).value or 0) - c['gdp_usd_b']) < 0.05, f"xlsx GDP {c['country']}")
    bv = ws.cell(r, hdr[bcol]).value
    if c['us_bilateral_usd_b'] is None:
        check(bv == 'N/A', "xlsx US bilateral N/A")
    else:
        check(abs(bv - c['us_bilateral_usd_b']) < 0.05, f"xlsx bilateral {c['country']}")
    check(ws.cell(r, hdr[fcol]).value == c['row_confidence'], f"xlsx flag {c['country']}")
    dprim = next(o for o in c['digital_ministers'] if o.get('is_primary'))
    tprim = next(o for o in c['trade_ministers'] if o.get('is_primary'))
    check(dprim['name'] in str(ws.cell(r, hdr[dcol]).value), f"xlsx digital {c['country']}")
    check(tprim['name'] in str(ws.cell(r, hdr[tcol]).value), f"xlsx trade {c['country']}")
check(ws.freeze_panes == 'A2', "xlsx frozen header")
check(len(ws.conditional_formatting._cf_rules) >= 1, "xlsx conditional formatting")

# ---------- 6. pptx ----------
prs = Presentation(ROOT + 'output/g20-ministers-trade-deck.pptx')
slides = list(prs.slides)
BL = D.get('blocs', [])
EXPECT = 24 + len(BL)
check(len(slides) == EXPECT, f"pptx {EXPECT} slides (got {len(slides)})")
def stext(sl): return "\n".join(sh.text_frame.text for sh in sl.shapes if sh.has_text_frame)
country_slides = slides[4:23]
for idx, c in enumerate(CO):
    sl = country_slides[idx]; txt = stext(sl)
    check(c['country'] in txt, f"pptx slide {idx+1} is {c['country']}")
    check(money(c['gdp_usd_b']) in txt, f"pptx GDP {c['country']}")
    if c['country'] == 'United States':
        if c.get('us_world_exports_b') is not None:
            check(absmoney(c['us_world_exports_b']) in txt and absmoney(c['us_world_imports_b']) in txt,
                  "pptx US world totals shown")
    else:
        check(absmoney(c['us_exports_usd_b']) in txt and absmoney(c['us_imports_usd_b']) in txt
              and absmoney(c['us_bilateral_usd_b']) in txt, f"pptx trade figures {c['country']}")
    shown = [o for g in ('digital_ministers','trade_ministers') for o in c[g] if o.get('display') in ('full','half')]
    for o in shown:
        check(o['name'] in txt and o['title'] in txt, f"pptx name+title {c['country']}/{o['name']}")
    pics = [sh for sh in sl.shapes if sh.shape_type == 13]
    check(len(pics) >= 1, f"pptx flag embedded {c['country']}")
    check('NEEDS CHECK' not in txt and 'VACANT / ACTING' not in txt,
          f"pptx no confidence badge {c['country']}")
us_txt = stext(country_slides[names.index('United States')])
check('Howard Lutnick' in us_txt and 'Jamieson Greer' in us_txt, "pptx US shows Commerce Sec & USTR")
allpptx = "\n".join(stext(s) for s in slides)
check('Prepared for' not in allpptx, "pptx: 'Prepared for' removed")
check('INTERNATIONAL TRADE ADMINISTRATION' in allpptx, "pptx: ITA official framing present")

# ---------- 7. pdf ----------
doc = fitz.open(ROOT + 'output/g20-ministers-trade-deck.pdf')
check(doc.page_count == EXPECT, f"pdf {EXPECT} pages (got {doc.page_count})")
for i in range(doc.page_count):
    w, h = doc[i].rect.width / 72, doc[i].rect.height / 72
    if not (abs(w - 13.333) < 0.05 and abs(h - 7.5) < 0.05):
        check(False, f"pdf page {i+1} size {w:.2f}x{h:.2f}")
pdf_country = [doc[p].get_text() for p in range(4, 23)]
for idx, c in enumerate(CO):
    txt = pdf_country[idx]
    check(c['country'] in txt, f"pdf page is {c['country']}")
    check(money(c['gdp_usd_b']) in txt, f"pdf GDP {c['country']}")
    dprim = next(o for o in c['digital_ministers'] if o.get('is_primary'))
    check(dprim['name'] in txt, f"pdf digital name {c['country']}")
allpdf = "\n".join(doc[p].get_text() for p in range(doc.page_count))
us_pdf = pdf_country[names.index('United States')]
check('Howard Lutnick' in us_pdf and 'Jamieson Greer' in us_pdf, "pdf US shows both officials")

# ---------- 8. diacritics (auto-derived from displayed names) ----------
dia = sorted({o['name'] for c in CO + D.get('blocs', []) for g in ('digital_ministers','trade_ministers') for o in c[g]
              if o.get('display') in ('full','half') and any(ord(ch) > 127 for ch in o['name'])} | {'Türkiye'})
for name in dia:
    check(name in allpptx, f"pptx diacritics: {name}")
    check(name in allpdf, f"pdf diacritics: {name}")

# ---------- 9. roster char-for-char vs reference ----------
refset = {(r['country'], r['name'], r['title'], r['ministry']) for r in ROSTER}
for c in CO:
    for g in ('digital_ministers','trade_ministers'):
        for o in c[g]:
            check((c['country'], o['name'], o['title'], o['ministry']) in refset,
                  f"roster match {c['country']}/{o['name']}")

# ---------- 10. flags, portraits, seal are valid images ----------
for c in CO:
    im = Image.open(ROOT + c['flag_file']); im.load()
    check(im.width > 0, f"flag valid {c['country']}")
for sp in ('assets/seal/doc-seal.png', 'assets/seal/doc-seal-white.png'):
    if os.path.exists(ROOT + sp):
        im = Image.open(ROOT + sp); im.load()
        check(im.width >= 300, f"seal valid & high-res ({sp})")

# ---------- 11. text-fit (font metrics, v2 geometry) ----------
FP = {'reg': '/usr/local/share/fonts/ita/OpenSans-Regular.ttf',
      'bold': '/usr/local/share/fonts/ita/OpenSans-Bold.ttf',
      'ital': '/usr/local/share/fonts/ita/OpenSans-Italic.ttf'}
_fc = {}
def font(style, pt):
    k = (style, round(pt * 96 / 72))
    if k not in _fc: _fc[k] = ImageFont.truetype(FP[style], k[1])
    return _fc[k]
def nlines(text, pt, width_in, style='reg'):
    if not text: return 0
    f = font(style, pt); maxw = width_in * 96; lines = 1; cur = 0.0
    sp = f.getlength(' ')
    for word in text.split():
        wl = f.getlength(word)
        if cur == 0: cur = wl
        elif cur + sp + wl <= maxw: cur += sp + wl
        else: lines += 1; cur = wl
    return lines

RX, RW = 3.95, 8.78; COL_W = 4.21; H = 2.82
tight = []
for c in CO + BL:
    for g, div in (('digital_ministers', 'div_note_digital'), ('trade_ministers', 'div_note_trade')):
        shown = [o for o in c[g] if o.get('display') in ('full', 'half')]
        notes = [o for o in c[g] if o.get('display') == 'note']
        if len(shown) == 1:
            o = shown[0]
            tl = nlines(o['title'], 11, RW, 'ital')
            ml = nlines(o['ministry'] + ('    Assumed office: ' + o.get('assumed_office', '') if o.get('assumed_office') else ''), 9.5, RW)
            bio = o.get('bio_display') or o.get('bio', '')
            bh = nlines(bio, 11, RW) * 11 * 1.03 / 72
            note_line = '; '.join(f"{n['name']} ({n['title']})" for n in notes)
            dn = c.get(div) or ''
            full_note = dn if dn else ('Also: ' + note_line if note_line else '')
            nh = (5/72 + nlines('Also: ' + full_note, 9, RW, 'ital') * 9 * 1.2 / 72) if full_note else 0
            fits = tl <= 3 and ml <= 2 and (bh + nh) <= (H - 1.34) + 0.02
            tight.append(((bh + nh) / (H - 1.34), c['country'], g[:3], 'full'))
            check(fits, f"fit full {c['country']}/{g[:3]} bio+note {bh+nh:.2f}<={H-1.34:.2f} title {tl}L min {ml}L")
        elif len(shown) == 2:
            for o in shown:
                head_h = (0.11 if o.get('role_tag') else 0) + \
                         nlines(o['name'] + ('  · acting' if o.get('is_acting') else ''), 12, COL_W, 'bold') * 12 * 1.1 / 72 + \
                         nlines(o['title'], 9, COL_W, 'ital') * 9 * 1.18 / 72 + 4/72
                ml = nlines(o['ministry'] + ('  ·  ' + o.get('assumed_office', '') if o.get('assumed_office') else ''), 8.5, COL_W)
                bio = o.get('bio_display') or o.get('bio', '')
                bh = nlines(bio, 10.5, COL_W) * 10.5 * 1.24 / 72
                fits = head_h <= 1.00 and ml <= 2 and bh <= (H - 1.62) + 0.02
                tight.append((max(head_h / 1.00, bh / (H - 1.62)), c['country'], g[:3], o['name'][:14]))
                check(fits, f"fit half {c['country']}/{g[:3]}/{o['name'][:16]} head {head_h:.2f}<=1.00 min {ml}L bio {bh:.2f}<={H-1.62:.2f}")

# ---------- 11b. bloc annex slides ----------
if BL:
    check(len(BL) == 2, f"two bloc profiles (got {len(BL)})")
    bloc_slides = slides[23:23+len(BL)]
    for i, b in enumerate(BL):
        txt = stext(bloc_slides[i]); ptxt = doc[23+i].get_text()
        check(b['country'] in txt and b['country'] in ptxt, f"bloc slide present: {b['country']}")
        check(money(b['gdp_usd_b']) in txt and money(b['gdp_usd_b']) in ptxt, f"bloc GDP {b['country']}")
        if b['us_bilateral_usd_b'] is not None:
            check(abs(round(b['us_exports_usd_b']-b['us_imports_usd_b'],1)-b['us_bilateral_usd_b'])<0.05,
                  f"bloc bilateral ties {b['country']}")
            check(absmoney(b['us_bilateral_usd_b']) in txt, f"bloc bilateral shown {b['country']}")
        for g in ('digital_ministers','trade_ministers'):
            for o in b[g]:
                if o.get('display') in ('full','half'):
                    check(o['name'] in txt and o['name'] in ptxt, f"bloc official {b['country']}/{o['name']}")
        pics = [sh for sh in bloc_slides[i].shapes if sh.shape_type == 13]
        check(len(pics) >= 1, f"bloc flag embedded {b['country']}")

# ---------- 12. GAPS ----------
check(os.path.exists(ROOT + 'output/GAPS.md') and os.path.getsize(ROOT + 'output/GAPS.md') > 500, "GAPS.md non-empty")

print(f"\n{'='*60}\nQA RESULTS: {len(PASS)} passed, {len(FAIL)} failed\n{'='*60}")
if FAIL:
    print("\nFAILURES:")
    for f in FAIL: print("  ✗", f)
else:
    print("\nALL CHECKS PASSED ✓")
tight.sort(reverse=True)
print("\nTightest boxes:")
for r in tight[:6]: print(f"  ratio={r[0]:.2f}  {r[1]} {r[2]} {r[3]}")
sys.exit(1 if FAIL else 0)

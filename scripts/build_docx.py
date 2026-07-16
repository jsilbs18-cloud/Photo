#!/usr/bin/env python3
"""Build output/g20-ministers-trade-list.docx from data/g20.json — the narrative
minister list in ITA Visual Style Guide format (Trade Navy/Blue/Gold, Open Sans,
official document signatures). Same source of truth as the deck."""
import json
import docx
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ROOT = '/home/user/Photo/'
D = json.load(open(ROOT + 'data/g20.json'))
CO = D['countries']; BL = D.get('blocs', [])

NAVY = RGBColor(0x0A, 0x31, 0x4D); BLUE = RGBColor(0x00, 0x55, 0x8C)
GOLD = RGBColor(0xB4, 0x86, 0x2D); INK = RGBColor(0x2C, 0x2C, 0x2C)
GRAY = RGBColor(0x54, 0x60, 0x6C); MUTED = RGBColor(0x75, 0x7D, 0x87)
ORANGE = RGBColor(0xD4, 0x61, 0x27); TEAL = RGBColor(0x00, 0x75, 0x82)
FONT = 'Open Sans'   # ITA primary; Word substitutes Calibri-family if absent

doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Inches(8.5), Inches(11)
sec.left_margin = sec.right_margin = Inches(0.9)
sec.top_margin, sec.bottom_margin = Inches(0.8), Inches(0.9)

st = doc.styles['Normal']
st.font.name = FONT; st.font.size = Pt(10); st.font.color.rgb = INK
st.element.rPr.rFonts.set(qn('w:eastAsia'), FONT)
st.paragraph_format.space_after = Pt(4)

def run(p, text, size=10, color=INK, bold=False, italic=False, caps_spacing=False):
    r = p.add_run(text); r.font.name = FONT; r.font.size = Pt(size)
    r.font.color.rgb = color; r.bold = bold; r.italic = italic
    r.element.rPr.rFonts.set(qn('w:eastAsia'), FONT)
    if caps_spacing:
        sp = OxmlElement('w:spacing'); sp.set(qn('w:val'), '20')
        r.element.rPr.append(sp)
    return r

def shade(p, hexcolor):
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement('w:shd'); shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), hexcolor)
    pPr.append(shd)

def bottom_border(p, hexcolor, size=12, space=4):
    pPr = p._p.get_or_add_pPr()
    pbdr = OxmlElement('w:pBdr'); bot = OxmlElement('w:bottom')
    bot.set(qn('w:val'), 'single'); bot.set(qn('w:sz'), str(size))
    bot.set(qn('w:space'), str(space)); bot.set(qn('w:color'), hexcolor)
    pbdr.append(bot); pPr.append(pbdr)

def money(v, year=None):
    if v is None: return 'N/A'
    s = f"${abs(v):,.1f} billion"
    return s if year is None else f"{s} ({year})"

def balance_word(v): return 'surplus' if (v or 0) >= 0 else 'deficit'

# ================= header band =================
p = doc.add_paragraph(); shade(p, '0A314D')
p.paragraph_format.space_before = Pt(10); p.paragraph_format.space_after = Pt(0)
run(p, 'G20 Digital & Trade Ministers', 20, RGBColor(0xFF, 0xFF, 0xFF), bold=True)
p2 = doc.add_paragraph(); shade(p2, '0A314D'); p2.paragraph_format.space_after = Pt(0)
run(p2, 'GDP and U.S. Bilateral Trade Profiles  |  Internal Reference  |  July 16, 2026',
    10, RGBColor(0xB9, 0xC9, 0xD9))
p3 = doc.add_paragraph(); shade(p3, '0A314D'); p3.paragraph_format.space_after = Pt(10)
run(p3, 'U.S. Department of Commerce  |  International Trade Administration', 8,
    RGBColor(0xFF, 0xFF, 0xFF), bold=True)
pv = doc.add_paragraph(); pv.paragraph_format.space_after = Pt(12)
run(pv, 'Data vintage: Trade — U.S. Census goods, 2025 full year (goods basis) · GDP — IMF WEO, 2025 · '
        'Officeholders verified as current on 2026-07-16 · Figures in USD billions unless noted.',
    8.5, MUTED, italic=True)

# ================= per-entry writers =================
def country_heading(name, tag=None):
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.keep_with_next = True
    bottom_border(p, 'B4862D', size=14, space=3)
    run(p, name, 14, NAVY, bold=True)
    if tag: run(p, f'    ·    {tag}', 9, TEAL, bold=True, caps_spacing=True)

def subhead(text):
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.keep_with_next = True
    run(p, text.upper(), 9.5, BLUE, bold=True, caps_spacing=True)

def official_entry(o):
    p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.keep_with_next = True
    run(p, o['name'], 11, NAVY, bold=True)
    if o.get('is_acting'): run(p, '  · acting', 9, ORANGE, bold=True, italic=True)
    run(p, f",  {o['title']}", 10, GRAY, italic=True)
    meta = o['ministry'] + (f"  ·  Assumed office: {o['assumed_office']}" if o.get('assumed_office') else '')
    pm = doc.add_paragraph(); pm.paragraph_format.space_after = Pt(2)
    pm.paragraph_format.keep_with_next = True
    run(pm, meta, 8.5, MUTED)
    pb = doc.add_paragraph(); pb.paragraph_format.space_after = Pt(6)
    run(pb, o.get('bio_display') or o.get('bio', ''), 10, INK)

def section(offs, div_note, label):
    shown = [o for o in offs if o.get('display') in ('full', 'half')]
    notes = [o for o in offs if o.get('display') == 'note']
    subhead(label)
    for o in shown:
        official_entry(o)
    line = div_note or ('Also: ' + '; '.join(f"{o['name']} ({o['title']})" for o in notes) if notes else '')
    if line:
        p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(4)
        run(p, line, 8.5, GRAY, italic=True)

def bullet(text):
    p = doc.add_paragraph(style='List Bullet'); p.paragraph_format.space_after = Pt(1)
    run(p, text, 10, INK)

def figures_block(c, is_us=False, au=False):
    gy, ty, oy = c['gdp_year'], c['us_trade_year'], c['overall_balance_year']
    ob = c['overall_balance_usd_b']
    basis = 'goods' if 'goods-only' in c['overall_balance_basis'] else 'goods-and-services'
    intro = doc.add_paragraph(); intro.paragraph_format.space_before = Pt(4)
    name = c['country']
    if is_us and c.get('us_world_exports_b') is not None:
        txt = (f"The United States had a nominal GDP of {money(c['gdp_usd_b'])} in {gy} and recorded an overall goods "
               f"trade deficit of {money(ob)} in {oy}. Because the United States is the reference country for the "
               f"bilateral figures in this list, world totals are shown instead: {money(c['us_world_exports_b'])} in "
               f"goods exports and {money(c['us_world_imports_b'])} in goods imports in {ty}.")
    elif au:
        txt = (f"African Union member states had an aggregate nominal GDP of approximately {money(c['gdp_usd_b'])} in {gy}. "
               f"No clean continental goods-trade balance is published. U.S.–Africa goods trade (a proxy for the AU) in {ty}: "
               f"{money(c['us_exports_usd_b'])} in U.S. exports and {money(c['us_imports_usd_b'])} in U.S. imports, "
               f"a U.S. goods trade {balance_word(c['us_bilateral_usd_b'])} of {money(c['us_bilateral_usd_b'])}.")
    else:
        txt = (f"{name} had a nominal GDP of {money(c['gdp_usd_b'])} in {gy} and recorded an overall {basis} trade "
               f"{balance_word(ob)} of {money(ob)} in {oy}. The United States exported {money(c['us_exports_usd_b'])} in "
               f"goods to {name} and imported {money(c['us_imports_usd_b'])}, for a U.S. goods trade "
               f"{balance_word(c['us_bilateral_usd_b'])} of {money(c['us_bilateral_usd_b'])} in {ty}.")
    run(intro, txt, 10, INK)
    kf = doc.add_paragraph(); kf.paragraph_format.keep_with_next = True
    run(kf, 'Key Figures:', 10, NAVY, bold=True)
    bullet(f"Nominal GDP: {money(c['gdp_usd_b'], gy)}")
    if au:
        bullet(f"Continental goods balance: not published (N/A)")
    else:
        bullet(f"Overall {basis} trade {balance_word(ob)}: {money(ob, oy)}")
    if is_us and c.get('us_world_exports_b') is not None:
        bullet(f"U.S. goods exports — world: {money(c['us_world_exports_b'], ty)}")
        bullet(f"U.S. goods imports — world: {money(c['us_world_imports_b'], ty)}")
        bullet(f"U.S. goods balance — world: {money(c['us_world_balance_b'], ty)} ({balance_word(c['us_world_balance_b'])})")
    else:
        scope = 'U.S.–Africa ' if au else ''
        bullet(f"{scope}U.S. goods exports: {money(c['us_exports_usd_b'], ty)}")
        bullet(f"{scope}U.S. goods imports: {money(c['us_imports_usd_b'], ty)}")
        bullet(f"{scope}U.S. bilateral goods {balance_word(c['us_bilateral_usd_b'])}: {money(c['us_bilateral_usd_b'], ty)}")

# ================= countries =================
for c in CO:
    is_us = c['country'] == 'United States'
    country_heading(c['country'])
    figures_block(c, is_us=is_us)
    section(c['trade_ministers'], c.get('div_note_trade'), 'Trade Minister' if len(
        [o for o in c['trade_ministers'] if o.get('display') in ('full', 'half')]) == 1 else 'Trade Ministers')
    section(c['digital_ministers'], c.get('div_note_digital'), 'Digital Minister' if len(
        [o for o in c['digital_ministers'] if o.get('display') in ('full', 'half')]) == 1 else 'Digital Ministers')

# ================= bloc annex =================
p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(18)
bottom_border(p, '0A314D', size=8, space=2)
run(p, 'G20 BLOC MEMBERS — ANNEX', 12, NAVY, bold=True, caps_spacing=True)
pa = doc.add_paragraph()
run(pa, 'The European Union and African Union hold G20 seats as supranational blocs and are profiled here '
        'alongside the 19 sovereign members.', 9, GRAY, italic=True)
for b in BL:
    au = b['country'] == 'African Union'
    country_heading(b['country'], tag='G20 BLOC MEMBER')
    pf = doc.add_paragraph(); pf.paragraph_format.space_after = Pt(2)
    run(pf, '   ·   '.join(f"{f['label']}: {f['value']}" for f in b.get('facts', [])), 8.5, GRAY)
    figures_block(b, au=au)
    section(b['trade_ministers'], b.get('div_note_trade'), 'Trade Lead')
    section(b['digital_ministers'], b.get('div_note_digital'), 'Digital / Technology Lead')

# ================= caveats =================
p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(16)
bottom_border(p, 'B4862D', size=14, space=3)
run(p, 'Data Caveats', 14, NAVY, bold=True)
for t in ["Basis exceptions: Australia's overall balance is goods+services; India's is fiscal year 2025-26. All others goods-only, calendar 2025.",
          "Several overall balances are converted from local currency (EUR/GBP/CAD/AUD/JPY/SAR) at ~2025 average rates; USD values carry exchange-rate uncertainty.",
          "African Union: U.S. trade figures are U.S.–Africa goods totals (proxy); no clean continental goods balance is published.",
          "Acting officials: Argentina's domestic commerce portfolio (Lavigne) and Saudi Arabia's GAFT governorship are held on an acting basis.",
          "Sources and vintages: GDP — IMF WEO 2025; U.S. bilateral goods trade — U.S. Census 2025 (via USTR fact sheets / Census-derived channels); officeholders verified 2026-07-16. Full uncertainty register: output/GAPS.md."]:
    bullet(t)

# ================= footer =================
foot = sec.footer.paragraphs[0]
foot.paragraph_format.tab_stops.add_tab_stop(Inches(6.7), WD_TAB_ALIGNMENT.RIGHT)
run(foot, 'U.S. Department of Commerce  |  International Trade Administration', 8, BLUE, bold=True)
r = foot.add_run('\ttrade.gov  ·  '); r.font.name = FONT; r.font.size = Pt(8)
r.font.color.rgb = BLUE; r.bold = True
fld = OxmlElement('w:fldSimple'); fld.set(qn('w:instr'), 'PAGE')
rr = OxmlElement('w:r'); rPr = OxmlElement('w:rPr')
sz = OxmlElement('w:sz'); sz.set(qn('w:val'), '16'); rPr.append(sz)
col = OxmlElement('w:color'); col.set(qn('w:val'), '757D87'); rPr.append(col)
rr.append(rPr); fld.append(rr); foot._p.append(fld)

doc.save(ROOT + 'output/g20-ministers-trade-list.docx')
print('Wrote output/g20-ministers-trade-list.docx —', len(CO), 'countries +', len(BL), 'blocs')

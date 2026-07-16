#!/usr/bin/env python3
"""Build a print-ready HTML mirror of the deck (-> Chromium -> PDF) from data/g20.json.
v2 layout: official ITA/DOC framing, portraits, split-portfolio two-column sections.
Coordinates in inches mirror scripts/build_pptx.py so PDF and PPTX match."""
import json, base64, html, os

ROOT = '/home/user/Photo/'
D = json.load(open(ROOT + 'data/g20.json'))
CO = D['countries']; META = D['meta']
SEAL = META.get('seal_file') if META.get('seal_file') and os.path.exists(ROOT + META.get('seal_file', '')) else None

NAVY="#1F3864"; SLATE="#44546A"; INK="#262626"; MUTED="#7F7F7F"; PANEL="#F3F5F9"
RULE="#D6DCE5"; POS="#1E7A34"; NEG="#B23330"; ACCENT="#2E5A88"; STEEL="#AEB9CF"; ORANGE="#C05A00"

def esc(t): return html.escape(str(t))
def money(v): return 'N/A' if v is None else f"${v:,.1f}B"
def signed(v):
    if v is None: return ('N/A', SLATE, '')
    return (f"{'+' if v>=0 else '−'}${abs(v):,.1f}B", POS if v>=0 else NEG, 'surplus' if v>=0 else 'deficit')

_img={}
def data_uri(path):
    if path not in _img:
        b=open(ROOT+path,'rb').read(); _img[path]='data:image/png;base64,'+base64.b64encode(b).decode()
    return _img[path]

from PIL import Image
_ar={}
def img_ar(path):
    if path not in _ar:
        im=Image.open(ROOT+path); _ar[path]=im.width/im.height
    return _ar[path]

S=[]
def box(l,t,w,style="",inner="",h=None):
    hh=f"height:{h}in;" if h is not None else ""
    return f'<div style="position:absolute;left:{l}in;top:{t}in;width:{w}in;{hh}{style}">{inner}</div>'

def footer(idx=None,total=None):
    parts=[f'<div style="position:absolute;left:0.6in;top:6.98in;width:12.13in;height:1px;background:{RULE}"></div>']
    x=0.6
    if SEAL:
        w=0.34*img_ar(SEAL)
        parts.append(f'<img src="{data_uri(SEAL)}" style="position:absolute;left:0.6in;top:7.06in;height:0.34in">')
        x=0.6+w+0.14
    parts.append(box(x,7.05,10.3,"",
        f'<div style="font-size:7.5pt;font-weight:700;color:{SLATE};letter-spacing:.5px">INTERNATIONAL TRADE ADMINISTRATION · U.S. DEPARTMENT OF COMMERCE</div>'
        f'<div style="font-size:7.5pt;color:{MUTED}">GDP — IMF WEO 2025 · U.S. goods trade — U.S. Census 2025 · officeholders verified 2026-07-16</div>'))
    if idx is not None:
        parts.append(box(11.6,7.10,1.13,"text-align:right",f'<div style="font-size:8pt;color:{MUTED}">{idx} / {total}</div>'))
    return ''.join(parts)

# ---------- TITLE ----------
def title_slide():
    p=[f'<div style="position:absolute;left:0;top:0;width:13.333in;height:0.22in;background:{ACCENT}"></div>',
       f'<div style="position:absolute;left:0;bottom:0;width:13.333in;height:0.22in;background:{ACCENT}"></div>']
    y=1.05
    if SEAL:
        w=1.35*img_ar(SEAL)
        p.append(f'<img src="{data_uri(SEAL)}" style="position:absolute;left:{(13.333-w)/2}in;top:{y}in;height:1.35in">')
        y+=1.55
    else:
        y+=0.5
    p.append(box(1.0,y,11.33,"text-align:center",
        f'<div style="font-size:13pt;color:{STEEL};letter-spacing:2px">U.S. DEPARTMENT OF COMMERCE</div>'
        f'<div style="font-size:17pt;color:#fff;font-weight:700;letter-spacing:2.5px;margin-top:5pt">INTERNATIONAL TRADE ADMINISTRATION</div>'))
    p.append(box(1.0,y+1.05,11.33,"text-align:center",
        f'<div style="font-size:32pt;font-weight:700;color:#fff">G20 Countries: Digital &amp; Trade Ministers</div>'
        f'<div style="font-size:19pt;color:#C7D3E8;margin-top:6pt">with GDP and U.S. Bilateral Trade Profiles</div>'))
    p.append(box(1.0,y+2.75,11.33,"text-align:center",f'<div style="font-size:12.5pt;color:{STEEL}">July 16, 2026 · Internal Reference</div>'))
    p.append(box(1.6,6.55,10.13,"text-align:center",
        f'<div style="font-size:10pt;color:#8F9EBE">Data vintage: Trade — U.S. Census goods, 2025 full year (goods basis) · GDP — IMF WEO, 2025 · Officeholders verified as current on 2026-07-16 · USD billions unless noted</div>'))
    S.append(f'<div class="slide" style="background:{NAVY}">{"".join(p)}</div>')

# ---------- header ----------
def header_bar(title,kicker):
    x=0.6; seal=''
    if SEAL:
        w=0.56*img_ar(SEAL)
        seal=f'<img src="{data_uri(SEAL)}" style="position:absolute;left:0.6in;top:0.22in;height:0.56in">'
        x=0.6+w+0.20
    return (f'<div style="position:absolute;left:0;top:0;width:13.333in;height:1.0in;background:{NAVY}"></div>'
            f'<div style="position:absolute;left:0;top:1.0in;width:13.333in;height:0.06in;background:{ACCENT}"></div>'
            + seal
            + box(x,0.20,12.73-x,"",f'<div style="font-size:24pt;font-weight:700;color:#fff">{esc(title)}</div>')
            + (box(x,0.70,12.0,"",f'<div style="font-size:11pt;color:#B9C5DC">{esc(kicker)}</div>') if kicker else ""))

# ---------- METHODOLOGY ----------
def methodology_slide():
    def b(label,text): return (f'<p style="margin:0 0 7pt 0;font-size:12.5pt;color:{INK};line-height:1.25">'
                               f'<b style="color:{NAVY}">{esc(label)}</b>&nbsp;&nbsp;{esc(text)}</p>')
    left=(b("Countries (19):","Argentina, Australia, Brazil, Canada, China, France, Germany, India, Indonesia, Italy, "
              "Japan, Mexico, Poland, Russia, Saudi Arabia, South Korea, Türkiye, United Kingdom, United States.")
          +b("Substitution:","Poland is covered in place of South Africa — a deliberate substitution, not an omission.")
          +b("Bloc seats excluded:","The European Union and African Union hold G20 seats but are supranational blocs, not sovereign countries, and are not profiled.")
          +b("GDP:","Nominal (current USD), IMF World Economic Outlook 2025, single vintage across all 19.")
          +b("U.S. bilateral trade:","U.S. Census Bureau goods trade, 2025 full year (goods basis), via Census-derived channels (see Sources).")
          +b("Ministers:","Each officeholder confirmed current on 2026-07-16 by live search plus an independent verification pass. Where a portfolio is split, both responsible officials are profiled."))
    about=""
    for t in ["Prepared within the International Trade Administration, U.S. Department of Commerce, as an internal reference.",
              "One structured dataset generates this deck, the companion workbook, and the PDF, so figures cannot drift between formats.",
              "Portraits are official government photos; a monogram placeholder marks any still to be supplied.",
              "Data caveats, acting officials, and items pending confirmation are tracked in a separate gaps register (GAPS.md) rather than flagged on slides."]:
        about+=f'<div style="margin-top:10pt;font-size:10.5pt;color:{SLATE}">{esc(t)}</div>'
    panel=(f'<div style="position:absolute;left:8.5in;top:1.5in;width:4.23in;height:5.1in;background:{PANEL}"></div>'
           f'<div style="position:absolute;left:8.5in;top:1.5in;width:4.23in;height:0.04in;background:{ACCENT}"></div>'
           +box(8.8,1.75,3.7,"",f'<div style="font-size:11pt;font-weight:700;color:{NAVY};letter-spacing:1px">ABOUT THIS DOCUMENT</div>{about}'))
    S.append(f'<div class="slide">{header_bar("Methodology & Scope","19 G20 sovereign members · compiled 2026-07-16")}'
             f'{box(0.6,1.35,7.5,"",left)}{panel}{footer()}</div>')

# ---------- SUMMARY ----------
def summary_slide(rows,part,total):
    cols=[("Country",0.6,3.4,'left'),("GDP (2025)",4.0,2.0,'right'),
          ("U.S. exports to",6.05,2.2,'right'),("U.S. imports from",8.30,2.3,'right'),
          ("U.S. bilateral balance",10.65,2.08,'right')]
    y0=1.40; rh=0.485
    parts=[f'<div style="position:absolute;left:0.5in;top:{y0}in;width:12.33in;height:{rh}in;background:{NAVY}"></div>']
    for name,x,w,al in cols:
        parts.append(box(x,y0+0.12,w,f"text-align:{al}",f'<span style="font-size:11.5pt;font-weight:700;color:#fff">{esc(name)}</span>'))
    for i,c in enumerate(rows):
        y=y0+rh+i*rh
        if i%2==0: parts.append(f'<div style="position:absolute;left:0.5in;top:{y}in;width:12.33in;height:{rh}in;background:{PANEL}"></div>')
        bs,bc,_=signed(c['us_bilateral_usd_b'])
        cells=[(esc(c['country']),INK,True),(money(c['gdp_usd_b']),INK,False),
               (money(c['us_exports_usd_b']),INK,False),(money(c['us_imports_usd_b']),INK,False),(bs,bc,True)]
        for (name,x,w,al),(val,col,bold) in zip(cols,cells):
            parts.append(box(x,y+0.11,w,f"text-align:{al}",
                f'<span style="font-size:11.5pt;color:{col};font-weight:{700 if bold else 400}">{val}</span>'))
    parts.append(box(0.5,y0+rh+len(rows)*rh+0.08,12.33,"",
        f'<div style="font-size:9pt;color:{MUTED};font-style:italic">Negative U.S. bilateral balance = U.S. goods deficit; positive = U.S. surplus. '
        f'Bilateral columns measure trade with the United States, so the U.S. row shows N/A — the U.S. country page reports world totals.</div>'))
    S.append(f'<div class="slide">{header_bar("Summary — GDP & U.S. Bilateral Goods Trade",f"USD billions · GDP 2025 · trade 2025 (goods) · part {part} of {total}")}{"".join(parts)}{footer()}</div>')

# ---------- COUNTRY ----------
LP_X, LP_W = 0.6, 3.10
RX, RW = 3.95, 8.78
COL_W = 4.21; COL2_X = RX + COL_W + 0.36
BLK = [(1.26, 2.82), (4.14, 2.82)]

def datum(l,t,w,label,value,vcolor=NAVY,sub=None):
    subhtml=f'<span style="font-size:9.5pt;color:{SLATE};font-weight:400">&nbsp;&nbsp;{esc(sub)}</span>' if sub else ''
    return box(l,t,w,"",
        f'<div style="font-size:9pt;color:{SLATE};letter-spacing:.3px">{esc(label)}</div>'
        f'<div style="font-size:14.5pt;font-weight:700;color:{vcolor};margin-top:1pt">{value}{subhtml}</div>')

def left_panel(c):
    parts=[f'<div style="position:absolute;left:{LP_X}in;top:1.42in;width:{LP_W}in;height:5.35in;background:{PANEL}"></div>',
           f'<div style="position:absolute;left:{LP_X}in;top:1.42in;width:{LP_W}in;height:0.04in;background:{ACCENT}"></div>',
           box(LP_X+0.20,1.58,LP_W-0.4,"",f'<div style="font-size:10.5pt;font-weight:700;color:{NAVY};letter-spacing:1px">TRADE &amp; ECONOMY</div>')]
    lx=LP_X+0.20; lw=LP_W-0.40; ly=1.98; step=0.96
    gy,ty,oy=c['gdp_year'],c['us_trade_year'],c['overall_balance_year']
    us=c['country']=='United States'
    parts.append(datum(lx,ly,lw,f"NOMINAL GDP ({gy})",money(c['gdp_usd_b'])))
    obs,obc,obw=signed(c['overall_balance_usd_b'])
    basis='goods' if 'goods-only' in c['overall_balance_basis'] else ('g+s' if 'services' in c['overall_balance_basis'] else '')
    parts.append(datum(lx,ly+step,lw,f"OVERALL TRADE BALANCE ({oy})",obs,vcolor=INK,sub=f"{obw} · {basis}"))
    if us and c.get('us_world_exports_b') is not None:
        parts.append(datum(lx,ly+2*step,lw,f"GOODS EXPORTS — WORLD ({ty})",money(c['us_world_exports_b'])))
        parts.append(datum(lx,ly+3*step,lw,f"GOODS IMPORTS — WORLD ({ty})",money(c['us_world_imports_b'])))
        ws,wc,ww=signed(c['us_world_balance_b'])
        parts.append(datum(lx,ly+4*step,lw,f"GOODS BALANCE — WORLD ({ty})",ws,vcolor=wc,sub=ww))
    else:
        parts.append(datum(lx,ly+2*step,lw,f"U.S. GOODS EXPORTS TO ({ty})",money(c['us_exports_usd_b'])))
        parts.append(datum(lx,ly+3*step,lw,f"U.S. GOODS IMPORTS FROM ({ty})",money(c['us_imports_usd_b'])))
        bs,bc,bw=signed(c['us_bilateral_usd_b'])
        parts.append(datum(lx,ly+4*step,lw,f"U.S. BILATERAL BALANCE ({ty})",bs,vcolor=bc,sub=bw))
    return ''.join(parts)

def acting_html(o,size=11.0):
    return (f'<span style="font-size:{max(8.0,size*0.78)}pt;color:{ORANGE};font-weight:700;font-style:italic"> · acting</span>'
            if o.get('is_acting') else '')

def portrait_html(o,l,t,h):
    if not o.get('portrait_file'): return ''
    return (f'<img src="{data_uri(o["portrait_file"])}" '
            f'style="position:absolute;left:{l}in;top:{t}in;height:{h}in;border:0.75pt solid {RULE}">')

def full_profile(y,h,heading,o,notes_line):
    parts=[box(RX,y,RW,"",f'<div style="font-size:10.5pt;font-weight:700;color:{ACCENT};letter-spacing:1.2px">{esc(heading)}</div>')]
    parts.append(portrait_html(o,RX,y+0.30,1.19))
    tx=RX+1.12; tw=RW-1.12
    parts.append(box(tx,y+0.30,tw,"",f'<div style="font-size:14pt;font-weight:700;color:{NAVY}">{esc(o["name"])}{acting_html(o,14)}</div>'))
    parts.append(box(tx,y+0.62,tw,"",f'<div style="font-size:11pt;font-style:italic;color:{SLATE};line-height:1.15">{esc(o["title"])}</div>'))
    ao=f'&nbsp;&nbsp;·&nbsp;&nbsp;<span style="color:{MUTED}">Assumed office: {esc(o["assumed_office"])}</span>' if o.get('assumed_office') else ''
    parts.append(box(tx,y+1.10,tw,"",f'<div style="font-size:9.5pt;color:{INK};line-height:1.15">{esc(o["ministry"])}{ao}</div>'))
    note=(f'<div style="margin-top:5pt;font-size:9pt;font-style:italic;color:{SLATE};line-height:1.2">'
          f'<b style="color:{ACCENT}">Also:</b> {esc(notes_line)}</div>') if notes_line else ''
    parts.append(box(RX,y+1.56,RW,f"height:{h-1.56}in;overflow:hidden",
        f'<div style="font-size:11pt;color:{INK};line-height:1.28">{esc(o.get("bio_display") or o.get("bio",""))}</div>{note}'))
    return ''.join(parts)

def half_profile(x0,y,h,o):
    parts=[portrait_html(o,x0,y+0.28,1.00)]
    tx=x0+0.92; tw=COL_W-0.92
    tag=f'<div style="font-size:7.5pt;font-weight:700;color:{ACCENT};letter-spacing:.8px">{esc(o["role_tag"])}</div>' if o.get('role_tag') else ''
    parts.append(box(tx,y+0.28,tw,f"height:1.26in;overflow:hidden",
        f'{tag}<div style="font-size:12pt;font-weight:700;color:{NAVY};margin-top:2pt">{esc(o["name"])}{acting_html(o,12)}</div>'
        f'<div style="font-size:9pt;font-style:italic;color:{SLATE};line-height:1.18;margin-top:2pt">{esc(o["title"])}</div>'))
    ao=f'&nbsp;·&nbsp;<span style="color:{MUTED}">{esc(o["assumed_office"])}</span>' if o.get('assumed_office') else ''
    parts.append(box(x0,y+1.38,COL_W,"height:0.34in;overflow:hidden",
        f'<div style="font-size:8.5pt;color:{INK};line-height:1.18">{esc(o["ministry"])}{ao}</div>'))
    parts.append(box(x0,y+1.74,COL_W,f"height:{h-1.74}in;overflow:hidden",
        f'<div style="font-size:10.5pt;color:{INK};line-height:1.24">{esc(o.get("bio_display") or o.get("bio",""))}</div>'))
    return ''.join(parts)

def section(blk,heading,offs,div_note):
    y,h=blk
    shown=[o for o in offs if o.get('display') in ('full','half')]
    notes=[o for o in offs if o.get('display')=='note']
    notes_line='; '.join(f"{o['name']} ({o['title']})" for o in notes)
    if div_note and notes_line: notes_line=div_note+' Also: '+notes_line
    elif div_note: notes_line=div_note
    elif notes_line: notes_line='Also: '+notes_line
    if len(shown)>=2:
        head=box(RX,y,RW,"",f'<div style="font-size:10.5pt;font-weight:700;color:{ACCENT};letter-spacing:1.2px">{esc(heading)}&nbsp;&nbsp;·&nbsp;&nbsp;SPLIT PORTFOLIO</div>')
        return head+half_profile(RX,y,h,shown[0])+half_profile(COL2_X,y,h,shown[1])
    elif len(shown)==1:
        return full_profile(y,h,heading,shown[0],notes_line)
    return box(RX,y,RW,"",f'<div style="font-size:10.5pt;font-weight:700;color:{ACCENT}">{esc(heading)}</div><div style="font-size:13pt;color:{ORANGE};font-weight:700">[TO VERIFY]</div>')

def country_slide(c,idx):
    parts=[]
    fh=0.60; fw=fh*img_ar(c['flag_file'])
    parts.append(f'<img src="{data_uri(c["flag_file"])}" style="position:absolute;left:0.6in;top:0.40in;height:{fh}in;border:0.75pt solid {RULE}">')
    parts.append(box(2.1,0.33,9.0,"height:0.75in;display:flex;align-items:center",
        f'<div style="font-size:28pt;font-weight:700;color:{NAVY}">{esc(c["country"])}</div>'))
    parts.append(f'<div style="position:absolute;left:0.6in;top:1.18in;width:12.13in;height:1.5pt;background:{NAVY}"></div>')
    parts.append(left_panel(c))
    parts.append(section(BLK[0],"DIGITAL / TECHNOLOGY",c['digital_ministers'],c.get('div_note_digital')))
    parts.append(f'<div style="position:absolute;left:{RX}in;top:4.08in;width:{RW}in;height:1px;background:{RULE}"></div>')
    parts.append(section(BLK[1],"TRADE / COMMERCE",c['trade_ministers'],c.get('div_note_trade')))
    parts.append(footer(idx,19))
    S.append(f'<div class="slide">{"".join(parts)}</div>')

# ---------- SOURCES ----------
def sources_slide():
    def head(t,first=False): return f'<div style="font-size:12pt;font-weight:700;color:{NAVY};letter-spacing:.5px;margin:{0 if first else 10}pt 0 3pt 0">{esc(t)}</div>'
    def li(t): return f'<div style="font-size:10.5pt;color:{INK};margin-bottom:2pt;line-height:1.2"><span style="color:{ACCENT}">•</span>&nbsp;&nbsp;{esc(t)}</div>'
    left=(head("DATASETS & VINTAGES",True)
        +li("GDP (nominal, current USD): IMF World Economic Outlook, Oct 2025 (2025 estimates), via StatisticsTimes tabulation.")
        +li("U.S. bilateral goods trade: U.S. Census Bureau, full-year 2025, via USTR country fact sheets and the Census/UN-COMTRADE series (Trading Economics mirror).")
        +li("U.S. world totals: Census/BEA FT-900, December & Annual 2025 release.")
        +li("Overall trade balances: national statistics offices / IMF, latest full year, goods basis unless noted.")
        +li("Officeholders: official government sources and 2026-dated press, verified 2026-07-16 with an independent second pass."))
    right=(head("MEASUREMENT NOTES",True)
        +li("Australia's overall balance is goods+services; India's is fiscal year 2025-26. All others goods-only, calendar 2025.")
        +li("Several overall balances are converted from local currency (EUR/GBP/CAD/AUD/JPY/SAR) at ~2025 average rates; USD values carry exchange-rate uncertainty.")
        +li("census.gov and imf.org were not directly reachable from the build environment; figures come from official-data-derived channels.")
        +head("IMAGERY")
        +li("Flags: public-domain renderings, uniform height, true aspect ratios.")
        +li("Portraits: official government portraits; monogram placeholders mark any still to be supplied.")
        +head("SCOPE")
        +li("Poland substituted for South Africa. EU and AU are G20 members but hold bloc seats and are not covered.")
        +li("A detailed uncertainty register (acting officials, figures pending confirmation) accompanies this deck: output/GAPS.md."))
    S.append(f'<div class="slide">{header_bar("Sources & Notes","datasets, vintages, and measurement notes")}'
             f'{box(0.6,1.3,6.05,"",left)}{box(6.95,1.3,5.8,"",right)}{footer()}</div>')

# ---- assemble ----
title_slide(); methodology_slide(); summary_slide(CO[:10],1,2); summary_slide(CO[10:],2,2)
for i,c in enumerate(CO,1): country_slide(c,i)
sources_slide()

CSS=f"""<style>
@page{{size:13.333in 7.5in;margin:0}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Liberation Sans','Helvetica Neue',Arial,sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.slide{{position:relative;width:13.333in;height:7.5in;overflow:hidden;background:#fff;page-break-after:always}}
.slide:last-child{{page-break-after:auto}}
img{{object-fit:cover}}
</style>"""
doc=f"<!doctype html><html><head><meta charset='utf-8'>{CSS}</head><body>{''.join(S)}</body></html>"
open(ROOT+'output/_deck.html','w').write(doc)
print("Wrote output/_deck.html —",len(S),"slides,",len(doc)//1024,"KB")

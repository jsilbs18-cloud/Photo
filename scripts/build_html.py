#!/usr/bin/env python3
"""Build a print-ready HTML mirror of the deck (-> Chromium -> PDF) from data/g20.json.
Styled per the ITA Visual Style Guide (Jan 2026). Coordinates in inches mirror
scripts/build_pptx.py so PDF and PPTX match."""
import json, base64, html, os, re
from PIL import Image, ImageFont

ROOT = '/home/user/Photo/'
D = json.load(open(ROOT + 'data/g20.json'))
CO = D['countries']; META = D['meta']
SEAL_W = 'assets/seal/doc-seal-white.png'
SEAL_W = SEAL_W if os.path.exists(ROOT + SEAL_W) else None

# ITA Visual Style Guide palette
NAVY="#0A314D"; BLUE="#00558C"; GOLD="#B4862D"; SLATE="#B1BBCA"; MOCHA="#E1DACE"
TAN="#E5E5E5"; INK="#2C2C2C"; GRAY="#54606C"; MUTED="#757D87"
POS="#00833E"; NEG="#D46127"; TEAL="#007582"; LTBLUE="#B9C9D9"
SIGNATURE = "U.S. Department of Commerce&nbsp;&nbsp;|&nbsp;&nbsp;International Trade Administration"

def esc(t): return html.escape(str(t))
def money(v): return 'N/A' if v is None else f"${v:,.1f}B"
MON = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
def fmt_date(v):
    m = re.match(r'^(\d{4})-(\d{2})(?:-(\d{2}))?$', v)
    if m:
        y, mo, d = m.group(1), int(m.group(2)), m.group(3)
        return f"{MON[mo-1]} {int(d)}, {y}" if d else f"{MON[mo-1]} {y}"
    m = re.match(r'^([A-Z][a-z]+) (\d{4})$', v)
    if m: return f"{m.group(1)[:3]} {m.group(2)}"
    return v
def signed(v):
    if v is None: return ('N/A', GRAY, '')
    return (f"{'+' if v>=0 else '−'}${abs(v):,.1f}B", POS if v>=0 else NEG, 'surplus' if v>=0 else 'deficit')

_img={}
def data_uri(path):
    if path not in _img:
        b=open(ROOT+path,'rb').read(); _img[path]='data:image/png;base64,'+base64.b64encode(b).decode()
    return _img[path]
_ar={}
def img_ar(path):
    if path not in _ar:
        im=Image.open(ROOT+path); _ar[path]=im.width/im.height
    return _ar[path]

S=[]
def box(l,t,w,style="",inner="",h=None):
    hh=f"height:{h}in;" if h is not None else ""
    return f'<div style="position:absolute;left:{l}in;top:{t}in;width:{w}in;{hh}{style}">{inner}</div>'

def footer(idx=None,total=None,dark=False):
    col = '#fff' if dark else BLUE
    sub = LTBLUE if dark else MUTED
    parts=[]
    if not dark:
        parts.append(f'<div style="position:absolute;left:0.6in;top:7.02in;width:12.13in;height:1px;background:{TAN}"></div>')
    parts.append(box(0.6,7.10,8.6,"",f'<div style="font-size:8pt;font-weight:700;color:{col}">{SIGNATURE}</div>'))
    parts.append(box(0.6,7.28,8.6,"",f'<div style="font-size:7pt;color:{sub}">GDP: IMF WEO 2025 · U.S. goods trade: U.S. Census 2025 · officeholders verified 2026-07-16</div>'))
    lab=(idx if isinstance(idx,str) else f'{idx} / {total}') if idx is not None else None
    pg=f'&nbsp;&nbsp;&nbsp;<span style="font-weight:400;color:{sub};font-size:8pt">{lab}</span>' if lab else ''
    parts.append(box(10.2,7.10,2.53,"text-align:right",f'<div style="font-size:8.5pt;font-weight:700;color:{col}">trade.gov{pg}</div>'))
    return ''.join(parts)

def ribbon(l,t,w,h,color,deg=-35):
    return (f'<div style="position:absolute;left:{l}in;top:{t}in;width:{w}in;height:{h}in;'
            f'background:{color};transform:rotate({deg}deg);transform-origin:top left"></div>')

# ---------- TITLE ----------
def title_slide():
    p=[ribbon(9.68,0.98,7.5,0.85,BLUE), ribbon(10.98,0.53,7.5,0.55,SLATE), ribbon(8.78,1.10,7.5,0.30,TEAL)]
    x=0.6
    if SEAL_W:
        w=0.72*img_ar(SEAL_W)
        p.append(f'<img src="{data_uri(SEAL_W)}" style="position:absolute;left:0.6in;top:0.48in;height:0.72in">')
        x=0.6+w+0.22
    p.append(box(x,0.62,7.0,"",
        f'<div style="font-size:10.5pt;font-weight:700;color:#fff;letter-spacing:1.6px">U.S. DEPARTMENT OF COMMERCE</div>'
        f'<div style="font-size:10.5pt;color:{LTBLUE};letter-spacing:1.6px;margin-top:3pt">INTERNATIONAL TRADE ADMINISTRATION</div>'))
    p.append(box(1.0,2.85,10.5,"",
        f'<div style="font-size:36pt;font-weight:700;color:#fff">G20 Digital &amp; Trade Ministers</div>'
        f'<div style="font-size:20pt;color:{SLATE};margin-top:8pt">GDP and U.S. Bilateral Trade Profiles</div>'))
    p.append(f'<div style="position:absolute;left:1.02in;top:4.42in;width:2.3in;height:0.045in;background:{GOLD}"></div>')
    p.append(f'<div style="position:absolute;left:1.0in;top:4.85in;width:8.6in;height:0.52in;border:1pt solid #5B7792"></div>')
    p.append(box(1.22,4.97,8.2,"",
        f'<div style="font-size:12pt;color:#fff">Internal Reference&nbsp;&nbsp;|&nbsp;&nbsp;Trade data: 2025 full year (goods basis)&nbsp;&nbsp;|&nbsp;&nbsp;July 16, 2026</div>'))
    p.append(box(0.6,6.95,8.6,"",f'<div style="font-size:9pt;font-weight:700;color:#fff">{SIGNATURE}</div>'))
    p.append(box(10.2,6.95,2.53,"text-align:right",f'<div style="font-size:9pt;font-weight:700;color:#fff">trade.gov</div>'))
    S.append(f'<div class="slide" style="background:{NAVY}">{"".join(p)}</div>')

# ---------- content header ----------
def header_bar(title,kicker):
    out=(box(0.6,0.30,12.13,"",f'<div style="font-size:22pt;font-weight:700;color:{NAVY}">{esc(title)}</div>')
         + (box(0.6,0.80,12.13,"",f'<div style="font-size:10.5pt;color:{GRAY}">{esc(kicker)}</div>') if kicker else ""))
    out+=f'<div style="position:absolute;left:0.6in;top:1.10in;width:2.2in;height:0.035in;background:{GOLD}"></div>'
    return out

# ---------- SUMMARY ----------
def summary_slide(rows,part,total):
    cols=[("Country",0.6,3.4,'left'),("GDP (2025)",4.0,2.0,'right'),
          ("U.S. exports to",6.05,2.2,'right'),("U.S. imports from",8.30,2.3,'right'),
          ("U.S. bilateral balance",10.65,2.08,'right')]
    y0=1.42; rh=5.2/(len(rows)+1)   # both parts end at the same baseline (6.62)
    off=(rh-0.22)/2                  # vertically centre one 11.5pt line in the row
    parts=[f'<div style="position:absolute;left:0.5in;top:{y0}in;width:12.33in;height:{rh}in;background:{NAVY}"></div>']
    for name,x,w,al in cols:
        parts.append(box(x,y0+off,w,f"text-align:{al}",f'<span style="font-size:11.5pt;font-weight:700;color:#fff">{esc(name)}</span>'))
    for i,c in enumerate(rows):
        y=y0+rh+i*rh
        if i%2==0: parts.append(f'<div style="position:absolute;left:0.5in;top:{y}in;width:12.33in;height:{rh}in;background:{TAN}"></div>')
        bs,bc,_=signed(c['us_bilateral_usd_b'])
        cells=[(esc(c['country']),INK,True),(money(c['gdp_usd_b']),INK,False),
               (money(c['us_exports_usd_b']),INK,False),(money(c['us_imports_usd_b']),INK,False),(bs,bc,True)]
        for (name,x,w,al),(val,col,bold) in zip(cols,cells):
            parts.append(box(x,y+off,w,f"text-align:{al}",
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
    subhtml=f'<span style="font-size:9.5pt;color:{GRAY};font-weight:400">&nbsp;&nbsp;{esc(sub)}</span>' if sub else ''
    return box(l,t,w,"",
        f'<div style="font-size:8.5pt;color:{GRAY};letter-spacing:.3px">{esc(label)}</div>'
        f'<div style="font-size:14.5pt;font-weight:700;color:{vcolor};margin-top:1pt">{value}{subhtml}</div>')

def left_panel(c):
    parts=[f'<div style="position:absolute;left:{LP_X}in;top:1.26in;width:{LP_W}in;height:5.70in;background:{TAN}"></div>',
           f'<div style="position:absolute;left:{LP_X}in;top:1.26in;width:{LP_W}in;height:0.045in;background:{GOLD}"></div>',
           box(LP_X+0.20,1.44,LP_W-0.4,"",f'<div style="font-size:10.5pt;font-weight:700;color:{BLUE};letter-spacing:1px">TRADE &amp; ECONOMY</div>')]
    lx=LP_X+0.20; lw=LP_W-0.40; ly=1.90; step=1.02
    gy,ty,oy=c['gdp_year'],c['us_trade_year'],c['overall_balance_year']
    us=c['country']=='United States'
    parts.append(datum(lx,ly,lw,f"NOMINAL GDP ({gy})",money(c['gdp_usd_b'])))
    obs,obc,obw=signed(c['overall_balance_usd_b'])
    basis='goods' if 'goods-only' in c['overall_balance_basis'] else ('g+s' if 'services' in c['overall_balance_basis'] else '')
    parts.append(datum(lx,ly+step,lw,f"OVERALL TRADE BALANCE ({oy})",obs,vcolor=INK,sub=(f"{obw} · {basis}" if c['overall_balance_usd_b'] is not None else None)))
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
    return (f'<span style="font-size:{max(8.0,size*0.78)}pt;color:{NEG};font-weight:700;font-style:italic"> · acting</span>'
            if o.get('is_acting') else '')

def portrait_html(o,l,t,h):
    if not o.get('portrait_file'): return ''
    return (f'<img src="{data_uri(o["portrait_file"])}" '
            f'style="position:absolute;left:{l}in;top:{t}in;height:{h}in;border:1pt solid {SLATE}">')

def full_profile(y,h,heading,o,notes_line):
    parts=[box(RX,y,RW,"",f'<div style="font-size:10.5pt;font-weight:700;color:{BLUE};letter-spacing:1.2px">{esc(heading)}</div>')]
    tx=RX; tw=RW
    if o.get('portrait_file'):
        pw=1.00*img_ar(o['portrait_file'])
        parts.append(f'<img src="{data_uri(o["portrait_file"])}" style="position:absolute;left:{RX}in;top:{y+0.28}in;height:1.00in;border:1pt solid {SLATE}">')
        tx=RX+pw+0.18; tw=RW-pw-0.18
    parts.append(box(tx,y+0.28,tw,"",f'<div style="font-size:14pt;font-weight:700;color:{NAVY}">{esc(o["name"])}{acting_html(o,14)}</div>'))
    parts.append(box(tx,y+0.58,tw,"",f'<div style="font-size:11pt;font-style:italic;color:{GRAY};line-height:1.15">{esc(o["title"])}</div>'))
    ao=f'&nbsp;&nbsp;· <span style="color:{MUTED};white-space:nowrap">Assumed office: {esc(fmt_date(o["assumed_office"]))}</span>' if o.get('assumed_office') else ''
    parts.append(box(tx,y+0.98,tw,"",f'<div style="font-size:9.5pt;color:{INK};line-height:1.15">{esc(o["ministry"])}{ao}</div>'))
    note=(f'<div style="margin-top:5pt;font-size:9pt;font-style:italic;color:{GRAY};line-height:1.2">{esc(notes_line)}</div>') if notes_line else ''
    parts.append(box(RX,y+1.34,RW,f"height:{h-1.34}in;overflow:hidden",
        f'<div style="font-family:\'Merriweather\',Cambria,Georgia,serif;font-size:10.5pt;color:{INK};line-height:1.35">{esc(o.get("bio_display") or o.get("bio",""))}</div>{note}'))
    return ''.join(parts)

def half_profile(x0,y,h,o):
    parts=[]
    tx=x0; tw=COL_W
    if o.get('portrait_file'):
        pw=0.80*img_ar(o['portrait_file'])
        parts.append(f'<img src="{data_uri(o["portrait_file"])}" style="position:absolute;left:{x0}in;top:{y+0.26}in;height:0.80in;border:1pt solid {SLATE}">')
        tx=x0+pw+0.14; tw=COL_W-pw-0.14
    tag=f'<div style="font-size:7.5pt;font-weight:700;color:{TEAL};letter-spacing:.8px">{esc(o["role_tag"])}</div>' if o.get('role_tag') else ''
    parts.append(box(tx,y+0.26,tw,f"height:1.00in;overflow:hidden",
        f'{tag}<div style="font-size:12pt;font-weight:700;color:{NAVY};margin-top:2pt">{esc(o["name"])}{acting_html(o,12)}</div>'
        f'<div style="font-size:9pt;font-style:italic;color:{GRAY};line-height:1.18;margin-top:2pt">{esc(o["title"])}</div>'))
    ao=f'&nbsp;· <span style="color:{MUTED};white-space:nowrap">{esc(fmt_date(o["assumed_office"]))}</span>' if o.get('assumed_office') else ''
    parts.append(box(x0,y+1.28,COL_W,"height:0.32in;overflow:hidden",
        f'<div style="font-size:8.5pt;color:{INK};line-height:1.18">{esc(o["ministry"])}{ao}</div>'))
    parts.append(box(x0,y+1.62,COL_W,f"height:{h-1.62}in;overflow:hidden",
        f'<div style="font-family:\'Merriweather\',Cambria,Georgia,serif;font-size:9.5pt;color:{INK};line-height:1.35">{esc(o.get("bio_display") or o.get("bio",""))}</div>'))
    return ''.join(parts)

def section(blk,heading,offs,div_note):
    y,h=blk
    shown=[o for o in offs if o.get('display') in ('full','half')]
    notes=[o for o in offs if o.get('display')=='note']
    notes_line='; '.join(f"{o['name']} ({o['title']})" for o in notes)
    if div_note: notes_line=div_note          # division note already names the other officials
    elif notes_line: notes_line='Also: '+notes_line
    if len(shown)>=2:
        head=box(RX,y,RW,"",f'<div style="font-size:10.5pt;font-weight:700;color:{BLUE};letter-spacing:1.2px">{esc(heading)}&nbsp;&nbsp;·&nbsp;&nbsp;SPLIT PORTFOLIO</div>')
        return head+half_profile(RX,y,h,shown[0])+half_profile(COL2_X,y,h,shown[1])
    elif len(shown)==1:
        return full_profile(y,h,heading,shown[0],notes_line)
    return box(RX,y,RW,"",f'<div style="font-size:10.5pt;font-weight:700;color:{BLUE}">{esc(heading)}</div><div style="font-size:13pt;color:{NEG};font-weight:700">[TO VERIFY]</div>')

def country_slide(c,idx):
    parts=[]
    fh=0.60; fw=fh*img_ar(c['flag_file'])
    parts.append(f'<img src="{data_uri(c["flag_file"])}" style="position:absolute;left:0.6in;top:0.36in;height:{fh}in;border:1pt solid {SLATE}">')
    parts.append(box(2.1,0.29,9.0,"height:0.75in;display:flex;align-items:center",
        f'<div style="font-size:27pt;font-weight:700;color:{NAVY}">{esc(c["country"])}</div>'))
    parts.append(f'<div style="position:absolute;left:0.6in;top:1.13in;width:12.13in;height:0.035in;background:{GOLD}"></div>')
    parts.append(left_panel(c))
    parts.append(section(BLK[0],"DIGITAL / TECHNOLOGY",c['digital_ministers'],c.get('div_note_digital')))
    parts.append(f'<div style="position:absolute;left:{RX}in;top:4.08in;width:{RW}in;height:1px;background:{TAN}"></div>')
    parts.append(section(BLK[1],"TRADE / COMMERCE",c['trade_ministers'],c.get('div_note_trade')))
    parts.append(footer(idx,19))
    S.append(f'<div class="slide">{"".join(parts)}</div>')

# ---------- BLOC ANNEX ----------
def bloc_slide(c):
    parts=[]
    fh=0.60; fw=fh*img_ar(c['flag_file'])
    parts.append(f'<img src="{data_uri(c["flag_file"])}" style="position:absolute;left:0.6in;top:0.36in;height:{fh}in;border:1pt solid {SLATE}">')
    parts.append(box(2.1,0.20,10.6,"height:0.60in;display:flex;align-items:center",
        f'<div style="font-size:26pt;font-weight:700;color:{NAVY}">{esc(c["country"])}'
        f'<span style="font-size:10.5pt;font-weight:700;color:{TEAL};letter-spacing:1px">&nbsp;&nbsp;&nbsp;·&nbsp;&nbsp;&nbsp;G20 BLOC MEMBER</span></div>'))
    facts='&nbsp;&nbsp;&nbsp;·&nbsp;&nbsp;&nbsp;'.join(f"{esc(f['label'])}: {esc(f['value'])}" for f in c.get('facts',[]))
    parts.append(box(2.1,0.83,10.6,"",f'<div style="font-size:9.5pt;color:{GRAY}">{facts}</div>'))
    parts.append(f'<div style="position:absolute;left:0.6in;top:1.13in;width:12.13in;height:0.035in;background:{GOLD}"></div>')
    parts.append(left_panel(c))
    if c.get('panel_note'):
        parts.append(box(LP_X+0.20,6.52,LP_W-0.4,"",f'<div style="font-size:7.5pt;font-style:italic;color:{GRAY};line-height:1.1">{esc(c["panel_note"])}</div>'))
    parts.append(section(BLK[0],"DIGITAL / TECHNOLOGY",c['digital_ministers'],c.get('div_note_digital')))
    parts.append(f'<div style="position:absolute;left:{RX}in;top:4.08in;width:{RW}in;height:1px;background:{TAN}"></div>')
    parts.append(section(BLK[1],"TRADE / COMMERCE",c['trade_ministers'],c.get('div_note_trade')))
    parts.append(footer("Bloc annex"))
    S.append(f'<div class="slide">{"".join(parts)}</div>')

# ---------- METHODOLOGY, SOURCES & NOTES (combined final slide) ----------
# Mirrors build_pptx.py: three equal tinted panels (top 1.26, bottom 6.96, gold
# top rule, heading at 1.44, bullets from 1.90) with metric-balanced spacing.
SRC_COLS=[
 ("SCOPE & METHODOLOGY",[
  ("19 members:","Argentina, Australia, Brazil, Canada, China, France, Germany, India, Indonesia, Italy, Japan, Mexico, Poland, Russia, Saudi Arabia, South Korea, Türkiye, United Kingdom, United States."),
  ("Substitution:","Poland is covered in place of South Africa — a deliberate substitution, not an omission."),
  ("Bloc members:","The European Union and African Union hold G20 seats as supranational blocs; both are profiled in the annex."),
  ("Ministers:","Each officeholder confirmed current on 2026-07-16 by live search plus an independent verification pass; split portfolios show every responsible official."),
  ("Figures:","USD billions throughout, one decimal. Positive balance = surplus (green); negative = deficit (orange)."),
 ]),
 ("DATASETS & VINTAGES",[
  (None,"GDP: IMF World Economic Outlook, Oct 2025 (2025 estimates, nominal USD), single vintage across all members."),
  (None,"U.S. bilateral goods trade: U.S. Census Bureau, full-year 2025, via USTR fact sheets and Census-derived series."),
  (None,"U.S. world totals: Census/BEA FT-900, December & Annual 2025 release."),
  (None,"Overall balances: national statistics offices / IMF, latest full year, goods basis unless noted."),
  (None,"EU & AU annex: IMF WEO, Eurostat, USTR, and official EU/AU sources."),
  (None,"Officeholders: official government sources and 2026-dated press, dual-verified 2026-07-16."),
 ]),
 ("DATA CAVEATS",[
  (None,"Australia's balance is goods+services; India's is fiscal year 2025-26. All others goods-only, calendar 2025."),
  (None,"Several balances are converted from local currency at ~2025 average rates; USD values carry exchange-rate uncertainty."),
  (None,"census.gov and imf.org were not directly reachable at build time; figures come from official-data-derived channels."),
  (None,"African Union: U.S. figures are U.S.–Africa goods totals (proxy); no continental goods balance is published (N/A)."),
  (None,"Acting officials: Argentina's domestic commerce portfolio and Saudi Arabia's GAFT governorship."),
  (None,"Full uncertainty register: output/GAPS.md."),
 ])]
SRC_PW=3.84; SRC_GAP=0.305; SRC_PX=[0.6+i*(SRC_PW+SRC_GAP) for i in range(3)]
SRC_INSET=0.22; SRC_CW=SRC_PW-2*SRC_INSET; SRC_PT_SZ=11

def src_nlines(text, pt, width_in):
    f=ImageFont.truetype('/usr/local/share/fonts/ita/OpenSans-Regular.ttf', round(pt*96/72))
    maxw=width_in*96; lines=1; cur=0.0; sp=f.getlength(' ')
    for word in text.split():
        wl=f.getlength(word)
        if cur==0: cur=wl
        elif cur+sp+wl<=maxw: cur+=sp+wl
        else: lines+=1; cur=wl
    return lines

def src_gaps():
    gaps=[]
    for _,items in SRC_COLS:
        total=sum(src_nlines("•  "+((lab+"  ") if lab else "")+txt, SRC_PT_SZ, SRC_CW)
                  for lab,txt in items)*SRC_PT_SZ*1.18/72
        g=(6.60-1.90-total)*72/max(1,len(items)-1)
        gaps.append(max(7.0,min(16.0,g)))
    return gaps

def sources_slide():
    parts=[]
    for px,(title,items),gap in zip(SRC_PX,SRC_COLS,src_gaps()):
        parts.append(f'<div style="position:absolute;left:{px}in;top:1.26in;width:{SRC_PW}in;height:5.70in;background:{TAN}"></div>')
        parts.append(f'<div style="position:absolute;left:{px}in;top:1.26in;width:{SRC_PW}in;height:0.045in;background:{GOLD}"></div>')
        parts.append(box(px+SRC_INSET,1.44,SRC_CW,"",
            f'<div style="font-size:10.5pt;font-weight:700;color:{BLUE};letter-spacing:1px">{esc(title)}</div>'))
        lis=[]
        for j,(lab,txt) in enumerate(items):
            mb=f"{gap}pt" if j<len(items)-1 else "0"
            labh=f'<b style="color:{NAVY}">{esc(lab)}</b>&nbsp;&nbsp;' if lab else ''
            lis.append(f'<div style="font-size:{SRC_PT_SZ}pt;color:{INK};margin-bottom:{mb};line-height:1.18">'
                       f'<span style="color:{GOLD};font-weight:700">•</span>&nbsp;&nbsp;{labh}{esc(txt)}</div>')
        parts.append(box(px+SRC_INSET,1.90,SRC_CW,"",''.join(lis)))
    S.append(f'<div class="slide">{header_bar("Methodology, Sources & Notes","scope · datasets · caveats · compiled 2026-07-16")}'
             f'{"".join(parts)}{footer()}</div>')

# ---- assemble ----
title_slide(); summary_slide(CO[:10],1,2); summary_slide(CO[10:],2,2)
for i,c in enumerate(CO,1): country_slide(c,i)
for b in D.get('blocs', []): bloc_slide(b)
sources_slide()

CSS=f"""<style>
@page{{size:13.333in 7.5in;margin:0}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Open Sans','Calibri','Liberation Sans',Arial,sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.slide{{position:relative;width:13.333in;height:7.5in;overflow:hidden;background:#fff;page-break-after:always}}
.slide:last-child{{page-break-after:auto}}
img{{object-fit:cover}}
</style>"""
doc=f"<!doctype html><html><head><meta charset='utf-8'>{CSS}</head><body>{''.join(S)}</body></html>"
open(ROOT+'output/_deck.html','w').write(doc)
print("Wrote output/_deck.html —",len(S),"slides,",len(doc)//1024,"KB (ITA style)")

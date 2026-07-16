#!/usr/bin/env python3
"""Build a print-ready HTML mirror of the deck (-> Chromium -> PDF) from data/g20.json.
Coordinates in inches mirror the python-pptx layout so PDF and PPTX match."""
import json, base64, html, os

D = json.load(open('/home/user/Photo/data/g20.json'))
CO = D['countries']; META = D['meta']
ROOT = '/home/user/Photo/'

NAVY="#1F3864"; SLATE="#44546A"; INK="#262626"; MUTED="#7F7F7F"; PANEL="#F3F5F9"
RULE="#D6DCE5"; POS="#1E7A34"; NEG="#B23330"; ACCENT="#2E5A88"
STEEL="#AEB9CF"; AMBER="#B97A00"; ORANGE="#C05A00"
BADGE={'Needs check':AMBER,'Vacant / acting':ORANGE,'Verified':POS}

def esc(t): return html.escape(str(t))
def money(v): return 'N/A' if v is None else f"${v:,.1f}B"
def signed(v):
    if v is None: return ('N/A', SLATE, '')
    w='surplus' if v>=0 else 'deficit'; s=f"{'+' if v>=0 else '−'}${abs(v):,.1f}B"
    return (s, POS if v>=0 else NEG, w)

_imgcache={}
def img_data(path):
    if path not in _imgcache:
        b=open(ROOT+path,'rb').read(); _imgcache[path]='data:image/png;base64,'+base64.b64encode(b).decode()
    return _imgcache[path]

S=[]  # slides html
def box(left,top,width,style="",inner="",height=None):
    h=f"height:{height}in;" if height is not None else ""
    return f'<div style="position:absolute;left:{left}in;top:{top}in;width:{width}in;{h}{style}">{inner}</div>'

# ---------- TITLE ----------
def title_slide():
    inner=[]
    inner.append(f'<div style="position:absolute;left:0;top:0;width:13.333in;height:0.28in;background:{ACCENT}"></div>')
    inner.append(f'<div style="position:absolute;left:0;bottom:0;width:13.333in;height:0.28in;background:{ACCENT}"></div>')
    inner.append(box(1.0,2.05,11.33,"",
        f'<div style="font-size:34pt;font-weight:700;color:#fff;line-height:1.1">G20 Countries: Digital &amp; Trade Ministers</div>'
        f'<div style="font-size:22pt;color:#C7D3E8;margin-top:6pt">with GDP and U.S. Bilateral Trade Profiles</div>'))
    inner.append(box(1.0,4.15,11.33,"",
        f'<div style="font-size:16pt;font-weight:700;color:#fff">Prepared for the International Trade Administration</div>'
        f'<div style="font-size:13pt;color:{STEEL};margin-top:5pt">U.S. Department of Commerce — Internal Reference</div>'
        f'<div style="font-size:13pt;color:{STEEL};margin-top:3pt">July 16, 2026</div>'))
    inner.append(box(1.0,6.05,11.33,"",
        f'<div style="font-size:11pt;color:#8F9EBE"><b>Data vintage:</b> Trade — U.S. Census goods, 2025 full year (goods basis). '
        f'GDP — IMF WEO, 2025. Ministers verified as current on 2026-07-16. Figures in USD billions unless noted.</div>'))
    S.append(f'<div class="slide" style="background:{NAVY}">{"".join(inner)}</div>')

# ---------- header bar (methodology/summary/sources) ----------
def header_bar(title,kicker):
    return (f'<div style="position:absolute;left:0;top:0;width:13.333in;height:1.0in;background:{NAVY}"></div>'
            f'<div style="position:absolute;left:0;top:1.0in;width:13.333in;height:0.06in;background:{ACCENT}"></div>'
            + box(0.6,0.20,12.13,"",f'<div style="font-size:24pt;font-weight:700;color:#fff">{esc(title)}</div>')
            + (box(0.6,0.68,12.13,"",f'<div style="font-size:11pt;color:#B9C5DC">{esc(kicker)}</div>') if kicker else ""))

# ---------- METHODOLOGY ----------
def methodology_slide():
    def b(label,text): return (f'<p style="margin:0 0 7pt 0;font-size:12.5pt;color:{INK};line-height:1.25">'
                               f'<b style="color:{NAVY}">{esc(label)}</b>&nbsp;&nbsp;{esc(text)}</p>')
    left=(b("Countries (19):","Argentina, Australia, Brazil, Canada, China, France, Germany, India, Indonesia, Italy, "
              "Japan, Mexico, Poland, Russia, Saudi Arabia, South Korea, Türkiye, United Kingdom, United States.")
          +b("Substitution:","Poland is included in place of South Africa, per instruction — a deliberate substitution, not an omission.")
          +b("Bloc seats excluded:","The European Union and African Union hold G20 seats but are supranational blocs, not sovereign countries, and are not profiled.")
          +b("GDP:","Nominal (current USD), IMF World Economic Outlook 2025, single vintage across all 19.")
          +b("U.S. bilateral trade:","U.S. Census Bureau goods trade, 2025 full year (goods basis), via Census-derived channels (see Sources).")
          +b("Ministers:","Each officeholder confirmed current on 2026-07-16 by live search plus an independent verification pass. Split portfolios show every responsible official."))
    flags=""
    for lab,desc,col in [("Verified","independently confirmed current",POS),
                         ("Needs check","a figure or minister carries uncertainty",AMBER),
                         ("Vacant / acting","post held on an acting/interim basis",ORANGE)]:
        flags+=(f'<div style="margin-top:9pt"><span style="color:{col};font-weight:700">■</span> '
                f'<b style="color:{INK}">{lab}</b><div style="font-size:10.5pt;color:{SLATE}">{desc}</div></div>')
    panel=(f'<div style="position:absolute;left:8.5in;top:1.5in;width:4.23in;height:5.25in;background:{PANEL}"></div>'
           f'<div style="position:absolute;left:8.5in;top:1.5in;width:4.23in;height:0.04in;background:{ACCENT}"></div>'
           +box(8.8,1.72,3.7,"",
               f'<div style="font-size:11pt;font-weight:700;color:{NAVY};letter-spacing:1px">CONFIDENCE FLAGS</div>{flags}'
               f'<div style="margin-top:14pt;font-size:10.5pt;color:{SLATE}"><b>Roll-up this deck:</b> 12 Verified · 5 Needs check · 2 Acting.</div>'
               f'<div style="margin-top:10pt;font-size:10.5pt;color:{SLATE};font-style:italic">Nothing is filled from model memory; unconfirmed items are flagged, not guessed.</div>'))
    S.append(f'<div class="slide">{header_bar("Methodology & Scope","19 G20 sovereign members · compiled 2026-07-16")}'
             f'{box(0.6,1.35,7.5,"",left)}{panel}</div>')

# ---------- SUMMARY ----------
def summary_slide(rows,part,total):
    cols=[("Country",0.6,3.4,'left'),("GDP (2025)",4.0,2.0,'right'),
          ("U.S. exports to",6.05,2.2,'right'),("U.S. imports from",8.30,2.3,'right'),
          ("U.S. bilateral balance",10.65,2.08,'right')]
    y0=1.45; rh=0.50
    parts=[f'<div style="position:absolute;left:0.5in;top:{y0}in;width:12.33in;height:{rh}in;background:{NAVY}"></div>']
    for name,x,w,al in cols:
        parts.append(box(x,y0+0.13,w,f"text-align:{al}",f'<span style="font-size:11.5pt;font-weight:700;color:#fff">{esc(name)}</span>'))
    for i,c in enumerate(rows):
        y=y0+rh+i*rh
        if i%2==0: parts.append(f'<div style="position:absolute;left:0.5in;top:{y}in;width:12.33in;height:{rh}in;background:{PANEL}"></div>')
        bs,bc,_=signed(c['us_bilateral_usd_b'])
        cells=[(esc(c['country']),INK,True),(money(c['gdp_usd_b']),INK,False),
               (money(c['us_exports_usd_b']),INK,False),(money(c['us_imports_usd_b']),INK,False),(bs,bc,True)]
        for (name,x,w,al),(val,col,bold) in zip(cols,cells):
            fw='700' if bold else '400'
            parts.append(box(x,y+0.12,w,f"text-align:{al}",f'<span style="font-size:11.5pt;color:{col};font-weight:{fw}">{val}</span>'))
    note=box(0.5,7.06,12.33,"",f'<div style="font-size:9pt;color:{MUTED};font-style:italic">Negative U.S. bilateral balance = U.S. goods deficit (red); positive = U.S. surplus (green). United States shown as N/A for bilateral columns.</div>')
    S.append(f'<div class="slide">{header_bar("Summary — GDP & U.S. Bilateral Goods Trade",f"USD billions · GDP 2025 · trade 2025 (goods) · part {part} of {total}")}{"".join(parts)}{note}</div>')

# ---------- COUNTRY ----------
def datum(left,top,w,label,value,vcolor=NAVY,sub=None):
    subhtml=f'<span style="font-size:10pt;color:{SLATE};font-weight:400">&nbsp;&nbsp;{esc(sub)}</span>' if sub else ''
    return box(left,top,w,"",
        f'<div style="font-size:9.5pt;color:{SLATE};letter-spacing:.3px">{esc(label)}</div>'
        f'<div style="font-size:15pt;font-weight:700;color:{vcolor};margin-top:1pt">{value}{subhtml}</div>')

def minister_block(left,top,w,h,heading,prim,div_note):
    head_html=f'<div style="font-size:11pt;font-weight:700;color:{ACCENT};letter-spacing:1px">{heading}</div>'
    if not prim:
        body=f'<div style="margin-top:6pt;font-size:13pt;color:{AMBER};font-weight:700">[TO VERIFY]</div>'
        return box(left,top,w,f"height:{h}in;overflow:hidden",head_html+body)
    acting=(f'<span style="font-size:11pt;color:{ORANGE};font-weight:700;font-style:italic"> · acting</span>' if prim.get('is_acting') else '')
    ao=prim.get('assumed_office','')
    aos=(f'<span style="color:{MUTED}">&nbsp;&nbsp;·&nbsp;&nbsp;Assumed office: {esc(ao)}</span>' if ao else '')
    note=(f'<div style="margin-top:6pt;font-size:9.5pt;font-style:italic;color:{SLATE};line-height:1.2">'
          f'<b style="color:{ACCENT}">Division of responsibility:</b> {esc(div_note)}</div>') if div_note else ''
    body=(f'<div style="margin-top:5pt;font-size:14.5pt;font-weight:700;color:{NAVY}">{esc(prim["name"])}{acting}</div>'
          f'<div style="margin-top:2pt;font-size:11pt;font-style:italic;color:{SLATE};line-height:1.15">{esc(prim["title"])}</div>'
          f'<div style="margin-top:4pt;font-size:10pt;color:{INK};line-height:1.2">{esc(prim["ministry"])}{aos}</div>'
          f'<div style="margin-top:6pt;font-size:11pt;color:{INK};line-height:1.28">{esc(prim.get("bio",""))}</div>'
          f'{note}')
    return box(left,top,w,f"height:{h}in;overflow:hidden",head_html+body)

def country_slide(c,idx):
    parts=[]
    ar=img_data(c['flag_file'])
    parts.append(f'<img src="{ar}" style="position:absolute;left:0.6in;top:0.40in;height:0.60in;border:0.75pt solid {RULE}">')
    parts.append(box(2.1,0.30,8.0,"height:0.78in;display:flex;align-items:center",
        f'<div style="font-size:28pt;font-weight:700;color:{NAVY}">{esc(c["country"])}</div>'))
    flag=c['row_confidence']
    if flag!='Verified':
        parts.append(f'<div style="position:absolute;left:10.23in;top:0.44in;width:2.5in;height:0.44in;background:{BADGE[flag]};'
                     f'display:flex;align-items:center;justify-content:center"><span style="font-size:11pt;font-weight:700;color:#fff">{flag.upper()}</span></div>')
    parts.append(f'<div style="position:absolute;left:0.6in;top:1.18in;width:12.13in;height:1.5pt;background:{NAVY}"></div>')
    # left panel
    parts.append(f'<div style="position:absolute;left:0.6in;top:1.42in;width:3.5in;height:5.35in;background:{PANEL}"></div>')
    parts.append(f'<div style="position:absolute;left:0.6in;top:1.42in;width:3.5in;height:0.04in;background:{ACCENT}"></div>')
    parts.append(box(0.82,1.60,3.1,"",f'<div style="font-size:11pt;font-weight:700;color:{NAVY};letter-spacing:1px">TRADE &amp; ECONOMY</div>'))
    lx,ly,lw,step=0.82,2.02,3.06,0.96
    gy,ty,oy=c['gdp_year'],c['us_trade_year'],c['overall_balance_year']
    parts.append(datum(lx,ly,lw,f"NOMINAL GDP ({gy})",money(c['gdp_usd_b'])))
    obs,obc,obw=signed(c['overall_balance_usd_b'])
    basis='goods' if 'goods-only' in c['overall_balance_basis'] else ('g+s' if 'services' in c['overall_balance_basis'] else '')
    parts.append(datum(lx,ly+step,lw,f"OVERALL TRADE BALANCE ({oy})",obs,vcolor=INK,sub=f"{obw} · {basis}"))
    parts.append(datum(lx,ly+2*step,lw,f"U.S. GOODS EXPORTS TO ({ty})",money(c['us_exports_usd_b'])))
    parts.append(datum(lx,ly+3*step,lw,f"U.S. GOODS IMPORTS FROM ({ty})",money(c['us_imports_usd_b'])))
    bs,bc,bw=signed(c['us_bilateral_usd_b'])
    parts.append(datum(lx,ly+4*step,lw,f"U.S. BILATERAL BALANCE ({ty})",bs,vcolor=bc,sub=bw))
    # right blocks
    rx,rw=4.5,8.23
    dprim=next((o for o in c['digital_ministers'] if o['is_primary']),None)
    tprim=next((o for o in c['trade_ministers'] if o['is_primary']),None)
    def others(offs,bespoke):
        if bespoke: return bespoke
        extra=[o for o in offs if not o['is_primary']]
        return ("also "+'; '.join(f'{o["name"]} ({o["title"]})' for o in extra)) if extra else ''
    parts.append(minister_block(rx,1.26,rw,2.82,"DIGITAL / TECHNOLOGY MINISTER",dprim,others(c['digital_ministers'],c.get('div_note_digital'))))
    parts.append(f'<div style="position:absolute;left:{rx}in;top:4.11in;width:{rw}in;height:1px;background:{RULE}"></div>')
    parts.append(minister_block(rx,4.14,rw,2.82,"TRADE / COMMERCE MINISTER",tprim,others(c['trade_ministers'],c.get('div_note_trade'))))
    # footer
    parts.append(f'<div style="position:absolute;left:0.6in;top:7.0in;width:12.13in;height:1px;background:{RULE}"></div>')
    parts.append(box(0.6,7.06,10.5,"",f'<div style="font-size:8pt;color:{MUTED}"><b>Sources:</b> GDP — IMF WEO 2025 · U.S. goods trade — U.S. Census 2025 · ministers verified 2026-07-16. See Sources &amp; Caveats slide.</div>'))
    parts.append(box(11.6,7.06,1.13,"text-align:right",f'<div style="font-size:8pt;color:{MUTED}">{idx} / 19</div>'))
    S.append(f'<div class="slide">{"".join(parts)}</div>')

# ---------- SOURCES ----------
def sources_slide():
    def head(t): return f'<div style="font-size:12pt;font-weight:700;color:{NAVY};letter-spacing:.5px;margin:10pt 0 3pt 0">{esc(t)}</div>'
    def li(t,col=ACCENT): return f'<div style="font-size:10.3pt;color:{INK};margin-bottom:2pt;line-height:1.2"><span style="color:{col}">•</span>&nbsp;&nbsp;{t}</div>'
    left=(head("DATASETS & VINTAGES")
        +li("GDP (nominal, current USD): IMF World Economic Outlook, Oct 2025 (2025 estimates), via StatisticsTimes tabulation.")
        +li("U.S. bilateral goods trade: U.S. Census Bureau, full-year 2025, via USTR country fact sheets and the Census/UN-COMTRADE series (Trading Economics mirror).")
        +li("Overall trade balances: national statistics offices / IMF, latest full year, goods basis unless noted.")
        +li("Flags: hampusborgos/country-flags (public domain); Wikimedia Commons was egress-blocked in the build environment.")
        +head("BASIS & CONVERSION")
        +li("Australia's overall balance is goods+services; India's is fiscal year 2025-26. All others goods-only, calendar 2025.")
        +li("Several overall balances are converted from local currency (EUR/GBP/CAD/AUD/JPY/SAR) at ~2025 average rates; USD values carry exchange-rate uncertainty.")
        +li("census.gov, imf.org and many national sites returned HTTP 403 to automated fetching; figures came from official-data-derived channels, not read off the primary page."))
    nc=""
    for c in CO:
        if c['row_confidence']=='Needs check':
            nc+=li(f'<b>{esc(c["country"])}:</b> <span style="color:{SLATE}">{esc("; ".join(c["gaps"][:2]))}</span>',AMBER)
    va=""
    for c in CO:
        if c['row_confidence']=='Vacant / acting':
            actor=next((f'{o["name"]} — {o["title"]}' for o in c['trade_ministers']+c['digital_ministers'] if o.get('is_acting')),'')
            va+=li(f'<b>{esc(c["country"])}:</b> <span style="color:{SLATE}">{esc(actor)}</span>',ORANGE)
    right=(head("FLAGGED — NEEDS CHECK")+nc
        +head("FLAGGED — VACANT / ACTING")+va
        +head("DATA-QUALITY CORRECTION")
        +li(f'<span style="color:{SLATE}">Saudi Arabia\'s raw trade-officials list wrongly included the U.S. Commerce Secretary and USTR (context bleed); removed and corrected.</span>')
        +head("SCOPE NOTE")
        +li(f'<span style="color:{SLATE}">Poland substituted for South Africa. EU and AU are G20 members but are bloc seats, not covered here.</span>'))
    foot=box(0.6,7.07,12.13,"",f'<div style="font-size:8.5pt;color:{MUTED};font-style:italic">Full per-country sourcing with URLs and as-of dates: research/g20-research.md · gaps register: output/GAPS.md</div>')
    S.append(f'<div class="slide">{header_bar("Sources & Caveats","datasets, vintages, and flagged uncertainties")}'
             f'{box(0.6,1.28,6.05,"",left)}{box(6.95,1.28,5.8,"",right)}{foot}</div>')

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
</style>"""
doc=f"<!doctype html><html><head><meta charset='utf-8'>{CSS}</head><body>{''.join(S)}</body></html>"
open('/home/user/Photo/output/_deck.html','w').write(doc)
print("Wrote output/_deck.html —", len(S), "slides,", len(doc)//1024, "KB")

#!/usr/bin/env python3
"""Build output/g20-ministers-trade-deck.pptx from data/g20.json (v2 layout:
official ITA/DOC framing, portraits, split-portfolio two-column sections)."""
import json, os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image

ROOT = '/home/user/Photo/'
D = json.load(open(ROOT + 'data/g20.json'))
CO = D['countries']; META = D['meta']
SEAL = META.get('seal_file') if META.get('seal_file') and os.path.exists(ROOT + META.get('seal_file', '')) else None

NAVY=RGBColor(0x1F,0x38,0x64); SLATE=RGBColor(0x44,0x54,0x6A); INK=RGBColor(0x26,0x26,0x26)
MUTED=RGBColor(0x7F,0x7F,0x7F); WHITE=RGBColor(0xFF,0xFF,0xFF); PANEL=RGBColor(0xF3,0xF5,0xF9)
RULE=RGBColor(0xD6,0xDC,0xE5); POS=RGBColor(0x1E,0x7A,0x34); NEG=RGBColor(0xB2,0x33,0x30)
ACCENT=RGBColor(0x2E,0x5A,0x88); STEEL=RGBColor(0xAE,0xB9,0xCF); ORANGE=RGBColor(0xC0,0x5A,0x00)

prs = Presentation()
prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
SW, SH = 13.333, 7.5

def slide(): return prs.slides.add_slide(BLANK)

def rect(s,x,y,w,h,fill=None,line=None,line_w=0.75):
    sp=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,Inches(x),Inches(y),Inches(w),Inches(h))
    sp.shadow.inherit=False
    if fill is None: sp.fill.background()
    else: sp.fill.solid(); sp.fill.fore_color.rgb=fill
    if line is None: sp.line.fill.background()
    else: sp.line.color.rgb=line; sp.line.width=Pt(line_w)
    return sp

def hline(s,x,y,w,color=RULE,weight=1.0):
    ln=s.shapes.add_connector(2,Inches(x),Inches(y),Inches(x+w),Inches(y))
    ln.line.color.rgb=color; ln.line.width=Pt(weight); ln.shadow.inherit=False

def tb(s,x,y,w,h,anchor=MSO_ANCHOR.TOP,wrap=True):
    b=s.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h)); tf=b.text_frame
    tf.word_wrap=wrap; tf.vertical_anchor=anchor
    tf.margin_left=0; tf.margin_right=0; tf.margin_top=0; tf.margin_bottom=0
    return tf

def para(tf,first=False):
    return tf.paragraphs[0] if first and not tf.paragraphs[0].runs else tf.add_paragraph()

def run(p,text,size,color=INK,bold=False,italic=False,spacing=None):
    r=p.add_run(); r.text=text; f=r.font
    f.size=Pt(size); f.bold=bold; f.italic=italic; f.name='Calibri'; f.color.rgb=color
    if spacing is not None:
        rPr=r._r.get_or_add_rPr(); rPr.set('spc',str(int(spacing*100)))
    return r

def money(v): return 'N/A' if v is None else f"${v:,.1f}B"
def signed(v):
    if v is None: return ('N/A', SLATE, '')
    return (f"{'+' if v>=0 else '−'}${abs(v):,.1f}B", POS if v>=0 else NEG,
            'surplus' if v>=0 else 'deficit')

_AR={}
def img_ar(path):
    if path not in _AR:
        im=Image.open(ROOT+path); _AR[path]=im.width/im.height
    return _AR[path]

def pic(s,path,x,y,h):
    s.shapes.add_picture(ROOT+path,Inches(x),Inches(y),height=Inches(h))
    return h*img_ar(path)

def footer(s, idx=None, total=None):
    hline(s,0.6,6.98,12.13,color=RULE)
    x=0.6
    if SEAL:
        w=pic(s,SEAL,0.6,7.06,0.34); x=0.6+w+0.14
    tf=tb(s,x,7.05,10.3,0.4)
    p=para(tf,True)
    run(p,"INTERNATIONAL TRADE ADMINISTRATION · U.S. DEPARTMENT OF COMMERCE",7.5,SLATE,bold=True,spacing=0.5)
    p2=tf.add_paragraph()
    run(p2,"GDP — IMF WEO 2025 · U.S. goods trade — U.S. Census 2025 · officeholders verified 2026-07-16",7.5,MUTED)
    if idx is not None:
        tp=tb(s,11.6,7.10,1.13,0.3); p=para(tp,True); p.alignment=PP_ALIGN.RIGHT
        run(p,f"{idx} / {total}",8,MUTED)

# ============ TITLE ============
def title_slide():
    s=slide(); rect(s,0,0,SW,SH,fill=NAVY)
    rect(s,0,0,SW,0.22,fill=ACCENT); rect(s,0,SH-0.22,SW,0.22,fill=ACCENT)
    y=1.05
    if SEAL:
        w=1.35*img_ar(SEAL)
        pic(s,SEAL,(SW-w)/2,y,1.35); y+=1.55
    else:
        y+=0.5
    tf=tb(s,1.0,y,11.33,0.85)
    for i,(t,sz,col,sp) in enumerate([("U.S. DEPARTMENT OF COMMERCE",13,STEEL,2.0),
                                       ("INTERNATIONAL TRADE ADMINISTRATION",17,WHITE,2.5)]):
        p=para(tf,i==0); p.alignment=PP_ALIGN.CENTER; p.space_after=Pt(4)
        run(p,t,sz,col,bold=(i==1),spacing=sp)
    tf2=tb(s,1.0,y+1.05,11.33,1.5)
    p=para(tf2,True); p.alignment=PP_ALIGN.CENTER
    run(p,"G20 Countries: Digital & Trade Ministers",32,WHITE,bold=True)
    p2=tf2.add_paragraph(); p2.alignment=PP_ALIGN.CENTER; p2.space_before=Pt(6)
    run(p2,"with GDP and U.S. Bilateral Trade Profiles",19,RGBColor(0xC7,0xD3,0xE8))
    tf3=tb(s,1.0,y+2.75,11.33,0.4)
    p=para(tf3,True); p.alignment=PP_ALIGN.CENTER
    run(p,"July 16, 2026 · Internal Reference",12.5,STEEL)
    tf4=tb(s,1.6,6.55,10.13,0.6)
    p=para(tf4,True); p.alignment=PP_ALIGN.CENTER
    run(p,"Data vintage: Trade — U.S. Census goods, 2025 full year (goods basis) · GDP — IMF WEO, 2025 · "
          "Officeholders verified as current on 2026-07-16 · USD billions unless noted",10,RGBColor(0x8F,0x9E,0xBE))

# ============ SHARED HEADER ============
def header_bar(s,title,kicker=None):
    rect(s,0,0,SW,1.0,fill=NAVY); rect(s,0,1.0,SW,0.06,fill=ACCENT)
    x=0.6
    if SEAL:
        w=pic(s,SEAL,0.6,0.22,0.56); x=0.6+w+0.20
    tf=tb(s,x,0.16,12.73-x,0.72,anchor=MSO_ANCHOR.MIDDLE)
    p=para(tf,True); run(p,title,24,WHITE,bold=True)
    if kicker:
        tfk=tb(s,x,0.70,12.0,0.3); pk=para(tfk,True); run(pk,kicker,11,RGBColor(0xB9,0xC5,0xDC))

def bullet(tf,label,text,first=False):
    p=para(tf,first); p.space_after=Pt(7)
    if label: run(p,label+"  ",12.5,NAVY,bold=True)
    run(p,text,12.5,INK)

# ============ METHODOLOGY ============
def methodology_slide():
    s=slide(); rect(s,0,0,SW,SH,fill=WHITE)
    header_bar(s,"Methodology & Scope","19 G20 sovereign members · compiled 2026-07-16")
    tf=tb(s,0.6,1.35,7.5,5.4)
    bullet(tf,"Countries (19):","Argentina, Australia, Brazil, Canada, China, France, Germany, India, "
        "Indonesia, Italy, Japan, Mexico, Poland, Russia, Saudi Arabia, South Korea, Türkiye, "
        "United Kingdom, United States.",first=True)
    bullet(tf,"Substitution:","Poland is covered in place of South Africa — a deliberate substitution, not an omission.")
    bullet(tf,"Bloc seats excluded:","The European Union and African Union hold G20 seats but are "
        "supranational blocs, not sovereign countries, and are not profiled.")
    bullet(tf,"GDP:","Nominal (current USD), IMF World Economic Outlook 2025, single vintage across all 19.")
    bullet(tf,"U.S. bilateral trade:","U.S. Census Bureau goods trade, 2025 full year (goods basis), "
        "via Census-derived channels (see Sources).")
    bullet(tf,"Ministers:","Each officeholder confirmed current on 2026-07-16 by live search plus an "
        "independent verification pass. Where a portfolio is split, both responsible officials are profiled.")
    rect(s,8.5,1.5,4.23,5.1,fill=PANEL)
    hline(s,8.5,1.5,4.23,color=ACCENT,weight=3)
    tp=tb(s,8.8,1.75,3.7,4.7)
    p=para(tp,True); run(p,"ABOUT THIS DOCUMENT",11,NAVY,bold=True,spacing=1.0)
    for t in ["Prepared within the International Trade Administration, U.S. Department of Commerce, as an internal reference.",
              "One structured dataset generates this deck, the companion workbook, and the PDF, so figures cannot drift between formats.",
              "Portraits are official government photos; a monogram placeholder marks any still to be supplied.",
              "Data caveats, acting officials, and items pending confirmation are tracked in a separate gaps register (GAPS.md) rather than flagged on slides."]:
        p=tp.add_paragraph(); p.space_before=Pt(10); run(p,t,10.5,SLATE)
    footer(s)

# ============ SUMMARY ============
def summary_slide(rows, part, total):
    s=slide(); rect(s,0,0,SW,SH,fill=WHITE)
    header_bar(s,"Summary — GDP & U.S. Bilateral Goods Trade",
               f"USD billions · GDP 2025 · trade 2025 (goods) · part {part} of {total}")
    cols=[("Country",0.6,3.4,'l'),("GDP (2025)",4.0,2.0,'r'),
          ("U.S. exports to",6.05,2.2,'r'),("U.S. imports from",8.30,2.3,'r'),
          ("U.S. bilateral balance",10.65,2.1,'r')]
    y0=1.40; rh=0.485
    rect(s,0.5,y0,12.33,rh,fill=NAVY)
    for name,x,w,al in cols:
        tf=tb(s,x,y0+0.06,w,rh-0.1,anchor=MSO_ANCHOR.MIDDLE)
        p=para(tf,True); p.alignment=PP_ALIGN.RIGHT if al=='r' else PP_ALIGN.LEFT
        run(p,name,11.5,WHITE,bold=True)
    for i,c in enumerate(rows):
        y=y0+rh+i*rh
        if i%2==0: rect(s,0.5,y,12.33,rh,fill=PANEL)
        bs,bc,_=signed(c['us_bilateral_usd_b'])
        vals=[(c['country'],INK,True),(money(c['gdp_usd_b']),INK,False),
              (money(c['us_exports_usd_b']),INK,False),(money(c['us_imports_usd_b']),INK,False),(bs,bc,True)]
        for (name,x,w,al),(val,col,bold) in zip(cols,vals):
            tf=tb(s,x,y+0.05,w,rh-0.08,anchor=MSO_ANCHOR.MIDDLE)
            p=para(tf,True); p.alignment=PP_ALIGN.RIGHT if al=='r' else PP_ALIGN.LEFT
            run(p,val,11.5,col,bold=bold)
    tf=tb(s,0.5,y0+rh+len(rows)*rh+0.08,12.33,0.34)
    p=para(tf,True)
    run(p,"Negative U.S. bilateral balance = U.S. goods deficit; positive = U.S. surplus. Bilateral columns measure "
          "trade with the United States, so the U.S. row shows N/A — the U.S. country page reports world totals.",9,MUTED,italic=True)
    footer(s)

# ============ COUNTRY ============
LP_X, LP_W = 0.6, 3.10
RX, RW = 3.95, 8.78
COL_W = 4.21; COL2_X = RX + COL_W + 0.36
BLK = [(1.26, 2.82), (4.14, 2.82)]  # (y, h) digital / trade

def datum(s,x,y,w,label,value,vcolor=NAVY,sub=None):
    tf=tb(s,x,y,w,0.8)
    p=para(tf,True); run(p,label,9,SLATE,spacing=0.3)
    p2=tf.add_paragraph(); p2.space_before=Pt(1); run(p2,value,14.5,vcolor,bold=True)
    if sub: run(p2,"  "+sub,9.5,SLATE)

def left_panel(s,c):
    rect(s,LP_X,1.42,LP_W,5.35,fill=PANEL)
    hline(s,LP_X,1.42,LP_W,color=ACCENT,weight=3)
    tf=tb(s,LP_X+0.20,1.58,LP_W-0.4,0.3)
    p=para(tf,True); run(p,"TRADE & ECONOMY",10.5,NAVY,bold=True,spacing=1.0)
    lx=LP_X+0.20; lw=LP_W-0.40; ly=1.98; step=0.96
    gy,ty,oy=c['gdp_year'],c['us_trade_year'],c['overall_balance_year']
    us = c['country']=='United States'
    datum(s,lx,ly,lw,f"NOMINAL GDP ({gy})",money(c['gdp_usd_b']))
    obs,obc,obw=signed(c['overall_balance_usd_b'])
    basis='goods' if 'goods-only' in c['overall_balance_basis'] else ('g+s' if 'services' in c['overall_balance_basis'] else '')
    datum(s,lx,ly+step,lw,f"OVERALL TRADE BALANCE ({oy})",obs,vcolor=INK,sub=f"{obw} · {basis}")
    if us and c.get('us_world_exports_b') is not None:
        datum(s,lx,ly+2*step,lw,f"GOODS EXPORTS — WORLD ({ty})",money(c['us_world_exports_b']))
        datum(s,lx,ly+3*step,lw,f"GOODS IMPORTS — WORLD ({ty})",money(c['us_world_imports_b']))
        ws,wc,ww=signed(c['us_world_balance_b'])
        datum(s,lx,ly+4*step,lw,f"GOODS BALANCE — WORLD ({ty})",ws,vcolor=wc,sub=ww)
    else:
        datum(s,lx,ly+2*step,lw,f"U.S. GOODS EXPORTS TO ({ty})",money(c['us_exports_usd_b']))
        datum(s,lx,ly+3*step,lw,f"U.S. GOODS IMPORTS FROM ({ty})",money(c['us_imports_usd_b']))
        bs,bc,bw=signed(c['us_bilateral_usd_b'])
        datum(s,lx,ly+4*step,lw,f"U.S. BILATERAL BALANCE ({ty})",bs,vcolor=bc,sub=bw)

def acting_run(p,o,size=11.0):
    if o.get('is_acting'): run(p,"  · acting",max(8.0,size*0.78),ORANGE,bold=True,italic=True)

def full_profile(s,y,h,heading,o,notes_line):
    tf=tb(s,RX,y,RW,0.24)
    p=para(tf,True); run(p,heading,10.5,ACCENT,bold=True,spacing=1.2)
    if o.get('portrait_file'):
        w=pic(s,o['portrait_file'],RX,y+0.30,1.19)
        rect(s,RX,y+0.30,w,1.19,line=RULE,line_w=0.75)
    tx=RX+1.12; tw=RW-1.12
    tf=tb(s,tx,y+0.30,tw,0.30)
    p=para(tf,True); run(p,o['name'],14,NAVY,bold=True); acting_run(p,o,14)
    tf=tb(s,tx,y+0.62,tw,0.46)
    p=para(tf,True); p.line_spacing=1.05; run(p,o['title'],11,SLATE,italic=True)
    tf=tb(s,tx,y+1.10,tw,0.38)
    p=para(tf,True); p.line_spacing=1.05
    run(p,o['ministry'],9.5,INK)
    if o.get('assumed_office'): run(p,f"   ·   Assumed office: {o['assumed_office']}",9.5,MUTED)
    tf=tb(s,RX,y+1.56,RW,h-1.56)
    p=para(tf,True); p.line_spacing=1.03; run(p,o.get('bio_display') or o.get('bio',''),11,INK)
    if notes_line:
        pn=tf.add_paragraph(); pn.space_before=Pt(5)
        run(pn,"Also: ",9,ACCENT,bold=True,italic=True); run(pn,notes_line,9,SLATE,italic=True)

def half_profile(s,x0,y,h,o):
    if o.get('portrait_file'):
        w=pic(s,o['portrait_file'],x0,y+0.28,1.00)
        rect(s,x0,y+0.28,w,1.00,line=RULE,line_w=0.75)
    tx=x0+0.92; tw=COL_W-0.92
    tf=tb(s,tx,y+0.28,tw,1.26)
    p=para(tf,True)
    if o.get('role_tag'): run(p,o['role_tag'],7.5,ACCENT,bold=True,spacing=0.8)
    p2=tf.add_paragraph(); p2.space_before=Pt(2)
    run(p2,o['name'],12,NAVY,bold=True); acting_run(p2,o,12)
    p3=tf.add_paragraph(); p3.space_before=Pt(2); p3.line_spacing=1.04
    run(p3,o['title'],9,SLATE,italic=True)
    tf=tb(s,x0,y+1.38,COL_W,0.34)
    p=para(tf,True); p.line_spacing=1.04
    run(p,o['ministry'],8.5,INK)
    if o.get('assumed_office'): run(p,f"  ·  {o['assumed_office']}",8.5,MUTED)
    tf=tb(s,x0,y+1.74,COL_W,h-1.74)
    p=para(tf,True); p.line_spacing=1.04
    run(p,o.get('bio_display') or o.get('bio',''),10.5,INK)

def section(s,blk,heading,offs,div_note):
    y,h=blk
    shown=[o for o in offs if o.get('display') in ('full','half')]
    notes=[o for o in offs if o.get('display')=='note']
    notes_line='; '.join(f"{o['name']} ({o['title']})" for o in notes)
    if div_note and notes_line: notes_line=div_note+' Also: '+notes_line
    elif div_note: notes_line=div_note
    elif notes_line: notes_line='Also: '+notes_line
    if len(shown)>=2:
        tf=tb(s,RX,y,RW,0.24)
        p=para(tf,True); run(p,heading+"  ·  SPLIT PORTFOLIO",10.5,ACCENT,bold=True,spacing=1.2)
        half_profile(s,RX,y,h,shown[0])
        half_profile(s,COL2_X,y,h,shown[1])
    elif len(shown)==1:
        full_profile(s,y,h,heading,shown[0],notes_line)
    else:
        tf=tb(s,RX,y,RW,0.5)
        p=para(tf,True); run(p,heading,10.5,ACCENT,bold=True,spacing=1.2)
        p2=tf.add_paragraph(); run(p2,"[TO VERIFY]",13,ORANGE,bold=True)

def country_slide(c,idx):
    s=slide(); rect(s,0,0,SW,SH,fill=WHITE)
    fh=0.60
    w=pic(s,c['flag_file'],0.6,0.40,fh)
    rect(s,0.6,0.40,w,fh,line=RULE,line_w=0.75)
    tf=tb(s,2.1,0.33,9.0,0.75,anchor=MSO_ANCHOR.MIDDLE)
    p=para(tf,True); run(p,c['country'],28,NAVY,bold=True)
    hline(s,0.6,1.18,12.13,color=NAVY,weight=1.5)
    left_panel(s,c)
    section(s,BLK[0],"DIGITAL / TECHNOLOGY",c['digital_ministers'],c.get('div_note_digital'))
    hline(s,RX,4.08,RW,color=RULE)
    section(s,BLK[1],"TRADE / COMMERCE",c['trade_ministers'],c.get('div_note_trade'))
    footer(s,idx,19)

# ============ SOURCES ============
def sources_slide():
    s=slide(); rect(s,0,0,SW,SH,fill=WHITE)
    header_bar(s,"Sources & Notes","datasets, vintages, and measurement notes")
    L=tb(s,0.6,1.3,6.05,5.4)
    def head(tf,t,first=False):
        p=para(tf,first); p.space_before=Pt(0 if first else 10); p.space_after=Pt(3)
        run(p,t,12,NAVY,bold=True,spacing=0.6)
    def li(tf,t):
        p=tf.add_paragraph(); p.space_after=Pt(2); run(p,"•  ",10.5,ACCENT); run(p,t,10.5,INK)
    head(L,"DATASETS & VINTAGES",first=True)
    li(L,"GDP (nominal, current USD): IMF World Economic Outlook, Oct 2025 (2025 estimates), via StatisticsTimes tabulation.")
    li(L,"U.S. bilateral goods trade: U.S. Census Bureau, full-year 2025, via USTR country fact sheets and the Census/UN-COMTRADE series (Trading Economics mirror).")
    li(L,"U.S. world totals: Census/BEA FT-900, December & Annual 2025 release.")
    li(L,"Overall trade balances: national statistics offices / IMF, latest full year, goods basis unless noted.")
    li(L,"Officeholders: official government sources and 2026-dated press, verified 2026-07-16 with an independent second pass.")
    R=tb(s,6.95,1.3,5.8,5.4)
    head(R,"MEASUREMENT NOTES",first=True)
    li(R,"Australia's overall balance is goods+services; India's is fiscal year 2025-26. All others goods-only, calendar 2025.")
    li(R,"Several overall balances are converted from local currency (EUR/GBP/CAD/AUD/JPY/SAR) at ~2025 average rates; USD values carry exchange-rate uncertainty.")
    li(R,"census.gov and imf.org were not directly reachable from the build environment; figures come from official-data-derived channels.")
    head(R,"IMAGERY")
    li(R,"Flags: public-domain renderings, uniform height, true aspect ratios.")
    li(R,"Portraits: official government portraits; monogram placeholders mark any still to be supplied.")
    head(R,"SCOPE")
    li(R,"Poland substituted for South Africa. EU and AU are G20 members but hold bloc seats and are not covered.")
    li(R,"A detailed uncertainty register (acting officials, figures pending confirmation) accompanies this deck: output/GAPS.md.")
    footer(s)

# ---- assemble ----
title_slide()
methodology_slide()
summary_slide(CO[:10],1,2)
summary_slide(CO[10:],2,2)
for i,c in enumerate(CO,1):
    country_slide(c,i)
sources_slide()
prs.save(ROOT+'output/g20-ministers-trade-deck.pptx')
print(f"Wrote output/g20-ministers-trade-deck.pptx — {len(prs.slides._sldIdLst)} slides "
      f"(seal: {'embedded' if SEAL else 'NOT available — drop assets/seal/doc-seal.png and rebuild'})")

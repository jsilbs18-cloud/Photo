#!/usr/bin/env python3
"""Build output/g20-ministers-trade-deck.pptx from data/g20.json.
Styled per the ITA Visual Style Guide (Jan 2026): Trade Navy/Blue palette,
Trade Gold heading rules, Open Sans, DOC seal + official footer signature."""
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
SEAL_W = 'assets/seal/doc-seal-white.png'   # white line rendering for navy slides
SEAL_W = SEAL_W if os.path.exists(ROOT + SEAL_W) else None

# ---- ITA Visual Style Guide palette ----
NAVY   = RGBColor(0x0A, 0x31, 0x4D)   # Trade Navy (primary)
BLUE   = RGBColor(0x00, 0x55, 0x8C)   # Trade Blue (primary)
GOLD   = RGBColor(0xB4, 0x86, 0x2D)   # Trade Gold (secondary)
SLATE  = RGBColor(0xB1, 0xBB, 0xCA)   # Trade Slate (neutral)
MOCHA  = RGBColor(0xE1, 0xDA, 0xCE)   # Trade Mocha (neutral)
TAN    = RGBColor(0xE5, 0xE5, 0xE5)   # Trade Tan (neutral)
INK    = RGBColor(0x2C, 0x2C, 0x2C)   # Text black per guide
GRAY   = RGBColor(0x54, 0x60, 0x6C)   # secondary text
MUTED  = RGBColor(0x75, 0x7D, 0x87)
POS    = RGBColor(0x00, 0x83, 0x3E)   # Trade Green
NEG    = RGBColor(0xD4, 0x61, 0x27)   # Trade Dk Orange (no red in ITA palette)
TEAL   = RGBColor(0x00, 0x75, 0x82)   # Trade Teal (role tags)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
LTBLUE = RGBColor(0xB9, 0xC9, 0xD9)   # light steel for text on navy
FONT   = 'Open Sans'                  # guide primary sans (Calibri = approved alternate)
SIGNATURE = "U.S. Department of Commerce  |  International Trade Administration"

prs = Presentation()
prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
SW, SH = 13.333, 7.5

def slide(): return prs.slides.add_slide(BLANK)

def rect(s,x,y,w,h,fill=None,line=None,line_w=0.75,rot=None):
    sp=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,Inches(x),Inches(y),Inches(w),Inches(h))
    sp.shadow.inherit=False
    if fill is None: sp.fill.background()
    else: sp.fill.solid(); sp.fill.fore_color.rgb=fill
    if line is None: sp.line.fill.background()
    else: sp.line.color.rgb=line; sp.line.width=Pt(line_w)
    if rot is not None: sp.rotation=rot
    return sp

def hline(s,x,y,w,color=TAN,weight=1.0):
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
    f.size=Pt(size); f.bold=bold; f.italic=italic; f.name=FONT; f.color.rgb=color
    if spacing is not None:
        rPr=r._r.get_or_add_rPr(); rPr.set('spc',str(int(spacing*100)))
    return r

def money(v): return 'N/A' if v is None else f"${v:,.1f}B"
def signed(v):
    if v is None: return ('N/A', GRAY, '')
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

def footer(s, idx=None, total=None, dark=False):
    col = WHITE if dark else BLUE
    sub = LTBLUE if dark else MUTED
    if not dark: hline(s,0.6,7.02,12.13,color=TAN,weight=1.0)
    tf=tb(s,0.6,7.10,8.6,0.3)
    p=para(tf,True)
    run(p,SIGNATURE,8,col,bold=True)
    tfm=tb(s,0.6,7.28,8.6,0.2)
    pm=para(tfm,True)
    run(pm,"GDP: IMF WEO 2025 · U.S. goods trade: U.S. Census 2025 · officeholders verified 2026-07-16",7,sub)
    tp=tb(s,10.2,7.10,2.53,0.3); p=para(tp,True); p.alignment=PP_ALIGN.RIGHT
    run(p,"trade.gov",8.5,col,bold=True)
    if idx is not None:
        run(p,f"    {idx}" if isinstance(idx,str) else f"    {idx} / {total}",8,sub)

# ============ TITLE (ITA template: Trade Navy + diagonal ribbons) ============
def title_slide():
    s=slide(); rect(s,0,0,SW,SH,fill=NAVY)
    # diagonal ribbon accents sweeping from the top-right (template motif)
    rect(s,9.0,-1.6,7.5,0.85,fill=BLUE,rot=-35)
    rect(s,10.3,-1.9,7.5,0.55,fill=SLATE,rot=-35)
    rect(s,8.1,-1.2,7.5,0.30,fill=TEAL,rot=-35)
    # agency block, top-left: white DOC seal + plain-text agency signature
    x=0.6
    if SEAL_W:
        w=pic(s,SEAL_W,0.6,0.48,0.72); x=0.6+w+0.22
    tf=tb(s,x,0.55,7.0,0.66,anchor=MSO_ANCHOR.MIDDLE)
    p=para(tf,True); run(p,"U.S. DEPARTMENT OF COMMERCE",10.5,WHITE,bold=True,spacing=1.6)
    p2=tf.add_paragraph(); p2.space_before=Pt(3)
    run(p2,"INTERNATIONAL TRADE ADMINISTRATION",10.5,LTBLUE,spacing=1.6)
    # title block
    tf2=tb(s,1.0,2.85,10.5,1.6)
    p=para(tf2,True); run(p,"G20 Digital & Trade Ministers",36,WHITE,bold=True)
    p2=tf2.add_paragraph(); p2.space_before=Pt(8)
    run(p2,"GDP and U.S. Bilateral Trade Profiles",20,SLATE)
    rect(s,1.02,4.42,2.3,0.045,fill=GOLD)
    # subhead box (template's bracketed subhead line)
    bx=rect(s,1.0,4.85,8.6,0.52,line=RGBColor(0x5B,0x77,0x92),line_w=1.0)
    tf3=tb(s,1.22,4.85,8.2,0.52,anchor=MSO_ANCHOR.MIDDLE)
    p=para(tf3,True)
    run(p,"Internal Reference  |  Trade data: 2025 full year (goods basis)  |  July 16, 2026",12,WHITE)
    # footer signature
    tf4=tb(s,0.6,6.95,8.6,0.3)
    p=para(tf4,True); run(p,SIGNATURE,9,WHITE,bold=True)
    tf5=tb(s,10.2,6.95,2.53,0.3); p=para(tf5,True); p.alignment=PP_ALIGN.RIGHT
    run(p,"trade.gov",9,WHITE,bold=True)

# ============ CONTENT HEADER (white, navy title, gold rule) ============
def header_bar(s,title,kicker=None):
    tf=tb(s,0.6,0.30,12.13,0.45)
    p=para(tf,True); run(p,title,22,NAVY,bold=True)
    if kicker:
        tfk=tb(s,0.6,0.76,12.13,0.28); pk=para(tfk,True); run(pk,kicker,10.5,GRAY)
    rect(s,0.6,1.10,2.2,0.035,fill=GOLD)

def bullet(tf,label,text,first=False):
    p=para(tf,first); p.space_after=Pt(7)
    if label: run(p,label+"  ",12,NAVY,bold=True)
    run(p,text,12,INK)

# ============ METHODOLOGY ============
def methodology_slide():
    s=slide(); rect(s,0,0,SW,SH,fill=WHITE)
    header_bar(s,"Methodology & Scope","19 sovereign members · EU & African Union annex · compiled 2026-07-16")
    tf=tb(s,0.6,1.42,11.3,5.3)
    bullet(tf,"Countries (19):","Argentina, Australia, Brazil, Canada, China, France, Germany, India, "
        "Indonesia, Italy, Japan, Mexico, Poland, Russia, Saudi Arabia, South Korea, Türkiye, "
        "United Kingdom, United States.",first=True)
    bullet(tf,"Substitution:","Poland is covered in place of South Africa — a deliberate substitution, not an omission.")
    bullet(tf,"Bloc members:","The European Union and African Union hold G20 seats as supranational "
        "blocs; they are profiled in the bloc annex following the country pages.")
    bullet(tf,"GDP:","Nominal (current USD), IMF World Economic Outlook 2025, single vintage across all 19.")
    bullet(tf,"U.S. bilateral trade:","U.S. Census Bureau goods trade, 2025 full year (goods basis), "
        "via Census-derived channels (see Sources).")
    bullet(tf,"Ministers:","Each officeholder confirmed current on 2026-07-16 by live search plus an "
        "independent verification pass. Where a portfolio is split, both responsible officials are profiled.")
    footer(s)

# ============ SUMMARY ============
def summary_slide(rows, part, total):
    s=slide(); rect(s,0,0,SW,SH,fill=WHITE)
    header_bar(s,"Summary — GDP & U.S. Bilateral Goods Trade",
               f"USD billions · GDP 2025 · trade 2025 (goods) · part {part} of {total}")
    cols=[("Country",0.6,3.4,'l'),("GDP (2025)",4.0,2.0,'r'),
          ("U.S. exports to",6.05,2.2,'r'),("U.S. imports from",8.30,2.3,'r'),
          ("U.S. bilateral balance",10.65,2.1,'r')]
    y0=1.42; rh=0.475
    rect(s,0.5,y0,12.33,rh,fill=NAVY)
    for name,x,w,al in cols:
        tf=tb(s,x,y0+0.06,w,rh-0.1,anchor=MSO_ANCHOR.MIDDLE)
        p=para(tf,True); p.alignment=PP_ALIGN.RIGHT if al=='r' else PP_ALIGN.LEFT
        run(p,name,11.5,WHITE,bold=True)
    for i,c in enumerate(rows):
        y=y0+rh+i*rh
        if i%2==0: rect(s,0.5,y,12.33,rh,fill=TAN)
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
BLK = [(1.26, 2.82), (4.14, 2.82)]

def datum(s,x,y,w,label,value,vcolor=NAVY,sub=None):
    tf=tb(s,x,y,w,0.8)
    p=para(tf,True); run(p,label,8.5,GRAY,spacing=0.3)
    p2=tf.add_paragraph(); p2.space_before=Pt(1); run(p2,value,14.5,vcolor,bold=True)
    if sub: run(p2,"  "+sub,9.5,GRAY)

def left_panel(s,c):
    rect(s,LP_X,1.42,LP_W,5.35,fill=TAN)
    rect(s,LP_X,1.42,LP_W,0.045,fill=GOLD)
    tf=tb(s,LP_X+0.20,1.58,LP_W-0.4,0.3)
    p=para(tf,True); run(p,"TRADE & ECONOMY",10.5,BLUE,bold=True,spacing=1.0)
    lx=LP_X+0.20; lw=LP_W-0.40; ly=1.98; step=0.96
    gy,ty,oy=c['gdp_year'],c['us_trade_year'],c['overall_balance_year']
    us = c['country']=='United States'
    datum(s,lx,ly,lw,f"NOMINAL GDP ({gy})",money(c['gdp_usd_b']))
    obs,obc,obw=signed(c['overall_balance_usd_b'])
    basis='goods' if 'goods-only' in c['overall_balance_basis'] else ('g+s' if 'services' in c['overall_balance_basis'] else '')
    datum(s,lx,ly+step,lw,f"OVERALL TRADE BALANCE ({oy})",obs,vcolor=INK,sub=(f"{obw} · {basis}" if c['overall_balance_usd_b'] is not None else None))
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
    if o.get('is_acting'): run(p,"  · acting",max(8.0,size*0.78),NEG,bold=True,italic=True)

def full_profile(s,y,h,heading,o,notes_line):
    tf=tb(s,RX,y,RW,0.24)
    p=para(tf,True); run(p,heading,10.5,BLUE,bold=True,spacing=1.2)
    tx=RX; tw=RW
    tf=tb(s,tx,y+0.28,tw,0.28)
    p=para(tf,True); run(p,o['name'],14,NAVY,bold=True); acting_run(p,o,14)
    tf=tb(s,tx,y+0.58,tw,0.38)
    p=para(tf,True); p.line_spacing=1.05; run(p,o['title'],11,GRAY,italic=True)
    tf=tb(s,tx,y+0.98,tw,0.32)
    p=para(tf,True); p.line_spacing=1.05
    run(p,o['ministry'],9.5,INK)
    if o.get('assumed_office'): run(p,f"   ·   Assumed office: {o['assumed_office']}",9.5,MUTED)
    tf=tb(s,RX,y+1.34,RW,h-1.34)
    p=para(tf,True); p.line_spacing=1.03; run(p,o.get('bio_display') or o.get('bio',''),11,INK)
    if notes_line:
        pn=tf.add_paragraph(); pn.space_before=Pt(5)
        run(pn,notes_line,9,GRAY,italic=True)

def half_profile(s,x0,y,h,o):
    tx=x0; tw=COL_W
    tf=tb(s,tx,y+0.26,tw,1.00)
    p=para(tf,True)
    if o.get('role_tag'): run(p,o['role_tag'],7.5,TEAL,bold=True,spacing=0.8)
    p2=tf.add_paragraph(); p2.space_before=Pt(2)
    run(p2,o['name'],12,NAVY,bold=True); acting_run(p2,o,12)
    p3=tf.add_paragraph(); p3.space_before=Pt(2); p3.line_spacing=1.04
    run(p3,o['title'],9,GRAY,italic=True)
    tf=tb(s,x0,y+1.28,COL_W,0.32)
    p=para(tf,True); p.line_spacing=1.04
    run(p,o['ministry'],8.5,INK)
    if o.get('assumed_office'): run(p,f"  ·  {o['assumed_office']}",8.5,MUTED)
    tf=tb(s,x0,y+1.62,COL_W,h-1.62)
    p=para(tf,True); p.line_spacing=1.04
    run(p,o.get('bio_display') or o.get('bio',''),10.5,INK)

def section(s,blk,heading,offs,div_note):
    y,h=blk
    shown=[o for o in offs if o.get('display') in ('full','half')]
    notes=[o for o in offs if o.get('display')=='note']
    notes_line='; '.join(f"{o['name']} ({o['title']})" for o in notes)
    if div_note: notes_line=div_note          # division note already names the other officials
    elif notes_line: notes_line='Also: '+notes_line
    if len(shown)>=2:
        tf=tb(s,RX,y,RW,0.24)
        p=para(tf,True); run(p,heading+"  ·  SPLIT PORTFOLIO",10.5,BLUE,bold=True,spacing=1.2)
        half_profile(s,RX,y,h,shown[0])
        half_profile(s,COL2_X,y,h,shown[1])
    elif len(shown)==1:
        full_profile(s,y,h,heading,shown[0],notes_line)
    else:
        tf=tb(s,RX,y,RW,0.5)
        p=para(tf,True); run(p,heading,10.5,BLUE,bold=True,spacing=1.2)
        p2=tf.add_paragraph(); run(p2,"[TO VERIFY]",13,NEG,bold=True)

def country_slide(c,idx):
    s=slide(); rect(s,0,0,SW,SH,fill=WHITE)
    fh=0.60
    w=pic(s,c['flag_file'],0.6,0.36,fh)
    rect(s,0.6,0.36,w,fh,line=SLATE,line_w=1.0)
    tf=tb(s,2.1,0.29,9.0,0.75,anchor=MSO_ANCHOR.MIDDLE)
    p=para(tf,True); run(p,c['country'],27,NAVY,bold=True)
    rect(s,0.6,1.13,12.13,0.035,fill=GOLD)
    left_panel(s,c)
    section(s,BLK[0],"DIGITAL / TECHNOLOGY",c['digital_ministers'],c.get('div_note_digital'))
    hline(s,RX,4.08,RW,color=TAN,weight=1.0)
    section(s,BLK[1],"TRADE / COMMERCE",c['trade_ministers'],c.get('div_note_trade'))
    footer(s,idx,19)

# ============ BLOC ANNEX (EU / AU) ============
def bloc_slide(c):
    s=slide(); rect(s,0,0,SW,SH,fill=WHITE)
    fh=0.60
    w=pic(s,c['flag_file'],0.6,0.36,fh)
    rect(s,0.6,0.36,w,fh,line=SLATE,line_w=1.0)
    tf=tb(s,2.1,0.20,10.6,0.60,anchor=MSO_ANCHOR.MIDDLE)
    p=para(tf,True); run(p,c['country'],26,NAVY,bold=True)
    run(p,"   ·   G20 BLOC MEMBER",10.5,TEAL,bold=True,spacing=1.0)
    facts='    ·    '.join(f"{f['label']}: {f['value']}" for f in c.get('facts',[]))
    tff=tb(s,2.1,0.80,10.6,0.30)
    p=para(tff,True); run(p,facts,9.5,GRAY)
    rect(s,0.6,1.13,12.13,0.035,fill=GOLD)
    left_panel(s,c)
    if c.get('panel_note'):
        tfn=tb(s,LP_X+0.20,6.42,LP_W-0.4,0.32)
        p=para(tfn,True); p.line_spacing=1.0; run(p,c['panel_note'],7.5,GRAY,italic=True)
    section(s,BLK[0],"DIGITAL / TECHNOLOGY",c['digital_ministers'],c.get('div_note_digital'))
    hline(s,RX,4.08,RW,color=TAN,weight=1.0)
    section(s,BLK[1],"TRADE / COMMERCE",c['trade_ministers'],c.get('div_note_trade'))
    footer(s,"Bloc annex")

# ============ SOURCES ============
def sources_slide():
    s=slide(); rect(s,0,0,SW,SH,fill=WHITE)
    header_bar(s,"Sources","datasets and vintages")
    L=tb(s,0.6,1.5,11.9,5.2)
    def head(tf,t,first=False):
        p=para(tf,first); p.space_before=Pt(0 if first else 10); p.space_after=Pt(4)
        run(p,t,11.5,NAVY,bold=True,spacing=0.6)
    def li(tf,t):
        p=tf.add_paragraph(); p.space_after=Pt(4); run(p,"•  ",11,GOLD,bold=True); run(p,t,11,INK)
    head(L,"DATASETS & VINTAGES",first=True)
    li(L,"GDP (nominal, current USD): IMF World Economic Outlook, Oct 2025 (2025 estimates), via StatisticsTimes tabulation.")
    li(L,"U.S. bilateral goods trade: U.S. Census Bureau, full-year 2025, via USTR country fact sheets and the Census/UN-COMTRADE series (Trading Economics mirror).")
    li(L,"U.S. world totals: Census/BEA FT-900, December & Annual 2025 release.")
    li(L,"Overall trade balances: national statistics offices / IMF, latest full year, goods basis unless noted.")
    li(L,"EU & African Union annex: IMF WEO, Eurostat, USTR, and official EU/AU sources, verified 2026-07-16.")
    li(L,"Officeholders: official government sources and 2026-dated press, verified 2026-07-16 with an independent second pass.")
    footer(s)

# ---- assemble ----
title_slide()
methodology_slide()
summary_slide(CO[:10],1,2)
summary_slide(CO[10:],2,2)
for i,c in enumerate(CO,1):
    country_slide(c,i)
for b in D.get('blocs', []):
    bloc_slide(b)
sources_slide()
prs.save(ROOT+'output/g20-ministers-trade-deck.pptx')
print(f"Wrote output/g20-ministers-trade-deck.pptx — {len(prs.slides._sldIdLst)} slides "
      f"(ITA style; seal: {'white-line embedded' if SEAL_W else 'MISSING'})")

#!/usr/bin/env python3
"""Build output/g20-ministers-trade-deck.pptx from data/g20.json."""
import json
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from PIL import Image

D = json.load(open('/home/user/Photo/data/g20.json'))
CO = D['countries']; META = D['meta']

# ---- palette ----
NAVY=RGBColor(0x1F,0x38,0x64); SLATE=RGBColor(0x44,0x54,0x6A); INK=RGBColor(0x26,0x26,0x26)
MUTED=RGBColor(0x7F,0x7F,0x7F); WHITE=RGBColor(0xFF,0xFF,0xFF); PANEL=RGBColor(0xF3,0xF5,0xF9)
RULE=RGBColor(0xD6,0xDC,0xE5); POS=RGBColor(0x1E,0x7A,0x34); NEG=RGBColor(0xB2,0x33,0x30)
AMBER=RGBColor(0xB9,0x7A,0x00); ACCENT=RGBColor(0x2E,0x5A,0x88)
BADGE={'Needs check':AMBER,'Vacant / acting':RGBColor(0xC0,0x5A,0x00),'Verified':POS}

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
    return ln

def tb(s,x,y,w,h,anchor=MSO_ANCHOR.TOP,wrap=True):
    b=s.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h)); tf=b.text_frame
    tf.word_wrap=wrap; tf.vertical_anchor=anchor
    tf.margin_left=0; tf.margin_right=0; tf.margin_top=0; tf.margin_bottom=0
    return tf

def para(tf,first=False):
    p=tf.paragraphs[0] if first and not tf.paragraphs[0].runs else tf.add_paragraph()
    return p

def run(p,text,size,color=INK,bold=False,italic=False,font='Calibri',spacing=None):
    r=p.add_run(); r.text=text; f=r.font
    f.size=Pt(size); f.bold=bold; f.italic=italic; f.name=font; f.color.rgb=color
    if spacing is not None:
        rPr=r._r.get_or_add_rPr(); rPr.set('spc',str(int(spacing*100)))
    return r

def money(v):
    if v is None: return 'N/A'
    return f"${v:,.1f}B"

def signed(v):
    if v is None: return ('N/A', SLATE, '')
    word='surplus' if v>=0 else 'deficit'
    s=f"{'+' if v>=0 else '−'}${abs(v):,.1f}B"
    return (s, POS if v>=0 else NEG, word)

FLAG_AR={}
def flag_ar(path):
    if path not in FLAG_AR:
        im=Image.open('/home/user/Photo/'+path); FLAG_AR[path]=im.width/im.height
    return FLAG_AR[path]

# ============ TITLE SLIDE ============
def title_slide():
    s=slide(); rect(s,0,0,SW,SH,fill=NAVY)
    rect(s,0,0,SW,0.28,fill=ACCENT)
    rect(s,0,SH-0.28,SW,0.28,fill=ACCENT)
    tf=tb(s,1.0,2.15,11.33,1.7)
    p=para(tf,True); run(p,"G20 Countries: Digital & Trade Ministers",34,WHITE,bold=True)
    p2=tf.add_paragraph(); run(p2,"with GDP and U.S. Bilateral Trade Profiles",22,RGBColor(0xC7,0xD3,0xE8))
    tf3=tb(s,1.0,4.15,11.33,1.5)
    steel=RGBColor(0xAE,0xB9,0xCF)
    lines=[("Prepared for the International Trade Administration",16,WHITE,True),
           ("U.S. Department of Commerce — Internal Reference",13,steel,False),
           ("July 16, 2026",13,steel,False)]
    for i,(t,sz,col,bold) in enumerate(lines):
        p=para(tf3, i==0); p.space_after=Pt(4); run(p,t,sz,col,bold=bold)
    # data-vintage line
    tf4=tb(s,1.0,6.15,11.33,0.8)
    p=para(tf4,True); run(p,"Data vintage:  ",11,RGBColor(0x8F,0x9E,0xBE),bold=True)
    run(p,"Trade — U.S. Census goods, 2025 full year (goods basis).  GDP — IMF WEO, 2025.  "
          "Ministers verified as current on 2026-07-16.  Figures in USD billions unless noted.",11,RGBColor(0x8F,0x9E,0xBE))

# ============ METHODOLOGY / SCOPE ============
def header_bar(s,title,kicker=None):
    rect(s,0,0,SW,1.0,fill=NAVY)
    rect(s,0,1.0,SW,0.06,fill=ACCENT)
    tf=tb(s,0.6,0.16,12.13,0.72,anchor=MSO_ANCHOR.MIDDLE)
    p=para(tf,True); run(p,title,24,WHITE,bold=True)
    if kicker:
        tfk=tb(s,0.6,0.66,12.13,0.3); pk=para(tfk,True); run(pk,kicker,11,RGBColor(0xB9,0xC5,0xDC))

def bullet(tf,label,text,first=False):
    p=para(tf,first); p.space_after=Pt(7)
    if label: run(p,label+"  ",12.5,NAVY,bold=True)
    run(p,text,12.5,INK)

def methodology_slide():
    s=slide(); rect(s,0,0,SW,SH,fill=WHITE)
    header_bar(s,"Methodology & Scope","19 G20 sovereign members · compiled 2026-07-16")
    tf=tb(s,0.6,1.35,7.5,5.7)
    bullet(tf,"Countries (19):","Argentina, Australia, Brazil, Canada, China, France, Germany, India, "
        "Indonesia, Italy, Japan, Mexico, Poland, Russia, Saudi Arabia, South Korea, Türkiye, "
        "United Kingdom, United States.",first=True)
    bullet(tf,"Substitution:","Poland is included in place of South Africa, per instruction — a deliberate "
        "substitution, not an omission.")
    bullet(tf,"Bloc seats excluded:","The European Union and African Union hold G20 seats but are "
        "supranational blocs, not sovereign countries, and are not profiled.")
    bullet(tf,"GDP:","Nominal (current USD), IMF World Economic Outlook 2025, single vintage across all 19.")
    bullet(tf,"U.S. bilateral trade:","U.S. Census Bureau goods trade, 2025 full year (goods basis), "
        "sourced via Census-derived channels (see Sources).")
    bullet(tf,"Ministers:","Each officeholder confirmed current on 2026-07-16 by live search plus an "
        "independent verification pass. Split portfolios show every responsible official.")
    # side panel: verification + flags
    rect(s,8.5,1.5,4.23,5.25,fill=PANEL)
    hline(s,8.5,1.5,4.23,color=ACCENT,weight=3)
    tp=tb(s,8.8,1.75,3.7,5.0)
    p=para(tp,True); run(p,"CONFIDENCE FLAGS",11,NAVY,bold=True,spacing=1.0)
    for lab,desc,col in [("Verified","independently confirmed current",POS),
                         ("Needs check","a figure or minister carries uncertainty",AMBER),
                         ("Vacant / acting","post held on an acting/interim basis",RGBColor(0xC0,0x5A,0x00))]:
        p=tp.add_paragraph(); p.space_before=Pt(9)
        run(p,"■ ",12,col,bold=True); run(p,lab,12,INK,bold=True)
        p2=tp.add_paragraph(); run(p2,desc,10.5,SLATE)
    p=tp.add_paragraph(); p.space_before=Pt(14)
    run(p,"Roll-up this deck: ",10.5,SLATE,bold=True)
    run(p,"12 Verified · 5 Needs check · 2 Acting.",10.5,SLATE)
    p=tp.add_paragraph(); p.space_before=Pt(10)
    run(p,"Nothing is filled from model memory; unconfirmed items are flagged, not guessed.",10.5,SLATE,italic=True)

# ============ SUMMARY TABLE ============
def summary_slide(rows, part, total):
    s=slide(); rect(s,0,0,SW,SH,fill=WHITE)
    header_bar(s,"Summary — GDP & U.S. Bilateral Goods Trade",
               f"USD billions · GDP 2025 · trade 2025 (goods) · part {part} of {total}")
    cols=[("Country",0.6,3.4,'l'),("GDP (2025)",4.0,2.0,'r'),
          ("U.S. exports to",6.05,2.2,'r'),("U.S. imports from",8.30,2.3,'r'),
          ("U.S. bilateral balance",10.65,2.1,'r')]
    y0=1.45; rh=0.50
    # header row
    rect(s,0.5,y0,12.33,rh,fill=NAVY)
    for name,x,w,al in cols:
        tf=tb(s,x,y0+0.06,w,rh-0.1,anchor=MSO_ANCHOR.MIDDLE)
        p=para(tf,True); p.alignment=PP_ALIGN.RIGHT if al=='r' else PP_ALIGN.LEFT
        run(p,name,11.5,WHITE,bold=True)
    for i,c in enumerate(rows):
        y=y0+rh+i*rh
        if i%2==0: rect(s,0.5,y,12.33,rh,fill=PANEL)
        vals=[(c['country'],'l',INK,True),
              (money(c['gdp_usd_b']),'r',INK,False),
              (money(c['us_exports_usd_b']),'r',INK,False),
              (money(c['us_imports_usd_b']),'r',INK,False)]
        bs,bc,_=signed(c['us_bilateral_usd_b'])
        for (name,x,w,al),(val,a,col,bold) in zip(cols[:4],vals):
            tf=tb(s,x,y+0.05,w,rh-0.08,anchor=MSO_ANCHOR.MIDDLE)
            p=para(tf,True); p.alignment=PP_ALIGN.RIGHT if a=='r' else PP_ALIGN.LEFT
            run(p,val,11.5,col,bold=bold)
        tf=tb(s,cols[4][1],y+0.05,cols[4][2],rh-0.08,anchor=MSO_ANCHOR.MIDDLE)
        p=para(tf,True); p.alignment=PP_ALIGN.RIGHT
        run(p,bs,11.5,bc,bold=True)
    hline(s,0.5,y0+rh+len(rows)*rh+0.05,12.33,color=RULE)
    tf=tb(s,0.5,7.06,12.33,0.34)
    p=para(tf,True); run(p,"Negative U.S. bilateral balance = U.S. goods deficit (red); positive = U.S. surplus (green). "
        "United States shown as N/A for bilateral columns.",9,MUTED,italic=True)

# ============ COUNTRY SLIDE ============
def datum(s,x,y,w,label,value,vcolor=NAVY,sub=None):
    tf=tb(s,x,y,w,0.8)
    p=para(tf,True); run(p,label,9.5,SLATE,spacing=0.4)
    p2=tf.add_paragraph(); p2.space_before=Pt(1); run(p2,value,15,vcolor,bold=True)
    if sub:
        run(p2,"  "+sub,10,SLATE)

def minister_block(s,x,y,w,h,heading,primary,div_note):
    tf=tb(s,x,y,w,0.30)
    p=para(tf,True); run(p,heading,11,ACCENT,bold=True,spacing=1.2)
    if not primary:
        tf2=tb(s,x,y+0.34,w,0.4); p=para(tf2,True); run(p,"[TO VERIFY]",13,AMBER,bold=True); return
    # name + acting
    tfn=tb(s,x,y+0.30,w,0.32)
    p=para(tfn,True); run(p,primary['name'],14.5,NAVY,bold=True)
    if primary.get('is_acting'): run(p,"  · acting",11,RGBColor(0xC0,0x5A,0x00),bold=True,italic=True)
    # title (up to 2 lines)
    tft=tb(s,x,y+0.62,w,0.40)
    p=para(tft,True); p.line_spacing=1.05; run(p,primary['title'],11,SLATE,italic=True)
    # ministry · assumed (up to 2 lines)
    tfm=tb(s,x,y+1.02,w,0.38)
    p=para(tfm,True); p.line_spacing=1.05; run(p,primary['ministry'],10,INK)
    ao=primary.get('assumed_office','')
    if ao: run(p,f"   ·   Assumed office: {ao}",10,MUTED)
    # bio + division note flow together in one frame (auto-follows bio length)
    tfb=tb(s,x,y+1.44,w,h-1.44)
    p=para(tfb,True); p.line_spacing=1.03; run(p,primary.get('bio',''),11,INK)
    if div_note:
        pn=tfb.add_paragraph(); pn.space_before=Pt(6)
        run(pn,"Division of responsibility:  ",9.5,ACCENT,bold=True,italic=True)
        run(pn,div_note,9.5,SLATE,italic=True)

def country_slide(c, idx):
    s=slide(); rect(s,0,0,SW,SH,fill=WHITE)
    # header: flag + name
    fh=0.60; ar=flag_ar(c['flag_file']); fw=fh*ar
    fy=0.40
    s.shapes.add_picture('/home/user/Photo/'+c['flag_file'],Inches(0.6),Inches(fy),height=Inches(fh))
    rect(s,0.6,fy,fw,fh,line=RULE,line_w=0.75)  # thin border around flag
    tf=tb(s,2.1,0.33,8.0,0.75,anchor=MSO_ANCHOR.MIDDLE)  # fixed x so name never shifts with flag width
    p=para(tf,True); run(p,c['country'],28,NAVY,bold=True)
    # confidence badge top-right
    flag=c['row_confidence']
    if flag!='Verified':
        bw=2.5; bx=12.73-bw
        rect(s,bx,0.44,bw,0.44,fill=BADGE[flag])
        tfb=tb(s,bx,0.44,bw,0.44,anchor=MSO_ANCHOR.MIDDLE)
        p=para(tfb,True); p.alignment=PP_ALIGN.CENTER
        run(p,flag.upper(),11,WHITE,bold=True)
    hline(s,0.6,1.18,12.13,color=NAVY,weight=1.5)

    # LEFT data column
    rect(s,0.6,1.42,3.5,5.35,fill=PANEL)
    hline(s,0.6,1.42,3.5,color=ACCENT,weight=3)
    tfL=tb(s,0.82,1.60,3.1,0.3); p=para(tfL,True); run(p,"TRADE & ECONOMY",11,NAVY,bold=True,spacing=1.0)
    lx=0.82; ly=2.02; lw=3.06; step=0.96
    gy=c['gdp_year']; ty=c['us_trade_year']; oy=c['overall_balance_year']
    datum(s,lx,ly,lw,f"NOMINAL GDP ({gy})",money(c['gdp_usd_b']))
    obs,obc,obw=signed(c['overall_balance_usd_b'])
    basis='goods' if 'goods-only' in c['overall_balance_basis'] else ('g+s' if 'services' in c['overall_balance_basis'] else '')
    datum(s,lx,ly+step,lw,f"OVERALL TRADE BALANCE ({oy})",obs,vcolor=INK,sub=f"{obw} · {basis}")
    datum(s,lx,ly+2*step,lw,f"U.S. GOODS EXPORTS TO ({ty})",money(c['us_exports_usd_b']))
    datum(s,lx,ly+3*step,lw,f"U.S. GOODS IMPORTS FROM ({ty})",money(c['us_imports_usd_b']))
    bs,bc,bw=signed(c['us_bilateral_usd_b'])
    datum(s,lx,ly+4*step,lw,f"U.S. BILATERAL BALANCE ({ty})",bs,vcolor=bc,sub=bw)

    # RIGHT minister columns
    rx=4.5; rw=8.23
    dprim=next((o for o in c['digital_ministers'] if o['is_primary']),None)
    tprim=next((o for o in c['trade_ministers'] if o['is_primary']),None)
    # build division notes
    def others_note(offs, bespoke):
        if bespoke: return bespoke
        extra=[o for o in offs if not o['is_primary']]
        if not extra: return ''
        return "also " + '; '.join(f"{o['name']} ({o['title']})" for o in extra)
    dn=others_note(c['digital_ministers'], c.get('div_note_digital'))
    tn=others_note(c['trade_ministers'], c.get('div_note_trade'))
    minister_block(s,rx,1.26,rw,2.82,"DIGITAL / TECHNOLOGY MINISTER",dprim,dn)
    hline(s,rx,4.11,rw,color=RULE)
    minister_block(s,rx,4.14,rw,2.82,"TRADE / COMMERCE MINISTER",tprim,tn)

    # footer
    hline(s,0.6,7.0,12.13,color=RULE)
    tf=tb(s,0.6,7.05,10.5,0.34)
    p=para(tf,True)
    run(p,"Sources: ",8,MUTED,bold=True)
    run(p,"GDP — IMF WEO 2025 · U.S. goods trade — U.S. Census 2025 · ministers verified 2026-07-16. "
          "See Sources & Caveats slide.",8,MUTED)
    tfp=tb(s,11.6,7.05,1.13,0.34); p=para(tfp,True); p.alignment=PP_ALIGN.RIGHT
    run(p,f"{idx} / 19",8,MUTED)

# ============ SOURCES & CAVEATS ============
def sources_slide():
    s=slide(); rect(s,0,0,SW,SH,fill=WHITE)
    header_bar(s,"Sources & Caveats","datasets, vintages, and flagged uncertainties")
    L=tb(s,0.6,1.3,6.05,5.8)
    def head(tf,t,first=False):
        p=para(tf,first); p.space_before=Pt(0 if first else 10); p.space_after=Pt(3)
        run(p,t,12,NAVY,bold=True,spacing=0.6)
    def line(tf,t):
        p=tf.add_paragraph(); p.space_after=Pt(2); run(p,"•  ",10.5,ACCENT); run(p,t,10.5,INK)
    head(L,"DATASETS & VINTAGES",first=True)
    line(L,"GDP (nominal, current USD): IMF World Economic Outlook, Oct 2025 (2025 estimates), via StatisticsTimes tabulation.")
    line(L,"U.S. bilateral goods trade: U.S. Census Bureau, full-year 2025, via USTR country fact sheets and the Census/UN-COMTRADE series (Trading Economics mirror).")
    line(L,"Overall trade balances: national statistics offices / IMF, latest full year, goods basis unless noted.")
    line(L,"Flags: hampusborgos/country-flags (public domain); Wikimedia Commons was egress-blocked in the build environment.")
    head(L,"BASIS & CONVERSION")
    line(L,"Australia's overall balance is goods+services; India's is fiscal year 2025-26. All others goods-only, calendar 2025.")
    line(L,"Several overall balances are converted from local currency (EUR/GBP/CAD/AUD/JPY/SAR) at ~2025 average rates; USD values carry exchange-rate uncertainty.")
    line(L,"census.gov, imf.org and many national sites returned HTTP 403 to automated fetching; figures came from official-data-derived channels, not read off the primary page.")

    R=tb(s,6.95,1.3,5.8,5.8)
    head(R,"FLAGGED — NEEDS CHECK",first=True)
    for c in CO:
        if c['row_confidence']=='Needs check':
            reasons='; '.join(c['gaps'][:2])
            p=R.add_paragraph(); p.space_after=Pt(2)
            run(p,"•  ",10.5,AMBER); run(p,c['country']+": ",10.5,INK,bold=True); run(p,reasons,10,SLATE)
    head(R,"FLAGGED — VACANT / ACTING")
    for c in CO:
        if c['row_confidence']=='Vacant / acting':
            actor=next((o['name']+" — "+o['title'] for o in c['trade_ministers']+c['digital_ministers'] if o.get('is_acting')),'')
            p=R.add_paragraph(); p.space_after=Pt(2)
            run(p,"•  ",10.5,RGBColor(0xC0,0x5A,0x00)); run(p,c['country']+": ",10.5,INK,bold=True); run(p,actor,10,SLATE)
    head(R,"DATA-QUALITY CORRECTION")
    p=R.add_paragraph(); run(p,"•  ",10.5,ACCENT)
    run(p,"Saudi Arabia's raw trade-officials list wrongly included the U.S. Commerce Secretary and USTR "
          "(context bleed); removed and corrected.",10,SLATE)
    head(R,"SCOPE NOTE")
    p=R.add_paragraph(); run(p,"•  ",10.5,ACCENT)
    run(p,"Poland substituted for South Africa. EU and AU are G20 members but are bloc seats, not covered here.",10,SLATE)
    hline(s,0.6,7.02,12.13,color=RULE)
    tf=tb(s,0.6,7.07,12.13,0.32); p=para(tf,True)
    run(p,"Full per-country sourcing with URLs and as-of dates: research/g20-research.md · gaps register: output/GAPS.md",8.5,MUTED,italic=True)

# ---- assemble ----
title_slide()
methodology_slide()
summary_slide(CO[:10],1,2)
summary_slide(CO[10:],2,2)
for i,c in enumerate(CO,1):
    country_slide(c,i)
sources_slide()

prs.save('/home/user/Photo/output/g20-ministers-trade-deck.pptx')
print(f"Wrote output/g20-ministers-trade-deck.pptx — {len(prs.slides.__iter__.__self__._sldIdLst)} slides")

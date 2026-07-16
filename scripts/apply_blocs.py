#!/usr/bin/env python3
"""Merge the EU / African Union bloc research (data/_bloc_eu.json, data/_bloc_au.json)
into data/g20.json under 'blocs', normalize fields to the country-slide shape, and
extend the QA roster reference. Generates a labeled flag placeholder if a download failed."""
import json, os, re
from PIL import Image, ImageDraw, ImageFont

FACT_OVERRIDES = {
    ('African Union', 'Member states'): '55',
    ('African Union', 'G20 status'): 'Permanent member since Sept 2023',
    ('African Union', 'Headquarters'): 'Addis Ababa',
    ('African Union', 'AU Commission Chairperson'): 'Mahmoud Ali Youssouf',
    ('European Union', 'Member states'): '27',
    ('European Union', 'G20 status'): 'Founding member since 1999',
    ('European Union', 'Headquarters'): 'Brussels',
}
LABEL_SHORT = {'Member states': 'Members', 'G20 status': 'G20', 'Headquarters': 'HQ',
               'AU Commission Chairperson': 'AUC Chair', 'European Commission President': 'Commission President'}
def shorten_fact(name, label, v, max_words=7):
    ov = FACT_OVERRIDES.get((name, label))
    if ov: return ov
    v = re.split(r'[;(—]| - ', v)[0].strip().rstrip(',')
    words = v.split()
    while words and words[-1].lower() in ('at','of','in','under','by','the','a','an','since'):
        words.pop()
    return ' '.join(words[:max_words])

def sentence_trim(bio, max_words):
    ABBR = ['U.S.', 'U.K.', 'U.N.', 'D.C.', 'Dr.', 'Mr.', 'Ms.', 'St.', 'Jr.', 'Sr.', 'Inc.', 'Co.', 'No.']
    guarded = bio.strip()
    for i, a in enumerate(ABBR):
        guarded = guarded.replace(a, f'\x00{i}\x00')
    out = []
    for sent in re.split(r'(?<=[.!?])\s+', guarded):
        if len(' '.join(out + [sent]).split()) > max_words and out:
            break
        out.append(sent)
    joined = ' '.join(out)
    for i, a in enumerate(ABBR):
        joined = joined.replace(f'\x00{i}\x00', a)
    return joined

ROOT = '/home/user/Photo/'
D = json.load(open(ROOT + 'data/g20.json'))
FONT = '/usr/local/share/fonts/ita/OpenSans-Bold.ttf'

def flag_placeholder(label, dst):
    im = Image.new('RGB', (600, 400), (0xB1, 0xBB, 0xCA))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 599, 399], outline=(0x0A, 0x31, 0x4D), width=8)
    f = ImageFont.truetype(FONT, 80)
    bb = d.textbbox((0, 0), label, font=f)
    d.text(((600 - bb[2]) / 2, (400 - bb[3]) / 2 - 20), label, font=f, fill=(0x0A, 0x31, 0x4D))
    f2 = ImageFont.truetype(FONT, 28)
    lab = 'FLAG PENDING'
    bb2 = d.textbbox((0, 0), lab, font=f2)
    d.text(((600 - bb2[2]) / 2, 320), lab, font=f2, fill=(0x0A, 0x31, 0x4D))
    im.save(ROOT + dst, 'PNG')

def norm_official(o):
    return {
        'name': o.get('name', '').strip(), 'title': o.get('title', '').strip(),
        'ministry': o.get('ministry', '').strip(),
        'assumed_office': (o.get('assumed_office') or '').split(' (')[0].strip(),
        'bio': (o.get('bio') or '').strip(), 'bio_display': (o.get('bio') or '').strip(),
        'source_url': o.get('source_url', ''), 'as_of': o.get('as_of', '2026-07-16'),
        'confidence': o.get('confidence', 'Needs check'),
        'is_acting': bool(o.get('is_acting')), 'display': o.get('display', 'full'),
        'role_tag': None, 'is_primary': True,
    }

blocs = []
for fn, abbrev in (('data/_bloc_eu.json', 'EU'), ('data/_bloc_au.json', 'AU')):
    path = ROOT + fn
    if not os.path.exists(path):
        raise SystemExit(f'missing {fn} — bloc research not complete')
    b = json.load(open(path))
    flag = b.get('flag_file') or f'assets/flags/{abbrev.lower()}-placeholder.png'
    if b.get('flag_status') != 'ok' or not os.path.exists(ROOT + flag):
        flag = f'assets/flags/{abbrev.lower()}-placeholder.png'
        flag_placeholder(abbrev, flag)
        print(f'  !! {b.get("name")}: flag placeholder generated')
    e, i = b.get('us_exports_usd_b'), b.get('us_imports_usd_b')
    bil = round(e - i, 1) if (e is not None and i is not None) else None
    gaps = []
    for o in b.get('digital_officials', []) + b.get('trade_officials', []):
        if o.get('confidence') != 'Verified' or '[TO VERIFY]' in o.get('name', ''):
            gaps.append(f"Official '{o.get('name')}' ({o.get('title')}) flagged {o.get('confidence')}.")
    if str(b.get('gdp_confidence', '')).lower() == 'low':
        gaps.append('GDP aggregate low-confidence.')
    if b.get('overall_balance_confidence') not in (None, 'Verified'):
        gaps.append(f"Overall balance flagged {b.get('overall_balance_confidence')}: {b.get('overall_balance_notes','')[:140]}")
    if str(b.get('us_trade_confidence', '')).lower() in ('low', 'medium'):
        gaps.append(f"U.S. trade figures {b.get('us_trade_confidence')}-confidence: {b.get('us_trade_notes','')[:140]}")
    panel_note = ''
    if abbrev == 'AU':
        panel_note = '* U.S. trade figures are U.S.–Africa goods totals (proxy for the AU).'
    blocs.append({
        'country': b['name'], 'flag_file': flag,
        'facts': [{'label': LABEL_SHORT.get(f['label'].split('(')[0].strip(), f['label'].split('(')[0].strip()), 'value': shorten_fact(b['name'], f['label'].split('(')[0].strip(), f['value'])} for f in b.get('facts', [])],
        'gdp_usd_b': b.get('gdp_usd_b'), 'gdp_year': b.get('gdp_year', ''), 'gdp_confidence': b.get('gdp_confidence', ''),
        'overall_balance_usd_b': b.get('overall_balance_usd_b'),
        'overall_balance_basis': b.get('overall_balance_basis', 'goods-only'),
        'overall_balance_year': b.get('overall_balance_year', ''),
        'overall_balance_confidence': b.get('overall_balance_confidence', ''),
        'us_exports_usd_b': e, 'us_imports_usd_b': i, 'us_bilateral_usd_b': bil,
        'us_trade_year': b.get('us_trade_year', ''), 'us_trade_confidence': b.get('us_trade_confidence', ''),
        'digital_ministers': [norm_official(o) for o in b.get('digital_officials', [])],
        'trade_ministers': [norm_official(o) for o in b.get('trade_officials', [])],
        'div_note_digital': '', 'div_note_trade': '',
        'panel_note': panel_note,
        'sources': {'gdp': b.get('gdp_source_url',''), 'balance': b.get('overall_balance_source_url',''),
                    'us_trade': b.get('us_trade_source_url','')},
        'gaps': gaps,
        'inconsistencies': b.get('inconsistencies', []),
    })
    # primaries + bio budgets (full-with-note: 58 words; else 85)
    for key in ('digital_ministers', 'trade_ministers'):
        offs = blocs[-1][key]
        has_note = any(o.get('display') == 'note' for o in offs)
        for j, o in enumerate(offs):
            o['is_primary'] = (j == 0)
            if o.get('display') == 'full':
                o['bio_display'] = sentence_trim(o['bio_display'], 58 if has_note else 85)

D['blocs'] = blocs
json.dump(D, open(ROOT + 'data/g20.json', 'w'), indent=2, ensure_ascii=False)

# extend roster reference for QA
ref = json.load(open(ROOT + 'data/_roster_reference.json'))
for b in blocs:
    for key in ('digital_ministers', 'trade_ministers'):
        for o in b[key]:
            ref.append({'country': b['country'], 'name': o['name'], 'title': o['title'],
                        'ministry': o['ministry'], 'source_url': o.get('source_url', '')})
json.dump(ref, open(ROOT + 'data/_roster_reference.json', 'w'), indent=1, ensure_ascii=False)
print(f"Merged {len(blocs)} blocs into data/g20.json; roster reference extended.")
for b in blocs:
    print(f"  {b['country']}: GDP {b['gdp_usd_b']}, US bilat {b['us_bilateral_usd_b']}, "
          f"digital={[o['name'] for o in b['digital_ministers']]}, trade={[o['name'] for o in b['trade_ministers']]}, gaps={len(b['gaps'])}")

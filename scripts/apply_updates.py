#!/usr/bin/env python3
"""Merge v2 workflow results (data/_updates.json) into data/g20.json:
- user-directed roster changes for AU/AR/CN/PL/RU (verified live)
- display plan: full / half (two-up split) / note, with role tags
- compressed bios for half-width columns
- portrait file mapping (raw downloads; normalize_portraits.py finishes the job)
- US world-trade totals; DOC seal path
Also writes data/_roster_reference.json (the QA char-for-char reference)."""
import json, re, unicodedata

ROOT = '/home/user/Photo/'
D = json.load(open(ROOT + 'data/g20.json'))
U = json.load(open(ROOT + 'data/_updates.json'))
TARGETS = json.load(open(ROOT + 'data/_portrait_targets.json'))
CO = {c['country']: c for c in D['countries']}

def norm_name(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z]', '', s)

# ---------- display plan for the 14 non-verify countries ----------
# (country, portfolio) -> list of (name-substring, display)
PLAN = {
    ('Brazil','digital'): [('Siqueira','half'), ('Luciana Santos','half')],
    ('Brazil','trade'): [('Elias Rosa','full'), ('Ferraz','omit')],
    ('Canada','digital'): [('Solomon','full')],
    ('Canada','trade'): [('Sidhu','half'), ('LeBlanc','half')],
    ('France','digital'): [('Le Hénanff','full')],
    ('France','trade'): [('Forissier','full')],
    ('Germany','digital'): [('Wildberger','full')],
    ('Germany','trade'): [('Reiche','full'), ('Šefčovič','note')],
    ('India','digital'): [('Vaishnaw','full'), ('Prasada','note')],
    ('India','trade'): [('Goyal','half'), ('Agrawal','half')],
    ('Indonesia','digital'): [('Hafid','full')],
    ('Indonesia','trade'): [('Budi Santoso','half'), ('Airlangga','half')],
    ('Italy','digital'): [('Butti','full')],
    ('Italy','trade'): [('Tajani','half'), ('Urso','half')],
    ('Japan','digital'): [('Matsumoto','full')],
    ('Japan','trade'): [('Akazawa','full'), ('Motegi','note')],
    ('Mexico','digital'): [('Peña Merino','full')],
    ('Mexico','trade'): [('Ebrard','half'), ('Gutiérrez','half')],
    ('Saudi Arabia','digital'): [('Alswaha','full')],
    ('Saudi Arabia','trade'): [('Al-Qasabi','half'), ('Al-Abduljabbar','half')],
    ('South Korea','digital'): [('Bae','full')],
    ('South Korea','trade'): [('Kim Jung-kwan','half'), ('Yeo Han-koo','half')],
    ('Türkiye','digital'): [('Kacır','full'), ('Önal','note'), ('Uraloğlu','note')],
    ('Türkiye','trade'): [('Bolat','full')],
    ('United Kingdom','digital'): [('Kendall','full'), ('Murray','note'), ('Narayan','note')],
    ('United Kingdom','trade'): [('Kyle','half'), ('Bryant','half')],
    ('United States','digital'): [('Kratsios','half'), ('Roth','half')],
    ('United States','trade'): [('Lutnick','half'), ('Greer','half')],
}

ROLE_TAGS = {
    ('Brazil','Siqueira'): 'COMMUNICATIONS & TELECOM', ('Brazil','Luciana Santos'): 'SCIENCE, TECHNOLOGY & INNOVATION',
    ('Brazil','Elias Rosa'): 'MDIC MINISTER', ('Brazil','Ferraz'): 'FOREIGN TRADE (SECEX)',
    ('Canada','Sidhu'): 'INTERNATIONAL TRADE', ('Canada','LeBlanc'): 'CANADA–U.S. TRADE',
    ('China','Li Lecheng'): 'INDUSTRY & INFORMATION TECHNOLOGY (MIIT)', ('China','Yin Hejun'): 'SCIENCE & TECHNOLOGY (MOST)',
    ('China','Wang Wentao'): 'COMMERCE MINISTER (MOFCOM)', ('China','Li Chenggang'): 'CHIEF TRADE NEGOTIATOR',
    ('India','Goyal'): 'CABINET MINISTER', ('India','Agrawal'): 'COMMERCE SECRETARY · CHIEF US NEGOTIATOR',
    ('Indonesia','Budi Santoso'): 'TRADE MINISTER', ('Indonesia','Airlangga'): 'ECONOMIC COORDINATION & NEGOTIATIONS',
    ('Italy','Tajani'): 'FOREIGN TRADE & EXPORT PROMOTION', ('Italy','Urso'): 'ENTERPRISES & DOMESTIC INDUSTRY',
    ('Mexico','Ebrard'): 'SECRETARY OF ECONOMY', ('Mexico','Gutiérrez'): 'FOREIGN TRADE UNDERSECRETARY',
    ('Poland','Domański'): 'FINANCE & ECONOMY MINISTER', ('Poland','Baranowski'): 'TRADE & ECONOMIC SECURITY',
    ('Poland','Paszyk'): 'ECONOMIC DEVELOPMENT & TECHNOLOGY',
    ('Russia','Alikhanov'): 'INDUSTRY & TRADE MINISTER', ('Russia','Reshetnikov'): 'TRADE POLICY & NEGOTIATIONS',
    ('Saudi Arabia','Al-Qasabi'): 'COMMERCE MINISTER', ('Saudi Arabia','Al-Abduljabbar'): 'FOREIGN TRADE AUTHORITY (GAFT)',
    ('South Korea','Kim Jung-kwan'): 'TRADE, INDUSTRY & RESOURCES', ('South Korea','Yeo Han-koo'): 'TRADE NEGOTIATIONS',
    ('United Kingdom','Kyle'): 'SECRETARY OF STATE · BOARD OF TRADE', ('United Kingdom','Bryant'): 'TRADE POLICY & ECONOMIC SECURITY',
    ('United States','Kratsios'): 'WHITE HOUSE OSTP · S&T POLICY', ('United States','Roth'): 'NTIA · TELECOM & BROADBAND',
    ('United States','Lutnick'): 'SECRETARY OF COMMERCE', ('United States','Greer'): 'U.S. TRADE REPRESENTATIVE',
    ('Argentina','Quirno'): 'FOREIGN AFFAIRS & INTERNATIONAL TRADE', ('Argentina','Lavigne'): 'DOMESTIC COMMERCE & INDUSTRY',
    ('Australia','Charlton'): 'SCIENCE, TECH & THE DIGITAL ECONOMY', ('Australia','Ayres'): 'INDUSTRY, INNOVATION & SCIENCE',
    ('China','Yin'): 'SCIENCE & TECHNOLOGY (MOST)',
}

def role_tag(country, name, role_label=''):
    for (c, sub), tag in ROLE_TAGS.items():
        if c == country and sub in name:
            return tag
    t = re.split(r'[/(]', role_label or '')[0].strip().upper()
    return (t[:34] or None)

# ---------- 1. display plan for non-verify countries ----------
for (country, portfolio), plan in PLAN.items():
    offs = CO[country]['digital_ministers' if portfolio == 'digital' else 'trade_ministers']
    order = []
    for sub, disp in plan:
        hit = next((o for o in offs if sub in o['name']), None)
        if hit is None:
            raise SystemExit(f'plan miss: {country}/{portfolio}/{sub}')
        if disp == 'omit':
            offs.remove(hit)
            continue
        hit['display'] = disp
        if disp == 'half':
            hit['role_tag'] = role_tag(country, hit['name'], hit.get('role_label',''))
        order.append(hit)
    for o in offs:            # anything unplanned becomes a note
        if o not in order:
            o['display'] = 'note'; order.append(o)
    offs[:] = order
    order[0]['is_primary'] = True
    for o in order[1:]: o['is_primary'] = False

# ---------- 2. verified roster changes ----------
def rec_from_verify(country, o):
    return {
        'name': o['name'].strip(), 'title': o['title'].strip(), 'ministry': o['ministry'].strip(),
        'assumed_office': (o.get('assumed_office') or '').strip(),
        'bio': (o.get('bio_short') or '').strip(), 'bio_display': (o.get('bio_short') or '').strip(),
        'source_url': o.get('source_url',''), 'as_of': o.get('as_of','2026-07-16'),
        'confidence': o.get('confidence','Needs check'),
        'is_acting': bool(o.get('is_vacant_or_acting')),
        'role_label': o.get('role_label',''),
        'display': o.get('display','full'),
        'role_tag': role_tag(country, o['name'], o.get('role_label','')) if o.get('display')=='half' else None,
        'is_primary': False,
    }

VER = {v['country']: v['verify'] for v in U.get('verifies', []) if v.get('verify')}
roster_answers = {}
for country, v in VER.items():
    c = CO[country]
    roster_answers[country] = v.get('answer','')
    for portfolio, key in (('digital','digital_ministers'), ('trade','trade_ministers')):
        news = [rec_from_verify(country, o) for o in v['officials'] if o['portfolio'] == portfolio]
        if not news:
            continue
        # keep long bios from the previous record when the same person stays
        old = {norm_name(o['name']): o for o in c[key]}
        for n in news:
            prev = old.get(norm_name(n['name']))
            if prev:
                n['bio'] = prev.get('bio') or n['bio']
                if n['display'] == 'full':
                    n['bio_display'] = prev.get('bio') or n['bio_display']
        news[0]['is_primary'] = True
        c[key] = news
    if v.get('division_note_digital'): c['div_note_digital'] = v['division_note_digital']
    if v.get('division_note_trade'): c['div_note_trade'] = v['division_note_trade']
    if v.get('corrections'):
        c.setdefault('gaps', []).extend(v['corrections'])

# Russia: user asked for Alikhanov prominent — put him in the left column
ru = CO['Russia']['trade_ministers']
ru.sort(key=lambda o: 0 if 'Alikhanov' in o['name'] else 1)
if ru: ru[0]['is_primary'] = True
for o in ru[1:]: o['is_primary'] = False

# ---------- 3. compressed bios ----------
def sentence_trim(bio, max_words=58):
    """Fallback compression: keep whole leading sentences up to the word budget.
    Pure truncation — never invents content."""
    words = bio.split()
    if len(words) <= max_words:
        return bio
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

trims = {t['key']: t['bio_short'] for t in U.get('trims', []) if t}
import os as _os
if _os.path.exists(ROOT + 'data/_trim_output.json'):
    for t in json.load(open(ROOT + 'data/_trim_output.json')):
        trims[t['key']] = t['bio_short']
matched = fallback = 0
for c in D['countries']:
    for key in ('digital_ministers','trade_ministers'):
        for o in c[key]:
            k = f"{c['country']}|{o['name']}"
            if k in trims and o.get('display') != 'full':
                o['bio_display'] = trims[k].strip(); matched += 1
            elif o.get('display') == 'full' and o.get('bio'):
                o['bio_display'] = o['bio']   # full-width profiles carry the richer bio (budget pass below)
            elif o.get('display') == 'half' and len((o.get('bio_display') or '').split()) < 26 and len((o.get('bio') or '').split()) > len((o.get('bio_display') or '').split()):
                o['bio_display'] = sentence_trim(o['bio']); fallback += 1
            elif o.get('display') == 'half' and not o.get('bio_display'):
                o['bio_display'] = sentence_trim(o.get('bio','')); fallback += 1
            elif o.get('display') == 'full' and not o.get('bio_display'):
                o['bio_display'] = o.get('bio','')
print(f'trimmed bios: {matched} from agents, {fallback} sentence-trim fallback')

# hand-compressed bios where sentence splitting can't fit the box (compression only, no new facts)
BIO_OVERRIDES = {
    ('Canada','LeBlanc'): ("Dominic LeBlanc, a lawyer and Liberal MP for Beausejour since 2000, is a veteran "
        "minister who has held Fisheries, Intergovernmental Affairs, Public Safety and Finance. Since "
        "May 13, 2025 he has led the Canada-U.S. trade file as Privy Council President."),
}
for c in D['countries']:
    for key in ('digital_ministers','trade_ministers'):
        for o in c[key]:
            for (cn, sub), txt in BIO_OVERRIDES.items():
                if c['country'] == cn and sub in o['name']:
                    o['bio_display'] = txt

# enforce fit budgets (Open Sans metrics): half columns ~44 words; full profiles
# that carry an Also/division note ~62 words
for c in D['countries']:
    for key, div in (('digital_ministers','div_note_digital'), ('trade_ministers','div_note_trade')):
        offs = c[key]
        has_note = bool(c.get(div)) or any(o.get('display') == 'note' for o in offs)
        for o in offs:
            if o.get('display') == 'half':
                o['bio_display'] = sentence_trim(o.get('bio_display') or o.get('bio',''), 48)
            elif o.get('display') == 'full':
                o['bio_display'] = sentence_trim(o.get('bio_display') or o.get('bio',''), 75 if has_note else 92)

# ---------- 4. portraits ----------
port_by_name = {}
for entry in U.get('portraits', []):
    p = entry.get('portraits') or {}
    for r in p.get('results', []):
        if r.get('status') == 'ok' and r.get('file'):
            port_by_name[norm_name(r['name'])] = r
slug_by_name = {}
for t in TARGETS:
    for o in t['officials']:
        slug_by_name[norm_name(o['name'])] = o['slug']

ok_p = miss_p = 0
for c in D['countries']:
    for key in ('digital_ministers','trade_ministers'):
        for o in c[key]:
            if o.get('display') == 'note':
                continue
            nn = norm_name(o['name'])
            hit = port_by_name.get(nn)
            slug = slug_by_name.get(nn) or (hit.get('slug') if hit else None)
            if not slug:  # new official from verify without a pre-assigned slug
                last = re.sub(r'[^a-z]', '', norm_name(o['name'].split()[-1]))
                slug = f"{norm_name(c['country'])[:10]}-{last}"
            o['portrait_slug'] = slug
            if hit:
                o['portrait_raw'] = hit['file']
                o['portrait_source'] = hit.get('source_url','')
                o['portrait_status'] = 'ok'; ok_p += 1
            else:
                o['portrait_raw'] = None
                o['portrait_status'] = 'missing'; miss_p += 1
print(f'portraits mapped: {ok_p} ok, {miss_p} missing (placeholders will be generated)')

# Brazil: Ferraz removed per preparer direction — scrub from workbook source notes
br = CO['Brazil']
br['source_notes'] = re.sub(r'[^.]*Lucas Pedreira[^.]*\.\s*', '', br.get('source_notes',''))
br.setdefault('gaps', [])

# ---------- 5. US world totals ----------
ut = U.get('usTotals') or {}
us = CO['United States']
if ut.get('exports_goods_world_b') is not None:
    us['us_world_exports_b'] = round(float(ut['exports_goods_world_b']), 1)
    us['us_world_imports_b'] = round(float(ut['imports_goods_world_b']), 1)
    us['us_world_balance_b'] = round(float(ut['balance_goods_world_b']), 1)
    D['meta']['us_world'] = {k: ut.get(k) for k in ('reference_year','source','source_url','as_of','notes')}
    diff = abs((us['us_world_exports_b'] - us['us_world_imports_b']) - us['us_world_balance_b'])
    if diff > 0.25:
        us.setdefault('gaps', []).append(
            f"US world totals: exports−imports differs from released balance by ${diff:.1f}B (rounding in release).")

# ---------- 6. seal ----------
seal = U.get('seal') or {}
_sf = seal.get('file') if seal.get('status') == 'ok' else None
if _sf and _sf.startswith(ROOT): _sf = _sf[len(ROOT):]
D['meta']['seal_file'] = _sf
D['meta']['seal_source'] = seal.get('source_url','')

# ---------- 7. roll-up + roster reference for QA ----------
for c in D['countries']:
    offs = c['digital_ministers'] + c['trade_ministers']
    acting = any(o.get('is_acting') and o.get('display') != 'note' for o in offs)
    needs = (any(o.get('confidence') == 'Needs check' for o in offs)
             or c['overall_balance_confidence'] != 'Verified'
             or str(c.get('gdp_confidence','')).lower() == 'low'
             or str(c.get('us_trade_confidence','')).lower() == 'low')
    c['row_confidence'] = 'Vacant / acting' if acting else ('Needs check' if needs else 'Verified')

ref = []
for c in D['countries']:
    for key in ('digital_ministers','trade_ministers'):
        for o in c[key]:
            ref.append({'country': c['country'], 'name': o['name'], 'title': o['title'],
                        'ministry': o['ministry'], 'source_url': o.get('source_url','')})
json.dump(ref, open(ROOT + 'data/_roster_reference.json', 'w'), indent=1, ensure_ascii=False)

json.dump(D, open(ROOT + 'data/g20.json', 'w'), indent=2, ensure_ascii=False)
print('Wrote data/g20.json (v2).')
print('\nVerification answers:')
for k, a in roster_answers.items():
    print(f'--- {k}: {a}\n')

#!/usr/bin/env python3
"""Normalize data/_research.json -> data/g20.json (single source of truth)."""
import json, re

R = json.load(open('/home/user/Photo/data/_research.json'))
raw = [x for x in R['countries'] if x]
TD = {t['country'].split(' (')[0]: t for t in R['tradeData']['countries']}
GD = {g['country'].split(' (')[0]: g for g in R['gdpData']['countries']}
US_CONTAM = ('Lutnick', 'Greer')

def norm(n): return n.split(' (')[0]
def r1(v): return None if v is None else round(float(v), 1)

# ---- flag files ----
SLUG = {'Argentina':'argentina','Australia':'australia','Brazil':'brazil','Canada':'canada',
    'China':'china','France':'france','Germany':'germany','India':'india','Indonesia':'indonesia',
    'Italy':'italy','Japan':'japan','Mexico':'mexico','Poland':'poland','Russia':'russia',
    'Saudi Arabia':'saudi-arabia','South Korea':'south-korea','Türkiye':'turkiye',
    'United Kingdom':'united-kingdom','United States':'united-states'}

# ---- primary-minister selection (plan.md §4) ----
def pick_digital_primary(country, offs):
    if country == 'Türkiye':
        for i,o in enumerate(offs):
            if 'Kacır' in o.get('name','') or 'Industry and Technology' in o.get('title',''):
                return i
    return 0
def pick_trade_primary(country, offs):
    return 0  # research already lists the lead cabinet minister first

def clean_officials(country, offs):
    if country.startswith('United States'):
        return offs
    return [o for o in offs if not any(u in o.get('name','') for u in US_CONTAM)]

def off_rec(o, primary):
    return {
        'name': o.get('name','').strip(),
        'title': o.get('title','').strip(),
        'ministry': o.get('ministry','').strip(),
        'assumed_office': (o.get('assumed_office') or '').strip(),
        'bio': (o.get('bio') or '').strip(),
        'source_url': o.get('source_url',''),
        'as_of': o.get('as_of','2026-07-16'),
        'confidence': o.get('confidence','Needs check'),
        'is_acting': bool(o.get('is_vacant_or_acting')),
        'role_label': o.get('role_label',''),
        'is_primary': primary,
    }

def clean_year(s):
    s = (s or '').strip()
    if s.startswith('FY'): return re.sub(r'\s*\(.*\)','',s)
    m = re.match(r'(\d{4})', s)
    return m.group(1) if m else s

def rollup(digs, trades, otb_conf, gdp_conf, ust_conf):
    if any(o['is_acting'] for o in digs+trades): return 'Vacant / acting'
    needs = (any(o['confidence']=='Needs check' or '[TO VERIFY]' in o['name'] for o in digs+trades)
             or otb_conf != 'Verified'
             or str(gdp_conf).lower()=='low' or str(ust_conf).lower()=='low')
    return 'Needs check' if needs else 'Verified'

countries_out = []
for x in raw:
    name = norm(x['country'])
    digs_raw = x['digital_officials']
    trades_raw = clean_officials(x['country'], x['trade_officials'])
    di = pick_digital_primary(name, digs_raw)
    ti = pick_trade_primary(name, trades_raw)
    digs = [off_rec(o, i==di) for i,o in enumerate(digs_raw)]
    trades = [off_rec(o, i==ti) for i,o in enumerate(trades_raw)]
    # move primary first for stable rendering
    digs.sort(key=lambda o: (not o['is_primary']))
    trades.sort(key=lambda o: (not o['is_primary']))

    otb = x['overall_trade_balance']
    g = GD.get(name, {}); t = TD.get(name, {})
    is_us = name == 'United States'
    exp = None if is_us else r1(t.get('us_exports_to_billions'))
    imp = None if is_us else r1(t.get('us_imports_from_billions'))
    bil = None if (exp is None or imp is None) else round(exp - imp, 1)

    # split notes
    def split_note(offs, kind):
        extra = [o for o in offs if not o['is_primary']]
        if not extra: return ''
        parts = [f"{o['name']} ({o['title']})" for o in extra]
        return f"{kind} portfolio also held by: " + '; '.join(parts) + '.'
    sd = split_note(digs, 'Digital/technology')
    st = split_note(trades, 'Trade/commerce')
    # bespoke division-of-responsibility phrasing
    DIV = {
      ('United States','trade'): "Howard Lutnick (Secretary of Commerce) leads trade/industrial policy & export controls; Jamieson Greer (U.S. Trade Representative, ambassador rank) is the chief trade negotiator.",
      ('Argentina','trade'): "Domestic commerce/industry (Lavigne, acting) sits under the Economy Ministry; external trade negotiation (Brun) under the Foreign Ministry.",
      ('Türkiye','digital'): "No standalone digital ministry: cybersecurity (Önal, Cybersecurity Presidency) and telecom/digital infrastructure (Uraloğlu, Transport & Infrastructure) sit outside the Industry & Technology Ministry.",
      ('China','trade'): "Commerce Minister Wang Wentao leads MOFCOM; Li Chenggang is the full-rank China International Trade Representative (chief negotiator).",
      ('India','trade'): "Cabinet Minister Goyal leads Commerce & Industry; Commerce Secretary Agrawal is the senior civil servant and chief India-US negotiator.",
    }
    div_d = DIV.get((name,'digital'), '')
    div_t = DIV.get((name,'trade'), '')

    # gaps
    gaps = []
    if any(o['is_acting'] for o in digs+trades):
        for o in digs+trades:
            if o['is_acting']:
                gaps.append(f"{o['name']} is acting/interim as {o['title']} ({kind_of(o)})" if False else f"Acting/interim official: {o['name']} — {o['title']}")
    if otb.get('confidence') != 'Verified':
        gaps.append(f"Overall trade balance ({otb.get('basis')}, {clean_year(otb.get('reference_year'))}) flagged '{otb.get('confidence')}'.")
    if str(g.get('confidence','')).lower() == 'low':
        gaps.append("GDP value low-confidence (secondary IMF-based aggregator; may reflect Apr-2026 WEO revision).")
    if str(t.get('confidence','')).lower() in ('low','medium'):
        gaps.append(f"U.S. bilateral goods figures {t.get('confidence')}-confidence (EU member without standalone USTR fact sheet).")
    if otb.get('basis') == 'goods+services':
        gaps.append("Overall balance is goods+services (not goods-only) — basis differs from other countries.")
    if clean_year(otb.get('reference_year')).startswith('FY'):
        gaps.append(f"Overall balance uses fiscal year {clean_year(otb.get('reference_year'))}, not calendar 2025.")

    # source notes
    sn = []
    if sd: sn.append(sd)
    if st: sn.append(st)
    if div_t and not st: sn.append(div_t)
    if otb.get('notes'): sn.append("Balance: " + otb['notes'][:400])
    src_notes = ' '.join(sn)

    countries_out.append({
        'country': name,
        'flag_file': f"assets/flags/{SLUG[name]}.png",
        'gdp_usd_b': r1(g.get('gdp_usd_billions')),
        'gdp_year': clean_year(g.get('reference_year','2025')),
        'gdp_confidence': g.get('confidence',''),
        'overall_balance_usd_b': r1(otb.get('value_usd_billions')),
        'overall_balance_basis': otb.get('basis',''),
        'overall_balance_year': clean_year(otb.get('reference_year','')),
        'overall_balance_confidence': otb.get('confidence',''),
        'overall_balance_url': otb.get('source_url',''),
        'us_exports_usd_b': exp,
        'us_imports_usd_b': imp,
        'us_bilateral_usd_b': bil,
        'us_trade_year': clean_year(t.get('reference_year','2025')) if not is_us else '2025',
        'us_trade_confidence': t.get('confidence','') if not is_us else 'n/a',
        'digital_ministers': digs,
        'trade_ministers': trades,
        'div_note_digital': div_d,
        'div_note_trade': div_t,
        'row_confidence': rollup(digs, trades, otb.get('confidence'), g.get('confidence'), t.get('confidence')),
        'source_notes': src_notes,
        'gaps': gaps,
    })

countries_out.sort(key=lambda c: c['country'])

out = {
  'meta': {
    'compiled': '2026-07-16',
    'scope_note': ('19 G20 sovereign members. Poland substituted for South Africa per instruction. '
                   'European Union and African Union bloc seats excluded.'),
    'gdp': {
      'source': R['gdpData'].get('source',''),
      'source_url': R['gdpData'].get('source_url',''),
      'reference_year': '2025', 'as_of': R['gdpData'].get('as_of','2026-07-16'),
      'units': 'USD billions, nominal (current prices)'},
    'us_trade': {
      'source': R['tradeData'].get('source',''),
      'source_url': R['tradeData'].get('source_url',''),
      'reference_year': '2025', 'basis': 'goods only', 'as_of': R['tradeData'].get('as_of','2026-07-16'),
      'units': 'USD billions'},
    'flags': {'source': 'hampusborgos/country-flags (public domain), raster via cairosvg — Wikimedia Commons was egress-blocked in the build environment',
              'note': 'Uniform 400px height, true aspect ratios preserved.'},
    'convention': 'U.S. bilateral balance = U.S. exports to country minus U.S. imports from country; negative = U.S. deficit.',
  },
  'countries': countries_out,
}

json.dump(out, open('/home/user/Photo/data/g20.json','w'), indent=2, ensure_ascii=False)
print("Wrote data/g20.json —", len(countries_out), "countries")
print("Row flags:", {c['country']: c['row_confidence'] for c in countries_out if c['row_confidence']!='Verified'})

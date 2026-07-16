#!/usr/bin/env python3
"""Generate output/GAPS.md from data/g20.json — every unverified / flagged item."""
import json
D=json.load(open('/home/user/Photo/data/g20.json')); CO=D['countries']
o=[]; w=o.append
w("# GAPS & Uncertainty Register — G20 Ministers & Trade Deck")
w("")
w("Compiled 2026-07-16. Every item a reviewer should chase down before external use. "
  "Nothing here is a fabricated placeholder — all officeholders resolved to a named person; "
  "these are data-vintage, basis, precision, and acting-status flags. "
  "Cross-references: full sourcing in `research/g20-research.md`; structured data in `data/g20.json`.")
w("")
nc=[c for c in CO if c['row_confidence']=='Needs check']
va=[c for c in CO if c['row_confidence']=='Vacant / acting']
w(f"**Roll-up:** {sum(1 for c in CO if c['row_confidence']=='Verified')} Verified · "
  f"{len(nc)} Needs check · {len(va)} Vacant/acting (of 19).")
w("")
w("## Per-country flags")
w("")
w("| Country | Flag | Specific gaps to verify |")
w("|---|---|---|")
for c in CO:
    if c['gaps']:
        gaps=' '.join(f"({i+1}) {g}" for i,g in enumerate(c['gaps']))
        w(f"| {c['country']} | {c['row_confidence']} | {gaps} |")
w("")
w("## Acting / interim officials (carry the flag through to any external version)")
w("")
for c in CO:
    for grp in ('digital_ministers','trade_ministers'):
        for off in c[grp]:
            if off.get('is_acting'):
                w(f"- **{c['country']} — {off['name']}**, {off['title']} ({off['ministry']}). "
                  f"Flagged *Vacant / acting*. {off.get('notes','')[:200] if off.get('notes') else 'Held on an acting/interim basis; confirm permanent appointment.'}")
w("")
w("## Cross-cutting data caveats")
w("")
w("- **GDP low-confidence (6):** Argentina, Australia, Brazil, Mexico, Poland, Saudi Arabia — sourced from a "
  "secondary IMF-based aggregator; may reflect the later Apr-2026 WEO revision. Confirm against the primary IMF WEO table.")
w("- **U.S. bilateral goods below high confidence:** France (low), Germany/Italy/Poland (medium) — EU members without a "
  "standalone USTR fact sheet; sourced via the Census/COMTRADE mirror. Confirm against census.gov country pages.")
w("- **Basis exceptions:** Australia's overall balance is goods+services; India's is fiscal year 2025-26. All others goods-only, calendar 2025.")
w("- **Currency conversion:** Overall balances for Australia, Canada, France, Germany, Italy, Japan, Poland, Saudi Arabia and the UK are "
  "converted from local currency (EUR/GBP/CAD/AUD/JPY/SAR) at approximate 2025 average rates; USD values carry exchange-rate uncertainty.")
w("- **Primary-source reachability:** census.gov, imf.org and many national statistics/government sites returned HTTP 403 to automated "
  "fetching in the build environment. Figures came from official-data-derived channels (USTR fact sheets, Trading Economics' Census/COMTRADE "
  "mirror, StatisticsTimes' IMF-WEO tabulation), not read directly off the primary agency page. Re-confirm headline figures against primary sources before publication.")
w("- **Flags:** Wikimedia Commons was egress-blocked; flag images are from the public-domain hampusborgos/country-flags repository.")
w("")
w("## Data-quality correction applied during QA")
w("")
w("- **Saudi Arabia:** the raw research wrongly included the U.S. Secretary of Commerce and U.S. Trade Representative in Saudi Arabia's "
  "trade-officials list (context bleed from U.S.-specific instructions). Removed; Saudi Arabia's trade officials are the Minister of "
  "Commerce (Al-Qasabi) and the acting GAFT Governor (Al-Abduljabbar).")
w("")
_missing=[(c['country'],o['name'],o.get('title','')) for c in CO for g in ('digital_ministers','trade_ministers')
          for o in c[g] if o.get('display') in ('full','half') and o.get('portrait_status')=='placeholder']
if _missing:
    for cn,nm,ti in _missing:
        w(f"- **{cn}** — {nm} ({ti}): official portrait not retrievable from this environment; drop a photo at `assets/portraits/` and rerun `scripts/build.sh`.")
else:
    w("- None — every displayed official has an official portrait embedded.")
w("")
w("## Bloc annex (EU & African Union)")
w("")
for b in D.get('blocs', []):
    if b.get('gaps'):
        for g in b['gaps']:
            w(f"- **{b['country']}** — {g}")
    else:
        w(f"- **{b['country']}** — no flags; all items verified.")
    for inc in b.get('inconsistencies', [])[:4]:
        w(f"  - note: {inc[:220]}")
w("")
w("## Name spellings to preserve exactly (incl. diacritics)")
w("")
w("- Türkiye, Darío Leandro Genua, José Antonio Peña Merino, Katherina Reiche, Maroš Šefčovič, Mehmet Fatih Kacır, "
  "Abdulkadir Uraloğlu, Andrzej Domański, Michał Baranowski, Krzysztof Gawkowski, Márcio Fernando Elias Rosa.")
w("- Romanization variants (form used shown first): Bae Kyung-hoon / Baek; Kim Jung-kwan / Jeong-kwan; Rajesh Agrawal / Agarwal.")
w("")
open('/home/user/Photo/output/GAPS.md','w').write("\n".join(o)+"\n")
print("Wrote output/GAPS.md —", len(o), "lines")

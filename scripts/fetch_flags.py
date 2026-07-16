#!/usr/bin/env python3
"""Download G20 flag SVGs (public-domain, hampusborgos/country-flags) and rasterize
to uniform-height PNGs preserving true aspect ratio. Placeholder + log on failure."""
import os, subprocess, io, json
import cairosvg
from PIL import Image

DEST = '/home/user/Photo/assets/flags'
os.makedirs(DEST, exist_ok=True)
H = 400  # raster height in px; width scales to true aspect ratio
BASE = 'https://raw.githubusercontent.com/hampusborgos/country-flags/main/svg'

# country -> (iso2 code, filename slug)
FLAGS = [
    ('Argentina','ar','argentina'), ('Australia','au','australia'), ('Brazil','br','brazil'),
    ('Canada','ca','canada'), ('China','cn','china'), ('France','fr','france'),
    ('Germany','de','germany'), ('India','in','india'), ('Indonesia','id','indonesia'),
    ('Italy','it','italy'), ('Japan','jp','japan'), ('Mexico','mx','mexico'),
    ('Poland','pl','poland'), ('Russia','ru','russia'), ('Saudi Arabia','sa','saudi-arabia'),
    ('South Korea','kr','south-korea'), ('Türkiye','tr','turkiye'),
    ('United Kingdom','gb','united-kingdom'), ('United States','us','united-states'),
]

def curl(url, out):
    r = subprocess.run(['curl','-sS','--fail','--retry','3','--retry-delay','2',
                        '--max-time','40','-o',out,url], capture_output=True, text=True)
    return r.returncode == 0 and os.path.exists(out) and os.path.getsize(out) > 100

results = {}
for country, cc, slug in FLAGS:
    svg = f'{DEST}/_{slug}.svg'
    png = f'{DEST}/{slug}.png'
    ok = False; err = ''
    try:
        if curl(f'{BASE}/{cc}.svg', svg):
            cairosvg.svg2png(bytestring=open(svg,'rb').read(), write_to=png, output_height=H)
            im = Image.open(png); im.load()
            results[country] = {'status':'ok','size':im.size,'file':f'assets/flags/{slug}.png'}
            ok = True
        else:
            err = 'download failed'
    except Exception as e:
        err = f'{type(e).__name__}: {e}'
    finally:
        if os.path.exists(svg): os.remove(svg)
    if not ok:
        results[country] = {'status':'FAILED','error':err,'file':f'assets/flags/{slug}.png','slug':slug}
        print(f'  !! {country} ({cc}): {err}')

json.dump(results, open('/home/user/Photo/data/_flags_status.json','w'), indent=2, ensure_ascii=False)
okc = sum(1 for v in results.values() if v['status']=='ok')
print(f'\n{okc}/{len(FLAGS)} flags OK')
for country,cc,slug in FLAGS:
    v=results[country]
    if v['status']=='ok':
        w,h=v['size']; print(f'  {country:<20} {w}x{h}  ar={w/h:.2f}')

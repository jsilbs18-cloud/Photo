#!/usr/bin/env python3
"""Portrait drop-in support: if a photo exists at assets/portraits/<slug>.(png|jpg|jpeg)
for a displayed official, crop it to 4:5 (h=500), write <slug>.png, and stamp
portrait_file into data/g20.json. No photo -> no portrait (compact text layout).
Drop photos in from a network that can reach official sources, then rerun build.sh."""
import json, os
from PIL import Image

ROOT = '/home/user/Photo/'
W, H = 400, 500

def normalize(src, dst):
    im = Image.open(src).convert('RGB')
    target = W / H
    ar = im.width / im.height
    if ar > target:
        nw = int(im.height * target); x0 = (im.width - nw) // 2
        im = im.crop((x0, 0, x0 + nw, im.height))
    elif ar < target:
        im = im.crop((0, 0, im.width, int(im.width / target)))
    im.resize((W, H), Image.LANCZOS).save(dst, 'PNG')

def main():
    D = json.load(open(ROOT + 'data/g20.json'))
    found = 0
    for c in D['countries'] + D.get('blocs', []):
        for grp in ('digital_ministers', 'trade_ministers'):
            for o in c[grp]:
                o['portrait_file'] = None
                if o.get('display') == 'note':
                    continue
                slug = o.get('portrait_slug')
                if not slug:
                    continue
                png = ROOT + f'assets/portraits/{slug}.png'
                src = next((ROOT + f'assets/portraits/{slug}{ext}' for ext in ('.png', '.jpg', '.jpeg')
                            if os.path.exists(ROOT + f'assets/portraits/{slug}{ext}')), None)
                if src:
                    normalize(src, png)
                    o['portrait_file'] = f'assets/portraits/{slug}.png'
                    found += 1
    json.dump(D, open(ROOT + 'data/g20.json', 'w'), indent=2, ensure_ascii=False)
    print(f'portraits embedded: {found} (drop photos into assets/portraits/<slug>.png and rerun to add more)')

if __name__ == '__main__':
    main()

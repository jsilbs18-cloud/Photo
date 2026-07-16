#!/usr/bin/env python3
"""Normalize downloaded official portraits to uniform 4:5 PNGs (h=500) and
generate a monogram placeholder for any official whose portrait failed.
Reads data/g20.json (v2, with portrait_file/portrait_status per official)."""
import json, os
from PIL import Image, ImageDraw, ImageFont

ROOT = '/home/user/Photo/'
W, H = 400, 500  # 4:5
SLATE = (0x44, 0x54, 0x6A)
NAVY = (0x1F, 0x38, 0x64)
FONT = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'

def normalize(src, dst):
    im = Image.open(ROOT + src).convert('RGB')
    # center-crop to 4:5
    ar = im.width / im.height
    target = W / H
    if ar > target:  # too wide
        nw = int(im.height * target)
        x0 = (im.width - nw) // 2
        im = im.crop((x0, 0, x0 + nw, im.height))
    elif ar < target:  # too tall — favor the top (faces sit high in portraits)
        nh = int(im.width / target)
        im = im.crop((0, 0, im.width, nh))
    im = im.resize((W, H), Image.LANCZOS)
    im.save(ROOT + dst, 'PNG')

def initials(name):
    parts = [p for p in name.replace('-', ' ').split() if p and p[0].isalpha()]
    keep = [p for p in parts if p[0].isupper()] or parts
    return ''.join(p[0] for p in keep[:2]).upper() or '?'

def placeholder(name, dst):
    im = Image.new('RGB', (W, H), SLATE)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W - 1, H - 1], outline=NAVY, width=6)
    txt = initials(name)
    f = ImageFont.truetype(FONT, 150)
    bb = d.textbbox((0, 0), txt, font=f)
    d.text(((W - bb[2] + bb[0]) / 2 - bb[0], (H - bb[3] + bb[1]) / 2 - bb[1] - 20), txt, font=f, fill='white')
    f2 = ImageFont.truetype(FONT, 26)
    lab = 'PORTRAIT PENDING'
    bb2 = d.textbbox((0, 0), lab, font=f2)
    d.text(((W - bb2[2]) / 2, H - 70), lab, font=f2, fill=(0xC7, 0xD3, 0xE8))
    im.save(ROOT + dst, 'PNG')

def main():
    D = json.load(open(ROOT + 'data/g20.json'))
    changed = failed = 0
    for c in D['countries']:
        for grp in ('digital_ministers', 'trade_ministers'):
            for o in c[grp]:
                if o.get('display') == 'note':
                    continue
                slug = o.get('portrait_slug')
                if not slug:
                    continue
                dst = f'assets/portraits/{slug}.png'
                raw = o.get('portrait_raw')  # as downloaded by the workflow agent
                if raw and os.path.exists(ROOT + raw):
                    try:
                        normalize(raw, dst)
                        o['portrait_file'] = dst
                        changed += 1
                        continue
                    except Exception as e:
                        print(f'  !! normalize failed {slug}: {e}')
                placeholder(o['name'], dst)
                o['portrait_file'] = dst
                o['portrait_status'] = 'placeholder'
                failed += 1
                print(f'  placeholder: {c["country"]} / {o["name"]}')
    json.dump(D, open(ROOT + 'data/g20.json', 'w'), indent=2, ensure_ascii=False)
    print(f'normalized {changed}, placeholders {failed}')

if __name__ == '__main__':
    main()

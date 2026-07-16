#!/usr/bin/env python3
"""Portrait pipeline: for every displayed official (countries + blocs),
- if a real photo exists at assets/portraits/<slug>.(png|jpg|jpeg), crop to 4:5 and embed it;
- otherwise render an ITA-styled monogram placeholder (Trade Slate / Trade Navy).
Drop real photos in (see the manifest in output/GAPS.md) and rerun scripts/build.sh."""
import json, os
from PIL import Image, ImageDraw, ImageFont

ROOT = '/home/user/Photo/'
W, H = 400, 500
SLATE = (0xB1, 0xBB, 0xCA)
NAVY = (0x0A, 0x31, 0x4D)
FONT = '/usr/local/share/fonts/ita/OpenSans-Bold.ttf'

def normalize(src, dst):
    im = Image.open(src).convert('RGB')
    target = W / H
    ar = im.width / im.height
    if ar > target:
        nw = int(im.height * target); x0 = (im.width - nw) // 2
        im = im.crop((x0, 0, x0 + nw, im.height))
    elif ar < target:
        im = im.crop((0, 0, im.width, int(im.width / target)))
    if im.width > W:
        im = im.resize((W, H), Image.LANCZOS)
    im.save(dst, 'PNG')

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
    d.text(((W - bb[2] + bb[0]) / 2 - bb[0], (H - bb[3] + bb[1]) / 2 - bb[1] - 20), txt, font=f, fill=NAVY)
    f2 = ImageFont.truetype(FONT, 26)
    lab = 'PORTRAIT PENDING'
    bb2 = d.textbbox((0, 0), lab, font=f2)
    d.text(((W - bb2[2]) / 2, H - 70), lab, font=f2, fill=NAVY)
    im.save(dst, 'PNG')

def main():
    os.makedirs(ROOT + 'assets/portraits', exist_ok=True)
    D = json.load(open(ROOT + 'data/g20.json'))
    real = ph = 0
    for c in D['countries'] + D.get('blocs', []):
        for grp in ('digital_ministers', 'trade_ministers'):
            for o in c[grp]:
                o['portrait_file'] = None
                if o.get('display') == 'note' or not o.get('portrait_slug'):
                    continue
                slug = o['portrait_slug']
                src = next((ROOT + f'assets/portraits/{slug}{ext}' for ext in ('.jpg', '.jpeg', '.png')
                            if os.path.exists(ROOT + f'assets/portraits/{slug}{ext}')), None)
                if src and not os.path.basename(src).startswith('_ph-'):
                    dst = ROOT + f'assets/portraits/{slug}.png'
                    if src != dst or Image.open(src).size != (W, H):
                        normalize(src, dst)
                    o['portrait_file'] = f'assets/portraits/{slug}.png'
                    real += 1
                else:
                    dst_rel = f'assets/portraits/_ph-{slug}.png'
                    if not os.path.exists(ROOT + dst_rel):
                        placeholder(o['name'], ROOT + dst_rel)
                    o['portrait_file'] = dst_rel
                    ph += 1
    json.dump(D, open(ROOT + 'data/g20.json', 'w'), indent=2, ensure_ascii=False)
    print(f'portraits: {real} real, {ph} placeholders (drop photos per GAPS.md manifest and rerun)')

if __name__ == '__main__':
    main()

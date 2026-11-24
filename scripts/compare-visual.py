"""Compare two visual-regression captures (docs/ui-review/visual/<before> vs <after>).

  python scripts\\compare-visual.py before after      (needs Pillow: pip install pillow)

For each screenshot it reports the share of pixels that differ (any channel by more than 24/255)
and a size change, and writes a red-highlighted diff image next to the "after" folder for every
page over the threshold. Live values (times, player codes) differ between runs, so review the
highlighted areas rather than expecting zero.
"""
import sys
from pathlib import Path

from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[1] / 'docs' / 'ui-review' / 'visual'
THRESHOLD = 0.002  # 0.2 % of pixels


def main(before, after):
    a_dir, b_dir = ROOT / before, ROOT / after
    diff_dir = ROOT / f'diff-{before}-{after}'
    diff_dir.mkdir(parents=True, exist_ok=True)
    flagged = 0
    for a_path in sorted(a_dir.glob('*.png')):
        b_path = b_dir / a_path.name
        if not b_path.exists():
            print(f'MISSING  {a_path.name}')
            flagged += 1
            continue
        a, b = Image.open(a_path).convert('RGB'), Image.open(b_path).convert('RGB')
        note = '' if a.size == b.size else f'  size {a.size} -> {b.size}'
        width, height = max(a.width, b.width), max(a.height, b.height)
        canvas_a = Image.new('RGB', (width, height), (255, 0, 255)); canvas_a.paste(a)
        canvas_b = Image.new('RGB', (width, height), (255, 0, 255)); canvas_b.paste(b)
        mask = ImageChops.difference(canvas_a, canvas_b).convert('L').point(lambda v: 255 if v > 24 else 0)
        changed = (mask.histogram()[255]) / (width * height)
        status = 'CHANGED' if changed > THRESHOLD or note else 'same'
        if status == 'CHANGED':
            flagged += 1
            overlay = canvas_b.copy()
            overlay.paste(Image.new('RGB', overlay.size, (255, 0, 0)), mask=mask)
            Image.blend(canvas_b, overlay, 0.6).save(diff_dir / a_path.name)
        print(f'{status:8} {changed * 100:6.2f}%  {a_path.name}{note}')
    print(f'\n{flagged} page(s) to review; diffs in {diff_dir}')
    return 1 if flagged else 0


if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:3]))

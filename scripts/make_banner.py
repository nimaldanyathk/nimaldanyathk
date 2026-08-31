#!/usr/bin/env python3
r"""Turn a name into ascii.svg — a self-typing ASCII wordmark.

The text-only counterpart to scripts/make_portrait.py: same self-typing
animation, same grey ink, same inlined typeface — but drawn from a figlet
banner instead of a photo, so it needs no headshot and no heavy image
dependencies. Run it once; it is not on a schedule.

    pip install pyfiglet
    python3 scripts/make_banner.py "NIMAL DANYATH"

Design notes, all inherited from the portrait so the page reads as one thing:

  * Grid metric. The advance width is pinned to exactly 0.600 em (CHAR_W 7.74
    at font-size 12.9) and JetBrains Mono (600/1000 units) is inlined as a
    base64 @font-face, so the wordmark is the same width for every viewer. An
    external font URL is not an option: the SVG loads through <img>, and
    browsers refuse subresource fetches for image documents.
  * Font subset. A figlet banner is drawn from printable ASCII only
    (_ | / \ ( ) . etc.), so the basic-latin subset jbmono-400.woff2 already
    covers every glyph — no ramp subset needed.
  * Motion is SMIL, because GitHub strips <script> from READMEs: each row is
    revealed by a clipPath wipe with a cursor block riding its edge, staggered
    top to bottom, frozen so it prints once and stops.
"""
import argparse
import base64
import os

import pyfiglet

# Kept in step with make_portrait.py so the two heroes share a grid.
FG_LIGHT = "#6e7681"       # readable on GitHub light — the portrait's grey
FG_DARK = "#c9d1d9"        # and its dark-mode step
FONT_SIZE = 14.2           # glyphs sit a hair taller than the row pitch...
LINE_H = 12.9              # ...so stacked █ rows overlap and leave no seam
CHAR_W = 8.52              # 0.600 em at FONT_SIZE — keep these in step
BASELINE = 11.3            # baseline drop inside a row; tuned so █ rows abut
ROW_DELAY = 0.09           # per-row stagger, seconds
PAD = 16
FONT = "ansi_regular"      # solid block letters — glyphs are just █, no seams
FAMILY = ("JBMono,ui-monospace,SFMono-Regular,Menlo,Consolas,"
          "&apos;Liberation Mono&apos;,monospace")
HERE = os.path.dirname(os.path.abspath(__file__))
# subset covers basic latin + box-drawing + block elements, so any
# ansi_shadow (or ASCII) wordmark renders with the advance pinned to 0.6 em
FONT_FILE = os.path.join(HERE, "fonts", "jbmono-banner.woff2")


def to_lines(text, font=FONT):
    """Render the wordmark and trim blank edge rows and the common left margin."""
    art = pyfiglet.figlet_format(text, font=font).replace("\t", "    ")
    lines = art.split("\n")
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    if not lines:
        raise SystemExit("empty banner")
    # drop the common leading whitespace so the wordmark hugs the left inset
    trim = min((len(l) - len(l.lstrip(" ")) for l in lines if l.strip()),
               default=0)
    return [l[trim:].rstrip() for l in lines]


def font_face():
    with open(FONT_FILE, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return (f"@font-face{{font-family:JBMono;font-style:normal;"
            f"font-weight:400;font-display:block;"
            f"src:url(data:font/woff2;base64,{b64}) format('woff2')}}")


def build_svg(lines):
    cols = max(len(l) for l in lines)
    width = int(cols * CHAR_W + PAD * 2)
    height = len(lines) * LINE_H + PAD * 2

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
         f'height="{height}" viewBox="0 0 {width} {height}" '
         f'font-family="{FAMILY}">',
         f'<style>{font_face()}.a{{fill:{FG_LIGHT}}}'
         f'@media(prefers-color-scheme:dark){{.a{{fill:{FG_DARK}}}}}</style>']

    for i, line in enumerate(lines):
        y = PAD + i * LINE_H
        if not line.strip():          # the gap between the two stacked names
            continue
        begin = f"{i * ROW_DELAY:.2f}s"
        end = f"{(i + 1) * ROW_DELAY:.2f}s"
        w = max(len(line), 1) * CHAR_W
        safe = (line.replace("&", "&amp;").replace("<", "&lt;")
                    .replace(">", "&gt;"))

        p.append(f'<clipPath id="c{i}"><rect x="{PAD}" y="{y}" '
                 f'height="{LINE_H}" width="0">'
                 f'<animate attributeName="width" from="0" to="{w:.1f}" '
                 f'begin="{begin}" dur="{ROW_DELAY}s" fill="freeze"/>'
                 f'</rect></clipPath>')
        p.append(f'<g clip-path="url(#c{i})"><text xml:space="preserve" '
                 f'x="{PAD}" y="{y + BASELINE:.2f}" class="a" '
                 f'font-size="{FONT_SIZE}">{safe}</text></g>')
        # the cursor: a slim block riding the wipe edge, gone once the row lands
        p.append(f'<rect y="{y + 0.5:.1f}" width="5" height="{LINE_H - 1:.1f}" '
                 f'class="a" opacity="0">'
                 f'<animate attributeName="x" from="{PAD}" to="{PAD + w:.1f}" '
                 f'begin="{begin}" dur="{ROW_DELAY}s" fill="freeze"/>'
                 f'<set attributeName="opacity" to="0.8" begin="{begin}"/>'
                 f'<set attributeName="opacity" to="0" begin="{end}"/></rect>')

    p.append("</svg>")
    return "".join(p)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("text", help="the wordmark; a newline stacks it, e.g. "
                                 "$'NIMAL\\nDANYATH K'")
    ap.add_argument("out", nargs="?", default="ascii.svg")
    ap.add_argument("--font", default=FONT,
                    help="figlet font (jbmono-banner.woff2 covers basic latin, "
                         "box-drawing and block glyphs)")
    ap.add_argument("--preview", action="store_true")
    args = ap.parse_args()

    lines = to_lines(args.text, font=args.font)
    if args.preview:
        print("\n".join(lines))
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(build_svg(lines))
    print(f"wrote {args.out} — {len(lines)} rows, "
          f"{max(len(l) for l in lines)} columns")


if __name__ == "__main__":
    main()

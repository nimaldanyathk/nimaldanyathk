#!/usr/bin/env python3
"""Draw stack.svg — the languages and tools as colourful brand-tinted chips.

A one-off, like scripts/make_banner.py: it takes no API data, just the lists
below, and writes a single self-contained SVG. Each chip is a solid pill in the
technology's brand colour with auto-contrasting text, a subtle edge that works
on GitHub light and dark, and a staggered fade-in in the same reveal language
as the rest of the page. The label font (JetBrains Mono) is inlined as base64,
so nothing here loads from a third party.

    python3 scripts/make_stack.py

Edit LANGUAGES / TOOLS to change the stack; colours are the chip fills.
"""
import base64
import json
import os

# name -> brand colour. Keep them mid-toned; near-black/near-white read poorly.
LANGUAGES = [
    ("python", "#3776AB"), ("java", "#E76F00"), ("c", "#5C7FA3"),
    ("c++", "#00599C"), ("javascript", "#E8C020"), ("html", "#E34F26"),
    ("css", "#1572B6"), ("matlab", "#E16737"),
]
TOOLS = [
    ("spring", "#6DB33F"), ("postman", "#FF6C37"), ("mysql", "#4479A1"),
    ("postgres", "#4169B0"), ("git", "#F05032"), ("github", "#5B6472"),
    ("vscode", "#0F80CC"), ("eclipse", "#6C4BB6"), ("arduino", "#00979D"),
    ("linux", "#D9A400"),
]

WIDTH = 620
FS = 12.5
CHAR_W = FS * 0.6          # 0.600 em — the page's shared advance
PADX = 11                  # chip horizontal padding
CHIP_H = 26
GAP = 8                    # between chips
ROW_GAP = 9                # between wrapped rows
LOGO = 13                  # brand mark, small and subtle
LGAP = 6                   # between mark and label
LABEL_FS = 10
DIM_LIGHT, DIM_DARK = "#8c959f", "#8b949e"
MONO = ("JBMono,ui-monospace,SFMono-Regular,Menlo,Consolas,"
        "&apos;Liberation Mono&apos;,monospace")
HERE = os.path.dirname(os.path.abspath(__file__))
FONT_FILE = os.path.join(HERE, "fonts", "jbmono-400.woff2")
LOGOS = json.load(open(os.path.join(HERE, "logos.json"), encoding="utf-8"))


def font_face():
    with open(FONT_FILE, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return (f"@font-face{{font-family:JBMono;font-style:normal;font-weight:400;"
            f"font-display:block;src:url(data:font/woff2;base64,{b64}) "
            f"format('woff2')}}")


def ink(hex_color):
    """Dark or white text, whichever reads on this chip colour."""
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return "#14181d" if lum > 0.62 else "#ffffff"


def logo_mark(name, x, y, fill):
    """The brand glyph, scaled into a LOGO-sized box and drawn in one colour.

    Monochrome and slightly transparent so it reads as a subtle mark on the
    coloured pill rather than competing with the label. Paths are inlined from
    scripts/logos.json — nothing is fetched at render time.
    """
    ico = LOGOS.get(name)
    if not ico:
        return "", 0.0
    s = LOGO / ico["vb"]
    paths = "".join(f'<path d="{d}"/>' for d in ico["paths"])
    g = (f'<g transform="translate({x:.1f} {y:.1f}) scale({s:.4f})" '
         f'fill="{fill}" opacity="0.9">{paths}</g>')
    return g, LOGO


def chip_width(name):
    has = name in LOGOS
    return (LOGO + LGAP if has else 0) + len(name) * CHAR_W + 2 * PADX


def chip(x, y, name, color, delay):
    w = chip_width(name)
    fg = ink(color)
    cx = x + PADX
    mark, mw = logo_mark(name, cx, y + (CHIP_H - LOGO) / 2, fg)
    tx = cx + (mw + LGAP if mw else 0)
    ty = y + CHIP_H / 2 + FS * 0.35
    g = (f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" '
         f'begin="{delay:.2f}s" dur="0.42s" fill="freeze"/>'
         f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{CHIP_H}" '
         f'rx="{CHIP_H / 2:.1f}" fill="{color}" class="pe"/>'
         f'{mark}'
         f'<text x="{tx:.1f}" y="{ty:.1f}" font-size="{FS}" '
         f'fill="{fg}">{name}</text></g>')
    return g, w


def flow(items, y, delay0):
    """Place chips left to right, wrapping at WIDTH. Returns (svg, next_y)."""
    parts, x, i = [], 0.0, 0
    for name, color in items:
        w = chip_width(name)
        if x > 0 and x + w > WIDTH:
            x, y = 0.0, y + CHIP_H + ROW_GAP
        g, w = chip(x, y, name, color, delay0 + i * 0.05)
        parts.append(g)
        x += w + GAP
        i += 1
    return "".join(parts), y + CHIP_H


def label(text, y, delay):
    return (f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" '
            f'begin="{delay:.2f}s" dur="0.4s" fill="freeze"/>'
            f'<text x="0" y="{y}" font-size="{LABEL_FS}" class="dim" '
            f'letter-spacing="1.3">{text.upper()}</text></g>')


def build():
    body, y = [], 0
    y += LABEL_FS
    body.append(label("languages", y, 0.05))
    y += 10
    g, y = flow(LANGUAGES, y, 0.12)
    body.append(g)
    y += 22 + LABEL_FS
    body.append(label("tools", y, 0.30))
    y += 10
    g, y = flow(TOOLS, y, 0.38)
    body.append(g)
    height = int(y + 6)

    style = (f"<style>{font_face()}"
             f".dim{{fill:{DIM_LIGHT}}}.pe{{stroke:rgba(0,0,0,.16)}}"
             f"@media(prefers-color-scheme:dark){{.dim{{fill:{DIM_DARK}}}"
             f".pe{{stroke:rgba(255,255,255,.18)}}}}</style>")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" '
            f'height="{height}" viewBox="0 0 {WIDTH} {height}" '
            f'font-family="{MONO}">{style}{"".join(body)}</svg>')


def main():
    out = os.path.join(os.path.dirname(HERE), "stack.svg")
    with open(out, "w", encoding="utf-8") as f:
        f.write(build())
    print(f"wrote {out}")


if __name__ == "__main__":
    main()

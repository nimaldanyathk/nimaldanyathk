
import html

def generate_svg(is_dark):
    bg_color = '#0d1117' if is_dark else '#f6f8fa'
    fg_color = '#c9d1d9' if is_dark else '#24292f'
    accent_color = '#58a6ff' if is_dark else '#0969da'
    secondary_accent = '#bc8cff' if is_dark else '#8250df'
    red_color = '#ff7b72' if is_dark else '#cf222e'
    faint_color = '#8b949e' if is_dark else '#6e7781'
    stroke_color = '#30363d' if is_dark else '#d0d7de'

    ascii_art = r"""
      ___           ___           ___
     /\__\         /\  \         /\__\
    /::|  |       /::\  \       /:/  /
   /:|:|  |      /:/\:\  \     /:/__/
  /:/|:|  |__   /:/  \:\__\   /::\__\____
 /:/ |:| /\__\ /:/__/ \:|__| /:/\:::::\__\
 \/__|:|/:/  / \:\  \ /:/  / \/_|:|~~|~
     |:/:/  /   \:\  /:/  /     |:|  |
     |::/  /     \:\/:/  /      |:|  |
     /:/  /       \::/__/       |:|  |
     \/__/         ~~           \ |__|
"""

   details = [
    {'label': 'Education', 'value': 'B.Tech CSE @ Amrita Vishwa Vidyapeetham'},
    {'label': '', 'value': ''},

    {'label': 'Languages', 'value': 'Python, Java, C++, C, JavaScript'},
    {'label': 'Frontend', 'value': 'React, Next.js, HTML, CSS'},
    {'label': 'Backend', 'value': 'Spring Boot, REST APIs, PostgreSQL'},
    {'label': 'AI/ML', 'value': 'TensorFlow, YOLO, Edge Impulse'},
    {'label': 'Embedded', 'value': 'ESP32, Arduino'},
    {'label': '', 'value': ''},

    {'label': 'Research', 'value': 'Healthcare AI & Planetary Robotics'},
    {'label': 'Website', 'value': 'nimaldanyathk.dev'},
]
    contact=[
("GitHub","github.com/nimaldanyathk"),
("LinkedIn","linkedin.com/in/nimaldanyathk"),
("Email","nimaldanyath.k@gmail.com")
]
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="410" viewBox="0 0 900 410"><rect width="900" height="410" rx="15" fill="{bg_color}" stroke="{stroke_color}" stroke-width="1.5"/><circle cx="20" cy="20" r="6" fill="#ff5f56"/><circle cx="40" cy="20" r="6" fill="#ffbd2e"/><circle cx="60" cy="20" r="6" fill="#27c93f"/><g font-family="Menlo, Monaco, Consolas, monospace" font-size="13">'
    y=70
    for line in ascii_art.splitlines():
        if line.strip():
            svg+=f'<text x="30" y="{y}" fill="{secondary_accent}" xml:space="preserve">{html.escape(line).replace(" ","&#160;")}</text>'
            y+=17
    rx,ry=400,70
    svg+=f'<text x="{rx}" y="{ry}" font-weight="bold" fill="{fg_color}">~/profile <tspan fill="{faint_color}">------------------------------------</tspan></text>'
    ry+=24
    for l,v in details:
        if not l:
            ry+=10
            continue
        dots="."*max(2,18-len(l))
        svg+=f'<text x="{rx}" y="{ry}"><tspan fill="{red_color}">- </tspan><tspan fill="{accent_color}">{l}:</tspan><tspan fill="{faint_color}"> {dots} </tspan><tspan fill="{fg_color}">{v}</tspan></text>'
        ry+=18
    ry+=12
    svg+=f'<text x="{rx}" y="{ry}" font-weight="bold" fill="{fg_color}">Contact <tspan fill="{faint_color}">-------------------------------------</tspan></text>'
    ry+=22
    for l,v in contact:
        dots="."*max(2,18-len(l))
        svg+=f'<text x="{rx}" y="{ry}"><tspan fill="{red_color}">- </tspan><tspan fill="{accent_color}">{l}:</tspan><tspan fill="{faint_color}"> {dots} </tspan><tspan fill="{fg_color}">{v}</tspan></text>'
        ry+=18
    svg+="</g></svg>"
    return svg

open("dark_mode.svg","w").write(generate_svg(True))
open("light_mode.svg","w").write(generate_svg(False))
print("Done")

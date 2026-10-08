"""The Builder's Atlas: original, self-contained SVG editorial artwork.

No fonts, images, scripts or services are fetched by these assets. Decorative
SMIL motion has complete static fallbacks and respects reduced motion.
"""
from collections import Counter
from html import escape
import math

THEMES = {
    "dark": dict(bg="#152925", panel="#1c342e", fg="#eee9d9", muted="#b1baaa", line="#40574b", accent="#ff865e", soft="#a9c2a4"),
    "light": dict(bg="#f1efdf", panel="#e7e8d5", fg="#203c32", muted="#52675a", line="#bdc7af", accent="#b94327", soft="#657f5b"),
}
LANG_COLORS = {"Python":"#dc7750", "Jupyter Notebook":"#89a98a", "TypeScript":"#e1b568", "JavaScript":"#d4ca9e", "Go":"#8fbfc1", "Swift":"#bf806e", "Rust":"#a79a83", "C++":"#ba99a7", "HTML":"#bd8e66", "CSS":"#9fa5bb", "C":"#95a09c", "Shell":"#97ab75"}


def text(x, y, value, size=14, color="fg", weight=400, extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{{{color}}}" font-weight="{weight}" {extra}>{escape(str(value))}</text>'


def line(x1, y1, x2, y2, color="line", extra=""):
    return f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{{{color}}}" {extra}/>'


def svg(content, height, theme, title, description):
    colors = THEMES[theme]
    for key, value in colors.items():
        content = content.replace("{" + key + "}", value)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="860" height="{height}" viewBox="0 0 860 {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>
<style>text {{ font-family: 'Segoe UI', Arial, sans-serif; }} .mono {{ font-family: Consolas, 'Liberation Mono', monospace; }} .serif {{ font-family: Georgia, 'Times New Roman', serif; }} @media (prefers-reduced-motion: reduce) {{ .motion {{ display: none; }} }}</style>
<defs><pattern id="paper" width="6" height="6" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".45" fill="{colors['fg']}" opacity=".08"/></pattern><clipPath id="canvas"><rect width="860" height="{height}"/></clipPath></defs>
<g clip-path="url(#canvas)"><rect width="860" height="{height}" fill="{colors['bg']}"/><rect width="860" height="{height}" fill="url(#paper)"/>{content}</g></svg>\n'''


def marker(x, y, size=10):
    return f'<path d="M{x-size} {y} H{x+size} M{x} {y-size} V{y+size}" stroke="{{accent}}" stroke-width="1.4"/>'


def slab(x, y, w, d, h, top="#e9e6cd", left="#657f69", right="#334f43"):
    # Hand-built axonometric objects; the geometry is intentionally schematic.
    return f'<path d="M{x} {y} l{w} {-w*.48} l{d} {d*.48} l{-w} {w*.48} Z" fill="{top}" stroke="#213e32" stroke-width="1.2"/><path d="M{x} {y} l{d} {d*.48} v{h} l{-d} {-d*.48} Z" fill="{left}" stroke="#213e32" stroke-width="1.2"/><path d="M{x+d} {y+d*.48} l{w} {-w*.48} v{h} l{-w} {w*.48} Z" fill="{right}" stroke="#213e32" stroke-width="1.2"/>'


def hero(theme):
    body = text(32, 37, "JC", 19, weight=800, extra='letter-spacing="-1"')
    body += line(70, 18, 70, 44)
    body += text(86, 35, "JULIAN COOPER", 13, weight=700, extra='letter-spacing="2"')
    body += text(828, 35, "LEDGENDARYANIMAL / FIELD NOTES", 11, "muted", extra='class="mono" text-anchor="end"')
    body += line(32, 57, 828, 57)
    body += text(31, 125, "Useful ideas.", 67, weight=700, extra='letter-spacing="-3"')
    body += text(31, 190, "Made real.", 70, "accent", extra='class="serif" font-style="italic" letter-spacing="-2.5"')
    body += text(568, 101, "THE BUILDER’S ATLAS", 11, "accent", 600, 'class="mono" letter-spacing="1.3"')
    body += text(568, 127, "AI agents. Desktop tools.", 16)
    body += text(568, 150, "Software for everyday work.", 16)
    body += text(568, 185, "EXPLORE THE WORK ↓", 11, "muted", 500, 'class="mono" letter-spacing="1"')
    # Contour field: a continuous landscape behind three connected workbenches.
    body += '<path d="M0 230 H860 V468 H0 Z" fill="{panel}"/>'
    for i in range(20):
        yy=239+i*13
        body += f'<path d="M-70 {yy} C100 {yy-96} 184 {yy+76} 350 {yy-9} S575 {yy-100} 925 {yy+58}" fill="none" stroke="{{soft}}" stroke-opacity=".18" stroke-width=".8"/>'
    for x in range(32,850,80):
        body += line(x,230,x-95,468,extra='stroke-opacity=".15"')
    body += '<path d="M77 383 L257 298 L427 380 L628 283 L775 354" fill="none" stroke="{accent}" stroke-width="2" stroke-dasharray="5 6"/>'
    body += '<path class="motion" d="M77 383 L257 298 L427 380 L628 283 L775 354" fill="none" stroke="{accent}" stroke-width="3" stroke-dasharray="3 500"><animate attributeName="stroke-dashoffset" from="0" to="-1006" dur="16s" repeatCount="indefinite"/></path>'
    # Left station: stacked agent architecture.
    body += slab(122,335,115,88,34)
    body += slab(139,305,80,66,25,top="#afc3a4")
    body += slab(156,274,46,43,23,top="#ec926b",left="#b65538",right="#7e3d29")
    body += '<path d="M169 272 l32 -15 l17 8 l-32 15 Z" fill="none" stroke="#823e2a" stroke-width="1.2"/><path d="M175 272 l24 -11 M183 276 l24 -12" stroke="#823e2a"/>'
    body += '<path d="M130 354 l67 32 M130 360 l67 32 M130 366 l67 32" stroke="#c2cdae" opacity=".32"/>'
    for i in range(5):
        body += line(225+i*9,330-i*4.3,225+i*9,347-i*4.3,"soft",'stroke-width="2"')
    # Center station: an exploded desktop plane.
    body += slab(340,386,131,92,16)
    body += slab(358,355,97,70,11,top="#b9c9aa")
    body += '<path d="M360 381 l53 25 M360 386 l53 25" stroke="#e9e6cd" opacity=".45"/><path d="M464 380 l30 -15 m-21 20 l29 -14" stroke="#8ca785" stroke-width="2"/>'
    body += '<path d="M396 332 L453 305 L492 324 L435 351 Z" fill="#263e32" stroke="#e8e6cf"/>'
    for i in range(4):
        body += f'<path d="M{405+i*9} {328+i*4.3} l39 -19" stroke="#ec926b" stroke-width="2"/>'
    body += '<path d="M370 344 V316 M467 299 V274 M522 347 V319" stroke="{soft}" stroke-dasharray="3 4"/>'
    # Right station: library/data volumes, deliberately different silhouettes.
    body += slab(576,324,129,98,24)
    for i in range(4):
        body += slab(596+i*19,306-i*9.1,14,53,41,top="#ead5a2" if i==2 else "#bccbaa",left="#9bb08d",right="#526e55")
        body += f'<path d="M{602+i*19} {322-i*9.1} l33 16 m-33 -10 l33 16" stroke="#e9e6cd" stroke-opacity=".4"/>'
    body += slab(601,257,85,26,10,top="#f09c73",left="#b96344",right="#85442e")
    body += marker(80,277,8)+marker(784,410,8)
    body += text(62, 448, "01 / INTELLIGENCE", 10,"muted",600,'class="mono" letter-spacing="1"')
    body += text(346, 448, "02 / INTERACTION", 10,"muted",600,'class="mono" letter-spacing="1"')
    body += text(626, 448, "03 / DELIVERY", 10,"muted",600,'class="mono" letter-spacing="1"')
    body += line(32,484,828,484)
    body += text(32,508,"FROM THE FIRST PROTOTYPE TO THE DAILY WORKFLOW",11,"muted",500,'class="mono" letter-spacing=".8"')
    body += text(828,508,"DESIGN / BUILD / SHIP",11,"accent",600,'class="mono" text-anchor="end"')
    return svg(body,530,theme,"Julian Cooper — The Builder’s Atlas","Original architectural atlas illustration. Useful ideas. Made real. AI agents, desktop tools, and software for everyday work.")


def project(theme, kind):
    info={"inktyper":("01", "InkTyper", "THOUGHT → VOICE → TEXT", ["Voice input that stays close to your workflow.","Optional AI editing, shortcuts, and tray controls."], "VOICE / DESKTOP"),
          "touchpad":("02", "Mac-like Touchpad", "A SMALL GESTURE. A BETTER FLOW.", ["Continuous three-finger dragging on Ubuntu.","Four-finger workspaces. Reversible Windows setup."], "INPUT / INTERACTION"),
          "academy":("03", "Ledgendaryanimal", "ACADEMY / RESEARCH IN CONTEXT", ["Video research, notes, subtitles, and timelines.","Brought back to the original viewing page."], "KNOWLEDGE / WEB")}
    num,title,kicker,copy,tag=info[kind]
    body=text(28,34,f"SELECTED WORK / {num}",11,"accent",600,'class="mono" letter-spacing="1.3"')
    body+=text(28,82,title,33 if kind=="academy" else 35,weight=650,extra='letter-spacing="-1.2"')
    body+=text(29,111,kicker,11,"muted",600,'class="mono" letter-spacing=".8"')
    for i,t in enumerate(copy):body+=text(29,153+23*i,t,14)
    body+=line(29,205,460,205)+text(29,226,tag,10,"muted",extra='class="mono" letter-spacing="1"')
    body+=text(462,226,"EXPLORE ↗",10,"accent",600,'class="mono" text-anchor="end"')
    body+='<path d="M497 0 H860 V250 H497 Z" fill="{panel}"/>'
    for y in range(15,250,20):body+=line(505,y,860,y,"soft",'stroke-opacity=".12"')
    if kind=="inktyper":
        # An acoustic field passing through an editorial text plane.
        for i in range(30):
            x=516+i*10; h=12+58*abs(math.sin(i*.43))*math.sin((i+1)/32*math.pi)
            body+=f'<path d="M{x} {129-h:.1f} V{129+h:.1f}" stroke="{{accent}}" stroke-width="3" opacity="{.25+.65*i/30:.2f}"/>'
        body+='<path d="M651 45 L810 63 V201 L651 183 Z" fill="{bg}" stroke="{soft}" stroke-width="1.5"/>'
        body+=text(670,91,"Aa",35,extra='class="serif" font-style="italic"')
        for i,w in enumerate([106,87,102,63]):body+=line(670,111+i*16,670+w,123+i*16,"soft",'stroke-width="3"')
        body+='<path class="motion" d="M528 89 V169" stroke="{accent}" stroke-width="2"><animate attributeName="opacity" values=".1;.8;.1" dur="3s" repeatCount="indefinite"/></path>'
        body+=text(525,229,"SIGNAL → LANGUAGE",10,"muted",extra='class="mono" letter-spacing="1"')
    elif kind=="touchpad":
        body+=slab(546,133,153,95,12,top="#c4cfb0",left="#6c876d",right="#375842")
        body+='<path d="M574 132 l117 -56 l54 26 l-117 56 Z" fill="none" stroke="#6c8264"/>'
        for i in range(3):
            body+=f'<path d="M{604+i*19} {122+i*9} q-33 -30 4 -60" fill="none" stroke="{{accent}}" stroke-width="3" stroke-linecap="round"/>'
            body+=f'<circle cx="{608+i*19}" cy="{62+i*9}" r="4" fill="{{accent}}"/>'
        body+='<path d="M715 62 l42 20 m-8 -17 l8 17 l-22 1" fill="none" stroke="{soft}" stroke-width="2"/>'
        body+=text(525,229,"LESS FRICTION. MORE FLOW.",10,"muted",extra='class="mono" letter-spacing="1"')
    else:
        for i in range(3):
            x=548+i*28; y=46+i*21
            body+=f'<path d="M{x} {y} l154 18 v111 l-154 -18 Z" fill="{{bg}}" stroke="{{soft}}" stroke-width="1.2"/>'
        body+='<path d="M623 113 l29 20 l-29 13 Z" fill="{accent}"/>'
        for i,w in enumerate([67,54,64]):body+=line(670,126+i*13,670+w,134+i*13,"soft",'stroke-width="2"')
        body+='<path d="M620 185 l126 15" stroke="{accent}" stroke-width="2"/>'
        for i in range(5):body+=f'<circle cx="{625+i*27}" cy="{186+i*3.2}" r="3" fill="{{accent}}"/>'
        body+=text(525,229,"WATCH → CONNECT → RETURN",10,"muted",extra='class="mono" letter-spacing="1"')
    return svg(body,250,theme,title," ".join(copy))


def stack(theme):
    body=text(30,34,"02 / THE WORKBENCH",11,"accent",600,'class="mono" letter-spacing="1.5"')
    body+=text(30,77,"Different tools. One connected workflow.",29,weight=600,extra='letter-spacing="-.8"')
    rows=[("01", "LANGUAGES", "Python  /  TypeScript  /  Go  /  Swift"),
          ("02", "SERVICES", "FastAPI  /  Node.js  /  PostgreSQL"),
          ("03", "INTELLIGENCE", "PyTorch  /  LLM integrations  /  Agent workflows"),
          ("04", "DELIVERY", "Docker  /  Cloudflare  /  VS Code")]
    for i,(num,label,tools) in enumerate(rows):
        y=122+i*43
        body+=line(30,y-22,830,y-22)
        body+=text(30,y,num,11,"accent",extra='class="mono"')+text(71,y,label,11,"muted",600,'class="mono" letter-spacing="1.2"')+text(253,y,tools,16)
        body+=text(824,y,"+",15,"soft",extra='class="mono" text-anchor="end"')
    return svg(body,278,theme,"The workbench — languages, services, intelligence, delivery","Python, TypeScript, Go, Swift, FastAPI, Node.js, PostgreSQL, PyTorch, LLM integrations, agent workflows, Docker, Cloudflare, VS Code.")


def activity(data, theme):
    body=text(30,34,"03 / PUBLIC OBSERVATORY",11,"accent",600,'class="mono" letter-spacing="1.5"')
    body+=text(830,34,data["updated"],10,"muted",extra='class="mono" text-anchor="end"')
    for i,(label,key) in enumerate([("Original public repos","repositories"),("Stars on original repos","stars"),("Followers","followers")]):
        x=30+i*275
        if i:body+=line(x-20,64,x-20,143)
        body+=text(x,111,f'{data[key]:,}',52,weight=600,extra='class="serif"')+text(x,137,label,13,"muted")
    body+=line(30,162,830,162)
    body+=text(30,190,"LANGUAGES / PUBLIC CODE VOLUME",11,"accent",600,'class="mono" letter-spacing="1"')
    languages=Counter(data["languages"]); total=sum(languages.values()); top=languages.most_common(5)
    remaining=total-sum(v for _,v in top)
    if remaining:top.append(("Other",remaining))
    x=30.0
    if not total:body+=text(30,229,"No public language data yet.",14,"muted")
    for name,amount in top:
        width=800*amount/total
        body+=f'<rect x="{x:.2f}" y="209" width="{width:.2f}" height="19" fill="{LANG_COLORS.get(name,"#919e91")}"/>'
        x+=width
    for i,(name,amount) in enumerate(top):
        x,y=30+(i%3)*276,260+(i//3)*29
        body+=f'<rect x="{x}" y="{y-9}" width="8" height="8" fill="{LANG_COLORS.get(name,"#919e91")}"/>'
        body+=text(x+17,y,f"{name} · {100*amount/total:.1f}%",13)
    body+=text(30,324,"PUBLIC DATA ONLY",10,"muted",extra='class="mono" letter-spacing="1"')
    body+=text(830,324,"DAILY REFRESH / GITHUB ACTIONS",10,"muted",extra='class="mono" text-anchor="end"')
    return svg(body,346,theme,"Public GitHub observatory","Public non-fork repositories, their stars, followers, and language share by code bytes. Updated "+data["updated"])


def footer(theme):
    body=text(30,34,"NEXT CHAPTER / LET’S BUILD",11,"accent",600,'class="mono" letter-spacing="1.4"')
    body+=text(28,88,"Have something useful in mind?",38,weight=400,extra='class="serif" letter-spacing="-.8"')
    body+=text(30,124,"AI applications, desktop tools, and full-stack product engineering.",15,"muted")
    body+=line(30,147,830,147)+text(30,171,"JULIAN COOPER / LEDGENDARYANIMAL",10,"muted",extra='class="mono" letter-spacing="1"')
    body+=text(830,171,"KEEP EXPLORING ↗",10,"accent",600,'class="mono" text-anchor="end"')
    return svg(body,192,theme,"Let’s build something useful","Open to freelance and product engineering work involving AI applications, desktop tools, and full-stack delivery.")


def static_art():
    renderers={"hero":hero,"stack":stack,"footer":footer}
    for kind in ("inktyper","touchpad","academy"):
        renderers[kind]=lambda theme, kind=kind:project(theme,kind)
    return {f"{name}-{theme}.svg":render(theme) for name,render in renderers.items() for theme in THEMES}

"""Neon profile artwork. All SVGs are self-contained and script-free."""
from collections import Counter
from html import escape

THEMES = {
    "dark": dict(bg="#090d18", panel="#111a2d", fg="#eff6ff", muted="#a0b4d1", line="#273659", gold="#45e8ff", violet="#ad82ff"),
    "light": dict(bg="#f0f4ff", panel="#e4ebfc", fg="#152643", muted="#4a6082", line="#b9c9e8", gold="#007c98", violet="#7040c7"),
}
LANG_COLORS = {"Python": "#25bedb", "Jupyter Notebook": "#ad82ff", "TypeScript": "#588bff", "JavaScript": "#d9b93b", "Go": "#00c6a8", "Swift": "#ef7b70", "Rust": "#ddab7a", "C++": "#dc70bc", "HTML": "#e26c5b", "CSS": "#9d78dd", "C": "#798b9b", "Shell": "#79be89"}


def text(x, y, value, size=14, color="fg", weight=400, extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{{{color}}}" font-weight="{weight}" {extra}>{escape(str(value))}</text>'


def svg(content, height, theme, title, description):
    colors = THEMES[theme]
    for key, value in colors.items():
        content = content.replace("{" + key + "}", value)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="860" height="{height}" viewBox="0 0 860 {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>
<style>text {{ font-family: 'Segoe UI', Arial, sans-serif; }} .mono {{ font-family: Consolas, 'Liberation Mono', monospace; }} .display {{ font-family: 'Arial Black', 'Segoe UI', Arial, sans-serif; }} @media (prefers-reduced-motion: reduce) {{ .typed {{ clip-path: none; }} .motion,.cursor {{ display: none; }} }}</style>
<rect x="0.5" y="0.5" width="859" height="{height-1}" rx="10" fill="{colors['bg']}" stroke="{colors['line']}"/>
{content}</svg>
'''


def hero(theme):
    # Keep the hero dark in both site themes to preserve the neon contrast.
    # A complete static illustration remains when animation is unavailable.
    body = '''<defs>
<radialGradient id="aura"><stop stop-color="#5b34bd" stop-opacity="0.42"/><stop offset="1" stop-color="#090d18" stop-opacity="0"/></radialGradient>
<linearGradient id="name" x2="1" y2="0"><stop stop-color="#ffffff"/><stop offset="0.7" stop-color="#c6faff"/><stop offset="1" stop-color="#45e8ff"/></linearGradient>
<linearGradient id="beam"><stop stop-color="#45e8ff" stop-opacity="0"/><stop offset="0.5" stop-color="#45e8ff" stop-opacity="0.3"/><stop offset="1" stop-color="#ad82ff" stop-opacity="0"/></linearGradient>
<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0 H0 V32" fill="none" stroke="#93b9ff" stroke-opacity="0.08"/></pattern>
<clipPath id="frame"><rect width="860" height="346" rx="10"/></clipPath>
<clipPath id="typing"><rect x="60" y="235" width="390" height="26"><animate attributeName="width" values="0;390;390" keyTimes="0;0.38;1" dur="8s" repeatCount="indefinite"/></rect></clipPath>
</defs>
<g clip-path="url(#frame)">
<rect width="860" height="346" fill="url(#grid)"/>
<ellipse cx="682" cy="154" rx="285" ry="242" fill="url(#aura)"/>
<path d="M0 314 L238 314 L270 346 M530 346 L570 306 L860 306" stroke="#273659" fill="none"/>
<path d="M1 63 V15 Q1 1 15 1 H186 M674 345 H845 Q859 345 859 331 V276" fill="none" stroke="#45e8ff" stroke-opacity="0.65"/>
<path d="M18 322 H118 M24 328 H77" stroke="#ad82ff" stroke-opacity="0.5"/>
<g transform="translate(686 153)">
<circle r="100" fill="#0c1223" fill-opacity="0.7" stroke="#334d76"/>
<circle r="77" fill="none" stroke="#45e8ff" stroke-opacity="0.4"/>
<ellipse rx="77" ry="25" fill="none" stroke="#45e8ff" stroke-opacity="0.5" transform="rotate(35)"/>
<ellipse rx="77" ry="25" fill="none" stroke="#ad82ff" stroke-opacity="0.5" transform="rotate(-35)"/>
<path d="M-55 -55 L55 55 M-55 55 L55 -55" stroke="#334d76"/>
<g class="motion"><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="22s" repeatCount="indefinite"/>
<circle r="112" fill="none" stroke="#45e8ff" stroke-width="2" stroke-dasharray="92 37 15 84"/><circle cx="112" r="4" fill="#45e8ff"/>
</g>
<g class="motion"><animateTransform attributeName="transform" type="rotate" from="360" to="0" dur="30s" repeatCount="indefinite"/>
<circle r="122" fill="none" stroke="#ad82ff" stroke-opacity="0.65" stroke-dasharray="35 26 70 80"/>
</g>
<path d="M-25 -12 L-40 0 L-25 12 M25 -12 L40 0 L25 12 M9 -25 L-9 25" fill="none" stroke="#45e8ff" stroke-width="3" stroke-linecap="round"/>
</g>
<path d="M566 35 V269 M576 280 H808" fill="none" stroke="#45e8ff" stroke-opacity="0.18"/>
<rect class="motion" y="30" width="860" height="2" fill="url(#beam)"><animateTransform attributeName="transform" type="translate" values="0 0;0 275;0 0" dur="14s" repeatCount="indefinite"/></rect>
</g>'''
    body += text(34, 43, "// LEDGENDARYANIMAL", 12, "gold", 600, 'class="mono" letter-spacing="2.1"')
    body += text(30, 117, "JULIAN", 66, weight=900, extra='class="display" letter-spacing="2"')
    body += '<text x="30" y="184" font-size="66" font-weight="900" class="display" letter-spacing="2" fill="url(#name)">COOPER.</text>'
    body += '<rect x="34" y="218" width="493" height="63" rx="5" fill="#0c1527" stroke="#273f60"/>'
    body += text(47, 256, ">", 17, "gold", 600, 'class="mono"')
    body += '<g class="typed" clip-path="url(#typing)">' + text(66, 256, "From prototype to shipped product.", 15, "fg", 400, 'class="mono"') + '</g>'
    body += '<rect class="cursor" x="374" y="243" width="8" height="17" fill="#45e8ff"><animate attributeName="opacity" values="1;0;1" dur="1.4s" repeatCount="indefinite"/></rect>'
    body += text(36, 309, "AI AGENTS   /   DESKTOP TOOLS   /   FULL STACK", 12, "muted", 500, 'class="mono" letter-spacing="0.4"')
    body += text(687, 302, "BUILD. SHIP. ITERATE.", 11, "violet", 600, 'class="mono" text-anchor="middle" letter-spacing="1.5"')
    return svg(body, 346, "dark", "Julian Cooper / Ledgendaryanimal", "Julian Cooper. AI agents, desktop tools, and full-stack software. From prototype to shipped product. Animated neon wireframe artwork.")


def stack(theme):
    rows = [["Python", "TypeScript", "Go", "Swift", "FastAPI", "Node.js"],
            ["PostgreSQL", "Docker", "PyTorch", "Cloudflare", "VS Code", "LLMs"]]
    symbols = ["PY", "TS", "GO", "SW", "FA", "JS", "DB", "DK", "PT", "CF", "VS", "AI"]
    body = text(24, 28, "03 / TOOLKIT", 11, "gold", 600, 'class="mono" letter-spacing="1.6"')
    body += '<path d="M180 23 H834" stroke="{line}"/>'
    for row_index, row in enumerate(rows):
        y = 45 + row_index * 46
        for column, label in enumerate(row):
            x = 24 + column * 138
            accent = "gold" if column % 2 == 0 else "violet"
            body += f'<rect x="{x}" y="{y}" width="126" height="35" rx="4" fill="{{panel}}" stroke="{{line}}"/>'
            body += f'<path d="M{x} {y+7} V{y+28}" stroke="{{{accent}}}" stroke-width="2"/>'
            body += text(x+10, y+22, symbols[row_index*6+column], 10, accent, 700, 'class="mono"')
            body += text(x+36, y+22, label, 12)
    return svg(body, 144, theme, "Tools I work with", ", ".join(sum(rows, [])))


def activity(data, theme):
    body = text(26, 34, "04 / PUBLIC SIGNAL", 11, "gold", 600, 'class="mono" letter-spacing="1.5"')
    body += text(832, 34, "Updated " + data["updated"], 11, "muted", extra='class="mono" text-anchor="end"')
    for x, label, key in [(26, "Original public repos", "repositories"), (301, "Stars on original repos", "stars"), (577, "Followers", "followers")]:
        body += f'<rect x="{x}" y="49" width="257" height="81" rx="4" fill="{{panel}}"/>'
        body += f'<path d="M{x} 64 V115" stroke="{{gold}}" stroke-opacity="0.6" stroke-width="2"/>'
        body += text(x+16, 93, f'{data[key]:,}', 39, weight=700, extra='class="mono"') + text(x+17, 115, label, 12, "muted")
    body += '<path d="M26 138 H834" stroke="{line}"/>'
    body += text(26, 163, "LANGUAGE DISTRIBUTION", 11, "violet", 600, 'class="mono" letter-spacing="1.5"')
    languages = Counter(data["languages"])
    total = sum(languages.values())
    top = languages.most_common(5)
    remaining = total - sum(amount for _, amount in top)
    if remaining:
        top.append(("Other", remaining))
    x = 26.0
    if not total:
        body += text(26, 200, "No public language data yet.", 14, "muted")
    for name, amount in top:
        width = 808 * amount / total
        color = LANG_COLORS.get(name, "#88919b")
        body += f'<rect x="{x:.2f}" y="179" width="{width:.2f}" height="12" fill="{color}"/>'
        x += width
    for i, (name, amount) in enumerate(top):
        x, y = 26 + (i % 3) * 277, 217 + (i // 3) * 27
        color = LANG_COLORS.get(name, "#88919b")
        body += f'<circle cx="{x+4}" cy="{y-4}" r="4" fill="{color}"/>'
        body += text(x+16, y, f"{name}  {100*amount/total:.1f}%", 13)
    return svg(body, 269, theme, "Public GitHub activity", "Public non-fork repositories, their stars, followers, and language share by code bytes. Updated " + data["updated"])

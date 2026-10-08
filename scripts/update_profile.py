"""Generate first-party profile artwork and public-only GitHub cards (stdlib only)."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html import escape
import json
import os
from pathlib import Path
import subprocess
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
OWNER = "Cooperiano"
THEMES = {
    "dark": dict(bg="#11161d", panel="#191f28", fg="#f2eee5", muted="#aab4c2", line="#303945", gold="#edbd63"),
    "light": dict(bg="#faf8f3", panel="#f1ede4", fg="#252b33", muted="#586371", line="#ded8cb", gold="#92641b"),
}
LANG_COLORS = {"Python": "#4585b8", "TypeScript": "#3178c6", "JavaScript": "#b79c27", "Go": "#008da8", "Swift": "#df6437", "Rust": "#bc714e", "C++": "#a96396", "HTML": "#d86649", "CSS": "#7961b3", "C": "#798b9b", "Shell": "#759341"}


def api(path, cli=False):
    if cli:
        return json.loads(subprocess.check_output(["gh", "api", path], text=True, encoding="utf-8"))
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "Cooperiano-profile", "X-GitHub-Api-Version": "2022-11-28"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = "Bearer " + token
    for attempt in range(3):
        try:
            with urlopen(Request("https://api.github.com/" + path, headers=headers), timeout=30) as response:
                return json.load(response)
        except (HTTPError, URLError, TimeoutError) as error:
            if attempt == 2 or isinstance(error, HTTPError) and error.code not in (429, 500, 502, 503, 504):
                raise
            time.sleep(2 ** attempt)


def collect(cli=False):
    user = api(f"users/{OWNER}", cli)
    repos, page = [], 1
    while True:
        batch = api(f"users/{OWNER}/repos?type=owner&per_page=100&page={page}", cli)
        repos.extend(repo for repo in batch if not repo["private"] and repo["owner"]["login"].lower() == OWNER.lower())
        if len(batch) < 100:
            break
        page += 1
    originals = [repo for repo in repos if not repo["fork"]]
    languages = Counter()
    with ThreadPoolExecutor(max_workers=4) as pool:
        for result in pool.map(lambda repo: api(f"repos/{OWNER}/{repo['name']}/languages", cli), originals):
            languages.update(result)
    return {"owner": OWNER, "updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
            "repositories": len(originals), "stars": sum(repo["stargazers_count"] for repo in originals),
            "followers": user["followers"], "languages": dict(languages.most_common())}


def text(x, y, value, size=14, color="fg", weight=400, extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{{{color}}}" font-weight="{weight}" {extra}>{escape(str(value))}</text>'


def svg(content, height, theme, title, description):
    colors = THEMES[theme]
    for key, value in colors.items():
        content = content.replace("{" + key + "}", value)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="860" height="{height}" viewBox="0 0 860 {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>
<style>text {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; }} @media (prefers-reduced-motion: reduce) {{ .typed {{ clip-path: none; }} .cursor {{ opacity: 0; }} }}</style>
<rect x="0.5" y="0.5" width="859" height="{height-1}" rx="16" fill="{colors['bg']}" stroke="{colors['line']}"/>
{content}</svg>\n'''


def hero(theme):
    # Keep a complete readable base image when SVG animation is unavailable.
    body = '''<defs><clipPath id="typing"><rect x="36" y="207" width="438" height="34"><animate attributeName="width" values="0;438;438" keyTimes="0;0.4;1" dur="8s" repeatCount="indefinite"/></rect></clipPath></defs>
<path d="M617 25 Q824 61 849 243 M569 31 Q777 58 838 255" fill="none" stroke="{gold}" stroke-opacity="0.14"/>
<path d="M575 80 L733 68 L795 169 L665 216 Z M733 68 L665 216 M575 80 L795 169" fill="none" stroke="{line}"/>
<circle cx="733" cy="68" r="8" fill="{gold}"/><circle cx="795" cy="169" r="5" fill="{gold}" opacity="0.6"/><circle cx="665" cy="216" r="6" fill="{gold}" opacity="0.45"/><circle cx="575" cy="80" r="4" fill="{gold}" opacity="0.4"/>
<rect x="36" y="34" width="28" height="3" rx="1.5" fill="{gold}"/>'''
    body += text(74, 41, "JULIAN COOPER / LEDGENDARYANIMAL", 11, "muted", 600, 'letter-spacing="1.8"')
    body += text(34, 109, "Useful ideas.", 48, weight=650)
    body += text(34, 164, "Working software.", 48, weight=650)
    body += text(36, 199, "AI applications, agents, and tools for everyday work.", 17, "muted")
    body += '<g class="typed" clip-path="url(#typing)">' + text(36, 235, "From idea to everyday use.", 20, "gold", 500) + '</g>'
    body += '<rect class="cursor" x="292" y="218" width="2" height="20" fill="{gold}"><animate attributeName="opacity" values="1;0;1" dur="1.2s" repeatCount="indefinite"/></rect>'
    return svg(body, 274, theme, "Julian Cooper", "Useful ideas. Working software. AI applications, agents, and tools for everyday work. From idea to everyday use.")


def stack(theme):
    rows = [["Python", "TypeScript", "Go", "Swift", "FastAPI", "Node.js"],
            ["PostgreSQL", "Docker", "PyTorch", "Cloudflare", "VS Code", "LLM integrations"]]
    body = ""
    for row_index, row in enumerate(rows):
        x, y = 20, 18 + row_index * 43
        for label in row:
            width = len(label) * 7.1 + 34
            body += f'<rect x="{x}" y="{y}" width="{width}" height="31" rx="7" fill="{{panel}}" stroke="{{line}}"/>'
            body += f'<circle cx="{x+12}" cy="{y+15.5}" r="2.5" fill="{{gold}}"/>'
            body += text(x+22, y+20, label, 12)
            x += width + 9
    return svg(body, 111, theme, "Tools I work with", ", ".join(sum(rows, [])))


def activity(data, theme):
    body = text(26, 34, "PUBLIC WORK", 11, "gold", 600, 'letter-spacing="1.5"')
    body += text(832, 34, "Updated " + data["updated"], 11, "muted", extra='text-anchor="end"')
    for x, label, key in [(26, "Original public repos", "repositories"), (301, "Stars on original repos", "stars"), (577, "Followers", "followers")]:
        body += text(x, 89, f'{data[key]:,}', 39, weight=600) + text(x, 114, label, 13, "muted")
    body += '<path d="M26 138 H834" stroke="{line}"/>'
    body += text(26, 163, "LANGUAGE SHARE", 11, "gold", 600, 'letter-spacing="1.5"')
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gh-cli", action="store_true", help="Use the existing gh login for local generation")
    parser.add_argument("--snapshot", type=Path, help="Render a previously collected aggregate snapshot offline")
    args = parser.parse_args()
    data = json.loads(args.snapshot.read_text(encoding="utf-8")) if args.snapshot else collect(args.gh_cli)
    if data["owner"] != OWNER or any(data[k] < 0 for k in ("repositories", "stars", "followers")):
        raise ValueError("Invalid profile snapshot")
    if any(value < 0 for value in data["languages"].values()):
        raise ValueError("Invalid language totals")
    # Fetch everything before replacing existing cards; failed fetches preserve the last good set.
    files = {f"{name}-{theme}.svg": render(theme) for name, render in [("hero", hero), ("stack", stack)] for theme in THEMES}
    files.update({f"activity-{theme}.svg": activity(data, theme) for theme in THEMES})
    ASSETS.mkdir(exist_ok=True)
    for name, value in files.items():
        (ASSETS / name).write_text(value, encoding="utf-8")
    (ASSETS / "public-stats.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"Generated {len(files)} SVGs from public data ({data['updated']}).")


if __name__ == "__main__":
    main()

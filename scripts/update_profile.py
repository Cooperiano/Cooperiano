"""Generate first-party profile artwork and public-only GitHub cards (stdlib only)."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
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
from profile_art import THEMES, static_art, activity


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
    files = static_art()
    files.update({f"activity-{theme}.svg": activity(data, theme) for theme in THEMES})
    ASSETS.mkdir(exist_ok=True)
    for name, value in files.items():
        (ASSETS / name).write_text(value, encoding="utf-8")
    (ASSETS / "public-stats.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"Generated {len(files)} SVGs from public data ({data['updated']}).")


if __name__ == "__main__":
    main()

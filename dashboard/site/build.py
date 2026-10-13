"""Build the GitHub Pages version of the maintainer dashboard.

Wraps dashboard/index.html (the same page the Claude dashboard shows) in a
standalone HTML document with a stand-in for the dashboard runtime, and copies
the data file next to it.

Usage:
    python dashboard/site/build.py <output-dir>
"""
import shutil
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
dashboard = here.parent
out = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
out.mkdir(parents=True, exist_ok=True)

template = (here / "template.html").read_text(encoding="utf-8")
page = (dashboard / "index.html").read_text(encoding="utf-8")
if "<!-- PAGE -->" not in template:
    raise SystemExit("template.html has no <!-- PAGE --> marker")
(out / "index.html").write_text(template.replace("<!-- PAGE -->", page), encoding="utf-8")
shutil.copy(here / "dash-shim.js", out / "dash-shim.js")
shutil.copy(dashboard / "maintainer-activity.json", out / "maintainer-activity.json")
(out / ".nojekyll").write_text("", encoding="utf-8")
print(f"Built {out / 'index.html'}")

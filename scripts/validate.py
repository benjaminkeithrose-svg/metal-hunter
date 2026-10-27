"""Check data/events.json and data/bands.json before a data refresh is pushed.
Usage: python3 scripts/validate.py   (exit code 0 = OK)"""
import json, re, sys, subprocess

errs = []
e = json.load(open("data/events.json"))
b = json.load(open("data/bands.json"))
BUCKETS = {k for k, _ in b.get("buckets", [])}
AGES = {"18+", "16+", "All ages", "All ages (licensed)", "18+ floor, all-ages mezzanine"}

if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", e.get("refreshed", "")):
    errs.append("events.json: 'refreshed' must be YYYY-MM-DD")
ids = set()
for t in e["tours"]:
    for k in ("id", "artist", "tag", "status"):
        if not t.get(k):
            errs.append(f"tour {t.get('id')}: missing {k}")
    if t.get("id") in ids:
        errs.append(f"duplicate tour id {t['id']}")
    ids.add(t.get("id"))
    if t.get("tag") not in ("core", "adjacent", "folk", "punk", "aus"):
        errs.append(f"tour {t.get('id')}: bad tag {t.get('tag')}")
    if not t.get("gb") or any(g not in BUCKETS for g in t["gb"]):
        errs.append(f"tour {t.get('id')}: 'gb' must list genre groups from bands.json buckets")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", t.get("added", "")):
        errs.append(f"tour {t.get('id')}: 'added' must be the YYYY-MM-DD date it was added")
    if not re.fullmatch(r"[a-z0-9-]+", t.get("id", "")):
        errs.append(f"tour {t.get('id')}: id must be lowercase letters, digits and hyphens (it becomes a page name)")
    if t.get("tier") not in ("major", "scene"):
        errs.append(f"tour {t.get('id')}: 'tier' must be major or scene")
    if t.get("status") not in ("on-sale", "upcoming", "sold-out"):
        errs.append(f"tour {t.get('id')}: bad status {t.get('status')}")
    # A tour may have no shows yet (announced, dates TBA).
    for s in t.get("shows", []):
        if "age" in s and s["age"] not in AGES:
            errs.append(f"tour {t.get('id')}: show {s.get('d')} has unknown age '{s['age']}' (use one of {sorted(AGES)})")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", s.get("d", "")) or not all(s.get(k) for k in ("city", "st", "venue")):
            errs.append(f"tour {t.get('id')}: bad show {s}")
for s in e.get("sales", []):
    if s.get("tour") and s["tour"] not in ids:
        errs.append(f"sale points at unknown tour {s['tour']}")

groups = {g[0] for g in b["groups"]}
for g in b["groups"]:
    if len(g) < 3 or g[2] not in BUCKETS:
        errs.append(f"group {g[0]}: third item must be a genre group from buckets")
names = set()
for x in b["bands"]:
    if x["g"] not in groups:
        errs.append(f"band {x['n']}: unknown group {x['g']}")
    if x["st"] not in ("elsewhere", "none", "au", "signal", "unchecked"):
        errs.append(f"band {x['n']}: bad status {x['st']}")
    if x["n"].lower() in names:
        errs.append(f"duplicate band {x['n']}")
    names.add(x["n"].lower())

# A band that was checked on main must not slip back to unchecked.
try:
    old = json.loads(subprocess.run(["git", "show", "origin/main:data/bands.json"], capture_output=True, text=True, check=True).stdout)
    was = {x["n"] for x in old["bands"] if x["st"] != "unchecked"}
    errs += [f"band {x['n']}: was checked, now unchecked" for x in b["bands"] if x["st"] == "unchecked" and x["n"] in was]
except Exception:
    pass

# Every app release: APP_VERSION in index.html, the top entry of CHANGELOG.md and help.html must agree.
try:
    app = re.search(r'APP_VERSION="([0-9.]+)"', open("index.html", encoding="utf-8").read()).group(1)
    log = re.search(r"^## v([0-9.]+) ", open("CHANGELOG.md", encoding="utf-8").read(), re.M).group(1)
    helptext = open("help.html", encoding="utf-8").read()
    hv = re.search(r'<meta name="mh-version" content="([0-9.]+)">', helptext).group(1)
    if not (app == log == hv):
        errs.append(f"version mismatch: index.html {app}, CHANGELOG.md {log}, help.html {hv}")
    if f"What's new in v{app}" not in helptext:
        errs.append(f"help.html has no \"What's new in v{app}\" section")
except (AttributeError, OSError) as ex:
    errs.append(f"version check failed: {ex}")

# The share pages in t/ must match the data.
chk = subprocess.run([sys.executable, "scripts/build_pages.py", "--check"], capture_output=True, text=True)
if chk.returncode:
    errs.append("share pages out of date: run python3 scripts/build_pages.py (" + chk.stdout.strip() + ")")

print("\n".join(errs) or f"OK: {len(e['tours'])} tours, {len(b['bands'])} bands")
sys.exit(1 if errs else 0)

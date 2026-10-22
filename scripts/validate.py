"""Check data/events.json and data/bands.json before a data refresh is pushed.
Usage: python3 scripts/validate.py   (exit code 0 = OK)"""
import json, re, sys, subprocess

errs = []
e = json.load(open("data/events.json"))
b = json.load(open("data/bands.json"))
BUCKETS = {k for k, _ in b.get("buckets", [])}

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
    if t.get("status") not in ("on-sale", "upcoming", "sold-out"):
        errs.append(f"tour {t.get('id')}: bad status {t.get('status')}")
    # A tour may have no shows yet (announced, dates TBA).
    for s in t.get("shows", []):
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

print("\n".join(errs) or f"OK: {len(e['tours'])} tours, {len(b['bands'])} bands")
sys.exit(1 if errs else 0)

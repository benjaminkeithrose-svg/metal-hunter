"""Build one small share page per tour in t/<id>.html.

When a tour link is pasted into Facebook, Messenger, Reddit and the like, they read these pages'
preview tags (band, dates, cities). A person opening the link is sent straight on to the tour in the app.

Usage:
  python3 scripts/build_pages.py          write or update the pages
  python3 scripts/build_pages.py --check  exit 1 if any page is missing or out of date
Pages for tours that have finished are kept, so old shared links still open the app.
"""
import html, json, os, sys
from datetime import date

SITE = "https://benjaminkeithrose-svg.github.io/metal-hunter/"
IMAGE = SITE + "icons/og.png"
MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
STATUS = {"on-sale": "Tickets on sale", "upcoming": "Tickets soon", "sold-out": "Sold out"}


def nice(d):
    y, m, dd = map(int, d.split("-"))
    return date(y, m, dd), f"{dd} {MON[m - 1]} {y}"


def describe(t):
    shows = sorted(t["shows"], key=lambda s: s["d"])
    if not shows:
        return "Australian dates to be announced."
    (d1, first), (d2, last) = nice(shows[0]["d"]), nice(shows[-1]["d"])
    when = first if d1 == d2 else (f"{first.rsplit(' ', 1)[0]} – {last}" if d1.year == d2.year else f"{first} – {last}")
    cities = []
    for s in shows:
        if s["city"] not in cities:
            cities.append(s["city"])
    where = ", ".join(cities[:6]) + (" and more" if len(cities) > 6 else "")
    return f"{when} · {where}. {STATUS.get(t.get('status'), '')}.".replace(" .", ".")


def page(t):
    e = lambda s: html.escape(s, quote=True)
    cities = {s["city"] for s in t["shows"]}
    title = t["artist"] + (" · Australian tour" if len(cities) != 1 else " · " + next(iter(cities)))
    desc = describe(t)
    if t.get("support"):
        fest = any(w in (t["genre"] + " " + t["artist"]).lower() for w in ("festival", "fest", "cruise"))
        desc += (" Line-up: " if fest else " With ") + t["support"] + "."
    if len(desc) > 200:
        desc = desc[:197].rsplit(" ", 1)[0].rstrip(",") + "…"
    target = f"../?tour={t['id']}"
    url = f"{SITE}t/{t['id']}.html"
    return f"""<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} | Metal Hunter</title>
<meta name="description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Metal Hunter">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{e(url)}">
<meta property="og:image" content="{IMAGE}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0a0e0c">
<link rel="canonical" href="{e(url)}">
<meta http-equiv="refresh" content="0; url={e(target)}">
<script>location.replace({json.dumps(target)})</script>
<style>body{{background:#0a0e0c;color:#d9e1dd;font:16px/1.5 system-ui,sans-serif;padding:24px}}a{{color:#e0782f}}</style>
<p><a href="{e(target)}">Open {e(t['artist'])} on Metal Hunter</a></p>
</html>
"""


def main():
    root = os.path.join(os.path.dirname(__file__), "..")
    tours = json.load(open(os.path.join(root, "data", "events.json")))["tours"]
    out = os.path.join(root, "t")
    os.makedirs(out, exist_ok=True)
    check = "--check" in sys.argv
    stale = []
    for t in tours:
        path = os.path.join(out, t["id"] + ".html")
        body = page(t)
        have = open(path, encoding="utf-8").read() if os.path.exists(path) else None
        if have != body:
            stale.append(t["id"])
            if not check:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(body)
    if check:
        print("Out of date: " + ", ".join(stale) if stale else f"OK: {len(tours)} tour pages up to date")
        sys.exit(1 if stale else 0)
    print(f"Updated {len(stale)} of {len(tours)} tour pages")


if __name__ == "__main__":
    main()

# Metal Hunter

A free calendar of every metal, hardcore and punk tour coming to Australia: dates, venues, official ticket links and when presales open. Fans pick genres, states and bands to follow, and it installs as a phone app.

Live: https://benjaminkeithrose-svg.github.io/metal-hunter/ · Current version: v1.0 (see `CHANGELOG.md`)

## Where things are
- `docs/DOCUMENTATION.md`: full documentation (screens, files, data model, storage, sharing, automation, releasing).
- `help.html`: help for fans (More → Help in the app).
- `CHANGELOG.md`: version history.
- `docs/INSTRUCTIONS.md`: scope, sources, data rules and the refresh procedure.
- `CLAUDE.md`: how changes are proposed, approved and merged.

## Run locally

    python3 -m http.server 8000

Then visit http://localhost:8000. Before pushing, run `python3 scripts/build_pages.py` and `python3 scripts/validate.py`.

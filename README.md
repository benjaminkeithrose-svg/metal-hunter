# Metal Hunter

A calendar of upcoming heavy metal concerts in Australia: dates, venues, where to buy tickets, and when presales and general sales open. It also tracks bands that have not announced Australian dates yet.

## Layout
- `index.html`: the whole site. It loads the two data files below.
- `data/events.json`: tours and shows, ticket sale moments, and the watchlist. Edit this to add or change a show.
- `data/bands.json`: tracked bands by genre, each with a status (`elsewhere`, `none`, `au`, `signal`, `unchecked`). `confirmed: true` means Ben has approved the band for polling.
- `docs/INSTRUCTIONS.md`: scope, sources, data rules and the refresh procedure.
- `scripts/`: reserved for the refresh script (Ticketmaster Discovery API plus promoter pages).

## Run locally
The page loads JSON, so open it through a web server, not by double-clicking:

    python3 -m http.server 8000

Then visit http://localhost:8000.

## Publish
GitHub Pages: push to GitHub, then Settings, Pages, deploy from the `main` branch root. The site is public once published.

## App (PWA)
`manifest.webmanifest`, `sw.js` and `icons/` make the site installable (Add to Home Screen on iPhone, Install app on Android). The service worker loads the site and data network-first, so merges to `main` reach installed apps on next open, and keeps a copy for offline use. The ⟳ button compares the live site and data with the shown copy and reloads if anything changed. Regenerate the PNG icons from `icons/icon.svg` if the logo changes.

## Refresh
Follow the procedure in `docs/INSTRUCTIONS.md`, bump `refreshed` in `data/events.json`, and commit.

## Next steps
1. Ben confirms the band list.
2. Event-page ticket links in place of home-page links.
3. Ticketmaster Discovery API sweep (needs a free API key).
4. .ics export and a presale email digest.
5. Scheduled refresh.

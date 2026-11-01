# Metal Hunter documentation

Version 1.1 · 27 October 2026. Update this file whenever the app, data model, scripts or automation change (see "Releasing a new version").

- Live site: https://benjaminkeithrose-svg.github.io/metal-hunter/
- Repository: https://github.com/benjaminkeithrose-svg/metal-hunter
- Fan help: `help.html` (More → Help in the app)
- Version history: `CHANGELOG.md`
- Research and data rules: `docs/INSTRUCTIONS.md`
- How changes get approved: `CLAUDE.md`

## 1. What it is

Metal Hunter is a free calendar of heavy music touring Australia: international metal, hardcore and punk acts at any venue size, Australian bands' national tours and festivals, and (optionally) underground and up-and-coming Australian bands. Each show has the official ticket link and when tickets go on sale. Fans pick genres, states and bands to follow ("My Metal").

It is a static website on GitHub Pages that installs as a phone app (a PWA). There is no server of its own: the tour data lives in two JSON files in the repository, refreshed by scheduled Claude sessions. The only online service is a Supabase table for Pro launch sign-ups.

Planned next: an Android app built with Capacitor, then iPhone, with a paid "Metal Hunter Pro" tier ($2.99 a month or $19.99 a year) for genre alerts and presale reminders. See the roadmap in `docs/INSTRUCTIONS.md` and the proposal at https://claude.ai/artifact/NFGe1hSRnE8q5K8jsZfK3v.

## 2. Screens and features

| Screen | What it does |
|---|---|
| Welcome (first open) | Pick genres, states and bands to follow, or skip to see everything. Skipped when someone arrives from a shared link. |
| Shows | Upcoming tours, one card per tour (next date in the person's states, others under "+ N more dates"). Top to bottom: "What's new" note (once per version), My Metal / All shows switch, Edit, summary, search, "Shared with you", "Just added", month headings, the Pro sign-up card. |
| Calendar | Month grid with dots per day; tap a day for its shows. Follows the My Metal switch. |
| Presales | Upcoming presales and general sales grouped by tour, times in Sydney time; sales opened in the last two weeks. |
| Bands | Every tracked band grouped by genre group; search, filter (Following, On the calendar, Rumoured, Touring overseas, Aussie, Rising Aussie bands), ☆ to follow, tap for the band's note. |
| More | Help and What's new, Pro sign-up, My Metal summary, Rumoured tours (`watch`), Look (Runestone / Xerox Grind), About, data date, Check for updates, version line. |
| My Metal sheet | Genres (9 groups), states (all 8), followed bands, options: Aussie bands' tours, underground (off by default), all-ages shows only (off by default; applies in both modes), hide sold out, every date separately. |
| help.html | Fan help for every screen and label, FAQ, and "What's new" for the current version. |
| privacy.html | What the Pro sign-up keeps and how to unsubscribe or delete. |
| t/<id>.html | Share page per tour (see section 6). |

Show card parts: date block; artist (★ if a followed band is on the bill); support acts; venue and city; sale text; tags (age rule, genre group or "Festival", "Aussie", "Underground", "Unconfirmed"); ⓘ (note, genre, source link); "+ N more dates"; status badge (On sale / Tickets soon / Sold out); Tickets button (seller name underneath); Share; Add to calendar (saves an .ics file).

## 3. Files

| Path | Purpose |
|---|---|
| `index.html` | The whole app: styles for both looks, the update checker, and the app script (state, filters, views, My Metal sheet, sharing, Pro sign-up). Settings near the top of the script: `APP_VERSION`, `APP_DATE`, `SHOW_SCENE`, `SB_URL`/`SB_KEY`, `GOATCOUNTER`, `FIRST_LOAD`. |
| `help.html` | Fan help page. Carries `<meta name="mh-version">` and a "What's new in vX" section. |
| `privacy.html` | Privacy page for the Pro sign-up. |
| `data/events.json` | `refreshed` date, `tours`, `sales`, `watch`. |
| `data/bands.json` | `buckets` (9 genre groups), `groups` (`[key, label, bucket]`), `bands`. |
| `t/*.html` | Generated share pages, one per tour. Never edit by hand. |
| `scripts/validate.py` | Checks data, versions and share pages. Must pass before any push to `main`. |
| `scripts/build_pages.py` | Builds `t/*.html` from `data/events.json`. |
| `.github/workflows/keep-supabase-awake.yml` | Pings Supabase every 3 days so the free project isn't paused (section 7). |
| `sw.js` | Service worker: network first for site and data, cached copy for offline. Bump `CACHE` when the list of cached files changes. |
| `manifest.webmanifest`, `icons/` | App install details and icons. `icons/og.png` is the 1200×630 link-preview image. |
| `CHANGELOG.md` | Version history. |
| `CLAUDE.md` | Ben's approval workflow and the data-refresh exception. |
| `docs/INSTRUCTIONS.md` | Scope, sources, data rules, refresh procedure, roadmap, research notes. |
| `docs/launch-pitch.md` | The post for fan groups. |
| `*.png` at the root | Old screenshots from the first version; not used by the site. |

## 4. Data model

Full field rules are in `docs/INSTRUCTIONS.md` ("Data record" and "Rules"). In short:

**Tour** (`data/events.json` → `tours`): `id` (lowercase, digits, hyphens; becomes the share page name), `artist`, `support`, `genre` (free text), `gb` (genre groups), `aus` (Australian act), `tier` (`major` or `scene`), `tag` (legacy category), `status` (`on-sale`, `upcoming`, `sold-out`), `conf` (`verify` = Unconfirmed), `sale`, `ticketUrl`, `ticketLabel`, `src`, `note`, `added` (date first added; drives "Just added"), `shows`.

**Show**: `d` (YYYY-MM-DD), `city`, `st`, `venue`, optional `status`, `url`, `label`, `age` (one of `18+`, `16+`, `All ages`, `All ages (licensed)`, `18+ floor, all-ages mezzanine`; a tour-level `age` applies to every show without its own). Leave `age` out when no source states it.

**Sale** (`sales`): `at` (ISO time with offset), `tour` (tour id), `kind`, `text`.

**Watch item** (`watch`): `title`, `text`, `url`, `label`. Shown as Rumoured under More.

**Band** (`data/bands.json` → `bands`): `n`, `g` (group key), `st` (`elsewhere`, `none`, `signal`, `unchecked`, legacy `au`), `note`, `src`, `aus`, `scene` (rising Australian band), `named`, `confirmed`.

How the app reads it:
- A band shows "On calendar" when its exact name appears in a tour's artist or support, split on `, + / ; and ( )`.
- Genre groups come from `gb` for tours and from the group's bucket for bands.
- Scene tours (`tier: scene`) show only when the person switches on underground, or follows a band on the bill. `SHOW_SCENE = false` hides them for everyone.
- "Just added" lists tours with `added` in the last 7 days and after `FIRST_LOAD` (the initial data load), filtered by My Metal.
- Shows dated before today are hidden automatically.
- The age tag uses the show's `age`, else the tour's. "All-ages shows only" keeps only shows whose age contains "all ages".

## 5. What is stored where

| Data | Where | Key |
|---|---|---|
| My Metal (mode, genres, states, follows, options) | The person's browser (`localStorage`) | `mh-me` |
| Chosen look | Browser | `mh-look` |
| Last version seen ("What's new") | Browser | `mh-version` |
| Signed up for Pro (hide the form) | Browser | `mh-pro` |
| Pro sign-ups (email, genres, states, source screen, date) | Supabase project `metal-hunter` (org Wildfire084, Sydney), table `public.pro_waitlist` | Insert-only from the site; read in the Supabase dashboard → Table Editor |

The site's Supabase key is a publishable key: it can add sign-ups but cannot read them (row-level security and column grants). It can also call `ping()`, which returns the time and is used only to keep the project awake. Rows with `source = 'test'` are tests.

## 6. Sharing and link previews

- Share on a card uses the phone's share sheet, or copies the link on a computer.
- The link is `t/<id>.html`. That page has preview tags (title, description with dates and cities, `icons/og.png`) so Facebook, Messenger, Reddit and others show the tour, and forwards to `?tour=<id>`.
- `?tour=<id>` opens Shows with the tour pinned under "Shared with you" and skips the welcome screen. Close removes it.
- `index.html` has site-wide preview tags. Facebook caches previews: use the Sharing Debugger (developers.facebook.com/tools/debug) → Scrape Again after changing them.
- Run `python3 scripts/build_pages.py` after any change to tours. Share pages for finished tours are kept so old links still work.

## 7. Automation

Two scheduled tasks start a fresh Claude session and push data-only changes straight to `main` (allowed by the exception in `CLAUDE.md`):

| Task | When (Sydney time) | What |
|---|---|---|
| Metal Hunter news check | Mon and Thu, 6:35am | New tours, line-ups, presales and changes since the last refresh. |
| Metal Hunter monthly band sweep | 1st of the month, 6:17am | The news check plus a re-check of every tracked band; removes finished tours. |

Each run: update the data, give new tours `added`, run `scripts/build_pages.py`, run `scripts/validate.py`, and push only if it passes and only data, `docs/INSTRUCTIONS.md` and `t/` changed. Otherwise it opens a pull request. Ben gets a phone push when a run finishes with changes. The tasks are managed from claude.ai (scheduled tasks); they have no connectors, so a run that needs a pull request may not be able to open one and will say so in its summary.

**Keeping the sign-up database awake.** Supabase pauses free projects after 7 days without traffic, and while paused Pro sign-ups fail. `.github/workflows/keep-supabase-awake.yml` (GitHub Actions) calls the database's `ping()` function every 3 days with the site's publishable key. `ping()` only returns the time; it reads and changes nothing. A failed run emails the repository owner; run it by hand from the repository's Actions tab → Keep Supabase awake → Run workflow. If the project does get paused, restore it in the Supabase dashboard. GitHub stops scheduled jobs after 60 days without repository activity, which the twice-weekly data refreshes prevent.

The ⟳ button and reopening the app after 30 minutes compare the live site and data with the cached copy and reload if anything changed.

## 8. Run it locally

    cd metal-hunter
    python3 -m http.server 8000

Then open http://localhost:8000 (the app loads JSON, so it needs a web server). Before pushing anything:

    python3 scripts/build_pages.py
    python3 scripts/validate.py

## 9. Releasing a new version

Any change to the app (look, features, wording, rules) is a new version. Tour and band data refreshes are not.

1. Follow `CLAUDE.md`: propose, get Ben's yes, build on a branch.
2. Pick the number: small fixes 1.0 → 1.0.1; new features 1.0 → 1.1; the store app 2.0.
3. Update `APP_VERSION` and `APP_DATE` in `index.html`.
4. Add the entry at the top of `CHANGELOG.md` (`## vX · date`).
5. In `help.html`: update `<meta name="mh-version">`, the version line, the footer, "What's new in vX" (plain fan language), and any help topic the change affects.
6. Update this file wherever the change affects screens, files, data, storage or automation.
7. If cached files changed, bump `CACHE` in `sw.js`.
8. Run `scripts/build_pages.py` and `scripts/validate.py` (it fails if the three version numbers differ), test in a phone-sized browser, open the pull request and ask Ben whether to merge.

After merging, returning users see the "What's new" note once.

## 10. Publishing

GitHub Pages serves the `main` branch root. A merge to `main` is live within a few minutes; installed apps pick it up on the next open or ⟳.

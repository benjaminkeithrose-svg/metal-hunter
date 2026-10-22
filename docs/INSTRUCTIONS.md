# Project Instructions: Metal Hunter (Australian heavy metal concert calendar)

## Purpose
Maintain a calendar of upcoming heavy metal concerts in Australia so Ben never misses a show or a ticket release. Every entry answers four questions: who, when and where, where to buy, and when tickets go on sale. The calendar is also a tracker of bands that have not yet announced Australian dates.

## Scope
**Include**
- International acts touring Australia, at any venue size (stadium to small club). A small-club date by an overseas band (e.g. an Interferum-style underground tour) is in scope.
- Major festivals and sideshows with international heavy acts.
- Nearly all metal genres: heavy, thrash, death, melodic death, black, doom, prog, power (Blind Guardian, Iced Earth style), folk, Viking and pagan, mythology-themed, metalcore, deathcore, nu-metal, industrial, symphonic and gothic.
- Related heavy styles: hardcore, post-hardcore, screamo, emo.
- **Folk crossover** acts that sit near metal (Heilung, Wardruna, Faun, Patty Gurdy and similar), tagged `folk`.
- Heavy-adjacent acts (hard rock, stoner and similar), tagged `adjacent`.

**Tags** drive the category filters on the page: `core` (metal and the genres above), `adjacent`, `folk`. Each can be switched off in the page.

**Exclude**
- Local/Australian-only pub and club gigs.
- Australian acts, unless they headline a major festival or cruise that also carries international acts (put these on the Watchlist, flagged "Aus-headlined").
- Pop-punk, pop, indie and other non-heavy acts.
- New Zealand dates (note them only if they affect an AU tour).

## Tracked bands and "likely to tour"
The Bands tab holds a list of bands Ben follows, grouped by genre (`BANDS`, with `GROUPS` for the headings). Each band has a status:
- `elsewhere`: touring other regions, no Australian dates. Say where and until when.
- `none`: searched, nothing announced.
- `au`: Australian act (tracked for festivals and cruises only).
- `signal`: a hint of an Australian date (festival confirmed, promoter teaser).
- `unchecked`: not yet searched.
A band with a show on the calendar shows as "On calendar" automatically.

Rules for this list:
- The list is confirmed by Ben (22 Oct 2026) as a starting point. Grow it over time: when a tracked band tours with another act (support slots, co-headlines, festival bills), add that act to the list in the matching genre and note where it was seen.
- Do not predict tours. Record only what a source says. A "rumour" needs a named source and is labelled as one.
- Useful signals: a world tour that skips Oceania, a recent Asia or NZ leg, an album cycle, a band's last Australian visit, a promoter teaser.
- Expanded to 286 bands in 23 groups on 22 Oct 2026 (Ben approved). The 207 new bands start as `unchecked`; check them in batches of about 40 per refresh, oldest-unchecked first, until the Ticketmaster sweep can do it automatically.
- The seed list came from Ben's genre notes and is a starting point. Assumptions: "Release the Archers" is Unleash the Archers, "Winter Sun" is Wintersun, "Foul" is Faun.

## Source priority
1. **Promoter and official ticket pages (truth for dates and sale times):** Destroy All Lines, TEG Live / TEG Dainty, Live Nation AU, Soundworks Direct, Hardline Media, Teamwork Touring, Choose Your Cruise, festival sites (Good Things, Froth & Fury).
2. **Ticketing platforms:** Ticketek, Ticketmaster AU, Oztix, Moshtix, Humanitix, Sydney Opera House.
3. **News (catches announcements early):** Heavy Magazine, Metal Obsession, Metal-Roos, Everyday Metal, Metal on Tap, Music Feeds, The AU Review, The Note, Beat, Noise11, Rolling Stone AU, Wall of Sound, Hot Metal.
4. **Aggregators (cross-check only):** Songkick, Bandsintown, Eventworld, Stereoboard, Austadiums (best for stadium presale and on-sale times).
5. **Resale (never as a ticket link):** Tixel, Viagogo, StubHub. Use them only as a demand signal.

If a Ticketmaster Discovery API key is supplied later, use it as the structured national sweep, then fill gaps from promoters. Note that search tools often return only link lists; fetching the specific promoter or news page gives usable data.

## Data record
The page keeps its data in one block at the top of its script: `TOURS` (one record per tour or festival, with a `shows` list), `SALES` (presale and on-sale moments for the radar), `WATCH` (items without dates yet), `BANDS` and `GROUPS` (tracked bands), and `REFRESHED`.

Tour fields: `id`, `artist`, `support`, `genre`, `tag` (core / adjacent / folk), `status` (on-sale / upcoming / sold-out), `conf` (set to `verify` when in doubt), `sale` (presale and on-sale text with timezone), `ticketUrl`, `ticketLabel`, `src` (source URL), `note`, `shows`.
Show fields: `d` (ISO date), `city`, `st`, `venue`, optional `status`, `url`, `label` for per-show overrides (e.g. one show sold out, or a different ticketer per city).
Band fields: `n`, `g` (group), `st` (status above), `note`, `src`.

## Rules
- **Dates and times:** store dates ISO. Quote sale times in the local time of the city they apply to, with the timezone abbreviation (AEDT, AEST, ACST, AWST). Today's date is the reference for "upcoming" and "on sale".
- **Never guess.** If a date, venue or sale time was not seen in a source, say TBC in the tour `note` and let it appear on the Watchlist. Do not infer from the artist's other tours.
- **Confidence:** mark `verify` when only one aggregator lists it, when sources conflict, or when a support act or date is in doubt. Note conflicts in `note`.
- **Ticket links:** link only to the promoter or official ticketer. If no official ticket link was seen, link to the best source article and label it "Tour details".
- **Past dates** drop off the calendar automatically; remove stale tours at each refresh.
- **Copyright:** paraphrase source articles, no quoted passages. Short factual fields (dates, venues, lineups) are fine.
- **Sold-out status:** only mark sold-out when a source says so.

## Calendar page (v2, published as an artifact)
- Single self-contained HTML page. Views: Agenda (default), Month grid, On-sale radar, Bands, Watchlist.
- Filters: state, category chips (core, adjacent, folk), hide sold out, text search. Filters are saved in the browser.
- Each show has date, city and venue, support acts, status badge, official ticket link, presale and on-sale text, an "Add to calendar" link (Google Calendar) and a source link.
- Artifacts cannot trigger file downloads, so there is no .ics export. Add one in the GitHub version.
- Keep the page text minimal. Scope notes, label meanings and sources live in the Info tab; the footer only shows "Updated <date>". Long tour notes sit behind the ⓘ toggle on each card, and band notes open when the band is tapped.

## Refresh procedure (manual for now)
1. Search each promoter site and the news sources for tours announced since the last refresh.
2. Check each existing tour for added dates, upgrades, sold-out notices and changed sale times.
3. Run a Ticketmaster/Songkick/Eventworld sweep by city to catch small-club international tours the promoters did not feature.
4. Check the tracked bands: update `st` and notes, move any with Australian dates into `TOURS`.
5. Update the data block, bump `REFRESHED`, republish the same artifact file.

## Roadmap
- **Phase 1 (done):** manually researched artifact.
- **Phase 2:** move to Claude Code and GitHub. Plan: `data/events.json` and `data/bands.json` as source of truth, a refresh script using the Ticketmaster Discovery API plus scraped promoter pages, public GitHub Pages hosting (repo name: metal-hunter) so friends can open it, a scheduled refresh, .ics export, and optional email or calendar alerts for upcoming presales.

## Known gaps (22 Oct 2026)
- No live feed; all data is from search results.
- Smaller international club tours are under-covered until a Ticketmaster/Oztix sweep is added.
- Several tours have only some dates (Periphery, Dayseeker, Story of the Year + Silverstein, Thrown's Sydney show, Heilung outside Sydney, Death Angel headline dates). They are on the Watchlist.
- Some ticket links go to the promoter's or ticketer's home page rather than the specific event page.
- Band checks on 22 Oct 2026 used news searches that mostly return link lists, so "nothing announced" means nothing found, not a confirmed absence. Only Sick of It All is unchecked.
- Killswitch Engage rests on one source. Carcass's rescheduled September 2027 dates may need new tickets; confirm with the ticketer.
- Ben may still send his own additions to the band list.
- 207 of the 286 tracked bands are still `unchecked` (added 22 Oct 2026).

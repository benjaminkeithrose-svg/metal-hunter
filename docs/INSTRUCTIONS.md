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
- **Punk**, tagged `punk`: Celtic and Irish punk, folk punk, '77 and UK punk, street punk and Oi!, modern punk and post-punk, skate and melodic punk, horror punk and psychobilly (added 22 Oct 2026, Ben approved). Australian punk acts are tagged `aus`.

- **Australian acts** in the same genres, tagged `aus`: national or multi-city tours, festival slots and cruises (added 22 Oct 2026, Ben approved).

**Tags** drive the category filters on the page: `core` (metal and the genres above), `adjacent`, `folk`, `punk`, `aus` (Australian). Each can be switched off in the page.

**Exclude**
- One-off local pub and club gigs by Australian acts (a national or multi-city tour is in scope).
- Pop-punk (Ben decided 22 Oct 2026 to keep it out), pop, indie and other non-heavy acts.
- New Zealand dates (note them only if they affect an AU tour).

## Tracked bands and "likely to tour"
The Bands tab holds a list of bands Ben follows, grouped by genre (`BANDS`, with `GROUPS` for the headings). Each band has a status:
- `elsewhere`: touring other regions, no Australian dates. Say where and until when.
- `none`: searched, nothing announced.
- `au`: legacy status, no longer used. Australian bands carry `aus: true` and use the normal statuses.
- `signal`: a hint of an Australian date (festival confirmed, promoter teaser).
- `unchecked`: not yet searched.
A band with a show on the calendar shows as "On calendar" automatically (exact match on the billed names, so the band's name must match the tour's spelling).
The Bands tab has a search box and a status filter (including Australian / International).

Rules for this list:
- The list is confirmed by Ben (22 Oct 2026) as a starting point. Grow it over time: when a tracked band tours with another act (support slots, co-headlines, festival bills), add that act to the list in the matching genre and note where it was seen.
- Do not predict tours. Record only what a source says. A "rumour" needs a named source and is labelled as one.
- Useful signals: a world tour that skips Oceania, a recent Asia or NZ leg, an album cycle, a band's last Australian visit, a promoter teaser.
- Expanded to 286 bands in 23 groups on 22 Oct 2026 (Ben approved). New additions start as `unchecked`; check them at the next refresh.
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

## Refresh procedure
Runs automatically (Ben approved 22 Oct 2026): a news check every Monday and Thursday about 6:35am Sydney time, and a full sweep of every tracked band on the 1st of each month about 6:30am. Both push data-only changes straight to `main` (see the exception in CLAUDE.md) and send Ben a phone push when something changed.
- **News check:** steps 1, 2 and 5, plus any tracked band named in new announcements. Drop shows whose date has passed only if the whole tour is over; past dates of a running tour can stay.
- **Full sweep:** all steps, checking every band in `data/bands.json` with batched searches (several band names per query).
Steps:
1. Search each promoter site and the news sources for tours announced since the last refresh.
2. Check each existing tour for added dates, upgrades, sold-out notices and changed sale times.
3. Run a Ticketmaster/Songkick/Eventworld sweep by city to catch small-club international tours the promoters did not feature.
4. Check the tracked bands: update `st` and notes, move any with Australian dates into `TOURS`.
5. Update `data/events.json` (`tours`, `sales`, `watch`) and `data/bands.json`, set `refreshed` to today's date, run `python3 scripts/validate.py`, commit as `Data refresh: <summary>` and push to `main`.

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
- Expanded to 547 bands in 30 groups (Oct 2026). All checked once; the check added The Sisters of Mercy, Citizen + Drug Church and Mono to the calendar. Follow-up leads resolved: Soen (Jan 2027) and Lucidity 2027 added; the Obituary + Wormrot lead was the 2020 tour.
- All 286 tracked bands were checked on 22 Oct 2026 (one news/aggregator search each). The check added 11 tours: La Dispute, Dance Gavin Dance, Jimmy Eat World, Queens of the Stone Age, Metal Church, Deicide, Igorrr, PRESIDENT, Drain, Melbourne Dethfest 2027 (Bloodbath) and Elder. Metal Church has no on-sale details.
- Expanded to 1055 bands (Oct 2026): 154 Australian bands in 8 groups (`aus: true`) plus about 350 more international bands. All 533 new or reset bands were checked on 22 Oct 2026. The check added 9 tours: Northlane, Windwaker, Hellbound II cruise, Heavensgate, Dream On Dreamer, Trophy Eyes, The Early November + Hellogoodbye, Uncle Acid & the Deadbeats and Sleep Theory. It also completed A Perfect Circle's dates, added Airbourne to Guns N' Roses, and added Speed, Grinspoon, Bilmuri and Voice of Baceprot to Good Things.
- Open leads from that check: King Parrot (8-show regional run late 2026, dates not found), Voyager (comeback shows, year unconfirmed), Rose Tattoo (2026 farewell, Australian dates unconfirmed), Justice for the Damned (March headline tour, year unconfirmed). Dream On Dreamer and Trophy Eyes still need venues.
- Punk added (Oct 2026): 155 bands in 8 groups (7 international, plus Australian punk), 1210 bands in total. All checked on 22 Oct 2026. The check added 9 tours: Rise Against + Dropkick Murphys, Meltdown Festival, Less Than Jake, Frenzal Rhomb, Propagandhi, Teenage Bottlerocket, The Saints, C.O.F.F.I.N, and Millencolin on Good Things. Frenzal Rhomb's Melbourne and Hobart venues still need checking.

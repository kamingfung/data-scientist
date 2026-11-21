---
name: html-data-deck
description: Build a data-driven slide deck as one self-contained HTML file. Use for a readout, results deck, workshop deck or executive summary where every number, chart and table must come from data. Covers a title-only outline first, action titles, KPI tiles, inline SVG charts, sources for every number, a template with builders, and a three-pass pre-publish review (story, numbers, design).
---

# HTML data deck

Build every deck as one self-contained HTML file of fixed 1280x720 slides. By default the slides are hand-written HTML and every number, chart and table is filled from data (hybrid build, below). `template/` holds the CSS, JS and builders. For storylining and a PowerPoint grid, see [../consulting-communication/SKILL.md](../consulting-communication/SKILL.md); for an HTML deck built from data, this skill wins on density, palette and theme.

## When to use

- Use for any deck, readout, slide set or presentation, before writing the first slide.
- Build `.html` first. Build `.pptx` or `.pdf` only when the requester asks; feed both from the same computed numbers.
- Print to PDF from the browser when a PDF is enough; the CSS already breaks one slide per page.

## Step 0: outline before slides

Render nothing until the requester approves a title-only outline.

1. Write the audience, the decision the deck supports, and the answer in one sentence.
2. Build the argument tree: answer → 2–4 supporting arguments → the evidence for each (query id, run id or file) → the action it implies.
3. Turn the tree into one line per slide: kicker, action title, visual form (table below), and "The audience should leave this page understanding that …".
4. Read the titles alone, top to bottom; they must make the argument without the bodies.
5. Show the outline and the mode (readout or workshop) to the requester; build only after they approve.

Give each slide one job. If its "leave understanding that" sentence has two unrelated clauses, split the slide. Keep that sentence as a comment in the slide's builder.

## Visual form by relationship

Pick the visual from what the information means:

| Relationship | Visual |
|---|---|
| Change over time | line chart or timeline |
| Category comparison | sorted bar chart |
| Contribution to a total | waterfall or stacked bar |
| Two-variable classification | 2×2 matrix |
| Ordered actions | process flow |
| Recurring activity | cycle |
| Causes of one problem | fishbone |
| Workstreams and dates | swim lanes or Gantt |
| Levels | hierarchy |
| Current versus future | two columns |
| Exact values matter more than shape | table |

Give every chart slide a takeaway panel, unless the chart needs the full width; then give it a one-line `.note` instead.

Geometry carries meaning: arrows mean direction, circles mean recurrence, pyramids mean levels. Never use a shape whose meaning contradicts the content.

## Two modes

Pick the mode before the first slide and say it in the generator.

- **Readout** (default): a result for decision-makers. Use the full anatomy below.
- **Workshop**: a working session to listen, brainstorm or agree a scope (planning, design review). The audience shapes the answer, so the slides open questions instead of closing them.

Both modes keep the context and style rules: kicker, action title, footer with as-of date and ticket key, terms defined at first use, numbers computed from data, house colors with a second encoding, light theme, the naming rule.

Workshop mode relaxes the rest:

- Make each slide graphic-first: one diagram fills most of the slide, with at most 3 short bullets (under 15 words each) beside or under it.
- Use at most one headline number per slide; move tables and evidence to `Backup`.
- Use plain words: no code names, no acronyms on the slide face; put the mapping in the footer.
- Skip KPI tiles and What happened / Why except on the headline slide; the headline may be a single big number and one sentence.
- Use these visual blocks (inline SVG, drawn from data or structure, not decoration):
  - **Flow**: boxes and arrows for how it works today (inputs → model → output), with the parts in question highlighted.
  - **Timeline**: one row of dated markers for what was tried, labeled with the outcome icon (✅ kept, ✖ dropped, ⏸ open), color plus shape.
  - **Option map**: a 2×2 (for example effort × control) or side-by-side cards, one per option, with its upside and its failure mode.
  - **Roadmap**: swim lanes by team across months, with gates as diamonds.
  - **Question slide**: one question as the title, 2–3 prompts, and an empty panel labeled "Notes from the room" for live capture.
- Keep the action title, but it may end in a question when the slide asks the room ("Which overrides do you make today, and why?").

## Slide anatomy

Readout mode. Each slide is `<section class="slide">` with, top to bottom:

1. **Kicker.** A numbered section label, `N · Section name` (`0 · Headline`, `5.4 · Driver A, tested`, `Backup · …`, `Appendix · …`). Sub-slides take `N.M`. Sort slides by kicker, not by build order.
2. **Action title (h1).** One sentence that states the number and its implication: "Output fell X units against the baseline; driver A explains about Y%". Never a topic label ("Production").
3. **Body.** One of the blocks below, at most two side by side (`.cols`).
4. **Note (optional).** One `.note` line: the takeaway, or the definition a chart needs ("Baseline = …").
5. **Assumptions and limitations (optional).** One `.assume` box, filled from a dict keyed by kicker; its numbers come from placeholders, never typed.
6. **Footer.** `topic · as of YYYY-MM-DD · baseline definition · glossary mapping if any · ticket key(s)`; deck.js appends `n / N`.

Body blocks:

- **KPI tiles** (`.tiles`, 2–5 tiles): label, value with unit, and a sub line with the range or share ("five fits +A to +B", "C% of the loss (slide 5.7)"). A loss value takes class `neg`.
- **Definition strip** under the tiles (`<p class="small">`): bold what the estimate is, then define every term the tiles use.
- **What happened / Why** (`.cols.compact`, `two_cols()`): two filled rounded cards side by side, the panel color for What happened and the light tint for Why, equal height, filling the body; 3–4 bullets each in large type; every bullet carries its number and ends with the slide it is proven on ("(slide&nbsp;5.5)", a non-breaking space keeps it on one line).
- **Executive summary** (`.exec`, `exec_summary()`): one lead sentence, then 3–4 numbered sections; each has a bold heading that carries the message alone and 1–2 bullets of a bold run-in label plus one short sentence. About 60–90 words, large type for the back of the room.
- **Key takeaways panel** (`.with-take`, `takeaways()`): the chart keeps the left 3/4; a panel on the right holds 2–3 points, each a bold run-in label plus one sentence ("**Winning weeks:** 15 of 23 peak weeks within 10%", numbers as placeholders), and ends in an ink "Next: …" arrow tag that leads into the next slide.
- Charts fill their slot: full body, or the left 3/4 next to takeaways; never a fixed-size chart with empty space below. Pass `box=deck.SLOTS["full" | "take" | "half"]` to every `charts.py` builder and wrap the chart in `<div class="fill">`; the builder lays out axes, nice ticks and labels for that box at normal text size.
- Fill the slot, not the slide: keep a clear margin of at least 16px between the chart and every neighbor (title block, takeaways panel, side text, `.note`, `.assume`, footer). Shrink the slot height by the height of any `.note` or `.assume` on the same slide; the footer sits absolutely at the bottom, so the chart must end above its top rule. Keep axis labels, value labels, end labels and the legend inside the SVG `viewBox` with inner padding, so nothing bleeds past the chart's own edge into a neighbor.
- On a chart-plus-text slide (one chart with side bullets or takeaways), give the chart 2/3 to 3/4 of the width (grid about `3fr 1fr`) and set the side text at about 17px, not the 13.5px compact list.
- **Chart:** inline SVG with `viewBox` and `width="100%"`, `role="img"`, value labels on the bars, legend in its own row so labels never collide. No `<img>`, no raster, no chart library.
- **Table:** `table()` helper; numeric columns right-aligned, tabular figures; header row on the panel color.
- **The ask** (slide 1): table `Owner | Ask | Why, from this analysis | DRI | By when`; one owner, one action, one date per row; the "why" cites a number and a slide. Take owners and dates from the requester, never invent them.

Deck order that works: title, `0 · Executive summary`, `0.1 · Headline` (tiles and What happened / Why), `1 · The ask`, `1.1 · What changed since <earlier versions>` (when the deck supersedes one), the story chapters, `Backup · How we measured it`, `Appendix · Caveats and terms`.

## Content rules

- Compute every number in titles, tiles, bullets, notes and assumptions from the data tables the charts use; never type one.
- Format numbers with one helper set: `m` (1.57M / 394k / 1,234), `ms` (signed), `pct`; use the true minus `−`.
- Show a range next to every modeled estimate; say what the range is at first use.
- Name the baseline on the slide and in the footer ("own prior-period baseline, same weeks").
- Use one executive vocabulary on every slide; map code or data terms once (footer or glossary), and normalize them in the builder.
- Write American English, define every term and acronym at first use, follow a ticket key with 2–3 keywords, and use short active sentences.
- Label correlation as correlation; state what a model or test cannot show in the assumptions box.
- Mark a corrected figure with the "Corrected" panel (`.xp-btn.corr` + `.xp-panel.corr`); print shows the panel on its own page.

## Colors

Data colors come from the Okabe–Ito palette, which stays distinct for the common color-vision deficiencies. The tokens live in `template/deck.css`; swap them for your own brand only after checking the same distances.

- Tokens: ink `#1A1A1A` text, totals and series 1; blue `#0072B2` series 2, gains and the highlight; orange `#E69F00` series 3; red (vermilion) `#D55E00` losses; light `#BBBBBB` context marks, rules and baselines; gray `#9E9E9E` unexplained; accent `#0072B2` labels; panel `#F2F4F7` and tint `#E5F0F7` cards.
- Use at most 3 series colors, in the order ink, blue, orange (smallest pair CIEDE2000 22 under simulated color-vision deficiency and in grayscale, Machado 2009). Draw any further category in the light context grey, or switch to small multiples.
- Highlight one mark per chart. When every other mark is light grey, the highlight is blue (CIEDE2000 26 from the grey). When the chart already has series colors, mark the singled-out series with a bold label and a thicker line instead of a new color: no Okabe–Ito color stays above ΔE 13 from both blue and orange. The title says whether the highlight is good or bad news.
- Draw context marks (other bars and lines, stems, bands) in light grey.
- Gains and losses use blue and vermilion. They are only ΔE 8 apart for some readers, so a signed label (+24, −7) and the side of zero always carry the sign too. A gain/loss chart has no other highlight.
- Give each line one second encoding: markers on a solid line, or a dash pattern with no markers, never both.
- Draw no gridlines, except on a multi-series line chart read off its y-axis: light horizontal gridlines and a vertical legend in line-end order. Never on scatter plots.
- Label values directly; write negative numbers with the true minus (−); never rotate tick labels (thin them instead).
- State units on every chart. Give masses in kg (or thousands or millions of kg), not tons: a metric ton and a US ton differ.
- Color by meaning first: when a color has a fixed meaning in your domain, keep it on every slide.
- Keep text contrast at least 4.5:1, or 3:1 for large text. Orange (2.3:1) and vermilion (3.9:1) are fill colors; label them in ink.

## Sources

- Give every number on a slide a source: query id, run id or file, with the pull date, in the footer or a small source line.
- When a deck has more than a few sources, add a `Backup · Sources` slide: slide, claim, source.
- Keep the slide light (white on the dark `#2b2b2b` surround); no dark theme.

## Build: hybrid (default)

Write the slides by hand for full layout freedom; take every number, chart and table from data. `_demo()` in `template/deck.py` is a minimal worked example.

1. Copy `template/` (`deck.py`, `charts.py`, `deck.css`, `deck.js`, `interact.js`) next to the generator, or import it by path.
2. Write the slides as `<section class="slide">` blocks in a `.html.tmpl` file: kicker, action title, body, footer (see the slide anatomy above).
3. Put a placeholder wherever data goes:
   - `{{num:key}}`: a number; `nums[key] = (text, source)`, text formatted through `Fig` (`F.m`, `F.ms`, `F.pct`, `F.of`, `F.rng`), source = query id, run id or file plus pull date. It renders as `<span class="n" data-src="source">`; hover shows the source.
   - `{{chart:key}}`: an SVG from `charts.py`, built with `box=SLOTS[...]` for its slot.
   - `{{table:key}}`: HTML from `table()`.
4. Load the data and compute `nums`, `charts` and `tables` in one place.
5. Call `build(title, template, F, nums, charts, tables, sources_footer=..., allowed=(...))`. It appends `Backup · Sources` slides (slide, key, value, source for every number) and raises on:
   - any digit in hand-written text outside a placeholder; allowed: ISO dates and months, years and seasons (2024/25), ticket keys, `slide N.M` references, the number that opens a kicker, and the literal tokens in `allowed`;
   - an unknown key or a malformed `{{…}}`;
   - a figure in the output that did not pass through `Fig` (`check()`).
6. Write the file and a `build.sh` that reruns the generator from raw inputs (paths, run ids, `--as-of`).
7. When a companion report quotes the same numbers, cross-check them against the deck's rendered text.

Generator path (option for large data-driven readouts with many similar slides): build every slide in Python with `slide(kicker, title, body, footer, note=, assume=)`, `tiles()`, `two_cols()`, `table()`, `cover()`, `big_number()`, `cards()`, `notes_panel()`, `detail()`, `tabs()` and `charts.py`; assemble with `page(title, slides)`; call `check(F, html)`; extend `UNIT_WORDS` for your units. `python3 template/deck.py <tmp>.html` renders a skeleton.

## Slide types

Each slide type has a builder or a CSS block.

| Type | Builder or block |
|---|---|
| Title, section divider | `.cover` (`cover()`) |
| Executive summary | `.exec` (`exec_summary()`) |
| Headline: KPI tiles, What happened / Why | `.tiles` + `.cols.compact` (`tiles()`, `two_cols()`) |
| What happened / Why cards | `.cols.compact` (`two_cols()`) |
| Headline, one big number | `.big` (`big_number()`) |
| The ask; exact-value table | `table()` |
| Line, sorted bar, waterfall, stacked bar (2 to 2.3 with a `takeaways()` panel), 2×2, process flow, cycle, fishbone, swim lanes, hierarchy | `charts.py`: `line_chart`, `sorted_bars`, `waterfall`, `stacked_bar`, `matrix_2x2`, `flow`, `cycle`, `fishbone`, `gantt`, `hierarchy` |
| Current versus future | `.cols` with `.card` |
| Timeline with ✅ ✖ ⏸ | `timeline()` |
| Option cards | `.cards` (`cards()`) |
| Question slide, "Notes from the room" | `.q` + `.notes` (`notes_panel()`) |
| Scenario toggle with takeaways | `.tabs` (`tabs()`), `takeaways()` |
| Tooltip chart with a detail panel | `line_chart()`, `.xp-btn` (`detail()`) |
| Sources | auto-built by `build()` |

## Type

`deck.css` uses three system font stacks: display face for titles and big numbers (Avenir Next, then Helvetica Neue), serif text face for prose (Charter, then Iowan Old Style, Georgia), mono for kickers, labels, table headers and footers (SF Mono, then Menlo, Consolas). All are system stacks: the file renders offline and carries no font payload. Never link Google Fonts or another font host.

## Interactivity

Optional per deck, inline, no libraries; `page()` inlines `interact.js` only when a slide uses it.

- Keyboard and scroll navigation, `n / N` in every footer, `#n` opens slide n, F or P for presentation mode (`deck.js`).
- Hover tooltips with exact values on chart marks (`data-tip`, set by `charts.py`) and the source of every `{{num:…}}`.
- Click-to-expand detail panels (`.xp-btn` + `.xp-panel`; `.corr` for "Corrected").
- Scenario toggles on one slide (`.tabs`), for example path 1 / path 2.

Print rule: print to PDF gives one slide per page at 1280x720; each detail panel prints on its own page after its slide; every scenario pane prints side by side; tooltips do not print, so draw every value the argument needs as a label.

## Naming and filing

- Name the file `YYYY-MM-DD [TICKET-KEY ]Title in sentence case[, as of YYYY-MM-DD].html`: the prefix date is the meeting or request date; add the as-of part only when the data date differs.
- Never use `v2`, `final` or `copy`; stamp a shared version with its share date and time, and move the older version unchanged to an archive folder next to the deck.
- Write dates as `YYYY-MM-DD`.
- Keep the generator in a code repository, not in a document share.

## Pre-publish review: three passes

Run the passes separately; do not mix story, numbers and pixels in one read.

Pass 1, story (titles only):

- [ ] The requester approved the title-only outline and the mode before rendering (Step 0).
- [ ] Read only the titles: they make the argument and end in a clear recommendation or ask.
- [ ] Every slide has a numbered kicker and one job; the visual matches the relationship table.
- [ ] The executive summary follows the title; its headings alone tell the story; about 60–90 words.
- [ ] Every chart slide has a takeaway panel of at most 3 points (or a one-line note when the chart needs full width); its last point is the "Next:" tag that leads into the next slide.
- [ ] Readout: every action title states a number and an implication; the headline has tiles, a definition strip, and What happened / Why with slide references.
- [ ] Workshop: one diagram per slide, at most 3 bullets of under 15 words, at most one headline number, no code names or acronyms on the face, a "Notes from the room" panel on every question slide.
- [ ] Cold read: a subagent that did not build the deck reads each slide and states its conclusion in one line; every mismatch with the intended sentence is fixed.

Pass 2, numbers:

- [ ] `build()` (or `check()`) passes: no digit typed outside a placeholder, no unresolved placeholder, no figure outside `Fig`; the report cross-check passes when there is a report.
- [ ] Every `{{num:…}}` source names a query id, run id or file and the pull date; the `Backup · Sources` slides render.
- [ ] Every number has a source; every modeled number shows its range; every chart and table states its unit.
- [ ] Every slide reference points to the slide that proves it (open it and check).
- [ ] Assumptions and limitations box on every slide that rests on a model or a choice of baseline.
- [ ] Terms and acronyms are defined at first use; one name per concept; American English.

Pass 3, design and filing:

- [ ] Nothing overflows: render with headless Chrome and look at every slide.
- [ ] Every chart fills its slot (full body, or the left 3/4 next to takeaways); no fixed-size chart with empty space below.
- [ ] No chart touches or overlaps its neighbors: at least 16px clear to the title, takeaways panel, note, assumptions box and footer, and no label or legend clipped at the SVG edge. Check every chart slide in the headless-Chrome render and in print.
- [ ] One accent color per chart; every color has a second encoding; at most 3 series colors (ink, blue, orange), context in light grey, one encoding per line; text contrast ≥ 4.5:1.
- [ ] Footer has topic, as-of date, baseline, ticket key; `n / N` renders.
- [ ] No `<img>`, no external script, font or stylesheet (`grep -E 'src="http|href="http|<img|@import|url\(http'` returns nothing); fonts are the system stacks in `deck.css`; light house theme only.
- [ ] Print to PDF: one slide per page, detail panels on their own pages, scenario panes side by side, nothing cut off.
- [ ] File name follows the naming rule; the older version is archived unchanged.
- [ ] `build.sh` (or the command) that rebuilds the deck is committed on a pushed branch.

Render check: `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --window-size=1600,900 --screenshot=<tmp>.png file://<deck>.html` shows the first slide; add `--print-to-pdf=<tmp>.pdf` to page through all of them.

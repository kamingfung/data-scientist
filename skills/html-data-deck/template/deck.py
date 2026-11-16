"""Builders for the HTML data deck.

Copy this file (with charts.py, deck.css, deck.js, interact.js) next to the deck
generator, or import it by path. It writes one self-contained HTML file: CSS and JS
are inlined, charts are inline SVG strings (charts.py), nothing loads from the
network.

Two build paths:
- Hybrid (default): hand-written slide HTML with {{num:key}}, {{chart:key}} and
  {{table:key}} placeholders, filled from data by build().
- Generator: slide() and the block builders assemble every slide in Python;
  see _demo() below.

    python3 deck.py /tmp/skeleton.html   # renders the generator demo
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent

# Figure-like tokens in rendered text: numbers with k/M/% units, signed numbers,
# "n of m" counts, decimals. Extend UNIT_WORDS for your deck.
UNIT_WORDS = "kg|hours|days|fields|weeks"
FIGURE = re.compile(
    r"[+−-]?\d[\d,]*(?:\.\d+)?(?:M|k|%)"
    r"|[+−]\d[\d,]*(?:\.\d+)?"
    r"|\d[\d,]* of \d[\d,]*"
    rf"|\d[\d,]*(?:\.\d+)?(?= (?:{UNIT_WORDS})\b)"
    r"|\d+\.\d+"
)


class Fig:
    """Formats figures and remembers every string it printed, so check() can
    prove no figure in the deck was typed by hand."""

    def __init__(self):
        self.seen: set[str] = set()

    def _keep(self, s):
        self.seen.update(FIGURE.findall(s))
        self.seen.add(s)  # a bare number matches FIGURE once a unit word follows it
        return s

    def m(self, v):
        """1.57M / 394k / 1,234; true minus sign, no plus."""
        a, s = abs(v), "−" if v < 0 else ""
        t = (
            f"{a / 1e6:.2f}M"
            if a >= 1e6
            else f"{a / 1e3:.0f}k"
            if a >= 1e3
            else f"{a:,.0f}"
        )
        return self._keep(s + t)

    def ms(self, v):
        """Signed: +1.57M / −394k."""
        return self._keep(("+" if v > 0 else "") + self.m(v))

    def pct(self, v):
        return self._keep(f"{v:.0%}".replace("-", "−"))

    def of(self, a, b):
        return self._keep(f"{a:,} of {b:,}")

    def rng(self, lo, hi):
        """Range text for a tile's sub line or a bullet: '+1.63M to +4.07M'."""
        return f"{self.ms(lo)} to {self.ms(hi)}"


def check(fig, deck_html, allowed=()):
    """Raise if the rendered deck holds a figure that did not pass through fig.
    ``allowed`` lists literal tokens that are not data (dates in the footer,
    slide numbers in cross-references, years)."""
    text = html.unescape(
        re.sub(r"<style>.*?</style>|<script>.*?</script>|<[^>]+>", " ", deck_html, flags=re.S)
    )
    stray = sorted(set(FIGURE.findall(text)) - fig.seen - set(allowed))
    if stray:
        raise ValueError(f"figures not computed through Fig: {stray}")


def slide(kicker, title, body, footer, note=None, assume=(), cls=""):
    """One 1280x720 slide: numbered kicker, action title, body, optional
    takeaway note, optional assumptions box, footer (deck.js adds n / N).
    ``cls`` adds a slide class ("cover")."""
    n = f'<p class="note">{note}</p>' if note else ""
    a = (
        '<div class="assume"><b>Assumptions and limitations.</b> '
        + " ".join(assume)
        + "</div>"
        if assume
        else ""
    )
    return (
        f'<section class="slide {cls}"><header><p class="kicker">{html.escape(kicker)}</p>'
        f"<h1>{html.escape(title)}</h1></header><div class=\"body\">{body}</div>"
        f"{n}{a}<footer>{html.escape(footer)}</footer></section>"
    )


def cover(kicker, title, lead, meta, footer):
    """Title slide or section divider: big title at the bottom, a lead sentence,
    and a meta row (date, audience, agenda)."""
    m = "".join(f"<span>{x}</span>" for x in meta)
    return slide(kicker, title, f'<p class="lead">{lead}</p><div class="meta">{m}</div>', footer, cls="cover")


def big_number(value, label, sub=""):
    """Workshop headline: one number and one sentence."""
    return f'<div class="big"><div class="big-num">{value}</div><p class="big-label">{label}</p><p class="small">{sub}</p></div>'


def cards(options):
    """Option cards side by side. options: [(tag, title, upside, failure_mode, pick)];
    pick=True marks the recommended option with a blue rule and the word "Pick"."""
    return '<div class="cards">' + "".join(
        f'<div class="card{" pick" if pick else ""}"><span class="tag">{tag}{" · Pick" if pick else ""}</span>'
        f"<h3>{t}</h3><p><b>Upside.</b> {up}</p><p><b>Fails when.</b> {fail}</p></div>"
        for tag, t, up, fail, pick in options
    ) + "</div>"


def exec_summary(lead, sections):
    """Executive summary, the first slide after the title. lead: one sentence;
    sections: 3-4 [(heading, [(label, sentence)])], 1-2 bullets each. The
    headings carry the message alone; keep the body to about 60-90 words."""
    secs = "".join(
        f"<li><h3>{h}</h3><ul>{''.join(f'<li><b>{lab}:</b> {txt}</li>' for lab, txt in pts)}</ul></li>"
        for h, pts in sections
    )
    return f'<div class="exec"><p class="exec-lead">{lead}</p><ol>{secs}</ol></div>'


def takeaways(main, points, next_):
    """Chart slide body: ``main`` (the chart) on the left 3/4, a panel "Key
    takeaways" panel on the right with 2-3 points [(label, sentence)] and an
    ink "Next:" arrow tag that leads into the next slide."""
    li = "".join(f"<li><b>{lab}:</b> {txt}</li>" for lab, txt in points)
    return (
        f'<div class="with-take"><div><div class="fill">{main}</div></div><aside class="take"><h3>Key takeaways</h3>'
        f'<ul>{li}</ul><span class="next">Next: {next_}</span></aside></div>'
    )


def notes_panel(prompts):
    """Question slide body: 2-3 prompts and an empty panel for live capture."""
    li = "".join(f"<li>{p}</li>" for p in prompts)
    return f'<div class="q"><div><h3>Prompts</h3><ul>{li}</ul></div><div class="notes"><h3>Notes from the room</h3></div></div>'


def detail(pid, label, body, tone=""):
    """Click-to-expand panel; interact.js prints it on its own page after the
    slide. tone="corr" is the red "Corrected" variant."""
    return (
        f'<button class="xp-btn {tone}" aria-expanded="false" aria-controls="{pid}">{html.escape(label)} ▸</button>'
        f'<div class="xp-panel {tone}" id="{pid}" hidden><h4>{html.escape(label)}</h4>{body}</div>'
    )


def tabs(panes):
    """Scenario toggle on one slide. panes: [(label, html)]; the first shows on
    screen, print lays all panes side by side under their labels."""
    bar = "".join(
        f'<button role="tab" aria-selected="{"true" if i == 0 else "false"}">{html.escape(lab)}</button>'
        for i, (lab, _) in enumerate(panes)
    )
    body = "".join(
        f'<div class="tab-panel" role="tabpanel"{"" if i == 0 else " hidden"}><h4>{html.escape(lab)}</h4>{h}</div>'
        for i, (lab, h) in enumerate(panes)
    )
    return f'<div class="tabs"><div class="tab-bar" role="tablist">{bar}</div>{body}</div>'


def mock(text="Mock data"):
    """Corner stamp for slides whose numbers are mock or not yet verified."""
    return f'<div class="mock">{html.escape(text)}</div>'


def tiles(items):
    """items: [(label, value, sub, cls)]; cls "neg" colors a loss red."""
    return (
        '<div class="tiles">'
        + "".join(
            f'<div class="tile"><div class="label">{lab}</div><div class="num {cls}">{val}</div><div class="sub">{sub}</div></div>'
            for lab, val, sub, cls in items
        )
        + "</div>"
    )


def two_cols(left_title, left_items, right_title, right_items, compact=True):
    """The "What happened / Why" pair; each bullet ends with its slide reference."""

    def col(t, items):
        return f"<div><h3>{t}</h3><ul>{''.join(f'<li>{x}</li>' for x in items)}</ul></div>"

    cls = "cols compact" if compact else "cols"
    return f'<div class="{cls}">{col(left_title, left_items)}{col(right_title, right_items)}</div>'


def table(headers, rows, align_right_from=1):
    th = "".join(f"<th>{html.escape(str(x))}</th>" for x in headers)
    body = []
    for r in rows:
        tds = "".join(
            f'<td class="{"num" if j >= align_right_from else ""}">{html.escape(str(x))}</td>'
            for j, x in enumerate(r)
        )
        body.append(f"<tr>{tds}</tr>")
    return f"<table><thead><tr>{th}</tr></thead><tbody>{''.join(body)}</tbody></table>"


# Chart slots in px (width, height): the body of a 1280x720 slide with a one-line
# title and a note line. Pass one as box= to every charts.py builder; the CSS
# (.fill) then stretches the SVG to the real slot, so text stays near its size.
SLOTS = {"full": (1168, 520), "take": (858, 500), "half": (572, 520)}
INTERACTIVE = re.compile(r'data-tip=|data-src=|class="xp-btn|class="tabs"')


def page(title, slides):
    """The whole self-contained file. interact.js is inlined only when a slide
    uses a tooltip, a sourced number, a detail panel or a scenario toggle."""
    read = lambda f: (HERE / f).read_text(encoding="utf-8")  # noqa: E731
    body = "".join(slides)
    js = read("deck.js") + (read("interact.js") if INTERACTIVE.search(body) else "")
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width">'
        f"<title>{html.escape(title)}</title><style>{read('deck.css')}</style></head><body>"
        f'<div class="deck">{body}</div>'
        '<p class="hint">Scroll, or press F for presentation mode and use the arrow keys. Print to PDF for a file.</p>'
        f"<script>{js}</script></body></html>"
    )


# ---- Hybrid build: hand-written slides, data-filled placeholders ----

PLACEHOLDER = re.compile(r"\{\{(num|chart|table):([A-Za-z0-9_]+)\}\}")
# Digits a hand-written slide may contain: ISO dates, years and seasons (2024/25),
# ticket keys, slide references, and the number at the start of a kicker.
ALLOWED_DIGITS = re.compile(
    r"\b\d{4}-\d{2}(?:-\d{2})?\b"
    r"|\b(?:19|20)\d{2}(?:/\d{2})?\b"
    r"|\b[A-Z][A-Z0-9]*-\d+\b"
    r"|\bslides?[ \xa0]\d+(?:\.\d+)?(?:(?:, | and | to |–)\d+(?:\.\d+)?)*"
)


def build(title, template, fig, nums, charts=None, tables=None, sources_footer="", allowed=()):
    """Fill a hand-written deck and return the page.

    template: slide HTML (<section class="slide">...</section> blocks) whose
    numbers, charts and tables are placeholders. nums: {key: (text, source)},
    text formatted through ``fig``, source = query id, run id or file plus pull
    date. charts / tables: {key: html} from charts.py and table(). Appends
    "Backup · Sources" slides listing slide, value and source for every number.
    Raises on a digit typed outside a placeholder, on an unknown or malformed
    placeholder, and (via check) on a figure that did not pass through ``fig``."""
    template = re.sub(r"<!--.*?-->", "", template, flags=re.S)
    check_template(template, allowed)
    filled = fill(template, nums, charts or {}, tables or {})
    out = page(title, [filled, *sources_slides(template, nums, sources_footer)])
    refs = re.findall(r'<p class="kicker">\s*(\d+(?:\.\d+)*)', template) + re.findall(r"\d+\.\d+", " ".join(ALLOWED_DIGITS.findall(template)))
    check(fig, out, allowed=(*allowed, *refs))
    return out


def check_template(template, allowed=()):
    """Raise if hand-written text holds a digit outside a placeholder.
    ``allowed`` lists extra literal tokens (a code name such as matrix_2x2)."""
    t = re.sub(r"<style>.*?</style>|<script>.*?</script>", " ", template, flags=re.S)
    t = re.sub(r'(<p class="kicker">)\s*\d+(?:\.\d+)*', r"\1", t)
    t = html.unescape(PLACEHOLDER.sub(" ", re.sub(r"<[^>]+>", " ", t)))
    for a in allowed:
        t = t.replace(a, " ")
    typed = sorted(set(re.findall(r"\S*\d\S*", ALLOWED_DIGITS.sub(" ", t))))
    if typed:
        raise ValueError(f"digits typed outside a placeholder: {typed}")


def fill(template, nums, charts, tables):
    """Replace every placeholder; raise on an unknown key or a leftover {{."""
    pools = {"num": nums, "chart": charts, "table": tables}

    def one(mt):
        kind, key = mt.groups()
        if key not in pools[kind]:
            raise KeyError(f"unresolved placeholder {{{{{kind}:{key}}}}}: no {kind} named {key!r}")
        if kind != "num":
            return pools[kind][key]
        text, src = nums[key]
        return f'<span class="n" data-src="{html.escape(src)}">{text}</span>'

    out = PLACEHOLDER.sub(one, template)
    if "{{" in out:
        raise ValueError(f"malformed placeholder near {out[out.index('{{'):][:40]!r}")
    return out


def sources_slides(template, nums, footer, rows_per_slide=14):
    """The "Backup · Sources" slides: one row per number per slide."""
    rows = []
    for sec in template.split('<section class="slide')[1:]:
        k = re.search(r'<p class="kicker">(.*?)</p>', sec, flags=re.S)
        where = " · ".join(html.unescape(re.sub(r"<[^>]+>", "", k.group(1))).split(" · ")[:2]).strip() if k else "?"
        for key in dict.fromkeys(m.group(2) for m in PLACEHOLDER.finditer(sec) if m.group(1) == "num"):
            if key in nums:
                rows.append([where, key, nums[key][0], nums[key][1]])
    pages = [rows[i : i + rows_per_slide] for i in range(0, len(rows), rows_per_slide)]
    return [
        slide(
            "Backup · Sources",
            f"Every number in this deck and where it came from{f' (part {p + 1})' if len(pages) > 1 else ''}",
            f'<div class="compact">{table(["Slide", "Key", "Value", "Source"], chunk, align_right_from=99)}</div>',
            footer,
        )
        for p, chunk in enumerate(pages)
    ]


def _demo():
    """Skeleton with made-up inputs; every figure still goes through Fig."""
    F = Fig()
    d = {"baseline": 950.0, "current": 820.0, "a": 120.0, "a_lo": 80.0, "a_hi": 150.0}
    gap = d["current"] - d["baseline"]
    footer = "Topic · as of YYYY-MM-DD · baseline: own prior seasons, same weeks · KEY-123"
    s1 = slide(
        "0 · Headline",
        f"Output is {F.pct(d['current'] / d['baseline'])} of baseline; driver A explains {F.pct(d['a'] / -gap)} of the gap",
        tiles(
            [
                ("Gap", F.ms(gap) + " kg", "against the baseline, same weeks", "neg"),
                ("Driver A at baseline level", F.ms(d["a"]) + " kg", "five fits " + F.rng(d["a_lo"], d["a_hi"]), ""),
            ]
        )
        + two_cols(
            "What happened",
            [f"Output {F.m(d['current'])} kg against {F.m(d['baseline'])} kg (slide 2)."],
            "Why",
            [f"Driver A gives back {F.ms(d['a'])} kg (slide 3)."],
        ),
        footer,
        assume=["The baseline is the mean of the reference seasons at the same weeks."],
    )
    s2 = slide(
        "1 · The ask",
        "The ask: one owner, one action, one date per row",
        table(["Owner", "Ask", "Why, from this analysis", "DRI", "By when"], [["Team", "Action", "Evidence (slide 3)", "Name", "YYYY-MM-DD"]], align_right_from=99),
        footer,
    )
    out = page("Deck title", [s1, s2])
    check(F, out)
    return out


if __name__ == "__main__":
    Path(sys.argv[1]).write_text(_demo(), encoding="utf-8")

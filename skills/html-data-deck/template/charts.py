"""Inline SVG chart builders for house decks, one per row of the SKILL.md
relationship table. Each returns an <svg class="chart"> string for a
{{chart:key}} placeholder or a slide() body.

- Every builder takes ``box=(width, height)`` in px, the slot it fills
  (deck.SLOTS: full body, left 3/4 next to takeaways, half body). The viewBox
  equals the box, so 1 unit = 1 px: layout, axis ranges, nice ticks and label
  gutters are recomputed for the box and text keeps its normal size.

- Colors are CSS classes (f-* fill, s-* stroke) bound to the house tokens in deck.css.
- Every number drawn goes through the ``fmt`` the caller passes (a Fig method), so
  check() still proves no figure was typed.
- Every mark with a value carries data-tip; interact.js shows it on hover. Print has
  no hover, so the values the argument needs are also drawn as labels.
- Every color has a second encoding: direct label, dash, marker shape or icon.
"""

from __future__ import annotations

import html
import math

CAT = ("ink", "blue", "orange", "light")  # 3 series colors, then context grey for "other" (SKILL.md Colors)
STATUS = {"kept": ("✅", "blue"), "dropped": ("✖", "red"), "open": ("⏸", "gray")}


def _svg(box, label, inner):
    return f'<svg class="chart" viewBox="0 0 {box[0]:.0f} {box[1]:.0f}" width="100%" role="img" aria-label="{html.escape(label)}">{inner}</svg>'


def _t(x, y, s, cls="", anchor="start", size=13, weight=""):
    c = f' class="{cls}"' if cls else ""
    w = f' font-weight="{weight}"' if weight else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="{size}"{w}{c}>{html.escape(str(s))}</text>'


def _lines(x, y, s, width, cls="", anchor="start", size=13, weight=""):
    """Word-wrapped text: one <text> per line of at most ``width`` characters."""
    rows, cur = [], ""
    for word in str(s).split():
        if cur and len(cur) + 1 + len(word) > width:
            rows.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    rows.append(cur)
    return "".join(_t(x, y + i * size * 1.25, r, cls, anchor, size, weight) for i, r in enumerate(rows))


def _tip(s):
    return f' data-tip="{html.escape(s)}"'


def _box(x, y, w, h, fill="f-paper", stroke="s-light", sw=1.5, extra=""):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="5" class="{fill} {stroke}" stroke-width="{sw}"{extra}/>'


def _arrow(x1, y1, x2, y2, color="ink"):
    """Line with a drawn arrowhead (no <marker>: ids would clash across slides)."""
    a = math.atan2(y2 - y1, x2 - x1)
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="s-{color}" stroke-width="1.6"/>' + _head(x2, y2, a, color)


def _head(x, y, a, color="ink", size=9):
    p = [(x, y), (x - size * math.cos(a) + size / 2 * math.sin(a), y - size * math.sin(a) - size / 2 * math.cos(a)),
         (x - size * math.cos(a) - size / 2 * math.sin(a), y - size * math.sin(a) + size / 2 * math.cos(a))]
    return f'<polygon points="{" ".join(f"{px:.1f},{py:.1f}" for px, py in p)}" class="f-{color}"/>'


def _nice(lo, hi, n):
    """About n nice tick intervals (step 1, 2 or 5 x 10^k) covering lo..hi."""
    raw = (hi - lo) / n or 1
    mag = 10 ** math.floor(math.log10(raw))
    step = next(k * mag for k in (1, 2, 5, 10) if k * mag >= raw)
    y0, y1 = math.floor(lo / step) * step, math.ceil(hi / step) * step
    return [y0 + i * step for i in range(round((y1 - y0) / step) + 1)]


def line_chart(series, xs, fmt, label, box, unit=""):
    """Change over time. series: [(name, values, color, dashed)]; color from CAT
    or "gray"; give the accent to the series the title claims, dash the baseline.
    Each point has a hover tip; the end of each line carries name and last value."""
    w, h = box
    vals = [v for _, vs, _, _ in series for v in vs]
    ticks = _nice(min(vals), max(vals), max(3, int(h // 90)))
    y0, y1 = ticks[0], ticks[-1]
    ends_txt = [f"{name} {fmt(vs[-1])}" for name, vs, _, _ in series]
    l, r, t, b = 14 + 8 * max(len(fmt(v)) for v in ticks), 20 + 7.5 * max(map(len, ends_txt)), 28, 30
    n = len(xs)
    X = lambda i: l + i * (w - l - r) / (n - 1)  # noqa: E731
    Y = lambda v: t + (y1 - v) / (y1 - y0) * (h - t - b)  # noqa: E731
    out = [_t(0, 13, unit, "m", size=12)] if unit else []
    for v in ticks:
        out.append(f'<line x1="{l}" x2="{w - r:.1f}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" class="s-light" stroke-width="0.6"/>')
        out.append(_t(l - 8, Y(v) + 4, fmt(v), "m", "end", 12))
    step = max(1, math.ceil(n / ((w - l - r) / 70)))
    out += [_t(X(i), h - 8, xs[i], "m", "middle", 12) for i in range(0, n, step)]
    ends = []
    for (name, vs, color, dashed), txt in zip(series, ends_txt):
        pts = " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(vs))
        out.append(f'<polyline points="{pts}" class="f-none s-{color}{" dash" if dashed else ""}" stroke-width="2.5"/>')
        for i, v in enumerate(vs):
            if n <= 20:  # dense series: hover targets only, no visible dots
                out.append(f'<circle cx="{X(i):.1f}" cy="{Y(v):.1f}" r="3.5" class="f-{color}"/>')
            out.append(f'<circle cx="{X(i):.1f}" cy="{Y(v):.1f}" r="9" class="hit"{_tip(f"{name} · {xs[i]}: {fmt(v)}")}/>')
        ends.append([Y(vs[-1]), txt])
    ends.sort()
    for k in range(1, len(ends)):  # keep end labels 16 px apart
        ends[k][0] = max(ends[k][0], ends[k - 1][0] + 16)
    out += [_t(X(n - 1) + 10, y + 4, s, weight="600") for y, s in ends]
    return _svg(box, label, "".join(out))


def sorted_bars(rows, fmt, label, box, accent=()):
    """Category comparison: horizontal bars sorted by value. Names in ``accent``
    get blue, losses red, the rest light; every bar carries its value label."""
    w, h = box
    rows = sorted(rows, key=lambda r: -r[1])
    rh = h / len(rows)
    l, r = 20 + 7.5 * max(len(n) for n, _ in rows), 20 + 8 * max(len(fmt(v)) for _, v in rows)
    lo, hi = min(0, min(v for _, v in rows)), max(0, max(v for _, v in rows))
    X = lambda v: l + (v - lo) / (hi - lo) * (w - l - r)  # noqa: E731
    bh = min(rh * 0.62, 48)
    out = []
    for i, (name, v) in enumerate(rows):
        yc = i * rh + rh / 2
        cls = "f-red" if v < 0 else "f-blue" if name in accent else "f-light"
        x, bw = min(X(0), X(v)), abs(X(v) - X(0))
        out.append(_t(l - 10, yc + 5, name, anchor="end", size=14))
        out.append(f'<rect x="{x:.1f}" y="{yc - bh / 2:.1f}" width="{bw:.1f}" height="{bh:.1f}" class="{cls}"{_tip(f"{name}: {fmt(v)}")}/>')
        out.append(_t(X(v) + 6 if v >= 0 else X(0) + 6, yc + 5, fmt(v), "m", size=13, weight="600"))
    out.append(f'<line x1="{X(0):.1f}" x2="{X(0):.1f}" y1="0" y2="{h}" class="s-ink" stroke-width="1"/>')
    return _svg(box, label, "".join(out))


def waterfall(start, steps, end_label, fmt, dfmt, label, box):
    """Contribution to a total: start bar, one bar per factor, end bar.
    start: (label, value); steps: [(label, delta)]. Totals ink, gains blue,
    losses red; the sign in each label is the second encoding."""
    w, h = box
    t, b = 26, 46
    cum = [start[1]]
    for _, d in steps:
        cum.append(cum[-1] + d)
    lo, hi = min(0, *cum), max(0, *cum)
    n = len(steps) + 2
    slot = w / n
    Y = lambda v: t + (hi - v) / (hi - lo) * (h - t - b)  # noqa: E731
    bars = [(start[0], 0, start[1], "f-ink", fmt(start[1]))]
    bars += [(s, cum[i], cum[i + 1], "f-blue" if d > 0 else "f-red", dfmt(d)) for i, (s, d) in enumerate(steps)]
    bars.append((end_label, 0, cum[-1], "f-ink", fmt(cum[-1])))
    out = []
    for i, (name, a, z, cls, txt) in enumerate(bars):
        x = i * slot + slot * 0.2
        out.append(f'<rect x="{x:.1f}" y="{Y(max(a, z)):.1f}" width="{slot * 0.6:.1f}" height="{max(abs(Y(a) - Y(z)), 1):.1f}" class="{cls}"{_tip(f"{name}: {txt}")}/>')
        out.append(_t(x + slot * 0.3, Y(max(a, z)) - 7, txt, anchor="middle", size=13, weight="600"))
        out.append(_lines(x + slot * 0.3, h - b + 20, name, int(slot / 7.5), "m", "middle", 12.5))
        if i < n - 1:
            out.append(f'<line x1="{x + slot * 0.6:.1f}" x2="{x + slot:.1f}" y1="{Y(z):.1f}" y2="{Y(z):.1f}" class="s-gray dash" stroke-width="1"/>')
    out.append(f'<line x1="0" x2="{w}" y1="{Y(0):.1f}" y2="{Y(0):.1f}" class="s-ink" stroke-width="1"/>')
    return _svg(box, label, "".join(out))


def stacked_bar(rows, parts, fmt, label, box):
    """Shares of a total: one 100% bar per row, parts in CAT order, a legend row
    on top, and the share written inside every segment wide enough to hold it."""
    w, h = box
    l, top = 20 + 7.5 * max(len(n) for n, _ in rows), 34
    rh = (h - top) / len(rows)
    bh = min(rh * 0.7, 64)
    out, lx = [], l
    for j, p in enumerate(parts):
        out.append(f'<rect x="{lx}" y="6" width="14" height="14" class="f-{CAT[j]}"/>')
        out.append(_t(lx + 20, 18, p))
        lx += 34 + 8 * len(p)
    for i, (name, vs) in enumerate(rows):
        yc, x, tot = top + i * rh + rh / 2, l, sum(vs)
        out.append(_t(l - 10, yc + 5, name, anchor="end", size=14))
        for j, v in enumerate(vs):
            sw = v / tot * (w - l - 4)
            out.append(f'<rect x="{x:.1f}" y="{yc - bh / 2:.1f}" width="{sw:.1f}" height="{bh:.1f}" class="f-{CAT[j]} s-paper"{_tip(f"{name} · {parts[j]}: {fmt(v / tot)}")}/>')
            if sw > 44:
                out.append(_t(x + sw / 2, yc + 5, fmt(v / tot), "on" if j < 3 else "", "middle", 14, "600"))
            x += sw
    return _svg(box, label, "".join(out))


def matrix_2x2(x_label, y_label, quadrants, points, label, box):
    """Two-variable classification. quadrants: (top_left, top_right, bottom_left,
    bottom_right) labels; points: [(name, x, y, accent)] with x, y in 0..1.
    The accent point is filled blue, the others are hollow."""
    w, h = box
    l, r, t, b = 40, 20, 6, 34
    pw, ph = w - l - r, h - t - b
    out = [_box(l, t, pw, ph, "f-paper", "s-light")]
    out.append(f'<line x1="{l + pw / 2:.1f}" x2="{l + pw / 2:.1f}" y1="{t}" y2="{t + ph}" class="s-light" stroke-width="1.5"/>')
    out.append(f'<line x1="{l}" x2="{l + pw}" y1="{t + ph / 2:.1f}" y2="{t + ph / 2:.1f}" class="s-light" stroke-width="1.5"/>')
    for k, q in enumerate(quadrants):
        out.append(_t(l + 14 + (k % 2) * pw / 2, t + 24 + (k // 2) * ph / 2, q, "m", size=14, weight="600"))
    out.append(_t(l + pw / 2, h - 8, f"{x_label} →", "m", "middle", 13))
    out.append(f'<text x="{l - 14}" y="{t + ph / 2:.1f}" text-anchor="middle" font-size="13" class="m" transform="rotate(-90 {l - 14} {t + ph / 2:.1f})">{html.escape(y_label)} →</text>')
    for name, x, y, accent in points:
        cx, cy = l + x * pw, t + (1 - y) * ph
        cls = "f-blue s-blue" if accent else "f-paper s-ink"
        out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="9" class="{cls}" stroke-width="2"{_tip(name)}/>')
        out.append(_t(cx + 15, cy + 5, name, size=14, weight="600" if accent else ""))
    return _svg(box, label, "".join(out))


def flow(steps, label, box, highlight=()):
    """Ordered actions: boxes left to right with arrows. steps: [(name, sub)];
    names in ``highlight`` get a dashed red border and a "? in question" tag."""
    w, h = box
    n, gap = len(steps), 40
    bw = (w - gap * (n - 1)) / n
    bh = min(h - 60, 220)
    y = 30 + (h - 30 - bh) / 2
    out = []
    for i, (name, sub) in enumerate(steps):
        x = i * (bw + gap)
        q = name in highlight
        out.append(_box(x, y, bw, bh, "f-panel" if q else "f-paper", "s-red dash" if q else "s-light", 2.5 if q else 1.5))
        if q:
            out.append(_t(x + bw / 2, y - 10, "? in question", "m", "middle", 14, "700"))
        out.append(_lines(x + bw / 2, y + bh / 2 - 8, name, int(bw / 9.5), anchor="middle", size=17, weight="700"))
        out.append(_lines(x + bw / 2, y + bh / 2 + 22, sub, int(bw / 7.5), "m", "middle", 13))
        if i < n - 1:
            out.append(_arrow(x + bw + 4, y + bh / 2, x + bw + gap - 4, y + bh / 2))
    return _svg(box, label, "".join(out))


def cycle(steps, label, box, center=""):
    """Recurring activity: steps on a closed ring, arrowheads between them show
    the direction; ``center`` names the cadence."""
    w, h = box
    n, cx, cy = len(steps), w / 2, h / 2
    rx, ry = w / 2 - 110, h / 2 - 34
    pt = lambda a: (cx + rx * math.cos(a), cy + ry * math.sin(a))  # noqa: E731
    ang = [-math.pi / 2 + 2 * math.pi * i / n for i in range(n)]
    out = [f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" class="f-none s-accent" stroke-width="2"/>']
    for i in range(n):
        m = ang[i] + math.pi / n
        x, y = pt(m)
        out.append(_head(x, y, math.atan2(ry * math.cos(m), -rx * math.sin(m)), "accent", 14))
    for a, s in zip(ang, steps):
        x, y = pt(a)
        out.append(_box(x - 100, y - 26, 200, 52, "f-paper", "s-ink", 1.5))
        out.append(_lines(x, y - 3 if len(s) > 24 else y + 5, s, 24, anchor="middle", size=14, weight="600"))
    out.append(_t(cx, cy + 6, center, "m", "middle", 17, "600"))
    return _svg(box, label, "".join(out))


def fishbone(problem, causes, label, box):
    """Causes of one problem: a spine to the problem box, one bone per cause
    category (alternating above and below), items along each bone."""
    w, h = box
    sy, hw = h / 2, 200
    x_head = w - hw
    k = math.ceil(len(causes) / 2)
    gap = (x_head - 200) / k
    reach = sy - 34
    out = [_arrow(20, sy, x_head - 4, sy, "ink"), _box(x_head, sy - 46, hw, 92, "f-panel", "s-ink", 2)]
    out.append(_lines(x_head + hw / 2, sy - 6, problem, 20, anchor="middle", size=16, weight="700"))
    for i, (cat, items) in enumerate(causes):
        up = i % 2 == 0
        xb = 80 + gap * (i // 2 + 1)
        xe, ye = xb - reach * 0.45, (sy - reach) if up else (sy + reach)
        out.append(f'<line x1="{xb:.1f}" y1="{sy:.1f}" x2="{xe:.1f}" y2="{ye:.1f}" class="s-accent" stroke-width="2"/>')
        out.append(_t(xe, ye - 10 if up else ye + 22, cat, anchor="middle", size=15, weight="700"))
        for m, item in enumerate(items):
            f = (m + 1) / (len(items) + 1)
            out.append(_t(xe + (xb - xe) * f + 8, ye + (sy - ye) * f + 5, item, "m", size=13))
    return _svg(box, label, "".join(out))


def gantt(lanes, periods, gates, label, box):
    """Workstreams and dates: one swim lane per team. lanes: [(team, [(task,
    start, end, done)])] in period indexes (end exclusive); done bars are solid
    ink, planned bars on the panel color with a dashed outline; gates: [(name, at)] diamonds."""
    w, h = box
    l, top, bottom = 20 + 8 * max(len(t) for t, _ in lanes), 30, 50
    lh = (h - top - bottom) / len(lanes)
    cw = (w - l) / len(periods)
    bh = min(lh * 0.55, 40)
    X = lambda p: l + p * cw  # noqa: E731
    out = [_t(X(i) + cw / 2, 18, p, "m", "middle", 13, "600") for i, p in enumerate(periods)]
    for i, (team, tasks) in enumerate(lanes):
        y = top + i * lh
        out.append(f'<line x1="0" x2="{w}" y1="{y:.1f}" y2="{y:.1f}" class="s-light" stroke-width="0.8"/>')
        out.append(_t(0, y + lh / 2 + 5, team, size=14, weight="600"))
        for task, a, z, done in tasks:
            tip = _tip(f"{team} · {task}: {periods[a]} to {periods[z - 1]}")
            cls = "f-ink s-ink" if done else "f-panel s-ink dash"
            out.append(f'<rect x="{X(a) + 2:.1f}" y="{y + (lh - bh) / 2:.1f}" width="{(z - a) * cw - 4:.1f}" height="{bh:.1f}" rx="4" class="{cls}" stroke-width="1.2"{tip}/>')
            out.append(_t(X(a) + 12, y + lh / 2 + 5, task, "on" if done else "", size=13.5))
    yb = top + len(lanes) * lh
    for name, at in gates:
        x = X(at)
        out.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{top}" y2="{yb:.1f}" class="s-accent dash" stroke-width="1.2"/>')
        out.append(f'<polygon points="{x:.1f},{yb + 2:.1f} {x + 9:.1f},{yb + 11:.1f} {x:.1f},{yb + 20:.1f} {x - 9:.1f},{yb + 11:.1f}" class="f-accent"{_tip(f"Gate: {name}")}/>')
        out.append(_t(x, yb + 38, name, "m", "middle", 13, "600"))
    return _svg(box, label, "".join(out))


def hierarchy(root, children, label, box):
    """Levels: a root, one row of children, each child's items listed below it."""
    w, h = box
    n = len(children)
    cw = w / n
    deepest = max(len(items) for _, items in children)
    ih = min((h - 150) / deepest, 56)
    out = [_box(w / 2 - 140, 4, 280, 48, "f-ink", "s-ink"), _t(w / 2, 34, root, "on", "middle", 16, "700")]
    out.append(f'<line x1="{w / 2}" x2="{w / 2}" y1="52" y2="72" class="s-ink"/>')
    out.append(f'<line x1="{cw / 2}" x2="{w - cw / 2}" y1="72" y2="72" class="s-ink"/>')
    for i, (name, items) in enumerate(children):
        x = i * cw + cw / 2
        out.append(f'<line x1="{x}" x2="{x}" y1="72" y2="92" class="s-ink"/>')
        out.append(_box(x - cw / 2 + 8, 92, cw - 16, 46, "f-panel", "s-ink"))
        out.append(_t(x, 121, name, anchor="middle", size=15, weight="700"))
        for m, item in enumerate(items):
            y = 152 + m * ih
            out.append(f'<line x1="{x - cw / 2 + 22}" x2="{x - cw / 2 + 22}" y1="{y - 14:.1f}" y2="{y + ih * 0.35:.1f}" class="s-light"/>')
            out.append(_box(x - cw / 2 + 32, y, cw - 50, ih * 0.7, "f-paper", "s-light"))
            out.append(_t(x - cw / 2 + 44, y + ih * 0.35 + 5, item, size=14))
    return _svg(box, label, "".join(out))


def timeline(events, label, box):
    """What was tried: dated markers on one axis. events: [(date, text, status)],
    status in STATUS (kept / dropped / open): icon, color and marker shape."""
    w, h = box
    n, ay = len(events), h / 2
    X = lambda i: 70 + i * (w - 140) / (n - 1)  # noqa: E731
    out = [_arrow(10, ay, w - 6, ay, "light")]
    for i, (date, text, status) in enumerate(events):
        icon, _ = STATUS[status]
        x, up = X(i), i % 2 == 0
        tip = _tip(f"{date} · {text}: {status}")
        if status == "kept":
            out.append(f'<circle cx="{x:.1f}" cy="{ay:.1f}" r="11" class="f-blue"{tip}/>')
        elif status == "dropped":
            out.append(f'<path d="M{x - 9:.1f},{ay - 9:.1f} l18,18 m0,-18 l-18,18" class="s-red" stroke-width="4.5"{tip}/>')
        else:
            out.append(f'<rect x="{x - 9:.1f}" y="{ay - 9:.1f}" width="18" height="18" class="f-gray"{tip}/>')
        out.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{ay + (-18 if up else 18):.1f}" y2="{ay + (-50 if up else 50):.1f}" class="s-light"/>')
        y = ay - 96 if up else ay + 74
        out.append(_t(x, y, date, "m", "middle", 13, "600"))
        out.append(_lines(x, y + 22, f"{icon} {text}", 20, anchor="middle", size=15))
    out.append(_t(w - 6, h - 6, "✅ kept · ✖ dropped · ⏸ open", "m", "end", 13))
    return _svg(box, label, "".join(out))

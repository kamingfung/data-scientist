# McKinsey Slide Design Specification

Empirical layout geometry, palette, and exhibit patterns extracted from 30 McKinsey `.pptx` decks.

## 1. Exact Slide Coordinates (`13.333" × 7.500"`)

| Zone | Left (`x`) | Top (`y`) | Width (`w`) | Height (`h`) | Typography |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Cover Title** | `0.60"` | `2.24"` | `6.58"` | `2.10"` | Georgia `24–28 pt`, `#FFFFFF` (dark) or `#051C2C` (light) |
| **Cover Subtitle / Date** | `0.60"` | `4.48"` / `4.93"` | `6.58"` | `0.34"` / `0.24"` | Arial `12–14 pt` |
| **Top-Right Tracker** | `7.83"` | `0.09"` | `4.90"` | `0.13"` | Arial `8 pt`, right-aligned, active section bold `#2251FF` |
| **Action Title** | `0.61"` | `0.20"` | `12.12"` (or `8.66"` for `3/4`) | `0.80"` (`1.13"` for 3-line) | Arial `14–16 pt` bold, `#051C2C` or `#000000` |
| **Subtitle / Lead-in** | `0.61"` | `0.99"` | `12.12"` | `0.30"` | Arial `11–12 pt`, `#303D48` + `0.5 pt` `#CCCCCC` rule below |
| **Body Canvas** | `0.61"` | `1.40"` | `12.12"` | `5.35"` | Arial `10–14 pt` body; `8–9 pt` dense tables/labels |
| **Source / Footnote** | `0.61"` | `6.95"` | `11.20"` | `0.30"` | Arial `7–8 pt`, `#303D48` (`Source: ...`) |
| **Slide Number** | `12.20"` | `6.95"` | `0.53"` | `0.30"` | Arial `8 pt`, right-aligned |

## 2. Color Palette

| Role | Hex | Usage |
| :--- | :--- | :--- |
| **Deep Navy** | `#051C2C` | Contrast backgrounds, primary headers, anchor data series |
| **Electric Blue** | `#2251FF` | Primary accent, active tracker/divider item, key callouts |
| **Cyan / Sky** | `#00A9F4` | Secondary chart series, highlights on dark navy slides |
| **Slate** | `#303D48` | Subtitles, secondary labels, source footnotes |
| **Light Card Fill** | `#E6E6E6` | Neutral card backgrounds, takeaway sidebars, zebra rows |
| **Soft Mint Fill** | `#EDF6F2` / `#E1F1E8` | Positive impact callouts, "To-Be" or opportunity highlight cards |
| **Mid-Gray Rule** | `#CCCCCC` / `#B3B3B3` | Thin (`0.5–0.75 pt`) horizontal/vertical dividers |
| **Semantic Status** | `#108980` / `#FFC000` / `#F17E7E` | Positive / Caution / Negative indicators |

## 3. Common Exhibit & Component Patterns

- **Flat Accent Card:** `RECTANGLE` with `#E6E6E6` (or `#EDF6F2`) fill, no outline, plus a `0.06"` top or left accent bar in `#2251FF` or `#051C2C`.
- **Harvey Balls / Status Badges:** `OVAL` (`0.22"`–`0.28"` diameter) for qualitative ratings (Empty / Quarter / Half / Three-Quarter / Full) or numbered step circles (`1`, `2`, `3`) in `#051C2C` with `#FFFFFF` bold Arial `10 pt`.
- **Chevron / Process Flow:** `RIGHT_ARROW` or pentagon chevrons across `12.12"` width (3–5 steps max), connected to 1-line bulleted deliverables below each step.
- **2×2 Matrix:** Thin `#B3B3B3` axes with centered labels, light-tinted winning quadrant (`#E1F1E8` or `#EDF6F2`), and `OVAL` plotted items with direct labels.
- **Sidebar Takeaway (`3/4 + 1/4`):** Left `8.80"` chart/table; right `2.90"` `#E6E6E6` panel titled `"Key takeaways"` with 3 bold-lead-in bullets (`<=15` words each).

## 4. Storylining, Lede & Content Patterns

- **Slide 2 Executive Synthesis ("N Themes" / Summary):**
  - Title: `"Four themes we are seeing in [Month Year]"` or `"Three takeaways from [Analysis]"`.
  - Body: `3–4` stacked horizontal rows or columns, each formatted as **`[Theme Label]: [1-sentence headline]`** followed by `1` line of quantified evidence.
- **Action Title (Lede) Formulas:**
  - *Trend / Shift:* `"[Metric] [rose/fell] [X%] in [Window] driven by [Driver]"`
  - *Comparison:* `"On a [volume/margin] basis, [Segment A] is [more/less] exposed to [Factor] than [Segment B]"`
  - *Value / Impact:* `"[Solution] enables [Target] to achieve [>X% / $Y] [savings/lift] by [Mechanism]"`
- **Content Delivery Triads (on `Default` or `1/2` slides):**
  - *Problem → Action → Value:* `Pain Points` | `Solutions` | `Results & Implications`
  - *Evidence → Meaning:* `What it shows (Impacts)` | `How to act on it (Usages)`
  - *Strategy → Execution:* `Why we are doing it` | `How we are doing it`
- **Multi-Slide Numbering:** Use `1.`, `2.` for main themes, `2A.`, `2B.` for sub-branches, and `(1/3)`, `(2/3)` when splitting dense tables or stories across slides.

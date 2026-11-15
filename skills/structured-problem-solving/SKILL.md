---
name: structured-problem-solving
description: Hypothesis-driven problem solving, MECE issue trees, quantitative 80/20 drill-down, and top-down synthesis. Use when structuring an open-ended investigation, diagnosing a root cause, sizing a market or impact, or evaluating strategic and architectural trade-offs.
---

# Structured Problem Solving

Apply a hypothesis-first, MECE (Mutually Exclusive, Collectively Exhaustive) workflow before diving into data or implementation. See [references/frameworks.md](references/frameworks.md) for customizable lenses and math templates.

## 1. First Five Steps (Before Analysis)

- **Clarify the question and metric:** restate the exact objective and quantify the target outcome (percentage, dollar impact, latency, timeline).
- **Probe scope and constraints:** identify affected segments, time window, and hard constraints before proposing causes.
- **State an initial hypothesis within five minutes:** pick the most probable answer upfront so every subsequent check tests, refines, or falsifies it.
- **Build a custom MECE `if/then` issue tree:** structure branches as testable conditions (`if X holds, then Y follows`), never as a rigid memorized checklist.
- **Prioritize the biggest lever first (80/20):** rank branches by expected impact and test the largest branch before exploring minor contributors.

## 2. Quantitative & Qualitative Drill-Down

- **Balance 70% quantitative / 30% qualitative:** anchor diagnosis in numbers first, then explain why the numbers moved using customer, operational, or technical context.
- **Segment every total and average:** break aggregate metrics by product, customer tier, channel, region, or cohort to uncover hidden shifts.
- **Compare historically and competitively:** benchmark current performance against prior periods and peers to separate internal issues from market-wide shifts.
- **Draft word-first formulas:** write out equations in plain words (`Profit = Price × Volume − Fixed Costs − Variable Costs`) before plugging in numbers.
- **Sanity-check every estimate:** verify units, orders of magnitude, and boundary cases before reporting a number.
- **Deliver mini-syntheses at branch transitions:** summarize what a branch proved or disproved before pivoting to the next branch.

## 3. Top-Down Synthesis Close

- **Lead with a binary recommendation:** open with `Yes` / `No` or the single recommended option, never a chronological recap of steps taken.
- **Support with at most three quantified facts:** list the three strongest pieces of evidence, ordered by impact.
- **Name risks and mitigations:** state the top 1–2 assumptions that could invalidate the recommendation and how to monitor them.
- **Propose concrete next steps:** end with immediate, owner-assigned actions and the decision or analysis needed next.

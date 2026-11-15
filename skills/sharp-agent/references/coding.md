# Sharp engineering

Build like a bamboo scaffolder: light, fast, built from what's on site (S35, S36). Inspect like the post-scandal MTR: digital forms and verified work, not trust (W62, W63).

The detailed code rules live in [../../developer-guides/SKILL.md](../../developer-guides/SKILL.md); this file is the posture, not a second rule set.

## Borrow
- **Check the kitchen first.** Grep for an existing helper, type or pattern before writing one. Re-implementing something a few files over is the commonest slop (S37, S38).
- **Grow the platform outward.** Extend the existing module or abstraction instead of adding a parallel one (S28, S29).
- **Small batch, fast turnover.** Make small diffs, run them, adjust. HK film crews edited while still shooting (S49). Iterate in production-like loops.
- **Use the codebase's shorthand.** Match its naming, idiom and comment density. Use the house order codes (S9, S10).
- **Orchestrate.** Fan out independent searches or reviews to subagents and keep the conclusions, not the dumps (S77).

## Guard
- **Rebar check: compiles ≠ works.** Run the test, hit the endpoint, open the page. Never report "done" on code you haven't executed or can't execute without saying so (W59, W60).
- **Never weaken the test to make it pass.** No skipping, loosening asserts or special-casing inputs. If it can't pass honestly, report why (W66).
- **Root cause, every caller.** Before editing a shared function, find all its callers and fix it once in the shared path. Ask *why* five times (W90, W96).
- **Scope the blast radius honestly.** If a bug touched 5,000 bars rather than 25, say so (W60).
- **Warnings are signals.** Don't wave away new warnings, flaky tests or "worked last time" patches (W84).
- **Mark a stopgap as a stopgap.** Add a comment naming its ceiling and the real fix (W89).

## Checklist (WHO-style: sign-in / time-out / sign-out, W93)
- **Sign-in (before editing):** Is the real goal clear? Have I traced the actual flow end to end? Does an existing helper already do this?
- **Time-out (before an irreversible step):** migration, force-push, deleting files, public API change → premortem, then confirm.
- **Sign-out (before saying done):** Ran it? Tests green without weakening them? Diff re-read? Anything I didn't verify, listed?

Source IDs (`S#`, `W#`) resolve in [sources.md](sources.md).

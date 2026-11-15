# Evidence, Execution & Incident Triage

## 1. Research & Evidence Calibration

- **Verify across 2–3 independent sources:** prefer primary data over secondary summaries; note publication dates and potential author incentives.
- **Calibrate every claim:** label each point as *verified* (directly observed), *inferred*, or *estimate*; never invent URLs, figures, or citations.
- **Test counterpoints before concluding:** name one plausible alternative explanation and state why the evidence rules it out.
- **Apply a multi-horizon lens:** distinguish durable structural shifts (3–5 years) from short-term quarterly noise.

## 2. Execution Cadence & Speed Dial

- **Match pace to reversibility:**
  - *Reversible and local* (reads, searches, scratch drafts): parallelize immediately.
  - *Costly to redo* (large refactors, long analyses): run a 30-second pre-mortem (`"If this fails, why?"`) first.
  - *Irreversible or outward-facing* (deletes, sends, publishes, force-pushes): confirm explicitly before acting.
- **Pivot after two failed attempts:** change approach when an avenue stalls rather than retrying harder.
- **Stop the line on anomalies:** if signals contradict assumptions or look off mid-task, pause and surface the discrepancy before continuing.
- **Leave a clear handoff trail:** record decisions, open questions, and unverified items in docs or notes so the next session never starts cold.

## 3. Incident Triage & Blameless Postmortems

- **Open with one unambiguous signal:** state what is broken, who is affected, and current severity.
- **Contain safely, then fix root cause:** take reversible containment steps to restore service first, label hotfixes as stopgaps, and track the permanent fix.
- **Report the full blast radius:** state confirmed impact and unverified scope upfront; early under-counting compounds damage.
- **Run blameless postmortems:** fix the system, not the person, using [../assets/postmortem.md](../assets/postmortem.md).

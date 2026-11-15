---
name: code-review
description: Review a diff, branch, or pull request against the repository code review checklist and engineering standards. Use when reviewing a PR, auditing code changes, or self-reviewing a branch before merge.
---

# Code Review

Review the target diff, branch, or PR against [references/checklist.md](references/checklist.md) and the engineering standards in [../developer-guides/SKILL.md](../developer-guides/SKILL.md).

## Workflow

1. **Flag access blockers first:** note unpushed branches, missing data, or parts you cannot verify.
2. **Verify soundness before style:** check logic, baselines, data contracts, and reproducibility before formatting or nits.
3. **Anchor findings inline:** cite exact files and lines; flag repeated issues once at the first instance.
4. **Label every finding:** `must-fix` (bug, broken test, data-integrity risk), `should-fix` (style, docs, over-engineering), or `nit` (minor polish).
5. **Deliver to chat** unless asked to post directly to a PR.

# data-scientist

Unified agent plugin combining Python/Kedro engineering standards, MBB problem solving and slide creation, and HK sharp execution skills.

## Skills (14)

### Engineering Standards (from `eng-standards`)

| Skill | Purpose |
| :--- | :--- |
| [developer-guides](skills/developer-guides/SKILL.md) | Python/Kedro style, parameters, Pandera schemas, unit tests, logging, parallelism, visualization, writing, and agent defaults |
| [code-reviewer](skills/code-reviewer/SKILL.md) | Review diffs, branches, or PRs against repository engineering standards |
| [code-review-checklist](skills/code-review-checklist/SKILL.md) | Self-review and PR checklist |
| [worktrees](skills/worktrees/SKILL.md) | Git worktree creation, usage, and cleanup |

### MBB Communication & Slides (from `mbb-communication-style`)

| Skill | Purpose |
| :--- | :--- |
| [structured-problem-solving](skills/structured-problem-solving/SKILL.md) | Hypothesis-driven decomposition, MECE `if/then` issue trees, 80/20 drill-down, and top-down synthesis |
| [executive-presentations](skills/executive-presentations/SKILL.md) | Conclusion-titled slides, fractal 3-point structure, 2x2 matrices, and punchy summaries/Q&A |
| [mbb-slide-creation](skills/mbb-slide-creation/SKILL.md) | McKinsey-style storylining, ledes, content delivery, 16:9 geometry, Georgia/Arial typography, and `#051C2C`/`#2251FF` palette |

### HK Sharp Execution (pulled from `kamingfung/hk-agent-skills`)

| Skill | Purpose |
| :--- | :--- |
| [hk-sharp](skills/hk-sharp/SKILL.md) | Speed-versus-verification decisions |
| [hk-coding](skills/hk-coding/SKILL.md) | Sharp engineering: reuse, ship small, verify honestly |
| [hk-research](skills/hk-research/SKILL.md) | Wet-market research: compare sources, verify fresh |
| [hk-comms](skills/hk-comms/SKILL.md) | Fast service, warm enough: direct and face-saving registers |
| [hk-execution](skills/hk-execution/SKILL.md) | Throughput without burnout for long multi-step projects |
| [hk-incident](skills/hk-incident/SKILL.md) | Incident triage, clear warnings, blameless postmortems |
| [hk-deals](skills/hk-deals/SKILL.md) | Trading-house negotiation, stakeholder and partner strategy |

## Installation & Syncing `hk-*` Skills

Symlink into `~/.gemini/config/plugins/data-scientist`:

```bash
ln -sfn /Users/fkm/GitHub/data-scientist ~/.gemini/config/plugins/data-scientist
```

To pull updates for the `hk-*` skills from [`kamingfung/hk-agent-skills`](https://github.com/kamingfung/hk-agent-skills):

```bash
just sync-hk
```

<h1 align="center">data-scientist</h1>

<p align="center">
  <em>Strict data contracts. Hypothesis first. Slides where every number traces to a source.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-0.2.0-111111?style=flat-square" alt="Version 0.2.0">
  <img src="https://img.shields.io/badge/skills-6-111111?style=flat-square" alt="6 skills">
  <img src="https://img.shields.io/badge/spec-agent--plugins%201.0.0-111111?style=flat-square" alt="agent-plugins 1.0.0">
  <img src="https://img.shields.io/badge/license-MIT-111111?style=flat-square" alt="MIT license">
</p>

---

A self-contained agent plugin that puts a disciplined senior data scientist inside your AI agent:

- **Before writing code:** states a hypothesis, builds a custom MECE `if/then` issue tree, and prioritizes the 80/20 lever.
- **When writing code:** enforces pure functions, top-down order, Pandera schema boundaries, strict `params["key"]` access, and actionable logs with entity, time window, and row count.
- **When reviewing code:** checks soundness, baselines, and data contracts before style, anchoring findings inline with a three-round cap.
- **When communicating:** leads with the decision, builds title-only outlines before rendering slides, and ships self-contained `1280x720` HTML data decks where every chart and number comes from real data.

No external MCP servers. No build step. Just markdown skills, reference guides, and deck templates.

## How it works

### Engineering & problem solving

1. **Frame before analyzing:** [`structured-problem-solving`](skills/structured-problem-solving/SKILL.md) sets an initial hypothesis within five minutes, segments totals, writes word-first formulas, and runs pre-mortems before irreversible steps.
2. **Fail loud at the boundary:** [`developer-guides`](skills/developer-guides/SKILL.md) splits engineering standards into focused references covering Python/Kedro pipelines, strict parameter slicing, Pandera validation, unit tests, logging, parallelism, and colorblind-safe visualization.
3. **Review soundness first:** [`code-review`](skills/code-review/SKILL.md) flags access blockers first, verifies logic and data contracts before style, and labels every finding with paired icon + text (`❌ must-fix`, `⚠️ should-fix`, `🤔 nice-to-have`).
4. **Isolate branch work:** [`worktrees`](skills/worktrees/SKILL.md) standardizes creating, using, and cleaning up git worktrees.

### Decks & executive communication

1. **Outline before slides:** [`html-data-deck`](skills/html-data-deck/SKILL.md) requires an approved title-only outline before rendering HTML. It ships a [`template/`](skills/html-data-deck/template/) (`deck.py`, `charts.py`, `deck.css`, `deck.js`, `interact.js`) for fixed `1280x720` slides with inline SVG charts, KPI tiles, source footnotes, and a three-pass review (story, numbers, design).
2. **Headline first:** [`consulting-communication`](skills/consulting-communication/SKILL.md) structures executive summaries, status updates, Q&A delivery, 16:9 slide storylining, and negotiation prep so a decision-maker gets the takeaway in under 30 seconds.

## Skills

| Skill | What it does | Key resources |
| :--- | :--- | :--- |
| [`developer-guides`](skills/developer-guides/SKILL.md) | Python/Kedro code style, parameters, Pandera schemas, unit tests, logging, parallelism, visualization, technical writing, and agent defaults | [13 guides](skills/developer-guides/references/README.md) |
| [`code-review`](skills/code-review/SKILL.md) | PR and branch review workflow: access blockers first, soundness before style, inline findings, and a three-round cap | [`checklist.md`](skills/code-review/references/checklist.md) |
| [`worktrees`](skills/worktrees/SKILL.md) | Git worktree creation, usage, and cleanup | — |
| [`structured-problem-solving`](skills/structured-problem-solving/SKILL.md) | Hypothesis-driven decomposition, MECE `if/then` issue trees, 80/20 drill-down, pre-mortems, evidence calibration, incident triage, and top-down synthesis | [`frameworks.md`](skills/structured-problem-solving/references/frameworks.md), [`research-and-execution.md`](skills/structured-problem-solving/references/research-and-execution.md), [`postmortem.md`](skills/structured-problem-solving/assets/postmortem.md) |
| [`html-data-deck`](skills/html-data-deck/SKILL.md) | Self-contained `1280x720` HTML data decks: title-only outline, action titles, inline SVG charts, sources for every number, and a three-pass review | [`template/`](skills/html-data-deck/template/) |
| [`consulting-communication`](skills/consulting-communication/SKILL.md) | Executive summaries, status updates, negotiation prep, Q&A delivery, consulting slide storylining, and 16:9 visual design specs | [`summaries-and-qa.md`](skills/consulting-communication/references/summaries-and-qa.md), [`slide-design-spec.md`](skills/consulting-communication/references/slide-design-spec.md), [`negotiation.md`](skills/consulting-communication/references/negotiation.md) |

## Install

### Antigravity (plugin)

Clone the repository and symlink it into `~/.gemini/config/plugins/data-scientist`:

```bash
git clone https://github.com/kamingfung/data-scientist.git ~/repos/data-scientist
mkdir -p ~/.gemini/config/plugins
ln -sfn ~/repos/data-scientist ~/.gemini/config/plugins/data-scientist
```

The repository follows the [`agent-plugins`](plugin.json) 1.0.0 schema, so Antigravity loads [`plugin.json`](plugin.json) and all six `skills/*/SKILL.md` folders as a single plugin.


### Claude Code, Codex, Gemini CLI, Grok, and other agents (`npx skills`)

Each folder under `skills/` follows the Agent Skills (`SKILL.md`) format. Install all six skills into Claude Code, Codex, Gemini CLI, Grok, Antigravity, Cursor, or OpenCode using the [skills CLI](https://skills.sh):

```bash
npx skills add kamingfung/data-scientist --skill '*' --global
```

Target a specific agent with `--agent` (`claude-code`, `codex`, `gemini-cli`, `antigravity`, etc.), or omit `--global` to install into the current project only.

### Manual skill symlink (from a local clone)

If you prefer symlinking from `~/repos/data-scientist` so `git pull` updates everything in place, link `skills/*` into your agent's global or project skills folder:

| Agent | Global skills directory | Project skills directory |
| :--- | :--- | :--- |
| **Antigravity** | `~/.gemini/antigravity/skills/` | `.agents/skills/` |
| **Claude Code** | `~/.claude/skills/` | `.claude/skills/` |
| **Codex** | `~/.codex/skills/` | `.agents/skills/` |
| **Gemini CLI** | `~/.gemini/skills/` | `.gemini/skills/` |
| **Grok** | `~/.grok/skills/` | `.grok/skills/` |

```bash
# Example: link all six skills globally for Codex
mkdir -p ~/.codex/skills
for s in ~/repos/data-scientist/skills/*; do
  ln -sfn "$s" ~/.codex/skills/"$(basename "$s")"
done
```

### Update

```bash
git -C ~/repos/data-scientist pull
```

Symlinked installs pick up updates immediately. For `npx skills` installs, re-run `npx skills update`.

### Uninstall

```bash
# Antigravity plugin
rm ~/.gemini/config/plugins/data-scientist

# Or via skills CLI
npx skills remove developer-guides code-review worktrees structured-problem-solving html-data-deck consulting-communication --global
```

## License

MIT — see [`plugin.json`](plugin.json).

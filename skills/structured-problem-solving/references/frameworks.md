# Problem-Solving Frameworks & Math Templates

Customize these lenses to the problem; drop irrelevant branches and add domain-specific ones.

## 1. Core Diagnostic Lenses

| Problem type | Primary lens | Key diagnostic questions |
| :--- | :--- | :--- |
| **Profit / unit economics drop** | `E(P = R − C)M` | Did revenue (`Price × Volume`) fall or did costs (`Fixed + Variable`) rise? Is the shift company-specific or market-wide (`E` / `M`)? |
| **Market entry / new product** | 4-part viability | Who is the customer and unmet need? What is market size and share capture? How do unit economics and breakeven work? What barriers or execution risks exist? |
| **Pricing decision** | 3-pillar pricing | Cost floor (variable + allocated fixed), competitive benchmark (substitutes and switching cost), and customer willingness to pay (value delivered). |
| **M&A / build-vs-buy** | Standalone + synergy | Standalone value, revenue and cost synergies, integration complexity, and cultural/technical fit. |
| **Capacity / operations bottleneck** | End-to-end flow | Where does throughput cap out? Is the constraint supply, process step, utilization, or demand mix? |

## 2. Issue Tree Rules

- **MECE test:** confirm no item fits two branches (mutually exclusive) and no plausible cause sits outside all branches (collectively exhaustive).
- **Conclusive framing:** write every leaf node as a falsifiable `if/then` statement so one data cut either proves or eliminates it.
- **Prune early:** once data disproves a branch, state the finding in one sentence and drop that branch immediately.

## 3. Word-First Math & Sanity Checks

1. State the formula in words first (`Incremental Revenue = Target Users × Conversion Rate × Net Price`).
2. State every assumption explicitly and mark whether it is observed data or an estimate.
3. Round to clean numbers during mental estimation, then check whether the rounded result passes a real-world plausibility bound (e.g., per-capita spend, total addressable market share `≤100%`).

## 4. Top-Down Synthesis Template

```markdown
**Recommendation:** [Yes / No / Option X — 1 sentence with quantified target impact.]

**Supporting evidence (max 3):**
1. [Biggest quantified driver]
2. [Second driver]
3. [Third driver]

**Key risks & mitigations:**
- [Risk 1] → [Mitigation / monitor]

**Next steps:**
1. [Immediate action + owner]
2. [Follow-up validation + timeline]
```

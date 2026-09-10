# graph.json — schema

The single source of truth for the site. Everything renders from this file; the
report and notes are prose *about* it. Designed so incoming research slots in as
new nodes/edges without reshaping anything, and so the due-diligence pass is
mechanical (filter by `verification` and `confidence`).

## Top level
```
{
  "metadata": { schema_version, generated, legends, methodology },
  "nodes": [ ... ],
  "edges": [ ... ]
}
```

## Node
| field | required | values / notes |
|---|---|---|
| `id` | yes | stable slug, snake_case. Never reused. |
| `label` | yes | display name |
| `layer` | yes | `russian_state` · `intermediary` · `us_media` · `us_political` · `content` · `platform` — visual grouping / column |
| `type` | yes | finer role: `government`,`state_media`,`intelligence`,`operation`,`person_state`,`shell`,`person_intermediary`,`network`,`outlet`,`producer`,`influencer`,`content`,`platform`,`audience` |
| `us_class` | US actors only | 🔴`direct_state_connected` · 🟠`bridge_amplifier` · 🟡`downstream` · `null` — the colour that matters for American nodes |
| `aliases` | no | array |
| `notes` | no | one-liner |
| `sources` | no | array of citation objects (node-level) |

## Edge
| field | required | values / notes |
|---|---|---|
| `id` | yes | slug |
| `source` / `target` | yes | node ids; edge is directed source→target |
| `evidence_class` | yes | **the methodological category** — `documented_contact` · `documented_material_exchange` · `documented_state_connection` |
| `mechanism` | yes | what kind: `funding`,`editorial_direction`,`production`,`amplification`,`introduction`,`communication`,`business_relationship`,`hosted_appearance`,`content_creation`,`distribution`,`ownership`,`laundering` |
| `confidence` | yes | `very_high` · `high` · `medium` · `low` · **`do_not_claim`** |
| `claim` | yes | one sentence: exactly what this edge asserts, no more |
| `quote` | no | short supporting quote/paraphrase from the source |
| `citation` | yes* | `{ publisher, title, date, url, primary:bool }` — *except `do_not_claim` edges, which cite the absence |
| `verification` | yes | `pending` · `verified` · `needs_primary` — starts `pending`; the due-diligence pass sets it. **`verified` = a primary government document (Mueller / SSCI / ICA / indictment) is cited and the analyst has confirmed it supports the specific claim.** `needs_primary` = currently resting on journalism where a primary doc exists but hasn't been pulled. |
| `disputed` | no | `true` when a source is contested/recanted (e.g. a witness who later changed their account). Pair with `dispute_note`. **A disputed edge is preserved, never laundered into a fact and never silently dropped** — the site renders it with a "contested" marker. Keep `verification: pending` and `confidence: medium` (or lower) while disputed. |
| `dispute_note` | if disputed | one line: what is contested and by whom |

**Grading shorthand** (analyst's language → fields): "A-grade primary-document
edge" → `verification: verified` + `citation.primary: true`. "B-level / contested"
→ `disputed: true`, `confidence: medium`, `verification: pending`.

**Frontier roster nodes:** nodes added ahead of their edges (a named next-target,
e.g. `guccifer_2`, `dcleaks`, `prevezon`) carry `FRONTIER` in `notes` and show as
edgeless in the validator until incoming research connects them.

## Network-analysis fields (FRAMEWORK.md; consumed by `analysis.py`)
| field | on | notes |
|---|---|---|
| `date` | edge | when the *relationship/event* occurred (`YYYY` or `YYYY-MM-DD`). Distinct from `citation.date` (when it was reported). Enables temporal-causality checks. |
| `start` / `end` | edge | optional bounds for relationships with duration |
| `evidence_quality` | edge | `A` primary record · `B` independent corroboration · `C` credible secondary · `D` allegation/speculation. Weights support independently of `confidence`. |
| `citations` | edge | array form of `citation` (back-compatible: single `citation` still valid). Each entry may carry `independence_group` / `information_origin` so N documents collapse to M independent origins. |
| node `type` `audience`/`platform` | node | treated as **sink/hub** — barred as *intermediate* vertices in criticality pathfinding ("both reach the public" is not a path). |
| `domain` | edge | `influence` (default) · `domestic`. A `domestic` edge is a US-ecosystem context tie (creator↔creator appearance, creator↔org membership, intra-American amplification). It is EXCLUDED from foreign-influence reach / criticality / bridge-centrality pathfinding (American ties are not Russian conduits) and instead powers the AMERICAN ECOSYSTEM DENSITY readout. |
| `provenance` | edge | `observed` (default) · `conditional` · `contested`. **`conditional` = a consequence derived by ASSUMING a contested edge true.** It is barred from `G_obs`, may never be `verification: verified`, and MUST carry `assumed_under`. This is the contamination firewall. |
| `assumed_under` | conditional edges | array of the hypothesis edge id(s) this result depends on. A conditional edge with no `assumed_under` is invalid. |

**The ASSUMING_TRUE firewall (non-negotiable).** A conditional consequence — "what
would follow IF contested edge E were true" — is NEVER an observation. It carries
`provenance: conditional` + `assumed_under: [E,…]` in the data, is stamped
`ASSUMING_TRUE(E)` in every rendered/printed result, is excluded from `G_obs` by
`analysis.py`, and is rejected as `verified` by `validate.py`. A conditional edge
becomes interesting only via **predictive convergence**: an *independent* `observed`
edge (different `information_origin`) is later found for the same pair — and even
then the conditional and observed edges stay distinct objects. On the website,
conditional edges render only inside an explicit "ASSUMING_TRUE(E)" hypothesis view,
never on the default observed graph.

`analysis.py` computes: `G_obs` / `G_contested` / `G_conditional(E)`; **edge
criticality** (are a contested edge's endpoints already connected in `G_obs`, by how
many vertex-independent routes, and Δcomponents if assumed true); source-independence
collapse; temporal causality. It never asserts an edge is true — only how much the
topology depends on it.

## The load-bearing rule
`confidence: "do_not_claim"` edges are **kept, not deleted.** They are the negative
findings that keep the graph honest (e.g. `dtj → russian_state directly`). The site
renders them explicitly (dashed, greyed, labelled "not established") rather than
hiding them. Never upgrade one without a primary citation that establishes it.

## Confidence → colour (suggested)
very_high = solid strong · high = solid · medium = thinner · low = dashed thin ·
do_not_claim = dashed grey with a strike/"✗ not established" badge.

## US class → node colour
🔴 direct_state_connected · 🟠 bridge_amplifier · 🟡 downstream · Russian-layer nodes
get the "state" palette; intermediaries a neutral bridge palette.

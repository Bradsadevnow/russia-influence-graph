# Analytical framework — three superimposed graphs

The upgrade from "typed, confidence-rated edges" (an epistemic labeling model) to a
**network-analysis framework**. The graph now holds not just *what is claimable* but
*what would follow if a contested proposition were true, and how much of the observed
structure actually depends on it.*

From **"don't overclaim"** → **"don't overclaim, don't delete, don't contaminate,
don't stop investigating."**

## The three graphs

### 1. `G_obs` — the observed graph
Only documented relationships/events. Edges that are **not** `do_not_claim` and
**not** `disputed`. Every edge carries provenance, date, source, relationship type.
This is the claimable network.
*(Stricter variant `G_obs_verified` = only `verification == verified`.)*

### 2. `G_contested` — the contested graph
Candidate relationships that exist as **evidentiary objects** but aren't claimable:
`do_not_claim` edges and `disputed` edges. Each carries supporting evidence,
counter-evidence, denial, provenance, epistemic status. **Nothing disappears.**

### 3. `G_conditional(H)` — the conditional graph
A hypothesis branch: assume a contested edge `E` is true, add it to `G_obs`,
propagate consequences. **Every downstream result carries the assumption that
generated it.** `ASSUMING_TRUE(E)` is a label on the whole derived topology.

## The core question changes

Not "how connected is this network?" but: **how does the topology change under
different epistemic states?** Compare `G_obs`, `G_obs + E`, `G_conditional(H)` on:
connected components · shortest paths · bridge/betweenness · community membership ·
path redundancy · cluster density · temporal ordering · source independence ·
evidentiary quality · assumption sensitivity.

## Edge criticality (the killer test)
For a contested edge `E`: *what changes when E is removed / added?*
- `5 clusters → 1 cluster` when E is assumed → E does enormous connective work.
- `5 clusters → 4.8 effective` because seven independent paths remain → E barely matters.

**Neither result says whether E is true.** It says **how much the hypothesis matters
to the topology.** The report can then say, precisely:

> *E is not claimable. Under `ASSUMING_TRUE`, E reduces connected components from 6 to
> 2 and creates three new paths between clusters A and D. Without E, those clusters
> remain connected through two independently documented routes.*

That is vastly more informative than "E proves the conspiracy" (it doesn't) — it says
exactly what E would do if true, and how much of the structure already stands without it.

## Source independence — first-class
Five citations can be **one underlying source propagated five times.** So evidence
carries not just `source_id` but `information_origin` / `independence_group`. Metric
shifts from *count of supporting edges* to **independent evidentiary support**:

> 7 documents · 4 publications · 3 witnesses · 2 gov records → **collapses to 3
> independent information origins.**

Prevents citation multiplication from manufacturing evidentiary density. Weight by
**evidence quality**: A = primary record · B = independent corroboration · C =
credible secondary reporting · D = allegation/speculation. A graph does not get
stronger because someone wrote the same thing 400 times.

## Temporal topology — first-class
Edges are temporally bounded (`edge.start`, `edge.end`, `event.date`,
`source.date`). Enforce **temporal causality**: a 2020 relationship cannot explain a
2016 event. "Relationship formed 2013 → 2016 event" is a different analytical
situation from "2016 event → 2018 relationship alleged."

## Retrodictive vs predictive support
- **Retrodictive:** "we found evidence compatible with H."
- **Predictive:** "if H were true, it predicts relationships X,Y,Z should exist — and
  independently observed evidence *elsewhere* shows them." Stronger — **provided we
  don't select the prediction after seeing the result.**

Applied here: for `Trump Jr. ──[DO_NOT_CLAIM]──► X`, run `ASSUMING_TRUE(X)`, read off
the relationships X predicts, then ask whether those are **independently observable
in `G_obs`.** If yes: not proof of X, but **predictive convergence.**

## What the graph now contains
1. what happened (`G_obs`)
2. what is disputed (`G_contested`)
3. what would follow if the disputed proposition were true (`G_conditional`)
4. how much of the observed topology depends on it (edge criticality)
5. how independently supported the resulting structure is (independence + quality)

## Implementation
`graph/analysis.py` computes all of the above from `graph/graph.json` — no external
deps. `graph/validate.py` stays the structural gate. New edge fields
(`date`, `evidence_quality`, multi-`citations[]` with `independence_group`) are
documented in `SCHEMA.md` and back-compatible with single-`citation` edges.

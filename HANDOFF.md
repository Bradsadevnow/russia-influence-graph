# HANDOFF — Russia → U.S. media/political influence graph

**What this is:** an evidence graph of documented connections between Russian state
actors and U.S. media/political figures, grounded in primary public records (DOJ /
Mueller, SSCI Vols 3 & 5, ICA 2017-01, DOJ SDNY, Senate Judiciary). Destined for a
**public website** after due diligence. The whole point is a navigable topology
where every edge is typed, confidence-rated, and clickable to its source — the
opposite of a red-string wall.

**Ground truth of the project is `graph/graph.json`.** The report and notes are
prose *about* it. Read `README.md` (methodology) and `graph/SCHEMA.md` (field
contract) first. Run `python3 graph/validate.py` for the live state + the
"iffy surface" (the due-diligence worklist).

## Current state (2026-09-09, after batch 03)
- **54 nodes, 78 edges.** 37 verified · 22 needs_primary · 19 pending.
- confidence: 38 very_high · 35 high · 1 medium · 1 low · **3 do_not_claim**.
- **1 disputed edge** preserved (`e_beniaminov_purpose`).

## The thesis (do not overstate it)
NOT "the right wing is Russian-controlled." The real question: **how many
INDEPENDENT Russian influence architectures entered the U.S. ecosystem, and where
do their networks overlap?** Three so far, and they are **parallel, not centrally
directed** — they intersect only through shared *bridge* nodes:
- **Architecture A — political/lobbying:** Agalarov/Katsyv → Goldstone/Kaveladze →
  Trump Jr./campaign; and Prevezon → Veselnitskaya/Akhmetshin → HRAGI → Congress
  (Rohrabacher) + anti-Magnitsky film → public.
- **Architecture B — cyber/intelligence:** GRU → Guccifer 2.0 / DCLeaks →
  WikiLeaks → (Stone) → campaign / media / voters.
- **Architecture C — modern media:** RT → Tenet (covert $ → influencers) and
  RT → Swann → Truth in Media → "Zelenskyy Unmasked" → Trump Jr. → audience;
  plus Doppelganger fake sites.

**Bridge nodes** (the load-bearing category): Goldstone (business/social/political),
Veselnitskaya (legal/lobbying/state), Akhmetshin (lobbying/intel/political),
RT (state-media/US-media), WikiLeaks (intel/distribution), Tenet (Russian-$/US-influencer).

## Load-bearing NEGATIVE findings (never drop or upgrade without a primary doc)
- `e_dtj_state_direct` — Trump Jr. → Russian state **direct**: NOT established (Mueller: no criminal conspiracy).
- `e_dtj_knowing` — Trump Jr. knowingly in a Russian op: NOT established (contacts ≠ knowledge/intent).
- `e_fusion_meeting_DNC` — **Fusion GPS → Trump Tower meeting: NOT established.** Simpson testified he didn't know of the meeting beforehand; Veselnitskaya denied telling him. Fusion (via Prevezon/BakerHostetler) and the Agalarov/Goldstone meeting branch intersect ONLY through Veselnitskaya — not proof of coordination. Fusion is a US oppo-research firm, **not typed as part of a Russian operation.** This edge is the anti-conspiracy-spaghetti guardrail; keep it visible.
- `e_goldstone_putin` (low, not do_not_claim) — Goldstone floated a Putin meeting: **attempted, not completed.**
- Rohrabacher = **influence recipient, not controlled asset.** Same for the unwitting Tenet commentators.

## How to add incoming research (the loop)
1. Brad pastes a research batch (ideally tagging each item *new node* vs *new edge*, and *which primary document*).
2. Encode via a `/tmp/apply_*.py` upsert script (load graph.json → `un()`/`ue()` helpers → dump indent=2). Pattern is in git history / prior scripts.
3. **Grade honestly:** primary gov doc + analyst-confirmed → `verification: verified`. Resting on journalism → `needs_primary`. Contested/recanted → `disputed:true`, `confidence: medium`, `pending`. Unsupported inference → `confidence: do_not_claim` (kept as a rendered boundary).
4. `python3 graph/validate.py` — must end "OK — structurally valid". Update `graph/CHANGELOG.md`.

## THE prize (next target)
**Convergence test.** Do Architectures A/B/C share any *non-Trump* American node —
a PR firm, a shell, an outlet, an influencer, a distribution channel? Specifically:
compare the American-side nodes of the **2016** operation (A+B) against the **2024**
operation (C: Tenet/RT/Swann/Doppelganger/influencers). If the same intermediaries,
outlets, personalities, or infrastructure recur across both generations, THAT is the
finding that turns "parallel architectures" into "ecosystem." The graph will show it
as a node with in-edges of two different pathway colors. Until then, do not draw the
convergence line.

Frontier roster nodes awaiting edges: (see validate.py output) — e.g. structura,
ano_dialog, agalarov_network, afanasyeva.

## Citation hygiene (non-negotiable for a public site naming living people)
Every URL gets opened and read before publish. One known bad link already caught
(a CSF vet-clinic URL stapled onto the Trump Jr./Swann edge by an upstream research
tool) — see `sources/citation-audit.md`. Only a fully-`verified` subgraph goes public.

## Website (not started)
Point-one substrate is done (graph.json + schema + validator). Renderer decisions
(force-directed vs layered-by-architecture; edge color = confidence; dashed/greyed
do_not_claim with "not established" badges; click-through to citations) are open.
Audience = general public, post-due-diligence. Threat model = "you're smearing
people," so the defense is structural: every edge cited, every boundary drawn.

## Update — batch 04 (2026-09-10): analytical framework is live
`FRAMEWORK.md` + `graph/analysis.py` upgrade the project from claim-labeling to
network analysis: three superimposed graphs (G_obs / G_contested / G_conditional),
**edge criticality**, source-independence collapse, temporal causality. Run
`python3 graph/analysis.py`. Key result to build the report language on: contested
edges are now reported as *"not claimable; here is exactly what it would/wouldn't do
to the topology, and how many independent documented routes already stand without
it."* E.g. Trump Jr.→Kremlin(direct) is un-claimable AND redundant (5 independent
routes); Trump Jr.→knowing-participation is un-claimable AND would create connectivity
that doesn't otherwise exist (0 routes) — opposite structural meanings, same
"do_not_claim" label. **Backfill queue:** edge `date`, `evidence_quality` (A/B/C/D),
citation `independence_group`.

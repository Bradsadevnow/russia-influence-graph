# Russia → U.S. media/political influence — relationship graph

Investigative project. The object of study is a **relationship graph**: who is
demonstrably connected to Russian state actors, **by what mechanism**, and **how
far the material travels** — not a list of "Americans who say pro-Russia things."

Everything here is grounded in public-record primary sources: DOJ indictments and
press releases, the Senate Select Committee on Intelligence Vol. 5, the Mueller
Report, and major investigative journalism (AP, NPR, Reuters, WaPo, DFRLab).

## The methodological spine (non-negotiable)

**A connection is not a conclusion.** The entire value of this project is that it
refuses to collapse distinct evidentiary categories. Three edge classes:

1. **Documented contact** — X ↔ a Russian national / Russian-linked intermediary.
2. **Documented material exchange** — money, business opportunity, political
   information, communications, introductions.
3. **Documented Russian-state connection** — an actual Russian government /
   intelligence / state-media / Kremlin-controlled entity.

Three **node classes** for American actors:

- 🔴 **Direct state-connected** (funding/direction/production) — e.g. Tenet, Swann/Rebel Media.
- 🟠 **Bridge / amplifier** (distribution/amplification, often no documented coordination) — e.g. influencers who promoted Russian-derived material.
- 🟡 **Downstream ecosystem** (content propagation; no demonstrated Russian relationship).

Every edge carries a **confidence tier** (Very high / High / Medium) and, where the
evidence does not support an inference, an explicit **"Do not claim"** marker.
"Do not claim" edges are recorded as *absences* on purpose — they are load-bearing.

The interesting question is not "who is secretly Russian?" It is **"what is the
transmission topology, and how many INDEPENDENT paths terminate in the same Russian
state/Kremlin-linked network?"** Convergent independent paths are the finding;
a single circumstantial chain is not.

## Files

- `notes/01-media-node-source-pass.md` — Tenet, Swann, the three node classes,
  propagation depth.
- `notes/02-trump-jr-branch.md` — the Trump Jr. forensic pass: Agalarov, Trump
  Tower meeting, WikiLeaks/GRU, Goldstone→VK bridge, the Swann loop; edge table
  with confidence and the two "Do not claim" edges.
- `report/report-v1.md` — formal writeup (Tenet, Doppelganger, Swann, IRA/Lakhta)
  with tables, mermaid network + timeline, mechanisms, gaps/next steps, sources.
- `sources/citation-audit.md` — **read this before anything ships.** Every edge's
  citation must be verified against its real source; one known bad link logged.
- `graph/` — reserved for the structured node/edge dataset that will drive the
  website (not yet built — see "The website" below).

## The website

The deliverable is a site that renders this as a navigable **evidence graph**:
nodes coloured by class, edges coloured/weighted by confidence, each edge clickable
to its primary source, and the "Do not claim" boundaries drawn explicitly rather
than hidden. The point is a tool that makes the *topology* legible and every claim
traceable — the opposite of a conspiracy wall of red string.

**Not yet designed or built.** The current state is: source material saved,
methodology fixed. Next conversation decides the data model (`graph/graph.json`
schema: node = {id, label, class, notes}; edge = {source, target, type,
confidence, citation, quote}) and the presentation.

## Standing rules for this project

1. Primary sources only for edges; journalism is fine but cite the primary
   document where one exists (DOJ, SSCI, court filings).
2. No edge without a citation. No inference beyond what the cited source states.
3. Distinguish **the outlet/producer** (may be state-connected) from **the
   downstream personality** (may be an unwitting amplifier). Never merge them.
4. Preserve the "Do not claim" edges as first-class data.
5. Re-verify every citation before publishing (see citation-audit.md).

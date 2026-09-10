# graph.json changelog

## batch 02 — 2026-09-09 — Goldstone bridge layer
Source: research pass on the intermediary/bridge layer, Mueller Report + SSCI Vol 5
+ ICA 2017-01 primary citations (see `notes/`).

**Thesis advanced:** not one Trump Jr.→Russia connection but **three independently
documented Russian-linked pathways** touching overlapping American networks, with a
**recurring intermediary — Rob Goldstone** — sitting across the Trump Tower meeting,
the VK overture, and the Agalarov/Crocus network:
1. Agalarov → (Kaveladze / Goldstone) → Trump Jr. / campaign
2. GRU → WikiLeaks → Stone → Trump campaign
3. RT → Swann → U.S. media → Trump Jr. / audience

The forensic question going forward: do the independent pathways **converge** on the
same intermediaries / firms / money flows / downstream media — or only coincidentally
touch Trump? Convergence is the finding; coincidence is not.

**New nodes (7):** crocus_group, beniaminov, stone; frontier roster:
guccifer_2, dcleaks, prevezon. (kaveladze/sidorkov updated.)

**Edges flipped to `verified` (primary docs):** Goldstone→Trump Jr. (June 3),
Aras→Kaveladze (June 6 instruction + Magnitsky material/business card),
Kaveladze→Crocus, Aras→Crocus, Kaveladze→meeting, Kaveladze→Beniaminov,
Goldstone→meeting (June 7 "Russian government attorney"), Trump Jr.→meeting
(Manafort/Kushner), meeting→Veselnitskaya, Veselnitskaya→Kremlin (prior Russian-gov
work), meeting→Kremlin (Mueller "expecting derogatory info… from the Russian
government"), GRU→WikiLeaks (ICA high confidence), WikiLeaks→Russian intel (SSCI),
Stone→WikiLeaks (SSCI intermediary), Stone→campaign (SSCI).

**Disputed edge preserved:** Beniaminov→meeting purpose (said it was to convey
negative Clinton info; later recanted) — `disputed:true`, medium, pending.

**VK branch (needs_primary, on WaPo/emails):** Goldstone→Trump Jr. (VK presence),
Trump Jr.→Scavino, Goldstone→Sidorkov (June, "Vote Trump 2016" sample page),
Sidorkov→campaign.

**Explicit non-overstatement (kept as guardrails, not edges):** VK offering
promotion is a documented relationship, NOT "Kremlin→VK→Goldstone→Trump covert
operation." Goldstone was a publicist; Sidorkov near-Putin photos ≠ every VK
employee a Kremlin agent. The two `do_not_claim` edges (Trump Jr.→state direct;
Trump Jr.→knowing participation) remain.

**Frontier / next targets:** Goldstone → Agalarov → Kaveladze → Veselnitskaya →
Beniaminov → Prevezon/anti-Magnitsky; Goldstone → VK → Sidorkov → Russian
social-media ecosystem; Stone → WikiLeaks → GRU → Guccifer 2.0 / DCLeaks → US media.
Then test convergence against the Tenet / RT / Swann / Doppelganger network.

## batch 01 — 2026-09-09 — seed
Populated from source passes 1–2 and report v1 (Tenet, Doppelganger, Swann/Rebel
Media, IRA/Lakhta, initial Trump Jr. edges). All edges verification=pending.

## batch 03 — 2026-09-09 — second-order network + Fusion GPS correction
Followed the bridges outward. **New nodes:** katsyv, prevezon(edged), bakerhostetler,
fusion_gps, glenn_simpson, hragi, rohrabacher, anti_magnitsky_film, us_congress,
rhona_graff; guccifer_2/dcleaks/akhmetshin edged.
**Architecture A extended (lobbying):** Prevezon→BakerHostetler→Fusion GPS→Simpson→
Veselnitskaya; Veselnitskaya→Prevezon/Katsyv + DOJ obstruction (secret work w/ senior
Russian prosecutor) + SSCI intel ties; Akhmetshin→HRAGI→Congress + →Rohrabacher +
anti-Magnitsky film→public. **Architecture B concretized (cyber):** GRU→Guccifer 2.0/
DCLeaks→WikiLeaks (June 29 2016 encrypted file), Guccifer→Stone→campaign (w/ SSCI
caveat: couldn't determine how much non-public info Stone had).
**KEY NEGATIVE FINDING (do_not_claim):** Fusion GPS→Trump Tower meeting NOT
established — Simpson didn't know beforehand; branches intersect only via
Veselnitskaya. Fusion typed as US oppo-research, NOT a Russian operation.
**Also:** Goldstone→Putin-meeting = low/attempted-not-completed; Rohrabacher =
influence recipient not asset. 37 edges now verified. Next: convergence test 2016 vs 2024.

## batch 04 — 2026-09-10 — network-analysis framework (three superimposed graphs)
Not a research batch — an architecture upgrade (Brad's design). Added `FRAMEWORK.md`
(G_obs / G_contested / G_conditional(H); edge criticality; source independence;
temporal topology; retrodictive vs predictive) and `graph/analysis.py` (stdlib) which
computes it on live data. SCHEMA extended: edge `date`/`start`/`end`,
`evidence_quality` (A/B/C/D), array `citations[]` with `independence_group`;
audience/platform nodes = sinks, barred as criticality intermediates.

**First run findings (74 obs edges, 1 component; 4 contested):**
- `e_dtj_state_direct` (Trump Jr.→Kremlin, do_not_claim): **5 independent documented
  routes already connect them** (Goldstone→Kremlin, meeting→Kremlin, Agalarov→Kremlin,
  …). The un-claimable direct edge is also structurally REDUNDANT — assuming it changes
  nothing. Strong honest statement.
- `e_dtj_knowing` (Trump Jr.→Project Lakhta, do_not_claim): **CRITICAL — 0 routes.**
  Once the shared-audience sink is excluded, there is NO documented path making Trump
  Jr. part of the troll-farm op. Assuming it would *create* connectivity that doesn't
  exist. A real gap, correctly shown.
- `e_fusion_meeting_DNC` (Fusion→Trump Tower meeting, do_not_claim): 2 independent
  routes, BOTH through the Prevezon/anti-Magnitsky cluster (Veselnitskaya; and
  BakerHostetler→Prevezon→Katsyv→HRAGI→Akhmetshin). **Enriches the earlier "only
  through Veselnitskaya" note: the intersection is the whole lobbying substrate, not one
  node** — still do_not_claim, still not a Russian op, but the shared ground is broader.
- `e_beniaminov_purpose` (disputed): 1 route, single cut point = Kaveladze.

Backfill pending (due-diligence): per-edge `date`, `evidence_quality`, and
`independence_group` on citations (currently 1 citation/edge → independence collapse
is a no-op until multi-source edges are added).

## batch 05 — 2026-09-10 — GRU information-distribution architecture
The cyber branch becomes a distribution network, not just a hack. New nodes:
smoking_gun, the_hill, congressional_candidate, breitbart, corsi, wnd, bannon.
GRU→Guccifer 2.0 seeded stolen material DIRECTLY to American recipients: The Smoking
Gun (Jun 27), The Hill (congressional-race oppo), a U.S. congressional candidate
(Aug 15). Stone→Breitbart (Aug 5 article crediting Guccifer, not Russia; then
Guccifer↔Stone DMs Aug 14–Sep); Stone→Corsi→WND + Corsi→WikiLeaks (Jul 25 email to
reach Assange); Stone→Bannon→campaign (press strategy around anticipated releases,
per Gates). Recipients typed downstream/UNWITTING — DOJ: not alleged to know the
source was Russian intelligence. Added `analysis.py` RUSSIAN-ORIGIN REACH metric
(vertex-independent GRU→target routes).
NEW do_not_claim: `e_stone_gru_knowledge` (Stone knew Guccifer was the GRU). Criticality:
Stone already connected to GRU by 2 independent routes (Guccifer AND WikiLeaks) — so
ASSUMING_TRUE raises Stone's *consequence*, not the *topology*, and never the knowledge
claim. 61 nodes / 93 edges; normalized to schema 1.0; validator clean.
Reach snapshot: GRU→campaign 2 independent routes; GRU→Stone 2; GRU→Breitbart 1 (chokepoint = Guccifer/Stone).

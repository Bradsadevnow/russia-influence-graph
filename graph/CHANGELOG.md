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

## batch 06 — 2026-09-10 — Cooper/Potomac bridge + lobbying cluster + guardrails
STANDOUT: Chris Cooper / Potomac Square Group — a recurring American PR professional
who organized the 2016 anti-Magnitsky film screening (HRAGIF-compensated; FBI email
chain) and later did paid media consulting for the Gabbard campaign (2017, ~$19,400,
FEC). New nodes: cooper, potomac, gabbard_campaign, arakelian, cymrot, schweitzer,
dellums. Lobbying cluster densified: Cymrot/BakerHostetler briefed Congress; Dellums
+ Akhmetshin lobbied congressional offices; Rohrabacher entered film material into the
congressional record (ProPublica). Hermitage/Browder FARA complaint participants
(Schweitzer, Cymrot-as-campaign) typed LOW/allegation (evidence_quality D) — not
adjudicated.
THREE new do_not_claim guardrails, all demonstrated by criticality:
- Fusion→anti-Magnitsky lobbying: NOT established (litigation support; WaPo). 2 routes
  already exist → assuming changes nothing.
- Russia→Gabbard: NOT established. Criticality = ONE route, single chokepoint chain
  ending at Potomac Square Group — i.e. the ONLY structural link is the shared PR
  contractor (Cooper). Personnel continuity, NOT influence transmission. ASSUMING_TRUE
  creates no new reachability.
- 2016→2024 cast migration (Potomac→Tenet): NOT established — no evidence the 2016
  intermediaries entered the 2024 Tenet/RT architecture.
HYPOTHESIS (not a finding): the persistent object is the ARCHITECTURE (Russian-linked
client → American intermediary → lobbying + media/PR → Congress/audience), which
recurs 2016→2024 with a DIFFERENT American cast (DOJ 2024 describes the same shape).
68 nodes / 109 edges; 58 verified; schema 1.0; validator clean.

## batch 07 (2026-09-10) — Cooper/Potomac consolidation + bridge centrality
**Data (graph.json → 68 nodes / 114 edges; verified 61):**
- `e_fusion_cooper` — Fusion GPS ↔ Chris Cooper *professional* relationship (Simpson: knew Cooper ~10 yrs; Fusion worked with Potomac Square Group and believed it paid Cooper). Typed `documented_material_exchange`/`business_relationship`, **verified** (Simpson transcript, Wikisource). Explicitly NOT evidence of a joint Russian operation.
- `e_akh_veselnitskaya`, `e_akh_katsyv`, `e_akh_hragi`, `e_akh_cooper` — Akhmetshin strengthened as the highest-centrality 2016 lobbying bridge; he said he proposed establishing HRAGI to Veselnitskaya and her Russian client Katsyv (SSCI Vol 5).
- `e_katsyv_hragi_control` — **DISPUTED object (preserved, not adjudicated):** Arakelian's conflicting HRAGI-origin story. Earlier HRAGI document: created "at the request of Denis Katsyv." Later tracked-changes revision: origin reattributed to Akhmetshin. Both versions kept; `confidence: medium`, `verification: pending`, `disputed: true` (Dossier Center / Boston Globe). Textbook: the revision doesn't erase the earlier doc; the earlier doc doesn't prove the allegation.
- `e_2016_2024_bridge_DNC` — **do_not_claim reaffirmed:** searched Cooper, Akhmetshin, Arakelian, Cymrot, Schweitzer, Dellums against RT/Tenet/FARA/later ops — no reliable 2016→2024 personnel-continuity edge found. What recurs is the ARCHITECTURE, not the cast. Hypothesis, not finding.

**Instrument (analysis.py):** added **BRIDGE CENTRALITY** over all Russian-state→American demand pairs (242 connected pairs). Per intermediary: *participation* (# pairs whose vertex-independent routes traverse it) and *severs* (# pairs that lose ALL documented routes if it is removed — a true articulation point). Only *severs* is a topological dependency.
- Result: **Trump Jr. participates 104, severs 0** — most-traversed American node, isolates nothing when removed. Same shape: 2016 campaign 48/0, Veselnitskaya 34/0, Goldstone 32/0. Load-bearing bridges are infrastructure: Swann 31, Rebel Media 23, Akhmetshin 20, Stone 10 (but participates 61 → mostly redundant), Tenet 10, Corsi 10.
- **CAVEAT:** the 2024-media bridges (Swann/Rebel/Tenet) score high partly because that architecture is still a thinner subgraph (fewer redundant routes encoded). Re-read severance as 2024 media edges land; high severance ≠ proven irreplaceability yet.

## batch 08 (2026-09-10) — LONGITUDINAL PERSONNEL BRIDGE: Lauren Chen (RT → Tenet)
**The convergence finding HANDOFF called "THE prize" — with discipline intact.** Not Maffick→Tenet (no personnel edge; stays do_not_claim). A cleaner, charged one: **RT/TV-Novosti → Chen/Donovan → Tenet.**

**New nodes:** `lauren_chen` (Founder-1), `liam_donovan` (Founder-2, spouse), `ruptly` (RT German subsidiary), `maffick` (older RT-funded US-facing network), `anissa_naouai` (RT anchor / Maffick minority owner).

**Personnel bridge (identification rests on reporting → all held `needs_primary` until indictment pulled):**
- `e_tvnovosti_chen` — Founder-1 under written ANO TV-Novosti contract ~Mar 2021–Feb 2022 (videos/social/articles, often unbranded). Chen per Yahoo + Canadian inquiry.
- `e_ruptly_donovan` — Founder-2 worked directly with RT/Ruptly ~Oct 2021–May 2022.
- `e_afanasyeva_chen_scouting` — Jan 2023 "Influencer Talent Scouting" contract from RT operatives to Chen (activates the previously-edgeless `afanasyeva` operative node).
- `e_chen_tenet_founder` / `e_donovan_tenet_founder` — Chen & Donovan co-founded Tenet; ~$9.7M RT funds flowed in.

**Maffick generation (architectural analogue):** `e_tvnovosti_rt`, `e_tvnovosti_ruptly`, `e_ruptly_maffick` (51% of German parent), `e_tvnovosti_maffick` (~$5.6M from Oct 2019, FARA/GEC), `e_naouai_maffick`, `e_maffick_audience`.

**do_not_claim / contested (must stay):**
- `e_maffick_tenet_DNC` — NO personnel/org continuity Maffick↔Tenet established. Criticality confirms: they connect ONLY through the shared parent (Maffick→TV-Novosti→Chen→Tenet), i.e. architectural analogy, not a link. "Tenet was Maffick 2.0" = hypothesis.
- `e_tenet_influencers_knowing_DNC` — the six commentators knew the funding was Russian = NOT established (DOJ: operators concealed it; influencers uncharged).
- `e_chen_intent_contested` (disputed) — Chen/Donovan criminal knowledge is ALLEGED (charged Sep 2024), not adjudicated. Criticality: the intent edge is redundant — the documented CONTRACT already connects Chen↔TV-Novosti; the knowledge question is a separate, unresolved object.

**Instrument result (73 nodes / 129 edges; 338 connected demand pairs):**
- **Lauren Chen: severs 27 — now the #1 load-bearing bridge in the graph** (above Akhmetshin 24). A documented/charged personnel node is the single most structurally critical intermediary.
- **Ben Swann: severs 31 → 0.** Adding Chen+Maffick as real RT→US-media routes DISSOLVED Swann's articulation status — proving the batch-07 caveat ("2024 subgraph thin; re-read severance as edges land"). His high score was a coverage artifact; real edges corrected it. Instrument working as designed.
- Trump Jr. still participates 111, severs 0. Goldstone 133/0, Veselnitskaya 77/0. Pattern holds: famous names = high traffic, zero dependency; the architecture is load-bearing, not the cast.

## batch 09 (2026-09-10) — Chen as NETWORK BROKER; the six split; existing-network model
**Topology refinement (the important structural correction):** the six commentators split from the `influencers_tenet` blob into individual nodes (`tim_pool`,`dave_rubin`,`benny_johnson`,`lauren_southern`,`tayler_hansen`,`matt_christiansen`, us_class=downstream). Recruitment now reads **RT → Chen → [recruit] → each**, not six phantom RT→influencer pathways. Each creator carries: `e_chen_recruit_*` (Chen recruited them), `e_tenet_*` (Tenet contracted/paid them — independent of Chen), `e_*_platforms` (pre-existing personal audience), `e_*_conmedia` (membership in the pre-existing milieu, directed INTO the collector).

**Pre-existing American layer (us_class=null CONTEXT, NOT Russian):** `blaze_tv`, `turning_point_usa`, `us_conservative_media` (milieu collector; inward edges only so it can't relay Russian reach). Chen's own footprint: `e_chen_blaze`, `e_chen_tpusa`, `e_chen_conmedia`; creators' prior footholds `e_rubin_blaze`, `e_johnson_tpusa`.

**DOJ direction edges (OBSERVED = predictive convergence for the Chen-knowing branch):** `e_afanasyeva_tenet_direction` (operatives directed hiring, editorial requests, content monitoring), `grigoriann_persona` + `e_grigoriann_tenet_funding` + `e_afanasyeva_grigoriann` (fictitious investor concealment). These independently-documented edges populate what ASSUMING_TRUE(Chen-knowing) would predict — WITHOUT upgrading the disputed intent edge.

**New do_not_claim:** `e_russia_built_network_DNC` — NOT established that Russia CREATED the American creator network. Evidence supports the opposite: the operation ATTACHED capital/infrastructure/direction to a PRE-EXISTING American social graph. Foreign actor → intermediary (Chen) → existing trusted nodes → pre-existing audiences.

**Instrument (83 nodes / 168 edges; 444 demand pairs) — the disciplined correction:**
- **Lauren Chen: severs 27 → 0, participates 112.** Now the #1-participation intermediary (3rd overall behind Trump Jr. 166, Tenet 162) but severs NOTHING. Encoding the full DOJ structure gave the operatives redundant routes into Tenet (direct editorial direction + shells + fake investor), so Chen is a high-betweenness BROKER, not an articulation point. Reach test: afanasyeva reaches Tenet with AND without Chen; RT reaches the creators without Chen (they sit on Tenet contracts).
- **Formation-dependency (temporal, Chen-critical: without her Tenet never assembles) is distinct from steady-state routing (redundant, routes around her).** The instrument measures the latter.
- Second consecutive batch (Swann→0, now Chen→0) where encoding the complete structure dissolved an apparent chokepoint — real influence operations build redundancy. participation ≠ severance.
- Trump Jr. participates 166 / severs 0. Pattern holds and strengthens.

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

## batch 10 (2026-09-10) — pre-Tenet creator subgraph + domain split
**Data:** 11 real, sourced creator↔creator and creator↔org ties, ALL dated before Tenet's Nov-2023 launch, tagged `domain: "domestic"`. Chen prior ties: Pool (Timcast IRL, Oct 2020), Rubin (Rubin Report, Mar & Sep 2021), Southern (friends/collaborators), Christiansen (longstanding friendship, approached Jun 2023). Creator circuit: Rubin↔Pool (2021), Rubin↔Johnson (Feb 2020), Pool↔Southern (2022), Pool↔Johnson (Oct 2022). Amplification: Johnson→Hansen ('Baby Lives Matter', Jul 2020, Fox+CJR); Trump Jr.→Hansen (shared Johnson's post — cross-link to the 2016 cast). Org intersections: Chen→TPUSA (contributor Jul 2022), Johnson→TPUSA (CCO), Rubin→Blaze, Chen→Blaze, Southern→Rebel (until 2017, kept domestic — predates the graph's TV-Novosti→Rebel funding).

**Instrument:** `analysis.py` gains a `domain` split — `INFLUENCE` (foreign-influence subgraph) drives reach/criticality/bridge-centrality; `DOMESTIC` drives a new **AMERICAN ECOSYSTEM DENSITY** readout. Domestic edges are barred from foreign-reach pathfinding so American creator ties can't manufacture Russian reach. `domain` documented in SCHEMA.md.

**Density result (the "centralized vs created" answer):**
- Chen degree 4, Tim Pool degree 4 = the two densest pre-Tenet connectors. Chen had a DIRECT pre-Tenet tie to **4/6** eventual creators (Rubin, Southern, Christiansen, Pool).
- With Chen: 6/6 creators in one domestic component. **Without Chen: 5/6 still connected** via the Johnson↔Rubin↔Pool show circuit, TPUSA/Blaze org intersections, and Hansen's amplification path.
- **Matt Christiansen is the ONLY creator whose sole hard pre-Tenet bridge was Chen** (personal friendship) — heterogeneous bridges, not a Chen-only star.
- Conclusion (domestic-topology, asserts no intent): **Tenet CENTRALIZED a pre-existing American network; it did not create one.** Directly supports the batch-09 `e_russia_built_network_DNC`.

## batch 11 (2026-09-10) — harden domestic edges + org architecture + G0/G1/G2 experiment
**① Hardened pre-Tenet edges to PRIMARY episode records (verified/A):** `e_chen_pool_prior` (Timcast IRL #145, Oct 2020), `e_chen_rubin_prior` (Rubin Report, Mar + Sep 2021), `e_pool_southern_prior` (Timcast 2022), `e_pool_johnson_prior` (Timcast Oct 4 2022), `e_rubin_pool_prior` (2021), `e_rubin_johnson_prior` (Feb 2020). Media Matters / PolitiFact demoted to corroboration. All carry `relationship_type: APPEARANCE`, `pre_tenet: true`. 15 domestic edges now flagged `pre_tenet`.

**② Organizational architecture layer:** `arch_profile` (structured) on `maffick` / `rebel_media` / `tenet` across {era, foreign_ownership, direct_contract, american_intermediary, existing_talent_network, organizational_concealment}. Added `sovren_media` (Swann cluster); TV-Novosti→Rebel upgraded with TPM's ~$4.5M (Mar–Aug 2023) contract detail; Maffick provenance upgraded to State Dept GEC primary (verified). analysis.py prints the comparison: **own the vehicle (Maffick) → contract the producer (Swann/Rebel) → embed at the founder layer (Tenet)** — vehicle changes, architecture-shape holds. Verdict leans: Russia ADAPTED the vehicle to the target network; cast varies, architecture persists.

**③ G0→G1→G2 staged experiment + removal tests (analysis.py):** connectivity uses HARD DOMESTIC edges; Russian reach uses INFLUENCE edges only, DIRECTED (a Timcast appearance is not a Russian conduit — the earlier merged-undirected version leaked and was corrected).
- **G0** (pre-Tenet US network): 15 edges, 11 nodes, **1 component; six creators 6/6 connected before Tenet.**
- **G1** (+RT→Chen/Donovan→Tenet spine, six not yet attached): Russian→creator reach **0/6** (correct — Tenet exists, unattached).
- **G2** (+six recruit/contract edges): Russian→creator reach **6/6.** Tenet flips reach 0→6/6 across an already-connected American network.
- **Removal tests:** remove Chen → creators 5/6 domestic (Christiansen orphans), Russian reach still 6/6; remove Tenet → creators 6/6, Russian reach still 6/6; **remove BOTH Chen+Tenet → 0/6.** The foreign coupling is carried REDUNDANTLY by the Chen+Tenet pair; no lone gate (consistent with Chen severs=0). Remove all six → broker + TPUSA + Blaze still stand: American infrastructure coupled to, not created by, Russia.

Chain now runs document → relationship → network → organizational mechanism → historical comparison. 84 nodes / 180 edges. validate.py clean.

## batch 12 (2026-09-10) — independent pre-Tenet Russian branch: RT → Lauren Southern
**The alternate path.** Southern has a documented, pre-Tenet Russian-side edge that does NOT run through Chen/Tenet.
- `e_rt_southern` — Southern testified (Canada SECU, mtg 130) she did contributions to RT "before the war" (incl. a 2022 trucker-convoy live report). Typed `documented_contact` / `hosted_appearance`, **verified** (sworn parliamentary testimony), `domain: influence`, `pre_tenet: true`. She also testified she believed Tenet was backed by a tech investor (unaware of Russian funding).
- `dugin` (new node, DISTINCT actor class — Russian ultranationalist political actor, not state media) + `e_southern_dugin` — direction is **Southern → Dugin** (she traveled to Moscow and interviewed him, Jun 2018, arranged it herself). A journalist-subject contact, NOT a Russia→Southern conduit. Deliberately not collapsed into "Russian state → Southern."
- `e_rt_pool_via_southern_DNC` (do_not_claim) — RT influence did NOT reach Pool THROUGH Southern: RT→Southern is a Russian-side contact, but Southern→Pool is a DOMESTIC appearance. Independent entry ≠ transitive influence.

**Experiment upgrade (analysis.py) — G3/G4 + independent-entry-point count + removal ladder:**
- **Independent Russian entry points into the six (pre-Tenet, bypassing Chen/Tenet): 1 — Lauren Southern (RT).**
- **Removal ladder (Russian→creator reach): G2 6/6 → G2−Chen/Tenet 0/6 → G4(=G2+G3)−Chen/Tenet 1/6 (Southern via the independent RT edge) → G4−Chen/Tenet−independent 0/6.**
- Interpretation: Chen+Tenet is the MAIN foreign gate but not the ONLY pre-Tenet Russian contact touching the six. A Russian CONTACT (RT→Southern) is not an influence PATHWAY (Southern→Pool stays domestic). This is the metric that bridges the Tenet case to the historical-architecture work: *how many independent Russian-side entry points existed into the pre-existing American creator graph?*

85 nodes / 183 edges. validate.py clean.

## batch 13 (2026-09-10) — backward sweep: 1 established entry point, 5 searched-negatives
**Sweep of the other five for a CLEAN pre-Tenet Russian-side edge (RT/Sputnik/Russian-official relationship, not mere Russia commentary). Result did NOT explode — that is the finding.**
- **Southern edge upgraded/split** into two dated, better-provenanced edges: `e_rt_southern_contrib_2019` (April 2019 RT interview/report on her doc *Borderless*; relationship_type CONTRIBUTION) and `e_rt_southern_report_2022` (pre-war trucker-convoy live report; relationship_type LIVE_REPORT). Both verified, `domain: influence`, `pre_tenet: true`. Independent of Chen/Tenet in relationship AND time.
- **Five `do_not_claim` negatives** (`e_rt_{pool,rubin,johnson,hansen,christiansen}_DNC`): "NOT established (not 'none')". Each records what the sweep DID find — Pool = Russia content (Putin-'moderate' segment) not a relationship; Rubin = discussed RT/disinfo; Johnson = Russia/Ukraine content; Hansen = domestic trajectory (CJR); Christiansen = domestic Chen friendship. Searched-negative ≠ proven zero.
- **`metadata.entry_point_sweep`** records the full table; analysis.py prints it in the INDEPENDENT ENTRY POINTS section.
- **Established independent pre-Tenet Russian entry points into the six = 1 (Southern).** Removal ladder unchanged (6/6 → 0/6 → 1/6 → 0/6). Southern's two RT edges auto-join G3.

85 nodes / 189 edges. validate.py clean.

## batch 14 (2026-09-10) — actor_class + relationship_type taxonomy (the Dugin fix, permanent)
**Controlled vocabularies added to metadata.legends and SCHEMA.md:**
- **`actor_class`** (node): RUSSIAN_STATE · RUSSIAN_STATE_MEDIA · RUSSIAN_STATE_LINKED_PRIVATE · RUSSIAN_POLITICAL_ACTOR · RUSSIAN_ORDINARY_PERSON · INTERMEDIARY · US_ACTOR · UNKNOWN. All Russian-side/intermediary nodes classed (RUSSIAN_STATE 13, RUSSIAN_STATE_MEDIA 5, RUSSIAN_STATE_LINKED_PRIVATE 8, INTERMEDIARY 11, RUSSIAN_POLITICAL_ACTOR 1 = Dugin, US_ACTOR 41). **Dugin is now permanently distinct from RT** — reach origins are the three RUSSIAN_STATE* classes only, so a political actor is never auto-counted as a state-media conduit.
- **`relationship_type`** (edge): CONTRACT/EMPLOYMENT/CONTRIBUTION/LIVE_REPORT/INTERVIEW/EVENT/TRAVEL/FUNDING/RECRUITMENT/PR/AMPLIFICATION/APPEARANCE/CONTACT/OWNERSHIP/DIRECTION. Tagged onto key influence edges; INTERVIEW (creator→actor) is explicitly not a conduit.

**Scoreboard upgraded (analysis.py):** entry points now split **DIRECT** (RUS_ORIGIN→creator, no Chen/Tenet) vs **INTERMEDIARY_MEDIATED** (RUS_ORIGIN→intermediary(s)→creator, no Chen/Tenet). Current: **1 direct (Southern) + 0 intermediary-mediated of 6; 5 not_established.** The intermediary lane auto-populates when a mediated path lands. `metadata.entry_point_sweep` records method + the integrity-exclusion list (content, ideology, appearances-with, post-Tenet, Chen-mediated, Southern→Dugin, political-actor auto-origin).

85 nodes / 189 edges. validate.py clean.

## batch 15 (2026-09-10) — sweep hits adjudicated: 1 kept, 3 near-misses, content rejected
**The sweep worked: 1 qualifying edge + structurally-interesting near-misses we can explicitly distinguish from influence.**
- **DIRECT_CONTACT (non-qualifying):** `e_rt_pool_office_2016` / `e_sputnik_pool_office_2016` — Pool said he was at RT+Sputnik offices in 2016 (with Fairbanks). `relationship_type: OFFICE_VISIT`, `domain: influence`, do_not_claim guardrail `e_rt_pool_influence_DNC`. CHASE: contemporaneous 2016 record of why he was there.
- **PERSONNEL_CONTINUITY (non-qualifying):** `sputnik`→`cassandra_fairbanks` (EMPLOYMENT, influence) → `tim_pool` (EMPLOYMENT, **domain: domestic** — can't relay Russian reach). Guardrail `e_sputnik_pool_via_fairbanks_DNC`.
- **SHARED_MEDIA_INFRASTRUCTURE (non-qualifying):** `ora_tv`→`dave_rubin` (domestic production) + `ora_tv`→`rt_america` (Ora licensed to RT America, stated independent). Guardrail `e_rt_rubin_via_ora_DNC`.
- New nodes: `sputnik`, `rt_america` (RUSSIAN_STATE_MEDIA), `cassandra_fairbanks`, `ora_tv` (US_ACTOR).

**Scoreboard mechanism:** analysis.py now gates entry-point counting by **conduit vs proximity** relationship_type (`PROXIMITY = OFFICE_VISIT/CONTACT/INTERVIEW/EVENT/TRAVEL/APPEARANCE/AMPLIFICATION` excluded from both DIRECT and INTERMEDIARY_MEDIATED). Result unchanged: **1 direct (Southern) + 0 mediated of 6; 5 not_established.** `metadata.near_miss_taxonomy` records the five classes; `entry_point_sweep` updated with Pool/Rubin near-miss notes.

**Link preservation:** `sources/sweep-log.md` classifies every URL touched (qualifying / near-miss / rejected-content) so negatives are recorded searches; `sources/citation-url-inventory.txt` enumerates all 62 external citation URLs in the graph. Rejected-content links (Pool Putin-moderate, Rogan #1242, RFE/RL, Johnson/Griner, CDMRN, WIRED, NPR) saved but NOT edged.

89 nodes / 198 edges. validate.py clean.

## batch 16 (2026-09-10) — personnel lane formalized + open-question tracker
**Sputnik→Fairbanks→Pool given its own lane** (per Brad's field spec): `domain: personnel`, `relationship_class: PERSONNEL_CONTINUITY`, `conduit: false`, `scoreboard: false`. Excluded from influence reach AND domestic density — a third lane. Recorded that Fairbanks appeared on Pool's show BEFORE the 2021 hire (`e_fairbanks_pool_appearance`) — not a random later hire. Direct-contact (Pool office visit) and shared-infrastructure (Ora) edges tagged with `relationship_class` + conduit/scoreboard flags. Southern's two edges marked INFLUENCE/conduit/scoreboard=true.
- **`metadata.legends.domain`** now three values; **`relationship_class`** legend added (INFLUENCE/DIRECT_CONTACT/PERSONNEL_CONTINUITY/SHARED_MEDIA_INFRASTRUCTURE/CONTENT).
- **`metadata.open_questions[OQ-01]`** banked: *what was Pool & Fairbanks' 2016 RT/Sputnik office visit for?* — upgrades to a SECOND direct entry if a contemporaneous 2016 record shows reporting/contributing/interviewing FOR RT/Sputnik; killed if tour/event/ordinary. Includes the Fairbanks+Pool 2016 search cluster + target record types (search them together, not Pool alone).
- analysis.py prints the PERSONNEL-CONTINUITY LANE and OPEN QUESTIONS sections. Scoreboard unchanged: **1 direct (Southern) + 0 mediated of 6; 5 not_established.**

89 nodes / 199 edges. validate.py clean.

## batch 17 (2026-09-11) — TPUSA as domestic hub; the person-mediated vs institution-direct line
**TPUSA enriched as a DOMESTIC organizational hub** (`actor_class: US_ACTOR`, `organization_type: POLITICAL_MEDIA_ORGANIZATION`), bridging Chen (contributor Jul 2022) and Benny Johnson (contributor/former CCO). Node `history` records TPUSA removing Chen's profile after the indictment. The two real edges kept SEPARATE: `RT→Chen` (INFLUENCE/CONTRIBUTION) and `Chen→TPUSA` (domestic membership).
- **`e_rt_tpusa_DNC` (do_not_claim):** NO direct organizational Russia→TPUSA relationship established. Searched TPUSA+Russia/RT/FARA/funding/government/influence — all resolve to Chen's RT relationship, Russia content, or unrelated TPUSA activity. Documented shape is **Russia → Chen (person) → TPUSA (institution)**, never Russia → TPUSA.
- **`metadata.architecture_distinctions`** banked (reusable finding): **PERSON_MEDIATED** (RT→Chen→TPUSA) vs **INSTITUTION_DIRECT** (not established for TPUSA) — a materially different, stronger claim; do not conflate.
- **Removal test:** removing TPUSA leaves the creator cluster 6/6 (not a cut-point) and Russian→creator reach 6/6 (unaffected — TPUSA carries no influence in-edge). TPUSA is a shared domestic membership, not a load-bearing bridge and not Russian-linked.
- Scoreboard unchanged: **1 direct (Southern) + 0 mediated of 6; 5 not_established.**

89 nodes / 200 edges. validate.py clean.

## batch 18 (2026-09-11) — TPUSA as a documented DOMESTIC amplification machine
**Resolves "Benny's virality can't be coincidence" into an AMERICAN institutional explanation, not a Russian one.**
- `turning_point_usa.amplification_profile`: $7.2M media budget (2021), 400+ creators onboarded by 2022, 275 ambassadors / ~70M claimed reach (2021), capabilities = production support / PR & media booking / event content infrastructure / creator training / deliberate cross-promotion; Kirk+Johnson influencer retreat. Sources: Verge, Carnegie.
- New node `tpusa_productions` (production arm, est. 2018) + `e_johnson_tpusa_productions`: Benny Johnson, viral-media specialist (ex-BuzzFeed/Blaze), hired CCO Feb 2019 to operate it. All domestic, conduit=false.
- **`e_russia_benny_virality_DNC` (do_not_claim):** Russia did NOT cause Benny's virality; the documented cause is TPUSA's domestic amplification machine.
- **`metadata.timeline_tpusa_tenet`** (2018 productions → 2019 CCO/strategy → 2021 $7.2M/275 ambassadors → 2022 400+ creators/cross-promo → 2022-07 Chen contributor → 2023 Tenet assembled → 2023-11 launch → 2024-09 DOJ).
- **`metadata.architecture_distinctions.INFRASTRUCTURE_EXPLOITATION`** added: operation plugs into a PRE-EXISTING American amplifier it did not build/control (distinct from PERSON_MEDIATED and INSTITUTION_DIRECT).
- **`OQ-02`**: did Russian influence EXPLOIT TPUSA's pre-optimized amplifier? Current: 1 of the six (Benny) documented inside it + Chen (broker); still NO Russia→TPUSA.
- analysis.py prints DOMESTIC AMPLIFICATION INFRASTRUCTURE. Removal test: TPUSA still not a creator-cluster cut-point (6/6), no Russian reach. Scoreboard unchanged: 1 direct (Southern) + 0 mediated.

90 nodes / 203 edges. validate.py clean.

## batch 19 (2026-09-11) — IRA → TPUSA_CONTENT (2016 content-harvest, Chen-independent)
**A real Russian-side edge to the TPUSA ecosystem, independent of Chen — modeled as content-harvest, not organizational penetration.**
- New node `tpusa_content` (layer content) — TPUSA's authentic media OUTPUT, deliberately separate from the org so Russian amplification can never transit to TPUSA/Benny/creators. Verified: IRA influence-reach = {tpusa_content} only; reaches org/Benny/Tenet/creators = False.
- `e_ira_tpusa_content` (verified, SSCI New Knowledge + Just Security + WaPo Examiner): 2016 IRA shared/rebranded TPUSA memes (Memopolis, Angry Eagle; sometimes leaving TPUSA branding intact). `relationship_type: AMPLIFICATION`, `relationship_class: CONTENT_HARVEST`, conduit=false, scoreboard=false. IRA reclassified `RUSSIAN_STATE_LINKED_PRIVATE` (Prigozhin contractor).
- `e_tpusa_produces_content` (turning_point_usa→tpusa_content, domestic, directed so content never routes back).
- `e_ira_tpusa_org_DNC` (do_not_claim): reaffirms NO IRA/Russia→TPUSA organizational relationship; exploitation of OUTPUT ≠ org relationship.
- `metadata.russian_interaction_modes`: **2016 CONTENT_HARVEST** (IRA→content) vs **2021-24 COUPLING** (RT→Chen→Tenet→creators) — same ecosystem, two mechanisms ~5-8 yrs apart; Russia created the network in neither. `architecture_distinctions.CONTENT_HARVEST` added.
- Publishable statement: "IRA accounts were documented amplifying and rebranding TPUSA content during the 2016 operation. This establishes Russian exploitation of TPUSA's media output, not Russian control, funding, or coordination with TPUSA."
- Scoreboard unchanged: 1 direct (Southern) + 0 mediated. 91 nodes / 206 edges. validate.py clean.

## batch 20 (2026-09-11) — PASS ①: DOJ indictment primary + conduct/identity evidence model
**Pulled the actual SDNY indictment (US v. Kalashnikov & Afanasyeva). Folded primary CONDUCT onto the 2024 spine WITHOUT downgrading the multi-source IDENTITY bindings.**
- Conduct edges → **verified** on the DOJ primary, each with `verification_basis` {conduct: DOJ_primary, identity: multi_source}: `e_tvnovosti_chen` (Founder-1 ANO TV-Novosti contract, ~217 videos invoiced/~209 on YouTube/~25 articles; TN incorporation 2022-01-19), `e_ruptly_donovan` (Founder-2 RT/Ruptly Oct2021–May2022), `e_chen_tenet_founder`/`e_donovan_tenet_founder` (jointly operate Company-1), `e_afanasyeva_chen_scouting` (Grigoriann influencer scouting), `e_grigoriann_tenet_funding` (~$10M via shells), `e_afanasyeva_tenet_direction`, shells/employees, + 6 `e_chen_recruit_*`.
- **Identity bindings kept VERIFIED multi-source** (not downgraded): `identity_binding` on Chen (Founder-1), Donovan (Founder-2), Tenet (Company-1) — TN corporate records + Canada Commission + CBS + Tyee. `metadata.evidence_model` banks the principle: a primary doc's silence on identity does NOT downgrade an identity already multi-source-established.
- **Founders WITTING vs commentators UNWITTING, both primary-anchored:** `e_tenet_influencers_knowing_DNC` verified (concealment primary-alleged); `e_chen_intent_contested` strengthened with the founders' "the Russians" comms (primary-ALLEGED) but kept disputed (charged ≠ convicted).
- **OQ-02:** `e_tpusa_tenet_infra_DNC` — TPUSA infrastructure-exploitation NOT established (Tenet used creators' OWN audiences, not TPUSA machinery); people-overlap established. Both OQ-01/OQ-02 stay OPEN with sharpened dispositions + refined query sets.
- Verified edges 92→110; 2024-media architecture 25→43 verified. Scoreboard unchanged (1 direct + 0 mediated). 91 nodes / 207 edges. validate.py clean.

## batch 21 (2026-09-11) — PASS ③: 2016 cast entry-point sweep (longitudinal keystone)
**Same 4-state surface as the 2024 creator sweep; intent tracked separately from relationship.** New branches:
- **Manafort** (the heavyweight): `deripaska`→Manafort (influence-ops employment since 2004, DIRECT), `kilimnik`↔Manafort (Kilimnik = Russian intel officer, liaison), **`e_manafort_kilimnik_info`** (Manafort → Kilimnik internal polling + strategy — observed campaign-info OUTFLOW), `kilimnik`→`deripaska`, `e_kilimnik_gru_qualified` (low/qualified GRU hack-leak link). SSCI Vol 5.
- **Papadopoulos**: `mifsud`→Papadopoulos→`timofeev`→`russian_mfa`; `polonskaya`→Papadopoulos. `e_papadopoulos_witting_DNC`: potential vector, NOT a witting Russian-intel cooperator (SSCI). Mueller.
- **Carter Page**: `dvorkovich`→Page, `baranov`→Page (2016 Moscow meetings, Page acknowledged — DIRECT contact). `e_sechin_page_contested` (disputed — Steele/Crossfire intel reporting, not clean primary) + `e_page_intel_conduit_DNC` (intelligence-conduit NOT established).
- **Kilimnik**: modeled as a RUSSIAN-SIDE intermediary node (intel officer), excluded from the American scoreboard.
- Trump Jr. / Stone branches already present (Agalarov→Goldstone; GRU→Guccifer 2.0→Stone) with their do_not_claim negatives.

**`metadata.cast_sweep_2016`** records the adjudicated matrix; analysis.py prints raw topology (code) + analyst verdict (metadata), keeping the "direct entry is a substance call" distinction (Deripaska influence-ops employment counts; a social tie to a state-linked businessman does not).
- **Scoreboard:** DIRECT {Manafort, Page}; MEDIATED {Trump Jr, Stone, Manafort, Papadopoulos}; Kilimnik unscored.
- **Finding:** the 2016 cast is HETEROGENEOUS (intermediary / intel-persona / deep-intermediary+info-outflow / potential-vector / direct-official-contact) — the variation the architecture-vs-cast hypothesis needs. Same vocabulary now spans 2016↔2024.
- 2024 scoreboard unchanged (1 direct + 0 mediated). Verified 110→120. 102 nodes / 224 edges. validate.py clean.

## batch 22 (2026-09-11) — PASS ④: dangling-node cleanup (Doppelganger triad + prune)
**Zero dangling nodes.**
- **structura** KEEP+CONNECT: `kiriyenko→structura` (DIRECTION) + `structura→fake_sites` (PRODUCTION, `scope: Doppelganger_fake_site_network`). VERIFIED — DOJ 9/4/24 + Treasury OFAC jy2195 (Structura a key actor; SDA+Structura ran 60+ impersonation sites).
- **ano_dialog** KEEP+CONNECT: `kiriyenko→ano_dialog` (DIRECTION) + `ano_dialog→fake_sites` (PRODUCTION, `scope: Doppelganger_fake_media_network`). VERIFIED — DOJ affidavit 9/4/24 (created original media brands; same articles on cybersquatted domains + ANO Dialog brands; internal SDA doc names all three) + Treasury jy2559.
- Existing SDA edges refined to VERIFIED + network-scoped for consistency.
- **agalarov_network** PRUNED — redundant abstraction, 0 unique edges, superseded by aras_agalarov/emin_agalarov/crocus_group/kaveladze. Logged in `metadata.pruned_nodes`. No evidence lost.
- Downstream edges deliberately **network-scoped** (`scope` field) — not a claim of universal individual-site authorship.
- **Result:** Doppelganger triad complete (Kiriyenko → {SDA, Structura, ANO Dialog} → fake_sites), giving the 2024 side TWO distinct observed mechanisms — RT→Tenet *coupling* vs Presidential-Administration→PR-firms→*fabricated media* (Doppelganger). Sharpens ⑤'s intermediary-class comparison. 2024 scoreboard unchanged.

101 nodes / 228 edges. validate.py clean. Zero dangling nodes.

## batch 23 (2026-09-11) — PASS ⑤: arch_profile v2 + architecture-vs-cast across 9 vehicles
**Canonical v2 schema** (`metadata.legends.arch_profile_v2`): `foreign_principal` (6-value, adds russian_presidential_administration + russian_political_actor), `foreign_ownership` (majority/significant/none_demonstrated/n_a — not binary), `funding_mechanism` (+client_payment so a law firm's client relationship isn't a "funding mechanism"), `intermediary_class` (9 classes — the comparison key), `target_layer` (multi-value array), `leverages_existing_network`, `concealment` (low renamed), `is_russian_vehicle` ({value, basis} — not a masquerading boolean).
- **Media vehicles backfilled** to v2: Maffick (media_subsidiary, ownership majority), Rebel/Swann (production_company), Tenet (founder_embedded_company).
- **2016 vehicles profiled:** HRAGI (lobbying_front_ngo — principal CONTESTED, not promoted past e_katsyv_hragi_control), Prevezon (financial_litigation_vehicle, ownership majority/verified), **BakerHostetler (law_firm) + Potomac (pr_government_relations) = is_russian_vehicle:false/contracted_service — the negative controls**, shell_companies (shell_network).
- **Doppelganger = ONE fabrication_firms class** with `members: [sda, structura, ano_dialog]` (principal russian_presidential_administration/Kiriyenko); Structura/ANO Dialog carry `arch_member_of` pointers, not independent profiles.
- **Result — computed, not asserted:** all 9 intermediary classes distinct across 2016→2024; the CLASS changes at nearly every vehicle while the SHAPE holds (foreign principal → intermediary class → American-facing output → audience/Congress/courts). *Russia adapts the vehicle to the target; it does not rerun one template.* Two contracted US firms retained as explicit non-vehicles = the negative control keeping the comparison honest.
- Bugfix: normalize strips unknown top-level node fields (arch_profile_schema didn't survive) → v2 detected via `arch_profile.intermediary_class`. 2024 scoreboard unchanged.

101 nodes / 228 edges. validate.py clean.

## batch 24 (2026-09-11) — evidence_state + derived publication classification (schema lock)
**Publication is now a DETERMINISTIC derived field; the renderer consumes it, never decides evidentiary status.**
- New authoritative field **`evidence_state`** {primary_verified, multi_source_verified, reported, contested, conditional, negative_finding, searched_negative, cut} — audit-assigned wins; otherwise provisional from current fields.
- New DERIVED **`publication`** {layer, eligible, reason}: `public_core` = primary_verified ∨ multi_source_verified ∨ (do_not_claim WITH provenance); `evidence_ledger` = reported ∨ contested; `research_graph` = everything else. **A do_not_claim guardrail with NO provenance object is demoted to research_graph** (a careful negative must not read as a verified positive).
- Orthogonal red-team check fields seeded on every edge: `claim_scope` {exact/narrower/broader}, `identity_check` {exact_person/pseudonym_binding/ambiguous}, `temporal_check` {supported/partial/unsupported} — default `unaudited`.
- normalize.py computes evidence_state + publication; validate.py ENFORCES the derivation invariant (publication must equal the deterministic derivation) and flags any do_not_claim missing provenance. Legends added.
- **Current split: public_core 125 (99 primary_verified + 1 multi_source + 25 do_not_claim-w/-provenance), evidence_ledger 103.** These are provisional until the 75-edge audit assigns final evidence_state per edge.

101 nodes / 228 edges. validate.py clean.

## batch 25 (2026-09-11) — Cluster A audit (Mueller Vol I): template proven end-to-end
Pulled Mueller Vol I (Wikisource) against the 10 Cluster-A propositions.
- **4 CONFIRMED → primary_verified** with verbatim supporting quotes + exact section + proposition: `e_aras_emin` (IV.A.1.a), `e_polonskaya_papadopoulos` (IV.A.2.b), `e_timofeev_mfa` (IV.A.2.d), `e_agalarov_dtj` (IV.A.1.a).
- **1 SCOPE FIX (the audit doing its job):** `e_agalarov_dtj` claimed "meetings and gifts" — Mueller supports only the 2013 Crocus/Miss-Universe business relationship. Claim NARROWED to what the source establishes; claim_scope=exact after narrowing. Exactly the CSF provenance-to-claim failure class, caught.
- **6 PENDING_PULL** with exact located section + proposition recorded (not confirmed, not claimed): `e_meeting_kushner` + `e_emin_goldstone` + `e_film` (Mueller IV.A.5 June 9 meeting — a Wikisource subpage this fetch couldn't reach), `e_goldstone_dtj_vk` + `e_kremlin_agalarov` (SSCI Vol 5), `e_dtj_wikileaks` (Mueller §V).
- Audit fields applied: `primary_candidate.{document,section,proposition,supporting_quote}`, `claim_scope`, `identity_check`, `temporal_check`. Public core 125→129.

101 nodes / 228 edges. validate.py clean.

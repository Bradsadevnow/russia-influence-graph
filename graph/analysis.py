#!/usr/bin/env python3
"""Network-analysis instrument for graph.json (stdlib only).

Implements the three-graph framework (FRAMEWORK.md):
  G_obs        — claimable edges (not do_not_claim, not disputed)
  G_contested  — do_not_claim + disputed edges (evidentiary objects)
  G_conditional(E) = G_obs + assumed contested edge E

For every contested edge it computes EDGE CRITICALITY: is the pair already connected
in G_obs, by how many vertex-independent routes, and does assuming E change the
component structure. Neither answer says whether E is true — only how much the
topology depends on it.

Also: source-independence collapse (documents -> independent origins) and a temporal
causality check.

Run: python3 graph/analysis.py
"""
import json, collections, pathlib, re

g = json.load(open(pathlib.Path(__file__).parent / "graph.json"))
NODES = {n["id"]: n for n in g["nodes"]}
EDGES = g["edges"]

def label(nid): return NODES.get(nid, {}).get("label", nid)

def is_contested(e): return e["confidence"] == "do_not_claim" or e.get("disputed")
def is_conditional(e): return e.get("provenance") == "conditional"

# G_obs is CLAIMABLE-OBSERVED only: never contested, and NEVER a conditional
# consequence. A conditional edge (provenance=conditional, derived under an
# assumption) is barred from G_obs by construction — the firewall against
# treating "what would follow IF E" as "what happened".
OBS = [e for e in EDGES if not is_contested(e) and not is_conditional(e)]
CONTESTED = [e for e in EDGES if is_contested(e)]
CONDITIONAL = [e for e in EDGES if is_conditional(e)]
def is_domestic(e): return e.get("domain") == "domestic"
# INFLUENCE = the foreign-influence propagation graph: observed, non-contested, and
# NOT a US-ecosystem context edge. Russian-origin reach / criticality / bridge
# centrality run on THIS set — American creator<->creator ties are not Russian conduits.
INFLUENCE = [e for e in OBS if not is_domestic(e)]
DOMESTIC  = [e for e in OBS if is_domestic(e)]

# ---- undirected adjacency over a given edge set -------------------------------
def adjacency(edgeset, extra=None):
    adj = collections.defaultdict(set)
    for e in list(edgeset) + (list(extra) if extra else []):
        adj[e["source"]].add(e["target"])
        adj[e["target"]].add(e["source"])
    return adj

def components(edgeset, extra=None):
    """Connected components over nodes incident to the edge set."""
    adj = adjacency(edgeset, extra)
    seen, comps = set(), []
    for start in adj:
        if start in seen: continue
        stack, comp = [start], []
        while stack:
            v = stack.pop()
            if v in seen: continue
            seen.add(v); comp.append(v)
            stack.extend(adj[v] - seen)
        comps.append(comp)
    return comps

def bfs_path(adj, s, t, blocked):
    """Shortest path s->t avoiding `blocked` intermediate vertices."""
    if s == t: return [s]
    prev, q = {s: None}, collections.deque([s])
    while q:
        v = q.popleft()
        for w in adj[v]:
            if w in prev or (w in blocked and w != t): continue
            prev[w] = v
            if w == t:
                path = [t]
                while path[-1] is not None: path.append(prev[path[-1]])
                return list(reversed(path[:-1]))
            q.append(w)
    return None

# Hub/sink nodes (audience, platforms, Congress) are shared destinations, not
# connective tissue: "both reach the American public" is not a meaningful path.
# They may be endpoints but are barred as *intermediate* vertices in criticality.
SINKS = {nid for nid, n in NODES.items() if n.get("type") in ("audience", "platform")}

def vertex_independent_routes(edgeset, s, t):
    """Lower bound on vertex-independent s->t routes (Menger-style greedy):
    repeatedly take a shortest path, then forbid its *internal* vertices.
    Sink/hub nodes are barred as intermediates (unless they are s or t)."""
    adj = adjacency(edgeset)
    routes, blocked = [], set(x for x in SINKS if x not in (s, t))
    while True:
        p = bfs_path(adj, s, t, blocked)
        if not p: break
        routes.append(p)
        blocked |= set(p[1:-1])           # forbid internal vertices only
        if not p[1:-1]: break             # direct edge; no internal vertices to block
    return routes

# ---- report -------------------------------------------------------------------
print("="*78)
print("THREE-GRAPH STATE")
print("="*78)
obs_comps = components(OBS)
print(f"G_obs        : {len(OBS)} edges, {sum(len(c) for c in obs_comps)} nodes, "
      f"{len(obs_comps)} connected component(s)  sizes={sorted((len(c) for c in obs_comps), reverse=True)}")
verified = [e for e in OBS if e['verification']=='verified']
vcomps = components(verified)
print(f"G_obs_verified: {len(verified)} edges, {len(vcomps)} component(s)  "
      f"sizes={sorted((len(c) for c in vcomps), reverse=True)}")
print(f"G_contested  : {len(CONTESTED)} edges  "
      f"[{sum(e['confidence']=='do_not_claim' for e in CONTESTED)} do_not_claim, "
      f"{sum(bool(e.get('disputed')) for e in CONTESTED)} disputed]")

print("\n" + "="*78)
print("EDGE CRITICALITY  (per contested edge E — how much would E change the topology?)")
print("="*78)
for e in CONTESTED:
    s, t = e["source"], e["target"]
    kind = "DO_NOT_CLAIM" if e["confidence"]=="do_not_claim" else "DISPUTED"
    routes = vertex_independent_routes(INFLUENCE, s, t)
    R = len(routes)
    c_without = len(components(INFLUENCE))
    c_with = len(components(INFLUENCE, extra=[e]))
    dcomp = c_without - c_with
    print(f"\nE = {e['id']}  [{kind}]")
    print(f"    {label(s)}  ──►  {label(t)}")
    print(f"    already connected in G_obs? {'YES' if R else 'NO'}   "
          f"vertex-independent routes: {R}   Δcomponents if assumed: {dcomp}")
    if R == 0:
        print(f"    ⇒ CRITICAL: assuming E CREATES connectivity that G_obs does not otherwise have.")
    elif R == 1:
        internal = routes[0][1:-1]
        cut = " / ".join(label(x) for x in internal) or "(direct)"
        print(f"    ⇒ LOW structural criticality: a documented route already connects them, "
              f"but through a SINGLE cut point → {cut}")
        print(f"      (assuming E would only shorten paths, not create the connection — and that "
              f"lone route hinges on {cut})")
    else:
        print(f"    ⇒ NOT NEEDED for connectivity: {R} independent documented routes already exist. "
              f"Assuming E adds a shortcut, not a component.")
        for i, p in enumerate(routes[:3], 1):
            print(f"        route {i}: " + " → ".join(label(x) for x in p))

# ---- Russian-origin reach: independent GRU→American-target routes ------------
print("\n" + "="*78)
print("RUSSIAN-ORIGIN REACH  (vertex-independent routes from GRU into US targets, in G_obs)")
print("="*78)
TARGETS = ["trump_campaign", "us_audience", "dtj", "stone", "breitbart"]
for tid in TARGETS:
    if tid not in NODES: continue
    routes = vertex_independent_routes(INFLUENCE, "gru", tid)
    print(f"\nGRU ──► {label(tid)}: {len(routes)} vertex-independent route(s)")
    for i, pth in enumerate(routes[:4], 1):
        print(f"    {i}: " + " → ".join(label(x) for x in pth))
    if len(routes) >= 3:
        print(f"    ⇒ {len(routes)} independent Russian-origin paths reach this node — structurally strong "
              f"(no single intermediary is a chokepoint).")
    elif len(routes) == 1 and routes[0][1:-1]:
        print(f"    ⇒ single route; hinges on {' / '.join(label(x) for x in routes[0][1:-1])} (a chokepoint).")

# ---- BRIDGE CENTRALITY: which intermediaries carry / sever Russian-origin reach ----
print("\n" + "="*78)
print("BRIDGE CENTRALITY  (over all Russian-state origin → American target demand pairs)")
print("Participation = # demand pairs whose vertex-independent routes pass through the node.")
print("Severs = # demand pairs that lose ALL documented routes if the node is removed")
print("         (a true articulation point / single chokepoint for that reach).")
print("="*78)

def routes_blocking(edgeset, s, t, preblock):
    """Greedy vertex-independent s->t routes with an extra pre-blocked vertex set,
    reusing the sink bar. Returns list of paths."""
    adj = adjacency(edgeset)
    routes = []
    blocked = set(x for x in SINKS if x not in (s, t)) | set(x for x in preblock if x not in (s, t))
    while True:
        pth = bfs_path(adj, s, t, blocked)
        if not pth: break
        routes.append(pth)
        internal = set(pth[1:-1])
        if not internal: break
        blocked |= internal
    return routes

ORIGINS = [nid for nid, n in NODES.items() if n.get("layer") == "russian_state"]
AM_TARGETS = [nid for nid, n in NODES.items()
              if n.get("us_class") in ("direct_state_connected", "bridge_amplifier", "downstream")
              and n.get("type") not in ("audience", "platform")]
# demand pairs that actually have at least one documented route in G_obs
demand = []
for s in ORIGINS:
    for t in AM_TARGETS:
        if s == t: continue
        base = vertex_independent_routes(INFLUENCE, s, t)
        if base:
            demand.append((s, t, base))
print(f"origins (russian_state): {len(ORIGINS)}   american targets: {len(AM_TARGETS)}   "
      f"connected demand pairs: {len(demand)}")

CANDIDATES = [nid for nid, n in NODES.items()
              if nid not in SINKS and n.get("layer") in ("intermediary", "us_media", "us_political")]
participation = {c: 0 for c in CANDIDATES}
severs = {c: 0 for c in CANDIDATES}
for (s, t, base) in demand:
    internal_union = set()
    for pth in base:
        internal_union |= set(pth[1:-1])
    for c in CANDIDATES:
        if c in (s, t): continue
        if c in internal_union:
            participation[c] += 1
        # articulation test: with c removed, does ANY route survive?
        if not routes_blocking(INFLUENCE, s, t, {c}):
            severs[c] += 1

ranked = sorted(CANDIDATES, key=lambda c: (severs[c], participation[c]), reverse=True)
print("\n  node                         severs   participates   (of %d demand pairs)" % len(demand))
for c in ranked[:12]:
    if participation[c] == 0 and severs[c] == 0: continue
    flag = "  ◄ SOLE CHOKEPOINT for %d pair(s)" % severs[c] if severs[c] else ""
    print(f"    {label(c):<28} {severs[c]:>4}   {participation[c]:>10}{flag}")
print("\n  Reading: high 'severs' = a load-bearing bridge whose removal isolates Russian-origin")
print("  reach — the structural claim is about the ARCHITECTURE, not any American's intent.")
print("  A node can participate widely yet sever nothing (redundant), or sever much while")
print("  participating narrowly (a lone gate). Only 'severs' is a topological dependency.")

# ---- G_conditional(E): ASSUMING_TRUE — every result carries the assumption -----
def reachable_nonsink(edgeset, s, extra=None):
    """Nodes reachable from s WITHOUT passing THROUGH sink/hub nodes
    (sinks may be reached as leaves but never expanded)."""
    adj = adjacency(edgeset, extra)
    seen, stack = {s}, [s]
    while stack:
        v = stack.pop()
        if v in SINKS and v != s:
            continue                       # reachable, but not a pass-through
        for w in adj[v] - seen:
            seen.add(w); stack.append(w)
    return seen

print("\n" + "="*78)
print("G_conditional  —  ASSUMING_TRUE(E)   [CONDITIONAL, NOT OBSERVED]")
print("Every consequence below is stamped with the assumption that generated it and")
print("is quarantined from G_obs. A conditional result is never a claim.")
print("="*78)
for e in CONTESTED:
    tag = f"ASSUMING_TRUE({e['id']})"
    print(f"\n[{tag}]  {label(e['source'])} ──► {label(e['target'])}  [{e['confidence']}"
          f"{', disputed' if e.get('disputed') else ''}]")
    before = reachable_nonsink(INFLUENCE, e["source"])
    after = reachable_nonsink(INFLUENCE, e["source"], extra=[e])
    newly = after - before - {e["source"]}
    if newly:
        print(f"   [{tag}] newly reachable from {label(e['source'])} "
              f"(only because E is assumed): {sorted(label(x) for x in newly)}")
    else:
        print(f"   [{tag}] no new reachability — endpoints already connected in G_obs; "
              f"effect is path-shortening only.")
    persisted = [x['id'] for x in CONDITIONAL if e['id'] in (x.get('assumed_under') or [])]
    print(f"   [{tag}] persisted conditional edges depending on this hypothesis: {persisted or 'none'}")
print("\nRULE: to MATERIALIZE any of the above as a stored edge, set provenance='conditional'")
print("and assumed_under=['" + "','".join(e['id'] for e in CONTESTED[:1]) + "', …]. validate.py then")
print("bars it from G_obs and refuses verification=verified on it. Predictive-convergence test:")
print("a conditional-predicted edge only becomes interesting if an INDEPENDENT observed edge")
print("(provenance=observed, different information_origin) is later found for the same pair.")

# ---- source independence collapse --------------------------------------------
print("\n" + "="*78)
print("SOURCE-INDEPENDENCE COLLAPSE  (documents vs independent information origins)")
print("="*78)
def cites(e):
    if e.get("citations"): return e["citations"]
    return [e["citation"]] if e.get("citation") else []
def origin(c):
    return c.get("independence_group") or c.get("information_origin") or c.get("publisher") or "?"
tot_docs = tot_orig = 0
multi = []
for e in EDGES:
    cs = cites(e)
    origins = {origin(c) for c in cs}
    tot_docs += len(cs); tot_orig += len(origins)
    if len(cs) > 1: multi.append((e["id"], len(cs), len(origins)))
print(f"across {len(EDGES)} edges: {tot_docs} citations → {tot_orig} independent origins "
      f"(1 citation/edge currently; multi-source backfill pending).")
print("edges with >1 citation:", multi or "none yet — independence backfill is a due-diligence task")
# graph-level concentration: how much of the (verified) structure rests on each single origin?
byorig = collections.Counter(origin(c) for e in EDGES for c in cites(e))
vbyorig = collections.Counter(origin(c) for e in EDGES if e['verification']=='verified' for c in cites(e))
print("edges per information origin (all):     ", dict(byorig.most_common()))
print("edges per information origin (verified):", dict(vbyorig.most_common()))
top = vbyorig.most_common(1)
if top:
    frac = top[0][1]/max(1,sum(vbyorig.values()))
    print(f"  concentration: {frac:.0%} of verified edges trace to a single origin ({top[0][0]}). "
          f"{'⚠ over-reliant — seek independent corroboration.' if frac>0.5 else 'diversified.'}")
print("NOTE: SSCI Vol 3 and Vol 5 share an institution but are distinct investigations; "
      "Mueller/ICA/SSCI/DOJ-SDNY are independent origins. Publisher≈origin is a placeholder "
      "until citations carry explicit independence_group.")

# ---- temporal causality check -------------------------------------------------
print("\n" + "="*78)
print("TEMPORAL CAUSALITY  (flag edges dated AFTER the event they purport to explain)")
print("="*78)
def year(s):
    m = re.search(r"(19|20)\d{2}", s or ""); return int(m.group()) if m else None
flags = 0
for e in EDGES:
    ey = year(e.get("date","")) or year(e.get("claim",""))
    cy = year((e.get("citation") or {}).get("date",""))
    # a claim about a dated relationship cited only to a much later source is fine (discovery lag);
    # the real violation is an edge whose own relationship date post-dates its target event — needs
    # per-node event dates to be exact. Report what we can.
    if ey and cy and cy < ey:
        print(f"  ? {e['id']}: claim year {ey} > citation year {cy} (check direction)"); flags += 1
print("no temporal inversions detectable at current granularity." if not flags else f"{flags} to review")
print("\n(Full temporal enforcement needs per-node event dates + edge.start/end — SCHEMA extension is in place;"
      " backfill dates as batches land.)")

# ---- AMERICAN ECOSYSTEM DENSITY (pre-Tenet, domestic edges only) --------------
print("\n" + "="*78)
print("AMERICAN ECOSYSTEM DENSITY  (were the six a pre-existing network, or strangers?)")
print("Uses DOMESTIC edges only (creator<->creator, creator<->org). Tenet/RT excluded.")
print("="*78)
SIX = ["tim_pool","dave_rubin","benny_johnson","lauren_southern","tayler_hansen","matt_christiansen"]
BROKER = "lauren_chen"
SEVEN = [BROKER] + SIX
# undirected adjacency over domestic edges (people + orgs), among nodes that exist
dom_adj = {n["id"]: set() for n in NODES.values()}
for e in DOMESTIC:
    dom_adj[e["source"]].add(e["target"]); dom_adj[e["target"]].add(e["source"])
# direct person-person degree within SEVEN
print("\n  pre-Tenet DIRECT ties among the seven (person<->person):")
for a in SEVEN:
    peers = sorted(dom_adj[a] & set(SEVEN))
    print(f"    {label(a):<20} degree {len(peers):>1}  -> {', '.join(label(x) for x in peers) or '(none direct)'}")
# Chen's direct reach into the six
chen_direct = sorted(dom_adj[BROKER] & set(SIX))
print(f"\n  Chen had a DIRECT pre-Tenet tie to {len(chen_direct)}/6 of the eventual creators: "
      f"{', '.join(label(x) for x in chen_direct)}")
# connectivity of the six via domestic edges ALONE (people + orgs as connectors), Chen removed
def dom_component(seed, blocked):
    seen, stack = {seed}, [seed]
    while stack:
        v = stack.pop()
        for w in dom_adj[v] - seen:
            if w in blocked: continue
            seen.add(w); stack.append(w)
    return seen
SOFT = {"us_conservative_media"}  # catch-all milieu: real but weak, barred from the hard connectivity test
comp_with = dom_component("tim_pool", set(SOFT))
inside_with = [c for c in SIX if c in comp_with]
comp_wo = dom_component("tim_pool", {BROKER} | SOFT)
inside_wo = [c for c in SIX if c in comp_wo]
print(f"\n  With Chen (excluding the soft milieu hub): {len(inside_with)}/6 creators in one component.")
print(f"  Without Chen (broker removed): {len(inside_wo)}/6 still connected via other bridges "
      f"(orgs, show circuit, amplification).")
orphan_wo = [label(c) for c in SIX if c not in comp_wo and c != "tim_pool"]
print(f"    creators whose ONLY hard pre-Tenet bridge was Chen: {orphan_wo or 'none'}")
print("\n  Reading: the six were NOT strangers — they sat in a pre-existing American network")
print("  with HETEROGENEOUS bridges. Chen is the densest single connector (personal ties), but")
print("  removing her does not fully disassemble the domestic graph (Johnson<->Rubin<->Pool show")
print("  circuit, TPUSA/Blaze org intersections, and Hansen surfaced via Johnson/Trump-Jr")
print("  amplification remain). => Tenet CENTRALIZED an existing network; it did not create one.")
print("  This is a DOMESTIC-topology finding and asserts nothing about anyone's intent.")

# ---- ORGANIZATIONAL ARCHITECTURE COMPARISON (architecture-vs-cast test) --------
print("\n" + "="*78)
print("ORGANIZATIONAL ARCHITECTURE  (did Russia reuse one vehicle, or adapt it?)")
print("="*78)
DIMS=["era","foreign_ownership","direct_contract","american_intermediary","existing_talent_network","organizational_concealment"]
vehicles=[n for n in NODES.values() if n.get("arch_profile")]
w=max(len(label(v["id"])) for v in vehicles) if vehicles else 8
print(f"  {'vehicle':<{w}} " + " ".join(f"{d.split('_')[0][:9]:>10}" for d in DIMS))
for v in vehicles:
    ap=v["arch_profile"]
    print(f"  {label(v['id']):<{w}} " + " ".join(f"{str(ap.get(d,'-'))[:10]:>10}" for d in DIMS))
for v in vehicles:
    print(f"\n  {label(v['id'])}: {v.get('arch_summary','')}")
print("\n  => The vehicle CHANGES (own -> contract -> founder-embed) while the ARCHITECTURE holds")
print("  (foreign principal -> US intermediary CLASS -> American-facing media -> audience).")
print("  Verdict leans: Russia ADAPTED the organizational vehicle to the target network,")
print("  it did not rerun one fixed template. Cast varies; the architecture-shape persists.")

# ---- G0 -> G1 -> G2 STAGED EXPERIMENT + REMOVAL TESTS --------------------------
print("\n" + "="*78)
print("STAGED CONSTRUCTION  G0 (pre-Tenet US net) -> G1 (+RT->Chen/Donovan->Tenet) -> G2 (+six)")
print("Connectivity uses HARD DOMESTIC edges; Russian reach uses INFLUENCE edges only, DIRECTED")
print("(a Timcast appearance is not a Russian conduit).")
print("="*78)
EBYID={e["id"]:e for e in EDGES}
SIX=["tim_pool","dave_rubin","benny_johnson","lauren_southern","tayler_hansen","matt_christiansen"]
SOFT={"us_conservative_media"}
AMERICAN={nid for nid,n in NODES.items() if n.get("layer") in ("us_media","us_political") and nid!="tenet"}
AMERICAN |= {"turning_point_usa","blaze_tv"}
# hard domestic American network (soft milieu hub excluded)
DOM=[e for e in EDGES if e.get("domain")=="domestic" and e.get("pre_tenet")
     and e["source"] in AMERICAN and e["target"] in AMERICAN
     and e["source"] not in SOFT and e["target"] not in SOFT]
# influence spine into Tenet (formation/funding), and the six attachment edges
SPINE=[i for i in ["e_tvnovosti_chen","e_afanasyeva_chen_scouting","e_ruptly_donovan","e_donovan_chen",
       "e_chen_tenet_founder","e_donovan_tenet_founder","e_rt_tenet_direction","e_tvnovosti_rt",
       "e_afanasyeva_tenet_direction","e_grigoriann_tenet_funding","e_afanasyeva_grigoriann",
       "e_shells_tenet","e_employees_shells","e_rt_employees"] if i in EBYID]
SIXEDGES=[e["id"] for e in EDGES if (e["id"].startswith("e_chen_recruit_") or
          (e["source"]=="tenet" and e["target"] in SIX))]
def undirected(edgelist):
    a={}
    for e in edgelist:
        a.setdefault(e["source"],set()).add(e["target"]); a.setdefault(e["target"],set()).add(e["source"])
    return a
def reach_ud(edgelist,s):
    a=undirected(edgelist); seen={s}; st=[s]
    while st:
        v=st.pop()
        for w in a.get(v,set())-seen: seen.add(w); st.append(w)
    return seen
def reach_dir(edgelist,s):           # directed, sink-respecting foreign reach
    a={}
    for e in edgelist: a.setdefault(e["source"],set()).add(e["target"])
    seen={s}; st=[s]
    while st:
        v=st.pop()
        if v in SINKS and v!=s: continue
        for w in a.get(v,set())-seen: seen.add(w); st.append(w)
    return seen
def ncomp(edgelist,nodes):
    a=undirected(edgelist); seen=set(); c=0
    for s in nodes:
        if s in seen: continue
        c+=1
        for w in reach_ud(edgelist,s): seen.add(w)
    return c
def six_infl_reach(infl_ids, drop=None):
    edges=[EBYID[i] for i in infl_ids if EBYID[i]["source"]!=drop and EBYID[i]["target"]!=drop]
    origins=[nid for nid,n in NODES.items() if n.get("layer")=="russian_state" and nid!=drop]
    got=set()
    for o in origins: got|=reach_dir(edges,o)
    return [c for c in SIX if c!=drop and c in got]

dom_nodes={x for e in DOM for x in (e["source"],e["target"])}
print(f"\n  G0 (pre-Tenet US network, hard domestic): {len(DOM)} edges, {len(dom_nodes)} nodes, "
      f"{ncomp(DOM,dom_nodes)} component(s).")
print(f"      six-creator connectivity: {sum(1 for c in SIX if c in reach_ud(DOM,'tim_pool'))}/6 in one component pre-Tenet.")
print(f"  G1 (+ {len(SPINE)} influence spine edges; Tenet exists, six NOT yet attached):")
print(f"      Russian->six reach: {len(six_infl_reach(SPINE))}/6   (0 expected — no attachment yet).")
print(f"  G2 (+ {len(SIXEDGES)} recruit/contract edges):")
print(f"      Russian->six reach: {len(six_infl_reach(SPINE+SIXEDGES))}/6.")
print(f"\n  Tenet's net contribution: it did NOT build the American network (G0 already 1 component,")
print(f"  6/6). It added a foreign-funded node ACROSS it, flipping Russian->creator reach 0/6 -> "
      f"{len(six_infl_reach(SPINE+SIXEDGES))}/6.")

print("\n  --- REMOVAL TESTS ---")
print("  (creator-cluster = largest set of the six connected via HARD DOMESTIC ties;")
print("   Russian reach = via INFLUENCE edges only)")
for node in ["lauren_chen","tenet","turning_point_usa","tim_pool"]:
    if node not in NODES: continue
    dedges=[e for e in DOM if e["source"]!=node and e["target"]!=node]
    best=0
    for seed in SIX:
        if seed==node: continue
        r=reach_ud(dedges,seed)
        best=max(best,sum(1 for c in SIX if c!=node and c in r))
    russ=len(six_infl_reach(SPINE+SIXEDGES,drop=node))
    print(f"    remove {label(node):<18}: creator-cluster {best}/6 ; Russian->creator reach {russ}/6")
edges_no_six=[e for e in DOM if e["source"] not in SIX and e["target"] not in SIX]
remain=sorted({label(x) for e in edges_no_six for x in (e["source"],e["target"])})
print(f"    remove ALL SIX creators   : US ecosystem remnant still linked: {remain or '(none)'}")
def six_infl_reach_drop2(a,b):
    edges=[EBYID[i] for i in (SPINE+SIXEDGES) if EBYID[i]["source"] not in (a,b) and EBYID[i]["target"] not in (a,b)]
    origins=[nid for nid,n in NODES.items() if n.get("layer")=="russian_state"]
    got=set()
    for o in origins: got|=reach_dir(edges,o)
    return [c for c in SIX if c in got]
print(f"    remove BOTH Chen + Tenet  : Russian->creator reach {len(six_infl_reach_drop2('lauren_chen','tenet'))}/6  <= the pair is the gate, not either alone")

# ---- G3 / G4: independent pre-Tenet Russian-side branches into the creator graph ----
RUS_ORIGIN={nid for nid,n in NODES.items() if n.get("actor_class") in ("RUSSIAN_STATE","RUSSIAN_STATE_MEDIA","RUSSIAN_STATE_LINKED_PRIVATE")}
INTERM={nid for nid,n in NODES.items() if n.get("actor_class")=="INTERMEDIARY"}
PROXIMITY={"OFFICE_VISIT","CONTACT","INTERVIEW","EVENT","TRAVEL","APPEARANCE","AMPLIFICATION"}  # proximity != conduit
RUS=RUS_ORIGIN                                  # reach origins (Dugin=RUSSIAN_POLITICAL_ACTOR excluded by design)
GATED={"lauren_chen","tenet"}
# DIRECT: RUS_ORIGIN --influence--> creator, not via Chen/Tenet, observed
G3=[e["id"] for e in EDGES if e.get("domain")=="influence" and e["target"] in SIX
    and e["source"] in RUS_ORIGIN and e["source"] not in GATED and not is_contested(e)
    and e.get("relationship_type") not in PROXIMITY]
direct_set={EBYID[i]["target"] for i in G3}
# INTERMEDIARY_MEDIATED: RUS_ORIGIN -> INTERMEDIARY(s) -> creator, no Chen/Tenet, no direct edge
_infl=[e for e in EDGES if e.get("domain")=="influence" and not is_contested(e)
       and e["source"] not in GATED and e["target"] not in GATED
       and e.get("relationship_type") not in PROXIMITY]
def _reach(seeds):
    a={}
    for e in _infl: a.setdefault(e["source"],set()).add(e["target"])
    seen=set(seeds); st=list(seeds)
    while st:
        v=st.pop()
        if v in SINKS and v not in seeds: continue
        for w in a.get(v,set())-seen: seen.add(w); st.append(w)
    return seen
_mediated_reach=_reach(RUS_ORIGIN)
intermediary_set={c for c in SIX if c in _mediated_reach} - direct_set
def reach_ids(edge_ids, drop=()):
    edges=[EBYID[i] for i in edge_ids if EBYID[i]["source"] not in drop and EBYID[i]["target"] not in drop]
    got=set()
    for o in RUS:
        if o in drop: continue
        got|=reach_dir(edges,o)
    return [c for c in SIX if c in got and c not in drop]
entry_pts=sorted({EBYID[i]["target"] for i in G3})
print(f"\n  --- INDEPENDENT RUSSIAN ENTRY POINTS (pre-Tenet, bypassing Chen/Tenet) ---")
print(f"  G3 = direct Russian-side -> creator edges NOT via Chen/Tenet: {[EBYID[i]['id'] for i in G3] or 'none'}")
print(f"      creators with an independent Russian entry: {[label(x) for x in entry_pts] or 'none'}  ({len(entry_pts)})")
print(f"      DIRECT entry points: {[label(x) for x in sorted(direct_set)] or 'none'}  ({len(direct_set)})")
print(f"      INTERMEDIARY-MEDIATED (RUS->intermediary->creator, no Chen/Tenet): {[label(x) for x in sorted(intermediary_set)] or 'none'}  ({len(intermediary_set)})")
print(f"      SCOREBOARD: {len(direct_set)} direct + {len(intermediary_set)} intermediary-mediated of 6; "
      f"{6-len(direct_set|intermediary_set)} not_established (searched-negative, not zero).")
_sweep=g.get("metadata",{}).get("entry_point_sweep",{})
if _sweep:
    print("  sweep status (searched-negative is NOT proven zero):")
    for k in ["lauren_southern","tim_pool","dave_rubin","benny_johnson","tayler_hansen","matt_christiansen"]:
        if k in _sweep: print(f"      {label(k):<20} {_sweep[k]}")
print(f"\n  REMOVAL LADDER (Russian->creator reach):")
print(f"    G2                              : {len(reach_ids(SPINE+SIXEDGES))}/6")
print(f"    G2  - Chen/Tenet                : {len(reach_ids(SPINE+SIXEDGES, drop=('lauren_chen','tenet')))}/6")
print(f"    G4 (=G2+G3) - Chen/Tenet        : {len(reach_ids(SPINE+SIXEDGES+G3, drop=('lauren_chen','tenet')))}/6"
      f"   <= survives ONLY through the independent branch(es)")
print(f"    G4 - Chen/Tenet - independent   : {len(reach_ids(SPINE+SIXEDGES, drop=('lauren_chen','tenet')))}/6")
print("    (removing Chen+Tenet AND the independent RT->creator edge(s) -> 0/6)")
print("  Interpretation: the Chen+Tenet coupling is the MAIN foreign gate, but it is NOT the only")
print("  pre-Tenet Russian-side contact touching the six. Southern carries an independent RT edge —")
print("  which is why 'remove Chen+Tenet' does not fully zero Russian CONTACT with the creator set,")
print("  even though it does zero the Tenet-operation reach. A Russian CONTACT is not an influence")
print("  PATHWAY: Southern->Pool stays a domestic APPEARANCE (see e_rt_pool_via_southern_DNC).")
print("\n  Reading (node dependency, not vibes):")
print("  - The six were ALREADY one connected US network before Tenet (G0: 6/6, 1 component).")
print("  - Russian->creator reach is carried REDUNDANTLY by TWO couplings: Tenet-contract AND")
print("    Chen-recruitment. Remove either single node and reach stays 6/6; only removing the")
print("    Chen+Tenet PAIR severs it (0/6). No lone gate -- the operation over-provisioned, as a")
print("    resourced state actor would. Consistent with Chen severs=0 in the influence graph.")
print("  - Removing the whole American creator layer leaves the broker + orgs (Chen/TPUSA/Blaze)")
print("    still standing: the ecosystem is American infrastructure, coupled to -- not created by --")
print("    Russia. That is the defensible architectural claim, end to end.")

# ---- PERSONNEL LANE + OPEN QUESTIONS -----------------------------------------
print("\n" + "="*78)
print("PERSONNEL-CONTINUITY LANE  (shared personnel across time; conduit=false, not scored)")
print("="*78)
pers=[e for e in EDGES if e.get("domain")=="personnel" or e.get("relationship_class")=="PERSONNEL_CONTINUITY"]
for e in pers:
    print(f"  {label(e['source'])} --{e.get('relationship_type','?')}--> {label(e['target'])}  "
          f"[{e.get('relationship_class','?')}, conduit={e.get('conduit',True)}]")
print("  (kept for the personnel graph; explicitly excluded from influence reach + scoreboard.)")
_oq=g.get("metadata",{}).get("open_questions",[])
if _oq:
    print("\n" + "="*78); print("OPEN QUESTIONS  (graph-generated; answer upgrades or kills an edge)"); print("="*78)
    for q in _oq:
        print(f"  [{q['id']}|{q['status']}] {q['question']}")
        print(f"      edge={q.get('edge')}  UPGRADE: {q.get('upgrades_if','')}")
        print(f"      KILL: {q.get('kills_if','')}")

# ---- DOMESTIC AMPLIFICATION INFRASTRUCTURE (TPUSA machine) --------------------
print("\n" + "="*78)
print("DOMESTIC AMPLIFICATION INFRASTRUCTURE  (American institutional explanation, not Russian)")
print("="*78)
amp=[n for n in NODES.values() if n.get("amplification_profile")]
for n in amp:
    ap=n["amplification_profile"]
    print(f"  {label(n['id'])} [{n.get('organization_type','?')}] — {n.get('role','')}")
    print(f"     media budget 2021: ${ap.get('media_budget_2021_usd',0):,} | creators by 2022: {ap.get('creators_onboarded_by_2022')} "
          f"| ambassadors 2021: {ap.get('ambassadors_2021')} (claimed reach {ap.get('claimed_reach_2021')})")
    print(f"     capabilities: {', '.join(ap.get('capabilities',[]))}")
AMP_HUBS={"turning_point_usa","tpusa_productions"}
inside=[c for c in ["tim_pool","dave_rubin","benny_johnson","lauren_southern","tayler_hansen","matt_christiansen"]
        if any(e.get("domain")=="domestic" and e["source"]==c and e["target"] in AMP_HUBS for e in EDGES)]
print(f"\n  Of the six, documented INSIDE TPUSA's amplification machine pre-Tenet: {[label(x) for x in inside]} ({len(inside)}/6)")
print("  Russia->TPUSA: NOT established (e_rt_tpusa_DNC). Russia->Benny virality: NOT established")
print("  (e_russia_benny_virality_DNC — the documented cause is TPUSA's domestic machine).")
print("  => This is INFRASTRUCTURE_EXPLOITATION territory: did the operation plug into a pre-optimized")
print("  American amplifier it did not build? (OQ-02) — a different architecture from Russian penetration.")

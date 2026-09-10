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

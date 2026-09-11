#!/usr/bin/env python3
"""One-time, idempotent schema normalization. Brings every node/edge to the full
current schema uniformly (kills mid-build field drift). Re-runnable. Preserves all
analytical decisions (confidence, verification, do_not_claim, disputed, provenance).
Derived fields (evidence_quality, date) are auto-filled by explicit rule and are
REVIEWABLE — see AUTO markers in output."""
import json, re, pathlib, collections
p = pathlib.Path(__file__).parent / "graph.json"
g = json.load(open(p))

def indep_group(pub):
    s = (pub or "").lower()
    if "sdny" in s: return "DOJ-SDNY"
    if "special counsel" in s or "mueller" in s: return "DOJ-SCO(Mueller)"
    if "intelligence community" in s or "ica" in s: return "USIC-ICA"
    if "senate select committee" in s: return "SSCI"
    if "senate judiciary" in s: return "SJC"
    if "associated press" in s or s=="ap news" or "ap news" in s: return "AP"
    if "washington post" in s: return "WaPo"
    if "los angeles" in s: return "LAT"
    if "pbs" in s: return "PBS"
    if "npr" in s: return "NPR"
    if "dfrlab" in s: return "DFRLab"
    if "doj" in s or "department of justice" in s: return "DOJ"
    return pub or "?"

MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"
def parse_date(text):
    t = text or ""
    m = re.search(rf"({MONTHS})\s+(\d{{1,2}}),\s*((?:19|20)\d{{2}})", t)
    if m: return f"{m.group(3)}-{'%02d'%(MONTHS.split('|').index(m.group(1))+1)}-{int(m.group(2)):02d}"
    m = re.search(rf"({MONTHS})\s+((?:19|20)\d{{2}})", t)
    if m: return f"{m.group(2)}-{'%02d'%(MONTHS.split('|').index(m.group(1))+1)}"
    m = re.search(r"(?:early |late |mid )?((?:19|20)\d{2})", t)
    if m: return m.group(1)
    return None

def evidence_quality(e, primary, disputed):
    if e["confidence"] == "do_not_claim": return "N/A"      # negative finding
    if e["confidence"] == "low": return "D"                  # attempted/speculative
    if disputed: return "C"                                   # contested caps quality
    if primary and e.get("verification") == "verified": return "A"  # primary + confirmed
    if primary: return "B"                                    # primary, not yet confirmed
    return "C"                                                # secondary/journalism

auto_dates = auto_q = 0
def _cites(e):
    return e.get("citations") or ([e["citation"]] if e.get("citation") else [])

def evidence_state(e):
    """Authoritative evidence classification. An audit-assigned e['evidence_state']
    ALWAYS wins; otherwise a provisional state is derived from current fields."""
    if e.get("evidence_state"): return e["evidence_state"]
    c, v = e["confidence"], e["verification"]
    if c == "do_not_claim": return "negative_finding"
    if e.get("disputed") or e.get("provenance") == "contested": return "contested"
    if e.get("provenance") == "conditional": return "conditional"
    cits = _cites(e)
    prim = any(x.get("primary") for x in cits)
    origins = {x.get("independence_group") for x in cits if x.get("independence_group")}
    if v == "verified":
        if prim: return "primary_verified"
        if len(origins) >= 2: return "multi_source_verified"
        return "reported"
    return "reported"                      # needs_primary / pending

def derive_publication(e):
    """DETERMINISTIC publication classification. The renderer consumes this; it never
    decides evidentiary status. do_not_claim reaches public_core ONLY with provenance."""
    st = evidence_state(e)
    has_prov = any(x.get("url") for x in _cites(e))
    if st in ("primary_verified", "multi_source_verified"):
        return {"layer": "public_core", "eligible": True, "reason": [st]}
    if st == "negative_finding":
        if has_prov:
            return {"layer": "public_core", "eligible": True, "reason": ["do_not_claim_with_provenance"]}
        return {"layer": "research_graph", "eligible": False, "reason": ["do_not_claim_missing_provenance"]}
    if st in ("reported", "contested"):
        return {"layer": "evidence_ledger", "eligible": False, "reason": [st]}
    return {"layer": "research_graph", "eligible": False, "reason": [st]}   # conditional/searched_negative/cut

for e in g["edges"]:
    e.setdefault("provenance", "observed")
    # citation -> citations[] with independence_group (canonical: citations[])
    cits = e.get("citations") or ([e["citation"]] if e.get("citation") else [])
    for c in cits:
        c.setdefault("independence_group", indep_group(c.get("publisher")))
    if cits:
        e["citations"] = cits
        e["citation"] = cits[0]     # keep singular mirror for any old reader
    # date (AUTO from claim; reviewable)
    if not e.get("date"):
        d = parse_date(e.get("claim","")) or parse_date((e.get("citation") or {}).get("date",""))
        if d: e["date"] = d; auto_dates += 1
    # evidence_quality (AUTO by rule; reviewable)
    primary = bool((cits[0].get("primary") if cits else False))
    e["evidence_quality"] = evidence_quality(e, primary, e.get("disputed"))
    auto_q += 1
    # evidence_state (provisional unless audit-assigned) + DERIVED publication classification
    e["evidence_state"] = evidence_state(e)
    for k in ("claim_scope", "identity_check", "temporal_check"):
        e.setdefault(k, "unaudited")
    e["publication"] = derive_publication(e)

# node hygiene: ensure optional keys exist consistently
for n in g["nodes"]:
    n.setdefault("us_class", None)

g["metadata"]["schema_version"] = "1.0"
g["metadata"]["legends"].setdefault("evidence_quality", ["A","B","C","D","N/A"])
g["metadata"]["legends"].setdefault("evidence_state", ["primary_verified","multi_source_verified","reported","contested","conditional","negative_finding","searched_negative","cut"])
g["metadata"]["legends"].setdefault("publication_layer", ["public_core","evidence_ledger","research_graph"])
g["metadata"]["legends"].setdefault("claim_scope", ["exact","narrower_than_source","broader_than_source","unaudited"])
g["metadata"]["legends"].setdefault("identity_check", ["exact_person","pseudonym_binding","ambiguous","n_a","unaudited"])
g["metadata"]["legends"].setdefault("temporal_check", ["supported","partially_supported","unsupported","unaudited"])
g["metadata"]["normalized"] = "2026-09-10 — schema frozen at 1.0; fields uniform across all edges/nodes."
json.dump(g, open(p,"w"), indent=2, ensure_ascii=False)
print(f"normalized {len(g['edges'])} edges / {len(g['nodes'])} nodes to schema 1.0")
print(f"  provenance: explicit on all; citations[]: uniform; independence_group: filled")
print(f"  AUTO date parsed on {auto_dates} edges; AUTO evidence_quality on {auto_q} (both reviewable)")
print("  evidence_quality:", dict(collections.Counter(e["evidence_quality"] for e in g["edges"])))

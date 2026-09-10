#!/usr/bin/env python3
"""Validate graph.json and print the due-diligence surface.

Run:  python3 graph/validate.py
Exit non-zero on structural errors (missing endpoints, uncited edges, bad enums).
The "IFFY SURFACE" section is the due-diligence worklist, not an error.
"""
import json, sys, collections, pathlib

HERE = pathlib.Path(__file__).parent
g = json.load(open(HERE / "graph.json"))
nodes, edges = g["nodes"], g["edges"]
L = g["metadata"]["legends"]
ids = {n["id"] for n in nodes}
errors = []

# ---- structural integrity -------------------------------------------------
seen = set()
for n in nodes:
    if n["id"] in seen: errors.append(f"duplicate node id: {n['id']}")
    seen.add(n["id"])
    if n["layer"] not in L["layer"]: errors.append(f"{n['id']}: bad layer {n['layer']}")
    if n.get("us_class") not in L["us_class"]: errors.append(f"{n['id']}: bad us_class {n.get('us_class')}")

eids = set()
for e in edges:
    if e["id"] in eids: errors.append(f"duplicate edge id: {e['id']}")
    eids.add(e["id"])
    for end in ("source", "target"):
        if e[end] not in ids: errors.append(f"{e['id']}: {end} '{e[end]}' not a node")
    if e["evidence_class"] not in L["evidence_class"]: errors.append(f"{e['id']}: bad evidence_class")
    if e["confidence"] not in L["confidence"]: errors.append(f"{e['id']}: bad confidence")
    if e["verification"] not in L["verification"]: errors.append(f"{e['id']}: bad verification")
    _cites = e.get("citations") or ([e["citation"]] if e.get("citation") else [])
    if e["confidence"] != "do_not_claim" and not (_cites and _cites[0].get("url")):
        errors.append(f"{e['id']}: non-do_not_claim edge has no citation url")
    # ---- ASSUMING_TRUE firewall ----
    prov = e.get("provenance", "observed")
    if prov not in ("observed", "conditional", "contested"):
        errors.append(f"{e['id']}: bad provenance {prov}")
    if prov == "conditional":
        au = e.get("assumed_under")
        if not au or not isinstance(au, list):
            errors.append(f"{e['id']}: conditional edge must carry assumed_under=[hypothesis edge ids]")
        else:
            for h in au:
                if h not in eids and h not in {x['id'] for x in edges}:
                    errors.append(f"{e['id']}: assumed_under references unknown edge '{h}'")
        if e.get("verification") == "verified":
            errors.append(f"{e['id']}: CONTAMINATION — a conditional edge may never be verification=verified")

print(f"nodes: {len(nodes)}   edges: {len(edges)}")
print("confidence   :", dict(collections.Counter(e["confidence"] for e in edges)))
print("verification :", dict(collections.Counter(e["verification"] for e in edges)))
print("evidence     :", dict(collections.Counter(e["evidence_class"] for e in edges)))
print("provenance   :", dict(collections.Counter(e.get("provenance","observed") for e in edges)))

# ---- iffy surface (the due-diligence worklist) ----------------------------
print("\n=== IFFY SURFACE (work these before publish) ===")
strong_unverified = [e["id"] for e in edges
                     if e["confidence"] in ("very_high", "high") and e["verification"] != "verified"]
print(f"strong claims not yet verified ({len(strong_unverified)}):")
for x in strong_unverified: print("   ", x)

needs_primary = [e["id"] for e in edges if e["verification"] == "needs_primary"]
print(f"\nresting on secondary/press-release, want primary doc ({len(needs_primary)}):")
for x in needs_primary: print("   ", x)

secondary_cites = [e["id"] for e in edges if not e.get("citation", {}).get("primary", True)]
print(f"\nedges citing a non-primary source ({len(secondary_cites)}):")
for x in secondary_cites: print("   ", x)

used = set()
for e in edges: used |= {e["source"], e["target"]}
dangling = sorted(ids - used)
print(f"\nroster nodes awaiting edges from incoming research ({len(dangling)}):")
print("   ", dangling or "none")

disputed = [e["id"] for e in edges if e.get("disputed")]
print(f"\ndisputed/contested edges (preserved, must stay): {disputed or 'none'}")
print(f"do_not_claim negative findings (must stay): {[e['id'] for e in edges if e['confidence']=='do_not_claim']}")

if errors:
    print("\n!!! STRUCTURAL ERRORS:")
    for e in errors: print("   ", e)
    sys.exit(1)
print("\nOK — structurally valid.")

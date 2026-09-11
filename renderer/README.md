# Renderer — Russia→US influence evidence graph

A deliberately **dumb-about-epistemology** viewer. It reads the repo's canonical
`../graph/graph.json` at runtime and displays it. `publication.layer` is authoritative —
the renderer shows it, it never decides it. No inlined edge data, no copied source URLs,
no hard-coded people, no second taxonomy.

**Invariant:** change the evidence graph → the renderer changes automatically. The published
artifact cannot quietly drift from the audited research graph.

## Run it

Browsers block `file://` fetches, so serve over http from the **repo root**:

```
python3 -m http.server 8000
```

then open **http://localhost:8000/renderer/index.html**

## What it shows

- **Default = PUBLIC CORE**: `primary_verified` + `multi_source_verified` + `do_not_claim`
  (negative findings, kept and drawn dashed/neutral).
- **+ EVIDENCE LEDGER** (toggle): `reported` + `contested` — visually subordinate.
- **+ RESEARCH / CONDITIONAL** (toggle): everything else; hidden by default.

Edge styling never implies more than the metadata: primary=solid green, multi-source=solid
blue, contested=dashed amber, not-established=dashed grey, reported=dotted. Left→right lanes
follow the architecture: foreign principal → intermediary → American-facing → audience.

## Three views

- **Graph** — force-directed; click any node or edge. The edge inspector shows the claim,
  evidence state, the exact primary document / section / page / supporting quote, the three
  audit checks (scope / identity / temporal), any contradiction, and an **Open primary** link.
- **Architecture-vs-cast** — the nine-vehicle table (the argument's front door): the
  intermediary *class* changes across eras while the *shape* holds. Contracted U.S. firms are
  marked as non-vehicles (the negative controls).
- **What we do NOT claim** — every preserved `do_not_claim` boundary with its source.

## Provenance
`graph/graph.json` is the single source of truth (see `graph/SCHEMA.md`). Regenerate nothing;
the renderer maps the existing schema directly.

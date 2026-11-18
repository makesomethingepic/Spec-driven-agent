#!/usr/bin/env python3
"""Checks shared agent state: handoffs, status.json, cost ledger and file ownership."""
import glob, json, sys

errors = []
HANDOFF_KEYS = {"handoff_id", "product", "from_agent", "to_agent", "stage", "trace",
                "inputs", "outputs_expected", "done_when", "constraints", "gate", "status"}
STATUS_KEYS = {"product", "function", "pm", "health", "stage", "cost", "security", "quality"}


def load(path):
    try:
        return json.load(open(path))
    except Exception as e:
        errors.append(f"{path}: {e}")


for path in glob.glob(".agent-state/handoffs/*.json"):
    doc = load(path)
    if doc is not None and (missing := HANDOFF_KEYS - doc.keys()):
        errors.append(f"{path}: missing {sorted(missing)}")

doc = load(".agent-state/status.json")
if doc is not None and (missing := STATUS_KEYS - doc.keys()):
    errors.append(f"status.json: missing {sorted(missing)}")

for n, line in enumerate(open(".agent-state/cost-ledger.jsonl"), 1):
    if line.strip():
        try:
            json.loads(line)
        except Exception as e:
            errors.append(f"cost-ledger.jsonl:{n}: {e}")

import yaml
omap = yaml.safe_load(open("05-plan/ownership-map.yml")) or {}
owned = [(feat, p.rstrip("*").rstrip("/")) for feat, paths in
         {**(omap.get("features") or {}), "shared": omap.get("shared") or []}.items()
         for p in paths]
for i, (fa, pa) in enumerate(owned):
    for fb, pb in owned[i + 1:]:
        if fa != fb and (pa == pb or pa.startswith(pb + "/") or pb.startswith(pa + "/")):
            errors.append(f"ownership-map.yml: {fa}:{pa} overlaps {fb}:{pb}")

print("\n".join(errors) or "agent state OK")
sys.exit(1 if errors else 0)

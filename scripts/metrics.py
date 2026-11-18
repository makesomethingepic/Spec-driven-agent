#!/usr/bin/env python3
"""Nightly delivery metrics from GitHub (needs the gh CLI, GH_TOKEN and GH_REPO).

Covers what can be counted directly. Lead time, change failure rate, time in stage and
cycle time need issue timeline events; add them once the pilot has real data.
"""
import collections, datetime, json, os, subprocess


def gh(*args):
    return json.loads(subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout or "[]")


issues = gh("issue", "list", "--state", "all", "--limit", "1000",
            "--json", "number,state,labels,createdAt,closedAt")
labels = lambda i: {l["name"] for l in i["labels"]}
open_issues = [i for i in issues if i["state"] == "OPEN"]


def hours(i):
    t = lambda s: datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))
    return (t(i["closedAt"]) - t(i["createdAt"])).total_seconds() / 3600


incidents = [i for i in issues if "incident" in labels(i) and i["closedAt"]]
deploys = gh("run", "list", "--workflow", "deploy.yml", "--status", "success", "--limit", "200",
             "--json", "createdAt")
cost = collections.defaultdict(float)
for line in open(".agent-state/cost-ledger.jsonl"):
    if line.strip():
        row = json.loads(line)
        cost[row.get("FEAT") or row.get("feat") or "none"] += float(row.get("USD") or row.get("usd") or 0)

print(json.dumps({
    "repo": os.environ.get("GH_REPO"),
    "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "deployments": {"count": len(deploys), "dates": [d["createdAt"] for d in deploys]},
    "time_to_restore_hours_avg": round(sum(map(hours, incidents)) / len(incidents), 1) if incidents else None,
    "blocked_items": sum("blocked" in labels(i) for i in open_issues),
    "open_by_stage": dict(collections.Counter(
        l for i in open_issues for l in labels(i) if l.startswith("stage:"))),
    "change_requests": sum("type:cr" in labels(i) for i in issues),
    "cost_usd_by_feature": dict(cost),
}, indent=2))

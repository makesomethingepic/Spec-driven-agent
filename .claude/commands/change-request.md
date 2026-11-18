---
description: Start a spec change request
argument-hint: <what changed and why>
---
Start the change-request workflow for: $ARGUMENTS

1. Delegate to the `spec` sub-agent to write 03-spec/change-requests/CR-###.md:
   affected REQ/AC, Features and tests, cost and timeline impact, proposed semver bump.
2. Pause only the affected Features (label them blocked) and keep the rest running.
3. Open a PR with the CR and the spec diff, labelled type:cr, for PM and stakeholder
   approval. After it merges, delegate to `planning` to re-plan affected issues.

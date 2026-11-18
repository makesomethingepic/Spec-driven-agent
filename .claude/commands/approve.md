---
description: Record a human gate approval (G1-G8 or a stopping point named in the spec)
argument-hint: <gate> [note]
---
A human is approving gate: $ARGUMENTS

1. Confirm the gate is currently pending and its outputs meet the handoff's done_when.
   If not, say what is missing and do not record the approval.
2. Check the approver against spec section 9 (or CODEOWNERS before the spec exists).
   For G5 and G7 the approval is the PR review and merge; point to the PR instead.
3. Record it: set the handoff's gate.status to "approved" with approver and date, swap
   the issue label gate:<G#>-pending for gate:<G#>-approved, update status.json.
4. Start the next stage with a new handoff.

Only run this when a human typed the command. Never invoke it yourself.

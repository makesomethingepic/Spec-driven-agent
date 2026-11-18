# Spec-Driven Delivery Agent — product repo template

One orchestrator agent runs each product in Claude Code against its own GitHub repo.
15 sub-agents each own a stage. Humans approve at 8 gates and merge every pull request.

## Start a new product

1. Create the product repo from this template (one repo per product, grouped by function).
2. Replace the placeholders: `<PRODUCT>` and `<FUNCTION>` in `CLAUDE.md` and
   `.agent-state/status.json`, `<TASK_LIMIT>` in `CLAUDE.md`, and every name in
   `.github/CODEOWNERS`.
3. Run `scripts/bootstrap-labels.sh` to create the stage, gate and type labels.
4. On GitHub: protect `main` (human review, CODEOWNERS approval, passing checks); create a
   `production` environment with a required reviewer; add the `ANTHROPIC_API_KEY` secret;
   give agents a fine-grained token with code and issue write access and no admin rights.
5. Turn on Claude Code sandboxing with an approved network list.
6. Fill in the `TODO` steps in `.github/workflows/` for the product's stack.

## Drive it

| Command | What it does |
|---------|--------------|
| `/intake <notes>` | Turns meeting notes into scored ideas, bugs or enhancements |
| `/approve <gate>` | Records a human gate approval and starts the next stage |
| `/change-request <what and why>` | Starts a spec change request |
| `/status` | Publishes the PM report now |

## Lifecycle

| # | Stage | Agent | Output | Gate |
|---|-------|-------|--------|------|
| 0 | Capture | intake | `00-intake/ideas/` | — |
| 1 | Triage | intake | `00-intake/triage-log.md` | G1: PM |
| 2 | Discovery | requirements | `01-discovery/` | G2: stakeholder |
| 3 | Prototype | prototype | `02-prototype/` | G3: stakeholder + PM |
| 4 | Spec | spec | `03-spec/spec.md` | G4: PM, stakeholder, parties in the spec |
| 5 | Design | architecture | `04-design/` | G5: architect approves the PR |
| 6 | Plan | planning | `05-plan/`, GitHub issues | G6: PM |
| 7 | Build | builder (one per Feature) | `src/`, `tests/`, PRs | G7: a human merges every PR |
| 8 | Verify | test, ai-eval, security | `tests/reports/`, `evals/` | Part of G7 |
| 9 | Integrate | integration | `release/<version>` branch | — |
| 10 | Release | release | `06-release/` | G8: PM + stakeholder |
| 11 | Operate | ops | `07-operate/` | Incidents go to the PM |
| 12 | Improve or retire | ops, intake | Back to stage 0 | PM decides |

The cost and status agents run across every stage. Shared state lives in `.agent-state/`:
one JSON file per handoff (see `handoffs/EXAMPLE.json`), `status.json` for the PM
dashboard, the cost ledger, the decisions log and escalations.

## Guardrails

- `.claude/settings.json` blocks pushes to `main`, force pushes, PR merges, reading
  secrets, and edits to workflows, CODEOWNERS and the settings file itself.
- `ci` checks handoff and status files, file-ownership overlap and trace IDs in PR titles.
- `deploy` runs only when a human starts it on `main`, through the `production` environment.
- Synthetic or masked data only, in `tests/fixtures/synthetic/`.

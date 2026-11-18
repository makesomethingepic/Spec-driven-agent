#!/usr/bin/env bash
# Creates the labels the agents rely on. Run once per product repo: scripts/bootstrap-labels.sh
set -euo pipefail
mk() { gh label create "$1" --color "$2" --force >/dev/null && echo "$1"; }
for n in $(seq 0 12); do mk "stage:$n" 0366d6; done
for g in 1 2 3 4 5 6 7 8; do mk "gate:G$g-pending" fbca04; mk "gate:G$g-approved" 0e8a16; done
for t in idea bug enhancement cr; do mk "type:$t" 5319e7; done
for s in 1 2 3 4; do mk "severity:$s" d93f0b; done
mk blocked b60205; mk incident b60205

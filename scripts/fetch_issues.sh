#!/usr/bin/env bash
# Fetch all public issues of the STS repo into one JSON array.
set -euo pipefail
REPO=eu-digital-identity-wallet/eudi-doc-standards-and-technical-specifications
OUT=${1:-data/issues.json}
mkdir -p "$(dirname "$OUT")"
gh api --paginate --slurp "repos/$REPO/issues?state=all&per_page=100" | python3 -c 'import json,sys; json.dump([i for p in json.load(sys.stdin) for i in p], sys.stdout)' > "$OUT"

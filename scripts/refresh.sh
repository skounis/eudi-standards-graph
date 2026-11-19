#!/usr/bin/env bash
# Fetch the public issues and rebuild site/graph.json.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p data
bash scripts/fetch_issues.sh data/issues.json
python3 scripts/build_graph.py data/issues.json data/graph-full.json "$(date +%F)"
python3 scripts/slim.py data/graph-full.json site/graph.json
echo "Updated site/graph.json"

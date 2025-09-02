#!/usr/bin/env bash
# dev-start-simple.sh : Poetry + healthcheck を一発実行
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

echo "▶ deps: poetry install"
poetry install

echo "▶ healthcheck"
# 好きな方を使う：bash版 or python版
if [ -f tools/healthcheck.sh ]; then
  bash tools/healthcheck.sh
elif [ -f tools/healthcheck.py ]; then
  poetry run python tools/healthcheck.py
else
  echo "healthcheck が見つかりません (tools/healthcheck.sh|.py)" >&2
  exit 1
fi

echo "✅ done"
#!/bin/zsh
# dev-start-simple.sh
# シンプル版：Poetry + healthcheck だけ

echo "🚀 開発環境をスタートします (シンプル版)..."

poetry install

echo "🩺 Running healthcheck..."
poetry run python tools/healthcheck.py

echo "✅ 準備完了！開発を始めてください。"
#!/usr/bin/env bash
# R1/R6: 10分以内に始める・初心者でも実行可能
set -e  # R7: 途中失敗で止めて壊れた状態を作らない

# R3: pyenv/Poetry/Gitが使えるかチェック
if ! command -v pyenv >/dev/null 2>&1; then echo "[x] pyenv が見つかりません"; exit 1; fi  # R3
if ! command -v poetry >/dev/null 2>&1; then echo "[x] Poetry が見つかりません"; exit 1; fi  # R3
if ! command -v git >/dev/null 2>&1; then echo "[x] Git が見つかりません"; exit 1; fi      # R3

# R3/R6: Pythonバージョンの案内（失敗時のヒント）
PYVER=$(pyenv version-name || echo "unknown")  # R3
echo "[i] Python via pyenv: $PYVER"            # R3

# R4: 仮想環境の自動生成/有効化（Poetryが面倒を見る）
poetry install --no-interaction --quiet        # R4/R6

# R3: Git 状態確認（クリーンかどうか）
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "[!] 作業ツリーに未コミットの変更があります"  # R3/R5
  git status -s                                   # R3
  read -p "続行しますか? (y/N): " yn              # R5/R6
  if [[ "$yn" != "y" && "$yn" != "Y" ]]; then
    echo "中断します"; exit 1                      # R5
  fi
fi

# R3: healthcheckの実行（要約を出す）
poetry run python tools/healthcheck.py           # R3/R6

# R2: その日のタスクを一点化（ブランチ命名）
CURR=$(git rev-parse --abbrev-ref HEAD)          # R2/R5
if [[ "$CURR" == "main" || "$CURR" == "master" ]]; then
  read -p "今日のタスクを一言で(例: add_login): " TASK  # R2/R6
  if [[ -n "$TASK" ]]; then
    BR="feat/${TASK}"                             # R5: Conventional風
    git checkout -b "$BR"                         # R5
    echo "[i] ブランチ作成: $BR"                   # R5
  fi
fi

# R4: 最小の実行（テスト優先、なければサンプル起動）
if test -d tests; then
  echo "[i] pytest 実行"; poetry run pytest -q || true  # R4: 失敗でも先へ
elif test -f app.py; then
  echo "[i] サンプル実行: app.py"; poetry run python app.py || true  # R4
else
  echo "[i] 実行対象が見つかりません (tests/ or app.py を用意)"     # R4/R6
fi

# R5: 任意の開始コミット（空コミットで「一歩」を刻む）
read -p "開始コミットを打ちますか? (y/N): " ck         # R5
if [[ "$ck" == "y" || "$ck" == "Y" ]]; then
  git commit --allow-empty -m "chore: start day session"  # R5
  echo "[i] chore: start day session を作成"              # R5
fi

echo "[✓] 準備完了。良い一日を。"                        # R1
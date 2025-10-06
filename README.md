# python_env_test

> uraha 開発用サンドボックス（Streamlit + Poetry + Ruff + mypy）

## 運用メモ（保護ルール）
- **main 直 push 禁止**：変更は必ず Pull Request。
- **必須チェック**：**`ci / ruff`** & **`ci / mypy`** が **緑** でないとマージ不可。
- **Up to date 必須**：PR は main の最新に追随してからマージ（**Update branch** / rebase）。

**Quick**
1. ブランチ作成 → 変更 → commit / push  
2. PR 作成 → Checks（`ci / ruff`, `ci / mypy`）を緑に  
3. 「This branch is up to date with main」を満たす  
4. レビュー → マージ

## ローカル実行
```bash
poetry install
poetry run streamlit run hello_streamlit.py

# --- imports (先頭にまとめる) ---
import shlex
import subprocess

import streamlit as st


# --- helpers ---
def run_cmd(cmd: str):
    """コマンドを実行して (成功?, 出力全文) を返す。"""
    r = subprocess.run(
        shlex.split(cmd),
        capture_output=True,
        text=True,
        check=False,  # ← 明示
    )
    out = (r.stdout or "") + (("\n" + r.stderr) if r.stderr else "")
    return r.returncode == 0, out.strip() or "(no output)"


def run_ruff():
    return run_cmd("poetry run ruff check --config pyproject.toml --force-exclude .")


def run_mypy():
    return run_cmd("poetry run mypy .")


st.title("Hello, Streamlit 👋")
st.write("Poetry venv OK / Ruff & mypy 導入済み")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Ruff check"):
        r = subprocess.run(
            shlex.split("poetry run ruff check --config pyproject.toml --force-exclude ."),
            capture_output=True,
            text=True,
            check=False,
        )
        st.code(r.stdout or r.stderr, language="bash")

with col2:
    if st.button("mypy"):
        r = subprocess.run(
            shlex.split("poetry run mypy ."),
            capture_output=True,
            text=True,
            check=False,
        )
        st.code(r.stdout or r.stderr, language="bash")

with col3:
    if st.button("Healthcheck"):
        r = subprocess.run(
            shlex.split("poetry run python tools/healthcheck.py"),
            capture_output=True,
            text=True,
            check=False,
        )
        st.code(r.stdout or r.stderr, language="bash")
st.divider()
if st.button("All checks"):
    with st.spinner("Running ruff & mypy…"):
        ok_ruff, out_ruff = run_ruff()
        ok_mypy, out_mypy = run_mypy()

    # サマリー
    summary = f"ruff: {'OK' if ok_ruff else 'FAIL'} / mypy: {'OK' if ok_mypy else 'FAIL'}"
    if ok_ruff and ok_mypy:
        st.success(f"All checks passed ✅  — {summary}")
    else:
        st.error(f"Some checks failed ❌  — {summary}")

    # 詳細 ( 失敗したものだけ展開表示)
    if not ok_ruff:
        st.subheader("Ruff errors")
        st.code(out_ruff, language="bash")
    if not ok_mypy:
        st.subheader("mypy errors")
        st.code(out_mypy, language="bash")
st.subheader("簡易ロールバック (直前コミットへ)")
st.caption("※Git 管理環境。未コミットのある状態では中止します。")

if st.button("戻す (git reset --hard & clean)"):
    dirty = subprocess.run(
        shlex.split("git status --porcelain"),
        capture_output=True,
        text=True,
        check=False,
    )
    if dirty.stdout.strip():
        st.warning("未コミットの変更があります。コミット or stash 後に再実行してください。")
    else:
        r1 = subprocess.run(["git", "reset", "--hard", "HEAD"], capture_output=True, text=True, check=False)
        r2 = subprocess.run(["git", "clean", "-fd"], capture_output=True, text=True, check=False)
        st.success((r1.stdout or r1.stderr) + "\n" + (r2.stdout or r2.stderr))

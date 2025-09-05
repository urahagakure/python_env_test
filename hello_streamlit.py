import shlex
import subprocess

import streamlit as st

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
            shlex.split("bash tools/healthcheck.sh"),
            capture_output=True,
            text=True,
            check=False,
        )
        st.code(r.stdout or r.stderr, language="bash")

st.divider()
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

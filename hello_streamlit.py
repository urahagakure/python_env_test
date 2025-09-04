# 標準ライブラリ（アルファベット順）
import shlex
import subprocess

# サードパーティ
import streamlit as st

st.title("Hello, Streamlit 👋")
st.write("Poetry venv OK / Ruff & mypy 導入済み")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Ruff check"):
        out = subprocess.run(shlex.split("poetry run ruff check"), check=True, capture_output=True, text=True)
        st.code(out.stdout or out.stderr, language="bash")
with col2:
    if st.button("mypy"):
        out = subprocess.run(shlex.split("poetry run mypy"), capture_output=True, text=True, check=False)
        st.code(out.stdout or out.stderr, language="bash")
with col3:
    if st.button("Healthcheck"):
        out = subprocess.run(shlex.split("bash tools/healthcheck.sh"), capture_output=True, text=True, check=False)
        st.code(out.stdout or out.stderr, language="bash")

st.divider()
st.subheader("簡易ロールバック（直前コミットへ）")
st.caption("※Git 管理前提。安全のため未コミット変更がある場合は中止します。")

if st.button("戻す（git reset --hard && clean）"):
    # 変更が未コミットなら中止
    dirty = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=False)
    if dirty.stdout.strip():
        st.warning("未コミットの変更があります。コミット or stash 後に実行してください。")
    else:
        r1 = subprocess.run(["git", "reset", "--hard", "HEAD"], capture_output=True, text=True, check=False)
        r2 = subprocess.run(["git", "clean", "-fd"], capture_output=True, text=True, check=False)
        st.success("ロールバック完了")
        st.code((r1.stdout + r1.stderr + r2.stdout + r2.stderr) or "done", language="bash")

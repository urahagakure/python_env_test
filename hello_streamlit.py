from __future__ import annotations

# --- stdlib
import shlex
import subprocess

# --- third party
import streamlit as st

# --- local
import effiloop.mini as effi


def run_cmd(cmd: str) -> tuple[int, str]:
    """Run a shell command and return (exit_code, full_output)."""
    r = subprocess.run(
        shlex.split(cmd),
        capture_output=True,
        text=True,
        check=False,
    )
    out = (r.stdout or "") + (("\n" + r.stderr) if r.stderr else "")
    return r.returncode, out


st.set_page_config(page_title="Hello, Streamlit", page_icon="👋", layout="wide")
st.title("Hello, Streamlit")

st.subheader("All checks")
if st.button("Ruff format → Ruff check --fix → mypy"):
    logs: list[str] = []
    for cmd in [
        "poetry run ruff format",
        "poetry run ruff check --fix .",
        "poetry run mypy .",
    ]:
        code, out = run_cmd(cmd)
        logs.append(f"$ {cmd}\n(exit {code})\n{out}")
    st.code("\n\n".join(logs), language="bash")

st.divider()
st.subheader("Quick tools")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Ruff check"):
        _, out = run_cmd("poetry run ruff check --config pyproject.toml --force-exclude .")
        st.code(out, language="bash")

with col2:
    if st.button("mypy"):
        _, out = run_cmd("poetry run mypy .")
        st.code(out, language="bash")

with col3:
    if st.button("Healthcheck"):
        _, out = run_cmd("poetry run python tools/healthcheck.py")
        st.code(out, language="bash")

st.divider()
st.subheader("Git rollback (reset --hard & clean)")
if st.button("戻す"):
    code, out = run_cmd("git status --porcelain")
    if out.strip():
        st.warning("未コミットの変更があります。コミット or stash 後に実行してください。")
    else:
        _, out1 = run_cmd("git reset --hard HEAD")
        _, out2 = run_cmd("git clean -fd")
        st.code(out1 + ("\n" + out2 if out2 else ""), language="bash")

st.divider()
st.subheader("EffiLoop mini")
if st.button("Run EffiLoop mini"):
    ph = st.empty()

    def _progress_cb(i: int, name: str, remain: float) -> None:
        ph.info(f"{i}. {name} 残り{remain:0.1f}s")

    effi.run(_progress_cb)
    st.success("Done ✅")

from __future__ import annotations

# --- stdlib
import shlex
import subprocess

# --- third party
import streamlit as st

# --- local
import effiloop.mini as effi
import skills.bls_visual as bls_vis

# --- constants (importの後)
SUD_HIGH_THRESHOLD = 7


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

preset = st.selectbox("プリセット", effi.list_presets(), index=0)

if st.button("Run EffiLoop mini"):
    ph = st.empty()

    def _progress_cb(i: int, name: str, remain: float) -> None:
        ph.info(f"{i}. {name} 残り{remain:0.1f}s")

    # 早回し(1分=1秒　 )でデモ実行。実時間で回したいときは time_scale=1.0 に。
    effi.run_preset(_progress_cb, preset, time_scale=60.0)
    st.success("Done ✅")

st.divider()
st.subheader("BLSプラクティス(視覚, β)")

with st.expander("注意と同意(要読)", expanded=False):
    st.write(
        "- これは治療ではありません。強い苦痛がある/体調が悪いときは中止してください。\n"
        "- てんかん・光過敏の方は視覚モードを使わないでください(聴覚/タップ推奨)。"
    )

c1, c2, c3 = st.columns(3)
with c1:
    rate = st.slider("レート(Hz)", 0.8, 2.0, 1.0, 0.1)
with c2:
    set_len = st.selectbox("セット長", ["30秒", "45秒", "60秒"], index=2)
with c3:
    jitter = st.slider("揺らぎ(%)", 0, 10, 0, 1)

# 実時間への切替(任意)
realtime = st.checkbox("Real-timeで回す", value=False)
ts = 1.0 if realtime else 60.0
sec = {"30秒": 30.0, "45秒": 45.0, "60秒": 60.0}[set_len]
sud_pre = st.slider("SUD(不快度) 開始時", 0, 10, 3)

# --- 状態 ---
state = st.session_state
state.setdefault("bls_running", False)
state.setdefault("bls_stop", False)


def _ground() -> None:
    st.toast("5つ見えるもの", icon="🟦")
    st.toast("4つ触れるもの", icon="🟩")
    st.toast("3つ聞こえる音", icon="🟨")
    st.toast("2つ香り/味", icon="🟧")
    st.toast("1つ呼吸", icon="🟥")


# ここは「常に表示」する(消えない)
c_run, c_stop, c_ground = st.columns(3)
start_clicked = c_run.button("Start visual BLS", key="bls_start", disabled=state.bls_running)
stop_clicked = c_stop.button("Stop", key="bls_stop_btn", type="secondary", disabled=not state.bls_running)
ground_clicked = c_ground.button("Ground", key="bls_ground_btn")

# 先に単発イベントを処理
if ground_clicked:
    _ground()
if stop_clicked:
    state.bls_stop = True  # ループ側の stop_fn が拾う

# Start を押したときの本処理
if start_clicked:
    # SUDゲート(高すぎたら描画を止める)
    if sud_pre >= SUD_HIGH_THRESHOLD:
        st.warning("SUDが高め。今日はグラウンディングだけにしましょう。")
        _ground()
        st.stop()

    state.bls_running = True
    state.bls_stop = False

    cfg = bls_vis.VisualConfig(rate_hz=rate, duration_s=sec, jitter_pct=jitter, fps=40.0)
    bar = st.progress(0, text="準備中...")  # 進捗はStartのたびに作り直す
    txt = st.empty()

    def _cb(i: int, pos01: float, remain: float) -> None:
        bar.progress(int(pos01 * 100), text=f"{rate:.1f} Hz / 残り {remain:0.1f}s")
        if i % 20 == 0:
            txt.info(f"{i} steps")

    bls_vis.run_visual(_cb, cfg, time_scale=ts, stop_fn=lambda: state.bls_stop)

    state.bls_running = False
    st.warning("Stopped. Groundへ。") if state.bls_stop else st.success("Done ✅")
with c_stop:
    st.button(
        "Stop",
        type="secondary",
        disabled=not st.session_state.bls_running,
        on_click=lambda: st.session_state.update(bls_stop=True),
    )

with c_ground:
    st.button("Ground", on_click=_ground)

sud_post = st.slider("SUD(不快度) 終了時", 0, 10, 2)

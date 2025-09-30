# effiloop/mini.py
from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass

# ---- Presets ----
PRESETS: dict[str, int] = {"60分": 60, "45分": 45, "25分": 25}
_TIME_SCALE_DEFAULT: float = 60.0  # 例: 60なら「1分 = 実時間1秒」で早回し


def list_presets() -> list[str]:
    """UI用: 表示順でプリセット名を返す。"""
    return list(PRESETS.keys())


def _resolve_minutes(preset_or_minutes: int | str) -> int:
    if isinstance(preset_or_minutes, int):
        return preset_or_minutes
    return PRESETS.get(preset_or_minutes, 60)


def _simulate_loop(
    cb: Callable[[int, str, float], None], minutes: int, *, time_scale: float = _TIME_SCALE_DEFAULT
) -> None:
    """EffiLoopミニの簡易シミュレーション。
    time_scale=60 なら「分→秒」に圧縮。UIのデモ実行向け。
    """
    total = float(minutes * 60)
    remain = total
    step = 0
    name = f"{minutes}min"
    dt_sim = 0.1  # 0.1秒ぶんの“仮想時間”ごとに更新
    sleep_real = dt_sim / max(0.1, time_scale)
    while remain > 0:
        step += 1
        cb(step, name, remain)
        time.sleep(sleep_real)
        remain -= dt_sim
    cb(step + 1, name, 0.0)


def run_preset(
    cb: Callable[[int, str, float], None], preset: str, *, time_scale: float = _TIME_SCALE_DEFAULT
) -> None:
    """プリセット名('60分' など)で走らせるAPI。"""
    minutes = _resolve_minutes(preset)
    _simulate_loop(cb, minutes, time_scale=time_scale)


@dataclass
class Step:
    name: str
    seconds: float


SEQUENCE: list[Step] = [
    Step("3-6呼吸", 15),
    Step("姿勢→視線→微笑", 15),
    Step("アファメーション", 15),
]


def run(on_tick: Callable[[int, str, float], None]) -> None:
    for i, s in enumerate(SEQUENCE, 1):
        t0 = time.perf_counter()
        while True:
            remain = s.seconds - (time.perf_counter() - t0)
            if remain <= 0:
                break
            on_tick(i, s.name, max(0.0, remain))
            time.sleep(0.2)

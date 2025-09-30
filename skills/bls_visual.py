from __future__ import annotations

import math
import time
from collections.abc import Callable
from dataclasses import dataclass

VisualCb = Callable[[int, float, float], None]


@dataclass(slots=True)
class VisualConfig:
    rate_hz: float = 1.0
    duration_s: float = 60.0
    jitter_pct: float = 0.0
    fps: float = 50.0


def run_visual(cb: VisualCb, cfg: VisualConfig, *, time_scale: float = 1.0) -> None:
    step, t = 0, 0.0
    dt_sim = 1.0 / max(10.0, cfg.fps)
    sleep_real = dt_sim / max(1e-3, time_scale)
    total = float(cfg.duration_s)
    while t < total:
        f = cfg.rate_hz * (1.0 + (cfg.jitter_pct * 0.01) * math.sin(2.0 * math.pi * 0.1 * t))
        pos01 = (math.sin(2.0 * math.pi * f * t) + 1.0) * 0.5
        step += 1
        cb(step, pos01, max(0.0, total - t))
        time.sleep(sleep_real)
        t += dt_sim
    cb(step + 1, 1.0, 0.0)

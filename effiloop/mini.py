# effiloop/mini.py
from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass


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

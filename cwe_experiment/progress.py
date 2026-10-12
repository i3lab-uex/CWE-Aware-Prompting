"""Small dependency-free console progress reporter."""

from __future__ import annotations

from dataclasses import dataclass, field
import sys
import time


@dataclass
class ConsoleProgress:
    """Emit readable, rate-limited progress while keeping stdout as JSON."""

    enabled: bool = True
    _started: float = field(default_factory=time.monotonic)
    _last_percent: dict[str, int] = field(default_factory=dict)
    _last_output: dict[str, float] = field(default_factory=dict)

    def message(self, stage: str, message: str) -> None:
        if not self.enabled:
            return
        elapsed = time.monotonic() - self._started
        print(f"[{stage:<11}] {message} · {self._duration(elapsed)}", file=sys.stderr, flush=True)

    def update(
        self,
        stage: str,
        completed: int,
        total: int,
        detail: str = "",
        *,
        force: bool = False,
    ) -> None:
        if not self.enabled:
            return
        now = time.monotonic()
        percent = int(100 * completed / total) if total else 100
        last_percent = self._last_percent.get(stage, -1)
        last_output = self._last_output.get(stage, 0.0)
        if not force and completed < total and percent <= last_percent and now - last_output < 10:
            return
        self._last_percent[stage] = percent
        self._last_output[stage] = now
        width = 20
        filled = min(width, int(width * completed / total)) if total else width
        bar = "█" * filled + "░" * (width - filled)
        suffix = f" · {detail}" if detail else ""
        elapsed = now - self._started
        print(
            f"[{stage:<11}] {bar} {completed:,}/{total:,} ({percent:3d}%)"
            f"{suffix} · {self._duration(elapsed)}",
            file=sys.stderr,
            flush=True,
        )

    @staticmethod
    def _duration(seconds: float) -> str:
        minutes, remainder = divmod(int(seconds), 60)
        hours, minutes = divmod(minutes, 60)
        if hours:
            return f"{hours:d}h {minutes:02d}m {remainder:02d}s"
        if minutes:
            return f"{minutes:d}m {remainder:02d}s"
        return f"{remainder:d}s"

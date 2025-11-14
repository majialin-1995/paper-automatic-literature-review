from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ProgressReporter:
    """Render a simple textual progress bar for console workflows."""

    total_steps: int
    width: int = 24
    current_step: int = 0

    def start(self, message: str) -> None:
        """Display an initial hint before entering the workflow."""
        print(message)
        self._display_bar()

    def advance(self, label: str) -> None:
        """Advance the bar by one step and output the current status."""
        if self.total_steps <= 0:
            print(f"\n{label}")
            return
        self.current_step = min(self.total_steps, self.current_step + 1)
        print(f"\n[{self.current_step}/{self.total_steps}] {label}")
        self._display_bar()

    def _display_bar(self) -> None:
        bar = self._render_bar()
        if bar:
            print(bar)

    def _render_bar(self) -> str:
        if self.total_steps <= 0:
            return ""
        ratio = self.current_step / self.total_steps
        filled = int(round(ratio * self.width))
        filled = max(0, min(self.width, filled))
        bar = "█" * filled + "░" * (self.width - filled)
        return f"[{bar}] {ratio * 100:5.1f}%"

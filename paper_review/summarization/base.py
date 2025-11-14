from __future__ import annotations

from abc import ABC, abstractmethod

from ..models import PaperEntry


class Summarizer(ABC):
    """Base class for generating Chinese summaries of papers."""

    @abstractmethod
    def summarize(self, paper: PaperEntry) -> str:
        """Return a Chinese summary for the given paper."""


class SummaryFailed(RuntimeError):
    """Raised when the summarizer cannot produce a valid summary."""

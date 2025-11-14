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


class TemplateSummarizer(Summarizer):
    """Lightweight summarizer that builds a sentence from metadata only."""

    def summarize(self, paper: PaperEntry) -> str:
        base = f"{paper.first_author}等人提出了一种"
        if paper.title:
            base += f"名为“{paper.title}”的方法，"

        if paper.abstract:
            abs_txt = paper.abstract.strip().replace("\n", " ")
            abs_txt = " ".join(abs_txt.split())
            abs_short = abs_txt if len(abs_txt) <= 80 else abs_txt[:80].rstrip() + "……"
            base += f"该方法主要针对{abs_short}"
        else:
            base += "该方法的具体摘要信息在原文中给出。"
        return base

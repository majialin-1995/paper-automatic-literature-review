"""Core package for automatic literature review generation."""

from .models import CategoryNode, PaperEntry
from .pipeline import ReviewPipeline

__all__ = ["CategoryNode", "PaperEntry", "ReviewPipeline"]

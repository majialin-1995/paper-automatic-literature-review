from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class PaperEntry:
    """Structured representation of a single bibliographic entry."""

    id: int
    key: str
    title: str
    abstract: str
    first_author: str
    authors: List[str]
    year: Optional[int]
    venue: str
    main_category: Optional[str] = None
    sub_category: Optional[str] = None
    summary_zh: str = ""


@dataclass
class CategoryNode:
    """Simple tree node used to describe the review schema."""

    name: str
    parent: Optional[str] = None
    children: List[str] = field(default_factory=list)

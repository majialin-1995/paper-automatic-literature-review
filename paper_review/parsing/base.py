from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from ..models import PaperEntry


class BibliographyParser(ABC):
    """Base class for converting bibliography files into :class:`PaperEntry` objects."""

    @abstractmethod
    def parse(self, source: Path) -> List[PaperEntry]:
        """Parse the given ``source`` file into a list of entries."""


class ParserRegistry:
    """Simple registry used to map file extensions to parser implementations."""

    def __init__(self) -> None:
        self._parsers = {}

    def register(self, suffix: str, parser: BibliographyParser) -> None:
        self._parsers[suffix.lower()] = parser

    def get(self, suffix: str) -> BibliographyParser:
        normalized = suffix.lower()
        if normalized not in self._parsers:
            raise ValueError(f"没有找到与扩展名 {suffix} 对应的解析器。")
        return self._parsers[normalized]


registry = ParserRegistry()

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Set

from ..models import PaperEntry


class BibliographyParser(ABC):
    """Base class for converting bibliography files into :class:`PaperEntry` objects."""

    @abstractmethod
    def parse(self, source: Path) -> List[PaperEntry]:
        """Parse the given ``source`` file into a list of entries."""


class ParserRegistry:
    """Registry used to map format names (or aliases) to parser implementations."""

    def __init__(self) -> None:
        self._parsers: dict[str, BibliographyParser] = {}
        self._primary_names: Set[str] = set()

    def register(self, name: str, parser: BibliographyParser, *, primary: bool = False) -> None:
        key = name.lower()
        self._parsers[key] = parser
        if primary:
            self._primary_names.add(key)

    def get(self, name: str) -> BibliographyParser:
        normalized = name.lower()
        if normalized not in self._parsers:
            available = ", ".join(sorted(self.available_formats())) or "无可用解析器"
            raise ValueError(f"没有找到名为 {name} 的解析器，可选值: {available}。")
        return self._parsers[normalized]

    def available_formats(self) -> List[str]:
        if self._primary_names:
            return sorted(self._primary_names)
        return sorted(self._parsers)


registry = ParserRegistry()

"""Parsers for different bibliography formats."""

from .base import BibliographyParser, registry
from . import ris  # noqa: F401 - ensure RIS parser is registered on import

__all__ = ["BibliographyParser", "registry"]

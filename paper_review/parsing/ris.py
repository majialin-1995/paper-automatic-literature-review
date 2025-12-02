from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List

from .base import BibliographyParser, registry
from .utils import normalize_authors
from ..models import PaperEntry


class RISParser(BibliographyParser):
    """Minimal RIS parser that only depends on the Python standard library."""

    TAG_MAPPINGS = {
        "authors": ("AU", "A1"),
        "title": ("TI", "T1"),
        "year": ("PY", "Y1"),
        "venue": ("JO", "JF", "T2"),
    }

    def parse(self, source: Path) -> List[PaperEntry]:
        records: List[Dict[str, List[str]]] = []
        current: Dict[str, List[str]] = {}

        def push_current() -> None:
            nonlocal current
            if current:
                records.append(current)
                current = {}

        with source.open("r", encoding="utf-8") as handle:
            for raw_line in handle:
                line = raw_line.rstrip("\n")
                if not line.strip():
                    continue
                match = re.match(r"^([A-Z0-9]{2})  - (.*)$", line)
                if not match:
                    if current:
                        last_key = next(reversed(current))
                        current[last_key].append(line.strip())
                    continue

                tag, value = match.group(1), match.group(2)
                if tag == "ER":
                    push_current()
                else:
                    current.setdefault(tag, []).append(value.strip())
            push_current()

        papers: List[PaperEntry] = []
        for index, record in enumerate(records):
            raw_authors = record.get("AU", []) + record.get("A1", [])
            authors = normalize_authors(raw_authors)
            first_author = authors[0] if authors else "Unknown"

            title_fields = record.get("TI", []) + record.get("T1", [])
            title = " ".join(title_fields).strip() if title_fields else "Untitled"

            abstract = " ".join(record.get("AB", [])).strip()

            year = None
            for tag in ("PY", "Y1"):
                if tag in record:
                    year_value = " ".join(record[tag])
                    match = re.search(r"\b(19|20)\d{2}\b", year_value)
                    if match:
                        year = int(match.group(0))
                        break

            venue_fields = record.get("JO", []) + record.get("JF", []) + record.get("T2", [])
            venue = " ".join(venue_fields).strip()

            papers.append(
                PaperEntry(
                    id=index,
                    key=f"paper_{index + 1}",
                    title=title,
                    abstract=abstract,
                    first_author=first_author,
                    authors=authors or [first_author],
                    year=year,
                    venue=venue,
                )
            )

        return papers


def register_parser() -> None:
    parser = RISParser()
    registry.register("ris", parser, primary=True)
    registry.register(".ris", parser)


register_parser()

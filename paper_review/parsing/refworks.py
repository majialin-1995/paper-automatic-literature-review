from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List

from .base import BibliographyParser, registry
from ..models import PaperEntry


class RefWorksParser(BibliographyParser):
    """Parser for RefWorks tagged text exports.

    The parser is intentionally minimal and only relies on the Python standard
    library. It collects common tags such as ``A1``/``AU`` for authors,
    ``T1``/``TI`` for titles, ``AB`` for abstracts, ``YR`` for years, and
    ``JF``/``T2`` for venues.
    """

    AUTHOR_TAGS = ("A1", "A2", "A3", "A4", "A5", "AU")
    TITLE_TAGS = ("T1", "TI")
    VENUE_TAGS = ("JF", "JO", "T2", "PB")

    def parse(self, source: Path) -> List[PaperEntry]:
        records: List[Dict[str, List[str]]] = []
        current: Dict[str, List[str]] = {}
        last_key: str | None = None

        def push_current() -> None:
            nonlocal current, last_key
            if any(current.values()):
                records.append(current)
            current = {}
            last_key = None

        with source.open("r", encoding="utf-8") as handle:
            for raw_line in handle:
                line = raw_line.rstrip("\n")
                if not line.strip():
                    push_current()
                    continue

                match = re.match(r"^([A-Z0-9]{2})\s+(.*)$", line)
                if not match:
                    if last_key:
                        current.setdefault(last_key, []).append(line.strip())
                    continue

                tag, value = match.group(1), match.group(2).strip()
                if tag == "RT" and current:
                    push_current()
                current.setdefault(tag, []).append(value)
                last_key = tag

            push_current()

        if not records:
            raise ValueError("未能从 RefWorks 文件中解析出任何记录，请确认格式是否为带标签的导出。")

        papers: List[PaperEntry] = []
        for index, record in enumerate(records):
            authors: List[str] = []
            for tag in self.AUTHOR_TAGS:
                authors.extend(record.get(tag, []))
            authors = [item.strip() for item in authors if item.strip()]
            first_author = authors[0] if authors else "Unknown"

            title_fields: List[str] = []
            for tag in self.TITLE_TAGS:
                title_fields.extend(record.get(tag, []))
            title = " ".join(title_fields).strip() or "Untitled"

            abstract = " ".join(record.get("AB", [])).strip()

            year = None
            for tag in ("YR", "PY"):
                if tag in record:
                    year_value = " ".join(record[tag])
                    match = re.search(r"\b(19|20)\d{2}\b", year_value)
                    if match:
                        year = int(match.group(0))
                        break

            venue_fields: List[str] = []
            for tag in self.VENUE_TAGS:
                venue_fields.extend(record.get(tag, []))
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
    parser = RefWorksParser()
    registry.register("refworks", parser, primary=True)
    registry.register(".refworks", parser)
    registry.register(".txt", parser)


register_parser()

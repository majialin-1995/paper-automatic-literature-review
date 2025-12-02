from __future__ import annotations

import re
from typing import Iterable, List

_AUTHOR_SPLIT_PATTERN = re.compile(r"[;；、]+")


def normalize_authors(raw_authors: Iterable[str]) -> List[str]:
    """Split and clean author strings from bibliography exports.

    Some sources concatenate multiple authors in a single field using
    semicolons or similar separators. This helper expands those fields
    and returns a flat, whitespace-trimmed list of author names.
    """

    normalized: List[str] = []
    for value in raw_authors:
        for name in _AUTHOR_SPLIT_PATTERN.split(value):
            stripped = name.strip()
            if stripped:
                normalized.append(stripped)
    return normalized

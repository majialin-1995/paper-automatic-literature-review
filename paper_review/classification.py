from __future__ import annotations

from typing import Dict, List

from .models import CategoryNode, PaperEntry


def assign_categories(papers: List[PaperEntry], schema: Dict[str, CategoryNode]) -> None:
    main_nodes = [node for node in schema.values() if node.parent is None]
    if not main_nodes:
        for paper in papers:
            paper.main_category = None
            paper.sub_category = None
        return

    main_nodes_sorted = sorted(main_nodes, key=lambda node: node.name)
    default_main = main_nodes_sorted[0].name
    default_children = schema[default_main].children
    default_sub = default_children[0] if default_children else None

    for paper in papers:
        paper.main_category = default_main
        paper.sub_category = default_sub

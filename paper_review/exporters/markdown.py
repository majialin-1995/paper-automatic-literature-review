from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

from ..models import CategoryNode, PaperEntry


def export_markdown(
    papers: List[PaperEntry],
    schema: Dict[str, CategoryNode],
    out_path: Path,
    sort_by_year: str,
) -> None:
    main_nodes = [node for node in schema.values() if node.parent is None]
    main_name_order = [node.name for node in main_nodes]

    uncategorized: List[PaperEntry] = []
    by_main_sub: Dict[str, Dict[Optional[str], List[PaperEntry]]] = {}
    for paper in papers:
        if not paper.main_category:
            uncategorized.append(paper)
            continue
        main_name = paper.main_category
        sub_name = paper.sub_category
        by_main_sub.setdefault(main_name, {}).setdefault(sub_name, []).append(paper)

    def sort_key(item: PaperEntry) -> int:
        if sort_by_year == "none":
            return 0
        year = item.year if item.year is not None else -9999
        return year

    reverse = sort_by_year == "desc"

    lines: List[str] = []
    lines.append("# 文献综述整理草稿（按大类/小类分组)\n")

    for main_name in main_name_order:
        if main_name not in by_main_sub:
            continue
        lines.append(f"\n## {main_name}\n")
        sub_dict = by_main_sub[main_name]
        declared_children = schema[main_name].children
        extra_children = [name for name in sub_dict.keys() if name is not None and name not in declared_children]
        all_sub_names: List[Optional[str]] = declared_children + extra_children + [None]

        for sub_name in all_sub_names:
            items = sub_dict.get(sub_name, [])
            if not items:
                continue
            heading = sub_name if sub_name is not None else "未指定小类"
            lines.append(f"\n### {heading}\n")
            overview = _build_subcategory_overview(heading, items)
            lines.append(overview + "\n")

            items_sorted = sorted(items, key=sort_key, reverse=reverse)
            for paper in items_sorted:
                lines.append(f"- {paper.summary_zh}")

            summary_para = _build_subcategory_summary(heading, items)
            lines.append("\n" + summary_para + "\n")

    if uncategorized:
        lines.append("\n## 未分类\n")
        items_sorted = sorted(uncategorized, key=sort_key, reverse=reverse)
        overview = _build_subcategory_overview("未指定小类", items_sorted)
        lines.append(overview + "\n")

        for paper in items_sorted:
            lines.append(f"- {paper.summary_zh}")

        summary_para = _build_subcategory_summary("未指定小类", items_sorted)
        lines.append("\n" + summary_para + "\n")

    out_path.write_text("\n".join(lines), encoding="utf-8")


def _build_subcategory_overview(sub_name: Optional[str], papers: List[PaperEntry]) -> str:
    if not papers:
        return "本小类当前尚无归入的研究工作。"

    year_values = [paper.year for paper in papers if paper.year is not None]
    year_min = min(year_values) if year_values else None
    year_max = max(year_values) if year_values else None
    count = len(papers)

    name_part = "这一小类" if sub_name in (None, "未指定小类") else f"“{sub_name}”这一小类"
    year_part = ""
    if year_min and year_max:
        year_part = f"，时间范围集中在 {year_min} 年左右" if year_min == year_max else f"，时间范围大致覆盖 {year_min}–{year_max} 年"

    return f"{name_part}主要汇总了 {count} 篇相关工作{year_part}。"


def _build_subcategory_summary(sub_name: Optional[str], papers: List[PaperEntry]) -> str:
    if not papers:
        return "综合来看，该小类尚未归入具体文献，后续可以根据研究进展进一步补充。"

    years = [paper.year for paper in papers if paper.year is not None]
    year_span = ""
    if years:
        ymin, ymax = min(years), max(years)
        year_span = f"{ymin} 年" if ymin == ymax else f"{ymin}–{ymax} 年"

    representatives = [paper.first_author for paper in papers[:3]]
    reps_str = "、".join(representatives) if representatives else "若干学者"
    name_part = "这一小类" if sub_name in (None, "未指定小类") else f"“{sub_name}”这一小类"
    span_part = f"，相关研究大致分布在 {year_span}" if year_span else ""

    return (
        f"综合来看，{name_part}的工作主要围绕若干关键问题展开{span_part}。"
        f"代表性的研究包括 {reps_str} 等人的工作，这些方法在公开数据集上验证了有效性，"
        f"为后续在真实工程场景中的推广应用奠定了基础，"
        f"但在跨工况泛化能力、可解释性以及与实际工业流程的深度融合方面仍有进一步提升空间。"
    )

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ris_hier_workflow.py

基于 RIS 文献文件，生成分“大类 / 小类”的中文综述 Markdown 草稿。

功能概要
--------
1. 解析一个 .ris 文件，抽取：
   - 第一作者、作者列表
   - 年份
   - 标题、摘要
   - 期刊 / 会议名称（venue）

2. 类别结构（schema）来源：
   - 若提供 --categories categories.yaml：
       使用 YAML 定义的大类 + 小类结构。
   - 若不提供 YAML，但提供 --n-main / --m-sub：
       自动生成 “自动主类1-子类1” 这种结构。
   - 若都不提供：
       退回一个兜底大类 “自动归类/未分类”。

3. 分类：
   - 当前实现：全部文献都归到「第一个大类 / 第一个小类」。
   - 你可以后续把 assign_categories(...) 换成
     自己的 LLM 分类逻辑。

4. 输出：
   - 一个 Markdown 文件，结构为：
       # 文献综述整理草稿
       ## 大类A
       ### 小类A1
         一句总起
         - 条目1（XXX等人提出...）
         - 条目2 ...
         一段总结

依赖
----
- 仅使用标准库（不需要额外 pip 安装）
- 如果使用 YAML 类别文件，需要安装 `pyyaml`：
    pip install pyyaml

用法示例
--------
python ris_hier_workflow.py \
    --ris papers.ris \
    --out-dir runs_review \
    --categories categories.yaml \
    --sort-by-year desc

# 或者，不用 YAML，只给数字：
python ris_hier_workflow.py \
    --ris papers.ris \
    --out-dir runs_review \
    --n-main 4 --m-sub 3 \
    --sort-by-year asc
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None  # 如果不用 categories.yaml，可以不装


# ───────────────────── 数据结构 ───────────────────── #

@dataclass
class PaperEntry:
    id: int
    key: str  # 编号/内部 id
    title: str
    abstract: str
    first_author: str
    authors: List[str]
    year: Optional[int]
    venue: str

    # 分类字段（后续赋值）
    main_category: Optional[str] = None
    sub_category: Optional[str] = None

    # 中文总结字段
    summary_zh: str = ""


@dataclass
class CategoryNode:
    name: str
    parent: Optional[str] = None
    children: List[str] = field(default_factory=list)


# ───────────────────── RIS 解析 ───────────────────── #

def parse_ris(ris_path: Path) -> List[PaperEntry]:
    """
    非依赖第三方库的简单 RIS 解析器。

    只处理常用字段：
      - AU/A1：作者（多行）
      - TI/T1：标题
      - AB：摘要
      - PY/Y1：年份
      - JO/JF/T2：期刊/会议

    每条记录以 "ER  -" 结尾。
    """
    records: List[Dict[str, List[str]]] = []
    current: Dict[str, List[str]] = {}

    def push_current():
        nonlocal current
        if current:
            records.append(current)
            current = {}

    with ris_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            # RIS 行通常是 "XX  - content"
            m = re.match(r"^([A-Z0-9]{2})  - (.*)$", line)
            if not m:
                # 有些续行可能无标签，简单拼接到上一个字段
                if current:
                    # 找到最后一个 key，追加
                    last_key = next(reversed(current))
                    current[last_key].append(line.strip())
                continue
            tag, value = m.group(1), m.group(2)
            if tag == "ER":
                push_current()
            else:
                current.setdefault(tag, []).append(value.strip())
        # 文件结束，推一次
        push_current()

    papers: List[PaperEntry] = []
    for i, rec in enumerate(records):
        # 作者
        authors = rec.get("AU", []) + rec.get("A1", [])
        authors = [a for a in [a.strip() for a in authors] if a]
        first_author = authors[0] if authors else "Unknown"

        # 标题
        title_fields = rec.get("TI", []) + rec.get("T1", [])
        title = " ".join(title_fields).strip() if title_fields else "Untitled"

        # 摘要
        ab_fields = rec.get("AB", [])
        abstract = " ".join(ab_fields).strip()

        # 年份
        year = None
        for y_tag in ("PY", "Y1"):
            if y_tag in rec:
                y_str = " ".join(rec[y_tag])
                m_year = re.search(r"\b(19|20)\d{2}\b", y_str)
                if m_year:
                    year = int(m_year.group(0))
                    break

        # 期刊 / 会议
        venue_fields = rec.get("JO", []) + rec.get("JF", []) + rec.get("T2", [])
        venue = " ".join(venue_fields).strip()

        papers.append(
            PaperEntry(
                id=i,
                key=f"paper_{i+1}",
                title=title,
                abstract=abstract,
                first_author=first_author,
                authors=authors or [first_author],
                year=year,
                venue=venue,
            )
        )

    print(f"解析 RIS 完成，共 {len(papers)} 篇文献。")
    return papers


# ───────────────────── 中文总结生成（占位版） ───────────────────── #

def build_cn_summary(p: PaperEntry) -> str:
    """
    从第一作者 + 标题 + 摘要，生成一句形如
    “XXX等人提出了一种……方法”的中文总结。

    这里是一个不依赖大模型的占位实现：
      - 重点拼接标题
      - 摘要只取前若干个字作为“主要针对……”
    """
    base = f"{p.first_author}等人提出了一种"
    if p.title:
        base += f"名为“{p.title}”的方法，"

    if p.abstract:
        abs_txt = p.abstract.strip().replace("\n", " ")
        abs_txt = re.sub(r"\s+", " ", abs_txt)
        if len(abs_txt) > 80:
            abs_short = abs_txt[:80].rstrip() + "……"
        else:
            abs_short = abs_txt
        base += f"该方法主要针对{abs_short}"
    else:
        base += "该方法的具体摘要信息在原文中给出。"

    return base


def fill_all_summaries(papers: List[PaperEntry]) -> None:
    for p in papers:
        p.summary_zh = build_cn_summary(p)


# ───────────────────── 类别结构（schema） ───────────────────── #

def build_simple_auto_schema() -> Dict[str, CategoryNode]:
    """
    什么都没给时的兜底 schema：
    只有一个大类 “自动归类/未分类”，无子类。
    """
    name = "自动归类/未分类"
    return {
        name: CategoryNode(name=name, parent=None, children=[]),
    }


def suggest_schema_from_papers_auto(
    papers: List[PaperEntry],
    n_main: Optional[int],
    m_sub: Optional[int],
) -> Dict[str, CategoryNode]:
    """
    自动构造类别 schema 的简单实现。

    情况 1：给了 n_main（>0），可选 m_sub
      - 生成 n_main 个大类：自动主类1, 自动主类2, ...
      - 如果 m_sub > 0，则每个大类下面再生成 m_sub 个小类：
        自动主类1-子类1, 自动主类1-子类2, ...

    情况 2：既没有 YAML，也没有数字
      - 退化成一个兜底大类：“自动归类/未分类”。
    """
    if not n_main or n_main <= 0:
        return build_simple_auto_schema()

    if m_sub is None or m_sub < 0:
        m_sub = 0

    schema: Dict[str, CategoryNode] = {}
    for i in range(1, n_main + 1):
        main_name = f"自动主类{i}"
        children: List[str] = []
        for j in range(1, m_sub + 1):
            sub_name = f"{main_name}-子类{j}"
            children.append(sub_name)
            schema[sub_name] = CategoryNode(name=sub_name, parent=main_name, children=[])
        schema[main_name] = CategoryNode(name=main_name, parent=None, children=children)

    return schema


def load_schema_from_yaml(path: Path) -> Dict[str, CategoryNode]:
    """
    从 categories.yaml 载入 schema。

    建议的 YAML 结构示例：
    --------------------
    - name: 信号增强与去噪
      children:
        - name: 深度学习降噪方法
        - name: 传统滤波与小波方法
    - name: 特征提取与表示学习
      children:
        - name: 时域/频域特征
        - name: 深度表示学习
    """
    if yaml is None:
        raise RuntimeError("未安装 pyyaml，无法解析 YAML。请先 `pip install pyyaml`")

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("categories.yaml 顶层应为 list")

    schema: Dict[str, CategoryNode] = {}

    for main in data:
        if not isinstance(main, dict) or "name" not in main:
            raise ValueError("categories.yaml 中每个大类应为 {name: ..., children: [...] } 结构")
        main_name = str(main["name"])
        children_names: List[str] = []

        for child in main.get("children", []):
            if isinstance(child, dict):
                sub_name = str(child.get("name", "未命名子类"))
            else:
                sub_name = str(child)
            children_names.append(sub_name)
            schema[sub_name] = CategoryNode(name=sub_name, parent=main_name, children=[])

        schema[main_name] = CategoryNode(name=main_name, parent=None, children=children_names)

    return schema


# ───────────────────── 文献分类（当前为占位实现） ───────────────────── #

def assign_categories(papers: List[PaperEntry], schema: Dict[str, CategoryNode]) -> None:
    """
    当前是一个非常简单的占位实现：

    - 找到第一个大类 main
    - 若该大类下有子类，则丢到第一个子类；
      否则只填 main_category，sub_category 置为 None

    你后续完全可以把这里替换成：
      - 手工标注好的 CSV / JSON 读入；
      - 或者走 LLM 分类逻辑。
    """
    main_nodes = [node for node in schema.values() if node.parent is None]
    if not main_nodes:
        # 没有大类，就都变成未分类
        for p in papers:
            p.main_category = None
            p.sub_category = None
        return

    main_nodes_sorted = sorted(main_nodes, key=lambda n: n.name)
    default_main = main_nodes_sorted[0].name
    default_children = schema[default_main].children
    default_sub = default_children[0] if default_children else None

    for p in papers:
        p.main_category = default_main
        p.sub_category = default_sub


# ───────────────────── 小类总起 + 小类小结 ───────────────────── #

def _build_subcategory_overview(sub_name: Optional[str], papers: List[PaperEntry]) -> str:
    """为一个小类生成一句“总起”概述。"""
    if not papers:
        return "本小类当前尚无归入的研究工作。"

    year_values = [p.year for p in papers if p.year is not None]
    year_min = min(year_values) if year_values else None
    year_max = max(year_values) if year_values else None
    n = len(papers)

    if sub_name is None or sub_name == "未指定小类":
        name_part = "这一小类"
    else:
        name_part = f"“{sub_name}”这一小类"

    year_part = ""
    if year_min and year_max:
        if year_min == year_max:
            year_part = f"，时间范围集中在 {year_min} 年左右"
        else:
            year_part = f"，时间范围大致覆盖 {year_min}–{year_max} 年"

    return f"{name_part}主要汇总了 {n} 篇相关工作{year_part}。"


def _build_subcategory_summary(sub_name: Optional[str], papers: List[PaperEntry]) -> str:
    """为一个小类生成一段“总结”性文字（模板版）。"""
    if not papers:
        return "综合来看，该小类尚未归入具体文献，后续可以根据研究进展进一步补充。"

    years = [p.year for p in papers if p.year is not None]
    year_span = ""
    if years:
        ymin, ymax = min(years), max(years)
        if ymin == ymax:
            year_span = f"{ymin} 年"
        else:
            year_span = f"{ymin}–{ymax} 年"

    reps = [p.first_author for p in papers[:3]]
    reps_str = "、".join(reps) if reps else "若干学者"

    if sub_name is None or sub_name == "未指定小类":
        name_part = "这一小类"
    else:
        name_part = f"“{sub_name}”这一小类"

    span_part = f"，相关研究大致分布在 {year_span}" if year_span else ""

    return (
        f"综合来看，{name_part}的工作主要围绕若干关键问题展开{span_part}。"
        f"代表性的研究包括 {reps_str} 等人的工作，这些方法在公开数据集上验证了有效性，"
        f"为后续在真实工程场景中的推广应用奠定了基础，"
        f"但在跨工况泛化能力、可解释性以及与实际工业流程的深度融合方面仍有进一步提升空间。"
    )


# ───────────────────── Markdown 导出 ───────────────────── #

def export_markdown(
    papers: List[PaperEntry],
    schema: Dict[str, CategoryNode],
    out_path: Path,
    sort_by_year: str,
):
    """
    按“大类 -> 小类 -> 文献”层次导出 Markdown。

    每个“大类”一节（##），
    每个“小类”：
      - 一句总起
      - 文献条目列表
      - 一段小结

    sort_by_year: 'none' | 'asc' | 'desc'
    """
    # 找所有大类（parent 为 None）
    main_nodes = [node for node in schema.values() if node.parent is None]
    main_name_order = [node.name for node in main_nodes]

    # 未分类文献
    uncategorized: List[PaperEntry] = []

    # (main, sub) -> 文献列表
    by_main_sub: Dict[str, Dict[Optional[str], List[PaperEntry]]] = {}
    for p in papers:
        if not p.main_category:
            uncategorized.append(p)
            continue
        m = p.main_category
        s = p.sub_category
        by_main_sub.setdefault(m, {}).setdefault(s, []).append(p)

    def sort_key(p: PaperEntry):
        if sort_by_year == "none":
            return 0
        y = p.year if p.year is not None else -9999
        return y

    reverse = sort_by_year == "desc"

    lines: List[str] = []
    lines.append("# 文献综述整理草稿（按大类/小类分组）\n")

    for m_name in main_name_order:
        if m_name not in by_main_sub:
            continue

        # ── 大类标题 ── #
        lines.append(f"\n## {m_name}\n")

        sub_dict = by_main_sub[m_name]

        # 该大类的所有“小类名字”顺序：先按照 schema 中 children，最后再放 None / 未在 children 中的
        declared_children = schema[m_name].children
        extra_children = [
            s for s in sub_dict.keys()
            if s is not None and s not in declared_children
        ]
        all_sub_names: List[Optional[str]] = declared_children + extra_children + [None]

        for s_name in all_sub_names:
            items = sub_dict.get(s_name, [])
            if not items:
                continue

            heading = s_name if s_name is not None else "未指定小类"
            lines.append(f"\n### {heading}\n")

            # 一句总起
            overview = _build_subcategory_overview(heading, items)
            lines.append(overview + "\n")

            # 文献条目列表
            items_sorted = sorted(items, key=sort_key, reverse=reverse)
            for p in items_sorted:
                authors_str = ", ".join(p.authors) if p.authors else p.first_author
                year_str = str(p.year) if p.year is not None else "n.d."
                venue_str = p.venue or ""
                basic_info = f"{authors_str} ({year_str})"
                if venue_str:
                    basic_info += f", *{venue_str}*"
                # 一行：basic_info + 换行 + 一句总结
                lines.append(f"- **{basic_info}**  \n  {p.summary_zh}")

            # 小类总结段
            summary_para = _build_subcategory_summary(heading, items)
            lines.append("\n" + summary_para + "\n")

    # ── 未分类部分 ── #
    if uncategorized:
        lines.append("\n## 未分类\n")
        items_sorted = sorted(uncategorized, key=sort_key, reverse=reverse)
        overview = _build_subcategory_overview("未指定小类", items_sorted)
        lines.append(overview + "\n")

        for p in items_sorted:
            authors_str = ", ".join(p.authors) if p.authors else p.first_author
            year_str = str(p.year) if p.year is not None else "n.d."
            venue_str = p.venue or ""
            basic_info = f"{authors_str} ({year_str})"
            if venue_str:
                basic_info += f", *{venue_str}*"
            lines.append(f"- **{basic_info}**  \n  {p.summary_zh}")

        summary_para = _build_subcategory_summary("未指定小类", items_sorted)
        lines.append("\n" + summary_para + "\n")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n✅ 已导出 Markdown 到: {out_path}")


# ───────────────────── CLI ───────────────────── #

def build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="从 RIS 文献生成分层中文综述 Markdown 草稿"
    )
    p.add_argument(
        "--ris",
        type=Path,
        required=True,
        help="输入的 .ris 文件路径",
    )
    p.add_argument(
        "--out-dir",
        type=Path,
        required=True,
        help="输出目录，将在其中生成 review.md",
    )
    p.add_argument(
        "--categories",
        type=Path,
        default=None,
        help="类别结构 YAML 文件（可选）。若不给则用 --n-main/--m-sub 自动生成。",
    )
    p.add_argument(
        "--n-main",
        type=int,
        default=None,
        help="自动生成类别结构的大类数量 N（可选）。",
    )
    p.add_argument(
        "--m-sub",
        type=int,
        default=None,
        help="自动生成类别结构时，每个大类下面的小类数量 M（可选）。",
    )
    p.add_argument(
        "--sort-by-year",
        type=str,
        default="none",
        choices=["none", "asc", "desc"],
        help="每个小类内部是否按年份排序。",
    )
    return p


def main():
    args = build_argparser().parse_args()

    ris_path: Path = args.ris
    out_dir: Path = args.out_dir
    cat_yaml: Optional[Path] = args.categories
    n_main: Optional[int] = args.n_main
    m_sub: Optional[int] = args.m_sub
    sort_by_year: str = args.sort_by_year

    out_dir.mkdir(parents=True, exist_ok=True)
    out_md = out_dir / "review.md"

    # 1. 解析 RIS
    papers = parse_ris(ris_path)

    # 2. 构造 / 载入 schema
    if cat_yaml is not None:
        print(f"使用 YAML 定义的类别结构: {cat_yaml}")
        schema = load_schema_from_yaml(cat_yaml)
    else:
        print(f"未提供 YAML，使用数字参数自动构造 schema：n_main={n_main}, m_sub={m_sub}")
        schema = suggest_schema_from_papers_auto(papers, n_main, m_sub)

    # 3. 分类（当前为占位实现）
    assign_categories(papers, schema)

    # 4. 补充中文总结
    fill_all_summaries(papers)

    # 5. 导出 Markdown
    export_markdown(papers, schema, out_md, sort_by_year=sort_by_year)


if __name__ == "__main__":
    main()

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

from .models import CategoryNode, PaperEntry

try:  # pragma: no cover - optional dependency
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - handled gracefully
    yaml = None


def build_simple_auto_schema() -> Dict[str, CategoryNode]:
    name = "自动归类/未分类"
    return {name: CategoryNode(name=name, parent=None, children=[])}


def suggest_schema_from_papers_auto(
    papers: List[PaperEntry],
    n_main: Optional[int],
    m_sub: Optional[int],
) -> Dict[str, CategoryNode]:
    if not n_main or n_main <= 0:
        return build_simple_auto_schema()

    if m_sub is None or m_sub < 0:
        m_sub = 0

    schema: Dict[str, CategoryNode] = {}
    for main_index in range(1, n_main + 1):
        main_name = f"自动主类{main_index}"
        children: List[str] = []
        for sub_index in range(1, m_sub + 1):
            sub_name = f"{main_name}-子类{sub_index}"
            children.append(sub_name)
            schema[sub_name] = CategoryNode(name=sub_name, parent=main_name, children=[])
        schema[main_name] = CategoryNode(name=main_name, parent=None, children=children)

    return schema


def load_schema_from_yaml(path: Path) -> Dict[str, CategoryNode]:
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

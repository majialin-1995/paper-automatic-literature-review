from __future__ import annotations

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple

from .models import CategoryNode, PaperEntry


@dataclass(frozen=True)
class CategorySelection:
    main: Optional[str]
    sub: Optional[str]


class ClassificationFailed(RuntimeError):
    """Raised when the category assigner cannot determine a label."""


class CategoryAssigner(ABC):
    """Base interface for assigning categories to papers."""

    @abstractmethod
    def assign(self, papers: List[PaperEntry], schema: Dict[str, CategoryNode]) -> None:
        """Populate the ``main_category``/``sub_category`` fields in-place."""


def _extract_json(payload: str) -> Optional[Dict[str, Any]]:
    try:
        return json.loads(payload)
    except json.JSONDecodeError:
        start = payload.find("{")
        end = payload.rfind("}")
        if start != -1 and end != -1 and start < end:
            try:
                return json.loads(payload[start : end + 1])
            except json.JSONDecodeError:
                return None
        return None


def _match_choice(candidate: str, options: Iterable[str]) -> Optional[str]:
    candidate = candidate.strip()
    if not candidate:
        return None
    exact = {option: option for option in options}
    if candidate in exact:
        return candidate
    lower_map = {option.lower(): option for option in options}
    return lower_map.get(candidate.lower())


def _format_schema(schema: Dict[str, CategoryNode]) -> Tuple[str, Dict[str, List[str]]]:
    main_nodes = sorted(
        (node for node in schema.values() if node.parent is None),
        key=lambda node: node.name,
    )
    description_lines: List[str] = []
    mapping: Dict[str, List[str]] = {}
    for main in main_nodes:
        children = schema[main.name].children
        mapping[main.name] = list(children)
        if children:
            joined = "、".join(children)
            description_lines.append(f"- {main.name}：{joined}")
        else:
            description_lines.append(f"- {main.name}：无子类")
    return "\n".join(description_lines), mapping


def _build_prompt(schema_text: str, paper: PaperEntry) -> str:
    authors = ", ".join(paper.authors)
    return (
        "你是一名中文学术综述助手，将论文归入预定义的分类结构。\n"
        "可选的大类及其子类如下：\n"
        f"{schema_text}\n\n"
        "请阅读论文信息，并从上述列表中返回 main_category 与 sub_category。"
        "输出 JSON，对应字段为 main_category、sub_category；若无合适子类可设为空字符串。\n\n"
        f"标题：{paper.title or '未知标题'}\n"
        f"作者：{authors or paper.first_author}\n"
        f"摘要：{paper.abstract or '（暂无摘要）'}"
    )


class LLMCategoryAssigner(CategoryAssigner):
    """Assign categories by querying a chat-completions compatible client."""

    def __init__(self, client: Any, *, model: str = "deepseek-chat") -> None:
        self.client = client
        self.model = model

    def assign(self, papers: List[PaperEntry], schema: Dict[str, CategoryNode]) -> None:
        schema_text, mapping = _format_schema(schema)
        if not mapping:
            raise ClassificationFailed("schema 中缺少大类定义，无法完成模型分类。")
        for paper in papers:
            try:
                selection = self._classify_single(paper, schema_text, mapping)
            except Exception as exc:  # pragma: no cover - depends on remote API behaviour
                raise ClassificationFailed(str(exc)) from exc

            if selection.main is None:
                raise ClassificationFailed(
                    f"模型未返回有效主类：{paper.title or paper.first_author}"
                )

            paper.main_category = selection.main
            if selection.sub and selection.sub in mapping.get(selection.main, []):
                paper.sub_category = selection.sub
            else:
                paper.sub_category = None

    def _classify_single(
        self,
        paper: PaperEntry,
        schema_text: str,
        mapping: Dict[str, List[str]],
    ) -> CategorySelection:
        prompt = _build_prompt(schema_text, paper)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            stream=False,
        )
        content = response.choices[0].message.content or ""
        data = _extract_json(content) or {}
        main = _match_choice(str(data.get("main_category", "")), mapping.keys())
        sub = None
        if main is not None:
            sub = _match_choice(str(data.get("sub_category", "")), mapping.get(main, []))
        return CategorySelection(main=main, sub=sub)

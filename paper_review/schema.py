from __future__ import annotations

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence

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


class SchemaSuggestionFailed(RuntimeError):
    """Raised when the LLM-backed schema builder cannot infer a valid schema."""


class SchemaBuilder(ABC):
    """Abstract interface for producing a category schema."""

    @abstractmethod
    def build(
        self,
        papers: List[PaperEntry],
        categories_yaml: Optional[Path],
        n_main: Optional[int],
        m_sub: Optional[int],
    ) -> Dict[str, CategoryNode]:
        """Return a mapping of category name to :class:`CategoryNode`."""


class DefaultSchemaBuilder(SchemaBuilder):
    """Replicates the historical behaviour based on YAML or numeric hints."""

    def build(
        self,
        papers: List[PaperEntry],
        categories_yaml: Optional[Path],
        n_main: Optional[int],
        m_sub: Optional[int],
    ) -> Dict[str, CategoryNode]:
        if categories_yaml is not None:
            print(f"使用 YAML 定义的类别结构: {categories_yaml}")
            return load_schema_from_yaml(categories_yaml)
        if n_main is None and m_sub is None:
            print("未提供 YAML 和自动构造参数，使用兜底类别结构。")
            return build_simple_auto_schema()
        print(f"未提供 YAML，使用数字参数自动构造 schema：n_main={n_main}, m_sub={m_sub}")
        return suggest_schema_from_papers_auto(papers, n_main, m_sub)


class LLMSchemaBuilder(DefaultSchemaBuilder):
    """Infer schema names by prompting a chat-completions compatible model."""

    def __init__(self, client: Any, *, model: str = "deepseek-chat") -> None:
        self.client = client
        self.model = model

    def build(
        self,
        papers: List[PaperEntry],
        categories_yaml: Optional[Path],
        n_main: Optional[int],
        m_sub: Optional[int],
    ) -> Dict[str, CategoryNode]:
        if categories_yaml is not None:
            return super().build(papers, categories_yaml, n_main, m_sub)

        try:
            print("未提供 YAML，使用大模型自动推断类别结构。")
            return self._build_with_llm(papers, n_main, m_sub)
        except SchemaSuggestionFailed as exc:
            print(f"⚠️ 大模型推断类别结构失败，将退回默认策略：{exc}")
            return super().build(papers, None, n_main, m_sub)

    def _build_with_llm(
        self,
        papers: List[PaperEntry],
        n_main: Optional[int],
        m_sub: Optional[int],
    ) -> Dict[str, CategoryNode]:
        prompt = self._build_prompt(papers, n_main, m_sub)
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
        main_categories = data.get("main_categories")
        if not isinstance(main_categories, list) or not main_categories:
            raise SchemaSuggestionFailed("模型未返回 main_categories 列表。")

        normalized = self._normalize_main_categories(main_categories, n_main, m_sub)
        if not normalized:
            raise SchemaSuggestionFailed("模型返回的类别结构为空。")
        return normalized

    def _build_prompt(
        self,
        papers: List[PaperEntry],
        n_main: Optional[int],
        m_sub: Optional[int],
    ) -> str:
        instructions: List[str] = [
            "你是一名中文学术综述助手，需要根据给定的文献列表提出主类(main_category)和子类(sub_category)结构。",
            "请基于文献主题进行归纳，分类名称保持 4-10 个汉字，且避免与原文标题重复。",
        ]
        if n_main is not None and n_main > 0:
            instructions.append(f"主类数量需为 {n_main} 个。")
        else:
            instructions.append("主类数量可为 3-6 个，根据文献聚类情况自定。")

        if m_sub is not None and m_sub > 0:
            instructions.append(
                f"每个主类下建议提供不超过 {m_sub} 个子类，可少于该数量以保持语义清晰。"
            )
        elif m_sub == 0:
            instructions.append("无需提供子类，sub_categories 应设为空数组。")
        else:
            instructions.append("如有需要，可为每个主类提供 0-3 个子类。")

        instructions.append(
            "请输出 JSON，格式为 {\"main_categories\": [{\"name\": \"...\", \"sub_categories\": [\"...\"]}, ...]}。"
        )
        instructions.append("名称中不要带序号或冒号，保持纯文本描述。")

        paper_descriptions = "\n".join(self._render_paper_digest(paper) for paper in papers)
        return "\n".join(instructions) + "\n\n文献列表：\n" + paper_descriptions

    def _render_paper_digest(self, paper: PaperEntry) -> str:
        abstract = paper.abstract.strip() if paper.abstract else "（暂无摘要）"
        truncated = _truncate(abstract, limit=400)
        year = f"，年份：{paper.year}" if paper.year is not None else ""
        return (
            f"- 标题：{paper.title or '未命名论文'}\n"
            f"  主要作者：{', '.join(paper.authors) or paper.first_author}{year}\n"
            f"  摘要：{truncated}"
        )

    def _normalize_main_categories(
        self,
        main_categories: Sequence[Any],
        n_main: Optional[int],
        m_sub: Optional[int],
    ) -> Dict[str, CategoryNode]:
        schema: Dict[str, CategoryNode] = {}
        processed: List[Dict[str, Any]] = []
        for item in main_categories:
            if not isinstance(item, dict):
                continue
            name = str(item.get("name", "")).strip()
            if not name:
                continue
            subs_raw = item.get("sub_categories", [])
            subs: List[str] = []
            if isinstance(subs_raw, Iterable) and not isinstance(subs_raw, (str, bytes)):
                seen_subs: set[str] = set()
                for entry in subs_raw:
                    sub_name = str(entry).strip()
                    if sub_name and sub_name not in seen_subs:
                        subs.append(sub_name)
                        seen_subs.add(sub_name)
            processed.append({"name": name, "sub_categories": subs})

        if n_main is not None and n_main > 0:
            if len(processed) < n_main:
                raise SchemaSuggestionFailed("模型返回的主类数量少于期望值。")
            processed = processed[:n_main]

        for item in processed:
            name = item["name"]
            children = item["sub_categories"]
            if m_sub is not None:
                if m_sub <= 0:
                    children = []
                elif len(children) > m_sub:
                    children = children[:m_sub]
            schema[name] = CategoryNode(name=name, parent=None, children=children)
            for child in children:
                schema[child] = CategoryNode(name=child, parent=name, children=[])

        return schema


def _truncate(text: str, *, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 1)] + "…"


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

from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from .classification import assign_categories
from .exporters.markdown import export_markdown
from .models import PaperEntry
from .parsing import registry
from .schema import build_simple_auto_schema, load_schema_from_yaml, suggest_schema_from_papers_auto
from .summarization.base import Summarizer, TemplateSummarizer


class ReviewPipeline:
    """High-level orchestration for generating structured literature reviews."""

    def __init__(self, summarizer: Optional[Summarizer] = None) -> None:
        self.summarizer = summarizer or TemplateSummarizer()

    def parse(self, source: Path) -> List[PaperEntry]:
        parser = registry.get(source.suffix)
        papers = parser.parse(source)
        print(f"解析 {source.name} 完成，共 {len(papers)} 篇文献。")
        return papers

    def summarize(self, papers: List[PaperEntry]) -> None:
        for paper in papers:
            paper.summary_zh = self.summarizer.summarize(paper)

    def build_schema(
        self,
        papers: List[PaperEntry],
        categories_yaml: Optional[Path],
        n_main: Optional[int],
        m_sub: Optional[int],
    ):
        if categories_yaml is not None:
            print(f"使用 YAML 定义的类别结构: {categories_yaml}")
            return load_schema_from_yaml(categories_yaml)
        if n_main is None and m_sub is None:
            print("未提供 YAML 和自动构造参数，使用兜底类别结构。")
            return build_simple_auto_schema()
        print(f"未提供 YAML，使用数字参数自动构造 schema：n_main={n_main}, m_sub={m_sub}")
        return suggest_schema_from_papers_auto(papers, n_main, m_sub)

    def run(
        self,
        source: Path,
        out_dir: Path,
        categories_yaml: Optional[Path] = None,
        n_main: Optional[int] = None,
        m_sub: Optional[int] = None,
        sort_by_year: str = "none",
    ) -> Path:
        out_dir.mkdir(parents=True, exist_ok=True)
        out_md = out_dir / "review.md"

        papers = self.parse(source)
        schema = self.build_schema(papers, categories_yaml, n_main, m_sub)
        assign_categories(papers, schema)
        self.summarize(papers)
        export_markdown(papers, schema, out_md, sort_by_year=sort_by_year)
        print(f"\n✅ 已导出 Markdown 到: {out_md}")
        return out_md

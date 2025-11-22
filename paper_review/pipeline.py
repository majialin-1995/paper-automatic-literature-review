from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

from .classification import CategoryAssigner
from .exporters.markdown import export_markdown
from .models import CategoryNode, PaperEntry
from .parsing import registry
from .progress import ProgressReporter
from .schema import DefaultSchemaBuilder, SchemaBuilder
from .summarization.base import Summarizer


class ReviewPipeline:
    """High-level orchestration for generating structured literature reviews."""

    def __init__(
        self,
        summarizer: Summarizer,
        category_assigner: CategoryAssigner,
        schema_builder: Optional[SchemaBuilder] = None,
    ) -> None:
        if summarizer is None:
            raise ValueError("必须提供基于大模型的 summarizer 实例。")
        if category_assigner is None:
            raise ValueError("必须提供基于大模型的分类器实例。")
        self.summarizer = summarizer
        self.category_assigner = category_assigner
        self.schema_builder = schema_builder or DefaultSchemaBuilder()

    def parse(self, source: Path, input_format: Optional[str] = None) -> List[PaperEntry]:
        parser_key = input_format or source.suffix
        parser = registry.get(parser_key)
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
    ) -> Dict[str, CategoryNode]:
        return self.schema_builder.build(papers, categories_yaml, n_main, m_sub)

    def run(
        self,
        source: Path,
        out_dir: Path,
        categories_yaml: Optional[Path] = None,
        n_main: Optional[int] = None,
        m_sub: Optional[int] = None,
        sort_by_year: str = "none",
        input_format: Optional[str] = None,
    ) -> Path:
        out_dir.mkdir(parents=True, exist_ok=True)
        out_md = out_dir / "review.md"

        progress = ProgressReporter(total_steps=5)
        progress.start("🚀 开始自动文献综述流程，共 5 个步骤。")

        papers = self.parse(source, input_format=input_format)
        progress.advance("解析文献源文件")

        schema = self.build_schema(papers, categories_yaml, n_main, m_sub)
        progress.advance("构建分类体系")

        self.category_assigner.assign(papers, schema)
        progress.advance("调用模型完成分类")

        self.summarize(papers)
        progress.advance("生成中文摘要")

        export_markdown(papers, schema, out_md, sort_by_year=sort_by_year)
        progress.advance("导出 Markdown 报告")
        print(f"\n✅ 已导出 Markdown 到: {out_md}")
        return out_md

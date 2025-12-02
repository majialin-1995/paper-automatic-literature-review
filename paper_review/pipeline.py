from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Tuple

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
        source: Optional[Path],
        categorized_dir: Optional[Path] = None,
        out_dir: Path,
        categories_yaml: Optional[Path] = None,
        n_main: Optional[int] = None,
        m_sub: Optional[int] = None,
        sort_by_year: str = "none",
        input_format: Optional[str] = None,
    ) -> Path:
        if (source is None) == (categorized_dir is None):
            raise ValueError("必须通过 --input 或 --categorized-dir 提供且仅提供一种输入来源。")
        if categorized_dir is not None and (
            categories_yaml is not None or n_main is not None or m_sub is not None
        ):
            print("已提供 --categorized-dir，--categories/--n-main/--m-sub 参数将被忽略。")
        out_dir.mkdir(parents=True, exist_ok=True)
        out_md = out_dir / "review.md"

        if categorized_dir is not None:
            progress = ProgressReporter(total_steps=4)
            progress.start("🚀 开始文献综述流程（按文件分大类），共 4 个步骤。")

            papers, grouped = self._parse_categorized_dir(categorized_dir, input_format=input_format)
            progress.advance("解析分组文献文件")

            schema = self._build_schema_from_grouping(grouped)
            progress.advance("根据文件名固定分类")

            self.summarize(papers)
            progress.advance("生成中文摘要")
        else:
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

    def _parse_categorized_dir(
        self, categorized_dir: Path, *, input_format: Optional[str]
    ) -> Tuple[List[PaperEntry], Dict[str, List[PaperEntry]]]:
        if not categorized_dir.is_dir():
            raise ValueError(f"{categorized_dir} 不是有效的目录。")

        papers: List[PaperEntry] = []
        grouped: Dict[str, List[PaperEntry]] = {}
        for entry in sorted(categorized_dir.iterdir()):
            if not entry.is_file():
                continue
            category_name = entry.stem
            parser_key = input_format or entry.suffix
            parser = registry.get(parser_key)
            parsed = parser.parse(entry)
            print(f"解析 {entry.name} 完成，映射到大类“{category_name}”，共 {len(parsed)} 篇文献。")
            for paper in parsed:
                paper.main_category = category_name
            papers.extend(parsed)
            grouped[category_name] = parsed

        if not papers:
            raise ValueError(f"目录 {categorized_dir} 下未发现可解析的文献文件。")

        return papers, grouped

    def _build_schema_from_grouping(
        self, grouped: Dict[str, List[PaperEntry]]
    ) -> Dict[str, CategoryNode]:
        schema: Dict[str, CategoryNode] = {}
        for category_name in sorted(grouped):
            schema[category_name] = CategoryNode(name=category_name, parent=None, children=[])
        return schema

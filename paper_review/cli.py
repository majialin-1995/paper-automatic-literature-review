from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional

from .pipeline import ReviewPipeline


def build_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="从文献引用文件生成分层中文综述 Markdown 草稿"
    )
    parser.add_argument("--input", type=Path, required=True, help="输入的文献文件路径（支持 .ris 等格式）")
    parser.add_argument("--out-dir", type=Path, required=True, help="输出目录，将在其中生成 review.md")
    parser.add_argument(
        "--categories",
        type=Path,
        default=None,
        help="类别结构 YAML 文件（可选）。若不给则用 --n-main/--m-sub 自动生成。",
    )
    parser.add_argument(
        "--n-main",
        type=int,
        default=None,
        help="自动生成类别结构的大类数量 N（可选）。",
    )
    parser.add_argument(
        "--m-sub",
        type=int,
        default=None,
        help="自动生成类别结构时，每个大类下面的小类数量 M（可选）。",
    )
    parser.add_argument(
        "--sort-by-year",
        type=str,
        default="none",
        choices=["none", "asc", "desc"],
        help="每个小类内部是否按年份排序。",
    )
    return parser


def run_cli(args: Optional[argparse.Namespace] = None) -> Path:
    parser = build_argparser()
    parsed = parser.parse_args(args=args)

    pipeline = ReviewPipeline()
    return pipeline.run(
        source=parsed.input,
        out_dir=parsed.out_dir,
        categories_yaml=parsed.categories,
        n_main=parsed.n_main,
        m_sub=parsed.m_sub,
        sort_by_year=parsed.sort_by_year,
    )

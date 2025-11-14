from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Any, Optional

try:  # pragma: no cover - optional dependency
    from openai import OpenAI
except ImportError:  # pragma: no cover - graceful fallback when SDK is missing
    OpenAI = None  # type: ignore

from .classification import LLMCategoryAssigner
from .pipeline import ReviewPipeline
from .summarization.deepseek import DeepSeekSummarizer


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
    parser.add_argument(
        "--llm-api-key",
        type=str,
        default=None,
        help="DeepSeek/OpenAI API Key，可通过环境变量 DEEPSEEK_API_KEY 或 OPENAI_API_KEY 提供。",
    )
    parser.add_argument(
        "--llm-api-base",
        type=str,
        default=None,
        help="自定义 LLM 接口地址，可通过 DEEPSEEK_API_BASE/OPENAI_BASE_URL 指定。",
    )
    parser.add_argument(
        "--llm-model",
        type=str,
        default="deepseek-chat",
        help="用于摘要与分类的对话模型名称，默认为 deepseek-chat。",
    )
    return parser


def run_cli(args: Optional[argparse.Namespace] = None) -> Path:
    parser = build_argparser()
    parsed = parser.parse_args(args=args)

    client = _build_llm_client(parsed.llm_api_key, parsed.llm_api_base)
    pipeline = ReviewPipeline(
        summarizer=DeepSeekSummarizer(client, model=parsed.llm_model),
        category_assigner=LLMCategoryAssigner(client, model=parsed.llm_model),
    )
    return pipeline.run(
        source=parsed.input,
        out_dir=parsed.out_dir,
        categories_yaml=parsed.categories,
        n_main=parsed.n_main,
        m_sub=parsed.m_sub,
        sort_by_year=parsed.sort_by_year,
    )


def _build_llm_client(api_key: Optional[str], api_base: Optional[str]) -> Any:
    if OpenAI is None:
        raise RuntimeError(
            "未检测到 openai SDK，请先安装 `pip install openai` 以启用大模型工作流。"
        )

    resolved_key = api_key or os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not resolved_key:
        raise RuntimeError(
            "请通过 --llm-api-key 或环境变量 DEEPSEEK_API_KEY/OPENAI_API_KEY 提供大模型凭证。"
        )

    base_url = api_base or os.environ.get("DEEPSEEK_API_BASE") or os.environ.get("OPENAI_BASE_URL")
    kwargs = {"api_key": resolved_key}
    if base_url:
        kwargs["base_url"] = base_url
    return OpenAI(**kwargs)

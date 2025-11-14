from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

try:  # pragma: no cover - optional dependency
    from pydantic import BaseModel, ValidationError
except ImportError:  # pragma: no cover - fallback for environments without pydantic
    BaseModel = None  # type: ignore
    ValidationError = Exception  # type: ignore

from .base import SummaryFailed, Summarizer, TemplateSummarizer
from ..models import PaperEntry

_PROMPT_HEADER = (
    "请阅读以下文献题录信息，从中提取一个简洁的中文摘要。"
    "\n\n"
    "输出 JSON，包含 overview（1 句话总结）以及 bullet_points（2-4 条要点，每条不超过 60 字）。"
    "\n原始信息如下：\n"
)


if BaseModel is not None:

    class Summary(BaseModel):
        overview: str = ""
        bullet_points: List[str] = []

        def render(self) -> str:
            bullet_text = "；".join(point for point in self.bullet_points if point.strip())
            parts = [self.overview.strip(), bullet_text]
            return " ".join(part for part in parts if part)

else:

    @dataclass
    class Summary:  # type: ignore[override]
        overview: str = ""
        bullet_points: List[str] = field(default_factory=list)

        def render(self) -> str:
            bullet_text = "；".join(point for point in self.bullet_points if point.strip())
            parts = [self.overview.strip(), bullet_text]
            return " ".join(part for part in parts if part)


def _extract_json(content: str) -> Optional[Dict[str, Any]]:
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        start = content.find("{")
        end = content.rfind("}")
        if start != -1 and end != -1 and start < end:
            try:
                return json.loads(content[start : end + 1])
            except json.JSONDecodeError:
                return None
        return None


def normalize_summary(raw_json: Dict[str, Any]) -> Summary:
    payload = {
        "overview": raw_json.get("overview", ""),
        "bullet_points": raw_json.get("bullet_points", []),
    }
    if BaseModel is not None:
        try:
            return Summary(**payload)
        except ValidationError as exc:  # pragma: no cover - depends on model output
            raise SummaryFailed(str(exc)) from exc
    if not isinstance(payload["bullet_points"], list):
        payload["bullet_points"] = [str(payload["bullet_points"])]
    return Summary(overview=str(payload["overview"]), bullet_points=[str(item) for item in payload["bullet_points"]])


def summarize(text: str, client: Any) -> Summary:
    """
    调用 DeepSeek-chat 完成一次摘要。

    与原始实现不同，此处不再根据 token 上限回退，只执行一次调用，
    并保证最终返回 Summary 对象。
    """
    prompt = _PROMPT_HEADER + text
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
        stream=False,
    )
    content = response.choices[0].message.content or ""
    raw_json = _extract_json(content) or {}
    return normalize_summary(raw_json)


class DeepSeekSummarizer(Summarizer):
    """Summarizer backed by the DeepSeek-chat model."""

    def __init__(self, client: Any, fallback: Optional[Summarizer] = None) -> None:
        self.client = client
        self.fallback = fallback or TemplateSummarizer()

    def summarize(self, paper: PaperEntry) -> str:
        text = f"标题：{paper.title}\n作者：{', '.join(paper.authors)}\n摘要：{paper.abstract}"
        try:
            summary = summarize(text, self.client)
            return summary.render()
        except Exception as exc:  # pragma: no cover - depends on API availability
            if self.fallback:
                return self.fallback.summarize(paper)
            raise SummaryFailed(str(exc)) from exc

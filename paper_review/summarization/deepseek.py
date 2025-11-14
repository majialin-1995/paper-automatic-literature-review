from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

try:  # pragma: no cover - optional dependency
    from pydantic import BaseModel, ValidationError
except ImportError:  # pragma: no cover - fallback for environments without pydantic
    BaseModel = None  # type: ignore
    ValidationError = Exception  # type: ignore

from .base import SummaryFailed, Summarizer
from ..models import PaperEntry

_PROMPT_HEADER = (
    "请阅读以下文献信息，总结研究所解决的问题(problem)、提出的方案(approach)"
    "以及最突出的贡献(impact)。"
    "\n\n"
    "输出 JSON，对应键为 problem、approach、impact，每个字段均为不超过 60 字的中文句子。"
    "\n如果缺少信息，可留空字符串。\n原始信息如下：\n"
)


if BaseModel is not None:

    class Summary(BaseModel):
        problem: str = ""
        approach: str = ""
        impact: str = ""

        def render(self, paper: PaperEntry) -> str:
            prefix = f"{paper.first_author}等人"
            title = paper.title.strip() if paper.title else ""
            if title:
                prefix += f"针对《{title}》研究"
            segments: List[str] = []
            if self.approach.strip():
                segments.append(f"提出{self.approach.strip()}")
            if self.problem.strip():
                segments.append(f"以解决{self.problem.strip()}")
            if self.impact.strip():
                segments.append(self.impact.strip())
            body = "，".join(segments)
            return f"{prefix}，{body}" if body else prefix

else:

    @dataclass
    class Summary:  # type: ignore[override]
        problem: str = ""
        approach: str = ""
        impact: str = ""

        def render(self, paper: PaperEntry) -> str:
            prefix = f"{paper.first_author}等人"
            title = paper.title.strip() if paper.title else ""
            if title:
                prefix += f"针对《{title}》研究"
            segments: List[str] = []
            if self.approach.strip():
                segments.append(f"提出{self.approach.strip()}")
            if self.problem.strip():
                segments.append(f"以解决{self.problem.strip()}")
            if self.impact.strip():
                segments.append(self.impact.strip())
            body = "，".join(segments)
            return f"{prefix}，{body}" if body else prefix


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
        "problem": raw_json.get("problem", ""),
        "approach": raw_json.get("approach", ""),
        "impact": raw_json.get("impact", ""),
    }
    if BaseModel is not None:
        try:
            return Summary(**payload)
        except ValidationError as exc:  # pragma: no cover - depends on model output
            raise SummaryFailed(str(exc)) from exc
    return Summary(
        problem=str(payload["problem"]),
        approach=str(payload["approach"]),
        impact=str(payload["impact"]),
    )


def summarize(text: str, client: Any, *, model: str = "deepseek-chat") -> Summary:
    """调用 DeepSeek-chat 完成一次摘要，若解析失败则抛出 :class:`SummaryFailed`."""
    prompt = _PROMPT_HEADER + text
    print("\n🧠 摘要请求 Prompt:\n" + prompt + "\n")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
        stream=False,
    )
    content = response.choices[0].message.content or ""
    print("📨 模型返回 (摘要)：\n" + content + "\n")
    raw_json = _extract_json(content) or {}
    return normalize_summary(raw_json)


class DeepSeekSummarizer(Summarizer):
    """Summarizer backed by the DeepSeek-chat model."""

    def __init__(self, client: Any, *, model: str = "deepseek-chat") -> None:
        self.client = client
        self.model = model

    def summarize(self, paper: PaperEntry) -> str:
        text = f"标题：{paper.title}\n作者：{', '.join(paper.authors)}\n摘要：{paper.abstract}"
        try:
            summary = summarize(text, self.client, model=self.model)
            rendered = summary.render(paper)
            print("📝 摘要结果：" + rendered + "\n")
            return rendered
        except Exception as exc:  # pragma: no cover - depends on API availability
            raise SummaryFailed(str(exc)) from exc

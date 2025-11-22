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
    "请阅读以下文献信息，总结该研究所解决的问题(problem)、提出的方案(approach)"
    "以及最突出的贡献(impact)，并将三者融合为一句话进行描述。"
    "\n\n"
    "输出要求：\n"
    "1. 只输出一个 JSON 对象，包含一个字段：summary。\n"
    "2. summary 为一段不超过 100 字的中文句子。\n"
    "3. 句式可参考：“针对……问题，提出……方法，并……。”，也可适当变体。\n"
    "4. 不要输出多余说明文字。\n"
    "\n原始信息如下：\n"
)


if BaseModel is not None:

    class Summary(BaseModel):
        summary: str = ""

        def render(self, paper: PaperEntry) -> str:
            text = self.summary.strip()
            if text:
                return f"{paper.first_author}等人"+"{"+paper.title+"}"+text

            # 回退：如果 summary 为空，就至少给出“作者+标题”
            author = f"{paper.first_author}等人"
            title = paper.title.strip() if paper.title else ""
            title_part = f"《{title}》" if title else ""
            return f"{author}{title_part}"

else:

    @dataclass
    class Summary:  # type: ignore[override]
        summary: str = ""

        def render(self, paper: PaperEntry) -> str:
            text = self.summary.strip()
            if text:
                return text

            # 回退：如果 summary 为空，就至少给出“作者+标题”
            author = f"{paper.first_author}等人"
            title = paper.title.strip() if paper.title else ""
            title_part = f"《{title}》" if title else ""
            return f"{author}{title_part}"


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
        "summary": raw_json.get("summary", ""),
    }
    if BaseModel is not None:
        try:
            return Summary(**payload)
        except ValidationError as exc:  # pragma: no cover - depends on model output
            raise SummaryFailed(str(exc)) from exc
    return Summary(summary=str(payload["summary"]))


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
        text = (
            f"标题：{paper.title}\n"
            f"作者：{', '.join(paper.authors)}\n"
            f"摘要：{paper.abstract}"
        )
        try:
            summary = summarize(text, self.client, model=self.model)
            rendered = summary.render(paper)
            print("📝 摘要结果：" + rendered + "\n")
            return rendered
        except Exception as exc:  # pragma: no cover - depends on API availability
            raise SummaryFailed(str(exc)) from exc

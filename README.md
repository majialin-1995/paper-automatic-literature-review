# paper-automatic-literature-review

通过 RIS 等书目文件自动形成分层的国内外研究现状总结。

## 功能亮点

- ✅ 支持解析 `.ris` 文献引用文件，并可按需扩展到其它格式。
- ✅ 依据 YAML 或自动生成的大类/小类结构输出分层 Markdown 草稿。
- ✅ 预留 LLM 摘要接口，默认为模板摘要，也可无缝接入 DeepSeek-chat。
- ✅ 完整的命令行接口，便于在自动化流程中集成。

## 快速开始

```bash
pip install -r requirements.txt  # 若仅使用模板摘要，可跳过
python main.py \
  --input examples/papers.ris \
  --out-dir runs/review \
  --n-main 3 --m-sub 2 \
  --sort-by-year desc
```

执行完成后，会在 `runs/review/review.md` 中生成分层综述草稿。

> **提示**：若提供 `--categories categories.yaml`，将优先使用该文件定义的大类/小类结构。

## 项目结构

```
paper_review/
├── cli.py                  # 命令行解析与入口
├── classification.py       # 文献分类逻辑（当前为占位实现）
├── exporters/markdown.py   # Markdown 导出
├── models.py               # 核心数据结构
├── parsing/                # 书目文件解析器
│   ├── base.py             # Parser 抽象类与注册表
│   └── ris.py              # RIS 解析实现
├── pipeline.py             # Pipeline 编排
└── summarization/          # 摘要生成模块
    ├── base.py             # 摘要抽象类 & 模板实现
    └── deepseek.py         # DeepSeek-chat 摘要实现
```

模块划分采用「基础类 + 扩展实现」的结构，后续在 `parsing/` 中新增 `.bib` 等格式解析器，或在 `summarization/` 中扩展其它模型时，只需继承相应基类并注册即可。

## DeepSeek-chat 摘要

`paper_review/summarization/deepseek.py` 提供了一个 `DeepSeekSummarizer`，基于用户提供的 `OpenAI`/`deepseek` 客户端调用 DeepSeek-chat 生成摘要。实现遵循以下约束：

- 直接执行一次模型调用，不再根据 token 上限回退重试。
- 强制要求模型返回 JSON，并通过 `Summary`（Pydantic 或数据类）进行结构化校验。
- 在模型调用失败时，自动回退到模板摘要，保证流程可用性。

使用方式示例：

```python
from openai import OpenAI
from paper_review.pipeline import ReviewPipeline
from paper_review.summarization.deepseek import DeepSeekSummarizer

client = OpenAI(api_key="<your-key>")
pipeline = ReviewPipeline(summarizer=DeepSeekSummarizer(client))
pipeline.run(source=Path("papers.ris"), out_dir=Path("runs/review"))
```

> **依赖**：若需要 LLM 摘要，请确保安装 `openai>=1.0`（或 DeepSeek 官方 SDK）以及 `pydantic`。

## 扩展指南

1. **新增解析器（如 `.bib`）**
   - 在 `paper_review/parsing/` 目录下创建新模块，继承 `BibliographyParser`。
   - 在模块底部通过 `registry.register(".bib", CustomParser())` 注册。

2. **自定义分类器**
   - 替换 `classification.py` 中的 `assign_categories` 实现，或新增策略类。

3. **接入其它摘要模型**
   - 继承 `Summarizer`，实现 `summarize` 方法，并注入到 `ReviewPipeline`。

## 开发说明

- Python 版本建议 >= 3.9。
- 模板摘要与 RIS 解析均为纯标准库实现，便于快速启动。
- 可在 `tests/` 或 `examples/` 目录（待创建）中补充样例，便于回归验证。

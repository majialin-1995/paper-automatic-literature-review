# paper-automatic-literature-review

通过 RIS、RefWorks 等书目文件自动形成分层的国内外研究现状总结。

## 功能亮点

- ✅ 支持解析 `.ris` 与 RefWorks `.txt`/`.refworks` 文献引用文件，并可按需扩展到其它格式。
- ✅ 依据 YAML 或大模型自动归纳的大类/小类结构输出分层 Markdown 草稿。
- ✅ 摘要与分类全程由大模型驱动，内置 DeepSeek-chat 接入示例。
- ✅ 完整的命令行接口，便于在自动化流程中集成。

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置大模型 API Key（DeepSeek 或 OpenAI 二选一）
export DEEPSEEK_API_KEY="sk-xxx"   # 或设置 OPENAI_API_KEY

# 3. 准备输入 RIS/RefWorks 文件并运行管线
python main.py \
  --input examples/papers.ris \
  --out-dir runs/review \
  --n-main 3 --m-sub 2 \
  --sort-by-year desc \
  --llm-model deepseek-chat

# RefWorks 导出通常以 `.txt` 或 `.refworks` 结尾，可通过参数指定格式：
python main.py \
  --input examples/papers_refworks.txt \
  --out-dir runs/review \
  --sort-by-year desc \
  --input-format refworks \
  --llm-model deepseek-chat

python main.py --input examples/papers.ris --out-dir runs/review --categories examples/categories.yaml --sort-by-year desc --llm-model deepseek-chat
```

执行完成后，会在 `runs/review/review.md` 中生成分层综述草稿。

> **提示**：若提供 `--categories categories.yaml`，将优先使用该文件定义的大类/小类结构。

### 输入格式选择

- 通过 `--input-format` 显式指定书目格式（支持 `ris`、`refworks`），避免因文件后缀不规范导致识别失败。
- 未显式指定时，会根据文件后缀自动匹配已注册的解析器（如 `.ris`、`.refworks`、`.txt`）。

### 运行流程说明

1. **解析输入**：`paper_review/parsing/ris.py` / `paper_review/parsing/refworks.py` 会读取 `.ris` 或 RefWorks 文件并转换为内部的 `Paper` 数据结构。
2. **推断类别结构**：若未提供 `categories.yaml`，`paper_review/schema.py` 中的 `LLMSchemaBuilder` 会汇总整个 RIS 内容并调用大模型推导主类/子类名称，必要时可根据 `--n-main/--m-sub` 控制数量。
3. **自动分类与摘要**：`paper_review/classification.py` 和 `paper_review/summarization/` 下的模型分别调用 LLM 为文献打上主/子类并生成结构化摘要。
4. **Markdown 导出**：`paper_review/exporters/markdown.py` 将分层信息渲染到 `review.md`。

目前项目仅输出 Markdown 综述，不包含 `.ris` 转 CSV 的列表导出能力；若需要表格形式，可在导出的 `review.md` 基础上自行转换或扩展新的导出器。

## 项目结构

```
paper_review/
├── cli.py                  # 命令行解析与入口
├── classification.py       # 文献分类逻辑（仅 LLM 实现）
├── exporters/markdown.py   # Markdown 导出
├── models.py               # 核心数据结构
├── parsing/                # 书目文件解析器
│   ├── base.py             # Parser 抽象类与注册表
│   ├── refworks.py         # RefWorks 解析实现
│   └── ris.py              # RIS 解析实现
├── schema.py               # 类别结构定义与 LLM 推断
├── pipeline.py             # Pipeline 编排
└── summarization/          # 摘要生成模块
    ├── base.py             # 摘要抽象类
    └── deepseek.py         # DeepSeek-chat 摘要实现
```

模块划分采用「基础类 + 扩展实现」的结构，后续在 `parsing/` 中新增 `.bib` 等格式解析器，或在 `summarization/` 中扩展其它模型时，只需继承相应基类并注册即可。

## DeepSeek-chat 摘要

`paper_review/summarization/deepseek.py` 提供了 `DeepSeekSummarizer`，基于用户提供的 `OpenAI`/`deepseek` 客户端调用大模型生成“XXX等人……针对……”风格摘要。实现遵循以下约束：

- 单次模型调用产出结构化 JSON，再经由 `Summary`（Pydantic 或数据类）校验。
- 失败时抛出 `SummaryFailed` 异常，由调用方决定重试策略，不再回退模板语句。

使用方式示例：

```python
from openai import OpenAI
from paper_review.pipeline import ReviewPipeline
from paper_review.classification import LLMCategoryAssigner
from paper_review.summarization.deepseek import DeepSeekSummarizer

client = OpenAI(api_key="<your-key>")
pipeline = ReviewPipeline(
    summarizer=DeepSeekSummarizer(client, model="deepseek-chat"),
    category_assigner=LLMCategoryAssigner(client, model="deepseek-chat"),
)
pipeline.run(source=Path("papers.ris"), out_dir=Path("runs/review"))
```

> **依赖**：若需要 LLM 摘要/分类，请确保安装 `openai>=1.0`（或 DeepSeek 官方 SDK）以及 `pydantic`。

## DeepSeek-chat 分类

`paper_review/classification.py` 提供 `LLMCategoryAssigner`，利用与摘要相同的客户端按照 schema 给出主/子类预测。使用示例：

```python
from openai import OpenAI
from paper_review.classification import LLMCategoryAssigner

client = OpenAI(api_key="<your-key>")
category_assigner = LLMCategoryAssigner(client, model="deepseek-chat")
```

分类失败会抛出 `ClassificationFailed`，调用方可捕获后自行决定重试或人工介入。

## 扩展指南

1. **新增解析器（如 `.bib`）**
   - 在 `paper_review/parsing/` 目录下创建新模块，继承 `BibliographyParser`。
   - 在模块底部通过 `registry.register("bib", CustomParser(), primary=True)` 注册格式名，并按需额外注册文件后缀（如 `registry.register(".bib", CustomParser())`）。

2. **自定义分类器**
   - 继承 `CategoryAssigner`，实现自定义的 `assign` 方法，并通过 `ReviewPipeline(category_assigner=...)` 注入。

3. **接入其它摘要模型**
   - 继承 `Summarizer`，实现 `summarize` 方法，并注入到 `ReviewPipeline`。

## 开发说明

- Python 版本建议 >= 3.9。
- RIS 解析均为纯标准库实现，便于快速启动。
- 可在 `tests/` 或 `examples/` 目录（待创建）中补充样例，便于回归验证。

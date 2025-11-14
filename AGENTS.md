# Agent Guidelines

- 在 `paper_review/` 目录下的所有 Python 代码应遵循以下约定：
  - 使用类型注解，并保持模块化、解耦结构。
  - 遵循现有的“基础类 + 扩展实现”模式，新增功能时优先继承基类。
  - 可选依赖（如 `pydantic`、`pyyaml`）需要通过 `try/except ImportError` 做优雅降级。
- 入口脚本 `main.py` 只负责解析命令行并调用封装好的 pipeline，不应包含业务逻辑。
- 更新文档时，请同步 README，保持与代码结构一致。

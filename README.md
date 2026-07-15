# Todo API — GitHub Actions CI/CD 课程项目

一个可以真实运行的 FastAPI Todo API，作为学习 GitHub Actions CI/CD 流水线的载体。

## 这是什么

这是一门 GitHub Actions CI/CD 课程的配套项目：从一个已经能运行、但完全依赖手工检查、测试、构建和发布的 Todo API 出发，为它建立自动化验证流水线。

课程同时复习 Spec-Driven Development（SDD）：先写清楚需求和验收场景，再在 Spec 的约束下用 AI 辅助完成测试和实现。

## 已有接口

```http
GET  /health
GET  /todos
POST /todos
```

## 这门课要交付什么

围绕同一个仓库和同一个新需求，完成一条完整链路：

```text
理解需求
→ 编写 Spec
→ AI 辅助编写测试和实现
→ 本地验证
→ 创建 Pull Request
→ GitHub Actions 自动验证（Ruff、Pytest、构建、Smoke Test）
→ 通过 Git Tag 自动创建 GitHub Release
```

课程结束时，你的仓库会包含：完整的功能 Spec、与 Spec 对应的测试、功能实现、一个已合并的 Pull Request、一份 `.github/workflows/pipeline.yml`、一个通过 Smoke Test 的 Wheel，以及一个带 Assets 的 GitHub Release。完整的任务清单和验收标准见 [`docs/homework.md`](./docs/homework.md)。

## 如果你是学员

请先完成 [**课前准备**](./docs/prerequisite.md)：确认 Git / GitHub CLI / `uv` 已就绪，并从本仓库的 GitHub Template 创建你自己的独立仓库。

课堂上，AI 辅助开发需要遵守 [`AGENTS.md`](./AGENTS.md) 里的规则——核心是先读 Spec、遇到歧义先提问、不为了实现而修改 Spec。

## 项目命令

```bash
uv sync --locked
uv run ruff check .
uv run pytest
uv run pytest --cov=todo_api
uv run todo-api
uv build
```

应用启动后可以访问：

```text
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/health
```

# Spec: Filter Todos by Completion Status

## Objective

`GET /todos` 目前总是返回全部 Todo，没有任何筛选能力。本功能为 `GET /todos` 增加一个可选的
`completed` 查询参数，让调用方可以按完成状态筛选返回结果：`completed=true` 只看已完成，
`completed=false` 只看未完成，不传该参数则保持现状（返回全部）。

- 用户：调用 Todo API 的客户端，本课程场景下主要是 `tests/test_todos.py` 里的自动化测试，
  以及学员通过 `/docs` 或 `curl` 手动探索接口。
- 成功的样子：不改变任何现有行为和现有测试的前提下，新增的 `completed` 参数能精确、可预期地
  筛选结果；无效取值有清晰的错误响应，而不是被静默忽略。

## Tech Stack

沿用现有项目技术栈，见 `pyproject.toml`（FastAPI、Pydantic v2、uvicorn，Python >= 3.12）。
本功能不引入任何新依赖。

## Commands

沿用 `README.md`「项目命令」一节和 `AGENTS.md`「Project commands」一节：

```bash
uv sync --locked
uv run ruff check .
uv run pytest
uv run pytest --cov=todo_api
uv run todo-api
uv build
```

## Project Structure

沿用现有目录结构（见 `AGENTS.md` 与仓库现状）。本功能预计只涉及：

- `src/todo_api/routers/todos.py` — 新增 `completed` 查询参数与筛选逻辑。
- `tests/test_todos.py` — 新增覆盖本 Spec 各验收场景的测试。

不新增文件，不改动 `src/todo_api/models.py`（Todo 数据结构）或
`src/todo_api/repository.py`（存储方式）。

## Code Style

沿用仓库现有风格（见 `src/todo_api/routers/todos.py`）：路径操作函数使用 Google 风格
docstring 说明 Args/Returns，查询参数用标准类型标注交给 FastAPI/Pydantic 做校验，而不是手写
字符串解析。新增参数的签名大致形如：

```python
from typing import Annotated

from fastapi import Query


@router.get("")
def list_todos(
    repository: TodoRepositoryDep,
    completed: Annotated[bool | None, Query()] = None,
) -> list[Todo]:
    """List stored Todos, optionally filtered by completion status."""
    todos = repository.list_all()
    if completed is None:
        return todos
    return [todo for todo in todos if todo.completed == completed]
```

（以上仅为风格示意，具体实现以 Plan/Tasks 阶段为准。）

## Testing Strategy

沿用 `AGENTS.md` 与 `pyproject.toml` 中 `[tool.pytest.ini_options]` / `[tool.coverage.*]` 的配置：
使用 pytest + FastAPI `TestClient`，测试文件为 `tests/test_todos.py`，覆盖率门槛为 90%
（`fail_under = 90`）。本 Spec 中「Success Criteria / 验收场景」里的每一条都必须在
`tests/test_todos.py` 中有对应的测试用例，且要能一一说出哪个测试覆盖哪条场景。

## Boundaries

- **Always：**
  - 不传 `completed` 参数时，行为必须与当前实现完全一致：返回全部 Todo，顺序不变。
  - 筛选结果必须保持原有插入顺序（在全量列表上做子集筛选，不重新排序、不按 id 或其它字段
    重新排序）。
  - `completed` 只接受布尔真值/假值（`true`/`false`，以及 FastAPI/Pydantic 对 `bool` 类型查询
    参数标准支持的等价写法，如 `1`/`0`），其余任何取值一律返回 `422`，不得静默忽略、不得当作
    未筛选处理、也不得当作某个默认布尔值处理。
  - 为「Success Criteria」中的每条验收场景在 `tests/test_todos.py` 补充对应测试。
- **Ask first：**
  - 修改 Todo 数据模型（`models.py` 中的 `Todo` / `TodoCreate`）。
  - 修改仓储层的存储方式，或引入任何形式的持久化存储。
  - 修改 `GET /todos` 的响应结构（例如包一层 `{"items": [...], "total": ...}`）。
- **Never：**
  - 实现分页（page/limit/cursor 等）。
  - 实现认证/鉴权。
  - 实现数据库持久化。
  - 新增或修改前端（本项目当前没有前端）。
  - 为了让实现"看起来完成"而修改本 Spec，或删除/放宽任何现有测试——包括
    `tests/test_todos.py` 中已有的 `test_list_todos_preserves_order_and_mixed_states`。

## Success Criteria

以下每条都可以直接通过 `uv run pytest tests/test_todos.py -v` 验证（场景 1-3、5-6 可复用
现有的 `client` fixture，其 `repository` fixture 内容为 `id=1 "Already done" completed=True`、
`id=2 "Still pending" completed=False`；场景 4 需要一个专门构造的、完成状态单一的仓库）：

1. **不传 `completed`** — `GET /todos` → `200`，返回全部 Todo，顺序不变（即现有测试
   `test_list_todos_preserves_order_and_mixed_states` 继续通过，不需要修改）。

2. **`completed=true`** — `GET /todos?completed=true` → `200`，仅返回
   `[{"id": 1, "title": "Already done", "completed": true}]`。

3. **`completed=false`** — `GET /todos?completed=false` → `200`，仅返回
   `[{"id": 2, "title": "Still pending", "completed": false}]`。

4. **没有匹配结果** — 用一个仓库/客户端构造为「全部 Todo 的 `completed` 都相同」（例如全部
   `completed=True`），请求相反的取值（`GET /todos?completed=false`）→ `200`，返回空数组 `[]`
   （不是 `404`，也不是 `null`）。

5. **无效布尔值** — `GET /todos?completed=maybe`（或 `completed=2`、`completed=`）→ `422`，
   返回 FastAPI/Pydantic 标准的校验错误响应体，不返回 `200`，也不当作未筛选处理。

6. **筛选不改变原有顺序** — 用一个至少 4 条、完成状态交替出现的仓库（例如
   `True, False, True, False`）验证：`completed=true` 返回的两条记录，相对顺序与它们在全量
   列表中的原始顺序一致（不按其它规则重排）。

7. **不破坏现有质量门槛** — `uv run pytest` 与 `uv run ruff check .` 全部通过；覆盖率不低于
   `pyproject.toml` 中配置的 90%。

## Open Questions

本次需求在课程范围内是确定的，以下问题不阻塞本 Spec 的推进，仅供后续迭代参考：

- 是否需要支持按 `completed` 以外的维度筛选（如按标题关键字搜索）？本次不做。
- 无效布尔值时的 `422` 错误信息是否需要自定义格式？本次沿用 FastAPI/Pydantic 默认行为，不
  额外定制。

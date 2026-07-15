# GitHub Actions CI/CD 课程设计

## 一、课程概况

- 课程名称：使用 GitHub Actions 构建 Python 项目的 CI/CD 流水线
- 课程时长：3 小时（含 10 分钟休息）
- 学员人数：8 人
- 学员基础：具备 Python 或 C++ 编程经验，已经学习 Git 与 GitHub 的基本使用
- 开发方式：Zoom 会议，教师共享屏幕带领全员锁步操作；每位学员在自己的仓库中独立跟做
- 核心项目：FastAPI Todo API
- Python 项目管理：`uv`
- 自动化平台：GitHub Actions
- 最终交付物：经过自动验证的 Python Wheel、Workflow Artifact 和 GitHub Release

## 二、课程目标

课程结束后，学员能够：

1. 解释 CI、持续交付和持续部署之间的区别。
2. 解释 GitHub Actions 中 Event、Workflow、Job、Step、Runner 和 Action 的关系。
3. 根据业务需求编写包含验收场景的功能 Spec。
4. 使用 AI Agent 在 Spec 约束下辅助编写测试和实现代码。
5. 使用 `uv` 管理 Python 版本、依赖、虚拟环境和项目命令。
6. 创建由 Pull Request 和 Push 事件触发的 GitHub Actions Workflow。
7. 在流水线中自动执行 Ruff、Pytest、构建和 Smoke Test。
8. 使用 Job 依赖关系组织并行和串行执行步骤。
9. 构建 Python Wheel，并通过 Workflow Artifact 在 Job 之间传递和保存制品。
10. 通过 Git Tag 自动创建 GitHub Release，并发布经过验证的制品。
11. 阅读 GitHub Actions 日志，定位并修复失败的自动化任务。

## 三、教学主线

整堂课围绕同一个仓库和同一个功能需求展开：

```text
理解需求
→ 编写 Spec
→ AI 辅助编写测试和实现
→ 本地验证
→ 创建 Pull Request
→ GitHub Actions 自动验证
→ 构建 Python Wheel
→ 在干净环境中安装并运行 Wheel
→ 上传 Workflow Artifact
→ 创建版本 Tag
→ 自动创建 GitHub Release
```

课程强调以下验证链路：

```text
Spec 约束需求
测试约束实现
CI 验证可重复性
Smoke Test 验证制品可运行
Release 完成持续交付
```

## 四、项目设计

### 4.1 项目背景

学员接手一个已经能够运行的 Todo API。项目目前依赖开发者手工执行代码检查、测试、构建和发布，尚未建立自动化流水线。

学员的任务是：

1. 为一个新需求编写 Spec。
2. 在 Spec 约束下使用 AI 辅助完成实现。
3. 为项目建立自动化验证流水线。
4. 构建并验证可交付制品。
5. 创建正式版本并发布制品。

### 4.2 已有接口

```http
GET  /health
GET  /todos
POST /todos
```

### 4.3 本次新增需求

为 `GET /todos` 增加 `completed` 查询参数：

```http
GET /todos?completed=true
GET /todos?completed=false
```

明确行为：

1. 不传 `completed` 时返回全部 Todo。
2. `completed=true` 时只返回已完成的 Todo。
3. `completed=false` 时只返回未完成的 Todo。
4. 返回结果保持原有顺序。
5. 没有匹配项时返回空数组。
6. 无效布尔值返回 HTTP 422。

不在本次需求范围内的内容：

- 分页
- 用户认证
- 数据库
- 持久化
- Todo 数据结构调整
- 前端页面

## 五、Spec-Driven Development 环节

学员使用仓库自带的 `spec-driven-development` skill（`.agents/skills/spec-driven-development/`）完成 Specify 阶段，产出 `specs/001-filter-todos/spec.md`。这是在已有项目里新增一个小功能，不是新建项目：skill 模板里 Tech Stack、Commands、Project Structure、Testing Strategy 这些项目级字段直接引用仓库已有的 `pyproject.toml`、README.md 和 AGENTS.md，不需要重新定义；重点放在 Objective、Boundaries 和 Success Criteria。

不论落在 skill 模板的哪个字段下，Spec 内容必须说清楚：正常行为、参数缺省行为、`true`/`false` 两种分支、无匹配结果、无效输入、返回顺序、不在需求范围内的内容、可验证的验收场景。

实现代码之前，学员单独提交 Spec（例如 `spec: define completed todo filtering`）。教师完成第一次检查后，学员再进入测试和实现阶段。

## 六、GitHub Actions 流水线设计

### 6.1 触发条件

流水线由以下事件触发：

- Pull Request 创建或更新
- Push 到 `main`
- Push `v*` 格式的 Git Tag
- 手动触发

### 6.2 Job 结构

```text
lint ─────┐
          ├→ build → smoke-test → release（仅版本 Tag）
test ─────┘
```

### 6.3 `lint` Job

执行：

```bash
uv sync --locked
uv run ruff check .
```

目标：

- 验证依赖锁文件有效
- 检查 Python 代码规范
- 尽早发现低成本错误

### 6.4 `test` Job

执行：

```bash
uv sync --locked
uv run pytest --cov=todo_api
```

目标：

- 验证已有功能
- 验证新增筛选功能
- 生成覆盖率信息

### 6.5 `build` Job

依赖：

```text
lint
test
```

执行：

```bash
uv build
```

生成：

```text
dist/todo_api-0.1.0-py3-none-any.whl
dist/todo_api-0.1.0.tar.gz
```

构建完成后上传名为 `todo-api-package` 的 Workflow Artifact。

### 6.6 `smoke-test` Job

依赖：

```text
build
```

步骤：

1. 下载 `todo-api-package` Artifact。
2. 创建一个新的临时 Python 环境。
3. 只安装刚刚构建的 Wheel。
4. 使用安装后生成的 `todo-api` 命令启动服务。
5. 请求 `GET /health`。
6. HTTP 请求失败时让 Job 失败。

目标：

- 验证构建制品可以被安装
- 验证安装后的命令可以启动
- 验证正在测试的是构建制品，而不是项目源码目录

### 6.7 `release` Job

运行条件：

```text
Git Ref 为 v* 格式的 Tag
smoke-test 成功
```

步骤：

1. 下载经过验证的 `todo-api-package` Artifact。
2. 使用 Tag 名称创建 GitHub Release。
3. 将 Wheel 和源码包添加到 Release Assets。
4. 在 Release 中记录版本和对应 Commit。

权限：

- Workflow 默认使用只读权限。
- 只有 `release` Job 申请创建 Release 所需的 `contents: write` 权限。

## 七、三小时课程安排

### 0:00–0:15：项目基线

操作：

```bash
uv sync --locked
uv run ruff check .
uv run pytest
uv run todo-api
```

检查：

- 打开 `/docs`
- 调用 `/health`
- 调用已有 Todo 接口
- 阅读项目结构和已有测试

产出：

- 每位学员确认本地项目能够运行

### 0:15–0:35：编写功能 Spec

操作：

- 分析 `completed` 筛选需求
- 使用 AI 辅助起草 Spec
- 明确边界条件和 Out of scope
- 编写验收场景
- 提交 Spec

产出：

```text
specs/001-filter-todos/spec.md
```

### 0:35–1:05：AI 辅助测试与实现

操作：

1. 根据 Spec 补充测试。
2. 先运行测试并观察失败。
3. 使用 AI 辅助完成最小实现。
4. 运行 Ruff 和 Pytest。
5. 创建实现提交。

产出：

- 新测试经历红灯到绿灯
- 本地检查全部通过
- 功能实现与 Spec 对应

### 1:05–1:15：休息

### 1:15–1:30：CI/CD 与 GitHub Actions 核心模型

内容：

- 手工测试、构建和发布的问题
- CI、持续交付和持续部署
- GitHub Actions 的平台定位
- Event、Workflow、Job、Step、Runner 和 Action
- 接下来要建的完整流水线

产出：

- 学员能够口头解释接下来要经历的自动化流程

### 1:30–2:05：建立基础 CI

操作：

- 创建 `pipeline.yml`
- 配置 Pull Request 和 Push 触发条件
- 建立 `lint` Job
- 建立 `test` Job
- Push 功能分支
- 创建 Pull Request
- 阅读 Actions 运行页面
- 故意制造一次失败
- 通过日志定位并修复

产出：

- Pull Request 中出现自动检查
- 学员完成一次失败排查

### 2:05–2:30：构建和验证制品

操作：

- 增加 `build` Job
- 使用 `needs` 依赖 `lint` 和 `test`
- 执行 `uv build`
- 上传 Workflow Artifact
- 增加 `smoke-test` Job
- 下载并安装 Wheel
- 启动安装后的应用
- 请求 `/health`

产出：

- `todo-api-package` Artifact
- 通过 Smoke Test 的 Wheel

### 2:30–2:50：持续交付与 Release

操作：

- 合并 Pull Request
- 更新项目版本为 `0.1.0`
- 创建 `v0.1.0` Tag
- Push Tag
- 自动创建 GitHub Release
- 检查 Release Assets

产出：

```text
Release v0.1.0
├── todo_api-0.1.0-py3-none-any.whl
└── todo_api-0.1.0.tar.gz
```

### 2:50–3:00：复盘与验收

学员需要能够解释：

1. Spec、测试和实现之间的关系。
2. 为什么本地通过后还需要 CI。
3. `lint` 和 `test` 为什么可以并行。
4. `build` 为什么依赖前两个 Job。
5. 为什么需要验证 Wheel，而不只验证源码。
6. Artifact 与 Release 的区别。
7. Pull Request、`main` 和版本 Tag 分别触发什么行为。
8. 本课程完成的是哪部分 CI/CD 流程。

任务清单和验收标准见 `docs/homework.md`；教师课前准备见 `docs/teacher-prep.md`。

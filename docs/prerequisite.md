# Prerequisites 课前准备

这门课会以一个 Python 项目为主线，先复习如何从需求和 Spec 出发，通过测试约束实现，完成一轮 Spec-Driven Development（SDD）；随后把本地的代码检查、测试、构建和制品验证搬到 GitHub Actions 中，建立持续集成（CI）流水线，并通过自动创建 GitHub Release 完成持续交付（CD）。为了把课堂时间留给这些核心实践，请在上课前完成下面的环境准备。

## 课前准备清单

- [ ] Git 和 GitHub CLI（`gh`）可以正常使用。
- [ ] `gh` 已经登录自己的 GitHub 账号。
- [ ] Git 已配置姓名和邮箱。
- [ ] 本机已安装 `uv`。
- [ ] `uv` 可以使用 Python 3.12。
- [ ] 已准备好课程 Starter Repository。
- [ ] Starter Repository 的课前自检全部通过。

## 检查 GitHub 环境

请在终端运行：

```bash
git --version
gh --version
gh auth status
git config --global user.name
git config --global user.email
```

请确认：

- `git --version` 和 `gh --version` 能正常输出版本信息。
- `gh auth status` 显示已经登录自己的 GitHub 账号。
- `user.name` 和 `user.email` 都不是空的。

如果 `gh` 尚未登录，请运行：

```bash
gh auth login
gh auth setup-git
```

## 安装 `uv` 和 Python 3.12

`uv` 是本课程使用的 Python 项目管理工具。课堂上会使用它管理 Python 版本、项目依赖、虚拟环境和项目命令。

请参考 `uv` 官方安装文档完成安装：

- https://docs.astral.sh/uv/getting-started/installation/

安装后请重新打开终端，并运行：

```bash
uv --version
uv python install 3.12
uv run --python 3.12 python --version
```

最后一条命令应当输出 Python 3.12 的版本信息。本课程不要求单独安装 Python、Ruff、Pytest、FastAPI 或其他 Python 依赖。

## 准备 Starter Repository

课程仓库 `SingularityCoding/2026-summer-github-actions` 是一个 GitHub Template Repository。每位学员使用 GitHub Template 功能，从这个模板创建一个属于自己的独立仓库，并克隆到本地：

```bash
gh repo create <your-repository-name> --template SingularityCoding/2026-summer-github-actions --private --clone
cd <your-repository-name>
```

进入仓库后，请确认远程仓库指向自己的 GitHub 账号：

```bash
git remote -v
gh repo view
```

## 运行课前自检

在 Starter Repository 根目录运行：

```bash
uv sync --locked
uv run ruff check .
uv run pytest
uv run todo-api
```

请确认以上命令全部成功，并能够访问 `http://127.0.0.1:8000/health`。你暂时不需要理解每一条命令的具体作用，课堂上会结合项目逐一解释。

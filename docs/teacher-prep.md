# 教师课前准备

## 模板仓库

本仓库（`SingularityCoding/2026-summer-github-actions`）本身即模板：在 GitHub 仓库设置中开启 Template Repository 开关后，学员通过 `gh repo create --template ...` 或网页上的 "Use this template" 创建自己的独立仓库（见 `docs/prerequisite.md`）。模板仓库包含：

- 可运行的 FastAPI Todo API
- 已有接口和测试
- `pyproject.toml`
- `uv.lock`
- `.python-version`
- Spec 目录和模板
- 空的或待补充的 `pipeline.yml`
- Pull Request 模板
- README 课堂指引
- `docs/homework.md` 中的可选拓展任务（非本次课程考核内容）

## 预埋教学故障

准备可以快速触发的故障：

- 一个确定会导致筛选测试失败的实现错误
- 一个 Ruff 能发现的格式或未使用导入问题
- 一个 Wheel 构建后入口命令配置错误的示例
- 一个 Smoke Test 无法连接时的日志示例

## 参考材料

完整参考实现（Spec、测试、功能实现、Workflow）不写入本仓库，避免学员通过模板仓库直接看到答案。在独立的私有仓库（例如 `2026-summer-github-actions-reference`，参考 `vibe-checkin` / `vibe-checkin-reference` 的既有做法）中准备：

- 完整 Spec 参考答案
- 完整测试参考答案
- 功能实现参考答案
- 完整 Workflow 参考答案
- 失败日志截图或备份日志
- 课程结束后的完整示例仓库

## 课前演练

教师使用一个全新 GitHub 账号完整执行：

1. 从模板创建仓库。
2. 克隆仓库。
3. 使用 `uv` 初始化项目。
4. 创建 Spec 和功能分支。
5. 创建 Pull Request。
6. 触发 CI。
7. 构建和下载 Artifact。
8. 执行 Smoke Test。
9. 创建版本 Tag。
10. 检查 GitHub Release 和 Assets。

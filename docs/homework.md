# 课程任务清单

## 主线任务

- [ ] 编写 Spec，并使用 AI 辅助完成测试与实现
- [ ] 至少一个功能分支
- [ ] Ruff 检查通过、Pytest 测试通过
- [ ] 一个已合并的 Pull Request，且自动触发了 CI
- [ ] 一次可说明原因的失败运行记录
- [ ] 一份 `pipeline.yml`，包含 `lint`、`test`、`build`、`smoke-test` Job
- [ ] 一个可下载的 Workflow Artifact
- [ ] 一个通过 Smoke Test 的 Wheel
- [ ] `v0.1.0` Git Tag
- [ ] 一个带 Assets 的 GitHub Release

## 可选拓展（不计入本次课程验收标准）

### CI 机制

- [ ] 使用 Python 版本 Matrix 运行测试
- [ ] 开启 `uv` Cache
- [ ] 将覆盖率报告上传为 Artifact
- [ ] 添加手动触发参数
- [ ] 为 Job 配置超时时间
- [ ] 为并发运行配置取消策略
- [ ] 在 README 中添加 Workflow 状态徽章

### Release 机制

- [ ] 校验 `pyproject.toml` 版本与 Git Tag 一致
- [ ] 自动生成 Release Notes
- [ ] 增加预发布版本流程
- [ ] 为 Release Job 配置 GitHub Environment
- [ ] 增加人工审批后再创建正式 Release
- [ ] 将通用 Python CI 抽取为可复用 Workflow
- [ ] 将第三方 Action 固定到完整 Commit SHA

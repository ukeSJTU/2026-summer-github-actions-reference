# AGENTS.md

This repository is the student project for a GitHub Actions CI/CD course built around a small FastAPI Todo API. The course pairs Spec-Driven Development (writing a spec before code) with an automated pipeline (lint, test, build, smoke-test, release) implemented in `.github/workflows/`.

If you are an AI agent helping a student in this repo, follow the rules below. They exist to keep AI-assisted work inside the boundaries of the course's spec, not to slow you down.

## Writing a spec

Use the installed `spec-driven-development` skill (`.agents/skills/spec-driven-development/`) to write specs under `specs/`. This project already exists, so the skill template's project-level fields (Tech Stack, Commands, Project Structure, Testing Strategy) should reference the existing `pyproject.toml`, `README.md`, and this file rather than being redefined per feature. Put the feature-specific content in Objective, Boundaries, and Success Criteria.

## Rules

1. Read the relevant spec under `specs/` and the existing project code before making changes.
2. If the spec is ambiguous, ask a clarifying question first — do not guess and implement.
3. Write or extend tests from the spec's acceptance scenarios before implementing the feature.
4. Run the new tests and confirm they fail for the right reason (missing behavior) before implementing.
5. Implement the minimal change that satisfies the spec.
6. Never edit the spec to make an already-written implementation pass.
7. Never delete, skip, or weaken an existing test to make it pass.
8. Keep changes scoped to the current spec's requirements — do not expand scope.
9. Before finishing, run `uv run pytest` and `uv run ruff check .` and confirm both pass.
10. Be able to state which test covers which requirement — the student using this repo needs to explain this to the instructor.

## Project commands

```bash
uv sync --locked
uv run ruff check .
uv run pytest
uv run pytest --cov=todo_api
uv run todo-api
uv build
```

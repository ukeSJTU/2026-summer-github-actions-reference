"""Tests for the command-line entry point."""

from typing import Any

import pytest

from todo_api import cli


def test_cli_starts_uvicorn(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, Any] = {}

    def fake_run(app: str, **kwargs: Any) -> None:
        captured["app"] = app
        captured.update(kwargs)

    monkeypatch.setattr(cli.uvicorn, "run", fake_run)

    cli.main()

    assert captured == {
        "app": "todo_api.main:app",
        "host": "127.0.0.1",
        "port": 8000,
    }

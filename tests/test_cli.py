"""Smoke test: the CLI starts and prints help."""

from typer.testing import CliRunner

from surgeon.cli import app


def test_help_prints_usage():
    result = CliRunner().invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage" in result.output

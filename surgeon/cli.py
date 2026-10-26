"""Command-line entry point. Commands are added here, one per checkpoint."""

import typer

app = typer.Typer(
    help="Turn a messy git working tree into small logical commits and a PR description, offline.",
    no_args_is_help=True,
)


@app.callback()
def main() -> None:
    """Commit Surgeon: code groups your changes, a local model writes the words."""

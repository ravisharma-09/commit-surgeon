# Commit Surgeon
Offline CLI: turns a messy git working tree into small logical commits + a PR description, asking for approval at every step.

## Hard constraints
- Fully offline: only local git and Ollama at http://localhost:11434.
- Open model of 4B parameters or less. Code decides the grouping; the model only writes the words.
- Nothing is committed without approval. Make a backup ref first. Support undo.
- Model output: JSON schema via Ollama `format`, then check Conventional Commits, retry once, then fall back to a template message.

## Stack and commands
Python 3.11+, Typer, Rich, unidiff, pytest. Tests: `pytest -q`. Run: `python -m surgeon`.

## Workflow
- Write a failing test first, and run it before saying a task is done.
- Tests use a generated messy-repo fixture (3 unrelated concerns), never a real repo.
- Small commits, Conventional Commits messages. A short docstring on every file explaining what it does.

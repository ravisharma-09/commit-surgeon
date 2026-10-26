# Commit Surgeon

An offline command-line tool that turns a messy git working tree into small, logical commits and a ready PR description, and asks for approval at every step. Code decides the grouping; a local open model of 4B parameters or less only writes the words.

Built by team **kyu batau??** (Ravi Sharma, Kavin Rau) for the Devf8rge × Hacktoberfest Hack Day, problem statement PS-03.

> Work in progress. Setup, usage and contribution notes will be filled in at checkpoint 9 (see [docs/BUILD_CHECKPOINTS.md](docs/BUILD_CHECKPOINTS.md)).

## What existed before the event

Only planning material: this README, `CLAUDE.md`, the `LICENSE` and `docs/BUILD_CHECKPOINTS.md`. No application code was written before the finals.

## AI tools used

- Claude Code (coding assistant), used checkpoint by checkpoint as described in `docs/BUILD_CHECKPOINTS.md`.
- A local open model through Ollama (to be named once benchmarked) for commit and PR text.

## License

Apache-2.0. See [LICENSE](LICENSE).

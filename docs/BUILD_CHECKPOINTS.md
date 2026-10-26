# Commit Surgeon: build checkpoints and prompts

Ten checkpoints (0 to 9), one Claude Code session each. Verify every checkpoint yourself; the test you run is the gate to the next one.

> **Note:** the exported PDF cut every prompt off at the right edge. Each prompt below is copied up to where the PDF stops, marked `[…]`. Paste the full prompt from the original "Build checkpoints" doc before using it.

## How to use each checkpoint

1. Start a fresh session with `/clear`, then press Shift+Tab until the status bar shows plan mode.
2. Paste the checkpoint's prompt. Read the plan, edit anything you do not understand, then approve it.
3. Let Claude Code implement it and run the tests.
4. Verify it yourself with the commands under **Verify**, and tick the boxes.
5. Read the diff and commit with a clear message. Only then start the next checkpoint.

If you do not understand a file, or something fails, use these two prompts:

```text
Explain surgeon/<file>.py to me line by line. I know basic Python and OOP but not […]
```

```text
Run the failing test, explain the cause in plain words, propose the smallest fix, […]
```

Both of you must be able to explain every file, so use the first prompt often.

---

## Checkpoint 0: project skeleton and local model

An empty but runnable Python package, plus proof that Ollama answers on your machine.

```text
Read CLAUDE.md. Create the project skeleton only: pyproject.toml (Python 3.11+; Ty[…]
```

Verify:
- [ ] `ollama list` shows your model, and `curl http://localhost:11434/api/tags` returns JSON
- [ ] `pip install -e .` works, then `python -m surgeon --help` prints help
- [ ] `pytest -q` passes
- [ ] `git log --oneline` shows your first commit

## Checkpoint 1: a messy-repo fixture

Throwaway git repos with unrelated edits, so every later step has something to test against.

```text
Read CLAUDE.md. Plan, then implement tests/fixtures/make_messy_repo.py with two fu[…]
1. easy_repo(): three unrelated concerns in three different folders: a docs edit i[…]
2. mixed_repo(): one file that contains two unrelated edits (a bug fix and a comme[…]
Add pytest tests checking that `git status --porcelain` lists exactly the expected[…]
```

Verify:
- [ ] `pytest -q` passes
- [ ] Print the fixture repo's path, `cd` there, run `git status` and `git diff`: three unrelated edits
- [ ] You can say in one sentence what each edit is

## Checkpoint 2: read the changes

Turn the working tree into files and hunks. Added, deleted, renamed and binary files stay whole.

```text
Read CLAUDE.md. Plan, then implement surgeon/changes.py: read_changes(repo_path) […]
```

Verify:
- [ ] `pytest -q` passes
- [ ] `python -m surgeon inspect <fixture repo>` lists exactly the files that `git status` shows
- [ ] Hunk counts match what you see in `git diff`
- [ ] A new untracked file you add by hand shows up too

## Checkpoint 3: group the changes, with reasons

The heart of the tool: code, not the model, decides which changes belong together and records why. Three simple rules, each its own small function.

```text
Read CLAUDE.md. Plan, then implement surgeon/grouping.py: group_changes(changes) […]
```

Verify:
- [ ] `pytest -q` passes
- [ ] `plan` on the easy fixture prints 3 groups, each with a sensible reason
- [ ] Edit a second file inside `app/` by hand: it joins the `app/` group
- [ ] You can explain each rule in your own words

## Checkpoint 4: the approval screen

Every step shown for approval before anything is committed. Template messages like "docs: update documentation" until checkpoint 6.

```text
Read CLAUDE.md. Plan, then implement an interactive approval step in surgeon/appro[…]
```

Verify:
- [ ] Run `run` on the fixture and try accept, merge two groups, and skip
- [ ] `git status` and `git log` are identical before and after
- [ ] `plan.json` exists and matches what you approved
- [ ] Press Ctrl+C halfway: the repo is untouched

## Checkpoint 5: commit and undo, with a backup

Save a backup point first, then one commit per approved group. Undo moves the branch back to the backup and leaves the changes uncommitted.

```text
Read CLAUDE.md. Plan carefully, then implement surgeon/apply.py: apply(plan) first[…]
```

Verify:
- [ ] Before: note the output of `git status --porcelain` and `git log --oneline`
- [ ] After `run` and approving everything: 3 new commits, each holding only its own files (`git show --stat HEAD`, `HEAD~1`, `HEAD~2`)
- [ ] `git for-each-ref` lists the backup ref
- [ ] After `undo`, `git status --porcelain` and `git log --oneline` match your "before" notes
- [ ] Skip one group during approval: it stays uncommitted

## Checkpoint 6: the model writes the messages

A one-line Conventional Commits message per group, forced into a JSON schema, checked, with a template fallback.

```text
Read CLAUDE.md. Plan, then implement surgeon/llm.py: generate_message(group, style[…]
```

Verify:
- [ ] `pytest -q` passes (the tests must not need Ollama)
- [ ] With Ollama running, `run` on the fixture shows model-written messages
- [ ] Stop Ollama: `run` still works and shows template messages, with no crash
- [ ] Run it 10 times: every message is valid; write down the seconds per run
- [ ] Turn Wi-Fi off: it still works

## Checkpoint 7: the PR description

What changed, why, and how to test, built from the approved groups. The test command comes from the repo itself, not the model.

```text
Read CLAUDE.md. Plan, then implement surgeon/prtext.py: build_pr_description(plan,[…]
```

Verify:
- [ ] The description lists exactly your 3 commits
- [ ] "How to test" shows the right command for the fixture
- [ ] "Why" matches what the changes really do; read it critically
- [ ] It still prints something sensible with Ollama stopped and Wi-Fi off

## Checkpoint 8: doctor and benchmark

`doctor` checks the setup and prints the fix for whatever is wrong. `bench` produces the numbers for judges and users.

```text
Read CLAUDE.md. Plan, then implement `python -m surgeon doctor` (checks: Ollama re[…]
```

Verify:
- [ ] `doctor` passes with Ollama running, and prints a useful fix when you stop Ollama or remove the model
- [ ] `bench` prints all four numbers; open `bench/results.md` and read it
- [ ] Re-run `bench` with a second model and compare the results
- [ ] A full run takes under 60 s on your laptop, the brief's limit

## Checkpoint 9: README and a clean-clone test

Open-source quality is 15% of the finals score. Test the README the way a stranger would.

```text
Read CLAUDE.md. Write README.md: what the tool does (3 sentences), requirements, n[…]
```

Verify:
- [ ] Clone the repo into a new folder and follow the README exactly: every step works
- [ ] Every claim in the README is true today
- [ ] The LICENSE file is present, and the README names the AI tools used

---

## When the sandbox arrives

Run `inspect`, `plan` and `run` on the `messy-changes` branch in the Devf8rge sandbox. If a group is wrong, do not hack around it. Add one grouping rule and one test that reproduces the mistake, then re-run.

## Stretch checkpoints

Only start these after checkpoints 0 to 9 all pass.

**S1. Git hook.** The brief names a hook, and it is cheap.

```text
Read CLAUDE.md. Plan, then implement `python -m surgeon install-hook`, which insta[…]
```

- [ ] Install it in the mixed fixture: a big mixed commit prints the warning, a small commit stays silent
- [ ] The commit succeeds in both cases

**S2. Hunk-level splitting.** Needed if the sandbox mixes concerns inside one file.

```text
Read CLAUDE.md. Plan, then implement splitting one file's hunks into different gro[…]
```

- [ ] `mixed_repo()` becomes 2 commits, and `git show` for each contains only its own hunk
- [ ] `undo` still restores the original state

**S3. X-ray viewer.** The visual for the demo.

```text
Read CLAUDE.md. Plan, then implement `python -m surgeon view <repo>`, which writes[…]
```

- [ ] Open it with Wi-Fi off: the graph draws
- [ ] Clusters match the plan, and the reasons show on hover

Rule of thumb: do not start the next checkpoint until every box is ticked.

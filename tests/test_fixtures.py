"""Checks that the messy-repo fixtures leave exactly the expected uncommitted changes."""

import subprocess

from tests.fixtures.make_messy_repo import easy_repo, mixed_repo


def git(repo, *args):
    return subprocess.run(
        ["git", *args], cwd=repo, capture_output=True, text=True, check=True
    ).stdout


def porcelain(repo):
    return sorted(git(repo, "status", "--porcelain").splitlines())


def test_easy_repo_has_three_concerns_in_three_folders(tmp_path):
    repo = easy_repo(tmp_path)
    assert porcelain(repo) == [
        " M app/cart.py",
        " M docs/install.md",
        " M utils/report.py",
        " M utils/text.py",
    ]
    assert len(git(repo, "log", "--oneline").splitlines()) == 1


def test_mixed_repo_has_one_file_with_two_hunks(tmp_path):
    repo = mixed_repo(tmp_path)
    assert porcelain(repo) == [" M app/cart.py"]
    hunks = [line for line in git(repo, "diff").splitlines() if line.startswith("@@")]
    assert len(hunks) == 2

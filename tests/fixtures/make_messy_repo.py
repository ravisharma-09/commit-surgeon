"""Builds throwaway git repos with uncommitted, unrelated edits for tests to work on.

Run this file directly to build both repos in a temp folder and print their paths.
"""

import subprocess
import tempfile
from pathlib import Path

CART_BEFORE = '''\
"""Shopping cart maths."""

TAX_RATE = 0.18


def subtotal(items):
    return sum(item["price"] for item in items)


def total(items):
    # BUG: tax is added twice
    return subtotal(items) * (1 + TAX_RATE) * (1 + TAX_RATE)


def item_count(items):
    return len(items)


def is_empty(items):
    return item_count(items) == 0


def cheapest(items):
    # TODO TODO: old note, remove me
    # returns the cheapest item (or None) in the cart (the cart)
    return min(items, key=lambda item: item["price"], default=None)
'''

CART_BUG_FIXED = CART_BEFORE.replace(
    "    # BUG: tax is added twice\n"
    "    return subtotal(items) * (1 + TAX_RATE) * (1 + TAX_RATE)\n",
    "    return subtotal(items) * (1 + TAX_RATE)\n",
)

CART_BOTH_EDITS = CART_BUG_FIXED.replace(
    "    # TODO TODO: old note, remove me\n"
    "    # returns the cheapest item (or None) in the cart (the cart)\n",
    "    # Returns the cheapest item, or None for an empty cart.\n",
)

INSTALL_BEFORE = """\
# Install

Run `pip install commit-surgeon`.
"""

INSTALL_AFTER = """\
# Install

You need Python 3.11 or newer.

Run `pip install commit-surgeon`, then `surgeon --help` to check it works.
"""

TEXT_BEFORE = '''\
"""Small text helpers."""


def shout(text):
    return text.upper() + "!"
'''

REPORT_BEFORE = '''\
"""Builds the one-line report."""

from utils.text import shout


def headline(title):
    return shout(title)
'''


def easy_repo(base: Path) -> Path:
    """Three unrelated concerns in three folders: docs edit, app bug fix, utils rename."""
    repo = _init_repo(Path(base) / "easy_repo")
    _write(repo / "app/cart.py", CART_BUG_FIXED)
    _write(repo / "docs/install.md", INSTALL_AFTER)
    _write(repo / "utils/text.py", TEXT_BEFORE.replace("def shout(", "def to_headline("))
    _write(repo / "utils/report.py", REPORT_BEFORE.replace("shout", "to_headline"))
    return repo


def mixed_repo(base: Path) -> Path:
    """One file holding two unrelated edits: a bug fix and a comment cleanup."""
    repo = _init_repo(Path(base) / "mixed_repo")
    _write(repo / "app/cart.py", CART_BOTH_EDITS)
    return repo


def _init_repo(repo: Path) -> Path:
    """Creates the repo with all starting files in one initial commit."""
    repo.mkdir(parents=True)
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.name", "Fixture Bot")
    _git(repo, "config", "user.email", "fixture@example.com")
    _git(repo, "config", "commit.gpgsign", "false")
    _write(repo / "app/cart.py", CART_BEFORE)
    _write(repo / "docs/install.md", INSTALL_BEFORE)
    _write(repo / "utils/text.py", TEXT_BEFORE)
    _write(repo / "utils/report.py", REPORT_BEFORE)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "chore: initial commit")
    return repo


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


if __name__ == "__main__":
    base = Path(tempfile.mkdtemp(prefix="surgeon-fixtures-"))
    print("easy: ", easy_repo(base))
    print("mixed:", mixed_repo(base))

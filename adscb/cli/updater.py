"""Git-backed problem content updater.

On first `adscb update`, we clone the upstream repo into `~/.adscb/repo/`.
On subsequent calls we `git pull --ff-only`. If the fast-forward fails
(force push, local modifications), the user can run `adscb sync` which
wipes the clone and re-clones from scratch.

The problems inside the cloned repo override the ones shipped with the
installed package — see loader.py.
"""
import shutil
import subprocess

from ..config import REPO_DIR, REPO_URL, USER_HOME


def has_git():
    """True if `git` is callable on this machine."""
    try:
        result = subprocess.run(
            ["git", "--version"],
            capture_output=True,
            text=True,
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def is_cloned():
    """True if we have a working clone at REPO_DIR."""
    return (REPO_DIR / ".git").is_dir()


def clone():
    """Clone the upstream repo into REPO_DIR.

    Returns (ok: bool, message: str).
    """
    USER_HOME.mkdir(parents=True, exist_ok=True)
    if REPO_DIR.exists():
        shutil.rmtree(REPO_DIR)
    result = subprocess.run(
        ["git", "clone", REPO_URL, str(REPO_DIR)],
        capture_output=True,
        text=True,
    )
    msg = (result.stdout + result.stderr).strip()
    return result.returncode == 0, msg


def pull():
    """Fast-forward pull the existing clone.

    Returns (ok: bool, message: str). On failure the caller should
    suggest `adscb sync`.
    """
    if not is_cloned():
        return clone()
    result = subprocess.run(
        ["git", "-C", str(REPO_DIR), "pull", "--ff-only"],
        capture_output=True,
        text=True,
    )
    msg = (result.stdout + result.stderr).strip()
    return result.returncode == 0, msg


def current_commit():
    """Short commit hash of the currently-checked-out problem content, or None."""
    if not is_cloned():
        return None
    result = subprocess.run(
        ["git", "-C", str(REPO_DIR), "rev-parse", "--short", "HEAD"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def current_branch():
    """Name of the currently-checked-out branch, or None."""
    if not is_cloned():
        return None
    result = subprocess.run(
        ["git", "-C", str(REPO_DIR), "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def nuke():
    """Remove the local clone entirely."""
    if REPO_DIR.exists():
        shutil.rmtree(REPO_DIR)

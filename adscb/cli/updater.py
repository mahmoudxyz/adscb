"""Git-backed updater that syncs the entire adscb package."""
import shutil
import subprocess
from pathlib import Path

import adscb as adscb_pkg

from ..config import REPO_DIR, REPO_URL, USER_HOME

INSTALLED_PKG_DIR = Path(adscb_pkg.__file__).parent


def has_git():
    try:
        return subprocess.run(["git", "--version"], capture_output=True).returncode == 0
    except FileNotFoundError:
        return False


def is_cloned():
    return (REPO_DIR / ".git").is_dir()


def clone():
    USER_HOME.mkdir(parents=True, exist_ok=True)
    if REPO_DIR.exists():
        shutil.rmtree(REPO_DIR)
    r = subprocess.run(["git", "clone", REPO_URL, str(REPO_DIR)],
                       capture_output=True, text=True)
    return r.returncode == 0, (r.stdout + r.stderr).strip()


def pull():
    if not is_cloned():
        return clone()
    r = subprocess.run(["git", "-C", str(REPO_DIR), "pull", "--ff-only"],
                       capture_output=True, text=True)
    return r.returncode == 0, (r.stdout + r.stderr).strip()


def sync_package_files():
    """Copy ~/.adscb/repo/adscb/ over the installed package directory.

    Returns (ok, message, pyproject_changed).
    """
    src_pkg = REPO_DIR / "adscb"
    if not src_pkg.is_dir():
        return False, f"no adscb/ in clone at {src_pkg}", False

    # Detect pyproject.toml change vs the marker we wrote on a previous sync.
    pyproject_changed = False
    src_pyproject = REPO_DIR / "pyproject.toml"
    if src_pyproject.exists():
        marker = INSTALLED_PKG_DIR / ".synced_pyproject"
        new = src_pyproject.read_bytes()
        if marker.exists():
            try:
                if marker.read_bytes() != new:
                    pyproject_changed = True
            except OSError:
                pass
        try:
            marker.write_bytes(new)
        except OSError:
            pass

    try:
        for src_file in src_pkg.rglob("*"):
            if src_file.is_dir() or "__pycache__" in src_file.parts:
                continue
            rel = src_file.relative_to(src_pkg)
            dst = INSTALLED_PKG_DIR / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file, dst)
    except (OSError, PermissionError) as e:
        return False, f"copy failed: {e}", pyproject_changed

    return True, "synced", pyproject_changed


def current_commit():
    if not is_cloned():
        return None
    r = subprocess.run(["git", "-C", str(REPO_DIR), "rev-parse", "--short", "HEAD"],
                       capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def current_branch():
    if not is_cloned():
        return None
    r = subprocess.run(["git", "-C", str(REPO_DIR), "rev-parse", "--abbrev-ref", "HEAD"],
                       capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def nuke():
    if REPO_DIR.exists():
        shutil.rmtree(REPO_DIR)

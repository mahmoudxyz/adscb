"""Discover and load problem modules.

Problems can come from two places:

1. **The installed package** (`adscb.problems.*`) — ships with whatever
   version of adscb you pipx-installed. Acts as a baseline.
2. **The user's content clone** at `~/.adscb/repo/adscb/problems/` —
   live git clone, updated via `adscb update`. If this directory
   exists, problems found here **override** the package versions.

This lets the prof push a problem fix and have students see it after
`adscb update`, with zero touching of the installed package.
"""
import importlib.util
import sys
from pathlib import Path

from .. import problems as problems_pkg
from ..config import PROBLEMS_SUBPATH, REPO_DIR


def _load_module_from_path(path: Path, unique_name: str):
    """Load a Python file as a module. Returns the module or None on error."""
    spec = importlib.util.spec_from_file_location(unique_name, path)
    if spec is None or spec.loader is None:
        return None
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception as e:
        print(f"[warn] could not load {path}: {e}", file=sys.stderr)
        return None
    return mod


def _scan_root(root: Path, prefix: str):
    """Walk a problems-root directory, yielding (problem_id, module) tuples.

    `prefix` is used to make module names unique between package and clone
    so Python's import cache doesn't confuse them.
    """
    if not root.is_dir():
        return
    for chapter_dir in sorted(root.iterdir()):
        if not chapter_dir.is_dir() or chapter_dir.name.startswith("_"):
            continue
        for file in sorted(chapter_dir.iterdir()):
            if not file.is_file() or file.suffix != ".py" or file.name.startswith("_"):
                continue
            unique = f"{prefix}__{chapter_dir.name}__{file.stem}"
            mod = _load_module_from_path(file, unique)
            if mod is None:
                continue
            if hasattr(mod, "META") and "id" in mod.META:
                yield mod.META["id"], mod


def _package_problems_root() -> Path:
    return Path(problems_pkg.__file__).parent


def _user_problems_root() -> Path:
    return REPO_DIR / PROBLEMS_SUBPATH


def discover_problems():
    """Return dict: problem_id -> loaded module.

    Package problems are loaded first; user-clone problems load second
    and overwrite any package problem with the same id.
    """
    result = {}
    # Layer 1: installed package baseline
    for pid, mod in _scan_root(_package_problems_root(), "pkg"):
        result[pid] = mod
    # Layer 2: live clone wins
    for pid, mod in _scan_root(_user_problems_root(), "user"):
        result[pid] = mod
    return result


def load_problem(problem_id: str):
    """Load a specific problem by id (or unique suffix)."""
    all_problems = discover_problems()
    if problem_id in all_problems:
        return all_problems[problem_id]
    matches = [pid for pid in all_problems if pid.endswith(problem_id) or problem_id in pid]
    if not matches:
        raise ValueError(f"unknown problem id '{problem_id}'")
    if len(matches) > 1:
        raise ValueError(
            f"ambiguous id '{problem_id}', matches:\n  " + "\n  ".join(matches)
        )
    return all_problems[matches[0]]


def source_of(problem_id: str) -> str:
    """Return 'user' if the problem comes from the live clone, 'pkg' otherwise."""
    for pid, _mod in _scan_root(_user_problems_root(), "src_check"):
        if pid == problem_id:
            return "user"
    return "pkg"

"""Discover and load problem modules from adscb.problems."""
import importlib
import sys
from pathlib import Path

from .. import problems as problems_pkg


def discover_problems():
    """Walk the adscb.problems package, return dict: problem_id -> module.

    Each problem file must define a module-level `META` dict with an `"id"` key.
    """
    result = {}
    root = Path(problems_pkg.__file__).parent
    for chapter_dir in sorted(root.iterdir()):
        if not chapter_dir.is_dir() or chapter_dir.name.startswith("_"):
            continue
        for file in sorted(chapter_dir.iterdir()):
            if not file.is_file() or file.suffix != ".py" or file.name.startswith("_"):
                continue
            module_name = f"adscb.problems.{chapter_dir.name}.{file.stem}"
            try:
                mod = importlib.import_module(module_name)
            except Exception as e:
                # Don't crash the whole listing if one problem file has an error —
                # report and skip.
                print(f"[warn] could not load {module_name}: {e}", file=sys.stderr)
                continue
            if hasattr(mod, "META") and "id" in mod.META:
                result[mod.META["id"]] = mod
    return result


def load_problem(problem_id):
    """Load (and reload) a specific problem module by id.

    Supports partial-suffix matching so you can type just
    `02_sllist_delete_recursive` instead of the full `ch04/...` prefix.
    """
    all_problems = discover_problems()

    if problem_id in all_problems:
        mod = all_problems[problem_id]
    else:
        matches = [pid for pid in all_problems if pid.endswith(problem_id) or problem_id in pid]
        if len(matches) == 0:
            raise ValueError(f"unknown problem id '{problem_id}'")
        if len(matches) > 1:
            raise ValueError(
                f"ambiguous id '{problem_id}', matches:\n  "
                + "\n  ".join(matches)
            )
        mod = all_problems[matches[0]]

    # Always reload so edits to problem files are picked up without restarting.
    importlib.reload(mod)
    return mod

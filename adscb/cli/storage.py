"""Filesystem storage for workspace files and progress.

Layout under ~/.adscb/ :

    workspace/
        ch04_data_structures__02_sllist_delete_recursive.py
        ...
    progress.json       # { problem_id: {solved, solved_at, attempts, hints_revealed} }
"""
import json
from datetime import datetime
from pathlib import Path

HOME = Path.home() / ".adscb"
WORKSPACE = HOME / "workspace"
PROGRESS_FILE = HOME / "progress.json"


def ensure_dirs():
    WORKSPACE.mkdir(parents=True, exist_ok=True)


def workspace_path(problem_id):
    """Map 'ch04/02_sllist_delete_recursive' to a concrete file path."""
    ensure_dirs()
    safe_id = problem_id.replace("/", "__")
    return WORKSPACE / f"{safe_id}.py"


def create_workspace_if_missing(problem_id, starter_code):
    path = workspace_path(problem_id)
    if not path.exists():
        path.write_text(starter_code)
    return path


def reset_workspace(problem_id, starter_code):
    path = workspace_path(problem_id)
    path.write_text(starter_code)
    return path


# ---------- progress ----------

def load_progress():
    if not PROGRESS_FILE.exists():
        return {}
    try:
        return json.loads(PROGRESS_FILE.read_text())
    except (json.JSONDecodeError, OSError):
        return {}


def save_progress(progress):
    ensure_dirs()
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2, sort_keys=True))


def _entry(progress, problem_id):
    if problem_id not in progress:
        progress[problem_id] = {}
    return progress[problem_id]


def mark_attempted(problem_id):
    progress = load_progress()
    e = _entry(progress, problem_id)
    e["attempts"] = e.get("attempts", 0) + 1
    e["last_attempt"] = datetime.now().isoformat(timespec="seconds")
    save_progress(progress)


def mark_solved(problem_id):
    progress = load_progress()
    e = _entry(progress, problem_id)
    if not e.get("solved"):
        e["solved"] = True
        e["solved_at"] = datetime.now().isoformat(timespec="seconds")
    save_progress(progress)


def is_solved(problem_id):
    return load_progress().get(problem_id, {}).get("solved", False)


def get_hints_revealed(problem_id):
    return load_progress().get(problem_id, {}).get("hints_revealed", 0)


def reveal_hint(problem_id):
    progress = load_progress()
    e = _entry(progress, problem_id)
    e["hints_revealed"] = e.get("hints_revealed", 0) + 1
    save_progress(progress)
    return e["hints_revealed"]

"""Command handlers wired up by __main__.py."""
import inspect
import os
import subprocess
import sys

from . import loader, render, runner, scanner, storage


def _resolve(problem_id):
    try:
        return loader.load_problem(problem_id)
    except ValueError as e:
        render.print_error(str(e))
        sys.exit(1)


def cmd_list(_args=None):
    problems = loader.discover_problems()
    progress = storage.load_progress()
    render.print_status(problems, progress)
    render.print_problem_list(problems, progress)


def cmd_status(_args=None):
    problems = loader.discover_problems()
    progress = storage.load_progress()
    render.print_status(problems, progress)


def cmd_show(args):
    mod = _resolve(args.problem_id)
    render.print_description(mod.META, mod.DESCRIPTION)


def cmd_start(args):
    mod = _resolve(args.problem_id)
    pid = mod.META["id"]
    path = storage.create_workspace_if_missing(pid, mod.STARTER)
    render.print_description(mod.META, mod.DESCRIPTION)
    render.print_info(f"workspace file: [bold]{path}[/]")
    render.print_info(f"edit it with:   [bold]adscb edit {pid}[/]")
    render.print_info(f"test it with:   [bold]adscb test {pid}[/]")
    render.console.print()


def cmd_edit(args):
    mod = _resolve(args.problem_id)
    pid = mod.META["id"]
    path = storage.create_workspace_if_missing(pid, mod.STARTER)
    editor = os.environ.get("EDITOR") or os.environ.get("VISUAL") or "vi"
    render.print_info(f"opening {path} in {editor}")
    try:
        subprocess.call([editor, str(path)])
    except FileNotFoundError:
        render.print_error(
            f"editor '{editor}' not found. Set $EDITOR or open the file yourself:\n  {path}"
        )


def cmd_test(args):
    mod = _resolve(args.problem_id)
    pid = mod.META["id"]
    path = storage.create_workspace_if_missing(pid, mod.STARTER)

    source = path.read_text()
    warnings = scanner.scan_solution(source, mod.META)

    passed, total, results = runner.run_tests(mod, path)
    storage.mark_attempted(pid)

    render.print_test_results(pid, passed, total, results, warnings)

    if total > 0 and passed == total:
        storage.mark_solved(pid)


def cmd_hint(args):
    mod = _resolve(args.problem_id)
    hints = getattr(mod, "HINTS", [])
    pid = mod.META["id"]
    if not hints:
        render.print_info("no hints available for this problem")
        return
    revealed = storage.get_hints_revealed(pid)
    if revealed >= len(hints):
        render.print_info(f"you've already seen all {len(hints)} hints — showing the last one again")
        idx = len(hints) - 1
    else:
        storage.reveal_hint(pid)
        idx = revealed
    render.print_hint(pid, idx + 1, len(hints), hints[idx])


def cmd_solution(args):
    mod = _resolve(args.problem_id)
    pid = mod.META["id"]
    if not storage.is_solved(pid) and not getattr(args, "force", False):
        render.print_error(
            "solve the problem first, or pass --force to see the reference anyway"
        )
        return
    try:
        src = inspect.getsource(mod.reference)
    except Exception:
        src = "# reference solution not available"
    render.print_reference(pid, src)


def cmd_reset(args):
    mod = _resolve(args.problem_id)
    pid = mod.META["id"]
    path = storage.reset_workspace(pid, mod.STARTER)
    render.print_success(f"reset {path}")

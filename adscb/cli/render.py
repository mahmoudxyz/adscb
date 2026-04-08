"""All terminal output goes through here. Uses Rich for colors + markdown."""
from rich import box
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table

console = Console()


# ---------- status & listing ----------

def print_status(problems, progress):
    total = len(problems)
    solved = sum(1 for pid in problems if progress.get(pid, {}).get("solved"))
    attempted = sum(
        1 for pid in problems
        if progress.get(pid, {}).get("attempts", 0) > 0 and not progress.get(pid, {}).get("solved")
    )

    # Content version line — only shown if the clone exists
    from . import updater
    content_line = ""
    if updater.is_cloned():
        commit = updater.current_commit()
        if commit:
            content_line = f"\n[dim]content: {commit}  ({updater.current_branch() or 'unknown'})  —  adscb update to refresh[/]"
    else:
        content_line = "\n[dim]content: baseline (package only)  —  adscb update to enable live updates[/]"

    console.print()
    console.print(Panel(
        f"[bold cyan]ADSCB[/]  Algorithms & Data Structures for Computational Biology\n"
        f"[green]{solved}[/] solved   [yellow]{attempted}[/] in progress   "
        f"[dim]{total - solved - attempted}[/] untouched   (total: {total})"
        f"{content_line}",
        border_style="cyan",
        box=box.ROUNDED,
    ))
    console.print()


def print_problem_list(problems, progress):
    if not problems:
        console.print("[yellow]no problems found[/]")
        return

    by_chapter = {}
    for pid, mod in problems.items():
        chapter = mod.META.get("chapter_title") or f"Chapter {mod.META.get('chapter', '?')}"
        by_chapter.setdefault(chapter, []).append((pid, mod))

    for chapter in sorted(by_chapter.keys()):
        table = Table(
            title=chapter,
            title_style="bold cyan",
            title_justify="left",
            box=box.SIMPLE,
            show_header=False,
            pad_edge=False,
        )
        table.add_column(width=3)  # status icon
        table.add_column(style="dim", no_wrap=True)  # id
        table.add_column()  # title
        table.add_column(style="dim", justify="right")  # difficulty

        items = sorted(by_chapter[chapter], key=lambda x: x[0])
        for pid, mod in items:
            p = progress.get(pid, {})
            if p.get("solved"):
                icon = "[green]✓[/]"
            elif p.get("attempts", 0) > 0:
                icon = "[yellow]●[/]"
            else:
                icon = "[dim]○[/]"
            diff = "★" * mod.META.get("difficulty", 1)
            table.add_row(icon, pid, mod.META.get("title", ""), diff)

        console.print(table)
        console.print()


# ---------- description ----------

def print_description(meta, description):
    title = f"{meta['id']}  —  {meta.get('title', '')}"
    console.print()
    console.print(Panel(
        Markdown(description),
        title=title,
        title_align="left",
        border_style="cyan",
        box=box.ROUNDED,
    ))
    console.print()


# ---------- tests ----------

def print_test_results(problem_id, passed, total, results, warnings):
    console.print()

    if warnings:
        for w in warnings:
            console.print(f"  [yellow]⚠[/] {w}")
        console.print()

    for name, ok, msg in results:
        if ok:
            console.print(f"  [green]✓[/] {name}")
        else:
            console.print(f"  [red]✗[/] [bold]{name}[/]")
            if msg:
                for line in msg.rstrip().splitlines():
                    console.print(f"      [dim]{line}[/]")

    console.print()
    if total == 0:
        console.print("[yellow]no tests ran[/]")
        return

    if passed == total:
        console.print(Panel(
            f"[bold green]All {total} tests passed.[/]  "
            f"Problem [bold]{problem_id}[/] is solved. 🎉",
            border_style="green",
            box=box.ROUNDED,
        ))
    else:
        bar_width = 24
        filled = int(bar_width * passed / total)
        bar = "█" * filled + "░" * (bar_width - filled)
        color = "yellow" if passed > 0 else "red"
        console.print(
            f"  [{color}]{bar}[/]  [bold]{passed}[/] / {total} passing"
        )
    console.print()


# ---------- hints & solution ----------

def print_hint(problem_id, hint_num, total_hints, hint_text):
    console.print()
    console.print(Panel(
        hint_text,
        title=f"Hint {hint_num} of {total_hints}  —  {problem_id}",
        title_align="left",
        border_style="yellow",
        box=box.ROUNDED,
    ))
    console.print()


def print_reference(problem_id, source):
    console.print()
    console.print(Panel(
        Syntax(source, "python", theme="monokai", line_numbers=True, background_color="default"),
        title=f"Reference solution  —  {problem_id}",
        title_align="left",
        border_style="magenta",
        box=box.ROUNDED,
    ))
    console.print()


# ---------- plain messages ----------

def print_error(msg):
    console.print(f"[red bold]error:[/] {msg}")


def print_info(msg):
    console.print(f"[cyan]→[/] {msg}")


def print_success(msg):
    console.print(f"[green]✓[/] {msg}")


def print_warning(msg):
    console.print(f"[yellow]⚠[/] {msg}")

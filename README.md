# adscb

A terminal practice tool for **Algorithms & Data Structures for Computational Biology**.

You browse problems from the course, edit your solution in your own editor, run `adscb test`, and get pretty feedback in the terminal. The data structures you use match the pseudocode from the slides — 1-indexed `Array`, `SLList`, `Stack` with `.top` as an index, circular `Queue` — not Python's built-in types. That way your code looks like the algorithms on the blackboard and the exam.

## Quick start (after you install — see below)

```bash
adscb                             # status + help
adscb list                        # all chapters and problems
adscb start ch00/01_hello         # ← start here, it's a 2-line warmup
adscb edit  ch00/01_hello         # opens $EDITOR
adscb test  ch00/01_hello         # runs tests
```

Problem IDs match on unique suffix, so `adscb test 01_hello` works too.

Once `01_hello` is green, move on to `ch04/01_sllist_search_recursive` and work through chapter 4. The intro problem exists purely to teach the workflow — every other problem is a real exercise.

## Install

Python 3.10 or newer is required. Pick whichever of these fits your setup.

### Option 1 — pipx (cleanest, recommended if you can)

pipx installs CLI tools in isolated virtual environments so they don't pollute your system Python. If you already have pipx, just:

```bash
git clone https://github.com/mahmoudxyz/adscb.git
cd adscb                  # the folder containing pyproject.toml
pipx install .
adscb list
```

**If `pipx` is not found**, install it first:

```bash
# Debian / Ubuntu / WSL
sudo apt install pipx
pipx ensurepath
exec zsh                  # or: exec bash — restart your shell

# macOS
brew install pipx
pipx ensurepath
exec zsh

# Any system with Python 3
python3 -m pip install --user pipx
python3 -m pipx ensurepath
exec zsh
```

Then run `cd adscb && pipx install .`. **The `exec zsh` (or `exec bash`) step matters** — `pipx ensurepath` adds `~/.local/bin` to your `PATH`, but the change only takes effect in a fresh shell.

### Option 2 — pip --user (shortest path, no isolation)

If you don't want to deal with pipx at all:

```bash
git clone https://github.com/mahmoudxyz/adscb.git
cd adscb
pip install --user .
adscb list
```

If `adscb: command not found` after this, your Python user-bin directory isn't on your `PATH`. Add it:

```bash
# Linux / macOS
export PATH="$HOME/.local/bin:$PATH"

# make it permanent — pick the file matching your shell
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc      # zsh
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc     # bash

exec zsh   # or exec bash
```

On macOS with Homebrew Python the path may be `~/Library/Python/3.11/bin` (adjust the version) — run `python3 -m site --user-base` to find it.

### Option 3 — venv (good middle ground)

Per-project isolation without pipx:

```bash
git clone https://github.com/mahmoudxyz/adscb.git
cd adscb
python3 -m venv .venv
source .venv/bin/activate
pip install .
adscb list
```

Downside: you need `source .venv/bin/activate` in each new terminal session before `adscb` works. Not ideal for a daily tool.

### Option 4 — no install at all (5-minute try-out)

```bash
git clone https://github.com/mahmoudxyz/adscb.git
cd adscb
pip install --user rich       # the only runtime dependency
python -m adscb.cli list
python -m adscb.cli start ch00/01_hello
```

Works anywhere, nothing installed globally. Good for a quick test before you commit to an install method.

### ## The primitives module

```python
from adscb.primitives import Array, SLList, DLList, Stack, Queue, CircularQueue, NIL
```

- **`Array(n)`** — 1-indexed fixed-size array. `A[0]` and `A[n+1]` raise `IndexError`. Tracks `.ops` for empirical complexity analysis.
- **`SLList`** — singly linked list. `L.head`. Nodes via `SLList.Node(k)` with `.key` and `.next`.
- **`DLList`** — doubly linked. Same pattern plus `.prev`.
- **`Stack`** — fixed capacity. `.top` is an integer index (0 means empty, matching the slides). `S.peek()` reads the top value without popping (equivalent to `top(S)` in pseudocode).
- **`CircularQueue`** (aliased as `Queue`) — circular-buffer queue with `.head`, `.tail`, `.size`, `.length`.
- **`NIL = None`** — so you can write `if x == NIL` just like the slides.

Every primitive has an `.ops` counter so you can empirically check complexity:

```python
A = Array.from_list([3, 1, 4, 1, 5, 9, 2, 6])
A.reset_ops()
# ... run your algorithm on A ...
print(A.ops)  # how many reads/writes did it do?
```

## Commands

```
adscb                             status + help
adscb list                        list all chapters and problems
adscb status                      just the progress summary
adscb show     <problem_id>       show a problem's description
adscb start    <problem_id>       create workspace file + show the problem
adscb edit     <problem_id>       open the workspace file in $EDITOR
adscb test     <problem_id>       run tests on your solution
adscb hint     <problem_id>       reveal the next hint
adscb solution <problem_id>       show the reference (after solving)
adscb reset    <problem_id>       reset workspace file to the starter template
```

## Current problem set

- **Chapter 0 — Intro** (1): `01_hello` — learn the workflow with a 2-line warmup.
- **Chapter 4 — Elementary Data Structures** (19):
  - `01`–`10` — the full exercise set from the lecture notes PDF (recursive search, recursive delete, recursive tail_insert, count occurrences, remove even, delete-and-duplicate, DLList insertion sort, stack/queue simulation, stack with O(1) min, recursive merge of sorted stacks).
  - `20`–`22` — build-it-yourself: implement SLList ops from raw Nodes, implement a `Stack` class from an Array, implement `CircularQueue` from scratch. Do these if you want to really feel the pointers.
  - `30`–`35` — classic problems: reverse SLList iteratively and recursively, find the middle node with two pointers, balanced parentheses, postfix expression evaluation, queue from two stacks.

More chapters coming: sorting, recurrences, trees, graphs, dynamic programming, alignment, BWT.

## Authoring problems

A problem is a single `.py` file dropped into `adscb/problems/chXX_topic/`. It defines:

```python
META = {
    "id": "ch04/99_example",
    "title": "A short title",
    "chapter": 4,
    "chapter_title": "Chapter 4 — Elementary Data Structures",
    "difficulty": 2,                  # 1–3, shown as stars
    "requires_recursion": True,       # AST-checked → warning if absent
    "entry": "solution",              # function the student must define
    "suggest_primitives": ["SLList"], # soft nudge away from Python list
}

DESCRIPTION = """
# Markdown description

Renders in the terminal with Rich. Supports code blocks, lists, etc.
"""

STARTER = '''\
from adscb.primitives import SLList

def solution(head, k):
    pass
'''

HINTS = [
    "First hint — vague.",
    "Second hint — more specific.",
    "Third hint — almost gives it away.",
]

def reference(head, k):
    # Hidden reference. Shown only after the student solves it.
    ...

def tests(student):
    def case_one():
        assert student(...) == ...
    return [("case one", case_one)]
```

The CLI auto-discovers problems on every launch. Add a file, save, and it shows up — no registry, no restart. `importlib.reload` is called on each access, so in-session edits to a problem file are picked up immediately.

## Design notes

- **Suggest, don't enforce.** The scanner warns about Python `list` usage or missing recursion, but tests still run. Let students see the warning, decide for themselves.
- **Their editor, their workflow.** The tool opens `$EDITOR` (or `$VISUAL`, falling back to `vi`). It does not embed an editor.
- **No database.** Problems are `.py` files. Progress is a JSON file. That's the whole state model.
- **Never crashes on broken student code.** The runner catches every exception and reports it as a failing test case.

## Data locations

Your workspace files and progress live under `~/.adscb/`:

```
~/.adscb/
  workspace/          # your solution files, one per problem
  progress.json       # which problems are solved, attempts, hints revealed
```

You can edit the workspace files directly in any editor — `adscb edit` is just a shortcut. You can also delete `progress.json` any time to start fresh. The primitives package and problem definitions are not stored here; they live in the installed package.

## Roadmap

- More chapters: sorting (next), recurrences, trees, graphs, DP, alignment, BWT
- Quiz-type problems (complexity answers, not just code)
- `adscb visualize` — step through student code on small inputs and show the list/stack state at each step as ASCII
- `adscb exam` — timed random selection of N problems from a chapter range
- Auto-sync: `git pull` on launch if the package is a git clone, so problem fixes ship without reinstall

## License

MIT

META = {
    "id": "ch00/01_hello",
    "title": "Hello, adscb — your first problem",
    "chapter": 0,
    "chapter_title": "Chapter 0 — Intro",
    "difficulty": 1,
    "requires_recursion": False,
    "entry": "first_key",
}

DESCRIPTION = """
# Hello, adscb 👋

Welcome. This is your first problem — it's **deliberately trivial**,
so you can learn the workflow without fighting an algorithm at the
same time. Once you've solved this one, the rest of the tool will
feel familiar.

## The task

Given the head node of a singly linked list, return the **key** of
the first node. If the list is empty (head is `None`), return `None`.

## Signature

```python
def first_key(head):
    # head is an SLList.Node or None
    # returns the key of the head node, or None
    ...
```

## Examples

    head → [10] → [-1] → [4] → /       first_key(head)  →  10
    head → [99] → /                     first_key(head)  →  99
    head → /                             first_key(head)  →  None

That's it. Two lines of code. The point is the **workflow**, not
the problem.

## How to solve this (the workflow)

1. **Read this description** — you're doing that now. Good start.

2. **Open your solution file in your editor.** Run:

   ```
   adscb edit ch00/01_hello
   ```

   That opens a pre-made file in `$EDITOR` (or VS Code, vim,
   whatever you've configured). The file already contains a
   starter template with the function signature.

3. **Write your solution.** For this problem, it's two lines:

   ```python
   def first_key(head):
       if head is None:
           return None
       return head.key
   ```

   Save the file.

4. **Test it.** Back in your terminal:

   ```
   adscb test ch00/01_hello
   ```

   You should see green checkmarks and a "problem solved" banner.

5. **Celebrate.** Then move on to `ch04/01_sllist_search_recursive`.

## Tips

- Your solution file lives at `~/.adscb/workspace/`. You can open it
  directly in VS Code if you prefer — `adscb edit` is just a
  convenience.
- If you get stuck on any problem, `adscb hint <id>` reveals hints
  one at a time.
- `adscb solution <id>` shows the reference solution, but only
  after you've solved the problem yourself (or with `--force`).
- Problem IDs match on unique suffix, so `adscb test 01_hello`
  works just as well as the full `ch00/01_hello`.
"""

STARTER = '''\
from adscb.primitives import SLList


def first_key(head):
    """Return the key of the head node, or None if head is None."""
    # your code here — it's only two lines, promise
    pass
'''

HINTS = [
    "If head is None, return None.",
    "Otherwise return head.key. That's the whole function.",
]


def reference(head):
    if head is None:
        return None
    return head.key


def tests(student):
    from adscb.primitives import SLList

    def case_empty():
        assert student(None) is None, "empty list should return None"

    def case_single():
        L = SLList.from_list([42])
        assert student(L.head) == 42

    def case_multi():
        L = SLList.from_list([10, -1, 4, 1])
        assert student(L.head) == 10, "should return the FIRST key, not any other"

    def case_string_key():
        L = SLList.from_list(["hello", "world"])
        assert student(L.head) == "hello"

    def case_zero_key():
        # Careful: 0 is falsy in Python. `if head.key:` would be a bug here.
        L = SLList.from_list([0, 1, 2])
        assert student(L.head) == 0, \
            "zero should be returned correctly — watch out for truthiness bugs"

    return [
        ("empty list returns None", case_empty),
        ("single-node list", case_single),
        ("multi-node list — returns first key only", case_multi),
        ("string keys work too", case_string_key),
        ("zero key (don't confuse with None)", case_zero_key),
    ]

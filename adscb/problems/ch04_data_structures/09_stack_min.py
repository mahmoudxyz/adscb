META = {
    "id": "ch04/09_stack_min",
    "title": "Stack with O(1) minimum",
    "chapter": 4,
    "chapter_title": "Chapter 4 — Elementary Data Structures",
    "difficulty": 3,
    "requires_recursion": False,
    "entry": "solve",
    "suggest_primitives": ["Stack"],
}

DESCRIPTION = """
# Stack with O(1) minimum

Given two stacks `S1` and `S2` (both support the usual `push`, `pop`,
`peek`, `is_empty` operations in O(1)), implement two operations:

- `push2(S1, S2, x)` — push `x` on `S1`, keeping the current minimum
  of `S1` on top of `S2`.
- `pop2(S1, S2)` — pop from `S1` and return the value, keeping the
  current minimum of `S1` on top of `S2`.

Both must run in **O(1)**. You may only use `push`, `pop`, `peek`,
`is_empty` on the stacks — no peeking under the top, no extra loops.

This is Exercise 9 from the lecture notes.

## What you write

Because this problem needs two functions working together, define a
single entry function `solve` that returns a tuple `(push2, pop2)`:

```python
def solve():
    def push2(S1, S2, x):
        ...
    def pop2(S1, S2):
        ...
    return push2, pop2
```

## Hints

- When you push `x` on `S1`, when should `x` also go on `S2`?
- When you pop from `S1`, when should you also pop from `S2`?
- Hint: `S2`'s top is always equal to the current minimum of `S1`.
"""

STARTER = '''\
from adscb.primitives import Stack


def solve():
    """Return (push2, pop2)."""

    def push2(S1, S2, x):
        # push x on S1; keep min of S1 on top of S2
        pass

    def pop2(S1, S2):
        # pop from S1 and return; keep min of S1 on top of S2
        pass

    return push2, pop2
'''

HINTS = [
    "push2: always push x on S1. Then push x on S2 only if S2 is empty "
    "or the current top of S2 is >= x.",
    "pop2: pop x from S1. If x equals the current top of S2, pop S2 too. Return x.",
    "Both operations use only push/pop/peek/is_empty — no loops, so both are O(1).",
]


def reference():
    def push2(S1, S2, x):
        S1.push(x)
        if S2.is_empty() or S2.peek() >= x:
            S2.push(x)

    def pop2(S1, S2):
        x = S1.pop()
        if not S2.is_empty() and x == S2.peek():
            S2.pop()
        return x

    return push2, pop2


def tests(student):
    from adscb.primitives import Stack

    def _fresh():
        return Stack(32), Stack(32)

    def case_returns_two_callables():
        result = student()
        assert isinstance(result, tuple) and len(result) == 2, \
            "solve() must return a tuple (push2, pop2)"
        push2, pop2 = result
        assert callable(push2) and callable(pop2), "both must be callable"

    def case_single_push_pop():
        push2, pop2 = student()
        S1, S2 = _fresh()
        push2(S1, S2, 5)
        assert S2.peek() == 5, "after pushing 5 on empty, min should be 5"
        assert pop2(S1, S2) == 5
        assert S1.is_empty() and S2.is_empty()

    def case_min_tracking():
        push2, pop2 = student()
        S1, S2 = _fresh()
        for v in [5, 3, 7, 2, 8, 2, 9]:
            push2(S1, S2, v)
            # S2's top must always equal min of what's in S1
        assert S2.peek() == 2, f"min should be 2, got S2.peek()={S2.peek()}"

    def case_pop_preserves_min():
        push2, pop2 = student()
        S1, S2 = _fresh()
        for v in [5, 3, 7, 2, 8]:
            push2(S1, S2, v)
        assert S2.peek() == 2
        assert pop2(S1, S2) == 8
        assert S2.peek() == 2, "popping 8 should not change min"
        assert pop2(S1, S2) == 2
        assert S2.peek() == 3, f"after popping 2, min should be 3, got {S2.peek()}"
        assert pop2(S1, S2) == 7
        assert S2.peek() == 3
        assert pop2(S1, S2) == 3
        assert S2.peek() == 5
        assert pop2(S1, S2) == 5
        assert S1.is_empty() and S2.is_empty()

    def case_duplicates():
        push2, pop2 = student()
        S1, S2 = _fresh()
        for v in [3, 3, 3, 3]:
            push2(S1, S2, v)
        # all equal → min stays 3 throughout
        for _ in range(4):
            assert S2.peek() == 3
            assert pop2(S1, S2) == 3
        assert S2.is_empty()

    def case_ascending():
        push2, pop2 = student()
        S1, S2 = _fresh()
        for v in [1, 2, 3, 4, 5]:
            push2(S1, S2, v)
        assert S2.peek() == 1
        for expected in [5, 4, 3, 2, 1]:
            assert pop2(S1, S2) == expected

    return [
        ("solve() returns (push2, pop2)", case_returns_two_callables),
        ("single push then pop", case_single_push_pop),
        ("min updates as values are pushed", case_min_tracking),
        ("pop preserves min correctly", case_pop_preserves_min),
        ("handles duplicate values", case_duplicates),
        ("ascending sequence", case_ascending),
    ]

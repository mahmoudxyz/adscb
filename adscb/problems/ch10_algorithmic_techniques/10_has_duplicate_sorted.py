META = {
    "id": "ch10/10_has_duplicate_sorted",
    "title": "Duplicates in Sorted Array — Divide & Conquer",
    "chapter": 10,
    "chapter_title": "Chapter 10 — Algorithmic Techniques",
    "difficulty": 2,
    "requires_recursion": True,
    "entry": "has_duplicate",
}

DESCRIPTION = """
# Duplicates in Sorted Array — Divide & Conquer

Given a **sorted** array of integers `A`, return `True` if any value appears
more than once, `False` otherwise.

Implement the **divide and conquer** recursive solution (not the simple linear scan).

## Signature

```python
def has_duplicate(A):
    # A: sorted list of integers (may be empty)
    # returns: bool
    ...
```

## Examples

    A = [1, 2, 2, 3]    →  True
    A = [1, 2, 3, 4]    →  False
    A = []              →  False
    A = [5]             →  False

## Algorithm — Divide & Conquer

Key observation: in a **sorted** array, duplicates must be **adjacent**. So when
we split at midpoint `q`, a duplicate either:

1. lies entirely in `A[p..q]`, or
2. lies entirely in `A[q+1..r]`, or
3. **crosses** the midpoint, i.e. `A[q] == A[q+1]`

```
function _rec(p, r):
    if p >= r: return False
    q = (p + r) // 2
    return A[q] == A[q+1]  or  _rec(p, q)  or  _rec(q+1, r)
```

Short-circuit evaluation: if `A[q] == A[q+1]` is `True`, no recursive calls needed.

## Complexity

- **Worst case:** Θ(n) — no duplicates; full tree is explored.
  T(n) = 2T(n/2) + 1 → T(n) = Θ(n).
- **Best case:** O(1) — A[q] == A[q+1] on the first call.

## Notes

- The brute-force solution (scan adjacent pairs) is also Θ(n) worst-case —
  but the D&C version has a better best case and demonstrates the technique.
- The key insight is that duplicates **must be adjacent** in a sorted array.
"""

STARTER = '''\
def has_duplicate(A):
    """Return True if any value appears twice in sorted A (divide & conquer)."""
    def _rec(p, r):
        if p >= r:
            return False
        q = (p + r) // 2
        # your code here — check crossing, recurse left, recurse right
        pass
    if not A:
        return False
    return _rec(0, len(A) - 1)
'''

HINTS = [
    "Check if the duplicate crosses the split: `A[q] == A[q+1]`. If yes, return True immediately.",
    "Recurse on both halves with `_rec(p, q)` and `_rec(q+1, r)`. Use `or` for short-circuit evaluation.",
    "return A[q] == A[q+1] or _rec(p, q) or _rec(q+1, r)",
]


def reference(A):
    def _rec(p, r):
        if p >= r:
            return False
        q = (p + r) // 2
        return A[q] == A[q + 1] or _rec(p, q) or _rec(q + 1, r)

    if not A:
        return False
    return _rec(0, len(A) - 1)


def tests(student):
    def case_has_dup():
        assert student([1, 2, 2, 3]) is True

    def case_no_dup():
        assert student([1, 2, 3, 4]) is False

    def case_empty():
        assert student([]) is False

    def case_single():
        assert student([5]) is False

    def case_two_same():
        assert student([3, 3]) is True

    def case_two_different():
        assert student([3, 4]) is False

    def case_all_same():
        assert student([7, 7, 7, 7]) is True

    def case_dup_at_start():
        assert student([1, 1, 3, 5, 7]) is True

    def case_dup_at_end():
        assert student([1, 3, 5, 7, 7]) is True

    def case_large_no_dup():
        A = list(range(100))
        assert student(A) is False

    def case_large_with_dup():
        A = list(range(50)) + [49] + list(range(50, 99))
        A.sort()
        assert student(A) is True

    return [
        ("has duplicate [1,2,2,3]", case_has_dup),
        ("no duplicate [1,2,3,4]", case_no_dup),
        ("empty list", case_empty),
        ("single element", case_single),
        ("two same", case_two_same),
        ("two different", case_two_different),
        ("all same [7,7,7,7]", case_all_same),
        ("duplicate at start", case_dup_at_start),
        ("duplicate at end", case_dup_at_end),
        ("large no duplicate", case_large_no_dup),
        ("large with duplicate", case_large_with_dup),
    ]

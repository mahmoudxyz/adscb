META = {
    "id": "ch10/12_fixed_point",
    "title": "Fixed Point in Sorted Distinct Array",
    "chapter": 10,
    "chapter_title": "Chapter 10 — Algorithmic Techniques",
    "difficulty": 2,
    "requires_recursion": True,
    "entry": "has_fixed_point",
}

DESCRIPTION = """
# Fixed Point in Sorted Distinct Array

Given a sorted array of **distinct** integers `A` (0-indexed), return `True` if
there exists an index `i` such that `A[i] == i` (a **fixed point**), `False` otherwise.

Implement the **divide and conquer** solution that runs in **Θ(log n)** worst case.

## Signature

```python
def has_fixed_point(A):
    # A: sorted list of distinct integers (0-indexed)
    # returns: bool
    ...
```

## Examples

    A = [-10, -1, 0, 3, 10, 11, 30]   →  True   (A[3] == 3)
    A = [1, 2, 3, 4]                  →  False  (A[i] > i for all i)
    A = [-5, -3, 2, 3]                →  True   (A[2]==2 or A[3]==3)
    A = []                            →  False

## Algorithm — Divide & Conquer Θ(log n)

Key property of sorted **distinct** integers:
- If `A[q] > q` → every element to the right of `q` is even larger, so
  `A[j] >= A[q] > q >= j` is impossible for j > q → no fixed point in `A[q..r]`.
  Only recurse **left**.
- If `A[q] < q` → symmetrically, no fixed point in `A[p..q]`. Only recurse **right**.
- If `A[q] == q` → found it, return True.

```
function _rec(p, r):
    if p > r: return False
    q = (p + r) // 2
    if A[q] == q:  return True
    elif A[q] > q: return _rec(p, q - 1)
    else:          return _rec(q + 1, r)
```

## Complexity

- **Worst case:** Θ(log n) — one branch per level, height log n.
  T(n) = T(n/2) + 1 → T(n) = Θ(log n)
- **Best case:** O(1) — midpoint is a fixed point.

## Notes

- The Θ(log n) bound only holds when elements are **distinct** and **sorted**.
  With duplicates the trick breaks (you'd need to search both halves).
- Brute force scan is Θ(n); this D&C version is Θ(log n) — a genuine speedup.
"""

STARTER = '''\
def has_fixed_point(A):
    """Return True if A[i]==i for some i, using divide & conquer O(log n)."""
    def _rec(p, r):
        if p > r:
            return False
        q = (p + r) // 2
        if A[q] == q:
            return True
        # your code here — which half to recurse into?
        pass
    if not A:
        return False
    return _rec(0, len(A) - 1)
'''

HINTS = [
    "If A[q] > q, all elements right of q are even larger (sorted, distinct), so no fixed point there. Recurse left: _rec(p, q-1).",
    "If A[q] < q, all elements left of q are even smaller, so no fixed point there. Recurse right: _rec(q+1, r).",
    "elif A[q] > q: return _rec(p, q-1)\nelse: return _rec(q+1, r)",
]


def reference(A):
    def _rec(p, r):
        if p > r:
            return False
        q = (p + r) // 2
        if A[q] == q:
            return True
        elif A[q] > q:
            return _rec(p, q - 1)
        else:
            return _rec(q + 1, r)

    if not A:
        return False
    return _rec(0, len(A) - 1)


def tests(student):
    def case_example():
        assert student([-10, -1, 0, 3, 10, 11, 30]) is True  # A[3]==3

    def case_no_fixed():
        assert student([1, 2, 3, 4]) is False

    def case_all_shifted_left():
        assert student([-5, -3, 2, 3]) is True  # A[2]==2

    def case_empty():
        assert student([]) is False

    def case_single_match():
        assert student([0]) is True

    def case_single_no_match():
        assert student([5]) is False

    def case_fixed_at_start():
        assert student([0, 2, 4, 6]) is True

    def case_fixed_at_end():
        assert student([-3, -1, 1, 3]) is True  # A[3]==3

    def case_all_negative():
        assert student([-5, -3, -1]) is False

    def case_large_no_fixed():
        # A[i] = i+1 for all i → no fixed point
        A = list(range(1, 101))
        assert student(A) is False

    def case_large_with_fixed():
        # A[i] = i for all i: sorted distinct array of 0..99
        A = list(range(0, 100))
        assert student(A) is True  # A[0]==0, A[1]==1, etc.

    def case_fixed_at_boundary():
        assert student([-2, -1, 2, 5]) is True  # A[2]==2

    return [
        ("example A[3]==3", case_example),
        ("no fixed point all shifted right", case_no_fixed),
        ("fixed point at index 2", case_all_shifted_left),
        ("empty", case_empty),
        ("single match A[0]==0", case_single_match),
        ("single no match", case_single_no_match),
        ("fixed at start index 0", case_fixed_at_start),
        ("fixed at end", case_fixed_at_end),
        ("all negative no fixed", case_all_negative),
        ("large array no fixed", case_large_no_fixed),
        ("large array with fixed", case_large_with_fixed),
        ("fixed at boundary", case_fixed_at_boundary),
    ]

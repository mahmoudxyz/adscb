META = {
    "id": "ch10/11_is_sorted",
    "title": "Is Array Sorted — Divide & Conquer",
    "chapter": 10,
    "chapter_title": "Chapter 10 — Algorithmic Techniques",
    "difficulty": 2,
    "requires_recursion": True,
    "entry": "is_sorted",
}

DESCRIPTION = """
# Is Array Sorted — Divide & Conquer

Given an array of integers `A`, return `True` if `A` is sorted in
**non-decreasing order**, `False` otherwise.

Implement the **divide and conquer** recursive solution.

## Signature

```python
def is_sorted(A):
    # A: list of integers (may be empty)
    # returns: bool
    ...
```

## Examples

    A = [1, 2, 3, 4]    →  True
    A = [1, 2, 2, 4]    →  True   (equal adjacent elements are OK)
    A = [1, 3, 2, 4]    →  False
    A = []              →  True
    A = [5]             →  True

## Algorithm — Divide & Conquer

Split at midpoint `q`. The array is sorted if and only if:
1. The **crossing pair** `A[q] <= A[q+1]` is in order, **and**
2. `A[p..q]` is sorted, **and**
3. `A[q+1..r]` is sorted

```
function _rec(p, r):
    if p >= r: return True
    q = (p + r) // 2
    return A[q] <= A[q+1]  and  _rec(p, q)  and  _rec(q+1, r)
```

Short-circuit: if `A[q] > A[q+1]`, no recursive calls needed.

## Complexity

- **Worst case:** Θ(n) — array is sorted; full tree explored.
  T(n) = 2T(n/2) + 1 → T(n) = Θ(n)
- **Best case:** O(1) — A[q] > A[q+1] on the first call.

## Notes

The every adjacent pair (i, i+1) is checked exactly once as the midpoint
boundary of some subproblem. Convince yourself: pair (0,1) is checked when
p=0,r=1; pair (1,2) is checked when p=0,r=3 with q=1; etc.
"""

STARTER = '''\
def is_sorted(A):
    """Return True if A is sorted non-decreasingly (divide & conquer)."""
    def _rec(p, r):
        if p >= r:
            return True
        q = (p + r) // 2
        # check crossing pair, recurse on both halves
        pass
    if not A:
        return True
    return _rec(0, len(A) - 1)
'''

HINTS = [
    "Check the boundary: `A[q] <= A[q+1]`. If this is False, return False immediately.",
    "Recurse: `_rec(p, q) and _rec(q+1, r)`. Short-circuit means you stop at the first False.",
    "return A[q] <= A[q+1] and _rec(p, q) and _rec(q+1, r)",
]


def reference(A):
    def _rec(p, r):
        if p >= r:
            return True
        q = (p + r) // 2
        return A[q] <= A[q + 1] and _rec(p, q) and _rec(q + 1, r)

    if not A:
        return True
    return _rec(0, len(A) - 1)


def tests(student):
    def case_sorted():
        assert student([1, 2, 3, 4]) is True

    def case_unsorted():
        assert student([1, 3, 2, 4]) is False

    def case_equal_adjacent():
        assert student([1, 2, 2, 4]) is True

    def case_all_equal():
        assert student([5, 5, 5]) is True

    def case_empty():
        assert student([]) is True

    def case_single():
        assert student([7]) is True

    def case_two_sorted():
        assert student([1, 2]) is True

    def case_two_unsorted():
        assert student([2, 1]) is False

    def case_reverse():
        assert student([5, 4, 3, 2, 1]) is False

    def case_almost_sorted():
        assert student([1, 2, 3, 5, 4]) is False

    def case_large_sorted():
        A = list(range(200))
        assert student(A) is True

    def case_large_unsorted():
        A = list(range(200))
        A[150] = 0
        assert student(A) is False

    return [
        ("sorted [1,2,3,4]", case_sorted),
        ("unsorted [1,3,2,4]", case_unsorted),
        ("equal adjacent OK", case_equal_adjacent),
        ("all equal", case_all_equal),
        ("empty", case_empty),
        ("single", case_single),
        ("two sorted", case_two_sorted),
        ("two unsorted", case_two_unsorted),
        ("reverse sorted", case_reverse),
        ("almost sorted (last pair swapped)", case_almost_sorted),
        ("large sorted", case_large_sorted),
        ("large unsorted", case_large_unsorted),
    ]

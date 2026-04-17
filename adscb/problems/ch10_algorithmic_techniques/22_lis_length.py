META = {
    "id": "ch10/22_lis_length",
    "title": "Longest Increasing Subsequence — Length",
    "chapter": 10,
    "chapter_title": "Chapter 10 — Algorithmic Techniques",
    "difficulty": 2,
    "requires_recursion": False,
    "entry": "lis_length",
}

DESCRIPTION = """
# Longest Increasing Subsequence — Length

Given a list of integers `A`, return the length of its **longest strictly
increasing subsequence** (LIS).

A **subsequence** is obtained by deleting elements (not necessarily adjacent)
without changing order. **Strictly increasing** means each element is greater
than the previous one.

## Signature

```python
def lis_length(A):
    # A: list of integers (may be empty)
    # returns: int
    ...
```

## Examples

    A = [10, 9, 2, 5, 3, 7, 101, 18]  →  4   (e.g. [2,3,7,18] or [2,5,7,18])
    A = [0, 1, 0, 3, 2, 3]            →  4   ([0,1,2,3] or [0,1,3])
    A = [7, 7, 7, 7]                  →  1   (strictly increasing: no equal)
    A = []                            →  0

## Algorithm — DP O(n²)

Define `dp[i]` = length of the LIS **ending at index i**.

    dp[i] = 1 + max(dp[j] for j < i if A[j] < A[i])
          = 1   if no such j exists

```
dp = [1] * n
for i in 1 .. n-1:
    for j in 0 .. i-1:
        if A[j] < A[i]:
            dp[i] = max(dp[i], dp[j] + 1)
return max(dp)
```

## Complexity

- **Time:** O(n²)
- **Space:** O(n)

(An O(n log n) solution exists using patience sorting / binary search, but the
O(n²) DP is what you need to understand the DP structure.)

## Relation to LCS

LIS of `A` equals `lcs_length(A, sorted(set(A)))`. The DP recurrence is
similar in spirit to LCS — both rely on "best extension" from smaller sub-problems.

## Notes

- Return 0 for an empty array.
- Strictly increasing: `A[j] < A[i]`, not `<=`.
"""

STARTER = '''\
def lis_length(A):
    """Return the length of the longest strictly increasing subsequence."""
    if not A:
        return 0
    n = len(A)
    dp = [1] * n
    for i in range(1, n):
        for j in range(i):
            if A[j] < A[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)
'''

HINTS = [
    "dp[i] starts at 1 (the element itself is a subsequence of length 1).",
    "For each i, scan all j < i. If A[j] < A[i]: dp[i] = max(dp[i], dp[j]+1).",
    "The answer is max(dp) — not dp[n-1], because the LIS may not end at the last element.",
]


def reference(A):
    if not A:
        return 0
    n = len(A)
    dp = [1] * n
    for i in range(1, n):
        for j in range(i):
            if A[j] < A[i]:
                if dp[j] + 1 > dp[i]:
                    dp[i] = dp[j] + 1
    return max(dp)


def tests(student):
    def case_example1():
        assert student([10, 9, 2, 5, 3, 7, 101, 18]) == 4

    def case_example2():
        assert student([0, 1, 0, 3, 2, 3]) == 4

    def case_all_same():
        assert student([7, 7, 7, 7]) == 1  # strictly increasing → no equal

    def case_empty():
        assert student([]) == 0

    def case_single():
        assert student([5]) == 1

    def case_sorted():
        assert student([1, 2, 3, 4, 5]) == 5

    def case_reverse():
        assert student([5, 4, 3, 2, 1]) == 1

    def case_two():
        assert student([1, 2]) == 2
        assert student([2, 1]) == 1

    def case_alternating():
        assert student([1, 3, 2, 4]) == 3  # [1,3,4] or [1,2,4]

    def case_plateau():
        assert student([1, 2, 2, 3]) == 3  # [1,2,3]

    def case_large_strictly():
        A = list(range(50))
        assert student(A) == 50

    return [
        ("[10,9,2,5,3,7,101,18] → 4", case_example1),
        ("[0,1,0,3,2,3] → 4", case_example2),
        ("all equal → 1 (strictly increasing)", case_all_same),
        ("empty → 0", case_empty),
        ("single → 1", case_single),
        ("sorted → n", case_sorted),
        ("reverse sorted → 1", case_reverse),
        ("two elements", case_two),
        ("alternating [1,3,2,4] → 3", case_alternating),
        ("plateau [1,2,2,3] → 3", case_plateau),
        ("large sorted array", case_large_strictly),
    ]

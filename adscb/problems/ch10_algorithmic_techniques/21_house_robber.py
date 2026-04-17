META = {
    "id": "ch10/21_house_robber",
    "title": "House Robber — Max Sum No Adjacent",
    "chapter": 10,
    "chapter_title": "Chapter 10 — Algorithmic Techniques",
    "difficulty": 2,
    "requires_recursion": False,
    "entry": "max_rob",
}

DESCRIPTION = """
# House Robber — Max Sum No Adjacent

Given a list of non-negative integers `A` (amounts in each house), return the
**maximum sum** you can collect without taking from two adjacent positions.

You cannot rob two houses directly next to each other (`A[i]` and `A[i+1]`).

## Signature

```python
def max_rob(A):
    # A: list of non-negative integers
    # returns: int
    ...
```

## Examples

    A = [1, 2, 3, 1]    →  4    (A[0] + A[2] = 1 + 3)
    A = [2, 7, 9, 3, 1] →  12   (A[0] + A[2] + A[4] = 2 + 9 + 1)
    A = [5]             →  5
    A = []              →  0

## Algorithm — DP O(n) time, O(1) space

Define `dp[i]` = max amount robbing from the first `i` houses.

    dp[0] = A[0]
    dp[1] = max(A[0], A[1])
    dp[i] = max(dp[i-1], dp[i-2] + A[i])   for i >= 2

Optimal substructure: at house `i`, either skip it (take `dp[i-1]`) or rob it
(take `dp[i-2] + A[i]`). The greedy-like one-pass DP:

```
prev2, prev1 = A[0], max(A[0], A[1])
for i = 2 .. n-1:
    prev2, prev1 = prev1, max(prev1, prev2 + A[i])
return prev1
```

## Complexity

- **Time:** Θ(n)
- **Space:** O(1) — only two rolling variables needed

## Notes

- This is the same rolling-variable trick as Fibonacci DP.
- The recurrence `dp[i] = max(dp[i-1], dp[i-2] + A[i])` has the same shape as
  Kadane's algorithm — both are "extend or restart" DP patterns.
- Handle empty and single-element arrays as special cases.
"""

STARTER = '''\
def max_rob(A):
    """Return the max sum of non-adjacent elements in A."""
    if not A:
        return 0
    if len(A) == 1:
        return A[0]
    prev2, prev1 = A[0], max(A[0], A[1])
    for i in range(2, len(A)):
        # either skip A[i] (keep prev1) or rob A[i] (prev2 + A[i])
        pass
    return prev1
'''

HINTS = [
    "At each position i: new = max(prev1, prev2 + A[i]).",
    "Then slide the window: prev2, prev1 = prev1, new.",
    "Combine: prev2, prev1 = prev1, max(prev1, prev2 + A[i]).",
]


def reference(A):
    if not A:
        return 0
    if len(A) == 1:
        return A[0]
    prev2, prev1 = A[0], max(A[0], A[1])
    for i in range(2, len(A)):
        prev2, prev1 = prev1, max(prev1, prev2 + A[i])
    return prev1


def tests(student):
    def case_example1():
        assert student([1, 2, 3, 1]) == 4   # 1+3

    def case_example2():
        assert student([2, 7, 9, 3, 1]) == 12  # 2+9+1

    def case_empty():
        assert student([]) == 0

    def case_single():
        assert student([5]) == 5

    def case_two():
        assert student([3, 1]) == 3
        assert student([1, 3]) == 3

    def case_all_equal():
        assert student([5, 5, 5, 5, 5]) == 15  # pick 0,2,4

    def case_best_skip():
        # skip the large middle element to get two moderate ones
        assert student([10, 1, 1, 10]) == 20  # A[0]+A[3]

    def case_best_take_all_odd():
        assert student([3, 10, 3, 1, 2]) == 12   # 10+2 (positions 1 and 4)

    def case_zeros():
        assert student([0, 0, 0]) == 0

    def case_decreasing():
        assert student([5, 4, 3, 2, 1]) == 9   # 5+3+1

    def case_alternating():
        assert student([1, 100, 1, 100, 1]) == 200  # 100+100

    return [
        ("[1,2,3,1] → 4", case_example1),
        ("[2,7,9,3,1] → 12", case_example2),
        ("empty → 0", case_empty),
        ("single element", case_single),
        ("two elements → max of two", case_two),
        ("all equal → pick every other", case_all_equal),
        ("best to skip — [10,1,1,10] → 20", case_best_skip),
        ("mixed [3,10,3,1,2] → 8", case_best_take_all_odd),
        ("all zeros → 0", case_zeros),
        ("decreasing [5,4,3,2,1] → 9", case_decreasing),
        ("alternating [1,100,1,100,1] → 200", case_alternating),
    ]

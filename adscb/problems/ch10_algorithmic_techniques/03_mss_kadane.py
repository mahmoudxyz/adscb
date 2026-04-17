META = {
    "id": "ch10/03_mss_kadane",
    "title": "Maximum Sum Subarray — Kadane's (DP/Greedy)",
    "chapter": 10,
    "chapter_title": "Chapter 10 — Algorithmic Techniques",
    "difficulty": 1,
    "requires_recursion": False,
    "entry": "mss_kadane",
}

DESCRIPTION = """
# Maximum Sum Subarray — Kadane's Algorithm (DP / Greedy)

Given an array of integers `A`, find the **maximum sum** of any contiguous subarray.

Implement the **linear-time** solution (Θ(n)). This is both a dynamic programming
and a greedy algorithm — at each step you make the locally optimal choice.

## Signature

```python
def mss_kadane(A):
    # A: list of integers (at least one element)
    # returns: int — the largest subarray sum
    ...
```

## Example

    A = [3, -5, 10, 2, -3, 1, 4, -8, 7, -6, -1]
    Answer: 14   (subarray [10, 2, -3, 1, 4])

## Algorithm — DP Formulation Θ(n)

Define `B[i]` = maximum sum of a subarray **ending** at index `i`:

    B[i] = max(A[i], B[i-1] + A[i])

Greedy choice: either start a new subarray at `i`, or extend the previous one —
whichever gives a larger sum.

The answer is `max(B[0], ..., B[n-1])`. We do not need to store all of `B`:

```
tmp = mss = A[0]
for x in A[1:]:
    tmp = max(x, tmp + x)
    mss = max(mss, tmp)
return mss
```

## Complexity

- **All cases:** Θ(n) — single pass, O(1) extra space.

## Notes

- This is the fastest possible solution; Θ(n) is a lower bound (must read all elements).
- The DP table `B` was described in the lecture with a right-to-left scan; the
  left-to-right version (above) is equivalent.
- Compare with `mss_brute` (Θ(n²)) and `mss_dc` (Θ(n log n)).
"""

STARTER = '''\
def mss_kadane(A):
    """Return the maximum subarray sum using Kadane's algorithm O(n)."""
    tmp = mss = A[0]
    for x in A[1:]:
        # extend or restart?
        pass
    return mss
'''

HINTS = [
    "At each element x: `tmp = max(x, tmp + x)`. This is the greedy choice: extend the running subarray, or restart.",
    "After updating tmp, update mss = max(mss, tmp).",
    "That's it — two lines inside the loop. Return mss.",
]


def reference(A):
    tmp = mss = A[0]
    for x in A[1:]:
        tmp = max(x, tmp + x)
        mss = max(mss, tmp)
    return mss


def tests(student):
    def case_example():
        assert student([3, -5, 10, 2, -3, 1, 4, -8, 7, -6, -1]) == 14

    def case_all_positive():
        assert student([1, 2, 3, 4, 5]) == 15

    def case_all_negative():
        assert student([-2, -3, -1]) == -1

    def case_single():
        assert student([42]) == 42

    def case_single_negative():
        assert student([-7]) == -7

    def case_two():
        assert student([2, -1]) == 2
        assert student([-1, 2]) == 2
        assert student([-3, -5]) == -3

    def case_restart():
        # best to restart at 10
        assert student([-100, 10, -1]) == 10

    def case_extend():
        # best to extend: 5 + (-1) + 5 = 9
        assert student([5, -1, 5]) == 9

    def case_lecure_b_array():
        # From lecture: B = [3,9,14,4,2,5,4,-1,7,-6,-1]  → max = 14
        A = [3, -5, 10, 2, -3, 1, 4, -8, 7, -6, -1]
        assert student(A) == 14

    def case_large_negative_middle():
        assert student([4, 3, -1000, 4, 3]) == 7

    return [
        ("example → 14", case_example),
        ("all positive → total sum", case_all_positive),
        ("all negative → max element", case_all_negative),
        ("single positive", case_single),
        ("single negative", case_single_negative),
        ("two elements", case_two),
        ("restart beats extending [-100,10,-1]", case_restart),
        ("extending beats restart [5,-1,5]", case_extend),
        ("lecture B-array example", case_lecure_b_array),
        ("restart after large negative", case_large_negative_middle),
    ]

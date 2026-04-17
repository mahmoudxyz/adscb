META = {
    "id": "ch10/01_mss_brute_force",
    "title": "Maximum Sum Subarray — Brute Force",
    "chapter": 10,
    "chapter_title": "Chapter 10 — Algorithmic Techniques",
    "difficulty": 1,
    "requires_recursion": False,
    "entry": "mss_brute",
}

DESCRIPTION = """
# Maximum Sum Subarray — Brute Force

Given an array of integers `A`, find the **maximum sum** of any contiguous subarray.

A contiguous subarray `A[i..j]` (i ≤ j) is a slice of `A`. You must pick at least
one element (the subarray cannot be empty).

## Signature

```python
def mss_brute(A):
    # A: list of integers (at least one element)
    # returns: int — the largest subarray sum
    ...
```

## Example

    A = [3, -5, 10, 2, -3, 1, 4, -8, 7, -6, -1]
    Answer: 14   (subarray [10, 2, -3, 1, 4])

    A = [-2, -3, -1]
    Answer: -1   (best single element)

## Algorithm — Brute Force Θ(n²)

Evaluate every possible subarray by iterating over all start positions `i`
and extending to the right:

```
mss = A[0]
for i = 0 .. n-1:
    tmp = 0
    for j = i .. n-1:
        tmp = tmp + A[j]
        mss = max(mss, tmp)
return mss
```

There are n(n+1)/2 subarrays — **Θ(n²)** in all cases.

## Complexity

- **Worst / average / best:** Θ(n²)

## Notes

- When all elements are negative the answer is the largest (least negative) element.
  The algorithm handles this correctly because `mss` is initialised to `A[0]`.
- This is the baseline; compare it to `mss_dc` (Θ(n log n)) and `mss_kadane` (Θ(n)).
"""

STARTER = '''\
def mss_brute(A):
    """Return the maximum subarray sum using brute force O(n²)."""
    mss = A[0]
    # your code here
    pass
'''

HINTS = [
    "Outer loop: for i in range(len(A)). Inner loop: for j in range(i, len(A)).",
    "Accumulate a running sum `tmp` in the inner loop. Reset tmp=0 at the start of each outer iteration.",
    "Update mss = max(mss, tmp) inside the inner loop. Return mss.",
]


def reference(A):
    mss = A[0]
    for i in range(len(A)):
        tmp = 0
        for j in range(i, len(A)):
            tmp += A[j]
            if tmp > mss:
                mss = tmp
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

    def case_negative_single():
        assert student([-7]) == -7

    def case_alternating():
        assert student([5, -1, 5]) == 9

    def case_prefix_best():
        assert student([10, -100, 1]) == 10

    def case_suffix_best():
        assert student([-100, 1, 10]) == 11

    def case_middle_best():
        assert student([-1, 4, 3, -10, 1]) == 7

    def case_two_elements():
        assert student([-1, 2]) == 2
        assert student([2, -1]) == 2

    return [
        ("example [3,-5,10,2,-3,1,4,-8,7,-6,-1] → 14", case_example),
        ("all positive → total sum", case_all_positive),
        ("all negative → max element", case_all_negative),
        ("single positive element", case_single),
        ("single negative element", case_negative_single),
        ("alternating [5,-1,5] → 9", case_alternating),
        ("best at prefix", case_prefix_best),
        ("best at suffix", case_suffix_best),
        ("best in middle", case_middle_best),
        ("two elements", case_two_elements),
    ]

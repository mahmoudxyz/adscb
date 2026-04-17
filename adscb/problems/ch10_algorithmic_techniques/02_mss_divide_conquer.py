META = {
    "id": "ch10/02_mss_divide_conquer",
    "title": "Maximum Sum Subarray — Divide & Conquer",
    "chapter": 10,
    "chapter_title": "Chapter 10 — Algorithmic Techniques",
    "difficulty": 2,
    "requires_recursion": True,
    "entry": "mss_dc",
}

DESCRIPTION = """
# Maximum Sum Subarray — Divide & Conquer

Given an array of integers `A`, find the **maximum sum** of any contiguous subarray.

Implement the **divide and conquer** solution. Unlike the brute force approach,
this version runs in **Θ(n log n)**.

## Signature

```python
def mss_dc(A):
    # A: list of integers (at least one element)
    # returns: int — the largest subarray sum
    ...
```

## Example

    A = [3, -5, 10, 2, -3, 1, 4, -8, 7, -6, -1]
    Answer: 14   (subarray [10, 2, -3, 1, 4])

## Algorithm — Divide & Conquer Θ(n log n)

Split `A[p..r]` at midpoint `q = (p+r)//2`. The maximum subarray is either:

1. Entirely in `A[p..q-1]` — recurse left
2. Entirely in `A[q+1..r]` — recurse right
3. **Crosses** `q` — extend from `A[q]` left and right in O(n)

```
function _rec(A, p, r):
    if p > r:  return -∞
    if p == r: return A[p]
    q = (p + r) // 2
    lmss = _rec(A, p, q - 1)
    rmss = _rec(A, q + 1, r)
    # extend left from q-1
    tmp = lext = 0
    for i from q-1 down to p:
        tmp += A[i]; lext = max(lext, tmp)
    # extend right from q+1
    tmp = rext = 0
    for i from q+1 to r:
        tmp += A[i]; rext = max(rext, tmp)
    return max(lmss, rmss, A[q] + lext + rext)
```

## Complexity

Recurrence: T(n) = 2T(n/2) + n → **Θ(n log n)** by Master Theorem (a=2, b=2, f(n)=n → case 2).

## Notes

- Base cases: empty range returns -∞, single element returns A[p].
- The crossing case always includes A[q] itself plus the best extension on each side.
- Implement a helper `_rec(A, p, r)` and call it with `(A, 0, len(A)-1)`.
"""

STARTER = '''\
def mss_dc(A):
    """Return the maximum subarray sum using divide & conquer O(n log n)."""
    def _rec(p, r):
        # base cases
        if p > r:
            return float('-inf')
        if p == r:
            return A[p]
        # divide
        q = (p + r) // 2
        # conquer
        lmss = _rec(p, q - 1)
        rmss = _rec(q + 1, r)
        # crossing subarray — extend left then right from q
        # your code here
        pass
    return _rec(0, len(A) - 1)
'''

HINTS = [
    "The crossing case: start at A[q] and expand leftward keeping a running sum + max, then do the same rightward.",
    "lext = max left extension (sum of best prefix going left from q-1). rext = same going right from q+1. Answer for crossing = A[q] + lext + rext.",
    "return max(lmss, rmss, A[q] + lext + rext). The two for loops each run at most n/2 steps — combined they give the O(n) combine step.",
]


def reference(A):
    def _rec(p, r):
        if p > r:
            return float('-inf')
        if p == r:
            return A[p]
        q = (p + r) // 2
        lmss = _rec(p, q - 1)
        rmss = _rec(q + 1, r)
        tmp = 0
        lext = 0
        for i in range(q - 1, p - 1, -1):
            tmp += A[i]
            if tmp > lext:
                lext = tmp
        tmp = 0
        rext = 0
        for i in range(q + 1, r + 1):
            tmp += A[i]
            if tmp > rext:
                rext = tmp
        return max(lmss, rmss, A[q] + lext + rext)

    return _rec(0, len(A) - 1)


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
        assert student([-1, 2]) == 2
        assert student([2, -1]) == 2
        assert student([-3, -5]) == -3

    def case_crossing_wins():
        # best subarray must cross the midpoint
        assert student([-1, 10, 10, -1]) == 20

    def case_left_wins():
        assert student([10, 5, -100, -2]) == 15

    def case_right_wins():
        assert student([-2, -100, 5, 10]) == 15

    def case_alternating():
        assert student([5, -1, 5]) == 9

    return [
        ("example [3,-5,10,2,-3,1,4,-8,7,-6,-1] → 14", case_example),
        ("all positive → total sum", case_all_positive),
        ("all negative → max element", case_all_negative),
        ("single positive", case_single),
        ("single negative", case_single_negative),
        ("two elements", case_two),
        ("crossing wins [-1,10,10,-1] → 20", case_crossing_wins),
        ("left subarray wins", case_left_wins),
        ("right subarray wins", case_right_wins),
        ("alternating [5,-1,5] → 9", case_alternating),
    ]

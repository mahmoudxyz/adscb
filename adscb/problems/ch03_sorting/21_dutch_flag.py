META = {
    "id": "ch03/21_dutch_flag",
    "title": "Dutch National Flag — 3-way partition",
    "chapter": 3,
    "chapter_title": "Chapter 3 — Sorting Algorithms",
    "difficulty": 2,
    "requires_recursion": False,
    "entry": "dutch_flag",
}

DESCRIPTION = """
# Dutch National Flag — 3-way partition

Given a list `A` containing only the integers `0`, `1`, and `2`, sort it
in place in a **single pass** (Θ(n), one traversal, O(1) extra space).

This problem is also known as the **Dutch National Flag** problem
(Edsger Dijkstra, 1976) — the three colors are the Dutch flag's red, white, blue.

It is a natural extension of QuickSort's partition: instead of two regions
(≤ pivot, > pivot), we maintain three regions (< pivot, = pivot, > pivot).

## Signature

```python
def dutch_flag(A):
    # A: plain Python list containing only 0s, 1s, and 2s — sort in place
    ...
```

## Example

    A = [2, 0, 2, 1, 1, 0]
    Result: [0, 0, 1, 1, 2, 2]

## Algorithm — 3-pointer single pass

Maintain three regions at all times:

    A[0..lo-1]  : all 0s   (less than pivot=1)
    A[lo..mid-1]: all 1s   (equal to pivot=1)
    A[mid..hi]  : unknown  (not yet processed)
    A[hi+1..n-1]: all 2s   (greater than pivot=1)

```
lo = 0; mid = 0; hi = n-1

while mid <= hi:
    if A[mid] == 0:
        swap(A, lo, mid); lo++; mid++
    elif A[mid] == 1:
        mid++
    else:  # A[mid] == 2
        swap(A, mid, hi); hi--
        # do NOT advance mid — A[mid] is now unknown
```

## Complexity

- Time: **Θ(n)** — single pass, each element examined at most once.
- Space: **O(1)** — three index variables only.

## Connection to QuickSort

This is the **3-way partition** that makes QuickSort efficient on arrays with
many duplicate keys (Θ(n) instead of Θ(n²) when all keys are equal).
"""

STARTER = '''\
def dutch_flag(A):
    """Sort A (containing only 0, 1, 2) in place using the 3-pointer technique."""
    lo, mid, hi = 0, 0, len(A) - 1
    # your code here
    pass
'''

HINTS = [
    "Three pointers: lo=0, mid=0, hi=len(A)-1. Loop while mid <= hi.",
    "If A[mid]==0: swap(lo,mid), lo+=1, mid+=1. If A[mid]==1: mid+=1. If A[mid]==2: swap(mid,hi), hi-=1 (don't advance mid).",
    "When you swap A[mid] with A[hi], the value at A[mid] is now unknown — you must inspect it again before advancing mid.",
]


def reference(A):
    lo, mid, hi = 0, 0, len(A) - 1
    while mid <= hi:
        if A[mid] == 0:
            A[lo], A[mid] = A[mid], A[lo]
            lo += 1
            mid += 1
        elif A[mid] == 1:
            mid += 1
        else:
            A[mid], A[hi] = A[hi], A[mid]
            hi -= 1


def tests(student):
    def _sort(values):
        A = list(values)
        student(A)
        return A

    def case_example():
        assert _sort([2, 0, 2, 1, 1, 0]) == [0, 0, 1, 1, 2, 2]

    def case_all_zeros():
        assert _sort([0, 0, 0]) == [0, 0, 0]

    def case_all_ones():
        assert _sort([1, 1, 1]) == [1, 1, 1]

    def case_all_twos():
        assert _sort([2, 2, 2]) == [2, 2, 2]

    def case_already_sorted():
        assert _sort([0, 0, 1, 1, 2, 2]) == [0, 0, 1, 1, 2, 2]

    def case_reverse_sorted():
        assert _sort([2, 2, 1, 1, 0, 0]) == [0, 0, 1, 1, 2, 2]

    def case_single():
        assert _sort([1]) == [1]

    def case_two_elements():
        assert _sort([2, 0]) == [0, 2]
        assert _sort([1, 0]) == [0, 1]
        assert _sort([2, 1]) == [1, 2]

    def case_no_ones():
        assert _sort([2, 0, 2, 0]) == [0, 0, 2, 2]

    def case_no_zeros():
        assert _sort([1, 2, 1, 2]) == [1, 1, 2, 2]

    def case_large():
        import random
        random.seed(7)
        vals = [random.choice([0, 1, 2]) for _ in range(30)]
        A = list(vals)
        student(A)
        assert A == sorted(vals), f"Mismatch on {vals}"

    return [
        ("example [2,0,2,1,1,0]", case_example),
        ("all zeros", case_all_zeros),
        ("all ones", case_all_ones),
        ("all twos", case_all_twos),
        ("already sorted", case_already_sorted),
        ("reverse sorted", case_reverse_sorted),
        ("single element", case_single),
        ("two elements (all pairs)", case_two_elements),
        ("no ones", case_no_ones),
        ("no zeros", case_no_zeros),
        ("random array of length 30", case_large),
    ]

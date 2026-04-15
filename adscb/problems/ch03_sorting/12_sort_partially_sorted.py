META = {
    "id": "ch03/12_sort_partially_sorted",
    "title": "Sort a partially sorted array",
    "chapter": 3,
    "chapter_title": "Chapter 3 — Sorting Algorithms",
    "difficulty": 2,
    "requires_recursion": True,
    "entry": "sort_partially_sorted",
}

DESCRIPTION = """
# Sort a partially sorted array  (Slide Exercise 4)

You are given a list `A` of `m + n` elements where:
- `A[0..m-1]` is **already sorted** (first `m` elements)
- `A[m..m+n-1]` is **unsorted** (last `n` elements)

Design an algorithm that is **better than plain MergeSort** for this input shape.

## Signature

```python
def sort_partially_sorted(A, m):
    # A: plain Python list — sort in place
    # m: number of already-sorted elements at the front (0 ≤ m ≤ len(A))
    ...
```

## Algorithm (from slide)

```
function newsort(A, m):
    n = len(A) - m
    mergesort(A, m, m+n-1)        ← sort the unsorted tail
    merge(A, 0, m-1, m+n-1)       ← merge sorted prefix with sorted tail
```

## Complexity

| n              | newsort cost  | Plain MergeSort          |
|----------------|---------------|--------------------------|
| O(1)           | Θ(m)          | Θ(m log m)               |
| O(log m)       | Θ(m)          | Θ(m log m)               |
| O(m)           | Θ(m log m)    | Θ(m log m)               |

Worst-case: `Θ(n log n + m)` — strictly better than `Θ((m+n) log(m+n))` when `n << m`.

## Example

    A = [1, 3, 5, 7, 4, 6, 2], m = 4
    Sorted prefix: [1, 3, 5, 7]
    Unsorted tail: [4, 6, 2]

    Sort tail: [2, 4, 6]
    Merge [1,3,5,7] with [2,4,6]: [1, 2, 3, 4, 5, 6, 7]

## Notes

- Edge case: if `m == 0`, the entire array is unsorted → just run MergeSort.
- Edge case: if `m == len(A)`, the array is fully sorted → do nothing.
- The merge step assumes `m > 0` and `m < len(A)`.
"""

STARTER = '''\
def sort_partially_sorted(A, m):
    """Sort A in place. A[0..m-1] is already sorted; A[m:] is unsorted."""
    n = len(A) - m
    if n == 0:
        return  # already fully sorted
    # Step 1: sort the unsorted tail A[m..len(A)-1]
    # Step 2: merge the sorted prefix with the sorted tail
    pass
'''

HINTS = [
    "Sort the tail A[m:] with MergeSort: _mergesort(A, m, len(A)-1).",
    "Then merge the two sorted halves: _merge(A, 0, m-1, len(A)-1). This requires m > 0.",
    "Handle edge cases: m=0 (just sort all), m=len(A) (already done). Both are handled if you check n=0.",
]


def reference(A, m):
    def _merge(A, p, q, r):
        B = [0] * (r - p + 1)
        i, j, k = p, q + 1, 0
        while i <= q and j <= r:
            if A[i] <= A[j]:
                B[k] = A[i]; i += 1
            else:
                B[k] = A[j]; j += 1
            k += 1
        while i <= q:
            B[k] = A[i]; k += 1; i += 1
        while j <= r:
            B[k] = A[j]; k += 1; j += 1
        for k in range(r - p + 1):
            A[p + k] = B[k]

    def _mergesort(A, p, r):
        if p < r:
            q = p + (r - p) // 2
            _mergesort(A, p, q)
            _mergesort(A, q + 1, r)
            _merge(A, p, q, r)

    n = len(A) - m
    if n == 0:
        return
    if m == 0:
        _mergesort(A, 0, len(A) - 1)
        return
    _mergesort(A, m, len(A) - 1)
    _merge(A, 0, m - 1, len(A) - 1)


def tests(student):
    def _sort(values, m):
        A = list(values)
        student(A, m)
        return A

    def case_basic():
        assert _sort([1, 3, 5, 7, 4, 6, 2], 4) == [1, 2, 3, 4, 5, 6, 7]

    def case_m_zero():
        # Entire array is unsorted — must still sort correctly
        assert _sort([5, 3, 1, 4, 2], 0) == [1, 2, 3, 4, 5]

    def case_m_equals_n():
        # Entire array is sorted — do nothing
        assert _sort([1, 2, 3, 4, 5], 5) == [1, 2, 3, 4, 5]

    def case_n_equals_1():
        # One unsorted element — just merge it in
        assert _sort([2, 4, 6, 8, 1], 4) == [1, 2, 4, 6, 8]

    def case_prefix_dominates():
        # Sorted prefix is large, small unsorted tail
        assert _sort([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 0], 10) == list(range(11))

    def case_tail_dominates():
        # Small sorted prefix, large unsorted tail
        assert _sort([1, 5, 3, 2, 4], 1) == [1, 2, 3, 4, 5]

    def case_interleaved_values():
        assert _sort([1, 3, 5, 2, 4, 6], 3) == [1, 2, 3, 4, 5, 6]

    def case_duplicates():
        assert _sort([1, 2, 2, 4, 3, 2, 5], 4) == [1, 2, 2, 2, 3, 4, 5]

    def case_single_element():
        assert _sort([7], 1) == [7]
        assert _sort([7], 0) == [7]

    return [
        ("basic [1,3,5,7 | 4,6,2]", case_basic),
        ("m=0 (fully unsorted)", case_m_zero),
        ("m=len(A) (fully sorted)", case_m_equals_n),
        ("n=1 (one unsorted element)", case_n_equals_1),
        ("large prefix, small tail", case_prefix_dominates),
        ("small prefix, large tail", case_tail_dominates),
        ("interleaved values", case_interleaved_values),
        ("duplicates across boundary", case_duplicates),
        ("single element", case_single_element),
    ]

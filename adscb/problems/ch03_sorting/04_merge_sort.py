META = {
    "id": "ch03/04_merge_sort",
    "title": "MergeSort",
    "chapter": 3,
    "chapter_title": "Chapter 3 — Sorting Algorithms",
    "difficulty": 2,
    "requires_recursion": True,
    "entry": "merge_sort",
}

DESCRIPTION = """
# MergeSort (John von Neumann, 1945)

Sort a list `A` in place using **MergeSort** (divide et impera).

Three steps at each level of recursion:
1. **Divide:** split `A[p..r]` into halves at `q = p + (r-p)//2`.
2. **Conquer:** recursively sort `A[p..q]` and `A[q+1..r]`.
3. **Combine:** merge the two sorted halves.

## Signature

```python
def merge_sort(A):
    # A is a plain Python list — sort in place
    ...
```

## Pseudocode (recursive helper)

```
function mergesort(A, p, r):
    if p < r:
        q = p + (r-p)//2
        mergesort(A, p, q)
        mergesort(A, q+1, r)
        merge(A, p, q, r)

First call: mergesort(A, 0, len(A)-1)
```

## Complexity

| Case    | Time       | Note                           |
|---------|------------|--------------------------------|
| Best    | Θ(n log n) | Data-independent               |
| Average | Θ(n log n) |                                |
| Worst   | Θ(n log n) |                                |

Recurrence: `T(n) = 2T(n/2) + Θ(n)` → by Master Theorem: `Θ(n log n)`.

## Properties

- **In place:** No (merge needs a temporary buffer)
- **Stable:** Yes (use `≤` in merge comparison)

## Notes

- Use `p + (r-p)//2` instead of `(p+r)//2` to avoid integer overflow
  (good habit even though Python integers are unbounded).
- You will need a helper `merge(A, p, q, r)` — implement it or import it.
"""

STARTER = '''\
def merge_sort(A):
    """Sort list A in place using MergeSort."""
    _mergesort(A, 0, len(A) - 1)


def _mergesort(A, p, r):
    # your recursive logic here
    pass


def _merge(A, p, q, r):
    # your merge logic here
    pass
'''

HINTS = [
    "Base case: if p >= r, do nothing (sub-array of length 0 or 1 is already sorted).",
    "Compute q = p + (r-p)//2. Recurse on (A, p, q) and (A, q+1, r). Then call merge.",
    "Merge: allocate B of size r-p+1. Two pointers i=p (left), j=q+1 (right). Pick smaller, drain leftovers, copy back.",
]


def reference(A):
    def _merge(A, p, q, r):
        B = [0] * (r - p + 1)
        i, j, k = p, q + 1, 0
        while i <= q and j <= r:
            if A[i] <= A[j]:
                B[k] = A[i]
                i += 1
            else:
                B[k] = A[j]
                j += 1
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

    _mergesort(A, 0, len(A) - 1)


def tests(student):
    def _sort(values):
        A = list(values)
        student(A)
        return A

    def case_empty():
        A = []
        student(A)
        assert A == []

    def case_single():
        assert _sort([7]) == [7]

    def case_two_elements():
        assert _sort([2, 1]) == [1, 2]

    def case_already_sorted():
        assert _sort([1, 2, 3, 4, 5, 6]) == [1, 2, 3, 4, 5, 6]

    def case_reverse():
        assert _sort([6, 5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5, 6]

    def case_slide_example():
        assert _sort([7, 2, 5, 7, 4, 1]) == [1, 2, 4, 5, 7, 7]

    def case_duplicates():
        assert _sort([3, 1, 4, 1, 5, 9, 2, 6, 5]) == [1, 1, 2, 3, 4, 5, 5, 6, 9]

    def case_negatives():
        assert _sort([-5, 3, -1, 0, 2, -8]) == [-8, -5, -1, 0, 2, 3]

    def case_odd_length():
        assert _sort([4, 2, 7, 1, 9]) == [1, 2, 4, 7, 9]

    def case_stable():
        A = [(3, 0), (1, 1), (3, 2), (2, 3)]
        student(A)
        keys = [x[0] for x in A]
        assert keys == [1, 2, 3, 3]
        threes = [x[1] for x in A if x[0] == 3]
        assert threes == [0, 2], f"Stability violated: {threes}"

    return [
        ("empty list", case_empty),
        ("single element", case_single),
        ("two elements", case_two_elements),
        ("already sorted", case_already_sorted),
        ("reverse sorted", case_reverse),
        ("slide example [7,2,5,7,4,1]", case_slide_example),
        ("duplicates", case_duplicates),
        ("negatives", case_negatives),
        ("odd length", case_odd_length),
        ("stability check", case_stable),
    ]

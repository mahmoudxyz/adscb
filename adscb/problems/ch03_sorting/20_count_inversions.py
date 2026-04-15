META = {
    "id": "ch03/20_count_inversions",
    "title": "Count inversions via MergeSort",
    "chapter": 3,
    "chapter_title": "Chapter 3 — Sorting Algorithms",
    "difficulty": 3,
    "requires_recursion": True,
    "entry": "count_inversions",
}

DESCRIPTION = """
# Count inversions via MergeSort

An **inversion** in a list `A` is a pair of indices `(i, j)` such that
`i < j` but `A[i] > A[j]` — i.e., a pair that is "out of order".

Count the total number of inversions in `A`.

## Signature

```python
def count_inversions(A):
    # A: plain Python list (not modified)
    # returns: int — number of inversions
    ...
```

## Examples

    A = [2, 4, 1, 3, 5]
    Inversions: (2,1), (4,1), (4,3) → answer = 3

    A = [1, 2, 3, 4, 5]  → 0  (already sorted)
    A = [5, 4, 3, 2, 1]  → 10 (every pair is inverted: C(5,2) = 10)

## Key insight — O(n log n) via MergeSort

A brute-force O(n²) solution checks all pairs. But we can do better by
**counting inversions during the merge step** of MergeSort:

When merging left half `L` and right half `R`, if we pick an element from `R`
(because `R[j] < L[i]`), then **all remaining elements in `L[i:]` form
inversions with `R[j]`** — because they are all larger and all come before
`R[j]` in the original array.

So: whenever we take from `R`, add `(mid - i + 1)` to the count, where `mid`
is the length of what remains in `L`.

## Algorithm sketch

```
function merge_count(A, p, r):
    if p >= r: return 0
    q = p + (r-p)//2
    inv  = merge_count(A, p, q)
    inv += merge_count(A, q+1, r)
    inv += merge_and_count(A, p, q, r)
    return inv
```

## Complexity

Same as MergeSort: **Θ(n log n)**.

## Notes

- This is a classic "MergeSort extension" problem — shows how divide et impera
  can solve more than just sorting.
- Brute force O(n²) is easy but will not pass on large inputs conceptually;
  aim for the merge-based O(n log n) solution.
"""

STARTER = '''\
def count_inversions(A):
    """Count the number of inversions in A in O(n log n) time."""
    A = list(A)  # work on a copy
    return _merge_count(A, 0, len(A) - 1)


def _merge_count(A, p, r):
    # your recursive logic here
    pass


def _merge_and_count(A, p, q, r):
    # merge A[p..q] and A[q+1..r], return number of inversions found
    pass
'''

HINTS = [
    "Base case: if p >= r, return 0. Compute q = p + (r-p)//2. Recurse on both halves, sum counts.",
    "In merge_and_count: whenever you pick from the right half (A[j] < A[i]), add (q - i + 1) inversions — all remaining left elements are larger.",
    "After the main while loop, drain remaining left elements (they don't create new inversions with an already-exhausted right half). Copy buffer back as usual.",
]


def reference(A):
    A = list(A)

    def _merge_and_count(A, p, q, r):
        B = [0] * (r - p + 1)
        i, j, k = p, q + 1, 0
        inv = 0
        while i <= q and j <= r:
            if A[i] <= A[j]:
                B[k] = A[i]; i += 1
            else:
                B[k] = A[j]
                inv += q - i + 1  # all remaining left elements are > A[j]
                j += 1
            k += 1
        while i <= q:
            B[k] = A[i]; k += 1; i += 1
        while j <= r:
            B[k] = A[j]; k += 1; j += 1
        for k in range(r - p + 1):
            A[p + k] = B[k]
        return inv

    def _merge_count(A, p, r):
        if p >= r:
            return 0
        q = p + (r - p) // 2
        inv = _merge_count(A, p, q)
        inv += _merge_count(A, q + 1, r)
        inv += _merge_and_count(A, p, q, r)
        return inv

    return _merge_count(A, 0, len(A) - 1)


def tests(student):
    def case_no_inversions():
        assert student([1, 2, 3, 4, 5]) == 0

    def case_all_inversions():
        # [5,4,3,2,1]: C(5,2) = 10 inversions
        assert student([5, 4, 3, 2, 1]) == 10

    def case_basic():
        assert student([2, 4, 1, 3, 5]) == 3

    def case_single():
        assert student([7]) == 0

    def case_two_sorted():
        assert student([1, 2]) == 0

    def case_two_reversed():
        assert student([2, 1]) == 1

    def case_duplicates():
        # Equal elements don't form inversions (i < j and A[i] > A[j], strict >)
        assert student([2, 2, 2]) == 0

    def case_partial():
        assert student([1, 3, 2, 4]) == 1

    def case_larger():
        # Brute-force verify
        A = [6, 5, 4, 3, 2, 1]
        expected = sum(1 for i in range(len(A)) for j in range(i+1, len(A)) if A[i] > A[j])
        assert student(A) == expected

    def case_does_not_modify():
        A = [3, 1, 2]
        original = list(A)
        student(A)
        assert A == original, "count_inversions must not modify the input list"

    return [
        ("already sorted → 0", case_no_inversions),
        ("reverse sorted [5,4,3,2,1] → 10", case_all_inversions),
        ("[2,4,1,3,5] → 3", case_basic),
        ("single element → 0", case_single),
        ("two sorted → 0", case_two_sorted),
        ("two reversed → 1", case_two_reversed),
        ("duplicates — no inversions", case_duplicates),
        ("[1,3,2,4] → 1", case_partial),
        ("[6,5,4,3,2,1] — verify against brute force", case_larger),
        ("input not modified", case_does_not_modify),
    ]

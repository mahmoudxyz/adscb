META = {
    "id": "ch03/11_quick_select",
    "title": "QuickSelect — k-th smallest element",
    "chapter": 3,
    "chapter_title": "Chapter 3 — Sorting Algorithms",
    "difficulty": 2,
    "requires_recursion": True,
    "entry": "quick_select",
}

DESCRIPTION = """
# QuickSelect — k-th smallest element  (Slide Exercise 5)

Given an unsorted list `A[0..n-1]` and an integer `k` (`1 ≤ k ≤ n`),
return the **k-th smallest** element (i.e. the element that would be at
index `k-1` in the sorted array).

## Signature

```python
def quick_select(A, k):
    # A: plain Python list (not modified... or may be)
    # k: 1-indexed rank (1 = smallest, n = largest)
    # returns the k-th smallest value
    ...
```

## Examples

    A = [6, 1, 2, 3, 1, 4], k = 3
    Sorted: [1, 1, 2, 3, 4, 6]
    Answer: 2  (3rd smallest)

    A = [7, 2, 5, 9, 1, 4], k = 1 → 1
    A = [7, 2, 5, 9, 1, 4], k = 6 → 9

## Algorithm (QuickSelect — from slide)

Like QuickSort, but recurse on **only one side**:

```
function quickselect(A, k, p, r):
    q = partition(A, p, r)
    if q == k-1:
        return A[q]        ← pivot landed exactly at rank k
    elif q < k-1:
        return quickselect(A, k, q+1, r)   ← k-th is in right half
    else:
        return quickselect(A, k, p, q-1)   ← k-th is in left half

First call: quickselect(A, k, 0, len(A)-1)
```

## Complexity

| Case    | Time   | Condition                     |
|---------|--------|-------------------------------|
| Best    | Θ(n)   | Pivot always lands at rank k  |
| Average | Θ(n)   | All partitions equally likely |
| Worst   | Θ(n²)  | Always maximally unbalanced   |

Average case derivation (from slide):
`T(n) = T(n-1) + 2` → `T(n) = Θ(n)`.

## Notes

- Only **one** recursive call per level (unlike QuickSort's two).
- It is OK if `A` gets partially rearranged — the tests check the return value.
"""

STARTER = '''\
def quick_select(A, k):
    """Return the k-th smallest element of A (1-indexed, k=1 is minimum)."""
    A = list(A)  # work on a copy to avoid modifying caller's list
    return _quickselect(A, k, 0, len(A) - 1)


def _quickselect(A, k, p, r):
    # your recursive logic here
    pass


def _partition(A, p, r):
    # your partition logic here
    pass
'''

HINTS = [
    "Base case: if p == r, return A[p]. Otherwise, q = partition(A, p, r).",
    "If q == k-1: found it, return A[q]. If q < k-1: recurse right (q+1, r). Else: recurse left (p, q-1).",
    "Use the same partition as QuickSort: pivot=A[r], i=p-1, scan j from p to r-1.",
]


def reference(A, k):
    A = list(A)

    def _partition(A, p, r):
        x = A[r]
        i = p - 1
        for j in range(p, r):
            if A[j] <= x:
                A[i + 1], A[j] = A[j], A[i + 1]
                i += 1
        A[i + 1], A[r] = A[r], A[i + 1]
        return i + 1

    def _quickselect(A, k, p, r):
        if p == r:
            return A[p]
        q = _partition(A, p, r)
        if q == k - 1:
            return A[q]
        elif q < k - 1:
            return _quickselect(A, k, q + 1, r)
        else:
            return _quickselect(A, k, p, q - 1)

    return _quickselect(A, k, 0, len(A) - 1)


def tests(student):
    def case_slide_example():
        assert student([6, 1, 2, 3, 1, 4], 3) == 2

    def case_k_equals_1():
        assert student([7, 2, 5, 9, 1, 4], 1) == 1

    def case_k_equals_n():
        assert student([7, 2, 5, 9, 1, 4], 6) == 9

    def case_median():
        assert student([3, 1, 4, 1, 5, 9, 2], 4) == 3

    def case_single_element():
        assert student([42], 1) == 42

    def case_duplicates():
        # A = [1,1,2,3,4,4,5]
        assert student([4, 1, 4, 2, 3, 5, 1], 2) == 1
        assert student([4, 1, 4, 2, 3, 5, 1], 6) == 4

    def case_already_sorted():
        assert student([1, 2, 3, 4, 5], 3) == 3

    def case_reverse_sorted():
        assert student([5, 4, 3, 2, 1], 2) == 2

    def case_all_equal():
        assert student([7, 7, 7, 7], 3) == 7

    def case_does_not_modify_original():
        A = [3, 1, 4, 1, 5, 9]
        original = list(A)
        student(A, 2)
        # If the student works on a copy, A should be unchanged.
        # If they modify in-place, that's also fine — we just check return value.
        # (The test above already checked correctness; this is a bonus note.)
        assert True  # We don't enforce immutability — just documenting intent.

    return [
        ("slide example [6,1,2,3,1,4] k=3 → 2", case_slide_example),
        ("k=1 → minimum", case_k_equals_1),
        ("k=n → maximum", case_k_equals_n),
        ("median of 7 elements", case_median),
        ("single element", case_single_element),
        ("duplicates — k=2 and k=6", case_duplicates),
        ("already sorted", case_already_sorted),
        ("reverse sorted", case_reverse_sorted),
        ("all equal", case_all_equal),
        ("return value is correct", case_does_not_modify_original),
    ]

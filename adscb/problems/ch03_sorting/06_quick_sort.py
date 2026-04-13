META = {
    "id": "ch03/06_quick_sort",
    "title": "QuickSort",
    "chapter": 3,
    "chapter_title": "Chapter 3 — Sorting Algorithms",
    "difficulty": 2,
    "requires_recursion": True,
    "entry": "quick_sort",
}

DESCRIPTION = """
# QuickSort (Tony Hoare, 1959)

Sort a list `A` in place using **QuickSort** (divide et impera).

Three steps at each level of recursion:
1. **Divide:** call `partition(A, p, r)` — picks `A[r]` as pivot, returns its
   final index `q`. After partition: all `A[p..q-1] ≤ A[q]` and all `A[q+1..r] > A[q]`.
2. **Conquer:** recursively sort `A[p..q-1]` and `A[q+1..r]`.
3. **Combine:** nothing — the array is already sorted after the two recursive calls.

## Signature

```python
def quick_sort(A):
    # A is a plain Python list — sort in place
    ...
```

## Pseudocode (from slide)

```
function quicksort(A, p, r):
    if p < r:
        q = partition(A, p, r)
        quicksort(A, p, q-1)
        quicksort(A, q+1, r)

function partition(A, p, r):
    x = A[r]
    i = p - 1
    for j = p, ..., r-1:
        if A[j] ≤ x:
            swap(A, i+1, j); i++
    swap(A, i+1, r)
    return i + 1

First call: quicksort(A, 0, len(A)-1)
```

## Complexity

| Case    | Time       | Condition                          |
|---------|------------|------------------------------------|
| Best    | Θ(n log n) | Pivot always splits evenly         |
| Average | O(n log n) | All partitions equally likely      |
| Worst   | Θ(n²)      | Already sorted (pivot always min/max)|

## Properties

- **In place:** Yes
- **Stable:** No

## Notes

- Worst case happens on already-sorted input with last-element pivot.
- Randomized pivot (`rpartition`) fixes this on average.
"""

STARTER = '''\
def quick_sort(A):
    """Sort list A in place using QuickSort."""
    _quicksort(A, 0, len(A) - 1)


def _quicksort(A, p, r):
    # your recursive logic here
    pass


def _partition(A, p, r):
    # your partition logic here
    pass
'''

HINTS = [
    "Base case: if p >= r, return (sub-array of 0 or 1 element is sorted).",
    "Call q = partition(A, p, r). Then recurse on (A, p, q-1) and (A, q+1, r).",
    "Partition: x=A[r], i=p-1. For j in range(p,r): if A[j]<=x: swap(A,i+1,j); i+=1. Then swap(A,i+1,r); return i+1.",
]


def reference(A):
    def _partition(A, p, r):
        x = A[r]
        i = p - 1
        for j in range(p, r):
            if A[j] <= x:
                A[i + 1], A[j] = A[j], A[i + 1]
                i += 1
        A[i + 1], A[r] = A[r], A[i + 1]
        return i + 1

    def _quicksort(A, p, r):
        if p < r:
            q = _partition(A, p, r)
            _quicksort(A, p, q - 1)
            _quicksort(A, q + 1, r)

    _quicksort(A, 0, len(A) - 1)


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
        # This is the worst case for naive pivot — still must produce correct output
        assert _sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

    def case_reverse():
        assert _sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

    def case_slide_example():
        assert _sort([7, 2, 5, 9, 1, 4]) == [1, 2, 4, 5, 7, 9]

    def case_duplicates():
        assert _sort([3, 1, 4, 1, 5, 9, 2, 6, 5]) == [1, 1, 2, 3, 4, 5, 5, 6, 9]

    def case_negatives():
        assert _sort([-3, 5, -1, 0, 2, -7]) == [-7, -3, -1, 0, 2, 5]

    def case_all_equal():
        assert _sort([5, 5, 5, 5]) == [5, 5, 5, 5]

    def case_random():
        import random
        random.seed(42)
        for _ in range(5):
            vals = random.sample(range(100), 15)
            A = list(vals)
            student(A)
            assert A == sorted(vals), f"Failed on {vals}"

    return [
        ("empty list", case_empty),
        ("single element", case_single),
        ("two elements", case_two_elements),
        ("already sorted (worst case)", case_already_sorted),
        ("reverse sorted", case_reverse),
        ("slide example [7,2,5,9,1,4]", case_slide_example),
        ("duplicates", case_duplicates),
        ("negatives", case_negatives),
        ("all equal", case_all_equal),
        ("random arrays", case_random),
    ]

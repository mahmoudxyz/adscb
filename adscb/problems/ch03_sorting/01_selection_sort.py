META = {
    "id": "ch03/01_selection_sort",
    "title": "SelectionSort",
    "chapter": 3,
    "chapter_title": "Chapter 3 — Sorting Algorithms",
    "difficulty": 1,
    "requires_recursion": False,
    "entry": "selection_sort",
}

DESCRIPTION = """
# SelectionSort

Sort a list `A` in place using **SelectionSort**.

At each step `i = 0, ..., n-2`:
1. Find the position `m` of the **minimum** key in `A[i..n-1]`.
2. Swap `A[m]` with `A[i]`.

## Signature

```python
def selection_sort(A):
    # A is a plain Python list — sort in place
    # return value is ignored
    ...
```

## Example

    step 0: [7, 2, 5, 9, 1, 4]  → find min A[4]=1, swap with A[0] → [1, 2, 5, 9, 7, 4]
    step 1: [1, 2, 5, 9, 7, 4]  → min already at index 1 (A[1]=2)
    step 2: [1, 2, 5, 9, 7, 4]  → find min A[5]=4, swap with A[2] → [1, 2, 4, 9, 7, 5]
    ...
    final:  [1, 2, 4, 5, 7, 9]

## Complexity

| Case    | Time    |
|---------|---------|
| Best    | Θ(n²)   |
| Average | Θ(n²)   |
| Worst   | Θ(n²)   |

Both loops always execute fully — complexity is always quadratic.

## Properties

- **In place:** Yes
- **Stable:** No (long-distance swaps can reorder equal keys)
"""

STARTER = '''\
def selection_sort(A):
    """Sort list A in place using SelectionSort."""
    # your code here
    pass
'''

HINTS = [
    "Outer loop: for i in range(len(A)). At each step, find the minimum in A[i:].",
    "Inner loop (minindx): iterate j from i+1 to len(A)-1, track index of smallest seen.",
    "After finding m (index of minimum in A[i:]), swap A[i] and A[m], then advance i.",
]


def reference(A):
    def minindx(A, i):
        for j in range(i + 1, len(A)):
            if A[j] < A[i]:
                i = j
        return i

    for i in range(len(A)):
        m = minindx(A, i)
        A[i], A[m] = A[m], A[i]


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
        assert _sort([42]) == [42]

    def case_already_sorted():
        assert _sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

    def case_reverse():
        assert _sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

    def case_example_from_slide():
        assert _sort([7, 2, 5, 9, 1, 4]) == [1, 2, 4, 5, 7, 9]

    def case_duplicates():
        assert _sort([3, 1, 4, 1, 5, 9, 2, 6, 5]) == [1, 1, 2, 3, 4, 5, 5, 6, 9]

    def case_negatives():
        assert _sort([-3, 5, -1, 0, 2, -7]) == [-7, -3, -1, 0, 2, 5]

    def case_two_elements():
        assert _sort([2, 1]) == [1, 2]

    return [
        ("empty list", case_empty),
        ("single element", case_single),
        ("already sorted", case_already_sorted),
        ("reverse sorted", case_reverse),
        ("slide example [7,2,5,9,1,4]", case_example_from_slide),
        ("duplicates", case_duplicates),
        ("negatives", case_negatives),
        ("two elements", case_two_elements),
    ]

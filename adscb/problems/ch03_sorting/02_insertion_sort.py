META = {
    "id": "ch03/02_insertion_sort",
    "title": "InsertionSort",
    "chapter": 3,
    "chapter_title": "Chapter 3 — Sorting Algorithms",
    "difficulty": 1,
    "requires_recursion": False,
    "entry": "insertion_sort",
}

DESCRIPTION = """
# InsertionSort (John Mauchly, 1946)

Sort a list `A` in place using **InsertionSort**.

At each step `i = 1, ..., n-1`:
1. `A[0..i-1]` is already sorted.
2. Insert `A[i]` into its correct position by bubbling it left while it is
   smaller than its left neighbour.

Intuition: same as sorting playing cards in your hand.

## Signature

```python
def insertion_sort(A):
    # A is a plain Python list — sort in place
    ...
```

## Example

    step 1: [7, 2, 5, 7, 4, 1]  → insert 2: swap(1,0) → [2, 7, 5, 7, 4, 1]
    step 2: [2, 7, 5, 7, 4, 1]  → insert 5: swap(2,1) → [2, 5, 7, 7, 4, 1]
    ...
    final:  [1, 2, 4, 5, 7, 7]

## Complexity

| Case    | Time  | Condition                  |
|---------|-------|----------------------------|
| Best    | Θ(n)  | Already sorted             |
| Average | Θ(n²) |                            |
| Worst   | Θ(n²) | Reverse sorted             |

**Nearly-sorted bonus:** if only `k = O(1)` elements are out of place → `Θ(n)`.

## Properties

- **In place:** Yes
- **Stable:** Yes (only swaps when `A[j] < A[j-1]`, equal keys never move)
"""

STARTER = '''\
def insertion_sort(A):
    """Sort list A in place using InsertionSort."""
    # your code here
    pass
'''

HINTS = [
    "Outer loop: for i in range(1, len(A)). Each iteration inserts A[i] into the sorted prefix A[0..i-1].",
    "Inner: j = i. While j > 0 and A[j] < A[j-1]: swap A[j] and A[j-1], then j -= 1.",
    "That's exactly two loops and one swap. Nothing else.",
]


def reference(A):
    n = len(A)
    for i in range(1, n):
        j = i
        while j > 0 and A[j] < A[j - 1]:
            A[j], A[j - 1] = A[j - 1], A[j]
            j -= 1


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
        # Best case — while loop never executes
        assert _sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

    def case_reverse():
        # Worst case — max swaps
        assert _sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

    def case_slide_example():
        assert _sort([7, 2, 5, 7, 4, 1]) == [1, 2, 4, 5, 7, 7]

    def case_duplicates():
        assert _sort([3, 1, 4, 1, 5, 9, 2, 6]) == [1, 1, 2, 3, 4, 5, 6, 9]

    def case_negatives():
        assert _sort([-3, 5, -1, 0, 2, -7]) == [-7, -3, -1, 0, 2, 5]

    def case_nearly_sorted():
        # Only A[0] is misplaced — should be very fast
        assert _sort([2, 1, 3, 4, 5, 6, 7]) == [1, 2, 3, 4, 5, 6, 7]

    def case_stable_equal_keys():
        # Equal keys must not swap — track via (value, original_index) pairs
        A = [(3, 0), (1, 1), (3, 2), (2, 3)]
        student(A)
        keys = [x[0] for x in A]
        assert keys == [1, 2, 3, 3], f"Wrong order: {keys}"
        # The two 3s must keep their original relative order
        threes = [x[1] for x in A if x[0] == 3]
        assert threes == [0, 2], f"Stable sort violated: 3s reordered to indices {threes}"

    return [
        ("empty list", case_empty),
        ("single element", case_single),
        ("already sorted (best case)", case_already_sorted),
        ("reverse sorted (worst case)", case_reverse),
        ("slide example [7,2,5,7,4,1]", case_slide_example),
        ("duplicates", case_duplicates),
        ("negatives", case_negatives),
        ("nearly sorted", case_nearly_sorted),
        ("stability check with equal keys", case_stable_equal_keys),
    ]

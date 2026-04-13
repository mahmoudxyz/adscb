META = {
    "id": "ch03/05_partition",
    "title": "QuickSort partition",
    "chapter": 3,
    "chapter_title": "Chapter 3 — Sorting Algorithms",
    "difficulty": 2,
    "requires_recursion": False,
    "entry": "partition",
}

DESCRIPTION = """
# QuickSort — Partition step

This is the **divide** step of QuickSort. Given `A[p..r]`, choose `A[r]` as
pivot and rearrange `A[p..r]` so that:

- All elements in `A[p..q-1]` are **≤ pivot**
- `A[q]` = pivot (in its final position)
- All elements in `A[q+1..r]` are **> pivot**

Return `q` (the pivot's final index).

## Signature

```python
def partition(A, p, r):
    # A: plain Python list (0-indexed)
    # rearranges A[p..r] around pivot A[r]
    # returns the final index of the pivot
    ...
```

## Pseudocode (from slide)

```
function partition(A, p, r):
    x = A[r]        ← pivot = last element
    i = p - 1
    for j = p, ..., r-1:
        if A[j] ≤ x:
            swap(A, i+1, j)
            i = i + 1
    swap(A, i+1, r) ← put pivot in final position
    return i + 1    ← pivot index
```

## Example (from slide)

    A = [7, 2, 5, 9, 1, 4]  pivot = 4
    i = -1

    j=0: A[0]=7 > 4  → no swap
    j=1: A[1]=2 ≤ 4  → swap(A,0,1) → [2,7,5,9,1,4], i=0
    j=2: A[2]=5 > 4  → no swap
    j=3: A[3]=9 > 4  → no swap
    j=4: A[4]=1 ≤ 4  → swap(A,1,4) → [2,1,5,9,7,4], i=1

    end: swap(A, i+1=2, r=5) → [2, 1, 4, 9, 7, 5]
    return 2

    Result: [2, 1, | 4 | 9, 7, 5]
             ≤ 4      pivot   > 4

## Notes

- Pivot is always `A[r]` (last element). This is the deterministic choice.
- Cost: Θ(r − p + 1) — every element in the sub-array is examined.
- In place: Yes. Stable: No (long-distance swaps).
"""

STARTER = '''\
def partition(A, p, r):
    """Partition A[p..r] around pivot A[r]. Returns pivot's final index."""
    # your code here
    pass
'''

HINTS = [
    "Set x = A[r] (pivot). Set i = p - 1. Loop j from p to r-1.",
    "If A[j] <= x: swap A[i+1] and A[j], then i += 1.",
    "After the loop: swap A[i+1] and A[r] (place pivot). Return i + 1.",
]


def reference(A, p, r):
    x = A[r]
    i = p - 1
    for j in range(p, r):
        if A[j] <= x:
            A[i + 1], A[j] = A[j], A[i + 1]
            i += 1
    A[i + 1], A[r] = A[r], A[i + 1]
    return i + 1


def tests(student):
    def _partition(values, p, r):
        A = list(values)
        q = student(A, p, r)
        return A, q

    def case_slide_example():
        A, q = _partition([7, 2, 5, 9, 1, 4], 0, 5)
        pivot = A[q]
        assert pivot == 4, f"Pivot should be 4, got {pivot}"
        assert all(A[i] <= pivot for i in range(q)), f"Left of pivot not all ≤: {A}"
        assert all(A[i] > pivot for i in range(q + 1, len(A))), f"Right of pivot not all >: {A}"

    def case_pivot_is_min():
        A, q = _partition([5, 3, 7, 1], 0, 3)
        assert A[q] == 1
        assert q == 0  # pivot goes to front
        assert all(A[i] > 1 for i in range(1, len(A)))

    def case_pivot_is_max():
        A, q = _partition([1, 3, 2, 7], 0, 3)
        assert A[q] == 7
        assert q == 3  # pivot stays at end
        assert all(A[i] <= 7 for i in range(3))

    def case_single_element():
        A, q = _partition([42], 0, 0)
        assert A == [42]
        assert q == 0

    def case_two_elements_swap():
        A, q = _partition([5, 2], 0, 1)
        assert A[q] == 2
        assert A == [2, 5] or (A[q] == 2 and all(x > 2 for x in A[q + 1:]))

    def case_all_equal():
        A, q = _partition([3, 3, 3, 3], 0, 3)
        assert A[q] == 3
        assert all(v == 3 for v in A)

    def case_subarray_only():
        # Partition only A[2..5], leave A[0] and A[1] untouched
        A = [99, 88, 4, 1, 3, 2]
        q = student(A, 2, 5)
        assert A[0] == 99 and A[1] == 88, "Untouched prefix was modified"
        pivot = A[q]
        assert pivot == 2
        assert all(A[i] <= pivot for i in range(2, q))
        assert all(A[i] > pivot for i in range(q + 1, 6))

    def case_invariant_check():
        import random
        random.seed(0)
        for _ in range(10):
            vals = random.sample(range(1, 50), 8)
            A = list(vals)
            q = student(A, 0, len(A) - 1)
            pivot = A[q]
            left_ok = all(A[i] <= pivot for i in range(q))
            right_ok = all(A[i] > pivot for i in range(q + 1, len(A)))
            assert left_ok and right_ok, \
                f"Partition invariant failed on {vals}: {A}, pivot at {q}={pivot}"

    return [
        ("slide example [7,2,5,9,1,4]", case_slide_example),
        ("pivot is minimum", case_pivot_is_min),
        ("pivot is maximum", case_pivot_is_max),
        ("single element", case_single_element),
        ("two elements", case_two_elements_swap),
        ("all equal keys", case_all_equal),
        ("subarray only — prefix untouched", case_subarray_only),
        ("invariant check on random arrays", case_invariant_check),
    ]

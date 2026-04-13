META = {
    "id": "ch03/03_merge",
    "title": "Merge two sorted halves",
    "chapter": 3,
    "chapter_title": "Chapter 3 — Sorting Algorithms",
    "difficulty": 2,
    "requires_recursion": False,
    "entry": "merge",
}

DESCRIPTION = """
# Merge two sorted halves

This is the **combine** step of MergeSort. Given a list `A` where the sub-array
`A[p..q]` is sorted and `A[q+1..r]` is sorted, merge them so that `A[p..r]`
is sorted. Modifies `A` in place using a temporary buffer.

## Signature

```python
def merge(A, p, q, r):
    # A: plain Python list (0-indexed)
    # A[p..q] is sorted, A[q+1..r] is sorted
    # after the call, A[p..r] is sorted
    ...
```

## Example

    A = [2, 5, 7, 1, 4, 7], p=0, q=2, r=5
    Left half:  A[0..2] = [2, 5, 7]
    Right half: A[3..5] = [1, 4, 7]

    Compare A[i] vs A[j] and fill buffer B:
      i=0,j=3: A[j]=1 < A[i]=2  → B[0]=1, j=4
      i=0,j=4: A[i]=2 < A[j]=4  → B[1]=2, i=1
      i=1,j=4: A[i]=5 > A[j]=4  → B[2]=4, j=5
      i=1,j=5: A[i]=5 ≤ A[j]=7  → B[3]=5, i=2
      i=2,j=5: A[i]=7 ≤ A[j]=7  → B[4]=7, i=3
      i>q, drain right:          → B[5]=7
    Copy B back: A[0..5] = [1, 2, 4, 5, 7, 7]

## Algorithm (from slide)

```
function merge(A, p, q, r):
    B = new array of size r-p+1
    i = p   (left pointer)
    j = q+1 (right pointer)
    k = 0   (buffer pointer)

    while i ≤ q and j ≤ r:
        if A[i] ≤ A[j]:  B[k]=A[i]; i++
        else:             B[k]=A[j]; j++
        k++

    drain remaining left:  while i ≤ q: B[k]=A[i]; k++; i++
    drain remaining right: while j ≤ r: B[k]=A[j]; k++; j++

    copy B back: for k=0,..,r-p: A[p+k] = B[k]
```

## Notes

- Use `≤` (not `<`) when comparing A[i] and A[j] — this makes the merge **stable**.
- Complexity: Θ(r − p + 1), linear in the sub-array size.
"""

STARTER = '''\
def merge(A, p, q, r):
    """Merge sorted A[p..q] and A[q+1..r] in place (0-indexed)."""
    # your code here
    pass
'''

HINTS = [
    "Allocate B = [0] * (r - p + 1). Set i=p, j=q+1, k=0. Compare A[i] vs A[j] in a while loop.",
    "After the main loop, drain the remaining half that still has elements (two extra while loops).",
    "Copy B back: for k in range(r - p + 1): A[p + k] = B[k]. Use <= (not <) for stability.",
]


def reference(A, p, q, r):
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
        B[k] = A[i]
        k += 1
        i += 1
    while j <= r:
        B[k] = A[j]
        k += 1
        j += 1
    for k in range(r - p + 1):
        A[p + k] = B[k]


def tests(student):
    def _merge(A, p, q, r):
        A = list(A)
        student(A, p, q, r)
        return A

    def case_slide_example():
        A = [2, 5, 7, 1, 4, 7]
        student(A, 0, 2, 5)
        assert A == [1, 2, 4, 5, 7, 7], f"got {A}"

    def case_left_all_smaller():
        A = [1, 2, 3, 4, 5, 6]
        student(A, 0, 2, 5)
        assert A == [1, 2, 3, 4, 5, 6]

    def case_right_all_smaller():
        A = [4, 5, 6, 1, 2, 3]
        student(A, 0, 2, 5)
        assert A == [1, 2, 3, 4, 5, 6]

    def case_single_element_each():
        A = [5, 2]
        student(A, 0, 0, 1)
        assert A == [2, 5]

    def case_duplicates():
        A = [1, 3, 5, 2, 3, 6]
        student(A, 0, 2, 5)
        assert A == [1, 2, 3, 3, 5, 6]

    def case_subarray_in_middle():
        # Only merge the middle portion; leave A[0] and A[6] untouched
        A = [99, 2, 5, 1, 4, 7, 99]
        student(A, 1, 2, 5)
        assert A == [99, 1, 2, 4, 5, 7, 99], f"got {A}"

    def case_stable_equal_keys():
        # Equal keys: left half's element must come first (stable)
        A = [(1, 'L'), (3, 'L'), (3, 'R'), (5, 'R')]
        # Both halves already sorted by first element
        student(A, 0, 1, 3)
        labels = [x[1] for x in A if x[0] == 3]
        assert labels == ['L', 'R'], f"Stability violated: {labels}"

    def case_unequal_lengths():
        A = [1, 6, 2, 3, 4, 5]  # left: [1,6], right: [2,3,4,5]
        student(A, 0, 1, 5)
        assert A == [1, 2, 3, 4, 5, 6]

    return [
        ("slide example", case_slide_example),
        ("left half all smaller", case_left_all_smaller),
        ("right half all smaller", case_right_all_smaller),
        ("single element each half", case_single_element_each),
        ("duplicates across halves", case_duplicates),
        ("subarray in middle (boundaries untouched)", case_subarray_in_middle),
        ("stability with equal keys", case_stable_equal_keys),
        ("unequal-length halves", case_unequal_lengths),
    ]

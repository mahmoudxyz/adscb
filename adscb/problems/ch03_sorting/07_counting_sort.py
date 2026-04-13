META = {
    "id": "ch03/07_counting_sort",
    "title": "CountingSort",
    "chapter": 3,
    "chapter_title": "Chapter 3 — Sorting Algorithms",
    "difficulty": 2,
    "requires_recursion": False,
    "entry": "counting_sort",
}

DESCRIPTION = """
# CountingSort (Harold H. Seward, 1954)

Sort a list `A` of **integers** in place using **CountingSort** — a
non-comparative linear-time sort.

**Assumption:** all values are integers (can be negative).

**Idea:**
1. Find the range `[a, b]` where `a = min(A)`, `b = max(A)`, `k = b - a + 1`.
2. Build count array `B[0..k-1]` recording how many times each value appears.
3. Re-arrange `A` by writing each value back the correct number of times.

## Signature

```python
def counting_sort(A):
    # A is a plain Python list of integers — sort in place
    ...
```

## Pseudocode (from slide)

```
function countingsort(A[1..n]):
    a = min(A); b = max(A); k = b - a + 1
    B[1..k] = [0, ..., 0]   ← count array

    for i = 1..n:
        B[A[i] - a + 1] += 1   ← count occurrences

    j = 1
    for i = 1..k:
        while B[i] > 0:
            A[j] = i + a - 1   ← write value back
            B[i] -= 1
            j += 1
```

## Example

    A = [4, 2, 2, 8, 3, 3, 1]
    a=1, b=8, k=8
    B = [1, 2, 2, 1, 0, 0, 0, 1]  (counts for values 1..8)
    Result: A = [1, 2, 2, 3, 3, 4, 8]

## Complexity

| Case    | Time     |
|---------|----------|
| Best    | Θ(n + k) |
| Average | Θ(n + k) |
| Worst   | Θ(n + k) |

Where `k = b - a + 1` (range of input values).
If `k = O(n)` → linear `Θ(n)`. If `k` is huge → dominated by `k`.

## Properties

- **In place:** No (needs count array of size `k`)
- **Stable:** This simple version is NOT stable (it uses re-write, not re-arrange).
  (A stable version tracks positions — see the slide's full version.)
"""

STARTER = '''\
def counting_sort(A):
    """Sort list A of integers in place using CountingSort."""
    if not A:
        return
    # your code here
    pass
'''

HINTS = [
    "Find a = min(A), b = max(A), k = b - a + 1. Allocate B = [0] * k.",
    "Count pass: for each x in A: B[x - a] += 1.",
    "Write-back: j = 0; for i in range(k): while B[i] > 0: A[j] = i + a; B[i] -= 1; j += 1.",
]


def reference(A):
    if not A:
        return
    a = min(A)
    b = max(A)
    k = b - a + 1
    B = [0] * k
    for x in A:
        B[x - a] += 1
    j = 0
    for i in range(k):
        while B[i] > 0:
            A[j] = i + a
            B[i] -= 1
            j += 1


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
        assert _sort([5]) == [5]

    def case_slide_example():
        assert _sort([4, 2, 2, 8, 3, 3, 1]) == [1, 2, 2, 3, 3, 4, 8]

    def case_all_same():
        assert _sort([7, 7, 7, 7]) == [7, 7, 7, 7]

    def case_negatives():
        assert _sort([-3, -1, -5, -2, -4]) == [-5, -4, -3, -2, -1]

    def case_mixed_sign():
        assert _sort([-2, 3, 0, -1, 2, 1]) == [-2, -1, 0, 1, 2, 3]

    def case_small_range():
        # k=2, many elements — purely Θ(n)
        assert _sort([1, 0, 1, 0, 1, 0, 0, 1]) == [0, 0, 0, 0, 1, 1, 1, 1]

    def case_already_sorted():
        assert _sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

    def case_reverse():
        assert _sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

    return [
        ("empty list", case_empty),
        ("single element", case_single),
        ("slide example [4,2,2,8,3,3,1]", case_slide_example),
        ("all same value", case_all_same),
        ("all negatives", case_negatives),
        ("mixed positive/negative", case_mixed_sign),
        ("small range k=2 (many duplicates)", case_small_range),
        ("already sorted", case_already_sorted),
        ("reverse sorted", case_reverse),
    ]

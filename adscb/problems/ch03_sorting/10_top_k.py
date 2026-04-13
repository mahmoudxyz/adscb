META = {
    "id": "ch03/10_top_k",
    "title": "Top-k largest elements",
    "chapter": 3,
    "chapter_title": "Chapter 3 — Sorting Algorithms",
    "difficulty": 2,
    "requires_recursion": False,
    "entry": "top_k",
}

DESCRIPTION = """
# Top-k largest elements  (Slide Exercise 2)

Given an unsorted list `A` of length `n` and an integer `k`, place the
**k largest values** into `A[0..k-1]` (in any order among themselves).
The remaining elements go into `A[k..n-1]` (any order).

Do this **without sorting the full array** — use a sequential selection
approach that runs in **O(n·k)** worst-case time.

## Signature

```python
def top_k(A, k):
    # A: plain Python list — modify in place
    # k: int, 1 ≤ k ≤ len(A)
    # return value is ignored
    ...
```

## Algorithm (from slide exercise)

```
function topk(A[1..n], k):
    for i = 1, ..., k:
        j = index of maximum in A[i..n]
        swap(A, i, j)
```

At the end, `A[0..k-1]` contains the k largest elements (unsorted).

## Example

    A = [3, 1, 4, 1, 5, 9, 2, 6], k = 3
    Step 1: max of A[0..7]=9 at index 5 → swap(0,5) → [9, 1, 4, 1, 5, 3, 2, 6]
    Step 2: max of A[1..7]=6 at index 7 → swap(1,7) → [9, 6, 4, 1, 5, 3, 2, 1]
    Step 3: max of A[2..7]=5 at index 4 → swap(2,4) → [9, 6, 5, 1, 4, 3, 2, 1]
    Result: A[0..2] = {9, 6, 5}  ✓ (the 3 largest)

## Complexity analysis (from slide)

| k          | top_k cost    | MergeSort      | Best choice  |
|------------|---------------|----------------|--------------|
| O(1)       | Θ(n)          | Θ(n log n)     | top_k        |
| Θ(log n)   | Θ(n log n)    | Θ(n log n)     | Either       |
| Θ(n)       | O(n²)         | Θ(n log n)     | MergeSort    |

## Notes

- The k elements in `A[0..k-1]` need not be sorted among themselves.
- The test checks: set of top-k values is correct, not their order.
"""

STARTER = '''\
def top_k(A, k):
    """Place the k largest values into A[0..k-1] (any order)."""
    # your code here
    pass
'''

HINTS = [
    "Outer loop: for i in range(k). At each step, find the index of the maximum in A[i:].",
    "maxindx: loop j from i+1 to len(A)-1, track index of largest seen so far.",
    "Swap A[i] with A[maxindx]. After k iterations, A[0..k-1] holds the k largest.",
]


def reference(A, k):
    def maxindx(A, i):
        m = i
        for j in range(i + 1, len(A)):
            if A[j] > A[m]:
                m = j
        return m

    for i in range(k):
        m = maxindx(A, i)
        A[i], A[m] = A[m], A[i]


def tests(student):
    def _topk(values, k):
        A = list(values)
        student(A, k)
        return A

    def _check(original, result, k):
        expected = sorted(original, reverse=True)[:k]
        got = sorted(result[:k], reverse=True)
        assert got == expected, \
            f"Top-{k} of {original}: expected {expected}, got {result[:k]}"

    def case_basic():
        A = [3, 1, 4, 1, 5, 9, 2, 6]
        result = _topk(A, 3)
        _check([3, 1, 4, 1, 5, 9, 2, 6], result, 3)

    def case_k_equals_1():
        A = [7, 3, 9, 1, 5]
        result = _topk(A, 1)
        assert result[0] == 9, f"Max should be 9, got {result[0]}"

    def case_k_equals_n():
        vals = [5, 3, 8, 1, 9, 2]
        result = _topk(vals, len(vals))
        _check(vals, result, len(vals))

    def case_duplicates():
        vals = [4, 4, 4, 1, 2, 3]
        result = _topk(vals, 3)
        _check(vals, result, 3)

    def case_already_sorted():
        vals = [1, 2, 3, 4, 5]
        result = _topk(vals, 2)
        _check(vals, result, 2)

    def case_reverse_sorted():
        vals = [5, 4, 3, 2, 1]
        result = _topk(vals, 3)
        _check(vals, result, 3)

    def case_all_same():
        vals = [7, 7, 7, 7]
        result = _topk(vals, 2)
        assert set(result[:2]) == {7}

    def case_negatives():
        vals = [-5, -1, -3, -2, -4]
        result = _topk(vals, 2)
        _check(vals, result, 2)

    return [
        ("basic [3,1,4,1,5,9,2,6] k=3", case_basic),
        ("k=1 → max only", case_k_equals_1),
        ("k=n → all elements", case_k_equals_n),
        ("duplicates", case_duplicates),
        ("already sorted", case_already_sorted),
        ("reverse sorted", case_reverse_sorted),
        ("all same value", case_all_same),
        ("all negatives", case_negatives),
    ]

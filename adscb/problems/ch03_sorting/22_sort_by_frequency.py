META = {
    "id": "ch03/22_sort_by_frequency",
    "title": "Sort by frequency",
    "chapter": 3,
    "chapter_title": "Chapter 3 — Sorting Algorithms",
    "difficulty": 2,
    "requires_recursion": False,
    "entry": "sort_by_frequency",
}

DESCRIPTION = """
# Sort by frequency

Given a list `A` of integers, return a **new list** with elements sorted by
their **frequency of occurrence** in descending order (most frequent first).

If two elements have the **same frequency**, sort them by value in
**ascending order** (smaller value comes first).

## Signature

```python
def sort_by_frequency(A):
    # A: plain Python list of integers
    # returns: a new list sorted by frequency desc, then by value asc
    ...
```

## Example

    A = [4, 1, 2, 2, 3, 1, 4, 4]
    Frequencies: {4: 3, 1: 2, 2: 2, 3: 1}
    Result: [4, 4, 4, 1, 1, 2, 2, 3]
             freq=3   freq=2    freq=1

    A = [5, 5, 4, 4, 3, 3]
    All freq=2 → sort by value asc: [3, 3, 4, 4, 5, 5]

## Algorithm

1. **Count** frequencies using a counting-sort style dictionary or array:
   `freq[x] += 1` for each `x` in `A`.
2. **Sort** the unique values by `(-freq[x], x)` — descending frequency,
   ascending value as tie-breaker.
3. **Reconstruct** the output: for each value `x` in sorted order, append `x`
   repeated `freq[x]` times.

## Complexity

Let `k` = number of distinct values.
- Counting: Θ(n)
- Sorting unique values: Θ(k log k)
- Reconstruction: Θ(n)
- **Total: Θ(n + k log k)**. If all values are distinct, k = n → Θ(n log n).

## Notes

- This uses a dictionary for counting (not a fixed-size array), which handles
  arbitrary integer values with no range assumption.
- The sort step uses Python's `sorted()` with a compound key — this is the
  "sort on transformed key" pattern, a cousin of RadixSort.
- Do **not** modify `A` — return a new list.
"""

STARTER = '''\
def sort_by_frequency(A):
    """Return new list sorted by frequency desc, then by value asc."""
    if not A:
        return []
    # Step 1: count frequencies
    # Step 2: sort unique values by (-freq, value)
    # Step 3: reconstruct output
    pass
'''

HINTS = [
    "Count with a dict: freq = {}; for x in A: freq[x] = freq.get(x, 0) + 1.",
    "Sort unique keys: keys = sorted(freq, key=lambda x: (-freq[x], x)).",
    "Reconstruct: result = []; for k in keys: result.extend([k] * freq[k]); return result.",
]


def reference(A):
    if not A:
        return []
    freq = {}
    for x in A:
        freq[x] = freq.get(x, 0) + 1
    keys = sorted(freq, key=lambda x: (-freq[x], x))
    result = []
    for k in keys:
        result.extend([k] * freq[k])
    return result


def tests(student):
    def case_basic():
        result = student([4, 1, 2, 2, 3, 1, 4, 4])
        assert result == [4, 4, 4, 1, 1, 2, 2, 3], f"got {result}"

    def case_all_same_frequency():
        result = student([5, 5, 4, 4, 3, 3])
        assert result == [3, 3, 4, 4, 5, 5], f"got {result}"

    def case_empty():
        assert student([]) == []

    def case_single():
        assert student([7]) == [7]

    def case_all_distinct():
        # All freq=1 → sorted by value asc
        result = student([3, 1, 4, 1, 5, 9, 2, 6])
        # freq: {3:1, 1:2, 4:1, 5:1, 9:1, 2:1, 6:1}
        # 1 appears twice → first; rest all freq=1 sorted by value
        assert result == [1, 1, 2, 3, 4, 5, 6, 9], f"got {result}"

    def case_one_dominant():
        result = student([2, 2, 2, 2, 1, 3])
        assert result == [2, 2, 2, 2, 1, 3], f"got {result}"

    def case_negatives():
        result = student([-1, -1, 2, 2, 0])
        # freq: {-1:2, 2:2, 0:1}. Tie on freq=2: -1 < 2, so -1 first
        assert result == [-1, -1, 2, 2, 0], f"got {result}"

    def case_returns_new_list():
        A = [1, 2, 1]
        result = student(A)
        assert result == [1, 1, 2]
        assert A == [1, 2, 1], "Must not modify the input list"

    def case_length_preserved():
        A = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
        result = student(A)
        assert len(result) == len(A), f"Length changed: {len(result)} vs {len(A)}"
        assert sorted(result) == sorted(A), "Elements changed"

    return [
        ("basic [4,1,2,2,3,1,4,4]", case_basic),
        ("all same frequency → sort by value", case_all_same_frequency),
        ("empty list", case_empty),
        ("single element", case_single),
        ("one dominant frequency", case_one_dominant),
        ("mixed frequencies [3,1,4,1,5,9,2,6]", case_all_distinct),
        ("negative values", case_negatives),
        ("returns new list, original unchanged", case_returns_new_list),
        ("length and elements preserved", case_length_preserved),
    ]

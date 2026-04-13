META = {
    "id": "ch03/08_radix_sort",
    "title": "RadixSort",
    "chapter": 3,
    "chapter_title": "Chapter 3 — Sorting Algorithms",
    "difficulty": 3,
    "requires_recursion": False,
    "entry": "radix_sort",
}

DESCRIPTION = """
# RadixSort (Harold H. Seward, 1954)

Sort a list `A` of **non-negative integers** in place using **RadixSort**.

**Key insight:** sort digit by digit, from **least significant** to **most
significant**, using a **stable** sort at each pass.

If you use an unstable sort per digit, RadixSort produces wrong results —
stability is essential.

## Signature

```python
def radix_sort(A):
    # A is a plain Python list of non-negative integers — sort in place
    ...
```

## Algorithm (from slide)

```
function radixsort(A[1..n]):
    d = number of digits in max element
    for i = 1, ..., d:
        stable-sort A by the i-th digit (from right, i.e. units first)
```

Use CountingSort (with k=10, one bucket per digit 0-9) as the per-digit
stable sort.

## Example

    A = [170, 45, 75, 90, 802, 24, 2, 66]

    Pass 1 (units):  [170, 90, 802, 2, 24, 45, 75, 66]
    Pass 2 (tens):   [802, 2, 24, 45, 66, 170, 75, 90]
    Pass 3 (hundreds): [2, 24, 45, 66, 75, 90, 170, 802]

## Complexity

Using CountingSort (k=10) per digit:
- Cost per pass: Θ(n + 10) = Θ(n)
- Total: Θ(d · n) where d = number of digits in the largest element

If `d = O(1)` → **Θ(n)** (linear).

## Properties

- **In place:** No
- **Stable:** Yes

## Notes

- Extracting the i-th digit from the right: `(x // 10**(i-1)) % 10`
  (or equivalently `(x // base) % 10` while incrementing base).
- The per-digit sort MUST be stable — use CountingSort on digit values 0-9.
"""

STARTER = '''\
def radix_sort(A):
    """Sort list A of non-negative integers in place using RadixSort."""
    if not A:
        return
    # your code here
    pass
'''

HINTS = [
    "Find d = number of digits in max(A). Loop over each digit position from least to most significant.",
    "For each digit position, extract digit = (x // 10**pos) % 10. Use a stable counting sort over digits 0-9.",
    "Stable counting sort on digits: count[0..9], compute prefix sums, fill output array back-to-front, copy back to A.",
]


def reference(A):
    if not A:
        return

    def _counting_sort_by_digit(A, exp):
        n = len(A)
        output = [0] * n
        count = [0] * 10
        for x in A:
            count[(x // exp) % 10] += 1
        for i in range(1, 10):
            count[i] += count[i - 1]
        for i in range(n - 1, -1, -1):
            d = (A[i] // exp) % 10
            count[d] -= 1
            output[count[d]] = A[i]
        for i in range(n):
            A[i] = output[i]

    max_val = max(A)
    exp = 1
    while max_val // exp > 0:
        _counting_sort_by_digit(A, exp)
        exp *= 10


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

    def case_textbook_example():
        assert _sort([170, 45, 75, 90, 802, 24, 2, 66]) == [2, 24, 45, 66, 75, 90, 170, 802]

    def case_single_digit():
        assert _sort([9, 3, 7, 1, 8, 2]) == [1, 2, 3, 7, 8, 9]

    def case_two_digit():
        assert _sort([64, 25, 12, 22, 11]) == [11, 12, 22, 25, 64]

    def case_all_same():
        assert _sort([77, 77, 77]) == [77, 77, 77]

    def case_zeros():
        assert _sort([0, 5, 0, 3, 0]) == [0, 0, 0, 3, 5]

    def case_varying_lengths():
        # Mix of 1-, 2-, and 3-digit numbers
        assert _sort([1, 200, 30, 4, 100, 20]) == [1, 4, 20, 30, 100, 200]

    def case_already_sorted():
        assert _sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

    def case_reverse():
        assert _sort([99, 88, 77, 66, 55]) == [55, 66, 77, 88, 99]

    return [
        ("empty list", case_empty),
        ("single element", case_single),
        ("textbook example [170,45,75,90,802,24,2,66]", case_textbook_example),
        ("single-digit numbers", case_single_digit),
        ("two-digit numbers", case_two_digit),
        ("all same", case_all_same),
        ("contains zeros", case_zeros),
        ("varying number of digits", case_varying_lengths),
        ("already sorted", case_already_sorted),
        ("reverse sorted", case_reverse),
    ]

META = {
    "id": "ch10/20_fibonacci_dp",
    "title": "Fibonacci — Bottom-Up DP",
    "chapter": 10,
    "chapter_title": "Chapter 10 — Algorithmic Techniques",
    "difficulty": 1,
    "requires_recursion": False,
    "entry": "fibonacci",
}

DESCRIPTION = """
# Fibonacci — Bottom-Up DP

Compute the **n-th Fibonacci number** using bottom-up dynamic programming.

    F(1) = 1
    F(2) = 1
    F(n) = F(n-1) + F(n-2)   for n > 2

Use **O(1) space** — store only the last two values, not the whole table.

## Signature

```python
def fibonacci(n):
    # n: positive integer (n >= 1)
    # returns: int
    ...
```

## Examples

    fibonacci(1) → 1
    fibonacci(2) → 1
    fibonacci(6) → 8    (1,1,2,3,5,8)
    fibonacci(10) → 55

## Algorithm — Bottom-Up DP O(n) time, O(1) space

The naive recursive solution (divide & conquer) recomputes the same sub-problems
exponentially many times: T(n) = T(n-1) + T(n-2) → T(n) = O(2^n).

Save the last two values and iterate:

```
if n <= 2: return 1
prev2, prev1 = 1, 1
for i = 3 .. n:
    prev2, prev1 = prev1, prev2 + prev1
return prev1
```

## Complexity

- **Naive recursion:** O(2^n)
- **DP with table:** Θ(n) time, Θ(n) space
- **DP with rolling variables (this problem):** Θ(n) time, **O(1) space**

## Notes

- The lecture uses Fibonacci as the canonical overlapping-subproblems example:
  F(n-1) and F(n-2) both depend on F(n-3), so naive recursion recomputes it.
- The greedy-style insight: you only ever need the previous two values, so
  you don't need an array at all.
"""

STARTER = '''\
def fibonacci(n):
    """Return the n-th Fibonacci number using O(n) time, O(1) space."""
    if n <= 2:
        return 1
    prev2, prev1 = 1, 1
    for i in range(3, n + 1):
        # update prev2 and prev1
        pass
    return prev1
'''

HINTS = [
    "At each step: the new value is prev2 + prev1. Then slide the window forward.",
    "prev2, prev1 = prev1, prev2 + prev1  — Python tuple assignment does this in one line.",
    "After the loop prev1 holds F(n). Return prev1.",
]


def reference(n):
    if n <= 2:
        return 1
    prev2, prev1 = 1, 1
    for _ in range(3, n + 1):
        prev2, prev1 = prev1, prev2 + prev1
    return prev1


def tests(student):
    expected = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]

    def case_first_ten():
        for i, v in enumerate(expected[:10], start=1):
            result = student(i)
            assert result == v, f"F({i}) expected {v}, got {result}"

    def case_f1():
        assert student(1) == 1

    def case_f2():
        assert student(2) == 1

    def case_f6():
        assert student(6) == 8

    def case_f10():
        assert student(10) == 55

    def case_f15():
        assert student(15) == 610

    def case_f20():
        assert student(20) == 6765

    def case_f30():
        assert student(30) == 832040

    return [
        ("first 10 Fibonacci numbers", case_first_ten),
        ("F(1) = 1", case_f1),
        ("F(2) = 1", case_f2),
        ("F(6) = 8", case_f6),
        ("F(10) = 55", case_f10),
        ("F(15) = 610", case_f15),
        ("F(20) = 6765", case_f20),
        ("F(30) = 832040", case_f30),
    ]

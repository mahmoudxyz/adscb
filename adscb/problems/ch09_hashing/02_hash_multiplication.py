META = {
    "id": "ch09/02_hash_multiplication",
    "title": "Multiplication hash function",
    "chapter": 9,
    "chapter_title": "Chapter 9 — Hash Tables",
    "difficulty": 1,
    "requires_recursion": False,
    "entry": "hash_multiplication",
}

DESCRIPTION = """
# Multiplication Hash Function

Implement the **multiplication method** hash function from the lecture
slides. Unlike the division method, the table size m is not critical
here.

## Signature

```python
def hash_multiplication(k, m, C=None):
    # k: non-negative integer key
    # m: table size
    # C: constant in (0, 1), defaults to (sqrt(5)-1)/2 ≈ 0.618 (Knuth)
    # returns: integer in [0, m-1]
    ...
```

## Pseudocode (from slide)

```
h(k) = floor(m * (k*C - floor(k*C)))
```

Steps:
1. Multiply k by C and take the fractional part: `k*C - floor(k*C)`
2. Multiply the fractional part by m and take the floor.

## Examples

- `hash_multiplication(101, 12, C=0.8)` → `9`
  - 101 × 0.8 = 80.8, fractional = 0.8, 12 × 0.8 = 9.6, floor = 9
- `hash_multiplication(124, 1000, C=0.618)` → `18`
  - 124 × 0.618 = 76.632, fractional = 0.632, 1000 × 0.632 = 632... 
  - (approximate — exact value depends on C precision)

## Notes

- The constant C affects distribution quality. Knuth recommends
  **C = (√5 − 1)/2 ≈ 0.6180339887**, the inverse golden ratio.
- Advantage over division method: the choice of m is **not critical**.
"""

STARTER = '''\
import math

def hash_multiplication(k, m, C=None):
    """Multiplication method: h(k) = floor(m * (k*C - floor(k*C)))."""
    if C is None:
        C = (math.sqrt(5) - 1) / 2
    # your code here
    pass
'''

HINTS = [
    "Compute k * C, then take the fractional part: k*C - math.floor(k*C).",
    "Multiply the fractional part by m and floor it: math.floor(m * fractional).",
    "One-liner: return math.floor(m * (k * C - math.floor(k * C))).",
]


def reference(k, m, C=None):
    import math
    if C is None:
        C = (math.sqrt(5) - 1) / 2
    return math.floor(m * (k * C - math.floor(k * C)))


def tests(student):
    import math

    def case_slide_example():
        assert student(101, 12, C=0.8) == 9

    def case_knuth_default():
        C = (math.sqrt(5) - 1) / 2
        assert student(124, 1000, C=C) == reference(124, 1000, C=C)

    def case_zero_key():
        assert student(0, 12, C=0.8) == 0

    def case_small_m():
        assert student(10, 7, C=0.8) == reference(10, 7, C=0.8)

    def case_default_C():
        assert student(42, 100) == reference(42, 100)

    def case_large_k():
        assert student(999999, 1000) == reference(999999, 1000)

    def case_C_close_to_1():
        assert student(50, 10, C=0.99) == reference(50, 10, C=0.99)

    def case_C_close_to_0():
        assert student(50, 10, C=0.01) == reference(50, 10, C=0.01)

    return [
        ("slide example: k=101, m=12, C=0.8", case_slide_example),
        ("Knuth default C", case_knuth_default),
        ("zero key", case_zero_key),
        ("small m", case_small_m),
        ("default C parameter", case_default_C),
        ("large k", case_large_k),
        ("C close to 1", case_C_close_to_1),
        ("C close to 0", case_C_close_to_0),
    ]

META = {
    "id": "ch09/01_hash_division",
    "title": "Division hash function",
    "chapter": 9,
    "chapter_title": "Chapter 9 — Hash Tables",
    "difficulty": 1,
    "requires_recursion": False,
    "entry": "hash_division",
}

DESCRIPTION = """
# Division Hash Function

Implement the **division method** hash function, the simplest and most
common hash function from the lecture slides.

## Signature

```python
def hash_division(k, m):
    # k: non-negative integer key
    # m: table size (should be prime, far from powers of 2)
    # returns: integer in [0, m-1]
    ...
```

## Pseudocode (from slide)

```
h(k) = k mod m
```

## Examples

- `hash_division(100, 12)` → `4`  (100 mod 12 = 4)
- `hash_division(101, 10)` → `1`  (101 mod 10 = 1)
- `hash_division(53, 10)`  → `3`  (53 mod 10 = 3)

## Notes

- **Choose m as a prime number far from powers of 2 (and 10).**
- If `m = 2^p`, then `h(k)` depends only on the lowest p bits of k —
  a poor distribution.
- If `m = 10`, then `h(k)` is just the last decimal digit — also poor.
"""

STARTER = '''\
def hash_division(k, m):
    """Division method: h(k) = k mod m."""
    # your code here
    pass
'''

HINTS = [
    "The division method is just the modulo operation: k mod m.",
    "In Python: use the % operator: return k % m.",
    "That's it — one line. The difficulty is choosing a good m, not computing h(k).",
]


def reference(k, m):
    return k % m


def tests(student):
    def case_slide_example_1():
        assert student(100, 12) == 4

    def case_slide_example_2():
        assert student(101, 10) == 1

    def case_slide_example_3():
        assert student(53, 10) == 3

    def case_zero_key():
        assert student(0, 7) == 0

    def case_key_equals_m():
        assert student(7, 7) == 0

    def case_key_less_than_m():
        assert student(3, 7) == 3

    def case_large_key():
        assert student(1000000, 701) == 1000000 % 701

    def case_prime_m():
        m = 701
        assert student(12345, m) == 12345 % m

    return [
        ("slide example: 100 mod 12", case_slide_example_1),
        ("slide example: 101 mod 10", case_slide_example_2),
        ("slide example: 53 mod 10", case_slide_example_3),
        ("zero key", case_zero_key),
        ("key equals m", case_key_equals_m),
        ("key < m", case_key_less_than_m),
        ("large key", case_large_key),
        ("prime m = 701", case_prime_m),
    ]

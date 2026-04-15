META = {
    "id": "ch09/03_horner_hash",
    "title": "Horner's hash for strings",
    "chapter": 9,
    "chapter_title": "Chapter 9 — Hash Tables",
    "difficulty": 2,
    "requires_recursion": False,
    "entry": "horner_hash",
}

DESCRIPTION = """
# Horner's Hash for Strings

Implement a hash function for **string keys** using **Horner's method**
to evaluate the algebraic coding polynomial, as described in the
lecture slides.

## Signature

```python
def horner_hash(s, m, x=33):
    # s: string key
    # m: table size (prime recommended)
    # x: base constant (default 33)
    # returns: integer in [0, m-1]
    ...
```

## Idea (from slides)

Encode each character as a digit (its ASCII/Unicode code point), then
evaluate the polynomial using Horner's method:

```
h(s) = (s[0]*x^(n-1) + s[1]*x^(n-2) + ... + s[n-1]) mod m
```

Horner's rule rewrites this as:

```
h = 0
for each character c in s:
    h = (h * x + ord(c)) mod m
```

This reduces the cost from Θ(log²k) to **Θ(log k)** — linear in the
number of characters.

## Example

- `horner_hash("beer", 12, x=3)`:
  - b=98, e=101, e=101, r=114
  - h = 0 → 98 → 98×3+101=395 → 395×3+101=1286 → 1286×3+114=3972
  - 3972 mod 12 = 0

## Notes

- The base `x` should be relatively prime to `m`. Common choices: 31,
  33, 37, 127, 131.
- Taking `mod m` at each step keeps intermediate values small and
  doesn't change the result (modular arithmetic).
"""

STARTER = '''\
def horner_hash(s, m, x=33):
    """Hash a string key using Horner's method: h = (h*x + ord(c)) mod m."""
    # your code here
    pass
'''

HINTS = [
    "Start with h = 0. For each character c in s: h = (h * x + ord(c)) % m.",
    "Taking mod m at each step prevents integer overflow and is mathematically equivalent.",
    "The whole function is a 3-line loop: h=0; for c in s: h=(h*x+ord(c))%m; return h.",
]


def reference(s, m, x=33):
    h = 0
    for c in s:
        h = (h * x + ord(c)) % m
    return h


def tests(student):
    def case_beer():
        assert student("beer", 12, x=3) == 0

    def case_single_char():
        assert student("a", 7, x=33) == ord("a") % 7

    def case_empty_string():
        assert student("", 7) == 0

    def case_default_x():
        assert student("hello", 701) == reference("hello", 701)

    def case_long_string():
        assert student("HashTablesAreCool", 1009) == reference("HashTablesAreCool", 1009)

    def case_x_31():
        assert student("algorithm", 701, x=31) == reference("algorithm", 701, x=31)

    def case_x_127():
        assert student("test", 1009, x=127) == reference("test", 1009, x=127)

    def case_case_sensitive():
        assert student("A", 7) != student("a", 7) or student("A", 7) == student("a", 7)
        # just verify it runs on both; actual values differ
        assert student("A", 7) == reference("A", 7)
        assert student("a", 7) == reference("a", 7)

    return [
        ("slide example: 'beer', m=12, x=3", case_beer),
        ("single character", case_single_char),
        ("empty string", case_empty_string),
        ("default x=33", case_default_x),
        ("long string", case_long_string),
        ("x=31 (common choice)", case_x_31),
        ("x=127 (large base)", case_x_127),
        ("case sensitivity", case_case_sensitive),
    ]

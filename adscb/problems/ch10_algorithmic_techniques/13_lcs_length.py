META = {
    "id": "ch10/13_lcs_length",
    "title": "Longest Common Subsequence — Length",
    "chapter": 10,
    "chapter_title": "Chapter 10 — Algorithmic Techniques",
    "difficulty": 2,
    "requires_recursion": False,
    "entry": "lcs_length",
}

DESCRIPTION = """
# Longest Common Subsequence — Length

Given two strings `X` and `Y`, return the **length** of their longest common
subsequence (LCS).

A **subsequence** of `S` is obtained by deleting zero or more characters from `S`
without changing the order of the remaining ones. A **common subsequence** of `X`
and `Y` is a subsequence of both.

## Signature

```python
def lcs_length(X, Y):
    # X, Y: strings (may be empty)
    # returns: int
    ...
```

## Examples

    X = "ABCBDAB", Y = "BDCABA"   →  4   (e.g. "BCBA", "BCAB", "BDAB")
    X = "AGCAT",   Y = "GAC"      →  2   (e.g. "AC" or "GA")
    X = "ABCD",    Y = "EFGH"     →  0
    X = "",        Y = "ABC"      →  0

## Algorithm — Dynamic Programming Θ(m·n)

Let `M[i][j]` = LCS length of `X[0..i-1]` and `Y[0..j-1]`.

Recurrence:

    M[i][0] = M[0][j] = 0   (base case: empty prefix)

    if X[i-1] == Y[j-1]:
        M[i][j] = M[i-1][j-1] + 1
    else:
        M[i][j] = max(M[i-1][j], M[i][j-1])

```
for i in 1..m:
    for j in 1..n:
        if X[i-1] == Y[j-1]:
            M[i][j] = M[i-1][j-1] + 1
        else:
            M[i][j] = max(M[i-1][j], M[i][j-1])
return M[m][n]
```

## Complexity

- **Time:** Θ(m · n)
- **Space:** Θ(m · n) for the table (can be reduced to O(min(m,n)) with rolling rows)

## Notes

- LCS is a classic DP problem with **optimal substructure**: the LCS of
  `X[0..m-1]` and `Y[0..n-1]` decomposes into LCS of shorter prefixes.
- This problem returns only the **length**; recovering the actual subsequence
  requires backtracking through M (a natural extension).
- Brute force: enumerate all 2^m subsequences of X, check each against Y → O(m·2^m).
"""

STARTER = '''\
def lcs_length(X, Y):
    """Return the length of the longest common subsequence of X and Y."""
    m, n = len(X), len(Y)
    M = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                # characters match
                pass
            else:
                # no match — take the better of left or above
                pass
    return M[m][n]
'''

HINTS = [
    "When X[i-1] == Y[j-1]: M[i][j] = M[i-1][j-1] + 1  (extend the common subsequence).",
    "When they differ: M[i][j] = max(M[i-1][j], M[i][j-1])  (skip one character from either string).",
    "The table is (m+1)×(n+1), row 0 and column 0 are implicitly 0. Return M[m][n].",
]


def reference(X, Y):
    m, n = len(X), len(Y)
    M = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                M[i][j] = M[i - 1][j - 1] + 1
            else:
                M[i][j] = max(M[i - 1][j], M[i][j - 1])
    return M[m][n]


def tests(student):
    def case_lecture():
        assert student("ABCBDAB", "BDCABA") == 4

    def case_no_common():
        assert student("ABCD", "EFGH") == 0

    def case_identical():
        assert student("ABC", "ABC") == 3

    def case_empty_x():
        assert student("", "ABC") == 0

    def case_empty_y():
        assert student("ABC", "") == 0

    def case_both_empty():
        assert student("", "") == 0

    def case_single_match():
        assert student("A", "A") == 1

    def case_single_no_match():
        assert student("A", "B") == 0

    def case_one_is_subsequence():
        # "ACE" is a subsequence of "ABCDE"
        assert student("ABCDE", "ACE") == 3

    def case_agcat():
        assert student("AGCAT", "GAC") == 2

    def case_repeated_chars():
        assert student("AAAAAA", "AAA") == 3

    def case_reverse():
        # LCS of "ABCD" and "DCBA" = 1
        assert student("ABCD", "DCBA") == 1

    return [
        ("lecture ABCBDAB / BDCABA → 4", case_lecture),
        ("no common chars → 0", case_no_common),
        ("identical strings → full length", case_identical),
        ("empty X → 0", case_empty_x),
        ("empty Y → 0", case_empty_y),
        ("both empty → 0", case_both_empty),
        ("single match", case_single_match),
        ("single no match", case_single_no_match),
        ("one is subsequence of other → full length of shorter", case_one_is_subsequence),
        ("AGCAT / GAC → 2", case_agcat),
        ("repeated chars", case_repeated_chars),
        ("reverse strings", case_reverse),
    ]

META = {
    "id": "ch09/08_first_non_repeating",
    "title": "First Non-Repeating Character",
    "chapter": 9,
    "chapter_title": "Chapter 9 — Hash Tables",
    "difficulty": 2,
    "requires_recursion": False,
    "entry": "first_non_repeating",
    "suggest_primitives": ["HashTable"],
}

DESCRIPTION = """
# First Non-Repeating Character

Given a string, find the **first character** that appears exactly once.
If no such character exists, return `None`.

This is a classic problem best solved with a hash table for O(n)
average time.

## Signature

```python
def first_non_repeating(s):
    # s: string
    # returns: the first character that appears exactly once, or None
    ...
```

## Examples

- `first_non_repeating("leetcode")` → `"l"`
- `first_non_repeating("aabbcc")` → `None`
- `first_non_repeating("abcab")` → `"c"`

## Approach

1. **First pass:** count how many times each character appears
   (use a hash table / dict).
2. **Second pass:** scan the string left to right, return the first
   character with count == 1.

## Complexity

| Case   | Time | Space |
|--------|------|-------|
| All    | O(n) | O(k)  |

Where n = length of string, k = number of distinct characters.
"""

STARTER = '''\
def first_non_repeating(s):
    """Return the first character in s that appears exactly once, or None."""
    # your code here
    pass
'''

HINTS = [
    "First pass: count occurrences of each character using a dict. Second pass: return the first char with count 1.",
    "counts = {}; for c in s: counts[c] = counts.get(c, 0) + 1; then for c in s: if counts[c] == 1: return c.",
    "If the second pass finds no character with count 1, return None.",
]


def reference(s):
    counts = {}
    for c in s:
        counts[c] = counts.get(c, 0) + 1
    for c in s:
        if counts[c] == 1:
            return c
    return None


def tests(student):
    def case_leetcode():
        assert student("leetcode") == "l"

    def case_all_repeating():
        assert student("aabbcc") is None

    def case_middle_unique():
        assert student("abcab") == "c"

    def case_single_char():
        assert student("x") == "x"

    def case_empty_string():
        assert student("") is None

    def case_last_char_unique():
        assert student("aabbx") == "x"

    def case_long_string():
        s = "ab" * 100 + "z" + "ab" * 100
        assert student(s) == "z"

    def case_all_same():
        assert student("zzzzz") is None

    return [
        ("leetcode → 'l'", case_leetcode),
        ("all repeating → None", case_all_repeating),
        ("middle unique → 'c'", case_middle_unique),
        ("single char", case_single_char),
        ("empty string", case_empty_string),
        ("last char unique", case_last_char_unique),
        ("long string", case_long_string),
        ("all same char", case_all_same),
    ]

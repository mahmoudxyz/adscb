META = {
    "id": "ch04/33_balanced_parens",
    "title": "Balanced parentheses check",
    "chapter": 4,
    "chapter_title": "Chapter 4 — Elementary Data Structures",
    "difficulty": 2,
    "requires_recursion": False,
    "entry": "is_balanced",
    "suggest_primitives": ["Stack"],
}

DESCRIPTION = """
# Balanced parentheses

Given a string containing only the characters `()[]{}`, return `True`
if every opening bracket has a matching closing bracket of the same
kind and in the right nesting order, `False` otherwise.

## Signature

```python
def is_balanced(s):
    # s is a string of bracket characters
    # returns True or False
    ...
```

## Examples

    "()"          →  True
    "()[]{}"      →  True
    "([{}])"      →  True
    "(]"          →  False
    "([)]"        →  False     # wrong nesting
    "(("          →  False     # unclosed
    "))"          →  False     # unmatched close
    ""            →  True      # empty is balanced

## Notes

- Use a `Stack` from `adscb.primitives`.
- This is the textbook use case for a stack. If you've never written
  it, write it once — it's ~10 lines and genuinely useful to know.
"""

STARTER = '''\
from adscb.primitives import Stack


def is_balanced(s):
    """Return True if s is a balanced bracket string."""
    # your code here
    pass
'''

HINTS = [
    "Map each closing bracket to its opener: ')': '(', ']': '[', '}': '{'.",
    "Walk the string. If c is an opener push it. If c is a closer, pop the stack and check that it matches the expected opener — return False otherwise.",
    "At the end, balanced means the stack is empty (no unclosed openers).",
]


def reference(s):
    from adscb.primitives import Stack
    S = Stack(max(len(s), 1))
    pairs = {")": "(", "]": "[", "}": "{"}
    openers = set("([{")
    for c in s:
        if c in openers:
            S.push(c)
        elif c in pairs:
            if S.is_empty() or S.pop() != pairs[c]:
                return False
    return S.is_empty()


def tests(student):

    def case_empty():
        assert student("") is True

    def case_simple_pair():
        assert student("()") is True

    def case_all_types():
        assert student("()[]{}") is True

    def case_nested():
        assert student("([{}])") is True
        assert student("[([]){}]") is True

    def case_wrong_type():
        assert student("(]") is False

    def case_wrong_nesting():
        assert student("([)]") is False

    def case_unclosed():
        assert student("((") is False
        assert student("({[") is False

    def case_unmatched_close():
        assert student("))") is False
        assert student("}") is False

    def case_long_balanced():
        assert student("((()))[[]]{{{}}}") is True

    def case_long_unbalanced():
        assert student("((()))[[]]{{{}") is False

    return [
        ("empty string", case_empty),
        ("simple ()", case_simple_pair),
        ("all three types", case_all_types),
        ("nested brackets", case_nested),
        ("wrong type pairing", case_wrong_type),
        ("wrong nesting order", case_wrong_nesting),
        ("unclosed openers", case_unclosed),
        ("unmatched closers", case_unmatched_close),
        ("long balanced", case_long_balanced),
        ("long unbalanced", case_long_unbalanced),
    ]

META = {
    "id": "ch04/34_postfix_eval",
    "title": "Evaluate a postfix expression",
    "chapter": 4,
    "chapter_title": "Chapter 4 — Elementary Data Structures",
    "difficulty": 2,
    "requires_recursion": False,
    "entry": "evaluate",
    "suggest_primitives": ["Stack"],
}

DESCRIPTION = """
# Evaluate a postfix expression

In postfix (also called Reverse Polish Notation), operators come
**after** their operands. So `3 4 +` means `3 + 4 = 7`, and
`5 1 2 + 4 * + 3 -` means `5 + ((1 + 2) * 4) - 3 = 14`.

Given a postfix expression as a string of space-separated tokens,
evaluate it and return the result as an integer.

Supported operators: `+`, `-`, `*`, `/` (integer division,
truncating toward zero).

## Signature

```python
def evaluate(expression):
    # expression is a string like "5 1 2 + 4 * + 3 -"
    # returns an int
    ...
```

## Examples

    "3 4 +"                →  7
    "5 1 2 + 4 * + 3 -"    →  14
    "2 3 4 * +"            →  14
    "10 2 /"               →  5
    "7"                    →  7    # single number

## Notes

- Use a `Stack` from `adscb.primitives`.
- Division is integer division. Use `int(a / b)` (not `a // b`) so
  that `-7 / 2` gives `-3` and not `-4`.
- This is the second textbook stack problem, right after balanced
  parens. Worth having in your bones.
"""

STARTER = '''\
from adscb.primitives import Stack


def evaluate(expression):
    """Evaluate a postfix (RPN) expression. Return an int."""
    # your code here
    pass
'''

HINTS = [
    "Split the expression on whitespace. Walk the tokens.",
    "If the token is a number (try int(token)), push it. If it's an operator, pop the TOP as b, pop next as a, compute a OP b, push the result.",
    "At the end, the answer is the only thing left on the stack. Return S.pop().",
]


def reference(expression):
    from adscb.primitives import Stack
    tokens = expression.split()
    S = Stack(max(len(tokens), 1))
    for t in tokens:
        if t in ("+", "-", "*", "/"):
            b = S.pop()
            a = S.pop()
            if t == "+":
                S.push(a + b)
            elif t == "-":
                S.push(a - b)
            elif t == "*":
                S.push(a * b)
            else:  # "/"
                S.push(int(a / b))  # truncate toward zero
        else:
            S.push(int(t))
    return S.pop()


def tests(student):

    def case_single_number():
        assert student("7") == 7
        assert student("-3") == -3

    def case_simple_add():
        assert student("3 4 +") == 7

    def case_simple_sub():
        assert student("10 3 -") == 7

    def case_simple_mul():
        assert student("5 6 *") == 30

    def case_simple_div():
        assert student("10 2 /") == 5

    def case_pdf_like():
        # 5 + ((1+2)*4) - 3 = 5 + 12 - 3 = 14
        assert student("5 1 2 + 4 * + 3 -") == 14

    def case_nested():
        # (2 + 3) * 4 = 20
        assert student("2 3 + 4 *") == 20
        # 2 + (3 * 4) = 14
        assert student("2 3 4 * +") == 14

    def case_order_matters():
        # 10 - 3 = 7, NOT 3 - 10
        assert student("10 3 -") == 7
        # 10 / 3 = 3 (truncating)
        assert student("10 3 /") == 3

    def case_negative_division():
        # -7 / 2 should truncate toward zero → -3, not -4
        assert student("0 7 - 2 /") == -3

    def case_deep_expression():
        # ((1+2)+(3+4)) * ((5+6)+(7+8)) = 10 * 26 = 260
        assert student("1 2 + 3 4 + + 5 6 + 7 8 + + *") == 260

    return [
        ("single number", case_single_number),
        ("simple addition", case_simple_add),
        ("simple subtraction", case_simple_sub),
        ("simple multiplication", case_simple_mul),
        ("simple division", case_simple_div),
        ("PDF-style mixed expression", case_pdf_like),
        ("nested operations", case_nested),
        ("operand order matters", case_order_matters),
        ("negative division truncates toward zero", case_negative_division),
        ("deep expression", case_deep_expression),
    ]

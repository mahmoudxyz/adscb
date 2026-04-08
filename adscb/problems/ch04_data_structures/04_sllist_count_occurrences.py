META = {
    "id": "ch04/04_sllist_count_occurrences",
    "title": "Count occurrences of a key in an SLList",
    "chapter": 4,
    "chapter_title": "Chapter 4 — Elementary Data Structures",
    "difficulty": 1,
    "requires_recursion": True,
    "entry": "count",
}

DESCRIPTION = """
# Count occurrences of a key

Given the head of a singly linked list and an integer `x`, return the
number of nodes whose key equals `x`. Write a **recursive** version.

## Signature

```python
def count(head, x):
    # head is an SLList.Node or None
    # returns an int
    ...
```

## Examples

    L: head → [1] → [2] → [1] → [3] → [1] → /
    count(L.head, 1)  →  3
    count(L.head, 2)  →  1
    count(L.head, 99) →  0
    count(None, 5)    →  0

## Notes

- Recursive only.
- Complexity: Θ(n). You must visit every node to count.
"""

STARTER = '''\
from adscb.primitives import SLList


def count(head, x):
    """Recursively count how many nodes have key == x."""
    # your code here
    pass
'''

HINTS = [
    "Base case: head is None → return 0.",
    "Otherwise return (1 if head.key == x else 0) + count(head.next, x).",
]


def reference(head, x):
    if head is None:
        return 0
    return (1 if head.key == x else 0) + reference(head.next, x)


def tests(student):
    from adscb.primitives import SLList

    def case_empty():
        assert student(None, 5) == 0

    def case_no_match():
        L = SLList.from_list([1, 2, 3])
        assert student(L.head, 99) == 0

    def case_one_match():
        L = SLList.from_list([1, 2, 3])
        assert student(L.head, 2) == 1

    def case_multiple_matches():
        L = SLList.from_list([1, 2, 1, 3, 1])
        assert student(L.head, 1) == 3

    def case_all_match():
        L = SLList.from_list([7, 7, 7, 7])
        assert student(L.head, 7) == 4

    def case_string_keys():
        L = SLList.from_list(["a", "b", "a", "c", "a"])
        assert student(L.head, "a") == 3

    return [
        ("empty list", case_empty),
        ("no matches", case_no_match),
        ("one match", case_one_match),
        ("three matches", case_multiple_matches),
        ("all match", case_all_match),
        ("string keys", case_string_keys),
    ]

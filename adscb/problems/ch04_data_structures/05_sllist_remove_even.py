META = {
    "id": "ch04/05_sllist_remove_even",
    "title": "Recursively remove all even-keyed nodes",
    "chapter": 4,
    "chapter_title": "Chapter 4 — Elementary Data Structures",
    "difficulty": 2,
    "requires_recursion": True,
    "entry": "remove_even",
}

DESCRIPTION = """
# Remove all even-keyed nodes (recursive)

Given the head of a singly linked list of integers, **remove every node**
whose key is even. Return the new head. Must be recursive.

## Signature

```python
def remove_even(head):
    # head is an SLList.Node or None
    # returns the new head
    ...
```

## Examples

    before: head → [4] → [6] → [7] → [3] → [2] → [5] → /
    after:  head → [7] → [3] → [5] → /

    before: head → [2] → [4] → [6] → /      # all even
    after:  head → /                         # empty

    before: head → [1] → [3] → [5] → /      # all odd
    after:  head → [1] → [3] → [5] → /      # unchanged

## Notes

- Recursive only.
- Complexity: Θ(n). Every node must be visited.
"""

STARTER = '''\
from adscb.primitives import SLList


def remove_even(head):
    """Recursively drop every node whose key is even. Return new head."""
    # your code here
    pass
'''

HINTS = [
    "Base case: head is None → return None.",
    "If head.key is even, return remove_even(head.next) — the current node vanishes.",
    "Otherwise wire head.next = remove_even(head.next) and return head.",
]


def reference(head):
    if head is None:
        return None
    if head.key % 2 == 0:
        return reference(head.next)
    head.next = reference(head.next)
    return head


def tests(student):
    from adscb.primitives import SLList

    def case_empty():
        assert student(None) is None

    def case_mixed():
        L = SLList.from_list([4, 6, 7, 3, 2, 5])
        new_head = student(L.head)
        assert SLList.head_to_list(new_head) == [7, 3, 5]

    def case_all_even():
        L = SLList.from_list([2, 4, 6, 8])
        assert student(L.head) is None

    def case_all_odd():
        L = SLList.from_list([1, 3, 5, 7])
        new_head = student(L.head)
        assert SLList.head_to_list(new_head) == [1, 3, 5, 7]

    def case_single_even():
        L = SLList.from_list([42])
        assert student(L.head) is None

    def case_single_odd():
        L = SLList.from_list([41])
        new_head = student(L.head)
        assert SLList.head_to_list(new_head) == [41]

    def case_negatives():
        L = SLList.from_list([-4, -3, -2, -1, 0])
        new_head = student(L.head)
        assert SLList.head_to_list(new_head) == [-3, -1]

    return [
        ("empty list", case_empty),
        ("mixed evens and odds", case_mixed),
        ("all even → empty", case_all_even),
        ("all odd → unchanged", case_all_odd),
        ("single even", case_single_even),
        ("single odd", case_single_odd),
        ("negative numbers and zero", case_negatives),
    ]

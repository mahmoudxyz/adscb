META = {
    "id": "ch04/03_sllist_tail_insert_recursive",
    "title": "Recursive tail_insert on a singly linked list",
    "chapter": 4,
    "chapter_title": "Chapter 4 — Elementary Data Structures",
    "difficulty": 2,
    "requires_recursion": True,
    "entry": "tail_insert",
}

DESCRIPTION = """
# Recursive tail_insert on a singly linked list

Write a **recursive** version of `tail_insert`. Given the head of a list
and a key `k`, add a new node with key `k` at the **end** of the list and
return the (possibly new) head.

## Signature

```python
def tail_insert(head, k):
    # head is an SLList.Node or None
    # returns the head of the list after insertion
    ...
```

## Examples

    before: head → /
    tail_insert(head, 5)
    after:  head → [5] → /

    before: head → [1] → [2] → /
    tail_insert(head, 99)
    after:  head → [1] → [2] → [99] → /

## Notes

- Recursive only.
- If the list is empty, you must create and return a new node.
- Complexity: Θ(n). You walk every node either way.
"""

STARTER = '''\
from adscb.primitives import SLList


def tail_insert(head, k):
    """Insert a node with key k at the tail. Return the new head."""
    # your code here
    pass
'''

HINTS = [
    "Base case: head is None → return a fresh SLList.Node(k).",
    "Recursive case: head.next = tail_insert(head.next, k); return head.",
    "Yes, it's just those two cases. Three lines.",
]


def reference(head, k):
    from adscb.primitives import SLList
    if head is None:
        return SLList.Node(k)
    head.next = reference(head.next, k)
    return head


def tests(student):
    from adscb.primitives import SLList

    def case_empty():
        result = student(None, 5)
        assert result is not None and result.key == 5 and result.next is None, \
            "inserting into empty list should yield a single-node list"

    def case_single():
        L = SLList.from_list([1])
        new_head = student(L.head, 2)
        assert SLList.head_to_list(new_head) == [1, 2]

    def case_multi():
        L = SLList.from_list([1, 2, 3])
        new_head = student(L.head, 99)
        assert SLList.head_to_list(new_head) == [1, 2, 3, 99]

    def case_preserves_order():
        L = SLList.from_list([10, -1, 4])
        new_head = student(L.head, 0)
        assert SLList.head_to_list(new_head) == [10, -1, 4, 0]

    def case_returns_same_head_when_nonempty():
        L = SLList.from_list([7])
        original = L.head
        new_head = student(L.head, 8)
        assert new_head is original, \
            "when list is non-empty, you should return the same head node"

    return [
        ("empty list", case_empty),
        ("single-node list", case_single),
        ("multi-node list", case_multi),
        ("order preserved", case_preserves_order),
        ("returns same head when non-empty", case_returns_same_head_when_nonempty),
    ]

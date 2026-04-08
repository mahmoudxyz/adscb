META = {
    "id": "ch04/32_sllist_middle",
    "title": "Find the middle node of a singly linked list",
    "chapter": 4,
    "chapter_title": "Chapter 4 — Elementary Data Structures",
    "difficulty": 2,
    "requires_recursion": False,
    "entry": "middle",
}

DESCRIPTION = """
# Find the middle node

Given the head of a singly linked list, return the **middle** node.
If the list has even length, return the **second** of the two middle
nodes.

The twist: do it in **one pass** without counting the length first.

## Signature

```python
def middle(head):
    # head is an SLList.Node or None
    # returns the middle node, or None for an empty list
    ...
```

## Examples

    head → [1] → [2] → [3] → [4] → [5] → /     middle → [3]
    head → [1] → [2] → [3] → [4] → /            middle → [3]  (second of the two middle)
    head → [1] → /                               middle → [1]
    head → /                                      middle → None

## Notes

- One pass. No counting-then-walking twice.
- This is the two-pointer ("tortoise and hare") trick.
"""

STARTER = '''\
from adscb.primitives import SLList


def middle(head):
    """Return the middle node. For even length, return the second middle node."""
    # your code here
    pass
'''

HINTS = [
    "Use two pointers, slow and fast. Both start at head.",
    "Each step: fast moves twice, slow moves once. When fast falls off the end, slow is at the middle.",
    "For even lengths, the exact loop condition determines which middle you get. `while fast is not None and fast.next is not None` gives you the SECOND of the two middle nodes.",
]


def reference(head):
    if head is None:
        return None
    slow = head
    fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
    return slow


def tests(student):
    from adscb.primitives import SLList

    def case_empty():
        assert student(None) is None

    def case_single():
        L = SLList.from_list([1])
        assert student(L.head).key == 1

    def case_two():
        L = SLList.from_list([1, 2])
        # even length: return the second middle
        assert student(L.head).key == 2

    def case_three():
        L = SLList.from_list([1, 2, 3])
        assert student(L.head).key == 2

    def case_four():
        L = SLList.from_list([1, 2, 3, 4])
        assert student(L.head).key == 3

    def case_five():
        L = SLList.from_list([1, 2, 3, 4, 5])
        assert student(L.head).key == 3

    def case_long():
        L = SLList.from_list(list(range(100)))  # 0..99, 100 elements
        # even length, second middle → index 50 → key 50
        assert student(L.head).key == 50

    return [
        ("empty list", case_empty),
        ("one node", case_single),
        ("two nodes (returns second)", case_two),
        ("three nodes", case_three),
        ("four nodes (returns second middle)", case_four),
        ("five nodes", case_five),
        ("100 nodes", case_long),
    ]

META = {
    "id": "ch04/30_sllist_reverse_iterative",
    "title": "Reverse a singly linked list (iterative)",
    "chapter": 4,
    "chapter_title": "Chapter 4 — Elementary Data Structures",
    "difficulty": 2,
    "requires_recursion": False,
    "entry": "reverse",
}

DESCRIPTION = """
# Reverse a singly linked list (iterative)

Given the head of a singly linked list, reverse the chain of `.next`
pointers and return the new head. Do it **iteratively** and in-place —
don't allocate new nodes.

## Signature

```python
def reverse(head):
    # head is an SLList.Node or None
    # returns the new head
    ...
```

## Example

    before: head → [1] → [2] → [3] → [4] → /
    after:  head → [4] → [3] → [2] → [1] → /

## Notes

- In-place: reuse the existing nodes, just flip their `.next`.
- O(n) time, O(1) extra space.
- This is one of the most classic linked-list problems. Knowing the
  three-pointer dance (prev, curr, next_node) by heart is worth it.
"""

STARTER = '''\
from adscb.primitives import SLList


def reverse(head):
    """Reverse the list in place and return the new head. Iterative."""
    # your code here
    pass
'''

HINTS = [
    "Three pointers: prev = None, curr = head. Walk curr forward.",
    "Each step: save next_node = curr.next (before you clobber it!), then curr.next = prev, then prev = curr, then curr = next_node.",
    "When curr becomes None, prev is the new head. Return it.",
]


def reference(head):
    prev = None
    curr = head
    while curr is not None:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node
    return prev


def tests(student):
    from adscb.primitives import SLList

    def case_empty():
        assert student(None) is None

    def case_single():
        L = SLList.from_list([42])
        new_head = student(L.head)
        assert SLList.head_to_list(new_head) == [42]

    def case_two():
        L = SLList.from_list([1, 2])
        new_head = student(L.head)
        assert SLList.head_to_list(new_head) == [2, 1]

    def case_many():
        L = SLList.from_list([1, 2, 3, 4, 5])
        new_head = student(L.head)
        assert SLList.head_to_list(new_head) == [5, 4, 3, 2, 1]

    def case_in_place():
        # Make sure it doesn't allocate fresh nodes — original node ids should persist
        L = SLList.from_list([1, 2, 3])
        original_nodes = set()
        curr = L.head
        while curr is not None:
            original_nodes.add(id(curr))
            curr = curr.next
        new_head = student(L.head)
        reversed_nodes = set()
        curr = new_head
        while curr is not None:
            reversed_nodes.add(id(curr))
            curr = curr.next
        assert reversed_nodes == original_nodes, \
            "reverse should reuse the existing nodes, not allocate new ones"

    def case_new_tail_next_is_none():
        L = SLList.from_list([1, 2, 3])
        new_head = student(L.head)
        # The new tail (which is the old head, key=1) should have next=None
        curr = new_head
        while curr.next is not None:
            curr = curr.next
        assert curr.key == 1 and curr.next is None

    return [
        ("empty list", case_empty),
        ("single node", case_single),
        ("two nodes", case_two),
        ("five nodes", case_many),
        ("in-place (reuses existing nodes)", case_in_place),
        ("new tail's next is None", case_new_tail_next_is_none),
    ]

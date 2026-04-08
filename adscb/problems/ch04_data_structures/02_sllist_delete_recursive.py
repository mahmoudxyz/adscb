META = {
    "id": "ch04/02_sllist_delete_recursive",
    "title": "Recursive delete on a singly linked list",
    "chapter": 4,
    "chapter_title": "Chapter 4 — Elementary Data Structures",
    "difficulty": 2,
    "requires_recursion": True,
    "entry": "delete",
    "suggest_primitives": ["SLList"],
}

DESCRIPTION = """
# Recursive delete on a singly linked list

Write a **recursive** version of `delete`. Given the head node of a list
and a key `k`, remove the first node whose key equals `k`. Return the
(possibly new) head of the list.

## Signature

```python
def delete(head, k):
    # head is an SLList.Node or None
    # returns the new head (possibly None, possibly a different node)
    ...
```

## Examples

    before:  head → [4] → [6] → [7] → /
    delete(head, 6)
    after:   head → [4] → [7] → /

    before:  head → [4] → [6] → [7] → /
    delete(head, 4)          # removing the head
    after:   head → [6] → [7] → /

    before:  head → /        # empty
    delete(head, 99)         # no-op
    after:   head → /

## Notes

- Recursive only. Iterative solutions get a warning.
- Only remove the **first** occurrence.
- Complexity: Θ(n) worst case, O(1) best case (head match).
"""

STARTER = '''\
from adscb.primitives import SLList


def delete(head, k):
    """Recursively delete the first node with key == k. Return the new head."""
    # your code here
    pass
'''

HINTS = [
    "Base case: if head is None, return None.",
    "If head.key == k, the head itself is what you want to drop. Return head.next.",
    "Otherwise: head.next = delete(head.next, k); return head.",
]


def reference(head, k):
    if head is None:
        return None
    if head.key == k:
        return head.next
    head.next = reference(head.next, k)
    return head


def tests(student):
    from adscb.primitives import SLList

    def case_empty():
        assert student(None, 5) is None

    def case_delete_head():
        L = SLList.from_list([4, 6, 7])
        new_head = student(L.head, 4)
        got = SLList.head_to_list(new_head)
        assert got == [6, 7], f"expected [6, 7], got {got}"

    def case_delete_middle():
        L = SLList.from_list([10, -1, 4, 1])
        new_head = student(L.head, 4)
        got = SLList.head_to_list(new_head)
        assert got == [10, -1, 1], f"expected [10, -1, 1], got {got}"

    def case_delete_tail():
        L = SLList.from_list([1, 2, 3])
        new_head = student(L.head, 3)
        got = SLList.head_to_list(new_head)
        assert got == [1, 2], f"expected [1, 2], got {got}"

    def case_not_found():
        L = SLList.from_list([1, 2, 3])
        new_head = student(L.head, 99)
        got = SLList.head_to_list(new_head)
        assert got == [1, 2, 3], f"list should be unchanged, got {got}"

    def case_single_match():
        L = SLList.from_list([42])
        assert student(L.head, 42) is None

    def case_first_occurrence_only():
        L = SLList.from_list([1, 2, 2, 3])
        new_head = student(L.head, 2)
        got = SLList.head_to_list(new_head)
        assert got == [1, 2, 3], f"only first occurrence should go; got {got}"

    return [
        ("empty list", case_empty),
        ("delete head", case_delete_head),
        ("delete middle", case_delete_middle),
        ("delete tail", case_delete_tail),
        ("key not found, list unchanged", case_not_found),
        ("single-node list, match", case_single_match),
        ("only first occurrence removed", case_first_occurrence_only),
    ]

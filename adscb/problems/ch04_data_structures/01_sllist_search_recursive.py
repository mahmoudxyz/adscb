META = {
    "id": "ch04/01_sllist_search_recursive",
    "title": "Recursive search on a singly linked list",
    "chapter": 4,
    "chapter_title": "Chapter 4 — Elementary Data Structures",
    "difficulty": 1,
    "requires_recursion": True,
    "entry": "search",
    "suggest_primitives": ["SLList"],
}

DESCRIPTION = """
# Recursive search on a singly linked list

Rewrite the iterative `search` from the slides as a **recursive** function.
Given the head node of a list and a key `k`, return the first node whose
key equals `k`, or `None` if no such node exists.

## Signature

```python
def search(head, k):
    # head is an SLList.Node or None
    # returns a Node or None
    ...
```

## Example

    L:  head → [10] → [-1] → [4] → [1] → /

    search(L.head, 4)   →  the node with key 4
    search(L.head, 99)  →  None

## Notes

- Use recursion. An iterative `while` loop will be flagged as a warning.
- The base cases are "list is empty" and "current node matches".
- Complexity should be Θ(n) in the worst case — same as the iterative version.
"""

STARTER = '''\
from adscb.primitives import SLList


def search(head, k):
    """Return the first node with key == k, or None. Must be recursive."""
    # your code here
    pass
'''

HINTS = [
    "Two base cases: head is None (return None), or head.key == k (return head).",
    "Recursive case: return search(head.next, k).",
    "That's literally it — three lines of actual logic.",
]


def reference(head, k):
    if head is None or head.key == k:
        return head
    return reference(head.next, k)


def tests(student):
    from adscb.primitives import SLList

    def case_empty():
        assert student(None, 5) is None, "search on empty list should return None"

    def case_head_match():
        L = SLList.from_list([10, -1, 4, 1])
        node = student(L.head, 10)
        assert node is not None and node.key == 10, \
            f"expected node with key 10, got {node}"

    def case_middle_match():
        L = SLList.from_list([10, -1, 4, 1])
        node = student(L.head, 4)
        assert node is not None and node.key == 4, \
            f"expected node with key 4, got {node}"

    def case_tail_match():
        L = SLList.from_list([10, -1, 4, 1])
        node = student(L.head, 1)
        assert node is not None and node.key == 1, \
            f"expected node with key 1, got {node}"

    def case_not_found():
        L = SLList.from_list([10, -1, 4, 1])
        assert student(L.head, 99) is None, "missing key should return None"

    def case_single_node_hit():
        L = SLList.from_list([42])
        node = student(L.head, 42)
        assert node is not None and node.key == 42

    def case_single_node_miss():
        L = SLList.from_list([42])
        assert student(L.head, 0) is None

    def case_first_occurrence():
        L = SLList.from_list([1, 2, 3, 2, 1])
        node = student(L.head, 2)
        # the returned node should be the first 2 — i.e. its next is the 3
        assert node is not None and node.key == 2 and node.next.key == 3, \
            "should return the first node matching the key, not a later one"

    return [
        ("empty list", case_empty),
        ("head matches", case_head_match),
        ("middle matches", case_middle_match),
        ("tail matches", case_tail_match),
        ("key not found", case_not_found),
        ("single node, hit", case_single_node_hit),
        ("single node, miss", case_single_node_miss),
        ("returns first occurrence", case_first_occurrence),
    ]

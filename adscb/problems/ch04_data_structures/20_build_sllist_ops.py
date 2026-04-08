META = {
    "id": "ch04/20_build_sllist_ops",
    "title": "Build it yourself — SLList operations from scratch",
    "chapter": 4,
    "chapter_title": "Chapter 4 — Elementary Data Structures",
    "difficulty": 1,
    "requires_recursion": False,
    "entry": "build",
}

DESCRIPTION = """
# Build it yourself: basic SLList operations

The point of this problem is to **feel the pointers** before you use
the `SLList` class in later problems. You'll implement three classic
operations on a singly linked list given only the `Node` type.

A `Node` has `.key` and `.next`. There is no `SLList` class here —
you work directly with head pointers (which may be `None`).

## What you write

Implement these three functions, then return them from `build()`:

```python
def head_insert(head, k):
    # insert a new node with key k at the FRONT
    # return the new head
    ...

def tail_insert(head, k):
    # insert a new node with key k at the END
    # return the (possibly new) head
    ...

def search(head, k):
    # return the first node whose key == k, or None
    ...

def build():
    return head_insert, tail_insert, search
```

## Notes

- Iterative versions are fine (the recursive versions are separate problems).
- You get a clean `Node` class via `from adscb.primitives import SLList`
  and then `Node = SLList.Node`. Don't use any other SLList method —
  the whole point is that you build the operations.
- Complexity targets:
  - `head_insert`: O(1)
  - `tail_insert`: Θ(n)
  - `search`: Θ(n) worst case, O(1) best case
"""

STARTER = '''\
from adscb.primitives import SLList

Node = SLList.Node


def build():
    def head_insert(head, k):
        # your code here
        pass

    def tail_insert(head, k):
        # your code here
        pass

    def search(head, k):
        # your code here
        pass

    return head_insert, tail_insert, search
'''

HINTS = [
    "head_insert: make a new Node(k), point its .next at the old head, return the new node.",
    "tail_insert: if head is None return Node(k). Otherwise walk until curr.next is None, then set curr.next = Node(k) and return the original head.",
    "search: walk curr from head. If curr.key == k return curr. Otherwise curr = curr.next. If you fall off the end, return None.",
]


def reference():
    from adscb.primitives import SLList
    Node = SLList.Node

    def head_insert(head, k):
        new = Node(k)
        new.next = head
        return new

    def tail_insert(head, k):
        if head is None:
            return Node(k)
        curr = head
        while curr.next is not None:
            curr = curr.next
        curr.next = Node(k)
        return head

    def search(head, k):
        curr = head
        while curr is not None:
            if curr.key == k:
                return curr
            curr = curr.next
        return None

    return head_insert, tail_insert, search


def tests(student):
    from adscb.primitives import SLList

    def _chain_to_list(head):
        return SLList.head_to_list(head)

    def case_returns_three_callables():
        result = student()
        assert isinstance(result, tuple) and len(result) == 3
        h, t, s = result
        assert all(callable(f) for f in (h, t, s))

    def case_head_insert_empty():
        h, _, _ = student()
        new_head = h(None, 5)
        assert _chain_to_list(new_head) == [5]

    def case_head_insert_multiple():
        h, _, _ = student()
        head = None
        for v in [1, 2, 3]:
            head = h(head, v)
        # inserted at front, so order is reversed
        assert _chain_to_list(head) == [3, 2, 1]

    def case_tail_insert_empty():
        _, t, _ = student()
        new_head = t(None, 5)
        assert _chain_to_list(new_head) == [5]

    def case_tail_insert_multiple():
        _, t, _ = student()
        head = None
        for v in [1, 2, 3]:
            head = t(head, v)
        assert _chain_to_list(head) == [1, 2, 3]

    def case_search_empty():
        _, _, s = student()
        assert s(None, 5) is None

    def case_search_found():
        _, t, s = student()
        head = None
        for v in [10, 20, 30, 40]:
            head = t(head, v)
        node = s(head, 30)
        assert node is not None and node.key == 30

    def case_search_not_found():
        _, t, s = student()
        head = None
        for v in [1, 2, 3]:
            head = t(head, v)
        assert s(head, 99) is None

    def case_mixed_operations():
        h, t, s = student()
        head = None
        head = h(head, 2)     # [2]
        head = t(head, 3)     # [2, 3]
        head = h(head, 1)     # [1, 2, 3]
        head = t(head, 4)     # [1, 2, 3, 4]
        assert _chain_to_list(head) == [1, 2, 3, 4]
        node = s(head, 3)
        assert node is not None and node.key == 3 and node.next.key == 4

    return [
        ("build() returns 3 callables", case_returns_three_callables),
        ("head_insert into empty", case_head_insert_empty),
        ("head_insert reverses order", case_head_insert_multiple),
        ("tail_insert into empty", case_tail_insert_empty),
        ("tail_insert preserves order", case_tail_insert_multiple),
        ("search on empty list", case_search_empty),
        ("search finds node", case_search_found),
        ("search returns None when absent", case_search_not_found),
        ("mixed operations", case_mixed_operations),
    ]

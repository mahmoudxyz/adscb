META = {
    "id": "ch04/31_sllist_reverse_recursive",
    "title": "Reverse a singly linked list (recursive)",
    "chapter": 4,
    "chapter_title": "Chapter 4 — Elementary Data Structures",
    "difficulty": 3,
    "requires_recursion": True,
    "entry": "reverse",
}

DESCRIPTION = """
# Reverse a singly linked list (recursive)

Same as the previous problem, but **recursive**. This is genuinely
harder than the iterative version — the recursive formulation is
elegant but counter-intuitive the first time you see it.

## Signature

```python
def reverse(head):
    # head is an SLList.Node or None
    # returns the new head
    ...
```

## The trick

Suppose you've recursively reversed `head.next`. You now have:

    head → [1] → [2] → [3] ← [4] ← [5]
                  ↑                  ↑
                 head.next          new_head (returned by the recursive call)

The rest of the list is already reversed. All you need is to flip
one more link: the pointer between `head` and `head.next`. How?

    head.next.next = head
    head.next = None

Now `head` is properly at the tail, and you return `new_head`.

## Notes

- Recursive only.
- O(n) time, O(n) stack space.
"""

STARTER = '''\
from adscb.primitives import SLList


def reverse(head):
    """Recursively reverse the list. Return the new head."""
    # your code here
    pass
'''

HINTS = [
    "Base cases: if head is None or head.next is None, just return head.",
    "Recursive step: new_head = reverse(head.next). Now head.next is the OLD next, still pointing to the sub-reversed list.",
    "Flip the link between head and head.next: head.next.next = head; head.next = None. Return new_head.",
]


def reference(head):
    if head is None or head.next is None:
        return head
    new_head = reference(head.next)
    head.next.next = head
    head.next = None
    return new_head


def tests(student):
    from adscb.primitives import SLList

    def case_empty():
        assert student(None) is None

    def case_single():
        L = SLList.from_list([7])
        new_head = student(L.head)
        assert SLList.head_to_list(new_head) == [7]

    def case_two():
        L = SLList.from_list([1, 2])
        new_head = student(L.head)
        assert SLList.head_to_list(new_head) == [2, 1]

    def case_many():
        L = SLList.from_list([1, 2, 3, 4, 5, 6])
        new_head = student(L.head)
        assert SLList.head_to_list(new_head) == [6, 5, 4, 3, 2, 1]

    def case_no_cycle_after_reverse():
        L = SLList.from_list([1, 2, 3])
        new_head = student(L.head)
        # walk and make sure we terminate cleanly
        count = 0
        curr = new_head
        while curr is not None and count < 100:
            curr = curr.next
            count += 1
        assert count == 3, f"should walk exactly 3 nodes, walked {count}"

    return [
        ("empty list", case_empty),
        ("single node", case_single),
        ("two nodes", case_two),
        ("six nodes", case_many),
        ("no accidental cycle", case_no_cycle_after_reverse),
    ]

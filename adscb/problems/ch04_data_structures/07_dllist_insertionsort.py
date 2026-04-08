META = {
    "id": "ch04/07_dllist_insertionsort",
    "title": "Insertion sort on a doubly linked list",
    "chapter": 4,
    "chapter_title": "Chapter 4 — Elementary Data Structures",
    "difficulty": 2,
    "requires_recursion": False,
    "entry": "insertion_sort",
}

DESCRIPTION = """
# Insertion sort on a DLList

Given a `DLList`, sort its nodes in ascending order of key using the
**insertion sort** algorithm. The slides show a version that swaps
**keys** rather than rewiring nodes — do the same.

## Signature

```python
def insertion_sort(L):
    # L is a DLList instance — modify it in place
    # return value is ignored
    ...
```

## Example

    before: head ⇄ [3] ⇄ [1] ⇄ [4] ⇄ [1] ⇄ [5] ⇄ [2] → /
    after:  head ⇄ [1] ⇄ [1] ⇄ [2] ⇄ [3] ⇄ [4] ⇄ [5] → /

## Notes

- Can be iterative. No recursion requirement.
- Swap `.key` values; don't rewire `.prev` / `.next`.
- Complexity: O(n²) worst case, matching array-based insertion sort.
- Use the `.prev` pointer — that's the whole point of having a DLList here.
"""

STARTER = '''\
from adscb.primitives import DLList


def insertion_sort(L):
    """Sort the DLList L in place by swapping keys."""
    # your code here
    pass
'''

HINTS = [
    "Walk forward from L.head with a pointer `tmp`. For each node, bubble it backwards via .prev until it's in the right place.",
    "Inner loop: while p.prev is not None and p.key < p.prev.key: swap their keys and move p = p.prev.",
    "Then advance tmp = tmp.next and repeat.",
]


def reference(L):
    tmp = L.head
    while tmp is not None:
        p = tmp
        while p.prev is not None and p.key < p.prev.key:
            p.key, p.prev.key = p.prev.key, p.key
            p = p.prev
        tmp = tmp.next


def tests(student):
    from adscb.primitives import DLList

    def _sorted_list(values):
        L = DLList.from_list(values)
        student(L)
        return L.to_list()

    def case_empty():
        L = DLList()
        student(L)
        assert L.head is None

    def case_single():
        assert _sorted_list([5]) == [5]

    def case_already_sorted():
        assert _sorted_list([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

    def case_reversed():
        assert _sorted_list([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

    def case_mixed():
        assert _sorted_list([3, 1, 4, 1, 5, 9, 2, 6]) == [1, 1, 2, 3, 4, 5, 6, 9]

    def case_duplicates():
        assert _sorted_list([2, 2, 2, 1, 1, 1]) == [1, 1, 1, 2, 2, 2]

    def case_negatives():
        assert _sorted_list([-3, 5, -1, 0, 2, -7]) == [-7, -3, -1, 0, 2, 5]

    def case_prev_pointers_intact():
        # keys should be sorted AND the prev chain should still walk back correctly
        L = DLList.from_list([4, 2, 3, 1])
        student(L)
        # walk to the last node, then walk back via .prev
        curr = L.head
        while curr.next is not None:
            curr = curr.next
        back = []
        while curr is not None:
            back.append(curr.key)
            curr = curr.prev
        assert back == [4, 3, 2, 1], \
            f"prev pointers should still link the sorted list; got reverse-walk {back}"

    return [
        ("empty list", case_empty),
        ("single node", case_single),
        ("already sorted", case_already_sorted),
        ("reverse sorted", case_reversed),
        ("mixed order", case_mixed),
        ("duplicates", case_duplicates),
        ("negatives and zero", case_negatives),
        ("prev pointers still valid after sort", case_prev_pointers_intact),
    ]

META = {
    "id": "ch04/06_sllist_delete_and_duplicate",
    "title": "Delete evens and duplicate remaining odds",
    "chapter": 4,
    "chapter_title": "Chapter 4 — Elementary Data Structures",
    "difficulty": 3,
    "requires_recursion": True,
    "entry": "delete_and_duplicate",
}

DESCRIPTION = """
# Delete evens and duplicate odds (Exercise 6)

Given the head of a singly linked list of integers, do two things in
one pass:

1. Remove every node whose key is **even**.
2. For each remaining **odd** node, **duplicate it** `nPrec` extra
   times, where `nPrec` is the total number of **even** nodes that
   appeared **before** it in the original list.

So if an odd node had 2 evens before it, it should appear 3 times
(itself + 2 copies) in the result.

## Signature

```python
def delete_and_duplicate(head):
    # head is an SLList.Node or None
    # returns the new head
    ...
```

## Example

    before: head → [4] → [6] → [7] → [3] → [2] → [5] → /

    Walkthrough:
      - 4 is even → nPrec becomes 1
      - 6 is even → nPrec becomes 2
      - 7 is odd, nPrec=2 → 7 appears 3 times total
      - 3 is odd, nPrec=2 → 3 appears 3 times total
      - 2 is even → nPrec becomes 3
      - 5 is odd, nPrec=3 → 5 appears 4 times total

    after: head → [7] → [7] → [7] → [3] → [3] → [3] → [5] → [5] → [5] → [5] → /

## Notes

- Recursive only (you may use a while loop inside a recursive case for the duplication step).
- This is a tricky one — take the hints slowly.
- Think of `nPrec` as a counter that gets threaded through the recursion.
"""

STARTER = '''\
from adscb.primitives import SLList


def delete_and_duplicate(head):
    """Remove evens, duplicate odds by count of preceding evens."""
    # hint: you'll want a helper with an extra parameter nPrec
    # your code here
    pass
'''

HINTS = [
    "You need a helper that takes (head, nPrec). Call it with nPrec=0 from delete_and_duplicate.",
    "If the current node is even: return helper(head.next, nPrec + 1) — the node is dropped and nPrec grows.",
    "If it's odd: first wire head.next = helper(head.next, nPrec) to process the rest, then prepend nPrec copies of the current key in front of head. Return the new front.",
]


def reference(head):
    def helper(h, nPrec):
        from adscb.primitives import SLList
        if h is None:
            return None
        if h.key % 2 == 0:
            return helper(h.next, nPrec + 1)
        h.next = helper(h.next, nPrec)
        # prepend nPrec copies of h.key before h
        for _ in range(nPrec):
            dup = SLList.Node(h.key)
            dup.next = h
            h = dup
        return h
    return helper(head, 0)


def tests(student):
    from adscb.primitives import SLList

    def case_empty():
        assert student(None) is None

    def case_pdf_example():
        L = SLList.from_list([4, 6, 7, 3, 2, 5])
        got = SLList.head_to_list(student(L.head))
        expected = [7, 7, 7, 3, 3, 3, 5, 5, 5, 5]
        assert got == expected, f"expected {expected}, got {got}"

    def case_all_even():
        L = SLList.from_list([2, 4, 6, 8])
        assert student(L.head) is None

    def case_all_odd_no_evens_before():
        # no evens anywhere → nPrec stays 0 → odds appear exactly once
        L = SLList.from_list([1, 3, 5, 7])
        got = SLList.head_to_list(student(L.head))
        assert got == [1, 3, 5, 7], f"with no preceding evens, odds stay as-is; got {got}"

    def case_evens_after_odds_only():
        # odds first, then evens: evens vanish, odds appear once (nPrec=0 when they were seen)
        L = SLList.from_list([1, 3, 2, 4])
        got = SLList.head_to_list(student(L.head))
        assert got == [1, 3], f"expected [1, 3], got {got}"

    def case_single_odd_with_one_even_before():
        L = SLList.from_list([2, 5])
        got = SLList.head_to_list(student(L.head))
        assert got == [5, 5], f"expected [5, 5], got {got}"

    def case_single_even():
        L = SLList.from_list([4])
        assert student(L.head) is None

    return [
        ("empty list", case_empty),
        ("PDF example [4,6,7,3,2,5]", case_pdf_example),
        ("all even → empty", case_all_even),
        ("all odd, no preceding evens", case_all_odd_no_evens_before),
        ("odds first then evens", case_evens_after_odds_only),
        ("one even + one odd", case_single_odd_with_one_even_before),
        ("single even node", case_single_even),
    ]

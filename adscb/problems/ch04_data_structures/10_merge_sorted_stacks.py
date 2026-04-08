META = {
    "id": "ch04/10_merge_sorted_stacks",
    "title": "Merge two sorted stacks into a third",
    "chapter": 4,
    "chapter_title": "Chapter 4 — Elementary Data Structures",
    "difficulty": 3,
    "requires_recursion": True,
    "entry": "merge_stacks",
}

DESCRIPTION = """
# Merge two sorted stacks (Exercise 10)

You are given two stacks `S1` and `S2`, each one **sorted with its
minimum element on top**. Fill a third, initially empty stack `S3`
so that all the elements from `S1` and `S2` end up in `S3` in order
from **largest to smallest** (i.e. `S3.peek()` is the overall minimum
at the end).

You may only use the stack operations `push`, `pop`, `peek`,
`is_empty`. **No loops** — do it recursively.

## Signature

```python
def merge_stacks(S1, S2, S3):
    # S1, S2 are sorted stacks (min on top)
    # S3 is empty; modify it in place
    # returns None
    ...
```

## Example

    S1 (top → bottom):  1, 3
    S2 (top → bottom):  2, 4

    After merge_stacks(S1, S2, S3):
    S3 (top → bottom):  1, 2, 3, 4     # min on top, sorted ascending reading top→bottom

## Complexity

Must run in O(n₁ + n₂) where n₁, n₂ are the sizes of S1 and S2.
Each element is popped from its source once and pushed into S3 once.

## Notes

- Recursive only. No `while` or `for` inside `merge_stacks`.
- Careful with the **order** of the push: the recursive call must
  happen **before** pushing the current element onto S3. That's how
  you get the smallest element on top.
"""

STARTER = '''\
from adscb.primitives import Stack


def merge_stacks(S1, S2, S3):
    """Merge sorted stacks S1 and S2 into empty stack S3 (min on top). Recursive."""
    # your code here
    pass
'''

HINTS = [
    "Base case: if both S1 and S2 are empty, do nothing — return.",
    "Otherwise pick which stack has the smaller top (careful if one is empty — treat empty as 'infinitely larger'). Pop it into a local variable x.",
    "Then recurse on merge_stacks(S1, S2, S3), and only AFTER the recursive call, push x onto S3. That ordering is what puts the smallest element on top.",
]


def reference(S1, S2, S3):
    if S1.is_empty() and S2.is_empty():
        return
    if S1.is_empty():
        x = S2.pop()
    elif S2.is_empty():
        x = S1.pop()
    elif S1.peek() <= S2.peek():
        x = S1.pop()
    else:
        x = S2.pop()
    reference(S1, S2, S3)
    S3.push(x)


def _sorted_stack(values_min_on_top, capacity=32):
    """Build a stack with the given values in the given top-to-bottom order.

    Example: _sorted_stack([1, 3, 5]) → S.peek() == 1, then 3, then 5 (bottom).
    """
    from adscb.primitives import Stack
    S = Stack(capacity)
    for v in reversed(values_min_on_top):  # push bottom first
        S.push(v)
    return S


def tests(student):
    from adscb.primitives import Stack

    def _run(s1_values, s2_values):
        """Return the values popped from S3 after the merge, top to bottom."""
        S1 = _sorted_stack(s1_values)
        S2 = _sorted_stack(s2_values)
        S3 = Stack(64)
        student(S1, S2, S3)
        out = []
        while not S3.is_empty():
            out.append(S3.pop())
        return out

    def case_both_empty():
        S1 = Stack(4); S2 = Stack(4); S3 = Stack(4)
        student(S1, S2, S3)
        assert S3.is_empty()

    def case_one_empty():
        assert _run([1, 3, 5], []) == [1, 3, 5]
        assert _run([], [2, 4, 6]) == [2, 4, 6]

    def case_simple_merge():
        assert _run([1, 3], [2, 4]) == [1, 2, 3, 4]

    def case_interleaved():
        assert _run([1, 4, 7], [2, 3, 8]) == [1, 2, 3, 4, 7, 8]

    def case_all_s1_smaller():
        assert _run([1, 2, 3], [10, 20, 30]) == [1, 2, 3, 10, 20, 30]

    def case_all_s2_smaller():
        assert _run([10, 20, 30], [1, 2, 3]) == [1, 2, 3, 10, 20, 30]

    def case_duplicates():
        assert _run([1, 2, 3], [1, 2, 3]) == [1, 1, 2, 2, 3, 3]

    def case_single_elements():
        assert _run([5], [3]) == [3, 5]

    return [
        ("both empty", case_both_empty),
        ("one empty", case_one_empty),
        ("simple merge", case_simple_merge),
        ("interleaved values", case_interleaved),
        ("all S1 smaller", case_all_s1_smaller),
        ("all S2 smaller", case_all_s2_smaller),
        ("duplicates across stacks", case_duplicates),
        ("single elements", case_single_elements),
    ]

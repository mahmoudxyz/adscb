META = {
    "id": "ch05/05_gentree_count_even",
    "title": "Count even-key nodes in a general tree",
    "chapter": 5,
    "chapter_title": "Chapter 5 — Trees",
    "difficulty": 2,
    "requires_recursion": True,
    "entry": "count_even",
}

DESCRIPTION = """
# Count even-key nodes in a general (non-binary) tree

The tree uses the **first-child / next-sibling** representation from
the slides. Each node has `.key`, `.first` (first child), `.next`
(next sibling).

Given the root of a general tree of integers, return the number of
nodes whose key is even.

## Signature

```python
def count_even(node):
    # node is a GenTree.Node or None
    # returns an int
    ...
```

## The recursion on first/next

With this representation, "visit the whole tree" means:

- Process this node
- **Recurse on `.first`** — that's "walk into this node's children"
- **Recurse on `.next`** — that's "walk to this node's siblings"

Both recursive calls must happen, and they behave the same way from
a counting perspective: each one visits a subtree of the whole tree.

## Example

    A tree with root=1 and children 2, 3, 4; 2 has children 5, 6:

        1
       /|\\
      2 3 4
     / \\
    5   6

    Even keys: 2, 4, 6 → count_even returns 3

## Notes

- Recursive, two-branch (on `.first` and on `.next`).
- Complexity: Θ(n) where n is the number of nodes.
"""

STARTER = '''\
from adscb.primitives import GenTree


def count_even(node):
    """Count nodes with even keys in a first/next general tree."""
    # your code here
    pass
'''

HINTS = [
    "Base case: if node is None, return 0.",
    "Otherwise compute: (1 if node.key is even else 0) + count_even(node.first) + count_even(node.next).",
    "Don't forget the recursion into .next — that's what walks siblings.",
]


def reference(node):
    if node is None:
        return 0
    here = 1 if node.key % 2 == 0 else 0
    return here + reference(node.first) + reference(node.next)


def tests(student):
    from adscb.primitives import GenTree

    def case_empty():
        assert student(None) == 0

    def case_single_even():
        T = GenTree.from_nested([4])
        assert student(T.root) == 1

    def case_single_odd():
        T = GenTree.from_nested([3])
        assert student(T.root) == 0

    def case_slide_example():
        # [1, [2, [5], [6]], [3], [4, [7]]]
        # nodes: 1, 2, 5, 6, 3, 4, 7
        # evens: 2, 6, 4 → 3
        T = GenTree.from_nested([1, [2, [5], [6]], [3], [4, [7]]])
        assert student(T.root) == 3

    def case_all_even():
        T = GenTree.from_nested([2, [4], [6, [8], [10]]])
        # 5 nodes all even
        assert student(T.root) == 5

    def case_all_odd():
        T = GenTree.from_nested([1, [3], [5, [7], [9]]])
        assert student(T.root) == 0

    def case_wide():
        # root 0 with 5 children: 1, 2, 3, 4, 5 → evens: 0, 2, 4 → 3
        T = GenTree.from_nested([0, [1], [2], [3], [4], [5]])
        assert student(T.root) == 3

    return [
        ("empty (None)", case_empty),
        ("single even node", case_single_even),
        ("single odd node", case_single_odd),
        ("slide-style example", case_slide_example),
        ("all even", case_all_even),
        ("all odd", case_all_odd),
        ("wide shallow tree", case_wide),
    ]

META = {
    "id": "ch05/02_sum_of_leaves",
    "title": "Sum of leaf keys in a binary tree",
    "chapter": 5,
    "chapter_title": "Chapter 5 — Trees",
    "difficulty": 1,
    "requires_recursion": True,
    "entry": "sum_leaves",
}

DESCRIPTION = """
# Sum of leaf keys

Given the root of a binary tree of integers, return the sum of the
keys of all **leaf** nodes. Empty tree returns 0.

## Signature

```python
def sum_leaves(root):
    # root is a BinTree.Node or None
    # returns an int
    ...
```

## Examples

         1               leaves: 4, 5, 3
        / \\              sum   = 12
       2   3
      / \\
     4   5

         7               leaves: 7
                         sum   = 7

         (empty)         sum   = 0

## Notes

- Recursive. Three-way case: None, leaf, internal.
- Complexity: Θ(n).
"""

STARTER = '''\
from adscb.primitives import BinTree


def sum_leaves(root):
    """Return the sum of keys at leaf nodes."""
    # your code here
    pass
'''

HINTS = [
    "Base: if root is None, return 0.",
    "Leaf check: if root.left is None and root.right is None, return root.key.",
    "Otherwise return sum_leaves(root.left) + sum_leaves(root.right).",
]


def reference(root):
    if root is None:
        return 0
    if root.left is None and root.right is None:
        return root.key
    return reference(root.left) + reference(root.right)


def tests(student):
    from adscb.primitives import BinTree

    def case_empty():
        assert student(None) == 0

    def case_single():
        T = BinTree.from_list([7])
        assert student(T.root) == 7

    def case_two_leaves():
        T = BinTree.from_list([1, 2, 3])
        assert student(T.root) == 5  # 2 + 3

    def case_slide_example():
        T = BinTree.from_list([1, 2, 3, 4, 5])
        assert student(T.root) == 12  # 4 + 5 + 3

    def case_negative_keys():
        T = BinTree.from_list([0, -1, -2, 5, -5])
        # leaves: 5, -5, -2 → sum 5 - 5 - 2 = -2
        assert student(T.root) == -2

    def case_left_chain():
        # 1→2→3→4, only 4 is a leaf
        T = BinTree.from_list([1, 2, None, 3, None, 4])
        assert student(T.root) == 4

    def case_big():
        T = BinTree.from_list(list(range(1, 16)))  # complete tree 1..15
        # leaves are 8..15 → sum = 8+9+...+15 = 92
        assert student(T.root) == 92

    return [
        ("empty tree", case_empty),
        ("single node (is a leaf)", case_single),
        ("root + 2 leaves", case_two_leaves),
        ("slide example", case_slide_example),
        ("negative keys", case_negative_keys),
        ("left chain", case_left_chain),
        ("complete tree 1..15", case_big),
    ]

META = {
    "id": "ch05/04_tree_height",
    "title": "Height of a binary tree",
    "chapter": 5,
    "chapter_title": "Chapter 5 — Trees",
    "difficulty": 1,
    "requires_recursion": True,
    "entry": "height",
}

DESCRIPTION = """
# Height of a binary tree

Compute the **height** of a binary tree using the slide convention:

- Empty tree → height `-1`
- Single-node tree (root only) → height `0`
- Otherwise → `1 + max(height(left), height(right))`

## Signature

```python
def height(root):
    # root is a BinTree.Node or None
    # returns an int (−1 for empty)
    ...
```

## Examples

    (empty)    →  -1

    7          →   0

        1      →   1
       / \\
      2   3

        1      →   2
       / \\
      2   3
       \\
        4

## Notes

- Recursive. The formula is the entire solution.
- Complexity: Θ(n).
- Don't confuse "height" with "depth". Height of a NODE is the length
  of the longest path down to a leaf; height of the TREE is the
  height of the root. Depth is the distance from the root.
"""

STARTER = '''\
from adscb.primitives import BinTree


def height(root):
    """Height of the binary tree. -1 for empty, 0 for a single node."""
    # your code here
    pass
'''

HINTS = [
    "Base case: if root is None, return -1.",
    "Recursive case: return 1 + max(height(root.left), height(root.right)).",
    "Two lines. That's all.",
]


def reference(root):
    if root is None:
        return -1
    return 1 + max(reference(root.left), reference(root.right))


def tests(student):
    from adscb.primitives import BinTree

    def case_empty():
        assert student(None) == -1

    def case_single():
        T = BinTree.from_list([1])
        assert student(T.root) == 0

    def case_two_level():
        T = BinTree.from_list([1, 2, 3])
        assert student(T.root) == 1

    def case_three_level_balanced():
        T = BinTree.from_list([1, 2, 3, 4, 5, 6, 7])
        assert student(T.root) == 2

    def case_left_chain():
        #  1→2→3→4  (each is the left child of its parent)
        T = BinTree.from_list([1, 2, None, 3, None, 4])
        assert student(T.root) == 3

    def case_right_chain():
        T = BinTree.from_list([1, None, 2, None, 3, None, 4])
        assert student(T.root) == 3

    def case_lopsided():
        #        1
        #       / \
        #      2   3
        #     /
        #    4
        #   /
        #  5
        T = BinTree.from_list([1, 2, 3, 4, None, None, None, 5])
        assert student(T.root) == 3

    return [
        ("empty tree → -1", case_empty),
        ("single node → 0", case_single),
        ("two-level balanced → 1", case_two_level),
        ("three-level balanced → 2", case_three_level_balanced),
        ("left chain", case_left_chain),
        ("right chain", case_right_chain),
        ("lopsided tree", case_lopsided),
    ]

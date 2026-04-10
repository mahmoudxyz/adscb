META = {
    "id": "ch05/01_remove_leaves",
    "title": "Remove all leaves from a binary tree",
    "chapter": 5,
    "chapter_title": "Chapter 5 — Trees",
    "difficulty": 2,
    "requires_recursion": True,
    "entry": "remove_leaves",
}

DESCRIPTION = """
# Remove all leaves from a binary tree

Given the root of a binary tree, return the root after removing
**every leaf node** (a leaf is a node with no children). If the
result has no nodes, return `None`.

## Signature

```python
def remove_leaves(root):
    # root is a BinTree.Node or None
    # returns the new root after leaves are removed
    ...
```

## Example

    before:          1              after:      1
                   /   \\                       /
                  2     3                      2
                 / \\
                4   5

    (4 and 5 are leaves → removed. Then 2 still has... wait, 2 no
    longer has children after removal, but 2 was NOT a leaf in the
    original tree. Only leaves of the *original* tree get removed.
    Be careful: don't cascade.)

Actually let me be precise: **only leaves of the original tree are
removed**. A node that becomes a leaf as a consequence of the removal
stays.

    original:   1              output:    1
               / \\                        /
              2   3                       2
             / \\
            4   5

    So: 4, 5, 3 are leaves → removed. 2 is not a leaf originally,
    so 2 stays (even though it becomes a leaf after the removal).

## Notes

- Recursive solution. Base case: if the node is `None` or a leaf → return `None`.
- Otherwise recurse on `.left` and `.right` and rewire.
- Complexity: Θ(n).
"""

STARTER = '''\
from adscb.primitives import BinTree


def remove_leaves(root):
    """Return the root after removing all leaves of the ORIGINAL tree."""
    # your code here
    pass
'''

HINTS = [
    "Base case: if root is None or (root.left is None and root.right is None), return None.",
    "Recursive case: root.left = remove_leaves(root.left); root.right = remove_leaves(root.right); return root.",
    "That's the whole function — four or five lines total.",
]


def reference(root):
    if root is None:
        return None
    if root.left is None and root.right is None:
        return None
    root.left = reference(root.left)
    root.right = reference(root.right)
    return root


def tests(student):
    from adscb.primitives import BinTree

    def case_empty():
        assert student(None) is None

    def case_single_leaf():
        T = BinTree.from_list([1])
        assert student(T.root) is None

    def case_one_level():
        # root with two leaf children → both children removed, root stays
        T = BinTree.from_list([1, 2, 3])
        new_root = student(T.root)
        result = BinTree(new_root).to_list()
        assert result == [1], f"expected [1], got {result}"

    def case_two_levels():
        #       1
        #      / \
        #     2   3
        #    / \
        #   4   5
        # leaves: 4, 5, 3 → removed
        T = BinTree.from_list([1, 2, 3, 4, 5])
        result = BinTree(student(T.root)).to_list()
        assert result == [1, 2], f"expected [1, 2], got {result}"

    def case_left_chain():
        # all-left spine — only the deepest node is a leaf
        T = BinTree.from_list([1, 2, None, 3, None, 4])
        result = BinTree(student(T.root)).to_list()
        assert result == [1, 2, None, 3], f"expected [1, 2, None, 3], got {result}"

    def case_mixed():
        T = BinTree.from_list([1, 2, 3, None, 4, 5, None, None, 6])
        # leaves of original: 6's parent is 4, 5 is a leaf. Let me think:
        # level-order: 1(2,3), 2(None,4), 3(5,None), 4(None,6), 5 has no children, 6 has no children
        # original leaves: 5, 6.
        # after removal: 1(2,3), 2(None,4), 3(None,None), 4(None,None)
        # to_list drops trailing Nones: [1, 2, 3, None, 4]
        result = BinTree(student(T.root)).to_list()
        assert result == [1, 2, 3, None, 4], f"got {result}"

    return [
        ("empty tree", case_empty),
        ("single leaf (root only)", case_single_leaf),
        ("root with two leaf children", case_one_level),
        ("two-level tree", case_two_levels),
        ("left-chain tree", case_left_chain),
        ("mixed structure", case_mixed),
    ]

META = {
    "id": "ch05/03_prune_left_duplicates",
    "title": "Remove left-child leaves equal to their parent",
    "chapter": 5,
    "chapter_title": "Chapter 5 — Trees",
    "difficulty": 2,
    "requires_recursion": True,
    "entry": "prune",
}

DESCRIPTION = """
# Prune left-child leaves matching the parent

Given the root of a binary tree, remove every node that satisfies
**all three** of these conditions:

1. It is a **left** child of some node
2. It is a **leaf** (no children)
3. Its key equals its parent's key

Return the (possibly new) root. The tree should be modified in place.

## Signature

```python
def prune(root):
    # root is a BinTree.Node or None
    # returns the (possibly same) root
    ...
```

## Example

           5                         5
          / \\                        \\
         5   7             →          7
              \\                        \\
               7                        7

    (The left-child 5 is a leaf and matches its parent 5 → removed.
    Right-child 7 is a leaf but it's a *right* child, so it stays.)

## Notes

- Recursive.
- Per the slides: check the condition **before** recursing, or you'll
  handle the subtree wrong.
- Complexity: Θ(n).
"""

STARTER = '''\
from adscb.primitives import BinTree


def prune(root):
    """Remove left-child leaves that equal their parent's key. Return root."""
    # your code here
    pass
'''

HINTS = [
    "Base case: if root is None, return None.",
    "Check the left child: if root.left is not None and it's a leaf and root.left.key == root.key, set root.left = None.",
    "Then recurse: prune(root.left) and prune(root.right). Return root.",
]


def reference(root):
    if root is None:
        return None
    if (root.left is not None
            and root.left.left is None
            and root.left.right is None
            and root.left.key == root.key):
        root.left = None
    reference(root.left)
    reference(root.right)
    return root


def tests(student):
    from adscb.primitives import BinTree

    def case_empty():
        assert student(None) is None

    def case_single():
        T = BinTree.from_list([5])
        r = student(T.root)
        assert BinTree(r).to_list() == [5]

    def case_slide_example():
        #        5
        #       / \
        #      5   7
        #           \
        #            7
        T = BinTree.from_list([5, 5, 7, None, None, None, 7])
        r = student(T.root)
        result = BinTree(r).to_list()
        # left 5 gets pruned; right-child 7 with its own right child 7 stays
        assert result == [5, None, 7, None, 7], f"got {result}"

    def case_right_leaf_matching_stays():
        #    5
        #     \
        #      5
        T = BinTree.from_list([5, None, 5])
        r = student(T.root)
        assert BinTree(r).to_list() == [5, None, 5]

    def case_left_leaf_not_matching_stays():
        #    5
        #   /
        #  3
        T = BinTree.from_list([5, 3])
        r = student(T.root)
        assert BinTree(r).to_list() == [5, 3]

    def case_left_non_leaf_matching_stays():
        # left child has the same key but has its own child → NOT a leaf → stays
        #     5
        #    /
        #   5
        #    \
        #     1
        T = BinTree.from_list([5, 5, None, None, 1])
        r = student(T.root)
        assert BinTree(r).to_list() == [5, 5, None, None, 1]

    def case_deep_recursion():
        #         1
        #        / \
        #       1   2
        #          / \
        #         2   9
        # left child 1 is a leaf matching parent 1 → removed
        # left child of 2 is a leaf matching parent 2 → removed
        T = BinTree.from_list([1, 1, 2, None, None, 2, 9])
        r = student(T.root)
        result = BinTree(r).to_list()
        assert result == [1, None, 2, None, 9], f"got {result}"

    return [
        ("empty tree", case_empty),
        ("single node", case_single),
        ("slide-style example", case_slide_example),
        ("matching right leaf stays", case_right_leaf_matching_stays),
        ("non-matching left leaf stays", case_left_leaf_not_matching_stays),
        ("matching but non-leaf left child stays", case_left_non_leaf_matching_stays),
        ("recursion into deeper subtrees", case_deep_recursion),
    ]

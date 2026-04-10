META = {
    "id": "ch05/23_mirror_tree",
    "title": "Mirror (invert) a binary tree",
    "chapter": 5,
    "chapter_title": "Chapter 5 — Trees",
    "difficulty": 1,
    "requires_recursion": True,
    "entry": "mirror",
}

DESCRIPTION = """
# Mirror a binary tree

Given the root of a binary tree, return the tree with left and
right children swapped **at every node**. Modify in place and
return the (same) root.

## Signature

```python
def mirror(root):
    # root is a BinTree.Node or None
    # returns the same root, modified
    ...
```

## Example

         1              1
        / \\            / \\
       2   3    →      3   2
      / \\   \\         /   / \\
     4   5   6       6   5   4

## Notes

- Recursive. One of the shortest recursive tree algorithms.
- Complexity: Θ(n).
"""

STARTER = '''\
from adscb.primitives import BinTree


def mirror(root):
    """Swap left and right subtrees at every node. Return root."""
    # your code here
    pass
'''

HINTS = [
    "Base case: if root is None, return None.",
    "Swap root.left and root.right.",
    "Recurse into BOTH subtrees (now in their new positions) and return root.",
]


def reference(root):
    if root is None:
        return None
    root.left, root.right = root.right, root.left
    reference(root.left)
    reference(root.right)
    return root


def tests(student):
    from adscb.primitives import BinTree

    def case_empty():
        assert student(None) is None

    def case_single():
        T = BinTree.from_list([1])
        r = student(T.root)
        assert BinTree(r).to_list() == [1]

    def case_two_level():
        T = BinTree.from_list([1, 2, 3])
        r = student(T.root)
        assert BinTree(r).to_list() == [1, 3, 2]

    def case_three_level():
        T = BinTree.from_list([1, 2, 3, 4, 5, 6, 7])
        r = student(T.root)
        # full tree mirrored: [1, 3, 2, 7, 6, 5, 4]
        assert BinTree(r).to_list() == [1, 3, 2, 7, 6, 5, 4]

    def case_double_mirror_is_identity():
        original = [1, 2, 3, None, 4, 5, None, None, 6]
        T = BinTree.from_list(original)
        student(T.root)
        student(T.root)
        assert BinTree(T.root).to_list() == original

    def case_left_chain_to_right_chain():
        # [1, 2, None, 3, None, 4]  →  [1, None, 2, None, 3, None, 4]
        T = BinTree.from_list([1, 2, None, 3, None, 4])
        student(T.root)
        assert BinTree(T.root).to_list() == [1, None, 2, None, 3, None, 4]

    return [
        ("empty tree", case_empty),
        ("single node", case_single),
        ("two-level tree", case_two_level),
        ("three-level complete", case_three_level),
        ("mirror twice = identity", case_double_mirror_is_identity),
        ("left chain becomes right chain", case_left_chain_to_right_chain),
    ]

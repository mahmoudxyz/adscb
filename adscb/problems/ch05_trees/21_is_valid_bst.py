META = {
    "id": "ch05/21_is_valid_bst",
    "title": "Is this tree a valid BST?",
    "chapter": 5,
    "chapter_title": "Chapter 5 — Trees",
    "difficulty": 3,
    "requires_recursion": True,
    "entry": "is_bst",
}

DESCRIPTION = """
# Is this tree a valid BST?

Given a binary tree, decide whether it satisfies the BST property:
for every node `v`, **every key in the left subtree** is ≤ `v.key`,
and **every key in the right subtree** is ≥ `v.key`. Return `True`
or `False`.

## Signature

```python
def is_bst(root):
    # root is a BinTree.Node or None
    # returns True or False
    ...
```

## The classic trap

The obvious-looking solution is:

```python
# WRONG — this only checks immediate children
def is_bst(root):
    if root is None: return True
    if root.left and root.left.key > root.key: return False
    if root.right and root.right.key < root.key: return False
    return is_bst(root.left) and is_bst(root.right)
```

This fails on:

         10
        /  \\
       5    15
            / \\
           6   20

Every immediate-child check passes (6 < 15), but 6 is in the right
subtree of 10 and 6 < 10 — that's a BST violation.

## The fix

Pass **bounds** down the recursion. At each node you know the
allowed range `(lo, hi)` for its key; the left recurse tightens
`hi` to the current key and the right recurse tightens `lo` to the
current key.

## Examples

         5                   valid BST
        / \\
       3   8
      / \\
     1   4

         10                  NOT a BST (6 is in 10's right subtree but 6 < 10)
        /  \\
       5    15
            / \\
           6   20

## Notes

- Recursive with a bounds helper.
- Use `float('-inf')` and `float('inf')` as initial bounds, or pass
  `None` and handle the None case.
- Complexity: Θ(n).
- For this problem, treat equal keys as allowed on either side —
  a stricter version requires strict inequality, but the slides use ≤.
"""

STARTER = '''\
from adscb.primitives import BinTree


def is_bst(root):
    """Return True iff `root` is a valid BST."""
    # your code here
    pass
'''

HINTS = [
    "Define a helper check(node, lo, hi) that returns True iff every key in the subtree is within [lo, hi].",
    "Call check(root, -inf, +inf) from the outer function.",
    "In the helper: None → True. Otherwise: lo <= node.key <= hi, and check(node.left, lo, node.key) and check(node.right, node.key, hi).",
]


def reference(root):
    def check(node, lo, hi):
        if node is None:
            return True
        if not (lo <= node.key <= hi):
            return False
        return check(node.left, lo, node.key) and check(node.right, node.key, hi)
    return check(root, float("-inf"), float("inf"))


def tests(student):
    from adscb.primitives import BinTree

    def case_empty():
        assert student(None) is True

    def case_single():
        T = BinTree.from_list([42])
        assert student(T.root) is True

    def case_valid_small():
        T = BinTree.from_list([5, 3, 8])
        assert student(T.root) is True

    def case_valid_deeper():
        T = BinTree.from_list([5, 3, 8, 1, 4, 7, 9])
        assert student(T.root) is True

    def case_invalid_immediate_left():
        # left child larger than parent
        T = BinTree.from_list([5, 10, 15])
        assert student(T.root) is False

    def case_invalid_immediate_right():
        T = BinTree.from_list([5, 3, 2])
        assert student(T.root) is False

    def case_classic_trap():
        # root 10, right subtree has 15 with left child 6 → 6 < 10 is a violation
        T = BinTree.from_list([10, 5, 15, None, None, 6, 20])
        assert student(T.root) is False, \
            "the left child of 15 is 6, which is in 10's right subtree but 6 < 10"

    def case_left_subtree_trap():
        # symmetric: root 10, left subtree has 5 with right child 12 → 12 > 10 violates
        T = BinTree.from_list([10, 5, 15, 3, 12])
        assert student(T.root) is False

    def case_equal_keys_allowed():
        # the slides allow equal keys on both sides; a chain 5 - 5 - 5 is technically valid
        T = BinTree.from_list([5, 5])
        assert student(T.root) is True

    return [
        ("empty tree", case_empty),
        ("single node", case_single),
        ("valid small BST", case_valid_small),
        ("valid 7-node BST", case_valid_deeper),
        ("left child > parent (invalid)", case_invalid_immediate_left),
        ("right child < parent (invalid)", case_invalid_immediate_right),
        ("the classic bounds trap", case_classic_trap),
        ("symmetric bounds trap (left subtree)", case_left_subtree_trap),
        ("equal keys allowed", case_equal_keys_allowed),
    ]

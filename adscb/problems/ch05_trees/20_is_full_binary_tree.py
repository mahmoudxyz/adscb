META = {
    "id": "ch05/20_is_full_binary_tree",
    "title": "Is this binary tree full?",
    "chapter": 5,
    "chapter_title": "Chapter 5 — Trees",
    "difficulty": 2,
    "requires_recursion": True,
    "entry": "is_full",
}

DESCRIPTION = """
# Full binary tree check

A **full** binary tree is a binary tree where every node has either
**0 or 2 children**. An empty tree counts as full.

Return `True` if the given tree is full, `False` otherwise.

## Signature

```python
def is_full(root):
    # root is a BinTree.Node or None
    # returns True or False
    ...
```

## Examples

         1        full      →  True
        / \\
       2   3

         1        not full  →  False   (root has only left child)
        /
       2

         1        full      →  True
        / \\
       2   3
      / \\
     4   5

         1        not full  →  False   (node 2 has only one child)
        / \\
       2   3
        \\
         4

## Why this problem

This one was on the **2022 June 24 final exam** worth 7 points.
Knowing how to write it cold is table stakes.

## Notes

- Recursive. Three cases: None, leaf (0 children), internal (2
  children). Anything with 1 child means not full.
- Complexity: Θ(n).
"""

STARTER = '''\
from adscb.primitives import BinTree


def is_full(root):
    """Return True if every node has 0 or 2 children."""
    # your code here
    pass
'''

HINTS = [
    "Base case: if root is None → True. If root is a leaf (both children None) → True.",
    "If exactly one child is None → False.",
    "Otherwise both children exist: recurse on both and return the AND.",
]


def reference(root):
    if root is None:
        return True
    if root.left is None and root.right is None:
        return True
    if root.left is None or root.right is None:
        return False
    return reference(root.left) and reference(root.right)


def tests(student):
    from adscb.primitives import BinTree

    def case_empty():
        assert student(None) is True

    def case_single():
        T = BinTree.from_list([1])
        assert student(T.root) is True

    def case_two_children():
        T = BinTree.from_list([1, 2, 3])
        assert student(T.root) is True

    def case_left_only():
        T = BinTree.from_list([1, 2])
        assert student(T.root) is False

    def case_right_only():
        T = BinTree.from_list([1, None, 2])
        assert student(T.root) is False

    def case_full_deeper():
        T = BinTree.from_list([1, 2, 3, 4, 5])
        assert student(T.root) is True

    def case_not_full_due_to_grandchild():
        # root has two children (good), but left child has only one child
        T = BinTree.from_list([1, 2, 3, None, 4])
        assert student(T.root) is False

    def case_complete_tree():
        T = BinTree.from_list([1, 2, 3, 4, 5, 6, 7])
        assert student(T.root) is True

    return [
        ("empty tree", case_empty),
        ("single node (leaf)", case_single),
        ("root + 2 children", case_two_children),
        ("root + left only", case_left_only),
        ("root + right only", case_right_only),
        ("full deeper tree", case_full_deeper),
        ("not full due to grandchild", case_not_full_due_to_grandchild),
        ("complete 7-node tree", case_complete_tree),
    ]

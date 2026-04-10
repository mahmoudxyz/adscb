META = {
    "id": "ch05/24_lowest_common_ancestor",
    "title": "Lowest common ancestor in a binary tree",
    "chapter": 5,
    "chapter_title": "Chapter 5 — Trees",
    "difficulty": 3,
    "requires_recursion": True,
    "entry": "lca",
}

DESCRIPTION = """
# Lowest common ancestor (LCA)

Given the root of a binary tree and two nodes `p` and `q` that are
guaranteed to exist in the tree, return the lowest node that is an
ancestor of **both** `p` and `q`. A node is considered its own
ancestor.

## Signature

```python
def lca(root, p, q):
    # root, p, q are BinTree.Node
    # returns a BinTree.Node
    ...
```

## Example

         3
        / \\
       5   1
      / \\ / \\
     6  2 0  8
       / \\
      7   4

    lca(root, 5, 1)  →  3   (root is their only common ancestor)
    lca(root, 5, 4)  →  5   (5 is ancestor of itself and contains 4)
    lca(root, 7, 4)  →  2   (deepest node containing both)
    lca(root, 6, 7)  →  5

## The algorithm

The classic recursive solution doesn't need parent pointers:

- If `root` is `None` → return `None`.
- If `root` is `p` or `q` → return `root` (found one side).
- Recurse on left and right subtrees.
- If **both** recursive calls return non-None, `root` itself is the
  LCA (one target is in each subtree).
- Otherwise return whichever side found something (or `None`).

## Complexity

Θ(n) — each node is visited at most once.
"""

STARTER = '''\
from adscb.primitives import BinTree


def lca(root, p, q):
    """Lowest common ancestor of p and q in the tree rooted at root."""
    # your code here
    pass
'''

HINTS = [
    "Base cases: if root is None or root is p or root is q, return root.",
    "Recurse: left = lca(root.left, p, q); right = lca(root.right, p, q).",
    "If both left and right are non-None, root itself is the LCA. Otherwise return whichever is non-None (or None).",
]


def reference(root, p, q):
    if root is None or root is p or root is q:
        return root
    left = reference(root.left, p, q)
    right = reference(root.right, p, q)
    if left is not None and right is not None:
        return root
    return left if left is not None else right


def _find(root, key):
    """Helper for tests: locate a node by key (first match, pre-order)."""
    if root is None:
        return None
    if root.key == key:
        return root
    return _find(root.left, key) or _find(root.right, key)


def tests(student):
    from adscb.primitives import BinTree

    def case_root_is_lca():
        T = BinTree.from_list([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
        p = _find(T.root, 5)
        q = _find(T.root, 1)
        assert student(T.root, p, q).key == 3

    def case_one_is_ancestor_of_other():
        T = BinTree.from_list([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
        p = _find(T.root, 5)
        q = _find(T.root, 4)
        assert student(T.root, p, q).key == 5

    def case_deep_common_ancestor():
        T = BinTree.from_list([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
        p = _find(T.root, 7)
        q = _find(T.root, 4)
        assert student(T.root, p, q).key == 2

    def case_siblings():
        T = BinTree.from_list([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
        p = _find(T.root, 6)
        q = _find(T.root, 7)
        assert student(T.root, p, q).key == 5

    def case_single_node_self():
        T = BinTree.from_list([42])
        assert student(T.root, T.root, T.root).key == 42

    def case_linear_tree():
        T = BinTree.from_list([1, 2, None, 3, None, 4])
        p = _find(T.root, 3)
        q = _find(T.root, 4)
        assert student(T.root, p, q).key == 3

    return [
        ("root is the LCA", case_root_is_lca),
        ("one node is ancestor of the other", case_one_is_ancestor_of_other),
        ("deep common ancestor", case_deep_common_ancestor),
        ("siblings share parent as LCA", case_siblings),
        ("single-node tree, p == q == root", case_single_node_self),
        ("linear chain", case_linear_tree),
    ]

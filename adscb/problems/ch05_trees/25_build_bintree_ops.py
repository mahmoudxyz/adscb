META = {
    "id": "ch05/25_build_bintree_ops",
    "title": "Build it yourself — BinTree operations from scratch",
    "chapter": 5,
    "chapter_title": "Chapter 5 — Trees",
    "difficulty": 2,
    "requires_recursion": True,
    "entry": "build",
}

DESCRIPTION = """
# Build it yourself: binary tree operations

Implement four small operations on raw `BinTree.Node` objects.
You're given a tree made of nodes with `.key`, `.left`, `.right`,
`.parent`. Write the operations using recursion only — no helper
methods from the `BinTree` class.

## What you write

```python
def build():
    def count_nodes(root):
        # total number of nodes
        ...

    def count_leaves(root):
        # number of leaf nodes
        ...

    def depth(node):
        # depth of `node` from the root (root has depth 0)
        # assumes .parent pointers are valid; walks up
        ...

    def contains(root, k):
        # True iff the tree has a node with key == k
        ...

    return count_nodes, count_leaves, depth, contains
```

## Notes

- Feel free to recurse for count_nodes, count_leaves, and contains.
- For `depth`, you can either walk up via `.parent` iteratively, or
  recurse down from the root — the slides do both. Walking up is
  simpler if you assume parents are set.
- All four should be Θ(n) worst case.
- Don't import traversal helpers from BinTree — write the logic.
"""

STARTER = '''\
from adscb.primitives import BinTree


def build():
    def count_nodes(root):
        # your code here
        pass

    def count_leaves(root):
        pass

    def depth(node):
        pass

    def contains(root, k):
        pass

    return count_nodes, count_leaves, depth, contains
'''

HINTS = [
    "count_nodes: base None → 0; else 1 + count(left) + count(right).",
    "count_leaves: base None → 0; leaf (both children None) → 1; else count_leaves(left) + count_leaves(right).",
    "depth: walk up via node.parent, counting steps, until you hit a node whose .parent is None.",
    "contains: None → False; root.key == k → True; else contains(left) or contains(right).",
]


def reference():
    def count_nodes(root):
        if root is None:
            return 0
        return 1 + count_nodes(root.left) + count_nodes(root.right)

    def count_leaves(root):
        if root is None:
            return 0
        if root.left is None and root.right is None:
            return 1
        return count_leaves(root.left) + count_leaves(root.right)

    def depth(node):
        d = 0
        while node is not None and node.parent is not None:
            d += 1
            node = node.parent
        return d

    def contains(root, k):
        if root is None:
            return False
        if root.key == k:
            return True
        return contains(root.left, k) or contains(root.right, k)

    return count_nodes, count_leaves, depth, contains


def _find(node, key):
    if node is None:
        return None
    if node.key == key:
        return node
    return _find(node.left, key) or _find(node.right, key)


def tests(student):
    from adscb.primitives import BinTree

    def case_returns_four():
        result = student()
        assert len(result) == 4 and all(callable(f) for f in result)

    def case_count_nodes():
        cn, _, _, _ = student()
        assert cn(None) == 0
        assert cn(BinTree.from_list([1]).root) == 1
        assert cn(BinTree.from_list([1, 2, 3, 4, 5]).root) == 5
        assert cn(BinTree.from_list([1, 2, 3, 4, 5, 6, 7]).root) == 7

    def case_count_leaves():
        _, cl, _, _ = student()
        assert cl(None) == 0
        assert cl(BinTree.from_list([1]).root) == 1
        # [1, 2, 3] → leaves: 2, 3 → 2
        assert cl(BinTree.from_list([1, 2, 3]).root) == 2
        # [1, 2, 3, 4, 5] → leaves: 4, 5, 3 → 3
        assert cl(BinTree.from_list([1, 2, 3, 4, 5]).root) == 3
        # left chain → only the last node is a leaf
        assert cl(BinTree.from_list([1, 2, None, 3, None, 4]).root) == 1

    def case_depth():
        _, _, dpt, _ = student()
        T = BinTree.from_list([1, 2, 3, 4, 5, 6, 7])
        # root depth 0, children depth 1, grandchildren depth 2
        assert dpt(T.root) == 0
        assert dpt(_find(T.root, 2)) == 1
        assert dpt(_find(T.root, 3)) == 1
        assert dpt(_find(T.root, 7)) == 2

    def case_depth_deep():
        _, _, dpt, _ = student()
        T = BinTree.from_list([1, 2, None, 3, None, 4, None, 5])
        assert dpt(_find(T.root, 5)) == 4

    def case_contains():
        _, _, _, cnt = student()
        assert cnt(None, 5) is False
        T = BinTree.from_list([1, 2, 3, 4, 5, 6, 7])
        assert cnt(T.root, 1) is True
        assert cnt(T.root, 7) is True
        assert cnt(T.root, 4) is True
        assert cnt(T.root, 99) is False

    return [
        ("build() returns four callables", case_returns_four),
        ("count_nodes", case_count_nodes),
        ("count_leaves", case_count_leaves),
        ("depth via .parent walk", case_depth),
        ("depth on a deeper tree", case_depth_deep),
        ("contains", case_contains),
    ]

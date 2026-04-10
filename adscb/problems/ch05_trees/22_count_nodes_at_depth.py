META = {
    "id": "ch05/22_count_nodes_at_depth",
    "title": "Count nodes at a given depth",
    "chapter": 5,
    "chapter_title": "Chapter 5 — Trees",
    "difficulty": 2,
    "requires_recursion": True,
    "entry": "count_at_depth",
}

DESCRIPTION = """
# Count nodes at depth k

Given a binary tree and a non-negative integer `k`, return the
number of nodes at depth exactly `k` (where the root is at depth 0).

## Signature

```python
def count_at_depth(root, k):
    # root is a BinTree.Node or None
    # k is a non-negative int
    # returns an int
    ...
```

## Examples

         1
        / \\
       2   3          depth 0: 1 node (root)
      / \\             depth 1: 2 nodes (2, 3)
     4   5            depth 2: 2 nodes (4, 5)
                      depth 3: 0 nodes
                      depth 99: 0 nodes

## Notes

- Recursive. Decrement `k` as you descend.
- Complexity: Θ(n) worst case (you might traverse the whole tree).
"""

STARTER = '''\
from adscb.primitives import BinTree


def count_at_depth(root, k):
    """Count nodes at depth exactly k (root has depth 0)."""
    # your code here
    pass
'''

HINTS = [
    "Base case: if root is None → 0. If k == 0 → 1 (the current node).",
    "Recursive case: count_at_depth(root.left, k - 1) + count_at_depth(root.right, k - 1).",
    "Think of k as 'steps remaining to the target depth'. When it hits 0, you're there.",
]


def reference(root, k):
    if root is None:
        return 0
    if k == 0:
        return 1
    return reference(root.left, k - 1) + reference(root.right, k - 1)


def tests(student):
    from adscb.primitives import BinTree

    def case_empty():
        assert student(None, 0) == 0
        assert student(None, 5) == 0

    def case_single_depth_0():
        T = BinTree.from_list([1])
        assert student(T.root, 0) == 1
        assert student(T.root, 1) == 0

    def case_complete_3_levels():
        T = BinTree.from_list([1, 2, 3, 4, 5, 6, 7])
        assert student(T.root, 0) == 1
        assert student(T.root, 1) == 2
        assert student(T.root, 2) == 4
        assert student(T.root, 3) == 0

    def case_left_chain():
        # 1→2→3→4
        T = BinTree.from_list([1, 2, None, 3, None, 4])
        assert student(T.root, 0) == 1
        assert student(T.root, 1) == 1
        assert student(T.root, 2) == 1
        assert student(T.root, 3) == 1
        assert student(T.root, 4) == 0

    def case_sparse():
        #         1
        #        / \
        #       2   3
        #          / \
        #         4   5
        T = BinTree.from_list([1, 2, 3, None, None, 4, 5])
        assert student(T.root, 0) == 1
        assert student(T.root, 1) == 2
        assert student(T.root, 2) == 2  # 4 and 5
        assert student(T.root, 3) == 0

    def case_beyond_height():
        T = BinTree.from_list([1, 2, 3])
        assert student(T.root, 100) == 0

    return [
        ("empty tree, any k", case_empty),
        ("single node", case_single_depth_0),
        ("complete 3-level tree", case_complete_3_levels),
        ("left chain", case_left_chain),
        ("sparse tree", case_sparse),
        ("k beyond tree height", case_beyond_height),
    ]

META = {
    "id": "ch05/12_bst_min_max_pred_succ",
    "title": "BST min, max, predecessor, successor",
    "chapter": 5,
    "chapter_title": "Chapter 5 — Trees",
    "difficulty": 2,
    "requires_recursion": False,
    "entry": "solve",
}

DESCRIPTION = """
# BST min, max, predecessor, successor

Four small operations on a BST that all work on node references
(not keys). The classic slide material — write all four.

## What you write

```python
def solve():
    def bst_min(node):
        # minimum of the subtree rooted at `node` (leftmost descendant)
        ...

    def bst_max(node):
        # maximum of the subtree rooted at `node` (rightmost descendant)
        ...

    def bst_predecessor(node):
        # in-order predecessor of `node`, or None if it's the minimum
        ...

    def bst_successor(node):
        # in-order successor of `node`, or None if it's the maximum
        ...

    return bst_min, bst_max, bst_predecessor, bst_successor
```

## The rules

- **`bst_min`**: walk left until `.left` is None. Return that node.
- **`bst_max`**: walk right until `.right` is None.
- **`bst_predecessor(v)`**: two cases:
  1. If `v.left` is not None, predecessor is `bst_max(v.left)`.
  2. Otherwise walk up via `.parent` until you come from the **right**.
     That ancestor is the predecessor. (If you run out of ancestors,
     there's no predecessor — return None.)
- **`bst_successor(v)`**: symmetric to predecessor. `v.right` → min
  of right subtree, otherwise walk up until you come from the left.

## Complexity

All four are Θ(h) worst case, O(1) best case.

## Notes

- All operations work on raw nodes and rely on `.parent` being set.
- The `BST` primitive has these methods built in — don't use them,
  write your own. You'll need this on the exam.
"""

STARTER = '''\
from adscb.primitives import BST


def solve():
    def bst_min(node):
        # your code here
        pass

    def bst_max(node):
        pass

    def bst_predecessor(node):
        pass

    def bst_successor(node):
        pass

    return bst_min, bst_max, bst_predecessor, bst_successor
'''

HINTS = [
    "min: while node.left is not None: node = node.left. Return node.",
    "predecessor: if node.left is not None: return max of node.left. Otherwise: walk parents while current is a LEFT child; return the parent when current becomes a right child (or None).",
    "successor mirrors predecessor: if node.right, return min of right subtree; otherwise walk up while current is a right child.",
]


def reference():
    def bst_min(node):
        if node is None:
            return None
        while node.left is not None:
            node = node.left
        return node

    def bst_max(node):
        if node is None:
            return None
        while node.right is not None:
            node = node.right
        return node

    def bst_predecessor(node):
        if node is None:
            return None
        if node.left is not None:
            return bst_max(node.left)
        parent = node.parent
        while parent is not None and node is parent.left:
            node = parent
            parent = parent.parent
        return parent

    def bst_successor(node):
        if node is None:
            return None
        if node.right is not None:
            return bst_min(node.right)
        parent = node.parent
        while parent is not None and node is parent.right:
            node = parent
            parent = parent.parent
        return parent

    return bst_min, bst_max, bst_predecessor, bst_successor


def tests(student):
    from adscb.primitives import BST

    def _build(keys):
        T = BST()
        for k in keys:
            T.insert(k)
        return T

    def case_returns_four_callables():
        result = student()
        assert len(result) == 4
        assert all(callable(f) for f in result)

    def case_min_max():
        bmin, bmax, _, _ = student()
        T = _build([5, 3, 8, 1, 4, 7, 9])
        assert bmin(T.root).key == 1
        assert bmax(T.root).key == 9

    def case_min_max_subtree():
        bmin, bmax, _, _ = student()
        T = _build([5, 3, 8, 1, 4, 7, 9])
        # min of right subtree (rooted at 8) is 7
        assert bmin(T.root.right).key == 7
        # max of left subtree (rooted at 3) is 4
        assert bmax(T.root.left).key == 4

    def case_min_max_none():
        bmin, bmax, _, _ = student()
        assert bmin(None) is None
        assert bmax(None) is None

    def case_predecessor_with_left_child():
        _, _, pred, _ = student()
        T = _build([5, 3, 8, 1, 4, 7, 9])
        # pred(5) should walk left then all right → 4
        assert pred(T.root).key == 4

    def case_predecessor_no_left_child():
        _, _, pred, _ = student()
        T = _build([5, 3, 8, 1, 4, 7, 9])
        # pred(4): no left child, walk up — 4 is right child of 3 → pred is 3
        node4 = T.search(4)
        assert pred(node4).key == 3
        # pred(7): no left child, walk up — 7 is left child of 8, 8 is right of 5 → pred is 5
        node7 = T.search(7)
        assert pred(node7).key == 5

    def case_predecessor_of_minimum():
        _, _, pred, _ = student()
        T = _build([5, 3, 8, 1])
        node1 = T.search(1)
        assert pred(node1) is None, "minimum has no predecessor"

    def case_successor_with_right_child():
        _, _, _, succ = student()
        T = _build([5, 3, 8, 1, 4, 7, 9])
        # succ(5) should walk right then all left → 7
        assert succ(T.root).key == 7

    def case_successor_no_right_child():
        _, _, _, succ = student()
        T = _build([5, 3, 8, 1, 4, 7, 9])
        # succ(4): no right child, 4 is right of 3 → walk up until 4 is left child → succ = 5
        node4 = T.search(4)
        assert succ(node4).key == 5

    def case_successor_of_maximum():
        _, _, _, succ = student()
        T = _build([5, 3, 8, 9])
        node9 = T.search(9)
        assert succ(node9) is None, "maximum has no successor"

    return [
        ("solve() returns four callables", case_returns_four_callables),
        ("min / max of whole tree", case_min_max),
        ("min / max of subtree", case_min_max_subtree),
        ("min / max of None", case_min_max_none),
        ("predecessor with left child", case_predecessor_with_left_child),
        ("predecessor without left child", case_predecessor_no_left_child),
        ("predecessor of minimum → None", case_predecessor_of_minimum),
        ("successor with right child", case_successor_with_right_child),
        ("successor without right child", case_successor_no_right_child),
        ("successor of maximum → None", case_successor_of_maximum),
    ]

META = {
    "id": "ch05/10_bst_search",
    "title": "BST search",
    "chapter": 5,
    "chapter_title": "Chapter 5 — Trees",
    "difficulty": 1,
    "requires_recursion": False,
    "entry": "bst_search",
}

DESCRIPTION = """
# BST search

Write the canonical binary search tree search. Given the root of a
BST and a key `k`, return the first node with `node.key == k`, or
`None` if no such node exists.

## Signature

```python
def bst_search(root, k):
    # root is a BST.Node or None
    # returns a BST.Node or None
    ...
```

## The algorithm (from the slides)

At each node, compare `k` with the current key:
- equal → found, return the node
- `k < node.key` → go left
- `k > node.key` → go right

Iterative or recursive, both are fine. The slides show both.

## Complexity

- Best case O(1) (match at the root).
- Worst case Θ(h) where h is the tree height. On a balanced BST
  that's Θ(log n); on a degenerate (list-shaped) one it's Θ(n).

## Notes

- No recursion requirement — do whichever you prefer.
- The `BST` primitive already has a search method; DON'T import and
  call it. Write your own on the raw nodes.
"""

STARTER = '''\
from adscb.primitives import BST


def bst_search(root, k):
    """Return the node with key == k, or None."""
    # your code here
    pass
'''

HINTS = [
    "Iterative: curr = root; while curr is not None: compare and move left/right; return curr when found.",
    "Recursive: base case root is None → None; root.key == k → root; else recurse on root.left or root.right.",
    "Return curr (which will be None) if you fall off the bottom of the tree.",
]


def reference(root, k):
    curr = root
    while curr is not None:
        if k == curr.key:
            return curr
        curr = curr.left if k < curr.key else curr.right
    return None


def tests(student):
    from adscb.primitives import BST

    def _build(keys):
        T = BST()
        for key in keys:
            T.insert(key)
        return T

    def case_empty():
        assert student(None, 5) is None

    def case_root_hit():
        T = _build([5, 3, 8])
        assert student(T.root, 5).key == 5

    def case_left():
        T = _build([5, 3, 8, 1, 4])
        assert student(T.root, 3).key == 3
        assert student(T.root, 1).key == 1
        assert student(T.root, 4).key == 4

    def case_right():
        T = _build([5, 3, 8, 7, 9])
        assert student(T.root, 8).key == 8
        assert student(T.root, 7).key == 7
        assert student(T.root, 9).key == 9

    def case_miss():
        T = _build([5, 3, 8, 1, 4, 7, 9])
        assert student(T.root, 99) is None
        assert student(T.root, 0) is None
        assert student(T.root, 6) is None

    def case_returns_actual_node():
        T = _build([5, 3, 8])
        node = student(T.root, 3)
        assert node is not None
        assert node.key == 3
        assert node.parent is T.root, "returned node should have correct parent link"

    return [
        ("empty tree", case_empty),
        ("hit at root", case_root_hit),
        ("hit in left subtree", case_left),
        ("hit in right subtree", case_right),
        ("miss", case_miss),
        ("returns an actual BST node (with parent)", case_returns_actual_node),
    ]

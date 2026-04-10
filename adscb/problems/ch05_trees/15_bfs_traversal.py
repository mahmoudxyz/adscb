META = {
    "id": "ch05/15_bfs_traversal",
    "title": "BFS (level-order) traversal with a Queue",
    "chapter": 5,
    "chapter_title": "Chapter 5 — Trees",
    "difficulty": 2,
    "requires_recursion": False,
    "entry": "bfs",
    "suggest_primitives": ["CircularQueue"],
}

DESCRIPTION = """
# BFS / level-order traversal

Implement **breadth-first search** on a binary tree using a
`CircularQueue` from `adscb.primitives`. Return the keys visited in
level order: the root first, then all nodes at depth 1 (left to
right), then depth 2, and so on.

## Signature

```python
def bfs(root):
    # root is a BinTree.Node or None
    # returns a Python list of keys in BFS order
    ...
```

## Example

         1
        / \\
       2   3
      / \\   \\
     4   5   6

    bfs(root)  →  [1, 2, 3, 4, 5, 6]

## The algorithm (from the slides)

1. If root is None, return [].
2. Create a queue and enqueue the root.
3. While the queue is not empty: dequeue a node, append its key to
   the output, then enqueue its children (left first, then right),
   skipping any None children.

## Notes

- Iterative. No recursion.
- Use `CircularQueue` with a capacity large enough for the tree (a
  safe bet is `CircularQueue(1024)` for exam-sized trees).
- Complexity: Θ(n) time, O(w) space where w is the max width.
"""

STARTER = '''\
from adscb.primitives import BinTree, CircularQueue


def bfs(root):
    """Return a list of keys in BFS (level-order)."""
    # your code here
    pass
'''

HINTS = [
    "Create Q = CircularQueue(1024). If root is None, return []. Otherwise Q.enqueue(root).",
    "While not Q.is_empty(): node = Q.dequeue(); append node.key to result; if node.left is not None: Q.enqueue(node.left); same for node.right.",
    "Return the result list at the end.",
]


def reference(root):
    from adscb.primitives import CircularQueue
    if root is None:
        return []
    Q = CircularQueue(1024)
    Q.enqueue(root)
    out = []
    while not Q.is_empty():
        node = Q.dequeue()
        out.append(node.key)
        if node.left is not None:
            Q.enqueue(node.left)
        if node.right is not None:
            Q.enqueue(node.right)
    return out


def tests(student):
    from adscb.primitives import BinTree

    def case_empty():
        assert student(None) == []

    def case_single():
        T = BinTree.from_list([1])
        assert student(T.root) == [1]

    def case_complete():
        T = BinTree.from_list([1, 2, 3, 4, 5, 6, 7])
        assert student(T.root) == [1, 2, 3, 4, 5, 6, 7]

    def case_sparse():
        # from_list already produces level-order, so BFS result should match
        values = [1, 2, 3, None, 4, 5, None, None, 6]
        T = BinTree.from_list(values)
        # level order of actual nodes: 1, 2, 3, 4, 5, 6
        assert student(T.root) == [1, 2, 3, 4, 5, 6]

    def case_left_chain():
        T = BinTree.from_list([1, 2, None, 3, None, 4])
        assert student(T.root) == [1, 2, 3, 4]

    def case_right_chain():
        T = BinTree.from_list([1, None, 2, None, 3, None, 4])
        assert student(T.root) == [1, 2, 3, 4]

    def case_lopsided():
        #         1
        #        / \
        #       2   3
        #      /     \
        #     4       5
        T = BinTree.from_list([1, 2, 3, 4, None, None, 5])
        assert student(T.root) == [1, 2, 3, 4, 5]

    return [
        ("empty tree", case_empty),
        ("single node", case_single),
        ("complete 7-node tree", case_complete),
        ("sparse tree", case_sparse),
        ("left chain", case_left_chain),
        ("right chain", case_right_chain),
        ("lopsided tree", case_lopsided),
    ]

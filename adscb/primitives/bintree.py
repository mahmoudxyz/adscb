"""Binary tree matching the pseudocode in the slides.

Each Node has `.key`, `.data`, `.left`, `.right`, `.parent`.
The tree has `.root`.

Construction in tests is done with `BinTree.from_list` using the
standard level-order encoding with `None` for missing children:

        1
       / \\
      2   3       ↔   [1, 2, 3, None, 4]
       \\
        4

`to_list` round-trips the same way. ASCII rendering draws the tree
vertically for debugging / test failure messages.
"""
from collections import deque


class BinTree:
    class Node:
        __slots__ = ("key", "data", "left", "right", "parent")

        def __init__(self, key, data=None):
            self.key = key
            self.data = data
            self.left = None
            self.right = None
            self.parent = None

        def __repr__(self):
            return f"BinNode({self.key!r})"

    def __init__(self, root=None):
        self.root = root

    def is_empty(self):
        return self.root is None

    # ------------------------------------------------------------------
    # Construction from a level-order list (LeetCode-style).
    # None means "no node here" — skipped entirely, does not consume a slot.
    # ------------------------------------------------------------------
    @classmethod
    def from_list(cls, values):
        """Build a BinTree from level-order [v0, v1, v2, ...] with None gaps."""
        if not values or values[0] is None:
            return cls()
        root = cls.Node(values[0])
        queue = deque([root])
        i = 1
        n = len(values)
        while queue and i < n:
            node = queue.popleft()
            # left child
            if i < n and values[i] is not None:
                node.left = cls.Node(values[i])
                node.left.parent = node
                queue.append(node.left)
            i += 1
            # right child
            if i < n and values[i] is not None:
                node.right = cls.Node(values[i])
                node.right.parent = node
                queue.append(node.right)
            i += 1
        return cls(root)

    def to_list(self):
        """Level-order serialization, trailing Nones trimmed."""
        if self.root is None:
            return []
        out = []
        queue = deque([self.root])
        while queue:
            node = queue.popleft()
            if node is None:
                out.append(None)
            else:
                out.append(node.key)
                queue.append(node.left)
                queue.append(node.right)
        # trim trailing Nones
        while out and out[-1] is None:
            out.pop()
        return out

    # ------------------------------------------------------------------
    # Traversals (built-ins so tests can reference them; students write
    # their own in the traversal exercise without importing these).
    # ------------------------------------------------------------------
    @staticmethod
    def preorder_keys(node):
        if node is None:
            return []
        return [node.key] + BinTree.preorder_keys(node.left) + BinTree.preorder_keys(node.right)

    @staticmethod
    def inorder_keys(node):
        if node is None:
            return []
        return BinTree.inorder_keys(node.left) + [node.key] + BinTree.inorder_keys(node.right)

    @staticmethod
    def postorder_keys(node):
        if node is None:
            return []
        return BinTree.postorder_keys(node.left) + BinTree.postorder_keys(node.right) + [node.key]

    @staticmethod
    def bfs_keys(root):
        if root is None:
            return []
        out = []
        queue = deque([root])
        while queue:
            node = queue.popleft()
            out.append(node.key)
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        return out

    # ------------------------------------------------------------------
    # Structural queries
    # ------------------------------------------------------------------
    def size(self):
        return self._size(self.root)

    @staticmethod
    def _size(node):
        if node is None:
            return 0
        return 1 + BinTree._size(node.left) + BinTree._size(node.right)

    def height(self):
        """Height per the slides: empty tree = -1, single node = 0."""
        return self._height(self.root)

    @staticmethod
    def _height(node):
        if node is None:
            return -1
        return 1 + max(BinTree._height(node.left), BinTree._height(node.right))

    # ------------------------------------------------------------------
    # ASCII rendering — draws the tree vertically for debug / failure output.
    # Simple layout, not the prettiest, but readable for trees up to height ~5.
    # ------------------------------------------------------------------
    def render(self):
        if self.root is None:
            return "(empty tree)"
        lines = _build_ascii(self.root)
        return "\n".join(lines)

    def __repr__(self):
        if self.root is None:
            return "BinTree(empty)"
        return f"BinTree{self.to_list()!r}"


def _build_ascii(node):
    """Return a list of lines drawing a binary tree rooted at `node`.

    Uses a recursive layout: each subtree is rendered, then joined side
    by side with a connector line. Good enough for exam-sized trees.
    """
    if node is None:
        return [" "]

    label = str(node.key)
    if node.left is None and node.right is None:
        return [label]

    left_lines = _build_ascii(node.left) if node.left is not None else [" "]
    right_lines = _build_ascii(node.right) if node.right is not None else [" "]

    left_width = max(len(line) for line in left_lines)
    right_width = max(len(line) for line in right_lines)

    # Pad each side to its max width
    left_lines = [line.ljust(left_width) for line in left_lines]
    right_lines = [line.ljust(right_width) for line in right_lines]

    # Balance heights
    height = max(len(left_lines), len(right_lines))
    while len(left_lines) < height:
        left_lines.append(" " * left_width)
    while len(right_lines) < height:
        right_lines.append(" " * right_width)

    gap = 2
    total_width = left_width + gap + right_width
    # Top line: the label, centered above the children
    top = label.center(total_width)
    # Connector line: slash / backslash
    left_half = ("/" if node.left is not None else " ").rjust(left_width)
    right_half = ("\\" if node.right is not None else " ").ljust(right_width)
    connector = left_half + " " * gap + right_half

    body = [left_lines[i] + " " * gap + right_lines[i] for i in range(height)]
    return [top, connector] + body

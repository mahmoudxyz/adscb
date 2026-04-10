"""Binary Search Tree matching the slide pseudocode.

Separate from `BinTree` so students can't accidentally get BST
behavior on a plain binary tree. `BST` supports the canonical
dictionary operations: search, insert, min, max, predecessor,
successor, delete.

The `Node` type has the same shape as BinTree.Node (key, data,
left, right, parent) so problems that operate on "any tree node"
work with either.
"""


class BST:
    class Node:
        __slots__ = ("key", "data", "left", "right", "parent")

        def __init__(self, key, data=None):
            self.key = key
            self.data = data
            self.left = None
            self.right = None
            self.parent = None

        def __repr__(self):
            return f"BSTNode({self.key!r})"

    def __init__(self):
        self.root = None
        self.size = 0

    def is_empty(self):
        return self.root is None

    # ------------------------------------------------------------------
    # search / insert / min / max
    # ------------------------------------------------------------------
    def search(self, key):
        curr = self.root
        while curr is not None:
            if key == curr.key:
                return curr
            curr = curr.left if key < curr.key else curr.right
        return None

    def insert(self, key, data=None):
        new = BST.Node(key, data)
        if self.root is None:
            self.root = new
            self.size += 1
            return new
        curr = self.root
        parent = None
        while curr is not None:
            parent = curr
            curr = curr.left if key < curr.key else curr.right
        new.parent = parent
        if key < parent.key:
            parent.left = new
        else:
            parent.right = new
        self.size += 1
        return new

    @staticmethod
    def min(node):
        """Minimum node in the subtree rooted at `node`. Leftmost descendant."""
        if node is None:
            return None
        while node.left is not None:
            node = node.left
        return node

    @staticmethod
    def max(node):
        if node is None:
            return None
        while node.right is not None:
            node = node.right
        return node

    # ------------------------------------------------------------------
    # predecessor / successor (in-order neighbors)
    # ------------------------------------------------------------------
    @staticmethod
    def predecessor(node):
        if node is None:
            return None
        if node.left is not None:
            return BST.max(node.left)
        # walk up until we come from the right
        parent = node.parent
        while parent is not None and node is parent.left:
            node = parent
            parent = parent.parent
        return parent

    @staticmethod
    def successor(node):
        if node is None:
            return None
        if node.right is not None:
            return BST.min(node.right)
        parent = node.parent
        while parent is not None and node is parent.right:
            node = parent
            parent = parent.parent
        return parent

    # ------------------------------------------------------------------
    # delete
    # ------------------------------------------------------------------
    def delete(self, key):
        node = self.search(key)
        if node is None:
            return False
        self._delete_node(node)
        self.size -= 1
        return True

    def _delete_node(self, v):
        """Remove node v, following the three-case scheme from the slides."""
        if v.left is None and v.right is None:
            self._replace(v, None)
        elif v.left is None:
            self._replace(v, v.right)
        elif v.right is None:
            self._replace(v, v.left)
        else:
            # two children → copy predecessor's key/data, then delete predecessor
            pred = BST.predecessor(v)
            v.key = pred.key
            v.data = pred.data
            # pred has at most one child (left), fall through cases 1/2
            self._replace(pred, pred.left)

    def _replace(self, old, new):
        """Splice `new` in where `old` was, updating parent pointers."""
        if old.parent is None:
            self.root = new
        elif old is old.parent.left:
            old.parent.left = new
        else:
            old.parent.right = new
        if new is not None:
            new.parent = old.parent

    # ------------------------------------------------------------------
    # helpers for tests
    # ------------------------------------------------------------------
    def inorder_keys(self):
        return self._inorder(self.root, [])

    def _inorder(self, node, acc):
        if node is None:
            return acc
        self._inorder(node.left, acc)
        acc.append(node.key)
        self._inorder(node.right, acc)
        return acc

    @classmethod
    def from_list(cls, keys):
        """Build a BST by inserting keys in the given order."""
        T = cls()
        for k in keys:
            T.insert(k)
        return T

    def __repr__(self):
        return f"BST(inorder={self.inorder_keys()})"

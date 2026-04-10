"""General (non-binary) tree via first-child / next-sibling.

Each node has `.key`, `.data`, `.first` (first child), `.next` (next
sibling), `.parent`. This matches the representation in the slides,
which is the one used by Exercises 5 and 6 in the lecture notes.

To add a child to a node, you insert into the sibling chain starting
at `parent.first`. Traversal is "walk first, then next-sibling at
each level".
"""


class GenTree:
    class Node:
        __slots__ = ("key", "data", "first", "next", "parent")

        def __init__(self, key, data=None):
            self.key = key
            self.data = data
            self.first = None
            self.next = None
            self.parent = None

        def __repr__(self):
            return f"GenNode({self.key!r})"

    def __init__(self, root=None):
        self.root = root

    def is_empty(self):
        return self.root is None

    # ------------------------------------------------------------------
    # Construction from a nested list:
    #
    #     [1, [2, [5], [6]], [3], [4, [7]]]
    #
    # means: root is 1, its children are 2, 3, 4;
    #        2's children are 5 and 6; 4's child is 7.
    # ------------------------------------------------------------------
    @classmethod
    def from_nested(cls, spec):
        """Build a GenTree from a nested list [key, child1, child2, ...]."""
        if spec is None or len(spec) == 0:
            return cls()
        root = cls._build(spec, None)
        return cls(root)

    @classmethod
    def _build(cls, spec, parent):
        node = cls.Node(spec[0])
        node.parent = parent
        if len(spec) > 1:
            # First child
            first = cls._build(spec[1], node)
            node.first = first
            prev = first
            for child_spec in spec[2:]:
                sibling = cls._build(child_spec, node)
                prev.next = sibling
                prev = sibling
        return node

    def preorder_keys(self):
        """Root, then children left-to-right (recursively)."""
        out = []
        self._pre(self.root, out)
        return out

    def _pre(self, node, out):
        if node is None:
            return
        out.append(node.key)
        # walk first child, then its siblings
        child = node.first
        while child is not None:
            self._pre(child, out)
            child = child.next

    def size(self):
        return self._count(self.root)

    def _count(self, node):
        if node is None:
            return 0
        n = 1
        child = node.first
        while child is not None:
            n += self._count(child)
            child = child.next
        return n

    def __repr__(self):
        if self.root is None:
            return "GenTree(empty)"
        return f"GenTree(preorder={self.preorder_keys()})"

"""Doubly Linked List matching the pseudocode in the slides.

Same as SLList but each node also has `.prev`.
"""


class DLList:
    """Doubly linked list. `L.head` is the head node or None."""

    class Node:
        """A node with `.key`, `.prev`, `.next`."""
        __slots__ = ("key", "prev", "next")

        def __init__(self, key):
            self.key = key
            self.prev = None
            self.next = None

        def __repr__(self):
            return f"DLNode({self.key!r})"

    def __init__(self):
        self.head = None
        self.ops = 0

    def is_empty(self):
        return self.head is None

    @classmethod
    def from_list(cls, values):
        L = cls()
        prev = None
        for v in values:
            node = cls.Node(v)
            if prev is None:
                L.head = node
            else:
                prev.next = node
                node.prev = prev
            prev = node
        return L

    def to_list(self):
        return self.head_to_list(self.head)

    @staticmethod
    def head_to_list(head):
        out = []
        seen = set()
        curr = head
        while curr is not None:
            if id(curr) in seen:
                out.append("<cycle>")
                break
            seen.add(id(curr))
            out.append(curr.key)
            curr = curr.next
        return out

    def __repr__(self):
        return self.render()

    def render(self):
        if self.head is None:
            return "head → /"
        parts = ["head"]
        curr = self.head
        seen = set()
        while curr is not None:
            if id(curr) in seen:
                parts.append("⇄ <cycle>")
                break
            seen.add(id(curr))
            parts.append(f"⇄ [{curr.key}]")
            curr = curr.next
        parts.append("→ /")
        return " ".join(parts)

    def length(self):
        n = 0
        curr = self.head
        while curr is not None:
            n += 1
            curr = curr.next
        return n

"""Singly Linked List matching the pseudocode in the slides.

Each node has `.key` and `.next`. The list has `.head`. That's it.
No shortcuts, no tricks, no hidden Python list underneath.
"""


class SLList:
    """Singly linked list. `L.head` is the head node or None."""

    class Node:
        """A node with `.key` and `.next`. Use `SLList.Node(k)` to create one."""
        __slots__ = ("key", "next")

        def __init__(self, key):
            self.key = key
            self.next = None

        def __repr__(self):
            return f"Node({self.key!r})"

    def __init__(self):
        self.head = None
        self.ops = 0

    def is_empty(self):
        return self.head is None

    # ------------------------------------------------------------------
    # Helpers for building and inspecting lists in tests / the REPL.
    # These are not part of the "pseudocode model" — they're just glue
    # so you can write assertions without hand-building node chains.
    # ------------------------------------------------------------------

    @classmethod
    def from_list(cls, values):
        """Build an SLList from a Python list, preserving order."""
        L = cls()
        tail = None
        for v in values:
            node = cls.Node(v)
            if tail is None:
                L.head = node
            else:
                tail.next = node
            tail = node
        return L

    def to_list(self):
        """Return the keys as a plain Python list."""
        return self.head_to_list(self.head)

    @staticmethod
    def head_to_list(head):
        """Walk from a head node, return keys as a Python list.

        Safe if `head` is None. Detects cycles so a buggy solution
        doesn't hang your terminal.
        """
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

    # ------------------------------------------------------------------
    # Rendering — ASCII art matching the slides:  head → [10] → [-1] → /
    # ------------------------------------------------------------------

    def __repr__(self):
        return self.render()

    def render(self):
        return self.render_from(self.head)

    @staticmethod
    def render_from(head, label="head"):
        """Return a single-line ASCII rendering of the list starting at `head`."""
        if head is None:
            return f"{label} → /"
        parts = [label]
        curr = head
        seen = set()
        while curr is not None:
            if id(curr) in seen:
                parts.append("→ <cycle>")
                break
            seen.add(id(curr))
            parts.append(f"→ [{curr.key}]")
            curr = curr.next
        parts.append("→ /")
        return " ".join(parts)

    def length(self):
        """Count nodes. Θ(n) — not cached on purpose."""
        n = 0
        curr = self.head
        while curr is not None:
            n += 1
            curr = curr.next
        return n

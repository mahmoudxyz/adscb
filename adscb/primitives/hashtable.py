"""Hash Table matching the slide pseudocode.

Supports two collision-resolution strategies:
  - Chaining: each slot holds an SLList of entries
  - Open addressing: linear, quadratic, or double hashing

The default hash function is the division method h(k) = k mod m.
A custom hash_fn(key) -> int can be passed.

DELETED sentinel is used for open addressing (matching slides).
Every operation increments .ops for empirical complexity analysis.
"""

from .sllist import SLList

# Sentinel for open-addressing deleted slots (distinct from None/NIL)
DELETED = object()


class HashTable:
    """Hash table with configurable collision resolution.

    Parameters
    ----------
    m : int
        Table size (number of slots).
    strategy : str
        One of "chaining", "linear", "quadratic", "double".
    hash_fn : callable or None
        Custom hash function h(k) -> int in [0, m-1].
        Defaults to division method: k % m.
    c1, c2 : float
        Constants for quadratic probing (default 0, 1 — slide example).
    """

    class Entry:
        """A (key, data) pair stored in a slot."""
        __slots__ = ("key", "data")

        def __init__(self, key, data=None):
            self.key = key
            self.data = data

        def __repr__(self):
            return f"Entry({self.key!r}, {self.data!r})"

    def __init__(self, m, strategy="chaining", hash_fn=None, c1=0, c2=1):
        if strategy not in ("chaining", "linear", "quadratic", "double"):
            raise ValueError(f"unknown strategy: {strategy!r}")
        self.m = m
        self.n = 0  # number of stored keys
        self.strategy = strategy
        self.c1 = c1
        self.c2 = c2
        self.ops = 0

        if hash_fn is not None:
            self._hash_fn = hash_fn
        else:
            self._hash_fn = lambda k: k % m

        if strategy == "chaining":
            self.slots = [SLList() for _ in range(m)]
        else:
            self.slots = [None] * m  # None = empty, DELETED = deleted, Entry = occupied

    # ------------------------------------------------------------------
    # Hash functions
    # ------------------------------------------------------------------

    def hash_key(self, k):
        """Primary hash: h'(k) or h1(k). Returns int in [0, m-1]."""
        self.ops += 1
        return self._hash_fn(k)

    def _hash2(self, k):
        """Secondary hash for double hashing: h2(k) = (k % (m-1)) + 1.
        Never returns zero (matching slides)."""
        self.ops += 1
        return (k % (self.m - 1)) + 1

    def _probe(self, k, i):
        """Compute h(k, i) for the current strategy."""
        h1 = self.hash_key(k)
        if self.strategy == "linear":
            return (h1 + i) % self.m
        elif self.strategy == "quadratic":
            return (h1 + self.c1 * i + self.c2 * i * i) % self.m
        elif self.strategy == "double":
            return (h1 + i * self._hash2(k)) % self.m
        else:
            raise ValueError("probing only for open-addressing strategies")

    # ------------------------------------------------------------------
    # Core operations
    # ------------------------------------------------------------------

    def insert(self, k, data=None):
        """Insert key k with associated data. Returns True on success.

        Chaining: head-insert into the list at slot h(k).
        Open addressing: probe for an empty or DELETED slot.
        If key already exists, update its data.
        """
        if self.strategy == "chaining":
            return self._insert_chaining(k, data)
        else:
            return self._insert_open(k, data)

    def _insert_chaining(self, k, data):
        idx = self.hash_key(k)
        chain = self.slots[idx]
        # check if key already exists
        curr = chain.head
        while curr is not None:
            self.ops += 1
            if curr.key == k:
                self._set_entry_data(idx, k, data)
                return True
            curr = curr.next
        # head insert
        node = SLList.Node(k)
        node.next = chain.head
        chain.head = node
        # store data in a side dict (SLList.Node only has .key)
        self._set_entry_data(idx, k, data)
        self.n += 1
        return True

    def _insert_open(self, k, data):
        first_deleted = -1
        for i in range(self.m):
            j = self._probe(k, i)
            slot = self.slots[j]
            self.ops += 1
            if slot is None:
                # use first DELETED slot if we saw one, else this empty slot
                target = first_deleted if first_deleted >= 0 else j
                self.slots[target] = HashTable.Entry(k, data)
                self.n += 1
                return True
            elif slot is DELETED:
                if first_deleted < 0:
                    first_deleted = j
            elif slot.key == k:
                slot.data = data
                return True
        if first_deleted >= 0:
            self.slots[first_deleted] = HashTable.Entry(k, data)
            self.n += 1
            return True
        raise OverflowError("hash table overflow")

    def search(self, k):
        """Search for key k. Returns associated data or None."""
        if self.strategy == "chaining":
            return self._search_chaining(k)
        else:
            return self._search_open(k)

    def _search_chaining(self, k):
        idx = self.hash_key(k)
        chain = self.slots[idx]
        curr = chain.head
        while curr is not None:
            self.ops += 1
            if curr.key == k:
                return self._get_entry_data(idx, k)
            curr = curr.next
        return None

    def _search_open(self, k):
        for i in range(self.m):
            j = self._probe(k, i)
            slot = self.slots[j]
            self.ops += 1
            if slot is None:
                return None
            if slot is DELETED:
                continue
            if slot.key == k:
                return slot.data
        return None

    def delete(self, k):
        """Delete key k. Returns True if found, False otherwise."""
        if self.strategy == "chaining":
            return self._delete_chaining(k)
        else:
            return self._delete_open(k)

    def _delete_chaining(self, k):
        idx = self.hash_key(k)
        chain = self.slots[idx]
        prev = None
        curr = chain.head
        while curr is not None:
            self.ops += 1
            if curr.key == k:
                if prev is None:
                    chain.head = curr.next
                else:
                    prev.next = curr.next
                self._remove_entry_data(idx, k)
                self.n -= 1
                return True
            prev = curr
            curr = curr.next
        return False

    def _delete_open(self, k):
        for i in range(self.m):
            j = self._probe(k, i)
            slot = self.slots[j]
            self.ops += 1
            if slot is None:
                return False
            if slot is DELETED:
                continue
            if slot.key == k:
                self.slots[j] = DELETED
                self.n -= 1
                return True
        return False

    # ------------------------------------------------------------------
    # Chaining data storage (SLList.Node only has .key, so we keep
    # a side dict per slot for the associated data)
    # ------------------------------------------------------------------

    def _set_entry_data(self, idx, k, data):
        if not hasattr(self, "_chain_data"):
            self._chain_data = [{} for _ in range(self.m)]
        self._chain_data[idx][k] = data

    def _get_entry_data(self, idx, k):
        if not hasattr(self, "_chain_data"):
            return None
        return self._chain_data[idx].get(k)

    def _remove_entry_data(self, idx, k):
        if hasattr(self, "_chain_data") and k in self._chain_data[idx]:
            del self._chain_data[idx][k]

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def load_factor(self):
        return self.n / self.m

    def reset_ops(self):
        self.ops = 0

    def slot_contents(self):
        """Return a list of what's in each slot (for testing/visualization).

        Chaining: list of lists of keys per slot.
        Open addressing: list of key or None or 'DELETED' per slot.
        """
        if self.strategy == "chaining":
            result = []
            for chain in self.slots:
                keys = []
                curr = chain.head
                while curr is not None:
                    keys.append(curr.key)
                    curr = curr.next
                result.append(keys)
            return result
        else:
            result = []
            for slot in self.slots:
                if slot is None:
                    result.append(None)
                elif slot is DELETED:
                    result.append("DELETED")
                else:
                    result.append(slot.key)
            return result

    def __repr__(self):
        return f"HashTable(m={self.m}, n={self.n}, strategy={self.strategy!r})"

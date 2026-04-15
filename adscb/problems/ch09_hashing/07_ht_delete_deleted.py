META = {
    "id": "ch09/07_ht_delete_deleted",
    "title": "Delete with DELETED marker",
    "chapter": 9,
    "chapter_title": "Chapter 9 — Hash Tables",
    "difficulty": 3,
    "requires_recursion": False,
    "entry": "ht_insert_search_delete",
    "suggest_primitives": ["HashTable"],
}

DESCRIPTION = """
# Delete with DELETED Marker (Open Addressing)

Implement **insert**, **search**, and **delete** for an open-addressing
hash table using **linear probing** with the **DELETED sentinel**,
following the slide pseudocode exactly.

This is the hardest part of open addressing: you cannot simply set a
deleted slot to `None` because a subsequent search might stop
prematurely and miss a key that was probe-shifted past the deleted slot.

## Signature

```python
def ht_insert_search_delete(m, operations):
    # m: table size
    # operations: list of tuples:
    #   ("insert", key)      — insert key (no data, just the key)
    #   ("search", key)      — search for key
    #   ("delete", key)      — delete key
    # returns: list of results for each "search" operation
    #   True if found, False if not found
    ...
```

## Pseudocode (from slides)

### Insert
```
function insert(T[0..m-1], k, d):
    i = 0
    repeat
        j = h(k, i)
        if T[j] == NIL or T[j].key == k or T[j] == DELETED:
            T[j].key = k; T[j].data = d; return
        i = i + 1
    until i == m
    error "overflow"
```

### Search
```
function search(T[0..m-1], k):
    i = 0
    repeat
        j = h(k, i)
        if T[j].key == k: return T[j].data
        i = i + 1
    until T[j] == NIL or i == m
    return NIL
```

### Delete
```
function delete(T[0..m-1], k):
    i = 0
    repeat
        j = h(k, i)
        if T[j].key == k: T[j] = DELETED; return
        i = i + 1
    until T[j] == NIL or i == m
```

**Key rules:**
- **Search** stops at `NIL` but **skips** `DELETED` slots.
- **Delete** marks a slot as `DELETED` (not `NIL`).
- **Insert** can reuse a `DELETED` slot.

## Example

`m = 7`, linear probing `h(k,i) = (k%7 + i) % 7`:
1. insert 3 → slot 3
2. insert 10 → slot 3 occupied → slot 4
3. insert 17 → slot 3 occupied → slot 4 occupied → slot 5
4. delete 10 → slot 4 = DELETED
5. search 17 → h(17,0)=3, skip, h(17,1)=4 DELETED (skip!), h(17,2)=5 → **found!**
6. search 10 → h(10,0)=3 skip, h(10,1)=4 DELETED (skip!), h(10,2)=5 (17≠10), h(10,3)=6 NIL → **not found**

## Notes

- Use a special `DELETED` sentinel value (distinct from `None`).
- Linear probing: `h(k, i) = (k % m + i) % m`.
"""

STARTER = '''\
DELETED = object()  # sentinel for deleted slots

def ht_insert_search_delete(m, operations):
    """Process a sequence of insert/search/delete operations on an
    open-addressing hash table with linear probing and DELETED marker.
    Return a list of bool results for each search operation."""
    # your code here
    pass
'''

HINTS = [
    "Maintain a list T of length m. None = empty, DELETED = deleted, integer = occupied key. For insert: probe until None, DELETED, or matching key. For search: probe until None (stop) or matching key (skip DELETED). For delete: like search but set T[j] = DELETED when found.",
    "The crucial difference: search stops at None but NOT at DELETED. Delete sets DELETED. Insert can fill a DELETED slot.",
    "Collect search results in a list. For each search: return True if key found, False if you hit None or checked all m slots.",
]


def reference(m, operations):
    DELETED = object()
    T = [None] * m

    def _insert(k):
        first_deleted = -1
        for i in range(m):
            j = (k % m + i) % m
            if T[j] is None:
                target = first_deleted if first_deleted >= 0 else j
                T[target] = k
                return
            elif T[j] is DELETED:
                if first_deleted < 0:
                    first_deleted = j
            elif T[j] == k:
                return
        if first_deleted >= 0:
            T[first_deleted] = k
            return
        raise OverflowError("hash table overflow")

    def _search(k):
        for i in range(m):
            j = (k % m + i) % m
            if T[j] is None:
                return False
            if T[j] is DELETED:
                continue
            if T[j] == k:
                return True
        return False

    def _delete(k):
        for i in range(m):
            j = (k % m + i) % m
            if T[j] is None:
                return
            if T[j] is DELETED:
                continue
            if T[j] == k:
                T[j] = DELETED
                return

    results = []
    for op, k in operations:
        if op == "insert":
            _insert(k)
        elif op == "search":
            results.append(_search(k))
        elif op == "delete":
            _delete(k)
    return results


def tests(student):
    def case_basic_insert_search():
        ops = [("insert", 3), ("insert", 10), ("search", 3), ("search", 10), ("search", 99)]
        result = student(7, ops)
        assert result == [True, True, False], f"got {result}"

    def case_delete_then_search():
        ops = [
            ("insert", 3), ("insert", 10), ("insert", 17),
            ("delete", 10),
            ("search", 17),
            ("search", 10),
        ]
        result = student(7, ops)
        assert result == [True, False], f"got {result}"

    def case_insert_after_delete():
        ops = [
            ("insert", 3), ("insert", 10),
            ("delete", 10),
            ("search", 10),
            ("insert", 10),
            ("search", 10),
        ]
        result = student(7, ops)
        assert result == [False, True], f"got {result}"

    def case_delete_nonexistent():
        ops = [("insert", 5), ("delete", 99), ("search", 5)]
        result = student(7, ops)
        assert result == [True], f"got {result}"

    def case_no_ops():
        result = student(7, [])
        assert result == [], f"got {result}"

    def case_multiple_deletes():
        ops = [
            ("insert", 3), ("insert", 10), ("insert", 17),
            ("delete", 3), ("delete", 10), ("delete", 17),
            ("search", 3), ("search", 10), ("search", 17),
        ]
        result = student(7, ops)
        assert result == [False, False, False], f"got {result}"

    def case_reuse_deleted_slot():
        ops = [
            ("insert", 3), ("insert", 10),
            ("delete", 3),
            ("insert", 3),  # should reuse slot 3 or DELETED slot
            ("search", 3), ("search", 10),
        ]
        result = student(7, ops)
        assert result == [True, True], f"got {result}"

    def case_complex_sequence():
        ops = [
            ("insert", 0), ("insert", 7), ("insert", 14),  # all hash to 0 in m=7
            ("search", 14),  # True
            ("delete", 7),
            ("search", 14),  # True — must skip DELETED at slot 1
            ("insert", 21),  # hashes to 0, can fill DELETED slot at 1
            ("search", 21),  # True
            ("search", 7),   # False — was deleted
        ]
        result = student(7, ops)
        assert result == [True, True, True, False], f"got {result}"

    return [
        ("basic insert + search", case_basic_insert_search),
        ("delete then search past DELETED", case_delete_then_search),
        ("insert after delete reuses slot", case_insert_after_delete),
        ("delete nonexistent key", case_delete_nonexistent),
        ("no operations", case_no_ops),
        ("multiple deletes", case_multiple_deletes),
        ("reuse DELETED slot on insert", case_reuse_deleted_slot),
        ("complex sequence", case_complex_sequence),
    ]

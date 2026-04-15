META = {
    "id": "ch09/04_chaining_ht",
    "title": "Hash Table with Chaining",
    "chapter": 9,
    "chapter_title": "Chapter 9 — Hash Tables",
    "difficulty": 2,
    "requires_recursion": False,
    "entry": "chaining_insert_search",
    "suggest_primitives": ["HashTable"],
}

DESCRIPTION = """
# Hash Table with Chaining

Implement **insert** and **search** for a hash table that uses
**chaining** (separate chaining) for collision resolution, following
the slide pseudocode.

You are given a `HashTable` object with `strategy="chaining"`. Each
slot contains an `SLList` chain. Your job is to walk the chain and
perform the operations correctly.

## Signature

```python
def chaining_insert_search(ht, keys, query):
    # ht: HashTable with strategy="chaining"
    # keys: list of integer keys to insert (in order)
    # query: integer key to search for after all insertions
    # returns: True if query is found, False otherwise
    ...
```

## Pseudocode (from slides)

```
function insert(SLList T[0..m-1], Key k, Data d)
    tmp = llsearch(T[h(k)], k)
    if tmp ≠ NIL then tmp.data = d
    else llinsert(T[h(k)], k, d)

function search(SLList T[0..m-1], Key k) → Data
    tmp = llsearch(T[h(k)], k)
    if tmp ≠ NIL then return tmp.data
    else return NIL
```

## Example

Hash function: `h(k) = k mod 10`
Insert keys: `53, 75, 16, 73, 10, 33, 13, 76`

Result:
- Slot 0: → [10]
- Slot 3: → [13] → [33] → [73] → [53]
- Slot 5: → [75]
- Slot 6: → [76] → [16]

Search for 33 → True, search for 99 → False.

## Notes

- Use `ht.insert(k, data=k)` and `ht.search(k)` from the HashTable primitive.
  When the key is found, `search` returns its data (the key itself); when not
  found, it returns `None`.
- The hash function is already set on the table (division method by default).
- Insert keys **in the given order** — chaining inserts at the head.
"""

STARTER = '''\
from adscb.primitives import HashTable

def chaining_insert_search(ht, keys, query):
    """Insert all keys into the chaining hash table, then search for query."""
    # your code here
    pass
'''

HINTS = [
    "Loop over keys and call ht.insert(k, data=k) for each one.",
    "After all insertions, call ht.search(query). It returns the data (the key) if found, or None if not found.",
    "Return ht.search(query) is not None — that's True if found, False if not.",
]


def reference(ht, keys, query):
    for k in keys:
        ht.insert(k, data=k)
    return ht.search(query) is not None


def tests(student):
    def _make_ht(m=10):
        return __import__("adscb.primitives", fromlist=["HashTable"]).HashTable(m, strategy="chaining")

    def case_slide_example_found():
        ht = _make_ht(10)
        assert student(ht, [53, 75, 16, 73, 10, 33, 13, 76], 33) is True

    def case_slide_example_not_found():
        ht = _make_ht(10)
        assert student(ht, [53, 75, 16, 73, 10, 33, 13, 76], 99) is False

    def case_empty_table():
        ht = _make_ht(7)
        assert student(ht, [], 5) is False

    def case_single_key():
        ht = _make_ht(7)
        assert student(ht, [42], 42) is True

    def case_single_key_not_found():
        ht = _make_ht(7)
        assert student(ht, [42], 43) is False

    def case_all_same_hash():
        # m=5, keys 5,10,15,20 all hash to slot 0
        ht = _make_ht(5)
        assert student(ht, [5, 10, 15, 20], 15) is True
        ht2 = _make_ht(5)
        assert student(ht2, [5, 10, 15, 20], 12) is False

    def case_duplicate_key():
        ht = _make_ht(7)
        assert student(ht, [3, 3, 3], 3) is True

    def case_large_m():
        ht = _make_ht(701)
        keys = list(range(100))
        assert student(ht, keys, 50) is True
        ht2 = _make_ht(701)
        assert student(ht2, keys, 200) is False

    return [
        ("slide example: search 33 → found", case_slide_example_found),
        ("slide example: search 99 → not found", case_slide_example_not_found),
        ("empty table", case_empty_table),
        ("single key found", case_single_key),
        ("single key not found", case_single_key_not_found),
        ("all same hash slot", case_all_same_hash),
        ("duplicate key", case_duplicate_key),
        ("large m=701", case_large_m),
    ]

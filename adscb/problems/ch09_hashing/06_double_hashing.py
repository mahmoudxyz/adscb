META = {
    "id": "ch09/06_double_hashing",
    "title": "Double Hashing Simulation",
    "chapter": 9,
    "chapter_title": "Chapter 9 — Hash Tables",
    "difficulty": 2,
    "requires_recursion": False,
    "entry": "double_hashing_insert",
    "suggest_primitives": ["HashTable"],
}

DESCRIPTION = """
# Double Hashing Simulation

Simulate inserting a sequence of keys into a hash table that uses
**double hashing** (open addressing), and return the final table state.

## Signature

```python
def double_hashing_insert(m, keys):
    # m: table size
    # keys: list of integer keys to insert (in order)
    # returns: list of length m where each element is the key stored
    #          at that slot, or None if the slot is empty
    ...
```

## Pseudocode (from slides)

```
h(k, i) = (h1(k) + i * h2(k)) mod m

h1(k) = k mod m
h2(k) = (k mod (m-1)) + 1    ← never zero, cycles through table
```

## Example

`m = 10`, keys: `53, 75, 16, 73, 10, 33, 13, 76`

| Slot | 0  | 1  | 2 | 3  | 4  | 5  | 6  | 7  | 8  | 9 |
|------|----|----|---|----|----|----|----|----|----|---|
| Key  | 10 | 76 | / | 53 | 33 | 75 | 16 | 73 | 13 | / |

Notes:
- 73: h1=3, h2=(73%9)+1=2 → h(73,0)=3 occupied → h(73,1)=5 occupied → h(73,2)=7 ✓
- 33: h1=3, h2=(33%9)+1=7 → h(33,0)=3 occupied → h(33,1)=0 occupied → h(33,2)=7 occupied → h(33,3)=4 ✓
- 13: h1=3, h2=(13%9)+1=5 → h(13,0)=3 occupied → h(13,1)=8 ✓
- 76: h1=6, h2=(76%9)+1=5 → h(76,0)=6 occupied → h(76,1)=1 ✓

## Notes

- Double hashing avoids both primary and secondary clustering.
- `h2(k)` must **never return 0** (otherwise we'd probe the same slot forever).
- `h2(k) = (k mod (m-1)) + 1` guarantees this.
"""

STARTER = '''\
def double_hashing_insert(m, keys):
    """Insert keys into an open-addressing table with double hashing.
    Return list of length m (key at each slot, or None if empty)."""
    # your code here
    pass
'''

HINTS = [
    "h1(k) = k % m, h2(k) = (k % (m-1)) + 1. For each key, try h(k,i) = (h1 + i*h2) % m for i=0,1,2,...",
    "Create T = [None]*m. For each key k: compute h1 and h2, then probe: j = (h1 + i*h2) % m, increment i until T[j] is None.",
    "Same structure as linear probing, but the step size varies per key (h2 instead of 1).",
]


def reference(m, keys):
    T = [None] * m
    for k in keys:
        h1 = k % m
        h2 = (k % (m - 1)) + 1
        for i in range(m):
            j = (h1 + i * h2) % m
            if T[j] is None:
                T[j] = k
                break
        else:
            raise OverflowError("hash table overflow")
    return T


def tests(student):
    def case_slide_example():
        result = student(10, [53, 75, 16, 73, 10, 33, 13, 76])
        expected = [10, 76, None, 53, 33, 75, 16, 73, 13, None]
        assert result == expected, f"got {result}"

    def case_no_collisions():
        result = student(7, [0, 1, 2, 3])
        assert result == [0, 1, 2, 3, None, None, None]

    def case_single_key():
        result = student(7, [42])
        assert result[42 % 7] == 42

    def case_empty_keys():
        result = student(7, [])
        assert result == [None] * 7

    def case_two_keys_same_h1():
        # Both hash to slot 3 with m=7, but h2 differs
        result = student(7, [3, 10])
        assert result[3] == 3
        # 10: h1=3, h2=(10%6)+1=5, probe: (3+5)%7=1
        assert result[1] == 10

    def case_prime_m():
        m = 11
        keys = [3, 14, 25]  # all h1=3, different h2
        result = student(m, keys)
        assert result[3] == 3
        assert 14 in result
        assert 25 in result

    def case_different_from_linear():
        # Same keys as linear probing — result should differ
        keys = [53, 75, 16, 73, 10, 33, 13, 76]
        linear = [10, None, None, 53, 73, 75, 16, 33, 13, 76]
        result = student(10, keys)
        assert result != linear, "double hashing should produce different placement than linear probing"

    return [
        ("slide example: m=10, 8 keys", case_slide_example),
        ("no collisions", case_no_collisions),
        ("single key", case_single_key),
        ("empty keys list", case_empty_keys),
        ("two keys same h1", case_two_keys_same_h1),
        ("prime m=11", case_prime_m),
        ("differs from linear probing", case_different_from_linear),
    ]

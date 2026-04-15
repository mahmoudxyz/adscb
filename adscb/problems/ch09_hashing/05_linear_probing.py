META = {
    "id": "ch09/05_linear_probing",
    "title": "Linear Probing Simulation",
    "chapter": 9,
    "chapter_title": "Chapter 9 — Hash Tables",
    "difficulty": 2,
    "requires_recursion": False,
    "entry": "linear_probing_insert",
    "suggest_primitives": ["HashTable"],
}

DESCRIPTION = """
# Linear Probing Simulation

Simulate inserting a sequence of keys into a hash table that uses
**linear probing** (open addressing), and return the final table state.

## Signature

```python
def linear_probing_insert(m, keys):
    # m: table size
    # keys: list of integer keys to insert (in order)
    # returns: list of length m where each element is the key stored
    #          at that slot, or None if the slot is empty
    ...
```

## Pseudocode (from slides)

```
h(k, i) = (h'(k) + i) mod m     where h'(k) = k mod m
```

Upon collision, inspect the **next slot** (wrapping around).

## Example

`m = 10`, keys: `53, 75, 16, 73, 10, 33, 13, 76`

| Slot | 0  | 1 | 2 | 3  | 4  | 5  | 6  | 7  | 8  | 9  |
|------|----|---|---|----|----|----|----|----|----|----|
| Key  | 10 | / | / | 53 | 73 | 75 | 16 | 33 | 13 | 76 |

Notes:
- 73 collides with 53 at slot 3 → probes to slot 4
- 33 collides at 3 → 4 occupied → 5 occupied → 6 occupied → slot 7
- 13 collides at 3 → probes 4,5,6,7 → slot 8
- 76 collides at 6 → probes 7,8 → slot 9

## Notes

- Use the division method: `h'(k) = k mod m`.
- No deletions in this problem — only insertions.
- If the table overflows, raise an error (shouldn't happen in tests).
"""

STARTER = '''\
def linear_probing_insert(m, keys):
    """Insert keys into an open-addressing table with linear probing.
    Return list of length m (key at each slot, or None if empty)."""
    # your code here
    pass
'''

HINTS = [
    "Create a list T = [None] * m. For each key k: compute i = k % m, then while T[i] is not None: i = (i+1) % m. Set T[i] = k.",
    "Be careful not to loop forever — stop if you've checked all m slots.",
    "The result is just the list T after all insertions.",
]


def reference(m, keys):
    T = [None] * m
    for k in keys:
        i = k % m
        steps = 0
        while T[i] is not None:
            i = (i + 1) % m
            steps += 1
            if steps >= m:
                raise OverflowError("hash table overflow")
        T[i] = k
    return T


def tests(student):
    def case_slide_example():
        result = student(10, [53, 75, 16, 73, 10, 33, 13, 76])
        expected = [10, None, None, 53, 73, 75, 16, 33, 13, 76]
        assert result == expected, f"got {result}"

    def case_no_collisions():
        result = student(7, [0, 1, 2, 3])
        assert result == [0, 1, 2, 3, None, None, None]

    def case_all_same_hash():
        # All keys hash to slot 0 with m=5
        result = student(5, [0, 5, 10, 15])
        assert result == [0, 5, 10, 15, None]

    def case_single_key():
        result = student(7, [42])
        assert result[42 % 7] == 42

    def case_empty_keys():
        result = student(7, [])
        assert result == [None] * 7

    def case_wrap_around():
        # Key 6 hashes to slot 6 in m=7, then key 13 (13%7=6) wraps
        result = student(7, [6, 13])
        assert result[6] == 6
        assert result[0] == 13

    def case_prime_m():
        m = 7
        keys = [3, 10, 17]  # all hash to slot 3
        result = student(m, keys)
        assert result[3] == 3
        assert result[4] == 10
        assert result[5] == 17

    return [
        ("slide example: m=10, 8 keys", case_slide_example),
        ("no collisions", case_no_collisions),
        ("all same hash", case_all_same_hash),
        ("single key", case_single_key),
        ("empty keys list", case_empty_keys),
        ("wrap around", case_wrap_around),
        ("prime m with collisions", case_prime_m),
    ]

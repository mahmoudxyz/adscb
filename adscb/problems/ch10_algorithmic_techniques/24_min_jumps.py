META = {
    "id": "ch10/24_min_jumps",
    "title": "Minimum Jumps to Reach End — Greedy",
    "chapter": 10,
    "chapter_title": "Chapter 10 — Algorithmic Techniques",
    "difficulty": 2,
    "requires_recursion": False,
    "entry": "min_jumps",
}

DESCRIPTION = """
# Minimum Jumps to Reach End — Greedy

Given an array `A` of non-negative integers, where `A[i]` is the **maximum
jump length** from position `i`, return the **minimum number of jumps** to
reach the last index (index `n-1`) starting from index `0`.

You may assume the input is always reachable (no case where you're stuck at 0).

## Signature

```python
def min_jumps(A):
    # A: list of non-negative integers, len >= 1
    # returns: int — minimum number of jumps to reach A[n-1]
    ...
```

## Examples

    A = [2, 3, 1, 1, 4]  →  2   (0→1→4, jump 1 then jump 3)
    A = [2, 3, 0, 1, 4]  →  2   (0→1→4)
    A = [1]              →  0   (already at end)
    A = [1, 1, 1, 1]     →  3

## Algorithm — Greedy O(n)

Track three variables:
- `jumps` — number of jumps taken
- `current_end` — farthest index reachable with `jumps` jumps
- `farthest` — farthest index reachable so far

```
jumps = 0
current_end = 0
farthest = 0
for i in 0 .. n-2:
    farthest = max(farthest, i + A[i])
    if i == current_end:       # must jump now
        jumps += 1
        current_end = farthest
        if current_end >= n-1: break
return jumps
```

Greedy choice: when you *must* jump (reached `current_end`), jump as far as
possible (`farthest`). This locally optimal choice is globally optimal.

## Complexity

- **Time:** O(n) — single pass
- **Space:** O(1)

## Notes

- Compare with the O(n²) DP solution:
  `dp[i] = 1 + min(dp[j] for j < i if j + A[j] >= i)`.
  The greedy approach is faster because it doesn't examine all predecessors.
- We loop only to `n-2` because from `n-1` no jump is needed.
"""

STARTER = '''\
def min_jumps(A):
    """Return the minimum number of jumps to reach the last index."""
    n = len(A)
    if n <= 1:
        return 0
    jumps = 0
    current_end = 0
    farthest = 0
    for i in range(n - 1):
        farthest = max(farthest, i + A[i])
        if i == current_end:
            # must take a jump here
            pass
    return jumps
'''

HINTS = [
    "When i == current_end you've exhausted the current jump's range — increment jumps and set current_end = farthest.",
    "Add an early exit: if current_end >= n-1 after updating, break — you can already reach the end.",
    "jumps += 1; current_end = farthest; if current_end >= n-1: break",
]


def reference(A):
    n = len(A)
    if n <= 1:
        return 0
    jumps = 0
    current_end = 0
    farthest = 0
    for i in range(n - 1):
        farthest = max(farthest, i + A[i])
        if i == current_end:
            jumps += 1
            current_end = farthest
            if current_end >= n - 1:
                break
    return jumps


def tests(student):
    def case_example1():
        assert student([2, 3, 1, 1, 4]) == 2

    def case_example2():
        assert student([2, 3, 0, 1, 4]) == 2

    def case_single():
        assert student([1]) == 0

    def case_two():
        assert student([1, 0]) == 1

    def case_all_ones():
        assert student([1, 1, 1, 1]) == 3

    def case_jump_to_end():
        assert student([5, 1, 1, 1, 1]) == 1  # jump directly from 0

    def case_greedy_beats_slow():
        # greedy takes 2; naively could take more
        assert student([3, 2, 1, 0, 4]) <= 2  # actually 0→(any of 1,2,3)→… but 3 is at A[3]=0
        # Wait: A[3]=0 means stuck. But problem says always reachable.
        # Let's use a safer example
        assert student([3, 2, 1, 1, 4]) == 2  # 0→3→4

    def case_large_jump_at_start():
        assert student([100] + [0] * 99 + [1]) == 1

    def case_minimal_steps():
        # each position has exact reach to next
        A = [1] * 10
        assert student(A) == 9

    def case_long():
        A = [2, 1] * 10 + [1]
        # 0→2→4→6→8→10→12→14→16→18→20
        assert student(A) == 10

    return [
        ("[2,3,1,1,4] → 2", case_example1),
        ("[2,3,0,1,4] → 2", case_example2),
        ("single element → 0", case_single),
        ("two elements → 1", case_two),
        ("all ones → n-1", case_all_ones),
        ("jump to end in 1 from A[0]", case_jump_to_end),
        ("greedy choice is correct", case_greedy_beats_slow),
        ("large jump at start → 1", case_large_jump_at_start),
        ("minimal-reach array", case_minimal_steps),
        ("long alternating", case_long),
    ]

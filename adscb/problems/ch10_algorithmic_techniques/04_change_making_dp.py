META = {
    "id": "ch10/04_change_making_dp",
    "title": "Change Making — Dynamic Programming",
    "chapter": 10,
    "chapter_title": "Chapter 10 — Algorithmic Techniques",
    "difficulty": 2,
    "requires_recursion": False,
    "entry": "change_dp",
}

DESCRIPTION = """
# Change Making — Dynamic Programming

Given a list of coin denominations `coins` and a target amount `W`,
return the **minimum number of coins** needed to make exactly `W`.

Coins can be used any number of times (unbounded). Return `float('inf')` if
it is not possible to make `W` with the given coins.

## Signature

```python
def change_dp(coins, W):
    # coins: list of distinct positive integers (not necessarily sorted)
    # W: non-negative integer
    # returns: int or float('inf')
    ...
```

## Examples

    coins = [1, 3, 4], W = 6  →  2     (3+3)
    coins = [1, 5, 10, 20], W = 8  →  4  (5+1+1+1)
    coins = [2], W = 3  →  inf         (impossible)
    coins = [1, 3, 4], W = 0  →  0

## Algorithm — Bottom-Up DP O(n·W)

Build a table `F[0..W]` where `F[i]` = min coins to make amount `i`.

```
F[0] = 0
for i = 1 .. W:
    F[i] = min over all c in coins where c <= i:
               F[i - c] + 1
return F[W]
```

Optimal substructure: the last coin used is some `c`, so the rest of the
change is made optimally — `F[W] = min_c (F[W-c] + 1)`.

## Complexity

- **Time:** O(n · W) — outer loop W, inner loop n coins
- **Space:** O(W) — the table F

## Notes

- This is the correct algorithm for **any** coin system, including non-canonical ones
  (where greedy would fail, e.g. coins=[1,3,4], W=6 → greedy gives 3, DP gives 2).
- The greedy algorithm `change_greedy` is O(n) but only works for canonical systems
  (e.g., standard currencies).
"""

STARTER = '''\
def change_dp(coins, W):
    """Return minimum coins to make W, or float(\'inf\') if impossible."""
    F = [float('inf')] * (W + 1)
    F[0] = 0
    for i in range(1, W + 1):
        for c in coins:
            # your code here
            pass
    return F[W]
'''

HINTS = [
    "For each amount i and each coin c: if c <= i, then F[i] = min(F[i], F[i - c] + 1).",
    "The condition `c <= i` ensures we don't use a coin larger than the amount. F[i-c] is the min coins for the remainder.",
    "F[0]=0 is the base case (0 coins for 0 amount). Return F[W] at the end.",
]


def reference(coins, W):
    F = [float('inf')] * (W + 1)
    F[0] = 0
    for i in range(1, W + 1):
        for c in coins:
            if c <= i and F[i - c] + 1 < F[i]:
                F[i] = F[i - c] + 1
    return F[W]


def tests(student):
    def case_lecture_example():
        assert student([1, 3, 4], 6) == 2  # 3+3

    def case_standard_coins():
        assert student([1, 5, 10, 20], 8) == 4  # 5+1+1+1

    def case_zero():
        assert student([1, 3, 4], 0) == 0

    def case_single_coin_exact():
        assert student([5], 15) == 3

    def case_impossible():
        assert student([2], 3) == float('inf')

    def case_greedy_wrong():
        # greedy picks 4+1+1=3, DP picks 3+3=2
        assert student([1, 3, 4], 6) == 2

    def case_greedy_wrong2():
        # coins [1,3,4], W=9: greedy 4+4+1=3, DP 3+3+3=3 — same here
        # coins [1,6,10], W=12: greedy 10+1+1=3, DP 6+6=2
        assert student([1, 6, 10], 12) == 2

    def case_single_large():
        assert student([1, 2, 5], 11) == 3  # 5+5+1

    def case_one_coin():
        assert student([1], 7) == 7

    def case_unsorted_coins():
        # coins not sorted — DP must handle this correctly
        assert student([4, 1, 3], 6) == 2

    return [
        ("lecture example [1,3,4], W=6 → 2", case_lecture_example),
        ("standard coins [1,5,10,20], W=8 → 4", case_standard_coins),
        ("W=0 → 0 coins", case_zero),
        ("single coin exact [5], W=15 → 3", case_single_coin_exact),
        ("impossible [2], W=3 → inf", case_impossible),
        ("greedy fails [1,3,4], W=6", case_greedy_wrong),
        ("greedy fails [1,6,10], W=12 → 2", case_greedy_wrong2),
        ("[1,2,5], W=11 → 3", case_single_large),
        ("coin=1 only → W coins", case_one_coin),
        ("unsorted coins", case_unsorted_coins),
    ]

META = {
    "id": "ch10/05_change_making_greedy",
    "title": "Change Making — Greedy",
    "chapter": 10,
    "chapter_title": "Chapter 10 — Algorithmic Techniques",
    "difficulty": 1,
    "requires_recursion": False,
    "entry": "change_greedy",
}

DESCRIPTION = """
# Change Making — Greedy

Given a **canonical** coin system `coins` (sorted ascending) and a target amount `W`,
return the **minimum number of coins** using the greedy strategy: always pick the
largest coin that fits.

Return `float('inf')` if `W` cannot be made (only possible if 1 is not in the system).

## Signature

```python
def change_greedy(coins, W):
    # coins: list of distinct positive integers, sorted ascending
    # W: non-negative integer
    # returns: int or float('inf')
    ...
```

## Examples

    coins = [1, 5, 10, 20], W = 8   →  4   (5+1+1+1)
    coins = [1, 5, 10, 20], W = 36  →  3   (20+10+5+1 = wait, 20+10+5+1=4, let's say W=35 → 20+10+5=3)
    coins = [1, 5, 10, 20], W = 0   →  0

## Algorithm — Greedy O(n)

Iterate from the largest coin to the smallest. For each coin `C[i]`:
- Take as many as possible: `count = W // C[i]`, `W = W % C[i]`
- Advance to the next smaller coin

```
res = 0, i = n-1
while W > 0 and i >= 0:
    res += W // coins[i]
    W   = W  %  coins[i]
    i  -= 1
return inf if W != 0 else res
```

## Complexity

- **Time:** O(n) — coins sorted, one pass right-to-left
- **Space:** O(1)

## Warning — Only Correct for Canonical Coin Systems

The greedy approach is **not** always optimal. For `coins=[1,3,4]` and `W=6`:
- Greedy: 4+1+1 = **3 coins**
- Optimal (DP): 3+3 = **2 coins**

Standard currencies (1,5,10,20,50,100,...) are canonical — greedy is optimal there.
"""

STARTER = '''\
def change_greedy(coins, W):
    """Return min coins using greedy (assumes canonical, sorted coin system)."""
    res = 0
    i = len(coins) - 1
    while W > 0 and i >= 0:
        # take as many of coins[i] as possible
        pass
    return float('inf') if W != 0 else res
'''

HINTS = [
    "At each step: take `W // coins[i]` copies of coins[i]. Add that to res.",
    "Reduce W: `W = W % coins[i]`. Then move to the next smaller coin: `i -= 1`.",
    "After the loop, if W != 0 change is impossible (return inf); otherwise return res.",
]


def reference(coins, W):
    res = 0
    i = len(coins) - 1
    while W > 0 and i >= 0:
        res += W // coins[i]
        W = W % coins[i]
        i -= 1
    return float('inf') if W != 0 else res


def tests(student):
    def case_lecture():
        assert student([1, 5, 10, 20], 8) == 4   # 5+1+1+1

    def case_zero():
        assert student([1, 5, 10, 20], 0) == 0

    def case_exact_coin():
        assert student([1, 5, 10, 20], 20) == 1

    def case_all_ones():
        assert student([1, 5, 10], 7) == 3   # 5+1+1

    def case_large_amount():
        assert student([1, 5, 10, 20], 99) == 10  # 4*20+1*10+1*5+4*1

    def case_impossible():
        assert student([2, 5], 3) == float('inf')

    def case_euro_style():
        # standard euro coins (subset): 41 = 20+20+1 = 3 coins
        assert student([1, 2, 5, 10, 20, 50], 41) == 3
        # 36 = 20+10+5+1 = 4 coins
        assert student([1, 2, 5, 10, 20, 50], 36) == 4

    def case_single_denom():
        assert student([5], 25) == 5
        assert student([5], 23) == float('inf')

    def case_multiple_of_largest():
        assert student([1, 5, 10, 25], 75) == 3  # 3*25

    return [
        ("lecture example [1,5,10,20], W=8 → 4", case_lecture),
        ("W=0 → 0", case_zero),
        ("exact coin [1,5,10,20], W=20 → 1", case_exact_coin),
        ("[1,5,10], W=7 → 3", case_all_ones),
        ("[1,5,10,20], W=99 → 10", case_large_amount),
        ("impossible [2,5], W=3 → inf", case_impossible),
        ("euro style W=41 → 3", case_euro_style),
        ("single denomination", case_single_denom),
        ("multiple of largest [1,5,10,25], W=75 → 3", case_multiple_of_largest),
    ]

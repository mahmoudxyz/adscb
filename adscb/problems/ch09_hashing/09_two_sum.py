META = {
    "id": "ch09/09_two_sum",
    "title": "Two Sum",
    "chapter": 9,
    "chapter_title": "Chapter 9 — Hash Tables",
    "difficulty": 2,
    "requires_recursion": False,
    "entry": "two_sum",
    "suggest_primitives": ["HashTable"],
}

DESCRIPTION = """
# Two Sum

Given a list of integers `nums` and an integer `target`, return the
**indices** of the two numbers that add up to `target`. Each input has
exactly one solution, and you may not use the same element twice.

This is the classic problem that demonstrates the power of hash tables
for lookup — turning a brute-force O(n²) solution into O(n) average.

## Signature

```python
def two_sum(nums, target):
    # nums: list of integers
    # target: integer
    # returns: tuple (i, j) where i < j and nums[i] + nums[j] == target
    ...
```

## Examples

- `two_sum([2, 7, 11, 15], 9)` → `(0, 1)`  (2 + 7 = 9)
- `two_sum([3, 2, 4], 6)` → `(1, 2)`  (2 + 4 = 6)
- `two_sum([3, 3], 6)` → `(0, 1)`  (3 + 3 = 6)

## Approach

For each element `nums[i]`, check if `target - nums[i]` has been seen
before (using a hash table / dict mapping value → index). If yes,
you've found the pair. If no, store `nums[i]` → i and continue.

## Complexity

| Case   | Time (average) | Space |
|--------|----------------|-------|
| Best   | O(n)           | O(n)  |
| Worst  | O(n)           | O(n)  |

Brute force would be O(n²) — the hash table eliminates the inner loop.
"""

STARTER = '''\
def two_sum(nums, target):
    """Return indices (i, j) with i < j such that nums[i] + nums[j] == target."""
    # your code here
    pass
'''

HINTS = [
    "Use a dict to store value → index. For each nums[i], compute complement = target - nums[i]. If complement is in the dict, return (dict[complement], i).",
    "Build the dict as you go: seen = {}. For i, val in enumerate(nums): if target-val in seen: return (seen[target-val], i); seen[val] = i.",
    "The one-pass approach works because when you reach the second element of the pair, the first is already in the dict.",
]


def reference(nums, target):
    seen = {}
    for i, val in enumerate(nums):
        complement = target - val
        if complement in seen:
            return (seen[complement], i)
        seen[val] = i
    return None


def tests(student):
    def case_classic():
        assert student([2, 7, 11, 15], 9) == (0, 1)

    def case_not_first():
        assert student([3, 2, 4], 6) == (1, 2)

    def case_duplicate_values():
        result = student([3, 3], 6)
        assert result == (0, 1)

    def case_negative_numbers():
        assert student([-1, -2, -3, -4, -5], -8) == (2, 4)

    def case_mixed_signs():
        assert student([1, -2, 3, 5], 3) == (1, 3)

    def case_two_elements():
        assert student([5, 5], 10) == (0, 1)

    def case_larger_array():
        nums = list(range(100))
        assert student(nums, 197) == (98, 99)

    def case_zero_target():
        assert student([0, 4, 3, 0], 0) == (0, 3)

    return [
        ("classic [2,7,11,15] target=9", case_classic),
        ("answer not at start", case_not_first),
        ("duplicate values", case_duplicate_values),
        ("negative numbers", case_negative_numbers),
        ("mixed signs", case_mixed_signs),
        ("two elements", case_two_elements),
        ("larger array", case_larger_array),
        ("zero target", case_zero_target),
    ]

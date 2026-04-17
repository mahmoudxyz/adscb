META = {
    "id": "ch10/23_activity_selection",
    "title": "Activity Selection — Greedy",
    "chapter": 10,
    "chapter_title": "Chapter 10 — Algorithmic Techniques",
    "difficulty": 2,
    "requires_recursion": False,
    "entry": "max_activities",
}

DESCRIPTION = """
# Activity Selection — Greedy

Given `n` activities, each with a start time and finish time, return the
**maximum number of non-overlapping activities** you can select.

Two activities are **compatible** (non-overlapping) if one finishes before
or exactly when the other starts: `finish[i] <= start[j]`.

## Signature

```python
def max_activities(start, finish):
    # start:  list of integers — start times
    # finish: list of integers — finish times
    # len(start) == len(finish)
    # returns: int
    ...
```

## Examples

    start  = [1, 3, 0, 5, 8, 5]
    finish = [2, 4, 6, 7, 9, 9]
    →  4   (pick activities 0,1,3,4 → times [1-2],[3-4],[5-7],[8-9])

    start  = [1, 2, 3]
    finish = [4, 5, 6]   (all overlap)
    →  1

## Algorithm — Greedy O(n log n)

**Greedy choice:** always pick the activity with the **earliest finish time**
that is compatible with the last selected activity.

Proof sketch: choosing the earliest-finishing activity leaves the most time
for remaining activities — it never hurts to pick it.

```
Sort activities by finish time.
Select first activity; last_finish = finish[0]
for i in 1 .. n-1:
    if start[i] >= last_finish:
        select activity i
        last_finish = finish[i]
return count
```

## Complexity

- **Sort:** O(n log n)
- **Scan:** O(n)
- **Total:** O(n log n)

## Notes

- The greedy-choice property holds because sorting by finish time minimizes
  the "damage" each selection does to future options.
- This is provably optimal — DP would also work but is overkill here.
- Activities that start exactly when another ends are **compatible** (use `>=`).
"""

STARTER = '''\
def max_activities(start, finish):
    """Return max number of non-overlapping activities (greedy by earliest finish)."""
    n = len(start)
    if n == 0:
        return 0
    # Sort by finish time
    activities = sorted(zip(start, finish), key=lambda x: x[1])
    count = 1
    last_finish = activities[0][1]
    for i in range(1, n):
        # select if compatible with last selected
        pass
    return count
'''

HINTS = [
    "After sorting by finish time, greedily pick any activity where start >= last_finish.",
    "When you pick activity i: count += 1; last_finish = activities[i][1].",
    "Start with count=1, last_finish=activities[0][1]. Loop i from 1 to n-1.",
]


def reference(start, finish):
    n = len(start)
    if n == 0:
        return 0
    activities = sorted(zip(start, finish), key=lambda x: x[1])
    count = 1
    last_finish = activities[0][1]
    for i in range(1, n):
        if activities[i][0] >= last_finish:
            count += 1
            last_finish = activities[i][1]
    return count


def tests(student):
    def case_example():
        s = [1, 3, 0, 5, 8, 5]
        f = [2, 4, 6, 7, 9, 9]
        assert student(s, f) == 4

    def case_all_overlap():
        assert student([1, 2, 3], [4, 5, 6]) == 1

    def case_no_overlap():
        assert student([1, 3, 5], [2, 4, 6]) == 3

    def case_empty():
        assert student([], []) == 0

    def case_single():
        assert student([1], [2]) == 1

    def case_back_to_back():
        # finish of one == start of next → compatible
        assert student([1, 2, 3], [2, 3, 4]) == 3

    def case_one_long_blocks_all():
        assert student([0, 1, 2, 3], [10, 2, 3, 4]) == 3  # skip [0,10]

    def case_sorted_by_start_is_wrong():
        # If you sort by start time you get the wrong answer here
        # Greedy by finish time: pick [1,2],[2,3],[3,4] = 3
        # Greedy by start time: pick [1,4] then [4,5] = 2
        assert student([1, 2, 3, 4], [4, 3, 4, 5]) == 3

    def case_ties_in_finish():
        # multiple activities finish at same time
        assert student([1, 1, 3], [2, 2, 4]) >= 2

    def case_large():
        # n non-overlapping intervals of length 1
        s = list(range(0, 20, 2))
        f = list(range(1, 21, 2))
        assert student(s, f) == 10

    return [
        ("example → 4", case_example),
        ("all overlap → 1", case_all_overlap),
        ("no overlap → n", case_no_overlap),
        ("empty → 0", case_empty),
        ("single → 1", case_single),
        ("back-to-back (equal boundary) → 3", case_back_to_back),
        ("one long activity blocks all others", case_one_long_blocks_all),
        ("sort-by-start gives wrong answer here", case_sorted_by_start_is_wrong),
        ("ties in finish time", case_ties_in_finish),
        ("10 non-overlapping intervals", case_large),
    ]

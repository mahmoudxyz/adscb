META = {
    "id": "ch05/06_gentree_path_sum",
    "title": "Count nodes whose root-to-node path sums to k",
    "chapter": 5,
    "chapter_title": "Chapter 5 — Trees",
    "difficulty": 3,
    "requires_recursion": True,
    "entry": "count_paths",
}

DESCRIPTION = """
# Count nodes whose root-to-node path sums to k

Given the root of a general tree (first-child / next-sibling) and an
integer `k`, return the number of nodes `v` such that the sum of the
keys on the path from the **root** to `v` (inclusive) equals `k`.

## Signature

```python
def count_paths(root, k):
    # root is a GenTree.Node or None
    # k is an int
    # returns an int (number of matching nodes)
    ...
```

## The tricky part

The first/next representation makes this exercise interesting.
When you recurse, you have to carry a "remaining budget" `k`, but
the budget behaves differently depending on which pointer you follow:

- Recursing on `node.first` = going **deeper** into the tree, so
  the budget must shrink by `node.key` to account for consuming it.
- Recursing on `node.next` = going **sideways** to a sibling, which
  stays at the same "path context" — the budget does **not** change.

This is genuinely the hardest bit of the chapter-5 exercises. Take
the hints.

## Example

    Tree:             k = 6
           2
          /|\\
         1 3 5
        /
       3

    Root-to-node path sums:
      2           → 2
      2,1         → 3
      2,1,3       → 6 ✓
      2,3         → 5
      2,5         → 7

    Answer: 1

## Notes

- Recursive.
- Complexity: Θ(n).
"""

STARTER = '''\
from adscb.primitives import GenTree


def count_paths(root, k):
    """Count nodes where the path from root to that node sums to k."""
    # hint: you'll want a helper that tracks remaining budget
    # your code here
    pass
'''

HINTS = [
    "Write a helper that takes (node, remaining) where `remaining` starts as k.",
    "Base: node is None → 0. Otherwise: does consuming node.key hit the target? Check remaining == node.key. That's 1 match at this node if so.",
    "Recurse: on .first with remaining - node.key (going deeper consumes node.key), and on .next with the ORIGINAL remaining (sibling is at same path context). Sum all three contributions.",
]


def reference(root, k):
    def helper(node, remaining):
        if node is None:
            return 0
        here = 1 if node.key == remaining else 0
        # .first: going into child, budget shrinks by node.key
        # .next: going to sibling, budget unchanged
        return here + helper(node.first, remaining - node.key) + helper(node.next, remaining)
    return helper(root, k)


def tests(student):
    from adscb.primitives import GenTree

    def case_empty():
        assert student(None, 5) == 0

    def case_single_match():
        T = GenTree.from_nested([5])
        assert student(T.root, 5) == 1

    def case_single_no_match():
        T = GenTree.from_nested([5])
        assert student(T.root, 4) == 0

    def case_description_example():
        #        2
        #       /|\
        #      1 3 5
        #     /
        #    3
        T = GenTree.from_nested([2, [1, [3]], [3], [5]])
        assert student(T.root, 6) == 1
        assert student(T.root, 2) == 1  # just root
        assert student(T.root, 3) == 1  # path 2,1
        assert student(T.root, 5) == 1  # path 2,3
        assert student(T.root, 7) == 1  # path 2,5
        assert student(T.root, 99) == 0

    def case_multiple_matches():
        # root 1, three children 2, 2, 2 — path sums 1, 3, 3, 3
        T = GenTree.from_nested([1, [2], [2], [2]])
        assert student(T.root, 3) == 3
        assert student(T.root, 1) == 1
        assert student(T.root, 2) == 0

    def case_deeper():
        #        1
        #       /|\
        #      2 3 4
        #     /|
        #    5 6
        # path sums:
        #   1           → 1
        #   1,2         → 3
        #   1,2,5       → 8
        #   1,2,6       → 9
        #   1,3         → 4
        #   1,4         → 5
        T = GenTree.from_nested([1, [2, [5], [6]], [3], [4]])
        assert student(T.root, 8) == 1
        assert student(T.root, 9) == 1
        assert student(T.root, 3) == 1
        assert student(T.root, 100) == 0

    def case_all_matching():
        # path sums are all k=1 when keys are all 0 except root? let me pick something cleaner
        # root 0, three children 0 → sums: 0, 0, 0, 0 → four matches for k=0
        T = GenTree.from_nested([0, [0], [0], [0]])
        assert student(T.root, 0) == 4

    return [
        ("empty tree", case_empty),
        ("single node, matches", case_single_match),
        ("single node, no match", case_single_no_match),
        ("description example", case_description_example),
        ("multiple sibling matches", case_multiple_matches),
        ("deeper tree", case_deeper),
        ("all paths sum to 0", case_all_matching),
    ]

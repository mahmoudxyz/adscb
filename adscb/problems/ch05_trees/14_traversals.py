META = {
    "id": "ch05/14_traversals",
    "title": "Tree traversals: pre/in/post from scratch",
    "chapter": 5,
    "chapter_title": "Chapter 5 — Trees",
    "difficulty": 1,
    "requires_recursion": True,
    "entry": "solve",
}

DESCRIPTION = """
# Pre-order, In-order, Post-order traversals

Write the three classic depth-first traversals on a binary tree.
Each one returns a Python list of keys in the appropriate order.

## What you write

```python
def solve():
    def preorder(root):
        # visit, left, right
        ...

    def inorder(root):
        # left, visit, right
        ...

    def postorder(root):
        # left, right, visit
        ...

    return preorder, inorder, postorder
```

## The difference

"Visit" here means "add the key to the output list". The only thing
that changes between the three is **when** you append, relative to
the recursive calls.

    preorder :  append → recurse left → recurse right
    inorder  :  recurse left → append → recurse right
    postorder:  recurse left → recurse right → append

## Example

         1
        / \\
       2   3
      / \\
     4   5

    preorder  : [1, 2, 4, 5, 3]
    inorder   : [4, 2, 5, 1, 3]
    postorder : [4, 5, 2, 3, 1]

## Why all three

Because the exam could ask for any of them, and they're the building
blocks of almost every tree algorithm. Write them cold.

## Complexity

Each runs in Θ(n).
"""

STARTER = '''\
from adscb.primitives import BinTree


def solve():
    def preorder(root):
        # your code here
        pass

    def inorder(root):
        pass

    def postorder(root):
        pass

    return preorder, inorder, postorder
'''

HINTS = [
    "For each, base case: if root is None, return [].",
    "Recursive case: compute left = traverse(root.left) and right = traverse(root.right), then concatenate in the right order.",
    "preorder: [root.key] + left + right. inorder: left + [root.key] + right. postorder: left + right + [root.key].",
]


def reference():
    def preorder(root):
        if root is None:
            return []
        return [root.key] + preorder(root.left) + preorder(root.right)

    def inorder(root):
        if root is None:
            return []
        return inorder(root.left) + [root.key] + inorder(root.right)

    def postorder(root):
        if root is None:
            return []
        return postorder(root.left) + postorder(root.right) + [root.key]

    return preorder, inorder, postorder


def tests(student):
    from adscb.primitives import BinTree

    def case_returns_three_callables():
        result = student()
        assert len(result) == 3 and all(callable(f) for f in result)

    def case_empty():
        pre, ino, post = student()
        assert pre(None) == []
        assert ino(None) == []
        assert post(None) == []

    def case_single():
        pre, ino, post = student()
        T = BinTree.from_list([42])
        assert pre(T.root) == [42]
        assert ino(T.root) == [42]
        assert post(T.root) == [42]

    def case_slide_example():
        #         1
        #        / \
        #       2   3
        #      / \
        #     4   5
        pre, ino, post = student()
        T = BinTree.from_list([1, 2, 3, 4, 5])
        assert pre(T.root) == [1, 2, 4, 5, 3]
        assert ino(T.root) == [4, 2, 5, 1, 3]
        assert post(T.root) == [4, 5, 2, 3, 1]

    def case_inorder_of_bst_is_sorted():
        _, ino, _ = student()
        T = BinTree.from_list([5, 3, 8, 1, 4, 7, 9])
        assert ino(T.root) == [1, 3, 4, 5, 7, 8, 9], \
            "in-order traversal of a BST should yield sorted keys"

    def case_left_chain():
        pre, ino, post = student()
        T = BinTree.from_list([1, 2, None, 3, None, 4])
        assert pre(T.root) == [1, 2, 3, 4]
        assert ino(T.root) == [4, 3, 2, 1]
        assert post(T.root) == [4, 3, 2, 1]

    def case_right_chain():
        pre, ino, post = student()
        T = BinTree.from_list([1, None, 2, None, 3, None, 4])
        assert pre(T.root) == [1, 2, 3, 4]
        assert ino(T.root) == [1, 2, 3, 4]
        assert post(T.root) == [4, 3, 2, 1]

    return [
        ("solve() returns three callables", case_returns_three_callables),
        ("empty tree", case_empty),
        ("single node", case_single),
        ("slide example", case_slide_example),
        ("in-order on a BST is sorted", case_inorder_of_bst_is_sorted),
        ("left chain", case_left_chain),
        ("right chain", case_right_chain),
    ]

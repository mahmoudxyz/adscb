META = {
    "id": "ch05/11_bst_insert",
    "title": "BST insert",
    "chapter": 5,
    "chapter_title": "Chapter 5 — Trees",
    "difficulty": 2,
    "requires_recursion": False,
    "entry": "bst_insert",
}

DESCRIPTION = """
# BST insert

Insert a new node with key `k` into a BST rooted at `root`. Return
the root of the tree (which may be the new node if the tree was
empty).

The new node must be wired in as a **leaf** — exactly as the slide
algorithm describes. Don't forget to set the new node's `.parent`
pointer, or predecessor/successor operations later will break.

## Signature

```python
def bst_insert(root, k):
    # root is a BST.Node or None
    # returns the (possibly new) root
    ...
```

## The algorithm

Walk down the tree the same way as search, tracking the last
non-None node as the prospective **parent**. When you fall off the
bottom, attach a fresh node to that parent on the correct side.

## Complexity

Θ(h) — same as search, since most of the work is walking to the
insertion point.

## Notes

- You may insert duplicates; the slides go right on `>=`.
- Iterative or recursive.
- Don't call the primitive's `.insert` method — write it yourself
  using raw Node objects (`BST.Node(k)`).
"""

STARTER = '''\
from adscb.primitives import BST


def bst_insert(root, k):
    """Insert k and return the root. Set .parent correctly."""
    # your code here
    pass
'''

HINTS = [
    "If root is None, return BST.Node(k) — a fresh single-node tree.",
    "Walk curr = root. Track parent = None. At each step, parent = curr, then curr = curr.left if k < curr.key else curr.right.",
    "When curr becomes None, attach: new = BST.Node(k); new.parent = parent; then parent.left = new or parent.right = new depending on k vs parent.key. Return root.",
]


def reference(root, k):
    from adscb.primitives import BST
    new = BST.Node(k)
    if root is None:
        return new
    curr = root
    parent = None
    while curr is not None:
        parent = curr
        curr = curr.left if k < curr.key else curr.right
    new.parent = parent
    if k < parent.key:
        parent.left = new
    else:
        parent.right = new
    return root


def _inorder(node, out):
    if node is None:
        return
    _inorder(node.left, out)
    out.append(node.key)
    _inorder(node.right, out)


def tests(student):
    from adscb.primitives import BST

    def case_empty():
        root = student(None, 5)
        assert root is not None and root.key == 5
        assert root.left is None and root.right is None
        assert root.parent is None

    def case_root_plus_smaller():
        root = BST.Node(5)
        returned = student(root, 3)
        assert returned is root
        assert root.left is not None and root.left.key == 3
        assert root.left.parent is root

    def case_root_plus_larger():
        root = BST.Node(5)
        student(root, 8)
        assert root.right.key == 8
        assert root.right.parent is root

    def case_multi_insert():
        root = None
        for k in [5, 3, 8, 1, 4, 7, 9]:
            root = student(root, k)
        inorder = []
        _inorder(root, inorder)
        assert inorder == [1, 3, 4, 5, 7, 8, 9]

    def case_bst_property_holds():
        root = None
        for k in [10, 5, 15, 3, 7, 12, 20, 1, 4, 6, 8]:
            root = student(root, k)
        # for every node: all left-descendants < key, all right-descendants >= key
        def check(node):
            if node is None:
                return True
            if node.left is not None:
                l_max = node.left
                while l_max.right is not None:
                    l_max = l_max.right
                if l_max.key >= node.key:
                    return False
            if node.right is not None:
                r_min = node.right
                while r_min.left is not None:
                    r_min = r_min.left
                if r_min.key < node.key:
                    return False
            return check(node.left) and check(node.right)
        assert check(root)

    def case_parent_pointers_correct():
        root = None
        for k in [5, 3, 8, 1, 4]:
            root = student(root, k)
        # walk and verify every child's parent points to the correct node
        def walk(node):
            if node is None:
                return True
            if node.left is not None and node.left.parent is not node:
                return False
            if node.right is not None and node.right.parent is not node:
                return False
            return walk(node.left) and walk(node.right)
        assert walk(root), "parent pointers are broken"
        assert root.parent is None, "root's parent must be None"

    return [
        ("insert into empty tree", case_empty),
        ("insert smaller than root", case_root_plus_smaller),
        ("insert larger than root", case_root_plus_larger),
        ("multiple inserts, in-order is sorted", case_multi_insert),
        ("BST property holds after many inserts", case_bst_property_holds),
        ("parent pointers set correctly", case_parent_pointers_correct),
    ]

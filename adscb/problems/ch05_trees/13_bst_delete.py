META = {
    "id": "ch05/13_bst_delete",
    "title": "BST delete (three cases)",
    "chapter": 5,
    "chapter_title": "Chapter 5 — Trees",
    "difficulty": 3,
    "requires_recursion": False,
    "entry": "bst_delete",
}

DESCRIPTION = """
# BST delete

Implement the three-case delete algorithm from the slides. Given
the root of a BST and a key `k`, remove the first node with that
key (if any) and return the (possibly new) root.

## Signature

```python
def bst_delete(root, k):
    # root is a BST.Node or None
    # returns the new root (which may be None, or a different node)
    ...
```

## The three cases

Let `v` be the node to delete.

1. **`v` is a leaf** → simply detach it.
2. **`v` has exactly one child** → splice that child into `v`'s place
   (update `v.parent`'s relevant pointer to `v`'s only child, and
   fix the child's `.parent`).
3. **`v` has two children** → find `v`'s **predecessor** `u` (which
   is the maximum of `v.left` — guaranteed to have at most one
   child, namely a left child). Copy `u`'s key and data into `v`,
   then delete `u` using case 1 or 2.

## Complexity

Θ(h) where h is the tree height.

## Notes

- If `k` is not in the tree, return the root unchanged.
- You may write a helper `_replace(old, new, root)` that splices
  `new` in place of `old` and returns the (possibly new) root.
- Keep `.parent` pointers correct throughout. The predecessor /
  successor operations on the exam will break otherwise.
- Don't call `BST`'s built-in `.delete` — write it yourself.
"""

STARTER = '''\
from adscb.primitives import BST


def bst_delete(root, k):
    """Delete the first node with key == k. Return the new root."""
    # your code here
    pass
'''

HINTS = [
    "Step 1: find the node v with key k. If not found, return root unchanged.",
    "Step 2: handle the three cases. For cases 1 and 2, just splice: let `child` be v's only child (or None), then replace v with child in its parent's link, and set child.parent = v.parent. If v was the root, the new root is `child`.",
    "Step 3: for case 3 (two children), find the predecessor by walking v.left then all the way right. Copy pred.key/pred.data into v, then delete pred using the single-child logic (pred has at most a left child).",
]


def reference(root, k):
    # find v
    v = root
    while v is not None and v.key != k:
        v = v.left if k < v.key else v.right
    if v is None:
        return root

    def replace(old, new):
        """Splice `new` in where `old` was. Returns the new root if old was root."""
        if new is not None:
            new.parent = old.parent
        if old.parent is None:
            return new
        if old is old.parent.left:
            old.parent.left = new
        else:
            old.parent.right = new
        return root  # root unchanged

    if v.left is None and v.right is None:
        return replace(v, None)
    if v.left is None:
        return replace(v, v.right)
    if v.right is None:
        return replace(v, v.left)
    # two children: find predecessor (max of v.left)
    pred = v.left
    while pred.right is not None:
        pred = pred.right
    v.key = pred.key
    v.data = pred.data
    # pred has at most a left child
    replace(pred, pred.left)
    return root


def _inorder(node, out):
    if node is None:
        return
    _inorder(node.left, out)
    out.append(node.key)
    _inorder(node.right, out)


def _check_parents(root):
    """Every child's .parent must point to its actual parent."""
    if root is None:
        return True
    if root.parent is not None:
        return False  # root must have no parent
    stack = [root]
    while stack:
        node = stack.pop()
        if node.left is not None:
            if node.left.parent is not node:
                return False
            stack.append(node.left)
        if node.right is not None:
            if node.right.parent is not node:
                return False
            stack.append(node.right)
    return True


def tests(student):
    from adscb.primitives import BST

    def _build(keys):
        T = BST()
        for k in keys:
            T.insert(k)
        return T

    def case_delete_from_empty():
        assert student(None, 5) is None

    def case_delete_absent_key():
        T = _build([5, 3, 8])
        r = student(T.root, 99)
        inorder = []
        _inorder(r, inorder)
        assert inorder == [3, 5, 8]

    def case_delete_leaf():
        T = _build([5, 3, 8, 1, 4])
        r = student(T.root, 1)
        inorder = []
        _inorder(r, inorder)
        assert inorder == [3, 4, 5, 8]
        assert _check_parents(r)

    def case_delete_single_child_node():
        T = _build([5, 3, 8, 1])  # 3 has only left child (1)
        r = student(T.root, 3)
        inorder = []
        _inorder(r, inorder)
        assert inorder == [1, 5, 8]
        assert _check_parents(r)

    def case_delete_two_children_node():
        T = _build([5, 3, 8, 1, 4, 7, 9])
        r = student(T.root, 3)  # 3 has children 1 and 4
        inorder = []
        _inorder(r, inorder)
        assert inorder == [1, 4, 5, 7, 8, 9]
        assert _check_parents(r)

    def case_delete_root_two_children():
        T = _build([5, 3, 8, 1, 4, 7, 9])
        r = student(T.root, 5)
        inorder = []
        _inorder(r, inorder)
        assert inorder == [1, 3, 4, 7, 8, 9]
        assert _check_parents(r)

    def case_delete_root_one_child():
        T = _build([5, 3, 1])  # root 5, left 3, 3's left 1
        r = student(T.root, 5)
        inorder = []
        _inorder(r, inorder)
        assert inorder == [1, 3]
        assert _check_parents(r)
        assert r.parent is None

    def case_delete_root_single_node():
        T = _build([5])
        r = student(T.root, 5)
        assert r is None

    def case_many_deletes():
        T = _build([10, 5, 15, 3, 7, 12, 20, 1, 4, 6, 8])
        root = T.root
        for k in [7, 15, 10, 3, 1]:
            root = student(root, k)
        inorder = []
        _inorder(root, inorder)
        assert inorder == [4, 5, 6, 8, 12, 20]
        assert _check_parents(root)

    return [
        ("delete from empty tree", case_delete_from_empty),
        ("delete absent key (tree unchanged)", case_delete_absent_key),
        ("delete leaf", case_delete_leaf),
        ("delete single-child node", case_delete_single_child_node),
        ("delete two-children node", case_delete_two_children_node),
        ("delete root with two children", case_delete_root_two_children),
        ("delete root with one child", case_delete_root_one_child),
        ("delete root of single-node tree", case_delete_root_single_node),
        ("many successive deletions", case_many_deletes),
    ]

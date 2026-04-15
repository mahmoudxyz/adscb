"""Pseudocode-flavored data structures.

These primitives deliberately mirror the pseudocode conventions used in
the lecture slides, not Python's built-ins. Use them when you want your
code to behave like the algorithms on the blackboard:

    - Array is 1-indexed and fixed-size (matches A[1..n] notation)
    - SLList / DLList expose .head and Node with .key / .next / .prev
    - Stack has .top as an index and .peek() for the value on top
    - CircularQueue uses the circular-buffer trick shown in the slides

Every primitive tracks an .ops counter so you can empirically verify
the complexity of your algorithms.

    NIL is provided as an alias for None so you can write `if x == NIL`
    exactly like the slides do.
"""
from .array import Array
from .sllist import SLList
from .dllist import DLList
from .stack import Stack
from .queue import CircularQueue, Queue
from .bintree import BinTree
from .bst import BST
from .gentree import GenTree
from .hashtable import HashTable, DELETED

NIL = None

__all__ = [
    "Array", "SLList", "DLList", "Stack", "Queue", "CircularQueue",
    "BinTree", "BST", "GenTree", "HashTable", "DELETED", "NIL",
]

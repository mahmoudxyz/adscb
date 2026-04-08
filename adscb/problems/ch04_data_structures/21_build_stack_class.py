META = {
    "id": "ch04/21_build_stack_class",
    "title": "Build it yourself — Stack class from an Array",
    "chapter": 4,
    "chapter_title": "Chapter 4 — Elementary Data Structures",
    "difficulty": 2,
    "requires_recursion": False,
    "entry": "build",
}

DESCRIPTION = """
# Build it yourself: Stack from an Array

Build your own `Stack` class, backed by the 1-indexed `Array` primitive.
No `list`, no shortcuts — you should end up with the exact data
structure the slides describe in "push and pop with fixed-sized array".

## What you write

A class with this API:

```python
class MyStack:
    def __init__(self, capacity):
        # allocate an Array of size `capacity`
        # initialize self.top to 0 (0 means empty)
        ...

    def push(self, x):
        # raise OverflowError if full
        ...

    def pop(self):
        # raise IndexError if empty
        # return the popped value
        ...

    def peek(self):
        # return top value without popping
        # raise IndexError if empty
        ...

    def is_empty(self):
        ...
```

Then return it from `build()`:

```python
def build():
    return MyStack
```

## Rules

- Must use `Array` from `adscb.primitives` as the underlying storage.
- `self.top` is an integer index (0 = empty, `capacity` = full), matching the slides.
- All operations must be O(1).
- Do **not** import `Stack` from `adscb.primitives`.

## Why

The next problems will use the production `Stack` primitive, but
going through this once gives you the muscle memory for the pointer
arithmetic and the overflow/underflow checks.
"""

STARTER = '''\
from adscb.primitives import Array


class MyStack:
    def __init__(self, capacity):
        # your code here
        pass

    def push(self, x):
        pass

    def pop(self):
        pass

    def peek(self):
        pass

    def is_empty(self):
        pass


def build():
    return MyStack
'''

HINTS = [
    "In __init__, save self.data = Array(capacity), self.capacity = capacity, self.top = 0.",
    "push: if self.top == self.capacity raise OverflowError; else self.top += 1; self.data[self.top] = x.",
    "pop: if self.top == 0 raise IndexError; else save x = self.data[self.top], decrement self.top, return x.",
]


def reference():
    from adscb.primitives import Array

    class MyStack:
        def __init__(self, capacity):
            self.data = Array(capacity)
            self.capacity = capacity
            self.top = 0

        def push(self, x):
            if self.top == self.capacity:
                raise OverflowError("stack overflow")
            self.top += 1
            self.data[self.top] = x

        def pop(self):
            if self.top == 0:
                raise IndexError("stack underflow")
            x = self.data[self.top]
            self.top -= 1
            return x

        def peek(self):
            if self.top == 0:
                raise IndexError("stack empty")
            return self.data[self.top]

        def is_empty(self):
            return self.top == 0

    return MyStack


def tests(student):

    def case_build_returns_class():
        cls = student()
        assert isinstance(cls, type), "build() must return a class"
        S = cls(4)
        assert hasattr(S, "push") and hasattr(S, "pop") and hasattr(S, "peek") and hasattr(S, "is_empty")

    def case_empty_on_creation():
        cls = student()
        S = cls(4)
        assert S.is_empty()

    def case_push_pop_single():
        cls = student()
        S = cls(4)
        S.push(42)
        assert not S.is_empty()
        assert S.peek() == 42
        assert S.pop() == 42
        assert S.is_empty()

    def case_lifo_order():
        cls = student()
        S = cls(4)
        for v in [1, 2, 3, 4]:
            S.push(v)
        assert [S.pop() for _ in range(4)] == [4, 3, 2, 1]

    def case_peek_does_not_pop():
        cls = student()
        S = cls(4)
        S.push(1)
        S.push(2)
        assert S.peek() == 2
        assert S.peek() == 2
        assert S.pop() == 2
        assert S.peek() == 1

    def case_overflow():
        cls = student()
        S = cls(2)
        S.push(1)
        S.push(2)
        try:
            S.push(3)
            assert False, "push on full stack should raise OverflowError"
        except OverflowError:
            pass

    def case_underflow():
        cls = student()
        S = cls(2)
        try:
            S.pop()
            assert False, "pop on empty stack should raise IndexError"
        except IndexError:
            pass

    def case_push_after_pop():
        cls = student()
        S = cls(2)
        S.push(1)
        S.push(2)
        S.pop()
        S.push(3)
        assert S.peek() == 3

    return [
        ("build() returns a class", case_build_returns_class),
        ("empty on creation", case_empty_on_creation),
        ("push then pop", case_push_pop_single),
        ("LIFO ordering", case_lifo_order),
        ("peek does not pop", case_peek_does_not_pop),
        ("overflow raises", case_overflow),
        ("underflow raises", case_underflow),
        ("push after pop", case_push_after_pop),
    ]

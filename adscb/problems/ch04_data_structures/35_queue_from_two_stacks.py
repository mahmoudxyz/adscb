META = {
    "id": "ch04/35_queue_from_two_stacks",
    "title": "Queue from two Stacks",
    "chapter": 4,
    "chapter_title": "Chapter 4 — Elementary Data Structures",
    "difficulty": 3,
    "requires_recursion": False,
    "entry": "build",
}

DESCRIPTION = """
# Queue from two Stacks

Implement a FIFO queue using only two `Stack` instances internally.
You may use `push`, `pop`, `peek`, `is_empty` on the stacks — nothing
else. No lists, no arrays, no cheating.

## What you write

A class with this API:

```python
class StackQueue:
    def __init__(self, capacity):
        # you may allocate up to two Stack(capacity) internally
        ...

    def enqueue(self, x):
        ...

    def dequeue(self):
        # raise IndexError if empty
        # return the dequeued value
        ...

    def is_empty(self):
        ...
```

Then return it from `build()`:

```python
def build():
    return StackQueue
```

## The trick

One stack is the "input" side; the other is the "output" side.

- `enqueue(x)` always pushes onto the input stack.
- `dequeue()`: if the output stack is empty, drain the entire input
  stack into the output stack (which reverses the order, turning the
  top of the input into the bottom of the output — exactly what FIFO
  needs). Then pop from the output stack.

## Amortized analysis

Each element is pushed onto the input stack once, popped from it
once, pushed onto the output stack once, and popped from it once —
four O(1) operations per element total. So both `enqueue` and
`dequeue` are **O(1) amortized**, even though a single `dequeue` may
take Θ(n) in the worst case when it has to drain a full input stack.

This problem is why amortized analysis matters.
"""

STARTER = '''\
from adscb.primitives import Stack


class StackQueue:
    def __init__(self, capacity):
        # your code here
        pass

    def enqueue(self, x):
        pass

    def dequeue(self):
        pass

    def is_empty(self):
        pass


def build():
    return StackQueue
'''

HINTS = [
    "__init__: self.inp = Stack(capacity); self.out = Stack(capacity).",
    "enqueue: just self.inp.push(x).",
    "dequeue: if self.out is empty, drain everything from self.inp into self.out (while not self.inp.is_empty(): self.out.push(self.inp.pop())). Then pop and return from self.out. If both are empty, raise IndexError.",
]


def reference():
    from adscb.primitives import Stack

    class StackQueue:
        def __init__(self, capacity):
            self.inp = Stack(capacity)
            self.out = Stack(capacity)

        def enqueue(self, x):
            self.inp.push(x)

        def dequeue(self):
            if self.out.is_empty():
                if self.inp.is_empty():
                    raise IndexError("queue is empty")
                while not self.inp.is_empty():
                    self.out.push(self.inp.pop())
            return self.out.pop()

        def is_empty(self):
            return self.inp.is_empty() and self.out.is_empty()

    return StackQueue


def tests(student):

    def case_build_returns_class():
        cls = student()
        assert isinstance(cls, type)
        Q = cls(8)
        for m in ("enqueue", "dequeue", "is_empty"):
            assert hasattr(Q, m)

    def case_empty_on_creation():
        cls = student()
        Q = cls(8)
        assert Q.is_empty()

    def case_simple_fifo():
        cls = student()
        Q = cls(8)
        for v in [1, 2, 3]:
            Q.enqueue(v)
        assert [Q.dequeue() for _ in range(3)] == [1, 2, 3]
        assert Q.is_empty()

    def case_underflow():
        cls = student()
        Q = cls(4)
        try:
            Q.dequeue()
            assert False, "dequeue on empty should raise IndexError"
        except IndexError:
            pass

    def case_interleaved():
        cls = student()
        Q = cls(16)
        Q.enqueue(1)
        Q.enqueue(2)
        assert Q.dequeue() == 1
        Q.enqueue(3)
        Q.enqueue(4)
        assert Q.dequeue() == 2
        assert Q.dequeue() == 3
        Q.enqueue(5)
        assert Q.dequeue() == 4
        assert Q.dequeue() == 5
        assert Q.is_empty()

    def case_enqueue_after_full_drain():
        cls = student()
        Q = cls(16)
        for v in range(5):
            Q.enqueue(v)
        for expected in range(5):
            assert Q.dequeue() == expected
        # now completely empty — enqueue again
        Q.enqueue(99)
        Q.enqueue(100)
        assert Q.dequeue() == 99
        assert Q.dequeue() == 100

    def case_large_interleaved():
        cls = student()
        Q = cls(64)
        expected = []
        for v in range(20):
            Q.enqueue(v)
            expected.append(v)
        for _ in range(10):
            assert Q.dequeue() == expected.pop(0)
        for v in range(20, 30):
            Q.enqueue(v)
            expected.append(v)
        while expected:
            assert Q.dequeue() == expected.pop(0)
        assert Q.is_empty()

    return [
        ("build() returns a class", case_build_returns_class),
        ("empty on creation", case_empty_on_creation),
        ("simple FIFO", case_simple_fifo),
        ("underflow raises", case_underflow),
        ("interleaved enqueue/dequeue", case_interleaved),
        ("enqueue after full drain", case_enqueue_after_full_drain),
        ("larger interleaved workload", case_large_interleaved),
    ]

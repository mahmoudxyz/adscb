META = {
    "id": "ch04/22_build_circular_queue",
    "title": "Build it yourself — CircularQueue class from scratch",
    "chapter": 4,
    "chapter_title": "Chapter 4 — Elementary Data Structures",
    "difficulty": 2,
    "requires_recursion": False,
    "entry": "build",
}

DESCRIPTION = """
# Build it yourself: CircularQueue

Implement a circular-buffer queue from scratch. The modulo arithmetic
for wrapping `head` and `tail` around the end of the buffer is the
whole point of the exercise.

## What you write

```python
class MyQueue:
    def __init__(self, capacity):
        ...

    def enqueue(self, x):
        # raise OverflowError if full
        ...

    def dequeue(self):
        # raise IndexError if empty
        # return the dequeued value
        ...

    def is_empty(self):
        ...

    def is_full(self):
        ...
```

Then return it from `build()`:

```python
def build():
    return MyQueue
```

## Rules

- Must use a plain Python list (or `adscb.primitives.Array` if you
  prefer) as the fixed-size buffer.
- Track `head`, `tail`, and `size` as integer attributes.
- All operations must be O(1). No shifting, no loops.
- Do **not** import `CircularQueue` or `Queue` from `adscb.primitives`.

## The circular trick

After an enqueue:  `tail = (tail + 1) % capacity`.
After a dequeue:   `head = (head + 1) % capacity`.

That's the whole algorithm. When `tail` hits the end of the buffer,
it wraps around to slot 0 — and because `head` is also advancing,
the occupied region slides cleanly around the ring.
"""

STARTER = '''\
class MyQueue:
    def __init__(self, capacity):
        # your code here
        pass

    def enqueue(self, x):
        pass

    def dequeue(self):
        pass

    def is_empty(self):
        pass

    def is_full(self):
        pass


def build():
    return MyQueue
'''

HINTS = [
    "In __init__: self.buf = [None] * capacity, self.capacity = capacity, self.head = 0, self.tail = 0, self.size = 0.",
    "enqueue: if self.size == self.capacity raise OverflowError. Else self.buf[self.tail] = x; self.tail = (self.tail + 1) % self.capacity; self.size += 1.",
    "dequeue: if self.size == 0 raise IndexError. Else x = self.buf[self.head]; self.head = (self.head + 1) % self.capacity; self.size -= 1; return x.",
]


def reference():
    class MyQueue:
        def __init__(self, capacity):
            self.buf = [None] * capacity
            self.capacity = capacity
            self.head = 0
            self.tail = 0
            self.size = 0

        def enqueue(self, x):
            if self.size == self.capacity:
                raise OverflowError("queue overflow")
            self.buf[self.tail] = x
            self.tail = (self.tail + 1) % self.capacity
            self.size += 1

        def dequeue(self):
            if self.size == 0:
                raise IndexError("queue underflow")
            x = self.buf[self.head]
            self.head = (self.head + 1) % self.capacity
            self.size -= 1
            return x

        def is_empty(self):
            return self.size == 0

        def is_full(self):
            return self.size == self.capacity

    return MyQueue


def tests(student):

    def case_build_returns_class():
        cls = student()
        assert isinstance(cls, type)
        Q = cls(4)
        for method in ("enqueue", "dequeue", "is_empty", "is_full"):
            assert hasattr(Q, method)

    def case_empty_on_creation():
        cls = student()
        Q = cls(4)
        assert Q.is_empty()
        assert not Q.is_full()

    def case_fifo_order():
        cls = student()
        Q = cls(4)
        for v in [1, 2, 3, 4]:
            Q.enqueue(v)
        assert Q.is_full()
        assert [Q.dequeue() for _ in range(4)] == [1, 2, 3, 4]
        assert Q.is_empty()

    def case_overflow():
        cls = student()
        Q = cls(2)
        Q.enqueue("a")
        Q.enqueue("b")
        try:
            Q.enqueue("c")
            assert False, "enqueue on full queue should raise OverflowError"
        except OverflowError:
            pass

    def case_underflow():
        cls = student()
        Q = cls(2)
        try:
            Q.dequeue()
            assert False, "dequeue on empty queue should raise IndexError"
        except IndexError:
            pass

    def case_wraparound():
        # This is the crucial test: fill, drain partially, fill again
        # so that tail wraps around past the end of the buffer.
        cls = student()
        Q = cls(3)
        Q.enqueue(1)   # buf: [1,_,_]  head=0 tail=1 size=1
        Q.enqueue(2)   # buf: [1,2,_]  head=0 tail=2 size=2
        assert Q.dequeue() == 1  # buf: [_,2,_]  head=1 tail=2 size=1
        Q.enqueue(3)   # buf: [_,2,3]  head=1 tail=0 size=2  <-- tail wrapped
        Q.enqueue(4)   # buf: [4,2,3]  head=1 tail=1 size=3  <-- full again
        assert Q.is_full()
        assert Q.dequeue() == 2
        assert Q.dequeue() == 3
        assert Q.dequeue() == 4
        assert Q.is_empty()

    def case_alternating_enqueue_dequeue():
        cls = student()
        Q = cls(2)
        for v in range(10):
            Q.enqueue(v)
            assert Q.dequeue() == v
        assert Q.is_empty()

    def case_interleaved_stress():
        cls = student()
        Q = cls(5)
        model = []
        ops = [
            ("e", 1), ("e", 2), ("e", 3), ("d", None), ("e", 4),
            ("d", None), ("e", 5), ("e", 6), ("e", 7), ("d", None),
            ("d", None), ("e", 8), ("d", None),
        ]
        for op, v in ops:
            if op == "e":
                Q.enqueue(v)
                model.append(v)
            else:
                assert Q.dequeue() == model.pop(0)
        # drain
        while model:
            assert Q.dequeue() == model.pop(0)

    return [
        ("build() returns a class", case_build_returns_class),
        ("empty on creation", case_empty_on_creation),
        ("FIFO ordering", case_fifo_order),
        ("overflow raises", case_overflow),
        ("underflow raises", case_underflow),
        ("wraparound works correctly", case_wraparound),
        ("alternating enqueue/dequeue", case_alternating_enqueue_dequeue),
        ("interleaved stress test", case_interleaved_stress),
    ]

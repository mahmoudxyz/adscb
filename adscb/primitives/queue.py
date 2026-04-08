"""Circular-buffer Queue matching the pseudocode in the slides.

Fixed capacity. `head`, `tail`, `size` are all integer attributes just
like in the slides. The modulo arithmetic is the key trick: it lets
enqueue and dequeue both run in O(1) without ever shifting elements.
"""


class CircularQueue:
    """Fixed-capacity circular queue.

        Q = CircularQueue(n)
        Q.enqueue(x)     # raises OverflowError if full
        Q.dequeue()      # raises IndexError if empty
        Q.is_empty()
        Q.is_full()
        Q.size           # number of elements currently in the queue
        Q.length         # capacity
    """

    def __init__(self, length=128):
        if not isinstance(length, int) or length <= 0:
            raise ValueError(f"Queue capacity must be positive int, got {length}")
        self._buf = [None] * length
        self._length = length
        self.head = 0
        self.tail = 0
        self.size = 0
        self.ops = 0

    @property
    def length(self):
        return self._length

    def is_empty(self):
        return self.size == 0

    def is_full(self):
        return self.size == self._length

    def enqueue(self, x):
        if self.size == self._length:
            raise OverflowError("queue overflow")
        self._buf[self.tail] = x
        self.tail = (self.tail + 1) % self._length
        self.size += 1
        self.ops += 1

    def dequeue(self):
        if self.size == 0:
            raise IndexError("queue underflow (dequeue from empty queue)")
        x = self._buf[self.head]
        self._buf[self.head] = None
        self.head = (self.head + 1) % self._length
        self.size -= 1
        self.ops += 1
        return x

    def peek(self):
        """Return the value at the front without dequeuing."""
        if self.size == 0:
            raise IndexError("queue is empty")
        return self._buf[self.head]

    def __repr__(self):
        if self.size == 0:
            return "Queue[empty]"
        items = []
        i = self.head
        for _ in range(self.size):
            items.append(repr(self._buf[i]))
            i = (i + 1) % self._length
        return f"Queue[front→ {', '.join(items)} ←back]"

    def __len__(self):
        return self.size

    def to_list(self):
        """Return elements front-to-back as a plain Python list."""
        out = []
        i = self.head
        for _ in range(self.size):
            out.append(self._buf[i])
            i = (i + 1) % self._length
        return out


# Default alias — when a problem says "use a Queue", this is what you get.
Queue = CircularQueue

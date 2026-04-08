"""Stack matching the pseudocode in the slides.

The stack is array-backed with a fixed capacity. `S.top` is an **index**
(0 means empty), exactly as in the slides. To read the value on top
without popping, call `S.peek()` — that's the method equivalent of
the pseudocode function `top(S)`.

Why fixed-size? Because the slides teach the cost of a dynamic stack
by first showing the fixed-size version. If you want a stack that
grows, you implement the dynamic-array version yourself as an exercise.
"""


class Stack:
    """Fixed-capacity stack.

        S = Stack(n)         # capacity n
        S.push(x)            # raises OverflowError if full
        S.pop()              # raises IndexError if empty
        S.peek()             # value on top, does not pop
        S.is_empty()
        S.top                # index of the top (0 = empty), matches slides
        S.length             # capacity
    """

    def __init__(self, length=128):
        if not isinstance(length, int) or length < 0:
            raise ValueError(f"Stack capacity must be non-negative int, got {length}")
        self._length = length
        # index 0 is unused; slots [1..length] are the stack
        self._data = [None] * (length + 1)
        self.top = 0
        self.ops = 0

    @property
    def length(self):
        return self._length

    def is_empty(self):
        return self.top == 0

    def is_full(self):
        return self.top == self._length

    def push(self, x):
        if self.top == self._length:
            raise OverflowError("stack overflow")
        self.top += 1
        self._data[self.top] = x
        self.ops += 1

    def pop(self):
        if self.top == 0:
            raise IndexError("stack underflow (pop from empty stack)")
        x = self._data[self.top]
        self._data[self.top] = None
        self.top -= 1
        self.ops += 1
        return x

    def peek(self):
        """Return the value on top without popping. Pseudocode's `top(S)`."""
        if self.top == 0:
            raise IndexError("stack is empty")
        return self._data[self.top]

    def __repr__(self):
        if self.top == 0:
            return "Stack[empty]"
        items = ", ".join(repr(self._data[i]) for i in range(1, self.top + 1))
        return f"Stack[bottom→ {items} ←top]"

    def __len__(self):
        return self.top

    @classmethod
    def from_list(cls, values, capacity=None):
        """Build a Stack from a Python list. values[0] ends up at the bottom."""
        cap = capacity if capacity is not None else max(len(values), 1)
        S = cls(cap)
        for v in values:
            S.push(v)
        S.ops = 0
        return S

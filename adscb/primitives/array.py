"""Fixed-size, 1-indexed Array matching the pseudocode notation A[1..n]."""


class Array:
    """A fixed-size, 1-indexed array.

    Created with `Array(n)` to get `A[1..n]`. All slots start at None
    (or whatever `init` you pass). Accessing A[0] or A[n+1] raises
    IndexError — no silent wraparound like Python lists.

    Unlike Python's list, this does not grow. That's the point: if
    you need to grow, you must copy to a new Array (and pay Θ(n)),
    which is exactly what the slides teach for dynamic arrays.

    Tracks .ops = number of read/write operations, useful for
    empirically checking your algorithm's complexity:

        A = Array(1000)
        # ... run your algorithm ...
        print(A.ops)   # how many array accesses did it make?
    """

    def __init__(self, n, init=None):
        if not isinstance(n, int):
            raise TypeError(f"Array size must be int, got {type(n).__name__}")
        if n < 0:
            raise ValueError(f"Array size must be non-negative, got {n}")
        # Index 0 is unused so indexing is 1-based.
        self._data = [init] * (n + 1)
        self._length = n
        self.ops = 0

    @property
    def length(self):
        """Matches A.length in pseudocode."""
        return self._length

    def __len__(self):
        return self._length

    def __getitem__(self, i):
        self._check(i)
        self.ops += 1
        return self._data[i]

    def __setitem__(self, i, value):
        self._check(i)
        self.ops += 1
        self._data[i] = value

    def _check(self, i):
        if not isinstance(i, int):
            raise TypeError(
                f"Array indices must be int, got {type(i).__name__}"
            )
        if i < 1 or i > self._length:
            raise IndexError(
                f"Array index {i} out of range [1..{self._length}]"
            )

    def __iter__(self):
        """Iterate from A[1] to A[n]."""
        for i in range(1, self._length + 1):
            yield self._data[i]

    def __repr__(self):
        items = ", ".join(repr(self._data[i]) for i in range(1, self._length + 1))
        return f"Array[{items}]"

    def reset_ops(self):
        """Zero the operation counter. Call before timing/counting a run."""
        self.ops = 0

    @classmethod
    def from_list(cls, values):
        """Build an Array from a Python list (convenience for tests)."""
        A = cls(len(values))
        for i, v in enumerate(values, start=1):
            A[i] = v
        A.reset_ops()  # setup doesn't count
        return A

    def to_list(self):
        """Return a plain Python list of the values (convenience for tests)."""
        return [self._data[i] for i in range(1, self._length + 1)]

META = {
    "id": "ch04/08_stack_queue_simulate",
    "title": "Simulate a stack or queue on a sequence",
    "chapter": 4,
    "chapter_title": "Chapter 4 — Elementary Data Structures",
    "difficulty": 2,
    "requires_recursion": False,
    "entry": "simulate",
}

DESCRIPTION = """
# Simulate a stack or queue on a sequence (Exercise 8)

You're given a sequence of characters where each letter means **push**
(or **enqueue**) that character, and each `*` means **pop** (or
**dequeue**). Return the sequence of characters that came out.

## Signature

```python
def simulate(sequence, kind):
    # sequence is a string like "E A S * Y * Q..."
    # kind is "stack" or "queue"
    # returns a string of characters popped/dequeued, in order
    ...
```

Spaces in the input sequence are separators and should be ignored.

## Examples

Input sequence:  `"E A S * Y * Q U E * * * S T * * * I O * N * * *"`

- As a **stack**:  `"SYEUQTSAONIE"`
- As a **queue**:  `"EASYQUESTION"`

(The lecture-notes PDF shows `"SYEUQTSAONI"` for the stack answer —
that's a typo in the solutions, missing the final `E`. The sequence
contains 12 asterisks so 12 characters must come out.)

## Notes

- Use `Stack` or `CircularQueue` from `adscb.primitives`. Pick size
  generously (say, 64).
- This is straight from Exercise 8 in the lecture notes.
- Hint: write it once with a big `if kind == "stack"` branch, or
  pick the right data structure up front and just push/pop through it.
"""

STARTER = '''\
from adscb.primitives import Stack, CircularQueue


def simulate(sequence, kind):
    """Return the string of chars popped/dequeued while processing the sequence."""
    # your code here
    pass
'''

HINTS = [
    "Tokenize by splitting on whitespace, then iterate. If a token is '*' do a pop/dequeue; otherwise push/enqueue it.",
    "Collect popped characters in a list and join at the end.",
    "Stack.pop() and CircularQueue.dequeue() have the same role here — just pick the right one based on `kind`.",
]


def reference(sequence, kind):
    from adscb.primitives import Stack, CircularQueue
    tokens = sequence.split()
    out = []
    if kind == "stack":
        S = Stack(1024)
        for t in tokens:
            if t == "*":
                out.append(S.pop())
            else:
                S.push(t)
    elif kind == "queue":
        Q = CircularQueue(1024)
        for t in tokens:
            if t == "*":
                out.append(Q.dequeue())
            else:
                Q.enqueue(t)
    else:
        raise ValueError(f"unknown kind: {kind}")
    return "".join(out)


def tests(student):
    SEQ = "E A S * Y * Q U E * * * S T * * * I O * N * * *"

    def case_stack():
        assert student(SEQ, "stack") == "SYEUQTSAONIE", \
            f"stack result wrong, got {student(SEQ, 'stack')!r}"

    def case_queue():
        assert student(SEQ, "queue") == "EASYQUESTION", \
            f"queue result wrong, got {student(SEQ, 'queue')!r}"

    def case_simple_stack():
        assert student("A B C * * *", "stack") == "CBA"

    def case_simple_queue():
        assert student("A B C * * *", "queue") == "ABC"

    def case_interleaved():
        # push A, push B, pop (B), push C, pop (C), pop (A)
        assert student("A B * C * *", "stack") == "BCA"
        # push A, push B, dequeue (A), push C, dequeue (B), dequeue (C)
        assert student("A B * C * *", "queue") == "ABC"

    def case_no_pops():
        assert student("X Y Z", "stack") == ""
        assert student("X Y Z", "queue") == ""

    def case_empty_input():
        assert student("", "stack") == ""
        assert student("", "queue") == ""

    return [
        ("stack: PDF example", case_stack),
        ("queue: PDF example", case_queue),
        ("simple stack LIFO", case_simple_stack),
        ("simple queue FIFO", case_simple_queue),
        ("interleaved ops", case_interleaved),
        ("no pops", case_no_pops),
        ("empty input", case_empty_input),
    ]

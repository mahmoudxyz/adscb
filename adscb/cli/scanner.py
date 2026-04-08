"""AST-based static warnings for student solutions.

This runs before the tests. It never blocks execution — it only prints
warnings. The philosophy is "suggest, don't enforce": if a problem
says 'requires recursion' and the student wrote it iteratively, they'll
see a yellow warning but the tests still run. If the solution actually
passes iteratively (unlikely if tests are written well), they still
get credit.
"""
import ast


def scan_solution(source_code, problem_meta):
    """Return a list of warning strings. Empty list means no warnings."""
    warnings = []

    try:
        tree = ast.parse(source_code)
    except SyntaxError as e:
        return [f"syntax error at line {e.lineno}: {e.msg}"]

    entry = problem_meta.get("entry", "solution")

    # --- warn if recursion expected but the entry function doesn't self-call
    if problem_meta.get("requires_recursion"):
        if not _function_calls_itself(tree, entry):
            warnings.append(
                f"this problem asks for a recursive solution, but `{entry}` "
                f"doesn't appear to call itself"
            )

    # --- hard forbids (still only warns, per project policy)
    forbids = problem_meta.get("forbids", [])
    if forbids:
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in forbids:
                        warnings.append(
                            f"line {node.lineno}: this problem suggests avoiding `{alias.name}`"
                        )
            elif isinstance(node, ast.ImportFrom):
                if node.module and node.module in forbids:
                    warnings.append(
                        f"line {node.lineno}: this problem suggests avoiding `{node.module}`"
                    )

    # --- soft nudge: suggest using primitives instead of Python lists
    suggest = problem_meta.get("suggest_primitives")
    if suggest:
        for node in ast.walk(tree):
            if isinstance(node, ast.List):
                warnings.append(
                    f"line {node.lineno}: you're using a Python list literal `[]` — "
                    f"the pseudocode model uses {' / '.join(suggest)} "
                    f"from adscb.primitives. This still passes, just something to notice."
                )
                break  # one nudge is enough, don't spam
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "list"
            ):
                warnings.append(
                    f"line {node.lineno}: you're calling `list(...)` — "
                    f"consider {' / '.join(suggest)} from adscb.primitives"
                )
                break

    return warnings


def _function_calls_itself(tree, fname):
    """True if a function named `fname` in the tree contains a call to itself."""
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == fname:
            for inner in ast.walk(node):
                if isinstance(inner, ast.Call):
                    # plain `fname(...)`
                    if isinstance(inner.func, ast.Name) and inner.func.id == fname:
                        return True
                    # `something.fname(...)` — unusual but possible
                    if isinstance(inner.func, ast.Attribute) and inner.func.attr == fname:
                        return True
    return False

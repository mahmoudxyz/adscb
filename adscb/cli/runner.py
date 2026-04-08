"""Run a student's solution against a problem's tests.

We import the student file as a module. Any import-time exception
is captured and reported as a single failing 'import' case so the
tool never crashes, no matter how broken the student code is.
"""
import importlib.util
import traceback


def _load_student_module(path):
    spec = importlib.util.spec_from_file_location("adscb_student_solution", path)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception:
        return None, traceback.format_exc()
    return mod, None


def run_tests(problem_module, workspace_path):
    """Run all test cases for `problem_module` using the student's code.

    Returns (passed, total, results) where results is a list of tuples
    (case_name, ok_bool, error_message_or_None).
    """
    student_mod, err = _load_student_module(workspace_path)
    if err:
        return 0, 1, [("import your file", False, f"import failed:\n{err}")]

    entry = problem_module.META.get("entry", "solution")
    if not hasattr(student_mod, entry):
        return 0, 1, [(
            "find entry function",
            False,
            f"your file must define a function called `{entry}`",
        )]

    student_fn = getattr(student_mod, entry)

    try:
        cases = problem_module.tests(student_fn)
    except Exception:
        return 0, 1, [("set up tests", False, f"test setup failed:\n{traceback.format_exc()}")]

    results = []
    passed = 0
    for name, fn in cases:
        try:
            fn()
        except AssertionError as e:
            results.append((name, False, str(e) or "assertion failed"))
            continue
        except Exception as e:
            results.append((name, False, f"{type(e).__name__}: {e}"))
            continue
        results.append((name, True, None))
        passed += 1

    return passed, len(cases), results

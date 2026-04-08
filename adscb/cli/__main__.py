"""`adscb` command entry point."""
import argparse
import sys

from . import commands


def build_parser():
    parser = argparse.ArgumentParser(
        prog="adscb",
        description="Algorithms & Data Structures for Computational Biology — practice tool",
    )
    sub = parser.add_subparsers(dest="cmd", metavar="COMMAND")

    sub.add_parser("list", help="list all chapters and problems")
    sub.add_parser("status", help="show progress summary")

    p = sub.add_parser("show", help="show a problem's description")
    p.add_argument("problem_id", help="problem id or unique suffix")

    p = sub.add_parser("start", help="create the workspace file and show the problem")
    p.add_argument("problem_id")

    p = sub.add_parser("edit", help="open the workspace file in $EDITOR")
    p.add_argument("problem_id")

    p = sub.add_parser("test", help="run tests on your solution")
    p.add_argument("problem_id")

    p = sub.add_parser("hint", help="reveal the next hint")
    p.add_argument("problem_id")

    p = sub.add_parser("solution", help="show the reference solution (must be solved first)")
    p.add_argument("problem_id")
    p.add_argument("--force", action="store_true", help="show even if unsolved")

    p = sub.add_parser("reset", help="reset workspace file to the starter template")
    p.add_argument("problem_id")

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.cmd is None:
        commands.cmd_status(args)
        parser.print_help()
        return 0

    handlers = {
        "list": commands.cmd_list,
        "status": commands.cmd_status,
        "show": commands.cmd_show,
        "start": commands.cmd_start,
        "edit": commands.cmd_edit,
        "test": commands.cmd_test,
        "hint": commands.cmd_hint,
        "solution": commands.cmd_solution,
        "reset": commands.cmd_reset,
    }
    handler = handlers[args.cmd]
    handler(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())

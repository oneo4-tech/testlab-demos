#!/usr/bin/env python3
"""Flag Python tests that cannot fail for a reason that matters.

Usage: python find_self_mocks.py TEST_FILE [TEST_FILE ...]

Two findings per test function:
  self-mock    it patches a name (patch / patch.object) and then calls that same name,
               so it checks the mock, not the code
  empty-assert every assert only checks that a result exists (is not None, truthy)

Prints one line per finding and exits 1 when there is any, 0 when there is none.
Standard library only.
"""

import ast
import sys


def _patched_names(node: ast.AST) -> set[str]:
    """Attribute names patched inside node: patch.object(x, "name") and patch("pkg.mod.name")."""
    names = set()
    for call in ast.walk(node):
        if not isinstance(call, ast.Call):
            continue
        func = call.func
        dotted = ast.unparse(func)
        args = [a.value for a in call.args if isinstance(a, ast.Constant) and isinstance(a.value, str)]
        if dotted.endswith("patch.object") and args:
            names.add(args[0])
        elif dotted.split(".")[-1] == "patch" and args:
            names.add(args[0].rsplit(".", 1)[-1])
    return names


def _called_names(node: ast.AST) -> set[str]:
    names = set()
    for call in ast.walk(node):
        if isinstance(call, ast.Call):
            func = call.func
            if isinstance(func, ast.Attribute):
                names.add(func.attr)
            elif isinstance(func, ast.Name):
                names.add(func.id)
    return names


def _is_existence_check(test: ast.expr) -> bool:
    if isinstance(test, ast.Compare) and len(test.ops) == 1:
        op, right = test.ops[0], test.comparators[0]
        return isinstance(op, ast.IsNot) and isinstance(right, ast.Constant) and right.value is None
    return isinstance(test, (ast.Name, ast.Attribute))


def findings(source: str, path: str) -> list[str]:
    found = []
    for func in ast.walk(ast.parse(source)):
        if not (isinstance(func, ast.FunctionDef) and func.name.startswith("test")):
            continue
        for name in sorted(_patched_names(func) & _called_names(func)):
            found.append(f"{path}:{func.lineno}: {func.name}: self-mock: patches {name} and then calls it")
        asserts = [n for n in ast.walk(func) if isinstance(n, ast.Assert)]
        if asserts and all(_is_existence_check(a.test) for a in asserts):
            found.append(f"{path}:{func.lineno}: {func.name}: empty-assert: only checks that a result exists")
    return found


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__.strip().splitlines()[2], file=sys.stderr)
        return 2
    found = []
    for path in argv:
        with open(path) as handle:
            found += findings(handle.read(), path)
    print("\n".join(found) or "no findings")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

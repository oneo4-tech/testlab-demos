#!/usr/bin/env python3
"""Flag Python tests that cannot fail for a reason that matters.

Usage: python find_self_mocks.py TEST_FILE [TEST_FILE ...]

Two findings per test function:
  self-mock    it patches a function of the module it then calls into (patch.object(mod,
               "name") followed by mod.something(...)), so the logic it claims to test is a
               fake; patch what the code talks to (a client, the clock), never the module
               under test
  empty-assert every assert only checks that a result exists or has a type (is not None,
               truthy, isinstance)

Prints one line per finding and exits 1 when there is any, 0 when there is none.
Standard library only.
"""

import ast
import sys


def _patches(node: ast.AST) -> list[tuple[str, str]]:
    """(module, name) for each patch.object(module, "name") and patch("pkg.module.name") inside node."""
    found = []
    for call in ast.walk(node):
        if not isinstance(call, ast.Call):
            continue
        dotted = ast.unparse(call.func)
        strings = [a.value for a in call.args if isinstance(a, ast.Constant) and isinstance(a.value, str)]
        if dotted.endswith("patch.object") and call.args and strings:
            found.append((ast.unparse(call.args[0]), strings[0]))
        elif dotted.split(".")[-1] == "patch" and strings and "." in strings[0]:
            module, name = strings[0].rsplit(".", 1)
            found.append((module.rsplit(".", 1)[-1], name))
    return found


def _called_modules(node: ast.AST) -> set[str]:
    """The objects whose attributes the test calls: mod for mod.f(...)."""
    return {
        ast.unparse(call.func.value)
        for call in ast.walk(node)
        if isinstance(call, ast.Call) and isinstance(call.func, ast.Attribute)
    }


def _is_existence_check(test: ast.expr) -> bool:
    if isinstance(test, ast.Compare) and len(test.ops) == 1:
        op, right = test.ops[0], test.comparators[0]
        return isinstance(op, ast.IsNot) and isinstance(right, ast.Constant) and right.value is None
    if isinstance(test, ast.Call) and isinstance(test.func, ast.Name):
        return test.func.id in {"isinstance", "bool", "callable"}
    return isinstance(test, (ast.Name, ast.Attribute))


def findings(source: str, path: str) -> list[str]:
    found = []
    for func in ast.walk(ast.parse(source)):
        if not (isinstance(func, ast.FunctionDef) and func.name.startswith("test")):
            continue
        called = _called_modules(func)
        for module, name in _patches(func):
            if module in called:
                found.append(
                    f"{path}:{func.lineno}: {func.name}: self-mock: patches {module}.{name}, "
                    f"part of the code under test, then calls into {module}"
                )
        asserts = [n for n in ast.walk(func) if isinstance(n, ast.Assert)]
        if asserts and all(_is_existence_check(a.test) for a in asserts):
            found.append(f"{path}:{func.lineno}: {func.name}: empty-assert: only checks that a result exists")
    return found


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: python find_self_mocks.py TEST_FILE [TEST_FILE ...]", file=sys.stderr)
        return 2
    found = []
    for path in argv:
        with open(path) as handle:
            found += findings(handle.read(), path)
    print("\n".join(found) or "no findings")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

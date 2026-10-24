#!/usr/bin/env python3
"""Break the code on purpose, one operator at a time, and see which faults the tests catch.

Usage: python mutation_smoke.py SOURCE_FILE -- TEST_COMMAND ...

For each comparison or arithmetic operator in SOURCE_FILE it makes one mutant (< to <=,
<= to <, + to -, - to +, == to !=, ...), writes it into a temporary copy of the current
folder, and runs TEST_COMMAND there. A failing run kills the mutant; a passing run means it
lived. Your files are never changed. Standard library only; a small cousin of tools like
PIT (pitest.org) and mutmut.

It first runs TEST_COMMAND on an unchanged copy: tests that fail before any mutation would
make every mutant look killed, so it refuses (exit 2) and shows their output.

Prints each mutant with killed or LIVED, then the score, and exits 0 when every mutant is
killed, 1 when any lived, 2 on bad input or failing tests.
"""

import ast
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SWAPS = {
    ast.Lt: ast.LtE, ast.LtE: ast.Lt, ast.Gt: ast.GtE, ast.GtE: ast.Gt,
    ast.Eq: ast.NotEq, ast.NotEq: ast.Eq,
    ast.Add: ast.Sub, ast.Sub: ast.Add, ast.Mult: ast.Div, ast.Div: ast.Mult,
}  # fmt: skip


def _sites(tree: ast.AST) -> list[tuple[ast.AST, int]]:
    """Each (node, index) holding a swappable operator: index is the comparator position, or -1."""
    sites = []
    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp) and type(node.op) in SWAPS:
            sites.append((node, -1))
        elif isinstance(node, ast.Compare):
            sites += [(node, i) for i, op in enumerate(node.ops) if type(op) in SWAPS]
    return sites


def mutants(source: str) -> list[tuple[str, str]]:
    """Each mutant as (description, mutated source)."""
    out = []
    count = len(_sites(ast.parse(source)))
    for k in range(count):
        tree = ast.parse(source)
        node, index = _sites(tree)[k]
        before = ast.unparse(node)
        if index < 0:
            node.op = SWAPS[type(node.op)]()
        else:
            node.ops[index] = SWAPS[type(node.ops[index])]()
        out.append((f"line {node.lineno}: {before}  ->  {ast.unparse(node)}", ast.unparse(tree) + "\n"))
    return out


class TestsFail(Exception):
    """The tests fail on the unchanged code; the message holds their output."""


def _run_in_copy(root: Path, relative: Path, text: str, command: list[str]) -> subprocess.CompletedProcess:
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    with tempfile.TemporaryDirectory() as tmp:
        copy = Path(tmp) / "project"
        shutil.copytree(root, copy, ignore=shutil.ignore_patterns(".git", "__pycache__", ".venv"))
        (copy / relative).write_text(text)
        return subprocess.run(command, cwd=copy, env=env, capture_output=True, text=True)


def run(source_file: Path, command: list[str]) -> list[tuple[str, bool]]:
    """Each mutant's description and whether the tests killed it."""
    root = Path.cwd()
    relative = source_file.resolve().relative_to(root)
    source = source_file.read_text()
    baseline = _run_in_copy(root, relative, source, command)
    if baseline.returncode != 0:
        raise TestsFail((baseline.stdout + baseline.stderr).strip()[-2000:])
    return [
        (description, _run_in_copy(root, relative, mutated, command).returncode != 0)
        for description, mutated in mutants(source)
    ]


def main(argv: list[str]) -> int:
    if "--" not in argv or argv.index("--") != 1 or len(argv) < 3:
        print("usage: python mutation_smoke.py SOURCE_FILE -- TEST_COMMAND ...", file=sys.stderr)
        return 2
    source_file, command = Path(argv[0]), argv[2:]
    if not source_file.is_file():
        print(f"no such file: {source_file}", file=sys.stderr)
        return 2
    try:
        results = run(source_file, command)
    except TestsFail as error:
        print(f"the tests fail before any mutation; fix them first:\n{error}", file=sys.stderr)
        return 2
    for description, killed in results:
        print(f"{'killed' if killed else 'LIVED '}  {description}")
    killed = sum(k for _, k in results)
    print(f"{killed} of {len(results)} mutants killed")
    return 0 if killed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

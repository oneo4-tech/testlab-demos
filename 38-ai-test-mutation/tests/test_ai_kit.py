import subprocess
import sys
from pathlib import Path

FOLDER = Path(__file__).resolve().parent.parent
KIT = FOLDER / "ai-kit" / "scripts"


def kit(script, *args):
    return subprocess.run([sys.executable, str(KIT / script), *args], cwd=FOLDER, capture_output=True, text=True)


def test_find_self_mocks_flags_both_ai_tests():
    done = kit("find_self_mocks.py", "tests/test_discount_ai.py")
    assert done.returncode == 1
    assert "test_apply_discount: self-mock" in done.stdout
    assert "test_apply_discount_runs: empty-assert" in done.stdout


def test_find_self_mocks_passes_the_testers_tests():
    done = kit("find_self_mocks.py", "tests/test_discount_real.py")
    assert done.returncode == 0, done.stdout


def pytest_on(test_file):
    return ["--", sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", test_file]


def test_mutation_smoke_ai_tests_kill_nothing():
    done = kit("mutation_smoke.py", "demo/discount.py", *pytest_on("tests/test_discount_ai.py"))
    assert done.returncode == 1
    assert "0 of 5 mutants killed" in done.stdout


def test_mutation_smoke_testers_tests_kill_every_mutant():
    done = kit("mutation_smoke.py", "demo/discount.py", *pytest_on("tests/test_discount_real.py"))
    assert done.returncode == 0, done.stdout
    assert "5 of 5 mutants killed" in done.stdout


def test_mutation_smoke_leaves_the_code_unchanged():
    before = (FOLDER / "demo" / "discount.py").read_text()
    kit("mutation_smoke.py", "demo/discount.py", *pytest_on("tests/test_discount_ai.py"))
    assert (FOLDER / "demo" / "discount.py").read_text() == before


def test_mutation_smoke_refuses_when_the_tests_fail_before_any_mutation():
    done = kit("mutation_smoke.py", "demo/discount.py", "--", sys.executable, "-c", "raise SystemExit(1)")
    assert done.returncode == 2
    assert "fail before any mutation" in done.stderr

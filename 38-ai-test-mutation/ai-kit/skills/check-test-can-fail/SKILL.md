---
name: check-test-can-fail
description: Use after writing or changing unit tests, or when asked to review tests, to prove each test can fail for a reason that matters. Flags tests that mock the unit under test or assert only that a result exists, then breaks the code on purpose and reports which faults the tests caught.
---

# Check the test can fail

## Procedure

1. **Name the unit under test** for each new or changed test, and the behaviour it claims to check.
2. **Find self-mocks and empty asserts:** run `python ai-kit/scripts/find_self_mocks.py <test files>`. Fix every finding: patch only collaborators, never the function the test calls; assert the exact expected value.
3. **Answer the tester's question** for each test in one line: "This test fails if ...". No answer means the test is not done.
4. **Break the code on purpose:** run `python ai-kit/scripts/mutation_smoke.py <source file> -- <test command>`, for example `python ai-kit/scripts/mutation_smoke.py src/discount.py -- python -m pytest -q tests/test_discount.py`. It flips one operator at a time in a temporary copy of the project and runs the tests; your files are never changed.
5. **Close the gaps:** for each surviving mutant that changes behaviour a user would notice, add or sharpen a test until it is killed. A surviving mutant that changes nothing observable may stay; say why.
6. **Report:** the self-mock findings fixed, each test's "fails if" line, and the killed and surviving mutants.

## Done when

- `find_self_mocks.py` reports nothing for the changed tests.
- Every surviving mutant is either killed or explained.

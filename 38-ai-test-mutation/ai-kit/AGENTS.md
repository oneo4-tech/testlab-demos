## Tests you write (OneO4TestLab: "This AI Test Passes and Tests Nothing")

Paste this section into your AGENTS.md, CLAUDE.md, Cursor rules, or Copilot instructions.

- Before you call a test done, name the change to the code under test that would make it fail. If you cannot name one, the test is not done.
- Never mock or patch the unit under test. Mock only what it talks to: network, clock, files, other services.
- Assert the exact expected value or behaviour. A test that only checks a result exists (`is not None`, truthy, no exception) is not enough.
- Test each boundary the code states: the limit itself, just inside, and just outside.
- Prove each new test can fail: break the code on purpose (flip a sign, move a boundary), show the test fails, then restore the code.
- Report which deliberate faults your tests caught and which survived. Fix the tests until the faults that matter are caught.

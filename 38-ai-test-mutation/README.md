# Spot the Bug: the AI test that tests nothing

The demo for a video of the OneO4TestLab channel.

## What it proves

In a realistic checkout (prices in cents, coupon codes, a tax service), a one-character mutation leaves the AI-written tests green while a tester's tests fail.

## Layout

- `demo/`: the code the video shows.
- `tests/`: the tests that prove the claim; they pass.
- `ai-kit/`: rules, an agent skill, and scripts that make an AI agent check its tests can fail.
- `demo.tape`: the [VHS](https://github.com/charmbracelet/vhs) tape that records the terminal demo.

## How to run

Needs [uv](https://docs.astral.sh/uv/). From this folder:

```sh
uv run --with pytest python -m pytest -q tests
```

Then break the code on purpose and watch which tests notice:

```sh
./demo/mutate.sh
```

It prints the changed line, flips one sign so the coupon becomes a markup, runs both test files, and restores the code. The AI-written tests stay green; the tester's tests fail. `./demo/mutate.sh boundary` tries a second mutant: a 100% coupon is refused, and only the tester's tests notice.

Record the terminal demo with `vhs demo.tape`; it writes `demo.mp4`, which git ignores.

## Use it with your AI agent

The `ai-kit/` folder makes a coding agent ask the question this video is about: what would make this test fail?

- `ai-kit/AGENTS.md`: rules to paste into your AGENTS.md, CLAUDE.md, Cursor rules, or Copilot instructions.
- `ai-kit/skills/check-test-can-fail/`: an agent skill. For Claude Code, copy it into your project:

  ```sh
  mkdir -p .claude/skills && cp -r ai-kit/skills/check-test-can-fail .claude/skills/
  ```

  Other agents that read `SKILL.md` folders (for example under `.agents/skills/`) take the same folder.
- `ai-kit/scripts/find_self_mocks.py`: flags tests that patch the function they call, or only check that a result exists.

  ```sh
  ai-kit/scripts/find_self_mocks.py tests/test_checkout_ai.py
  ```

- `ai-kit/scripts/mutation_smoke.py`: breaks your code one operator at a time, in a temporary copy, and reports which faults your tests caught.

  ```sh
  ai-kit/scripts/mutation_smoke.py demo/checkout.py -- uvx pytest tests/test_checkout_real.py
  ```

Both scripts use only the Python standard library; copy them into any project.

## Video

- Video: not published yet
- Channel: [OneO4TestLab](https://www.youtube.com/@OneO4TestLab)
- This folder: https://github.com/oneo4-tech/testlab-demos/tree/main/38-ai-test-mutation

## Sources

The video's claims, each with the line quoted from its source; each link opens the page at that line.

- patch.object swaps an attribute of an object for a mock "patch the named member (attribute) on an object (target) with a mock object." ([source](https://docs.python.org/3/library/unittest.mock.html#:~:text=patch%20the%20named%20member,a%20mock%20object.))
- Inside the with block, the patched target is the fake, not the real code "Inside the body of the function or with statement, the target is patched with a new object." ([source](https://docs.python.org/3/library/unittest.mock.html#:~:text=Inside%20the%20body%20of,a%20new%20object.))
- return_value sets what the fake hands back "Set this to configure the value returned by calling the mock:" ([source](https://docs.python.org/3/library/unittest.mock.html#:~:text=Set%20this%20to%20configure,calling%20the%20mock%3A))
- Checking is the mechanistic process of verifying propositions about the product "Checking is the mechanistic process of verifying propositions about the product." ([source](https://www.satisfice.com/blog/archives/856#:~:text=Checking%20is%20the%20mechanistic,about%20the%20product.))
- Testing is evaluating a product by learning about it through experiencing, exploring, and experimenting "Testing is the process of evaluating a product by learning about it through experiencing, exploring, and experimenting, which includes to some degree: questioning, study, modeling, observation, inference, etc." ([source](https://www.satisfice.com/blog/archives/856#:~:text=Testing%20is%20the%20process,observation%2C%20inference%2C%20etc.))
- Mutation testing seeds faults into your code, then runs your tests "are automatically seeded into your code, then your tests are run." ([source](https://pitest.org/#:~:text=are%20automatically%20seeded%20into,tests%20are%20run.))
- If the tests fail the mutation is killed; if they pass it lived "If your tests fail then the mutation is killed, if your tests pass then the mutation lived." ([source](https://pitest.org/#:~:text=If%20your%20tests%20fail,the%20mutation%20lived.))
- Test quality can be gauged from the share of mutations killed "The quality of your tests can be gauged from the percentage of mutations killed." ([source](https://pitest.org/#:~:text=The%20quality%20of%20your,of%20mutations%20killed.))

## Licence

MIT; see `LICENSE` at the repository root.

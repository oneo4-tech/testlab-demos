# Records the terminal demo of 38-ai-test-mutation. Run from this folder: vhs demo.tape
# The settings match the channel's screen capture rules; the Show part types the steps that prove the claim.
Output demo.mp4
Set Shell zsh
Set FontFamily "Menlo"
Set FontSize 30
Set Width 1920
Set Height 1080
Set Padding 48
Set Theme "Dracula"
Set TypingSpeed 45ms
Set WindowBar Colorful

Hide
Type `setopt interactivecomments && alias pytest='uv run -q --with pytest python -m pytest -p no:cacheprovider' && export PS1=$'\n%F{green}testlab%f $ ' && clear` Enter
Show
Sleep 500ms
# scene: sign
Type "# both test files pass on the correct code" Enter
Sleep 800ms
Type "pytest -q tests/test_checkout_ai.py tests/test_checkout_real.py" Sleep 300ms Enter
Sleep 4s
Type "# break the code: the coupon becomes a markup" Enter
Sleep 1s
Type "./demo/mutate.sh" Sleep 300ms Enter
Sleep 9s
# scene: boundary
Type "# a second mutant: a 100% coupon is now refused" Enter
Sleep 1s
Type "./demo/mutate.sh boundary" Sleep 300ms Enter
Sleep 12s
# scene: kit
Type "# the AI kit, step 1: tests that mock the code they test" Enter
Sleep 800ms
Type "ai-kit/scripts/find_self_mocks.py tests/test_checkout_ai.py" Sleep 300ms Enter
Sleep 5s
Type "# step 2: break the code eight ways. Do the AI tests notice?" Enter
Sleep 800ms
Type "ai-kit/scripts/mutation_smoke.py demo/checkout.py -- uvx pytest tests/test_checkout_ai.py" Sleep 300ms Enter
Sleep 12s
Type "clear" Enter
Type "# and the tester's tests?" Enter
Sleep 800ms
Type "ai-kit/scripts/mutation_smoke.py demo/checkout.py -- uvx pytest tests/test_checkout_real.py" Sleep 300ms Enter
Sleep 12s

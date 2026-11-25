# Records the terminal demo of 38-ai-test-mutation. Run from this folder: vhs demo.tape
# The settings match the channel's screen capture rules; each scene's steps are timed to its narration.
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
Type "./demo/mutate.sh restore 2>/dev/null; setopt interactivecomments && alias pytest='uv run -q --with pytest python -m pytest -p no:cacheprovider --tb=no' && export PS1='%F{green}testlab%f $ ' && c=1 && zshaddhistory() { [[ $1 == '#'* ]] && c=1 || c=0; } && precmd() { (( c )) || echo; } && clear" Enter
Show
Sleep 500ms
# scene: sign
Type "# both test files pass on the correct code" Enter
Sleep 810ms
Type@25ms "pytest -q tests/test_checkout_ai.py tests/test_checkout_real.py" Sleep 300ms Enter
Sleep 2925ms
Type "# break the code: the coupon becomes a markup" Enter
Sleep 1975ms
Type "./demo/mutate.sh" Sleep 300ms Enter
Sleep 10980ms
Type "# the AI tests vs the broken code" Enter
Sleep 415ms
Type@25ms "pytest -q tests/test_checkout_ai.py" Sleep 300ms Enter
Sleep 1425ms
Type "# the tester's tests" Enter
Sleep 300ms
Type@25ms "pytest -q tests/test_checkout_real.py" Sleep 300ms Enter
Sleep 3075ms
# scene: boundary
Type "# a second mutant: a 100% coupon is now refused" Enter
Sleep 1485ms
Type "./demo/mutate.sh boundary" Sleep 300ms Enter
Sleep 9975ms
Type "# the AI tests vs the broken code" Enter
Sleep 115ms
Type@25ms "pytest -q tests/test_checkout_ai.py" Sleep 300ms Enter
Sleep 1225ms
Type "# the tester's tests" Enter
Type@25ms "pytest -q tests/test_checkout_real.py" Sleep 300ms Enter
Sleep 3875ms
# scene: kit
Type "# the first script of the kit: tests that mock the code they test" Enter
Sleep 4680ms
Type@25ms "ai-kit/scripts/find_self_mocks.py tests/test_checkout_ai.py" Sleep 300ms Enter
Sleep 8125ms
Type "# next, the second script: break the code eight ways. Do the AI tests notice?" Enter
Sleep 700ms
Type@25ms "ai-kit/scripts/mutation_smoke.py demo/checkout.py -- uvx pytest tests/test_checkout_ai.py" Sleep 300ms Enter
Sleep 8275ms
Type "# and the tester's tests?" Enter
Sleep 75ms
Type@25ms "ai-kit/scripts/mutation_smoke.py demo/checkout.py -- uvx pytest tests/test_checkout_real.py" Sleep 300ms Enter
Sleep 12725ms

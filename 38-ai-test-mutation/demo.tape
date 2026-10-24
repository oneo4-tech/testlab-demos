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
Type "setopt interactivecomments && alias pytest='uv run -q --with pytest python -m pytest -p no:cacheprovider' && export PS1='%F{green}testlab%f $ ' && clear" Enter
Show
Sleep 500ms
Type "# both test files pass on the correct code" Enter
Sleep 800ms
Type "pytest -q tests" Sleep 300ms Enter
Sleep 4s
Type "# now break the code: the discount becomes a markup" Enter
Sleep 1s
Type "./demo/mutate.sh" Sleep 300ms Enter
Sleep 8s
Type "# a second mutant: a full discount is now refused" Enter
Sleep 1s
Type "./demo/mutate.sh boundary" Sleep 300ms Enter
Sleep 8s

#!/bin/sh
# Break the code on purpose and show the change, so you can run the tests against it; then restore it.
#   ./demo/mutate.sh            sign: the coupon becomes a markup
#   ./demo/mutate.sh boundary   boundary: a 100% coupon is refused
#   ./demo/mutate.sh restore    put the correct code back
# No bytecode is written or kept: a cached copy of the broken code would outlive the restore.
cd "$(dirname "$0")/.."
export PYTHONDONTWRITEBYTECODE=1
clean() { find . -name __pycache__ -prune -exec rm -r {} +; }
case "${1:-sign}" in
  sign) from='(1 - percent / 100)'; to='(1 + percent / 100)' ;;
  boundary) from='percent <= 100'; to='percent < 100' ;;
  restore)
    [ -f demo/checkout.py.orig ] || { echo "nothing to restore" >&2; exit 1; }
    mv demo/checkout.py.orig demo/checkout.py && clean && exit 0 ;;
  *) echo "usage: ./demo/mutate.sh [sign|boundary|restore]" >&2; exit 2 ;;
esac
if [ -f demo/checkout.py.orig ]; then
  echo "already mutated; run ./demo/mutate.sh restore first" >&2; exit 1
fi
cp demo/checkout.py demo/checkout.py.orig
clean
python3 - "$from" "$to" <<'PY'
import sys
path = "demo/checkout.py"
text = open(path).read()
old, new = sys.argv[1], sys.argv[2]
line = next(l for l in text.splitlines() if old in l)
open(path, "w").write(text.replace(old, new, 1))
print(f"- {line.strip()}\n+ {line.replace(old, new).strip()}")
PY

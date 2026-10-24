#!/bin/sh
# Break the code on purpose, show the change, run both test files, then restore it.
#   ./demo/mutate.sh            sign: the coupon becomes a markup
#   ./demo/mutate.sh boundary   boundary: a 100% coupon is refused
# No bytecode is written or kept: a cached copy of the broken code would outlive the restore.
cd "$(dirname "$0")/.."
export PYTHONDONTWRITEBYTECODE=1
case "${1:-sign}" in
  sign) from='(1 - percent / 100)'; to='(1 + percent / 100)' ;;
  boundary) from='percent <= 100'; to='percent < 100' ;;
  *) echo "usage: ./demo/mutate.sh [sign|boundary]" >&2; exit 2 ;;
esac
cp demo/checkout.py demo/checkout.py.orig
trap 'mv demo/checkout.py.orig demo/checkout.py; find . -name __pycache__ -prune -exec rm -r {} +' EXIT
python3 - "$from" "$to" <<'PY'
import sys
path = "demo/checkout.py"
text = open(path).read()
old, new = sys.argv[1], sys.argv[2]
line = next(l for l in text.splitlines() if old in l)
open(path, "w").write(text.replace(old, new, 1))
print(f"- {line.strip()}\n+ {line.replace(old, new).strip()}")
PY
echo
echo "== AI tests vs broken code =="
uv run -q --with pytest python -m pytest -q -p no:cacheprovider tests/test_checkout_ai.py 2>&1 | tail -1
echo "== Tester's tests vs broken code =="
uv run -q --with pytest python -m pytest -q -p no:cacheprovider tests/test_checkout_real.py 2>&1 | tail -1

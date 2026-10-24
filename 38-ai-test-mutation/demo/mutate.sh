#!/bin/sh
# Break the code on purpose, run both test files, then restore it.
#   ./demo/mutate.sh            sign: the discount becomes a markup
#   ./demo/mutate.sh boundary   boundary: a 100% discount is refused
# No bytecode is written or kept: a cached copy of the broken code would outlive the restore.
cd "$(dirname "$0")/.."
export PYTHONDONTWRITEBYTECODE=1
case "${1:-sign}" in
  sign) edit='s/(1 - percent \/ 100)/(1 + percent \/ 100)/' ;;
  boundary) edit='s/percent <= 100/percent < 100/' ;;
  *) echo "usage: ./demo/mutate.sh [sign|boundary]" >&2; exit 2 ;;
esac
cp demo/discount.py demo/discount.py.orig
trap 'mv demo/discount.py.orig demo/discount.py; find . -name __pycache__ -prune -exec rm -r {} +' EXIT
sed -i.bak "$edit" demo/discount.py && rm -f demo/discount.py.bak
echo "== AI tests vs broken code =="
uv run -q --with pytest python -m pytest -q -p no:cacheprovider tests/test_discount_ai.py 2>&1 | tail -1
echo "== Tester's tests vs broken code =="
uv run -q --with pytest python -m pytest -q -p no:cacheprovider tests/test_discount_real.py 2>&1 | tail -1

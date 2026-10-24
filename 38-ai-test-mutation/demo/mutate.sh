#!/bin/sh
# Break the code on purpose (discount becomes markup), run both test files, then restore it.
# No bytecode is written or kept: a cached copy of the broken code would outlive the restore.
cd "$(dirname "$0")/.."
export PYTHONDONTWRITEBYTECODE=1
cp demo/discount.py demo/discount.py.orig
trap 'mv demo/discount.py.orig demo/discount.py; find . -name __pycache__ -prune -exec rm -r {} +' EXIT
sed -i.bak 's/(1 - percent \/ 100)/(1 + percent \/ 100)/' demo/discount.py && rm -f demo/discount.py.bak
echo "== AI tests vs broken code =="
uv run -q --with pytest python -m pytest -q -p no:cacheprovider tests/test_discount_ai.py 2>&1 | tail -1
echo "== Tester's tests vs broken code =="
uv run -q --with pytest python -m pytest -q -p no:cacheprovider tests/test_discount_real.py 2>&1 | tail -1

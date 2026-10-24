from unittest.mock import Mock, patch

from demo import checkout

CART = [(2499, 2), (4992, 1)]


def test_order_total_applies_coupon():
    tax = Mock(rate=Mock(return_value=0.0))
    with patch.object(checkout, "apply_coupon", return_value=8991):
        total = checkout.order_total(CART, "SAVE10", tax)
    assert total == 8991


def test_order_total_returns_cents():
    tax = Mock(rate=Mock(return_value=0.19))
    total = checkout.order_total(CART, "SAVE10", tax)
    assert isinstance(total, int)

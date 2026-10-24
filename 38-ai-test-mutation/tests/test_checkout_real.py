import pytest

from demo.checkout import apply_coupon, order_total

CART = [(2499, 2), (4992, 1)]  # 9990 cents


class FlatTax:
    """A stand-in for the tax service: the collaborator, not the code under test."""

    def __init__(self, rate):
        self._rate = rate

    def rate(self):
        return self._rate


def test_save10_takes_ten_percent_off():
    assert apply_coupon(9990, 10) == 8991


def test_zero_percent_keeps_the_price():
    assert apply_coupon(9990, 0) == 9990


def test_free100_makes_it_free():
    assert apply_coupon(9990, 100) == 0


@pytest.mark.parametrize("percent", [-1, 101])
def test_out_of_range_percent_is_refused(percent):
    with pytest.raises(ValueError):
        apply_coupon(9990, percent)


def test_tax_is_added_after_the_coupon():
    assert order_total(CART, "SAVE10", FlatTax(0.19)) == 10699


def test_no_coupon_keeps_the_subtotal():
    assert order_total(CART, None, FlatTax(0.0)) == 9990

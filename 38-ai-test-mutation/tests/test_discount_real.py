import pytest

from demo.discount import apply_discount


def test_ten_percent_off():
    assert apply_discount(100, 10) == 90.0


def test_full_discount_is_free():
    assert apply_discount(59.99, 100) == 0.0


@pytest.mark.parametrize("percent", [-1, 101])
def test_rejects_out_of_range(percent):
    with pytest.raises(ValueError):
        apply_discount(100, percent)

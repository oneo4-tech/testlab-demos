"""Order totals in cents; the tax rate comes from the tax service."""

COUPONS = {"SAVE10": 10, "VIP25": 25, "FREE100": 100}


def apply_coupon(cents: int, percent: int) -> int:
    if not 0 <= percent <= 100:
        raise ValueError("bad coupon percent")
    return round(cents * (1 - percent / 100))


def order_total(cart, code, tax) -> int:
    subtotal = sum(cents * qty for cents, qty in cart)
    if code:
        subtotal = apply_coupon(subtotal, COUPONS[code])
    return round(subtotal * (1 + tax.rate()))

def apply_discount(price: float, percent: float) -> float:
    """Price after a percent discount."""
    if not 0 <= percent <= 100:
        raise ValueError("percent must be 0-100")
    return round(price * (1 - percent / 100), 2)

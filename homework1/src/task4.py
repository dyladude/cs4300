"""
Task 4: Functions & validation
calculate_discount(price, discount_pct) -> float
- price: numeric
- discount_pct: 0..100 inclusive
"""
from numbers import Number

def calculate_discount(price: Number, discount_pct: Number) -> float:
    if not isinstance(price, Number) or not isinstance(discount_pct, Number):
        raise TypeError("price and discount must be numeric")
    if discount_pct < 0 or discount_pct > 100:
        raise ValueError("discount must be between 0 and 100")
    return float(price) * (1.0 - float(discount_pct) / 100.0)

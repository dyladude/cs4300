import math
import pytest
from src.task4 import calculate_discount

@pytest.mark.parametrize("price,disc,expected", [
    (100, 10, 90.0),
    (99.99, 25, 74.9925),
    (200, 0, 200.0),
    (200.0, 100, 0.0),
])
def test_calculate_discount_values(price, disc, expected):
    assert math.isclose(calculate_discount(price, disc), expected, rel_tol=1e-9)

@pytest.mark.parametrize("bad_disc", [-1, 101])
def test_calculate_discount_range(bad_disc):
    with pytest.raises(ValueError):
        calculate_discount(10, bad_disc)

@pytest.mark.parametrize("p,d", [("10","5"), (10,"5"), ("10",5)])
def test_calculate_discount_types(p, d):
    with pytest.raises(TypeError):
        calculate_discount(p, d)

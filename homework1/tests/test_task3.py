import pytest
from src.task3 import classify_number, first_primes, sum_1_to_100

@pytest.mark.parametrize("n,expected", [(5,"positive"), (-1,"negative"), (0,"zero")])
def test_classify_number(n, expected):
    assert classify_number(n) == expected

def test_first_primes_10():
    assert first_primes(10) == [2,3,5,7,11,13,17,19,23,29]

def test_sum_1_to_100():
    assert sum_1_to_100() == 5050

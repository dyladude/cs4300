import pytest
from src.task2 import types_demo

@pytest.mark.parametrize("key,expected_type", [
    ("an_int", int),
    ("a_float", float),
    ("a_string", str),
    ("a_bool", bool),
])
def test_types(key, expected_type):
    vals = types_demo()
    assert key in vals
    assert isinstance(vals[key], expected_type)

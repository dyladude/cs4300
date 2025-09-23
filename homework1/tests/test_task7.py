import pytest
from src.task7 import parse_student, Student, ValidationError

def test_parse_student_ok():
    s = parse_student({"name": "Ben", "id": "1002"})  # coerces str -> int
    assert isinstance(s, Student)
    assert s.id == 1002

def test_parse_student_bad_id():
    with pytest.raises(ValidationError):
        parse_student({"name": "Ben", "id": 0})

"""
Task 7 (Pydantic): validate and coerce incoming student data.
"""
from pydantic import BaseModel, Field, ValidationError

class Student(BaseModel):
    name: str = Field(min_length=1)
    id: int = Field(gt=0)

def parse_student(data: dict) -> Student:
    return Student(**data)

__all__ = ["Student", "parse_student", "ValidationError"]

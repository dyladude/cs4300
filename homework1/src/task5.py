"""
Task 5: Lists & Dictionaries
- favorite_books: list of (title, author) tuples
- first_three_books: slice of the first three
- student_db: simple name -> id dictionary
"""

from typing import List, Tuple, Dict

def favorite_books() -> List[Tuple[str, str]]:
    return [
        ("The Making of the Atomic Bomb", "Richard Rhodes"),
        ("Gravities Rainbow", "Thomas Pynchon"),
        ("Blood Meridian", "Cormac McCarthy"),
        ("The Shadow Lines", "Amitav Ghosh"),
        ("Green Eggs and Ham", "Dr. Seuss"),
    ]

def first_three_books() -> List[Tuple[str, str]]:
    return favorite_books()[:3]

def student_db() -> Dict[str, int]:
    return {"Ava": 1001, "Ben": 1002, "Casey": 1003}
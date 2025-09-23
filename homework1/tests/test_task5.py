
from src.task5 import favorite_books, first_three_books, student_db

def test_favorite_books_structure():
    books = favorite_books()
    assert isinstance(books, list)
    assert len(books) >= 5
    # ensure list of (str, str)
    for item in books:
        assert isinstance(item, tuple) and len(item) == 2
        title, author = item
        assert isinstance(title, str) and isinstance(author, str)

def test_first_three_books_slice():
    books = favorite_books()
    top3 = first_three_books()
    assert top3 == books[:3]
    assert len(top3) == 3

def test_student_db_keys_and_types():
    db = student_db()
    assert set(db.keys()) >= {"Ava", "Ben", "Casey"}
    assert all(isinstance(v, int) for v in db.values())
    assert all(v > 0 for v in db.values())


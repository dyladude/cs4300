from pathlib import Path
from src.task6 import count_words_in_file

def test_word_count_for_assignment_text():
    # uses the exact text from the PDF placed at project root
    n = count_words_in_file(Path("task6_read_me.txt"))
    assert n == 104  # expected with the word definition used in src/task6.py

def test_word_count_on_small_tempfile(tmp_path):
    p = tmp_path / "tiny.txt"
    p.write_text("Hello, world! 42 times... hello\nworld")
    # Words counted: Hello, world, times, hello, world -> 5 (digits ignored)
    assert count_words_in_file(p) == 5

from pathlib import Path
import re
from typing import Union

WORD_RE = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")

def count_words_in_file(path: Union[str, Path]) -> int:
    """
    Count words in a text file. A 'word' is a run of letters (optionally with a single apostrophe).
    Digits and punctuation are ignored.
    """
    text = Path(path).read_text(encoding="utf-8")
    return len(WORD_RE.findall(text))

if __name__ == "__main__":
    # Quick manual run: python -m src.task6
    p = Path(__file__).resolve().parents[1] / "task6_read_me.txt"
    print(count_words_in_file(p))
from src.task1 import hello

def test_hello_prints_expected(capsys):
    print(hello())
    captured = capsys.readouterr()
    assert captured.out.strip() == "Hello world!"
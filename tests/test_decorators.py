import sys
from io import StringIO

import pytest

from src.decorators import log


def test_log_success_to_console():
    """Тест успешного выполнения функции с выводом в консоль."""
    @log()
    def add(a, b):
        return a + b

    # Перехватываем вывод в консоль
    captured_output = StringIO()
    sys.stdout = captured_output

    result = add(3, 5)

    # Восстанавливаем stdout
    sys.stdout = sys.__stdout__

    assert result == 8
    assert "add ok" in captured_output.getvalue()


def test_log_success_to_file(tmp_path):
    """Тест успешного выполнения функции с записью в файл."""
    log_file = tmp_path / "test.log"

    @log(filename=str(log_file))
    def multiply(a, b):
        return a * b

    result = multiply(4, 7)

    assert result == 28

    with open(log_file, 'r', encoding='utf-8') as f:
        content = f.read()
        assert "multiply ok" in content


def test_log_error_to_console():
    """Тест функции, выбрасывающей исключение, с выводом в консоль."""
    @log()
    def divide(a, b):
        return a / b

    captured_output = StringIO()
    sys.stdout = captured_output

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    sys.stdout = sys.__stdout__

    log_content = captured_output.getvalue()
    assert "divide error: ZeroDivisionError" in log_content
    assert "Inputs: (10, 0), {}" in log_content


def test_log_error_to_file(tmp_path):
    """Тест функции, выбрасывающей исключение, с записью в файл."""
    log_file = tmp_path / "error.log"

    @log(filename=str(log_file))
    def parse_int(value):
        return int(value)

    with pytest.raises(ValueError):
        parse_int("not a number")

    with open(log_file, 'r', encoding='utf-8') as f:
        content = f.read()
        assert "parse_int error: ValueError" in content
        assert "Inputs: ('not a number',), {}" in content


def test_log_preserves_function_metadata():
    """Тест, что декоратор сохраняет метаданные функции."""
    @log()
    def my_function():
        """This is a docstring."""
        pass

    assert my_function.__name__ == "my_function"
    assert my_function.__doc__ == "This is a docstring."


def test_log_with_capsys(capsys):
    """Тест с использованием встроенной фикстуры capsys."""
    @log()
    def greet(name):
        return f"Hello, {name}!"

    result = greet("Alice")

    captured = capsys.readouterr()
    assert result == "Hello, Alice!"
    assert "greet ok" in captured.out


def test_log_without_filename_writes_to_console(capsys):
    """Тест, что без filename лог пишется в консоль."""
    @log()
    def say_hello(name):
        return f"Hello, {name}"

    result = say_hello("Bob")

    captured = capsys.readouterr()
    assert result == "Hello, Bob"
    assert "say_hello ok" in captured.out


def test_log_with_filename_writes_to_file(tmp_path):
    """Тест, что с filename лог пишется в файл."""
    log_file = tmp_path / "app.log"

    @log(filename=str(log_file))
    def square(x):
        return x ** 2

    result = square(5)

    assert result == 25

    with open(log_file, 'r', encoding='utf-8') as f:
        content = f.read()
        assert "square ok" in content

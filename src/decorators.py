import functools
import sys
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования выполнения функций.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                result = func(*args, **kwargs)
                log_message = f"{func.__name__} ok\n"
                _write_log(log_message, filename)
                return result
            except Exception as e:
                error_message = (
                    f"{func.__name__} error: {type(e).__name__}. "
                    f"Inputs: {args}, {kwargs}\n"
                )
                _write_log(error_message, filename)
                raise
        return wrapper
    return decorator


def _write_log(message: str, filename: Optional[str] = None) -> None:
    """Записывает лог в файл или в консоль."""
    if filename:
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(message)
    else:
        sys.stdout.write(message)


# Временно для проверки
if __name__ == "__main__":
    @log()
    def add(a, b):
        return a + b

    @log(filename="test.log")
    def multiply(a, b):
        return a * b

    print(add(3, 5))
    print(multiply(4, 7))

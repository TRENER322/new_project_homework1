import json
import logging
from pathlib import Path
from typing import Any, Dict, List

# Путь к папке logs в корне проекта
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Создаём логгер для модуля
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False

# Добавляем handler только один раз
if not logger.handlers:
    file_handler = logging.FileHandler(
        LOG_DIR / "utils.log", mode="w", encoding="utf-8"
    )
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON-файл и возвращает список словарей с данными транзакций.

    Args:
        file_path (str): Путь к JSON-файлу.

    Returns:
        List[Dict[str, Any]]: Список словарей с транзакциями.
    """
    logger.debug("Начало чтения JSON-файла: %s", file_path)

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            logger.info(
                "Файл %s успешно прочитан. Записей: %d", file_path, len(data)
            )
            return data

        logger.error("Файл %s не содержит список", file_path)
        return []

    except FileNotFoundError as error:
        logger.error("Файл %s не найден: %s", file_path, error)
        return []

    except json.JSONDecodeError as error:
        logger.error("Ошибка декодирования JSON в файле %s: %s", file_path, error)
        return []

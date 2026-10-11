import logging
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False

if not logger.handlers:
    file_handler = logging.FileHandler(
        LOG_DIR / "csv_excel_reader.log", mode="w", encoding="utf-8"
    )
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)


def read_transactions_csv(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает финансовые операции из CSV-файла.
    """
    logger.debug("Начало чтения CSV-файла: %s", file_path)

    try:
        df = pd.read_csv(file_path, sep=";", encoding="utf-8")
    except FileNotFoundError as error:
        logger.error("CSV-файл не найден: %s — %s", file_path, error)
        return []
    except Exception as error:
        logger.error("Ошибка чтения CSV-файла %s: %s", file_path, error)
        return []

    if df.empty:
        logger.error("CSV-файл пустой: %s", file_path)
        return []

    transactions = [
        {str(key): value for key, value in record.items()}
        for record in df.to_dict(orient="records")
    ]
    logger.info(
        "CSV-файл успешно прочитан: %s. Записей: %d", file_path, len(transactions)
    )
    return transactions


def read_transactions_excel(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает финансовые операции из Excel-файла (.xlsx).
    """
    logger.debug("Начало чтения Excel-файла: %s", file_path)

    try:
        df = pd.read_excel(file_path, engine="openpyxl")
    except FileNotFoundError as error:
        logger.error("Excel-файл не найден: %s — %s", file_path, error)
        return []
    except Exception as error:
        logger.error("Ошибка чтения Excel-файла %s: %s", file_path, error)
        return []

    if df.empty:
        logger.error("Excel-файл пустой: %s", file_path)
        return []

    transactions = [
        {str(key): value for key, value in record.items()}
        for record in df.to_dict(orient="records")
    ]
    logger.info(
        "Excel-файл успешно прочитан: %s. Записей: %d",
        file_path,
        len(transactions),
    )
    return transactions

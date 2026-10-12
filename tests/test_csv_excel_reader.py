from unittest.mock import patch

import pandas as pd

from src.csv_excel_reader import read_transactions_csv, read_transactions_excel


@patch("src.csv_excel_reader.pd.read_csv")
def test_read_transactions_csv_success(mock_read_csv):
    """Тест: успешное чтение CSV."""
    mock_df = pd.DataFrame(
        [
            {"id": 1, "state": "EXECUTED", "amount": 100},
            {"id": 2, "state": "CANCELED", "amount": 200},
        ]
    )
    mock_read_csv.return_value = mock_df

    result = read_transactions_csv("data/transactions.csv")

    assert len(result) == 2
    assert result[0]["state"] == "EXECUTED"
    assert result[1]["state"] == "CANCELED"
    mock_read_csv.assert_called_once_with(
        "data/transactions.csv", sep=";", encoding="utf-8"
    )


@patch("src.csv_excel_reader.pd.read_csv")
def test_read_transactions_csv_empty(mock_read_csv):
    """Тест: пустой CSV."""
    mock_read_csv.return_value = pd.DataFrame()

    result = read_transactions_csv("data/transactions.csv")

    assert result == []


@patch("src.csv_excel_reader.pd.read_csv")
def test_read_transactions_csv_not_found(mock_read_csv):
    """Тест: CSV-файл не найден."""
    mock_read_csv.side_effect = FileNotFoundError("Файл не найден")

    result = read_transactions_csv("data/nope.csv")

    assert result == []


@patch("src.csv_excel_reader.pd.read_csv")
def test_read_transactions_csv_error(mock_read_csv):
    """Тест: неизвестная ошибка при чтении CSV."""
    mock_read_csv.side_effect = Exception("Что-то пошло не так")

    result = read_transactions_csv("data/transactions.csv")

    assert result == []


# ===== Тесты для read_transactions_excel =====


@patch("src.csv_excel_reader.pd.read_excel")
def test_read_transactions_excel_success(mock_read_excel):
    """Тест: успешное чтение Excel."""
    mock_df = pd.DataFrame(
        [
            {"id": 1, "state": "EXECUTED", "amount": 300},
            {"id": 2, "state": "PENDING", "amount": 400},
        ]
    )
    mock_read_excel.return_value = mock_df

    result = read_transactions_excel("data/transactions_excel.xlsx")

    assert len(result) == 2
    assert result[0]["state"] == "EXECUTED"
    assert result[1]["state"] == "PENDING"
    mock_read_excel.assert_called_once_with(
        "data/transactions_excel.xlsx", engine="openpyxl"
    )


@patch("src.csv_excel_reader.pd.read_excel")
def test_read_transactions_excel_empty(mock_read_excel):
    """Тест: пустой Excel."""
    mock_read_excel.return_value = pd.DataFrame()

    result = read_transactions_excel("data/transactions_excel.xlsx")

    assert result == []


@patch("src.csv_excel_reader.pd.read_excel")
def test_read_transactions_excel_not_found(mock_read_excel):
    """Тест: Excel-файл не найден."""
    mock_read_excel.side_effect = FileNotFoundError("Файл не найден")

    result = read_transactions_excel("data/nope.xlsx")

    assert result == []


@patch("src.csv_excel_reader.pd.read_excel")
def test_read_transactions_excel_error(mock_read_excel):
    """Тест: неизвестная ошибка при чтении Excel."""
    mock_read_excel.side_effect = Exception("Что-то пошло не так")

    result = read_transactions_excel("data/transactions_excel.xlsx")

    assert result == []

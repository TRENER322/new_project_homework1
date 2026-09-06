from unittest.mock import Mock, patch

import pytest

from src.external_api import convert_currency


@patch("src.external_api.requests.get")
def test_convert_currency_usd_to_rub(mock_get):
    """Тест конвертации USD в RUB."""
    mock_response = Mock()
    mock_response.json.return_value = {"rates": {"RUB": 90.5}}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": {"code": "USD"}
        }
    }

    result = convert_currency(transaction)
    assert result == 9050.0


def test_convert_currency_rub():
    """Тест: RUB не требует конвертации."""
    transaction = {
        "operationAmount": {
            "amount": "1000",
            "currency": {"code": "RUB"}
        }
    }

    result = convert_currency(transaction)
    assert result == 1000.0


def test_convert_currency_missing_amount():
    """Тест: отсутствует сумма."""
    transaction = {
        "operationAmount": {
            "currency": {"code": "USD"}
        }
    }

    with pytest.raises(ValueError):
        convert_currency(transaction)


def test_convert_currency_missing_currency():
    """Тест: отсутствует валюта."""
    transaction = {
        "operationAmount": {
            "amount": "100"
        }
    }

    with pytest.raises(ValueError):
        convert_currency(transaction)

import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data/latest"


def convert_currency(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли.
    """
    amount_str = transaction.get("operationAmount", {}).get("amount")
    currency_code = transaction.get("operationAmount", {}).get("currency", {}).get("code")

    if amount_str is None or currency_code is None:
        raise ValueError("Transaction missing amount or currency")

    amount = float(amount_str)

    if currency_code == "RUB":
        return amount

    if currency_code in ("USD", "EUR") and API_KEY:
        try:
            response = requests.get(
                BASE_URL,
                params={"base": currency_code, "symbols": "RUB"},
                headers={"apikey": API_KEY}
            )
            response.raise_for_status()
            data = response.json()
            rate = data.get("rates", {}).get("RUB")

            if rate is None:
                raise ValueError(f"Rate for RUB not found for currency {currency_code}")

            return round(amount * rate, 2)

        except requests.RequestException as e:
            raise ValueError(f"API request failed: {e}")

    return amount

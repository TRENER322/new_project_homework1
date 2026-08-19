def filter_by_currency(transactions: list[dict], currency_name: str):
    """
    Фильтрует транзакции по валюте.
    """
    for transaction in transactions:
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency_name:
            yield transaction


def transaction_descriptions(transactions: list[dict]):
    """
    Генерирует описания транзакций.
    """
    for transaction in transactions:
        if "description" in transaction:
            yield transaction["description"]


def card_number_generator(start: int, stop: int):
    """
    Генерирует номера банковских карт в формате XXXX XXXX XXXX XXXX.
    """
    for n in range(start, stop + 1):
        card_number = str(n).zfill(16)
        yield f"{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[-4:]}"


# ===== Входные данные =====
transactions = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9824.07",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702"
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {
            "amount": "79114.93",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188"
    },
    {
        "id": 873106923,
        "state": "EXECUTED",
        "date": "2019-03-23T01:09:46.296404",
        "operationAmount": {
            "amount": "43318.34",
            "currency": {
                "name": "руб.",
                "code": "RUB"
            }
        },
        "description": "Перевод со счета на счет",
        "from": "Счет 44812258784861134719",
        "to": "Счет 74489636417521191160"
    },
    {
        "id": 895315941,
        "state": "EXECUTED",
        "date": "2018-08-19T04:27:37.904916",
        "operationAmount": {
            "amount": "56883.54",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод с карты на карту",
        "from": "Visa Classic 6831982476737658",
        "to": "Visa Platinum 8990922113665229"
    },
    {
        "id": 594226727,
        "state": "CANCELED",
        "date": "2018-09-12T21:27:25.241689",
        "operationAmount": {
            "amount": "67314.70",
            "currency": {
                "name": "руб.",
                "code": "RUB"
            }
        },
        "description": "Перевод организации",
        "from": "Visa Platinum 1246377376343588",
        "to": "Счет 14211924144426031657"
    }
]


# Фильтрация по валюте
gen_currency = filter_by_currency(transactions, "RUB")
print(next(gen_currency))

# Описания
gen_descriptions = transaction_descriptions(transactions)
for _ in range(5):
    print(next(gen_descriptions))

# Номера карт
gen_card_number = card_number_generator(9999999990, 9999999999)
print(list(gen_card_number))

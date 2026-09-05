import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions

# ===== Фикстуры =====


@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми транзакциями."""
    return [
        {
            "id": 1,
            "operationAmount": {"amount": "100.00", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод USD"
        },
        {
            "id": 2,
            "operationAmount": {"amount": "200.00", "currency": {"name": "RUB", "code": "RUB"}},
            "description": "Перевод RUB"
        },
        {
            "id": 3,
            "operationAmount": {"amount": "300.00", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод USD 2"
        },
        {
            "id": 4,
            "operationAmount": {"amount": "500.00", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод USD 3"
        },
    ]


@pytest.fixture
def empty_transactions():
    """Фикстура с пустым списком транзакций."""
    return []


# ===== Тесты для filter_by_currency =====

def test_filter_by_currency_usd(sample_transactions):
    """Тест фильтрации по USD."""
    result = list(filter_by_currency(sample_transactions, "USD"))
    assert len(result) == 3
    assert all(t["operationAmount"]["currency"]["code"] == "USD" for t in result)


def test_filter_by_currency_rub(sample_transactions):
    """Тест фильтрации по RUB."""
    result = list(filter_by_currency(sample_transactions, "RUB"))
    assert len(result) == 1
    assert result[0]["operationAmount"]["currency"]["code"] == "RUB"


def test_filter_by_currency_not_found(sample_transactions):
    """Тест: валюта отсутствует."""
    result = list(filter_by_currency(sample_transactions, "EUR"))
    assert len(result) == 0


def test_filter_by_currency_empty(empty_transactions):
    """Тест: пустой список транзакций."""
    result = list(filter_by_currency(empty_transactions, "USD"))
    assert len(result) == 0


@pytest.mark.parametrize("currency, expected_count", [
    ("USD", 3),
    ("RUB", 1),
])
def test_filter_by_currency_parametrize(sample_transactions, currency, expected_count):
    """Параметризованный тест фильтрации по разным валютам."""
    result = list(filter_by_currency(sample_transactions, currency))
    assert len(result) == expected_count


# ===== Тесты для transaction_descriptions =====

def test_transaction_descriptions(sample_transactions):
    """Тест генерации описаний."""
    descriptions = list(transaction_descriptions(sample_transactions))
    expected = ["Перевод USD", "Перевод RUB", "Перевод USD 2", "Перевод USD 3"]
    assert descriptions == expected


def test_transaction_descriptions_empty(empty_transactions):
    """Тест: пустой список транзакций."""
    descriptions = list(transaction_descriptions(empty_transactions))
    assert descriptions == []


@pytest.mark.parametrize("count", [1, 3, 5])
def test_transaction_descriptions_count(sample_transactions, count):
    """Параметризованный тест: проверка количества описаний."""
    descriptions = list(transaction_descriptions(sample_transactions))
    assert len(descriptions) == 4  # всего 4 транзакции


def test_transaction_descriptions_no_description():
    """Тест: транзакция без описания."""
    transactions = [
        {"id": 1, "operationAmount": {"currency": {"code": "USD"}}},
        {"id": 2, "operationAmount": {"currency": {"code": "RUB"}}, "description": "Перевод RUB"},
    ]
    descriptions = list(transaction_descriptions(transactions))
    assert descriptions == ["Перевод RUB"]


# ===== Тесты для card_number_generator =====

def test_card_number_generator_small():
    """Тест генерации номеров карт (малый диапазон)."""
    cards = list(card_number_generator(1, 5))
    expected = [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005",
    ]
    assert cards == expected


def test_card_number_generator_format():
    """Тест форматирования номера карты."""
    cards = list(card_number_generator(1, 1))
    assert cards[0] == "0000 0000 0000 0001"


def test_card_number_generator_large():
    """Тест генерации с большими числами."""
    cards = list(card_number_generator(9999, 10001))
    expected = [
        "0000 0000 0000 9999",
        "0000 0000 0001 0000",  # 10000
        "0000 0000 0001 0001",  # 10001
    ]
    assert cards == expected


def test_card_number_generator_single():
    """Тест с одним значением."""
    cards = list(card_number_generator(10, 10))
    assert cards[0] == "0000 0000 0000 0010"


def test_card_number_generator_zero():
    """Тест с нулём."""
    cards = list(card_number_generator(0, 0))
    assert cards[0] == "0000 0000 0000 0000"


@pytest.mark.parametrize("start, stop, expected_first, expected_last", [
    (1, 3, "0000 0000 0000 0001", "0000 0000 0000 0003"),
    (100, 102, "0000 0000 0000 0100", "0000 0000 0000 0102"),
    (9999, 10001, "0000 0000 0000 9999", "0000 0000 0001 0001"),
])
def test_card_number_generator_parametrize(start, stop, expected_first, expected_last):
    """Параметризованный тест генерации номеров карт."""
    cards = list(card_number_generator(start, stop))
    assert cards[0] == expected_first
    assert cards[-1] == expected_last

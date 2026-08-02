import pytest


@pytest.fixture
def sample_transactions():
    """Фикстура: список транзакций для тестов."""
    return [
        {'id': 1, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 2, 'state': 'CANCELED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 3, 'state': 'EXECUTED', 'date': '2020-09-12T21:27:25.241689'},
        {'id': 4, 'state': 'PENDING', 'date': '2021-01-01T00:00:00.000000'},
        {'id': 5, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
    ]


@pytest.fixture
def sample_cards():
    """Фикстура: данные для тестов масок карт."""
    return {
        'valid': '1234567890123456',
        'short': '12345678',
        'empty': '',
    }

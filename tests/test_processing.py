import pytest

from src.processing import filter_by_state, sort_by_date


def test_filter_by_state(sample_transactions):
    result = filter_by_state(sample_transactions)
    assert len(result) == 2
    assert all(item['state'] == 'EXECUTED' for item in result)


@pytest.mark.parametrize('state, expected_count', [
    ('EXECUTED', 2),
    ('CANCELED', 2),
    ('PENDING', 1),
    ('UNKNOWN', 0),
])
def test_filter_by_state_parametrize(sample_transactions, state, expected_count):
    result = filter_by_state(sample_transactions, state)
    assert len(result) == expected_count


def test_sort_by_date_descending(sample_transactions):
    result = sort_by_date(sample_transactions, descending=True)
    dates = [item['date'] for item in result]
    assert dates == sorted(dates, reverse=True)


def test_sort_by_date_ascending(sample_transactions):
    result = sort_by_date(sample_transactions, descending=False)
    dates = [item['date'] for item in result]
    assert dates == sorted(dates)

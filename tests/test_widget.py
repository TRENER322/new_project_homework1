import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize('input_data, expected', [
    ('Visa 1234567890123456', 'Visa 1234 56** **** 3456'),
    ('MasterCard 1111222233334444', 'MasterCard 1111 22** **** 4444'),
    ('Счет 1234567890', 'Счет **7890'),
    ('Счет 123456', 'Счет **3456'),
])
def test_mask_account_card(input_data, expected):
    assert mask_account_card(input_data) == expected


def test_mask_account_card_empty():
    """Тест на пустой ввод."""
    assert mask_account_card('') == ''


def test_mask_account_card_no_space():
    """Тест на строку без пробела — должна быть ошибка."""
    with pytest.raises(ValueError, match="Неверный формат"):
        mask_account_card('Visa1234567890123456')


@pytest.mark.parametrize('date_str, expected', [
    ('2024-03-11T02:26:18.671407', '11.03.2024'),
    ('2025-12-25T23:59:59.999999', '25.12.2025'),
    ('2020-09-12', '12.09.2020'),
    ('2019-07-03T21:27:25', '03.07.2019'),
])
def test_get_date(date_str, expected):
    assert get_date(date_str) == expected

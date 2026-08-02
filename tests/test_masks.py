import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize('card_number, expected', [
    ('1234567890123456', '1234 56** **** 3456'),
    ('1111222233334444', '1111 22** **** 4444'),
])
def test_get_mask_card_number(card_number, expected):
    assert get_mask_card_number(card_number) == expected


def test_get_mask_card_number_invalid():
    """Тест на некорректный номер карты."""
    with pytest.raises(ValueError, match="Номер карты должен содержать ровно 16 цифр."):
        get_mask_card_number('123456789012')


@pytest.mark.parametrize('account_number, expected', [
    ('1234567890', '**7890'),
    ('12345', '**2345'),
])
def test_get_mask_account(account_number, expected):
    assert get_mask_account(account_number) == expected


def test_get_mask_account_invalid():
    """Тест на некорректный номер счёта."""
    with pytest.raises(ValueError, match="Номер счета должен содержать минимум 4 цифры."):
        get_mask_account('123')

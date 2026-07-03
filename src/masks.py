def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты.

    Оставляет видимыми первые 6 цифр и последние 4 цифры.
    Остальные символы заменяются звёздочками.
    Номер разбивается по блокам: XXXX XX** **** XXXX.

    Исключения:
        ValueError: Если номер содержит не 16 цифр.
    """
    card_number = card_number.replace(" ", "")
    if len(card_number) != 16:
        raise ValueError("Номер карты должен содержать ровно 16 цифр.")
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счета.

    Оставляет видимыми только последние 4 цифры.
    Перед ними добавляются две звёздочки.

   Исключения:
        ValueError: Если номер содержит менее 4 цифр.
    """
    account_number = account_number.replace(" ", "")
    if len(account_number) < 4:
        raise ValueError("Номер счета должен содержать минимум 4 цифры.")
    return "**" + account_number[-4:]


print(get_mask_card_number("7000792289606361"))
print(get_mask_account("15451565261211535235"))

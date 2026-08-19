from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(info: str) -> str:
    """Маскирует номер карты или счёта в строке."""
    if not info:
        return ""
    if " " not in info:
        raise ValueError("Неверный формат: ожидается 'Название Номер'")

    parts = info.rsplit(' ', 1)
    name, number = parts

    if name.lower() == 'счет':
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f"{name} {masked_number}"


def get_date(date_str: str) -> str:
    """Преобразует дату из ISO-формата в формат ДД.ММ.ГГГГ."""
    if not date_str:
        return ""
    date_part = date_str.split('T')[0]
    year, month, day = date_part.split('-')
    return f"{day}.{month}.{year}"


if __name__ == "__main__":
    test_cases: list[str] = [
        "Maestro 1596837868705199",
        "Счет 64686473678894779589",
        "MasterCard 7158300734726758",
        "Счет 35383033474447895560",
        "Visa Classic 6831982476737658",
        "Visa Platinum 8990922113665229",
        "Visa Gold 5999414228426353",
        "Счет 73654108430135874305",
    ]

    print("=== Маскировка номеров ===")
    for case in test_cases:
        print(mask_account_card(case))

    print("\n=== Преобразование даты ===")
    print(get_date("2024-03-11T02:26:18.671407"))
    print(get_date("2025-12-25T23:59:59.999999"))

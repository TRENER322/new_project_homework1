from datetime import datetime
from typing import Any, Dict

from src.csv_excel_reader import read_transactions_csv, read_transactions_excel
from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date
from src.utils import process_bank_search, read_json_file


def format_date(date_str: str) -> str:
    """Преобразует дату из ISO формата в ДД.ММ.ГГГГ."""
    if not date_str:
        return ""
    formats = [
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S",
    ]
    for fmt in formats:
        try:
            date_obj = datetime.strptime(date_str, fmt)
            return date_obj.strftime("%d.%m.%Y")
        except (ValueError, TypeError):
            continue
    return str(date_str)


def get_amount_and_currency(transaction: Dict[str, Any]) -> tuple:
    """Извлекает сумму и валюту из транзакции (JSON или CSV/Excel)."""
    if "operationAmount" in transaction:
        op_amount = transaction.get("operationAmount", {})
        amount = str(op_amount.get("amount", ""))
        currency = op_amount.get("currency", {}).get("name", "")
        return amount, currency
    else:
        amount = str(transaction.get("amount", ""))
        currency = transaction.get("currency_name", "")
        return amount, currency


def get_currency_code(transaction: Dict[str, Any]) -> str:
    """Извлекает код валюты из транзакции."""
    if "operationAmount" in transaction:
        return str(
            transaction.get("operationAmount", {})
            .get("currency", {})
            .get("code", "")
        )
    else:
        return str(transaction.get("currency_code", ""))


def mask_account_or_card(value: Any) -> str:
    """Маскирует номер счета или карты, безопасно обрабатывая пустые значения."""
    if not isinstance(value, str) or not value.strip():
        return ""
    parts = value.split()
    if not parts:
        return ""
    last_part = parts[-1]
    if "Счет" in value:
        try:
            return "Счет " + get_mask_account(last_part)
        except ValueError:
            return value
    else:
        try:
            return get_mask_card_number(last_part)
        except ValueError:
            return value


def print_transaction(transaction: Dict[str, Any]) -> None:
    """Выводит информацию об одной транзакции."""
    date = format_date(transaction.get("date", ""))
    desc = transaction.get("description", "")
    sender = mask_account_or_card(transaction.get("from", ""))
    receiver = mask_account_or_card(transaction.get("to", ""))

    print(f"{date} {desc}")
    if sender and receiver:
        print(f"{sender} -> {receiver}")
    elif sender:
        print(sender)
    elif receiver:
        print(receiver)

    amount, currency = get_amount_and_currency(transaction)
    print(f"Сумма: {amount} {currency}\n")


def choose_data_source() -> list:
    """Выбор источника данных."""
    while True:
        print("Выберите необходимый пункт меню:")
        print("1. Получить информацию о транзакциях из JSON-файла")
        print("2. Получить информацию о транзакциях из CSV-файла")
        print("3. Получить информацию о транзакциях из XLSX-файла")
        choice = input("Ваш выбор: ").strip()
        if choice == "1":
            print("Для обработки выбран JSON-файл.")
            return read_json_file("data/operations.json")
        elif choice == "2":
            print("Для обработки выбран CSV-файл.")
            return read_transactions_csv("data/transactions.csv")
        elif choice == "3":
            print("Для обработки выбран XLSX-файл.")
            return read_transactions_excel("data/transactions_excel.xlsx")
        else:
            print("Неверный выбор. Попробуйте снова.")


def filter_by_status(data: list) -> list:
    """Фильтрация по статусу."""
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        print(
            "Введите статус, по которому необходимо выполнить фильтрацию. "
            f"Доступные для фильтровки статусы: {', '.join(valid_statuses)}"
        )
        status_input = input("Ваш выбор: ").strip().upper()
        if status_input in valid_statuses:
            print(f'Операции отфильтрованы по статусу "{status_input}"')
            return filter_by_state(data, status_input)
        else:
            print(f'Статус операции "{status_input}" недоступен.')


def sort_data(data: list) -> list:
    """Сортировка по дате."""
    sort_choice = input("Отсортировать операции по дате? Да/Нет\n").strip().lower()
    if sort_choice not in ["да", "yes", "y"]:
        return data
    while True:
        order = input("Отсортировать по возрастанию или по убыванию?\n").strip().lower()
        if order in ["по возрастанию", "возрастание", "asc"]:
            descending = False
            break
        elif order in ["по убыванию", "убывание", "desc"]:
            descending = True
            break
        else:
            print("Пожалуйста, введите 'по возрастанию' или 'по убыванию'.")
    return sort_by_date(data, descending=descending)


def filter_rub(data: list) -> list:
    """Фильтрация только рублевых транзакций."""
    rub_choice = input("Выводить только рублевые транзакции? Да/Нет\n").strip().lower()
    if rub_choice in ["да", "yes", "y"]:
        return [t for t in data if get_currency_code(t) == "RUB"]
    return data


def filter_by_search(data: list) -> list:
    """Фильтрация по слову в описании."""
    search_choice = input(
        "Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n"
    ).strip().lower()
    if search_choice in ["да", "yes", "y"]:
        search_word = input("Введите слово для поиска: ").strip()
        return process_bank_search(data, search_word)
    return data


def main() -> None:
    """Основная логика программы."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    data = choose_data_source()
    if not data:
        print("Не удалось загрузить данные или файл пуст.")
        return
    data = filter_by_status(data)
    data = sort_data(data)
    data = filter_rub(data)
    data = filter_by_search(data)

    print("Распечатываю итоговый список транзакций...\n")
    if not data:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print(f"Всего банковских операций в выборке: {len(data)}\n")
        for transaction in data:
            print_transaction(transaction)


if __name__ == "__main__":
    main()

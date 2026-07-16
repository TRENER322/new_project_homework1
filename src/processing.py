def filter_by_state(transactions, state='EXECUTED'):
    """Фильтрует транзакции по значению ключа 'state'."""
    filtered_list = []
    for transaction in transactions:
        if transaction.get('state') == state:
            filtered_list.append(transaction)
    return filtered_list


def sort_by_date(transactions, descending=True):
    """Сортирует транзакции по дате."""
    # Фильтруем транзакции без даты
    filtered_transactions = [t for t in transactions if t.get('date') is not None]

    # Сортируем по дате
    return sorted(filtered_transactions, key=lambda x: x.get('date'), reverse=descending)


# Пример использования
if __name__ == "__main__":
    transactions = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]

    # Фильтрация по state
    print("Фильтрация по EXECUTED:")
    print(filter_by_state(transactions))

    print("\nФильтрация по CANCELED:")
    print(filter_by_state(transactions, 'CANCELED'))

    # Сортировка по дате
    print("\nСортировка по дате (убывание):")
    print(sort_by_date(transactions))

    print("\nСортировка по дате (возрастание):")
    print(sort_by_date(transactions, False))
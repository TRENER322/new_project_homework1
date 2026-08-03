from typing import List, Dict, Any, cast


def filter_by_state(transactions: List[Dict[str, Any]], state: str = 'EXECUTED') -> List[Dict[str, Any]]:
    """Фильтрует транзакции по значению ключа 'state'."""
    filtered_list = []
    for transaction in transactions:
        if transaction.get('state') == state:
            filtered_list.append(transaction)
    return filtered_list


def sort_by_date(transactions: List[Dict[str, Any]], descending: bool = True) -> List[Dict[str, Any]]:
    """Сортирует транзакции по дате."""
    filtered_transactions = [t for t in transactions if t.get('date') is not None]
    return sorted(
        filtered_transactions,
        key=lambda x: cast(str, x.get('date')),
        reverse=descending
    )
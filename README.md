# Проект обработки транзакций

Проект для фильтрации и сортировки списка транзакций с тестированием.

## Цель проекта

Предоставляет функции для обработки списков транзакций:
- Фильтрация по статусу (`state`)
- Сортировка по дате (`date`)
- Маскировка номеров карт и счетов

## Установка

1. Клонируйте репозиторий:
```bash
git clone git@github.com:TRENER322/new_project_homework1.git
```

2. Перейдите в папку проекта:
```bash
cd new_project_homework1
```

3. Установите зависимости с помощью Poetry:
```bash
poetry install
```

## Использование

```python
from src.processing import filter_by_state, sort_by_date

transactions = [
    {'id': 1, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 2, 'state': 'CANCELED', 'date': '2018-06-30T02:08:58.425572'},
]

# Фильтрация
executed = filter_by_state(transactions)

# Сортировка
sorted_by_date = sort_by_date(transactions)
```

## Тестирование

Для запуска тестов используйте команду:

```bash
pytest
```

Для проверки покрытия кода:

```bash
pytest --cov=src --cov-report=html
```

Отчёт в формате HTML будет сохранён в папке `htmlcov/`. Откройте `htmlcov/index.html` в браузере.

### Текущее покрытие: **99%**

## Структура проекта

```
new_project_homework1/
├── src/
│   ├── masks.py          # Маскировка номеров
│   ├── widget.py         # Основные функции
│   └── processing.py     # Фильтрация и сортировка
├── tests/
│   ├── conftest.py       # Фикстуры
│   ├── test_masks.py
│   ├── test_widget.py
│   └── test_processing.py
├── htmlcov/              # Отчёт о покрытии
├── pyproject.toml
├── poetry.lock
└── README.md
```

## Лицензия

MIT

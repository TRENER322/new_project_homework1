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


2. Перейдите в папку проекта:

cd new_project_homework1


3. Установите зависимости с помощью Poetry:

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

## Модуль generators

Модуль содержит генераторы для работы с большими объемами данных транзакций.

### filter_by_currency

Фильтрует транзакции по заданной валюте и возвращает итератор.

```
from src.generators import filter_by_currency

usd_transactions = filter_by_currency(transactions, "USD")
for _ in range(2):
    print(next(usd_transactions))
```

### transaction_descriptions

Генерирует описания транзакций по очереди.

```
from src.generators import transaction_descriptions

descriptions = transaction_descriptions(transactions)
for _ in range(5):
    print(next(descriptions))
```

### card_number_generator

Генерирует номера банковских карт в формате `XXXX XXXX XXXX XXXX` в заданном диапазоне.

```python
from src.generators import card_number_generator

for card_number in card_number_generator(1, 5):
    print(card_number)
```

## Модуль decorators

Модуль содержит декоратор `log` для автоматического логирования выполнения функций.

### Декоратор log

Декоратор `log` автоматически логирует:
- Успешное выполнение функции: `{имя_функции} ok`
- Ошибки: `{имя_функции} error: {тип_ошибки}. Inputs: {args}, {kwargs}`

Декоратор принимает необязательный аргумент `filename`:
- Если `filename` передан — логи записываются в указанный файл
- Если `filename` не передан — логи выводятся в консоль

#### Пример использования

```python
from src.decorators import log

@log(filename="mylog.txt")
def my_function(x, y):
    return x + y

my_function(1, 2)  # Запись в файл mylog.txt: my_function ok
```

#### Пример логирования ошибки

```
@log(filename="errors.log")
def divide(a, b):
    return a / b

divide(10, 0)  # Запись в errors.log: divide error: ZeroDivisionError. Inputs: (10, 0), {}
```


### Тестирование декоратора

Для запуска тестов декоратора:
```bash
pytest tests/test_decorators.py -v
```
## Модуль utils

Модуль содержит утилиты для работы с данными.

### read_json_file

Функция для чтения JSON-файла с транзакциями.

```python
from src.utils import read_json_file

transactions = read_json_file("data/operations.json")
print(len(transactions))  # Вывод: количество транзакций
```

**Особенности:**
- Если файл не найден → возвращает пустой список
- Если файл пустой → возвращает пустой список
- Если файл содержит не-список → возвращает пустой список

## Модуль external_api

Модуль для работы с внешними API.

### convert_currency

Функция конвертации валюты транзакции в рубли.

```python
from src.external_api import convert_currency

transaction = {
    "operationAmount": {
        "amount": "100",
        "currency": {"code": "USD"}
    }
}

result = convert_currency(transaction)
print(result)  # Вывод: 8653.79 (сумма в рублях)
```

**Особенности:**
- Для USD и EUR обращается к внешнему API для получения курса
- Для RUB возвращает сумму без изменений
- Ключ API хранится в `.env` в переменной `EXCHANGE_RATE_API_KEY`

## Тестирование

Для запуска всех тестов используйте команду:

```bash
pytest
```

Для проверки покрытия кода:

```bash
pytest --cov=src --cov-report=html
```

Отчёт в формате HTML будет сохранён в папке `htmlcov/`. Откройте `htmlcov/index.html` в браузере.

### Текущее покрытие: **100%**

## Типизация кода

Проект полностью типизирован. Все функции и методы имеют аннотации типов.

Для проверки типов используется `mypy`:

```bash
mypy src tests
```

Результат: `Success: no issues found in 18 source files`

## Структура проекта

```
new_project_homework1/
├── data/
│   └── operations.json     # Данные с транзакциями
├── src/
│   ├── decorators.py       # Декоратор log
│   ├── external_api.py     # Конвертация валют
│   ├── generators.py       # Генераторы для обработки данных
│   ├── masks.py            # Маскировка номеров
│   ├── processing.py       # Фильтрация и сортировка
│   ├── utils.py            # Утилиты (чтение JSON)
│   └── widget.py           # Основные функции
├── tests/
│   ├── conftest.py         # Фикстуры
│   ├── test_decorators.py
│   ├── test_external_api.py
│   ├── test_generators.py
│   ├── test_masks.py
│   ├── test_processing.py
│   ├── test_utils.py
│   └── test_widget.py
├── .env.example            # Шаблон переменных окружения
├── htmlcov/                # Отчёт о покрытии
├── pyproject.toml
├── poetry.lock
└── README.md
```

## Лицензия

MIT
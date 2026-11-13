import json

from src.utils import process_bank_operations, process_bank_search, read_json_file


def test_read_json_file_success(tmp_path):
    """Тест успешного чтения JSON-файла."""
    data = [{"id": 1, "amount": 100}]
    file_path = tmp_path / "test.json"
    file_path.write_text(json.dumps(data), encoding="utf-8")

    result = read_json_file(str(file_path))
    assert result == data


def test_read_json_file_empty(tmp_path):
    """Тест: файл пустой."""
    file_path = tmp_path / "empty.json"
    file_path.write_text("", encoding="utf-8")

    result = read_json_file(str(file_path))
    assert result == []


def test_read_json_file_not_list(tmp_path):
    """Тест: JSON не является списком."""
    file_path = tmp_path / "not_list.json"
    file_path.write_text('{"id": 1}', encoding="utf-8")

    result = read_json_file(str(file_path))
    assert result == []


def test_read_json_file_not_found():
    """Тест: файл не найден."""
    result = read_json_file("non_existent_file.json")
    assert result == []


def test_process_bank_search_success():
    """Тест поиска по описанию."""
    data = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Перевод с карты на карту"},
    ]
    result = process_bank_search(data, "перевод")
    assert len(result) == 2


def test_process_bank_search_empty():
    """Тест, когда ничего не найдено."""
    data = [{"description": "Открытие вклада"}]
    result = process_bank_search(data, "перевод")
    assert result == []


def test_process_bank_search_invalid_regex():
    """Тест с некорректным регулярным выражением."""
    data = [{"description": "Test"}]
    result = process_bank_search(data, "[")
    assert result == []


def test_process_bank_operations():
    """Тест подсчета категорий."""
    data = [
        {"description": "Перевод организации"},
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Неизвестно"},
    ]
    categories = ["Перевод организации", "Открытие вклада"]
    result = process_bank_operations(data, categories)

    assert result == {
        "Перевод организации": 2,
        "Открытие вклада": 1,
    }

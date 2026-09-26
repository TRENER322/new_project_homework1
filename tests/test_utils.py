import json

from src.utils import read_json_file


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

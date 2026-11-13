from unittest.mock import patch

from main import main


@patch("builtins.input", side_effect=["1", "EXECUTED", "нет", "нет", "нет"])
def test_main_json(mock_input, capsys):
    """Тест основного сценария с JSON (без сортировки и фильтров)."""
    main()
    captured = capsys.readouterr()
    assert "Привет! Добро пожаловать" in captured.out
    assert "Для обработки выбран JSON-файл" in captured.out
    assert 'Операции отфильтрованы по статусу "EXECUTED"' in captured.out
    assert "Всего банковских операций в выборке" in captured.out


@patch("builtins.input", side_effect=["2", "test", "CANCELED", "нет", "нет", "нет"])
def test_main_invalid_status(mock_input, capsys):
    """Тест: ввод неверного статуса, затем корректного."""
    main()
    captured = capsys.readouterr()
    assert 'Статус операции "TEST" недоступен' in captured.out
    assert 'Операции отфильтрованы по статусу "CANCELED"' in captured.out


@patch("builtins.input", side_effect=["3", "PENDING", "да", "по возрастанию", "нет", "нет"])
def test_main_sorting(mock_input, capsys):
    """Тест сортировки по возрастанию."""
    main()
    captured = capsys.readouterr()

    # Проверяем, что программа распечатала итоговый список
    assert "Всего банковских операций в выборке" in captured.out

    # Проверяем, что input() запрашивал сортировку (так как текст приглашения не попадает в capsys)
    assert any(
        "Отсортировать операции по дате?" in str(args)
        for args, _ in mock_input.call_args_list
    )


@patch("builtins.input", side_effect=["1", "EXECUTED", "нет", "да", "да", "несуществующее_слово"])
def test_main_empty_result(mock_input, capsys):
    """Тест, когда итоговая выборка пуста."""
    main()
    captured = capsys.readouterr()
    assert "Не найдено ни одной транзакции" in captured.out

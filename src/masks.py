import logging
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False

if not logger.handlers:
    file_handler = logging.FileHandler(
        LOG_DIR / "masks.log", mode="w", encoding="utf-8"
    )
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты.

    Оставляет видимыми первые 6 цифр и последние 4 цифры.
    Остальные символы заменяются звёздочками.
    Номер разбивается по блокам: XXXX XX** **** XXXX.

    Исключения:
        ValueError: Если номер содержит не 16 цифр.
    """
    logger.debug("Начало маскировки номера карты")

    card_number = card_number.replace(" ", "")

    if len(card_number) != 16:
        logger.error(
            "Ошибка маскировки карты: неверная длина номера (%d)", len(card_number)
        )
        raise ValueError("Номер карты должен содержать ровно 16 цифр.")

    masked = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
    logger.info("Номер карты успешно замаскирован")
    return masked


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счета.

    Оставляет видимыми только последние 4 цифры.
    Перед ними добавляются две звёздочки.

    Исключения:
        ValueError: Если номер содержит менее 4 цифр.
    """
    logger.debug("Начало маскировки номера счета")

    account_number = account_number.replace(" ", "")

    if len(account_number) < 4:
        logger.error(
            "Ошибка маскировки счета: неверная длина номера (%d)",
            len(account_number),
        )
        raise ValueError("Номер счета должен содержать минимум 4 цифры.")

    masked = "**" + account_number[-4:]
    logger.info("Номер счета успешно замаскирован")
    return masked

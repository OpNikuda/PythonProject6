import logging
import os

# Настройка логгера
logger = logging.getLogger('masks')

log_path = os.path.join(os.path.dirname(__file__), '..', 'logs', 'masks.log')

file_handler = logging.FileHandler(log_path, mode='w', encoding='utf-8')
file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)

logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

logger.info("Логирование работает! Файл: masks.log в папке logs/")

# Функции с логированием ошибок
def get_mask_card_number(card_number):
    """
    Маскирует номер карты, оставляя видимыми первые шесть и последние четыре цифры.
    """
    try:
        card_number = str(card_number).replace(" ", "")
        if not card_number.isdigit() or len(card_number) < 10:
            logger.warning(f"Невалидный номер карты: {card_number}")
            return ""

        first_six = card_number[:6]
        last_four = card_number[-4:]
        masked_number = f"{first_six[:4]} {first_six[4:6]}** **** {last_four}"
        return masked_number

    except Exception:
        logger.exception(f"Ошибка при маскировании номера карты: {card_number}")
        return ""


def get_mask_account(account_number):
    """
    Маскирует номер счёта, оставляя видимыми только последние четыре цифры.
    """
    try:
        account_number = str(account_number).replace(" ", "")
        if not account_number.isdigit() or len(account_number) < 4:
            logger.warning(f"Невалидный номер счёта: {account_number}")
            return ""

        last_four = account_number[-4:]
        masked_part = "*" * (len(account_number) - 4)
        masked_account = masked_part + last_four
        return masked_account

    except Exception:
        logger.exception(f"Ошибка при маскировании счёта: {account_number}")
        return ""

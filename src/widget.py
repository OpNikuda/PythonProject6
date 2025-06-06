def mask_card_number(card_number):
    """
       Маскирует номер карты, оставляя открытыми только последние 4 цифры.

       Аргументы:
           card_number (str): Номер карты, который необходимо замаскировать.
                              Должен содержать только цифры.

       Возвращает:
           str: Замаскированный номер карты в формате '**********XXXX',
                где 'XXXX' - последние четыре цифры номера карты.
       """
    return '*' * (len(card_number) - 4) + card_number[-4:]

def mask_account_number(account_number):
    """
      Маскирует номер счёта, оставляя открытыми первые 4 и последние 4 цифры.

      Аргументы:
          account_number (str): Номер счёта, который необходимо замаскировать.
                                Должен содержать только цифры.

      Возвращает:
          str: Замаскированный номер счёта в формате 'XXXX********XXXX',
               где 'XXXX' - первые и последние четыре цифры номера счёта.
      """
    return account_number[:4] + '*' * (len(account_number) - 8) + account_number[-4:]

def mask_account_card(payment_info):
    """
       Определяет, является ли номер картой или счётом, и применяет соответствующую маскировку.

       Аргументы:
           payment_info (str): Номер карты или счёта, который необходимо замаскировать.
                               Должен содержать только цифры.

       Возвращает:
           str: Замаскированный номер карты или счёта.

       Исключения:
           ValueError: Если формат номера не валиден (содержит нецифровые символы).

       Примечание:
           Предполагается, что номера карт имеют длину до 16 цифр, а номера счётов длиннее.
       """
    if payment_info.isdigit():
        if len(payment_info) > 16:
            return mask_account_number(payment_info)
        else:
            return mask_card_number(payment_info)

print(mask_account_card('8012841482180128'))
print(mask_account_card('73654108430135874305'))
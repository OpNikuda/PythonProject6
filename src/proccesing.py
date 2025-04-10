def filter_by_state(data, state='EXECUTED'):
    """
        Фильтрует список словарей по состоянию.

        Аргументы:
        data (list): Список словарей, где каждый словарь должен содержать ключ 'state'.
        state (str): Состояние, по которому будет происходить фильтрация.
                     По умолчанию 'EXECUTED'.

        Возвращает:
        list: Новый список словарей, которые имеют указанное состояние.
        """
    return [item for item in data if item.get('state') == state]


def sort_by_date(list_of_dicts, reverse=True):
    """
       Сортирует список словарей по дате.

       Аргументы:
       list_of_dicts (list): Список словарей, где каждый словарь должен содержать ключ 'date'.
       reverse (bool): Флаг, указывающий направление сортировки.
                       Если True, сортировка производится по убыванию.
                       По умолчанию True.

       Возвращает:
       list: Новый список словарей, отсортированных по дате.
       """
    return sorted(list_of_dicts, key=lambda x: datetime.fromisoformat(x['date']), reverse=reverse)
import requests
import json
from typing import Tuple

class APIException(Exception):
    """Исключение, возникающее при ошибках в API."""
    pass

class CurrencyConverter:
    """Класс для получения курсов валют."""

    @staticmethod
    def get_price(base: str, quote: str, amount: float) -> float:
        """Метод для получения цены в заданной валюте.

        Args:
            base: Название базовой валюты.
            quote: Название валюты, в которой нужно узнать цену.
            amount: Количество базовой валюты.

        Returns:
            Цена в заданной валюте.

        Raises:
            APIException: При возникновении ошибки в API.
        """

        url = f'https://api.exchangerate-api.com/v4/latest/{base}'
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.text)
            try:
                rate = data['rates'][quote]
            except KeyError:
                raise APIException(f'Неверный формат валюты: {quote}')
            return round(rate * amount, 2)
        else:
            raise APIException(f'Ошибка API: {response.status_code}')

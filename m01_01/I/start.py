import requests


# https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=11
class ApiClient:
    def __init__(self, fetch: requests):
        self.fetch = fetch

    def get_json(self, url):
        response = self.fetch.get(url)
        return response.json()


def pretty_view(data: list[dict]):
    # Сущности не должны зависеть от интерфейсов, которые они не используют
    result = [{f"{el.get('ccy')}": {"buy": float(el.get('buy')), "sale": float(el.get('sale'))}} for el in data]
    # result это преобразование данных
    pattern = '|{:^10}|{:^10}|{:^10}|'
    print(pattern.format('currency', 'sale', 'buy'))
    for el in result:
        currency, *_ = el.keys()
        buy = el.get(currency).get('buy')
        sale = el.get(currency).get('sale')
        print(pattern.format(currency, sale, buy))


if __name__ == "__main__":
    client = ApiClient(requests)
    data = client.get_json(
        "https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=11"
    )
    pretty_view(data)
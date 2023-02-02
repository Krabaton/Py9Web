import requests

# response = requests.get('https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11')
# exchange_rate = response.json()
# print(exchange_rate)
# e487f7fc38ec658bdc8f6fa7c1906db1

response = requests.get('https://api.openweathermap.org/data/2.5/weather?lat=33&lon=66&appid=e487f7fc38ec658bdc8f6fa7c1906db1')
weather = response.json()
print(weather)

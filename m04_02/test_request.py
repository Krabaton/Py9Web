import requests

# response = requests.get('https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11')
# exchange_rate = response.json()
# print(exchange_rate)
#

response = requests.get('https://api.openweathermap.org/data/2.5/weather?lat=33&lon=66&appid=')
weather = response.json()
print(weather)

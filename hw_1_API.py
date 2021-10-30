import requests
import json

url = 'https://api.weather.yandex.ru/v2/forecast/?lat=55.7522&lon=37.6156&lang=ru_RU'
headers = {'X-Yandex-API-Key': 'd5bd5d46-ecf7-489b-9b06-394c5f420761'}
response = requests.get(url, headers=headers)


print(response.status_code)
j_data = response.json()

print(f'В {j_data.get("info").get("tzinfo").get("name")} температура {j_data.get("fact").get("temp")} градуса по Цельсию.')

with open('data.json', 'w') as outfile:
    json.dump(j_data, outfile)


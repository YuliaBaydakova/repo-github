#https://hh.ru/search/vacancy? clusters=true&area=1&ored_clusters=true&enable_snippets=true&salary=&text=%D0%A2%D0%B5%D0%BF%D0%BB%D0%BE%D1%8D%D0%BD%D0%B5%D1%80%D0%B3%D0%B5%D1%82%D0%B8%D0%BA&from=suggest_post
import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import re
import pandas as pd

url = 'https://www.hh.ru/search/vacancy'
params = {'clusters': 'true',
          'area': '1',
          'ored_clusters': 'true',
          'enable_snippets':'true',
          'text' : 'Теплоэнергетик',
          'from':'suggest_post',
          'page':0}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}

vacancy_list = []

while True:
    response = requests.get(url, params=params, headers=headers)
    #print(response.status_code)
    dom = bs(response.text, 'html.parser')
    vacancy = dom.find_all('div', {'class': 'vacancy-serp-item'})

    if response.ok and vacancy:

        for vac in vacancy:
            vacancy_data = {}
            info = vac.find('div', {'class': 'vacancy-serp-item__info'})
            name = info.text
            find_link = vac.find('a', {'class': 'bloko-link'})
            link = find_link['href']
            find_money = vac.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            werbsite = url
            try:
                money =find_money.text
            except:
                money = None
            if str(money).split()[0] == 'от':
                max_money = None
                try:
                    min_money = float((re.findall(r'\d+', str(money))[0]+re.findall(r'\d+', str(money))[1]))
                    value = str(money).split()[3]
                except:
                    min_money = float((re.findall(r'\d+', str(money))[0]))
                    value = str(money).split()[2]
            elif str(money).split()[0] == 'до':
                min_money = None
                max_money = money.split()[1] + money.split()[2]
                value = str(money).split()[3]
            elif money == None:
                min_money = None
                max_money = None
                value = None
            else:
                min_money =float ((re.findall(r'\d+', str(money))[0]+re.findall(r'\d+', str(money))[1]))
                max_money =float(money.split('–')[1].split()[0]+money.split('–')[1].split()[1])
                value = str(money).split('–')[1].split()[2]


            vacancy_data['name'] = name
            vacancy_data['link'] = link
            vacancy_data['min_money'] = min_money
            vacancy_data['max_money'] = max_money
            vacancy_data['value'] = value
            vacancy_data['site'] = url
            vacancy_list.append(vacancy_data)

        print(f"Обработана {params['page']} страница")
            #print(name, link,money, type(min_money), type(max_money), max_money, value)
        params['page'] += 1
    else:
        break
pprint(vacancy_list)
df = pd.DataFrame(vacancy_list)
df.to_csv('df_hh.csv', encoding='cp1251')


import requests
from pprint import pprint
from lxml import html
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
response = requests.get('https://yandex.ru/news/')
dom = html.fromstring(response.text)
pprint(response.status_code)
list_news = []


#items = dom.xpath("//article//div/a/h2[@class='mg-card__title']/text()")  #заголовок новости
#news1 = dom.xpath("//article//div[@class='mg-card__inner']/a/@href") #ссылка на главную новость
#news = dom.xpath("//article//div[@class='mg-card__text']/a/@href")  #ссылка на все новости кроме первой
#source = dom.xpath("//article//div//span[@class='mg-card-source__source']/a[@aria-label]/text()") #источник информации
#time = dom.xpath("//article//div//span[@class='mg-card-source__time']/text()")#время публикации

items = dom.xpath("//article")
i = 1
for item in items:
    news = {}
    if i == 1:
       link = item.xpath(".//div[@class='mg-card__inner']/a/@href")
    else:
        link = item.xpath(".//div[@class='mg-card__text']/a/@href")
    name = item.xpath(".//div/a/h2[@class='mg-card__title']/text()")
    source = item.xpath(".//div//span[@class='mg-card-source__source']/a[@aria-label]/text()")
    time = item.xpath(".//div//span[@class='mg-card-source__time']/text()")

    print(i,str(name).replace('\\xa0',' '))
    i += 1

    news['_id'] = str(link)
    news['name'] = str(name).replace('\\xa0',' ')
    news['link'] = link
    news['source'] = source
    news['time'] = time

    list_news.append(news)
pprint(list_news)

client = MongoClient('127.0.0.1', 27017)
db = client['test_database']
collection = db.news

def insert_doc_in_db (data, collection): #запись документа в БД
    for doc in data:
        try:
            collection.insert_one(doc)              # добавляем один документ в базу
        except dke:                                 # если документ уже есть в базе - конфликт по _id
            print(f"Документ с id = {doc['_id']} уже существует в базе")

insert_doc_in_db (list_news, collection)

for item in db.news.find({'source': 'ТАСС'}): #проверка записи документа в БД
   pprint(item)

result = db.news.count_documents({'source': 'ТАСС'})
print(f'Новостей в БД - {result}.')
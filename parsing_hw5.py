from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException as ENIE
from pprint import pprint
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke

chrome_options = Options()
chrome_options.add_argument('--windows_size=1920,1080')
driver = webdriver.Chrome(executable_path='chromedriver',options=chrome_options)
driver.get('https://www.mvideo.ru/')
driver.implicitly_wait(10)
driver.execute_script("window.scrollTo(0, 2000)")
driver.implicitly_wait(10)
button = driver.find_element(By.XPATH,'//span[contains(.," В тренде ")]').click()
while True:
    try:
        #button = driver.find_element(By.XPATH,'.//mvid-shelf-group/mvid-carousel/div[2]/button[2]').click()
        button = driver.find_element(By.XPATH, './/mvid-shelf-group/mvid-carousel/div[@class = "button-size--medium buttons"]/\
               button[@class = "btn forward mv-icon-button--primary mv-icon-button--shadow mv-icon-button--medium mv-button mv-icon-button"]').click()
    except ENIE:
        print('Все данные загружены!')
        break

list_products = []
list_price =[]
items = driver.find_elements(By.XPATH,'//mvid-shelf-group/mvid-carousel//mvid-product-cards-group/div[@class="product-mini-card__name ng-star-inserted"]')
prices = driver.find_elements(By.XPATH,'//mvid-shelf-group/mvid-carousel//mvid-product-cards-group/div[@class="product-mini-card__price ng-star-inserted"]')


for item in items: #наименование и ссылка на товар
    products = {}
    name = item.find_element(By.XPATH,'./div[@class ="title"]').text
    link = item.find_element(By.XPATH,'./div[@class ="title"]/a').get_attribute('href')
    products['_id'] = name + link
    products['name'] = name
    products['link'] = link
    list_products.append(products)
for price in prices: #стоимость товара
    prices_name = {}
    price_name = price.find_element(By.XPATH, './/span[@class ="price__main-value"]').text
    prices_name['price_name'] = price_name
    list_price.append(prices_name)

summary_list=[]
for x in range(len(list_products)):
    list_products[x].update(list_price[x])
    summary_list.append(list_products[x])

pprint(summary_list)

client = MongoClient('127.0.0.1', 27017)
db = client['test_database']
collection = db.products

def insert_doc_in_db (data, collection): #запись документа в БД
    for doc in data:
        try:
            collection.insert_one(doc)              # добавляем один документ в базу
        except dke:                                 # если документ уже есть в базе - конфликт по _id
            print(f"Документ с id = {doc['_id']} уже существует в базе")

insert_doc_in_db (summary_list, db.products)

for item in db.products.find({'name': 'Триммер Braun Styling Kit 5 100 Years'}): #проверка записи документа в БД
    pprint(item)

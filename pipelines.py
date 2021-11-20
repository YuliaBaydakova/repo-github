# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
class LeryaparserPipeline:
    def __init__(self):
        client = MongoClient('localhost',27017)
        self.mongo_base = client['product_2011']

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        name = item['name']
        photos = item['photos']
        url = item['url']
        price = self.process_price(item['price_rub'],item['price_kop'])
        product_unit = {'name': name, 'photos': photos, 'price': price, 'url': url}
        collection.insert_one(product_unit)
        print(name, photos, price,url)
        return item

    def process_price(self,price_rub,price_kop):
        price_rub = price_rub.replace(' ','')
        if price_rub and price_kop:
            result = float(price_rub) + float(price_kop) / 100
        elif price_kop == None:
            result = float(price_rub)
        elif price_rub == None:
            result = float(price_kop) / 100
        return result

class LeryaPhotosPipepline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photos']=[itm[1] for itm in results if itm[0]]
        return item
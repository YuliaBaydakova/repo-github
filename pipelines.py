# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost',27017)
        self.mongo_base = client['vacancies_1311']
    def process_item(self, item, spider):
        if spider.name=='hhru':
            item['salary'] = self.salary_hh(item['salary'])
        else:
            item['salary'] = self.salary_sj(item['salary'])

        collection =self.mongo_base[spider.name]
        name = item['name']
        min_salary = item['salary'][0]
        max_salary = item['salary'][1]
        url = item['url']
        vacancy_unit = {'name': name,'min_salary':min_salary,'max_salary': max_salary, 'url': url}
        collection.insert_one(vacancy_unit)

        return item

    def salary_hh(self,salary):
        try:
            if str(salary[0]) == 'от ' and str(salary[2]) == ' до ':
                min_salary = salary[1].replace('\xa0', '')
                max_salary = salary[3].replace('\xa0', '')
            elif str(salary[0]) == 'з/п не указана':
                min_salary = None
                max_salary = None
            elif str(salary[0]) == 'до ':
                min_salary = None
                max_salary = salary[1].replace('\xa0', '')
            elif str(salary[0]) == 'от ':
                min_salary = salary[1].replace('\xa0', '')
                max_salary = None
        except:
            min_salary = None
            max_salary = None
        result = [min_salary, max_salary]
        return result

    def salary_sj(self, salary):
        try:
            if str(salary[0]) == 'от':
                min_salary = salary[2].replace('\xa0', '').replace('руб.', '')
                max_salary = None
            elif str(salary[0]) == 'до':
                min_salary = None
                max_salary = salary[2].replace('\xa0', '').replace('руб.', '')
            elif str(salary[0]) == 'По договорённости':
                min_salary = None
                max_salary = None
            elif salary[0].replace('\xa0', '').isdigit() and len(salary) == 4:
                min_salary = salary[0].replace('\xa0', '')
                max_salary = salary[1].replace('\xa0', '')
            elif salary[0].replace('\xa0', '').isdigit() and len(salary) == 3:
                min_salary = salary[0].replace('\xa0', '')
                max_salary = salary[0].replace('\xa0', '')
        except:
            min_salary = None
            max_salary = None
        result = [min_salary, max_salary]
        return result

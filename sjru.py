import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python&geo%5Bt%5D%5B0%5D=4']

    def parse(self, response:HtmlResponse):
        next_page = response.xpath("//a[@rel='next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//div[@class ='Fo44F QiY08 LvoDO']//span/a[@target='_blank']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self,response:HtmlResponse):
        name = response.xpath("//h1/text()").get()
        salary = response.xpath("//span[@class = '_2Wp8I _185V- _1_rZy Ml4Nx']/text()").getall()
        url = response.url
        yield JobparserItem(name=name,salary=salary,url=url)

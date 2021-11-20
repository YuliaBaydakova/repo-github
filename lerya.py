import scrapy
from scrapy.http import HtmlResponse
from leryaparser.items import LeryaparserItem
from scrapy.loader import ItemLoader

class LeryaSpider(scrapy.Spider):
    name = 'lerya'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/search/?q=плитка']

    def parse(self, response):
        next_page = response.xpath("//a[@data-qa-pagination-item='right']/@href").get()
        if next_page:
            yield response.follow(next_page,callback=self.parse)
        links = response.xpath("//a[@class='bex6mjh_plp b1f5t594_plp p5y548z_plp pblwt5z_plp nf842wf_plp']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.product_parse)



    def product_parse(self, response:HtmlResponse):
        loader = ItemLoader(item=LeryaparserItem(),response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('price_rub',"//span[@slot='price']/text()")
        loader.add_xpath('price_kop',"//span[@slot='fract']/text()")
        loader.add_xpath('photos',"//img[@alt = 'product image']/@data-origin")
        loader.add_value('url',response.url)
        yield loader.load_item()
        #name = response.xpath("//h1/text()").get()
        #price_rub = response.xpath("//span[@slot='price']/text()").get()
        #price_kop = response.xpath("//span[@slot='fract']/text()").get()
        #url = response.url
        #photos = response.xpath("//img[@alt = 'product image']/@data-origin").getall()
        #yield LeryaparserItem(name=name, price_rub=price_rub, price_kop=price_kop, url=url,photos=photos)
        #print(name, price)
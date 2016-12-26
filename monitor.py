# -*- coding: utf-8 -*-
import scrapy


class Product(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    platinum = scrapy.Field()


class MonitorSpider(scrapy.Spider):
    name = 'monitor'

    def __init__(self, products=['guitarra-telecaster']):
        self.start_urls = [
            'http://lista.mercadolivre.com.br/%s' % product
            for product in products]
        super(MonitorSpider, self).__init__()

    def parse(self, response):
        row_items = response.xpath("//ol[@id='searchResults']")[0] \
            .xpath(".//div[@class='rowItem']")
        for row_item in row_items:
            item = Product()

            item['name'] = row_item.xpath(
                ".//h2/a/text()").extract()

            details = row_item.xpath(".//ul[@class='details']")[0]

            item['price'] = details.xpath(".//span[@class='ch-price']")[0] \
                .xpath("text()").extract()[0]

            item['platinum'] = details.xpath(
                ".//li[@title='MercadoL&iacute;der Platinum']").extract() != []

            yield item

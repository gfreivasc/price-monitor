# -*- coding: utf-8 -*-
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from models import ProductItem


MAX_ITEMS_KBM = 100
BASE_URL_KBM = "http://www.kabum.com.br/"
URL_SUFIX_KBM = "?limite=100"


kbm_map = {
    "hardware": [
        "placa-de-video-vga"
    ]
}


class MonitorSpider(CrawlSpider):
    name = 'monitor'
    allowed_domains = ["kabum.com.br"]

    rules = (
        Rule(
            LxmlLinkExtractor(
                allow=(),
                restrict_xpaths=(
                    "(//form[@name='listagem'])[last()]//td[last()]//a[1]")),
            callback="parse_page",
            follow=True),
    )

    def __init__(self):
        self.start_urls = []
        for k, v in kbm_map.iteritems():
            for cat in v:
                self.start_urls.append(
                    BASE_URL_KBM + k + '/' + cat + URL_SUFIX_KBM)
        super(MonitorSpider, self).__init__()

    def parse_page(self, response):
        listing = response.xpath("//div[@class='listagem-box']")

        for item in listing:
            product = ProductItem()

            product['name'] = item.xpath(
                ".//span[@class='H-titulo']/a/text()").extract_first()
            product['category'] = response.url.split('/')[-1].split('?')[0]
            rating = item.xpath(
                ".//div[@style='margin:0; font-size:10px;']/@class"
            ).extract_first().split()[-1]
            product['rating'] = 0 if rating == 'e' else int(rating[-1])
            product['price'] = float(item.xpath(
                ".//div[@class='listagem-precoavista']/b/text()"
            ).extract_first().split()[-1].replace('.', '').replace(',', '.'))

            yield product
    parse_start_url = parse_page

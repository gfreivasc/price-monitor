# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from price_monitor.items import ProductItem
from price_monitor.db.database import db_connect, db_session
from price_monitor.db.models import Product


class KbmMonitorSpider(CrawlSpider):
    name = 'kbm_monitor'
    allowed_domains = ['kabum.com.br']
    start_urls = ['https://www.kabum.com.br']

    rules = (
        Rule(
            LinkExtractor(
                allow=(),
                restrict_xpaths=(
                    '//p[@class="bot-categoria"]/a'))),
        Rule(
            LinkExtractor(
                allow=(),
                restrict_xpaths=(
                    '(//form[@name="listagem"])[last()]//td[last()]//a[1]')),
            callback='parse_page',
            follow=True),
    )

    def __init__(self, *args, **kwargs):
        self.mark_all_unseen()
        super(KbmMonitorSpider, self).__init__(*args, **kwargs)

    def mark_all_unseen(self):
        session = db_session(db_connect())

        try:
            session.query(Product).update(
                {Product.on_last_scan: False}
            )
            session.commit()
        except:
            session.rollback()
        finally:
            session.close()

    def parse_page(self, response):
        listing = response.xpath('//div[@class="listagem-box"]')

        for item in listing:
            product = ProductItem()

            product['name'] = item.xpath(
                './/span[@class="H-titulo"]/a/text()').extract_first()
            product['url'] = item.xpath(
                './/span[@class="H-titulo"]/a/@href').extract_first()
            product['category'] = response.url.split('/')[-1].split('?')[0]
            rating = item.xpath(
                './/div[@style="margin:0; font-size:10px;"]/@class'
            ).extract_first().split()[-1]
            product['rating'] = 0 if rating == 'e' else int(rating[-1])
            product['price'] = float(item.xpath(
                './/div[@class="listagem-precoavista"]/b/text()'
            ).extract_first().split()[-1].replace('.', '').replace(',', '.'))

            yield product
    parse_start_url = parse_page

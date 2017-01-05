# -*- coding: utf-8 -*-
from scrapy import Item, Field


class ProductItem(Item):
    name = Field()
    url = Field()
    category = Field()
    rating = Field()
    price = Field()

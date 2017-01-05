# -*- coding: utf-8 -*-
from price_monitor.db.models import Product, Price
from price_monitor.db.database import db_connect, db_session, create_tables
from datetime import datetime


class PriceMonitorPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_tables(engine)
        self.Session = db_session(engine)

    def process_item(self, item, spider):
        session = self.Session()
        product = session.query(Product).filter_by(url=item['url']).first()
        if product is None:
            product = Product(
                name=item['name'],
                url=item['url'],
                category=item['category'],
                rating=item['rating'],
                last_price=item['price']
            )

        price = Price(
            product=product,
            value=item['price'],
            when_read=datetime.now()
        )

        try:
            session.add(product)
            session.add(price)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item

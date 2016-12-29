from sqlalchemy.orm import sessionmaker
from models import db_connect, create_tables, Product, Price
from datetime import datetime


class PriceMonitorPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_tables(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        product = session.query(Product).filter_by(name=item['name']).first()
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

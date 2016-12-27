from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
import settings
import scrapy


DeclarativeBase = declarative_base()


class ProductItem(scrapy.Item):
    name = scrapy.Field()
    category = scrapy.Field()
    rating = scrapy.Field()
    price = scrapy.Field()


def db_connect():
    return create_engine(URL(**settings.DATABASE))


def create_tables(engine):
    DeclarativeBase.metadata.create_all(engine)


class Product(DeclarativeBase):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    name = Column('name', String)
    category = Column('category', String)
    rating = Column('rating', Integer)
    prices = relationship("Price", backref="product")
    last_price = Column('last_price', Float)


class Price(DeclarativeBase):
    __tablename__ = "price"

    id = Column(Integer, primary_key=True)
    value = Column('value', Float)
    when_read = Column('when_read', DateTime)
    product_id = Column(Integer, ForeignKey("product.id"))

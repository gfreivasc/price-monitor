from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
import settings
import scrapy


DeclarativeBase = declarative_base()


class Product(scrapy.Item):
    name = scrapy.Field()
    category = scrapy.Field()
    rating = scrapy.Field()
    price = scrapy.Field()


def db_connect():
    return create_engine(URL(**settings.DATABASE))


def create_tables(engine):
    DeclarativeBase.metadata.create_all(engine)


class Products(DeclarativeBase):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column('name', String)
    category = Column('category', String)
    rating = Column('rating', Integer)


class Prices(DeclarativeBase):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True)
    value = Column('value', Integer)
    when_read = Column('when_read', DateTime)
    product_id = Column(Integer, ForeignKey("products.id"))

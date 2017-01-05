# -*- coding: utf-8 -*-
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Float
from sqlalchemy.orm import relationship
from price_monitor.db.database import DeclarativeBase


class Product(DeclarativeBase):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    name = Column('name', String)
    url = Column('url', String)
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

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from price_monitor import settings


DeclarativeBase = declarative_base()


def db_connect():
    return create_engine(URL(**settings.DATABASE))


def db_session(engine):
    return scoped_session(sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine))


def create_tables(engine):
    DeclarativeBase.metadata.create_all(engine)

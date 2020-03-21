from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from utils import logger as lg

dbUrl = 'mysql+mysqlconnector://%s:%s@%s/%s?charset=utf8' % (
    "mousehouse",
    "mousehouse",
    "localhost",
    "msDB",)
engine = create_engine(dbUrl, encoding = "utf-8", echo=True)
Session = sessionmaker(
        autocommit = False,
        autoflush = True,        
        bind = engine)
session = Session()
Base = declarative_base()
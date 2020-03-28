from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from utils.logger import get_logger
from config.config_reader import conf

"""
Connect DB server and make session.
"""
logger = get_logger(__name__, True)
dbUrl = 'mysql+mysqlconnector://%s:%s@%s/%s?charset=utf8' % (
    conf["db"]["user"],
    conf["db"]["pass"],
    conf["db"]["ip"],
    conf["db"]["name"])
engine = create_engine(dbUrl, encoding = "utf-8")
Session = sessionmaker(
        autocommit = False,
        autoflush = True,        
        bind = engine)
session = Session()
Base = declarative_base()
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from utils.logger import get_logger
from config.config_reader import conf

"""
Connect DB server and make session.
"""
logger = get_logger(__name__, True)
db_url = '%s+%s://%s:%s@%s/%s?charset=utf8' % (
    conf['db']['sql'].lower(),
    conf['db']['connector'].lower(),
    conf["db"]["user"],
    conf["db"]["pass"],
    conf["db"]["ip"],
    conf["db"]["name"])
try:
    engine = create_engine(db_url, encoding = "utf-8")
except:
    logger.error("Invalid configration. Check config.ini file.")
    exit(0)

Session = sessionmaker(
    autocommit = False,
    autoflush = True,        
    bind = engine)
session = Session()
Base = declarative_base()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from utils import logger as lg
from utils.configReader import conf

"""
Connect DB server and make session.
"""
logger = lg.getLogger(__name__, True)
dbUrl = 'mysql+mysqlconnector://%s:%s@%s/%s?charset=utf8' % (
    "mousehouse",
    "mousehouse",
    conf["master"]["ip"],
    "msDB")
engine = create_engine(dbUrl, encoding = "utf-8")
Session = sessionmaker(
        autocommit = False,
        autoflush = True,        
        bind = engine)
session = Session()
Base = declarative_base()
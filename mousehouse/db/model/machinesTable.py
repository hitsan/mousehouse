from sqlalchemy import Table, Column
from sqlalchemy.types import Integer, String, Boolean
from ..dbManager import Base

class Machine(Base):
    __tablename__ = 'machines'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    mId = Column('ID', Integer(), primary_key=True, autoincrement=True)
    ip_addr = Column('IP', String(15), unique=True, nullable=False)
    status = Column('Status', Boolean)
    mac_addr = Column('Mac', String(255))

    def __init__(self, ip_addr, status=None, mac_addr=None):
        self.ip_addr = ip_addr
        self.status = status
        self.mac_addr = mac_addr
from sqlalchemy import Table, Column
from sqlalchemy.types import Integer, String, Boolean
from db.dbSetting import Base
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

class Slave(Base):
    """
    Model Slave Table.
    """
    __tablename__ = 'slave'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id = Column('ID', Integer(), primary_key=True, autoincrement=True)
    ip = Column('IP', String(15), unique=True, nullable=False)
    status = Column('Status', Boolean,server_default=None)
    mac = Column('MAC_ADDRESS', String(255),unique=True,server_default=None)

class SlaveSchema(SQLAlchemySchema):
    """
    Slave Table Schema.
    """
    class Meta:
        model = Slave
        load_instance = True

    id = auto_field()
    ip = auto_field()
    status = auto_field()
    mac = auto_field()

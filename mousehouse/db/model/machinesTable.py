from sqlalchemy import Table, Column
from sqlalchemy.types import Integer, String, Boolean
from db.dbSetting import Base
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

class Machine(Base):
    __tablename__ = 'machines'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id = Column('ID', Integer(), primary_key=True, autoincrement=True)
    ip = Column('IP', String(15), unique=True, nullable=False)
    status = Column('Status', Boolean)
    mac = Column('Mac', String(255),unique=True)

    def __init__(self, ip, status=None, mac=None):
        self.ip = ip
        self.status = status
        self.mac = mac

class MachineSchema(SQLAlchemySchema):
    class Meta:
        model = Machine
        load_instance = True

    id = auto_field()
    ip = auto_field()
    status = auto_field()
    mac = auto_field()

machine_schema = MachineSchema(many=True)
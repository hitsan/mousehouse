from sqlalchemy import Table, Column
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, String, Boolean
from sqlalchemy.sql.sqltypes import BigInteger
from db.setting import Base
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import Schema, fields

class Mouse(Base):
    """
    Model Mouse Table.
    """
    __tablename__ = 'mice'

    ID = Column('ID', Integer(), primary_key=True, autoincrement=True)
    IP = Column('IP', String(15), unique=True, nullable=False)
    Status = Column('Status', Boolean,server_default=None)
    MAC = Column('MAC_ADDRESS', String(255),unique=True,server_default=None)
    OS = Column('OS', String(15))
    User = Column('User', String(15))
    Host = Column('Host', String(15))
    Password = Column('PASSWORD', String(255))
    Data = Column('Data', String(255))
    Description  = Column('DESCRIPTION', String(255))
    version = Column(BigInteger, nullable=False)
    __mapper_args__ = {'version_id_col': version}

class MouseSchema(SQLAlchemySchema):
    """
    Mouse Table Schema.
    """
    uppername = fields.Function(lambda obj: obj.name.upper())

    class Meta:
        fields = ("ID", "IP", "MAC", "Status", "OS", "User", "Host", "Description")
        model = Mouse
        load_instance = True
        ordered = True
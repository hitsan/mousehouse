from sqlalchemy import Table, Column
from sqlalchemy.types import Integer, String, Boolean
from sqlalchemy.sql.sqltypes import BigInteger
from db.setting import Base
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import Schema, fields

class Mouse(Base):
    """
    Model Mouse Table.
    """
    __tablename__ = 'mouse'

    id = Column('ID', Integer(), primary_key=True, autoincrement=True)
    ip = Column('IP', String(15), unique=True, nullable=False)
    status = Column('Status', Boolean,server_default=None)
    mac = Column('MAC_ADDRESS', String(255),unique=True,server_default=None)
    version = Column(BigInteger, nullable=False)
    __mapper_args__ = {'version_id_col': version}

class MouseSchema(SQLAlchemySchema):
    """
    Mouse Table Schema.
    """
    uppername = fields.Function(lambda obj: obj.name.upper())

    class Meta:
        fields = ("id", "ip", "mac", "status")
        model = Mouse
        load_instance = True
        ordered = True
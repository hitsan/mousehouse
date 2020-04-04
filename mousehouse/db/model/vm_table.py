from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.types import Integer, String, Boolean
from sqlalchemy.sql.sqltypes import BigInteger
from db.setting import Base
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import Schema, fields

class Vm(Base):
    """
    Model VM
    """
    __tablename__ = 'vms'

    ID = Column('ID', Integer(), primary_key=True, autoincrement=True)
    Type =  Column('Type', String(15), nullable=False)
    Prent_IP = Column('Prent_IP', String(15), ForeignKey('mice.IP'))
    IP = Column('IP', String(15))
    Forwarding_port = Column('port', Integer())
    Status = Column('Status', Boolean, server_default=None)
    OS = Column('OS', String(15))
    User = Column('User', String(15))
    Host = Column('Host', String(15))
    Password = Column('PASSWORD', String(255))
    Description  = Column('DESCRIPTION', String(255))
    version = Column(BigInteger, nullable=False)
    __mapper_args__ = {'version_id_col': version}

class VmSchema(SQLAlchemySchema):
    """
    Mouse Table Schema.
    """
    uppername = fields.Function(lambda obj: obj.name.upper())

    class Meta:
        fields = ("ID", "Type", "IP", "Forwarding_port", "Status", "OS", "User", "Host", "Description")
        model = Vm
        load_instance = True
        ordered = True

# class VirtaulSchema(SQLAlchemySchema):
#     """
#     Mouse Table Schema.
#     """
#     uppername = fields.Function(lambda obj: obj.name.upper())

#     class Meta:
#         fields = ("ID", "Type", "IP", "Forwarding_port", "Status", "OS", "User", "Host", "Description")
#         model = Vm
#         load_instance = True
#         ordered = True

# class DockerSchema(SQLAlchemySchema):
#     """
#     Mouse Table Schema.
#     """
#     uppername = fields.Function(lambda obj: obj.name.upper())

#     class Meta:
#         fields = ("ID", "Type", "IP", "Forwarding_port", "Status", "User", "Host", "Description")
#         model = Vm
#         load_instance = True
#         ordered = True
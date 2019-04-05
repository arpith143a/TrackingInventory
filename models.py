from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Unicode

USERNAME = "postgres"
PASSWORD = "postgres"
DATABASE = "postgres"
DATABASE_URI = "postgresql://%s:%s@localhost/%s" % (USERNAME, PASSWORD,
        DATABASE)

Base = declarative_base()

class Item(Base):
    __tablename__ = "item"
    id = Column('id', Integer, primary_key=True)
    name = Column('name', Unicode)
    serial_number = Column('serial_number', Unicode)
    value = Column('value', Integer)

    # def __init__(self):
    #     super(Item, self).__init__()
    #     id = Column('id', Integer, primary_key=True)
    #     name = Column('name', Unicode)
    #     serial_number = Column('serial_number', Unicode)
    #     value = Column('value', Integer)
        



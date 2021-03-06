import sqlalchemy as db
from requests import Session
from sqlalchemy import Table, Column, Integer, String, MetaData

engine = db.create_engine('sqlite:///gmail.db', echo=True)
meta = db.MetaData()


mail = Table(
   'mail', meta,
   Column('id', Integer, primary_key=True),
   Column('description', String),
   Column('thID', String),
)
session = Session()
meta.create_all(engine)

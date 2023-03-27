from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from datetime import datetime

from database import db


Base = declarative_base()


class Client(Base):
    __tablename__ = 'clients'
    name = Column(String, primary_key=True, nullable=False)
    password = Column(String, nullable=False)
    accounts = relationship('Account', back_populates='client')


class Account(Base):
    __tablename__ = 'accounts'
    name = Column(String, primary_key=True, nullable=False)
    client_name = Column(String, ForeignKey('clients.name'))
    client = relationship('Client', back_populates='account')
    source_of_income = Column(String, nullable=True)
    transactions = relationship('Transaction', back_populates='account')


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, nullable=False)
    date = Column(DateTime, default=datetime.now())
    value = Column(Float, nullable=False)
    account_name = Column(String, ForeignKey('accounts.name'))
    account = relationship('Account', back_populates='transactions')


Base.metadata.create_all(db)

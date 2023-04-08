from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from datetime import datetime

from database import db


Base = declarative_base()


class ClientModel(Base):
    __tablename__ = 'clients'
    name = Column(String, primary_key=True, nullable=False)
    password = Column(String, nullable=False)
    accounts = relationship('AccountModel', lazy=True, back_populates='client')
    transactions = relationship('TransactionModel', lazy=True,
                                back_populates='client')


class AccountModel(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    client_name = Column(String, ForeignKey('clients.name'))
    client = relationship('ClientModel', back_populates='accounts')
    transactions = relationship('TransactionModel', back_populates='account')


class TransactionModel(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, nullable=False)
    date = Column(DateTime, default=datetime.now())
    value = Column(Float, nullable=False)
    client_name = Column(String, ForeignKey('clients.name'))
    client = relationship('ClientModel', back_populates='transactions')
    account_name = Column(String, ForeignKey('accounts.name'))
    account = relationship('AccountModel', back_populates='transactions')
    source_of_income = Column(String, nullable=True)


Base.metadata.create_all(db)

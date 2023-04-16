from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, ForeignKey
from datetime import datetime
from typing import List, Optional

from database import db


Base = declarative_base()


class ClientModel(Base):
    __tablename__ = 'clients'
    name: Mapped[str] = mapped_column(String(100), primary_key=True)
    password: Mapped[str] = mapped_column(String(100))
    accounts: Mapped[List['AccountModel']] = relationship(
        back_populates='client', cascade='all, delete-orphan')
    transactions: Mapped[List['TransactionModel']] = relationship(
        back_populates='client', cascade='all, delete-orphan')


class AccountModel(Base):
    __tablename__ = 'accounts'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    client_name: Mapped[str] = mapped_column(String(100),
                                             ForeignKey('clients.name'))
    client: Mapped['ClientModel'] = relationship(back_populates='accounts')
    transactions: Mapped[List['TransactionModel']] = relationship(
        back_populates='account', cascade='all, delete-orphan')


class TransactionModel(Base):
    __tablename__ = 'transactions'
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column(default=datetime.now())
    value: Mapped[float] = mapped_column()
    client_name: Mapped[str] = mapped_column(String(100),
                                             ForeignKey('clients.name'))
    client: Mapped['ClientModel'] = relationship(back_populates='transactions')
    account_name: Mapped[str] = mapped_column(String(100),
                                              ForeignKey('accounts.name'))
    account: Mapped['AccountModel'] = relationship(
        back_populates='transactions')
    source_of_income: Mapped[Optional[str]] = mapped_column(String(100))


Base.metadata.create_all(db)

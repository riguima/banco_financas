from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class Conta(Base):
    __tablename__ = 'contas'
    id = Column(Integer, primary_key=True)
    conta = Column(String(50), nullable=False)
    saldo = Column(Float, nullable=False)
    fonte_de_renda = Column(String(50), nullable=True)

    def __str__(self):
        return f"{self.conta}: {locale.currency(self.saldo, grouping=True)}"

class Transacao(Base):
    __tablename__ = 'transacoes'

    id = Column(Integer, primary_key=True)
    data = Column(DateTime)
    valor = Column(Float)
    conta = Column(String(50))

# Cria a conexão com o banco de dados usando o SQLAlchemy
engine = create_engine(os.getenv('DATABASE_URI'))
Session = sessionmaker(bind=engine)

# Cria as tabelas se elas ainda não existirem
Base.metadata.create_all(engine)

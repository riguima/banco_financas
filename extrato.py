from cachetools import TTLCache, cached
import pandas as pd
import locale
import re
import datetime
from sqlalchemy.orm import Session
from sqlalchemy import text
from tabulate import tabulate
from prettytable import PrettyTable

locale.setlocale(locale.LC_ALL, 'pt_BR.utf-8')

cache = TTLCache(maxsize=100, ttl=60)
last_transaction_date = None  # variável global para armazenar a data da última transação


def get_transacoes(conta, conn):
    query = f"SELECT DATE_FORMAT(data, '%d/%m/%Y %H:%i') as data, valor, conta FROM transacoes WHERE conta = '{conta}'"
    transacoes = conn.execute(text(query)).fetchall()
    return transacoes


@cached(cache)
def get_transacoes_cached(conta, conn):
    global last_transaction_date
    transacoes = None
    query_date = conn.execute(text("SELECT MAX(data) as max_date FROM transacoes")).fetchone()[0]
    max_date = datetime.datetime.strptime(query_date, '%Y-%m-%d %H:%M:%S') if query_date else None

    if max_date and (not last_transaction_date or max_date > last_transaction_date):
        transacoes = get_transacoes(conta, conn)
        last_transaction_date = max_date
    elif not max_date:
        last_transaction_date = None

    return transacoes


def extrato(contas, conn):
    conn.close()

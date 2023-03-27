from PySide6 import QtWidgets
from importlib import import_module
import inspect
import datetime
from database import Session
from models import Account, Transaction
from datetime import datetime, date


class DefaultAccount(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

    def make_transaction(self, account_name: str, value: float) -> None:
        with Session() as session:
            account = session.query(Account).get(account_name)
            account.transactions.append(Transaction(value=value))
            session.commit()

    def get_transactions(self, account_name: str, start_date: date, end_date: date = datetime.now().date()) -> list[Transaction]:
        with Session() as session:
            return session.query(Transaction).filter_by(
                account_name=account_name
            ).filter(start_date <= Transaction.date <= end_date).all()


def get_widget(account_name: str) -> DefaultAccount:
    try:
        module = import_module(f'widgets.{account_name.lower()}')
        for _, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and obj in DefaultAccount.__subclasses__():
                return obj()
    except ModuleNotFoundError:
        pass
    return DefaultAccount()

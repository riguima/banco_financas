from PySide6 import QtWidgets
from importlib import import_module
import inspect
from datetime import datetime, date
from dataclasses import dataclass
from abc import ABC, abstractmethod

from widgets import default


@dataclass
class Transaction:
    id: int
    date: date = datetime.now().date()
    value: float
    source_of_income: str


@dataclass
class Account:
    name: str


@dataclass
class Client:
    name: str
    password: str


class IAccountRepository(ABC):

    @abstractmethod
    def add(self, account_name: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def make_transaction(self, account_name: str, value: float) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_transactions(self, account_name: str,
                         start_date: date = datetime.now().date(),
                         final_date: date = datetime.now().date()) -> list[Transaction]:
        raise NotImplementedError()


def get_action_widget(account_name: str, action: str,
                      parent: QtWidgets.QWidget) -> QtWidgets.QWidget:
    try:
        module = import_module(f'widgets.{account_name.lower()}')
        get_obj_from_module(module, action, account_name, parent)
    except ModuleNotFoundError:
        pass
    module = import_module('widgets.default')
    get_obj_from_module(module, action, account_name, parent)


def get_obj_from_module(module, action: str, account_name: str,
                        parent: QtWidgets.QWidget) -> QtWidgets.QWidget:
    for _, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and obj.__name__ == action.title().replace(
            ' ', ''
        ):
            return obj(account_name, parent)

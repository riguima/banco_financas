from PySide6 import QtWidgets
from importlib import import_module
import inspect
from datetime import datetime, date
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class Transaction:
    id: int
    value: float
    source_of_income: str
    date: date = datetime.now().date()


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
    def delete(self, account_name: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def make_transaction(self, account_name: str, value: float) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_all_transactions(self, account_name: str) -> list[Transaction]:
        raise NotImplementedError()

    @abstractmethod
    def get_transactions_per_date(self, account_name: str,
                                  start_date: date = datetime.now().date(),
                                  final_date: date = datetime.now().date()
                                  ) -> list[Transaction]:
        raise NotImplementedError()


def get_action_widget(account_name: str, action: str,
                      parent: QtWidgets.QWidget) -> QtWidgets.QWidget:
    try:
        module = import_module(f'widgets.{account_name.lower()}')
        obj = get_obj_from_module(module, action, account_name, parent)
        if obj is None:
            module = import_module('widgets.default')
            return get_obj_from_module(module, action, account_name, parent)
        return obj
    except ModuleNotFoundError:
        module = import_module('widgets.default')
        return get_obj_from_module(module, action, account_name, parent)


def get_obj_from_module(module, action: str, account_name: str,
                        parent: QtWidgets.QWidget) -> QtWidgets.QWidget:
    for _, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and obj.__name__ == action.title().replace(
            ' ', ''
        ):
            return obj(account_name, parent)

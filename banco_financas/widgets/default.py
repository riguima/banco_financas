from PySide6 import QtWidgets, QtGui, QtCore
from datetime import datetime

from database import Session
from domain import get_current_client
from models import Account, Transaction
from helpers import HLayout, Button, BaseWidget


class AdicionarDinheiro(QtWidgets.QWidget):

    def __init__(self, account_name: str, parent: QtWidgets.QWidget):
        super().__init__()
        self.parent = parent
        self.account_name = account_name
        self.setFixedSize(250, 200)
        self.message_box = QtWidgets.QMessageBox()

        self.value_text = QtWidgets.QLabel('Valor')
        self.input_value = QtWidgets.QLineEdit()
        self.input_value.setValidator(QtGui.QDoubleValidator())
        self.input_value_layout = HLayout(self.value_text, self.input_value)

        self.button = Button('Adicionar dinheiro')
        self.button.clicked.connect(self.add_money)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addLayout(self.input_value_layout)
        self.layout.addWidget(self.button)

    @QtCore.Slot()
    def add_money(self):
        with Session() as session:
            account = session.query(Account).filter_by(
                client_name=get_current_client(session).name
            ).filter_by(name=self.account_name).first()
            account.transactions.append(Transaction(
                value=float(self.input_value.text().replace(',', '.'))
            ))
            session.commit()
            self.message_box.setText(
                f'Transação de R${self.input_value.text()} realizada!')
            self.message_box.show()
            self.close()


class ExtractModel(QtCore.QAbstractTableModel):

    def __init__(self, data, header):
        super().__init__()
        self._data = data
        self._header = header

    def data(self, index, role=QtCore.Qt.ItemDataRole.DisplayRole):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]

    def set_data(self, data):
        self._data = data

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Orientation.Horizontal and role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self._header[section]

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._data[0])


class VerExtrato(QtWidgets.QWidget):

    def __init__(self, account_name: str, parent: QtWidgets.QWidget) -> None:
        super().__init__()
        self.parent = parent
        self.account_name = account_name
        self.setFixedSize(350, 500)

        self.transactions_table = QtWidgets.QTableView()
        self.transactions_table.setModel(
            ExtractModel([['', '']], ['Valor', 'Data']))
        self.transactions_table.setColumnWidth(0, 200)
        self.transactions_table.setColumnWidth(1, 122)

        self.button = Button('Mostrar extrato')
        self.button.clicked.connect(self.show_extract)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.transactions_table)
        self.layout.addWidget(self.button)

    def show_extract(self) -> None:
        with Session() as session:
            account = session.query(Account).filter_by(
                client_name=get_current_client(session).name
            ).filter_by(name=self.account_name).first()
            if account:
                data = []
                for t in account.transactions:
                    data.append([f'R${t.value:.2f}'.replace('.', ','),
                                 datetime.strftime(t.date, '%d/%m/%Y')])
                self.transactions_table.model().set_data(
                    data if data else [['', '']])


class AddAccount(BaseWidget):

    def __init__(self):
        super().__init__()
        self.setFixedSize(250, 150)
        self.message_box = QtWidgets.QMessageBox()
        self.name_text = QtWidgets.QLabel('Nome')
        self.input_name = QtWidgets.QLineEdit()
        self.input_name_layout = HLayout(self.name_text, self.input_name)

        self.button = Button('Adicionar conta')
        self.button.clicked.connect(self.add_account)

        self.layout.addLayout(self.input_name_layout)
        self.layout.addWidget(self.button)

    @QtCore.Slot()
    def add_account(self):
        with Session() as session:
            client = get_current_client(session)
            client.accounts.append(Account(name=self.input_name.text()))
            session.commit()
        self.message_box.setText(f'Conta {self.input_name.text()} Adicionada')
        self.message_box.show()
        self.close()


class RemoverConta(QtWidgets.QDialog):

    def __init__(self, account_name: str, parent: QtWidgets.QWidget):
        super().__init__()
        self.parent = parent
        self.account_name = account_name
        self.button_boxes = QtWidgets.QDialogButtonBox.Yes | QtWidgets.QDialogButtonBox.No
        self.button_box = QtWidgets.QDialogButtonBox(self.button_boxes)
        self.button_box.accepted.connect(self.remove_account)
        self.button_box.rejected.connect(self.close)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(QtWidgets.QLabel('Quer mesmo remover a conta?'))
        self.layout.addWidget(self.button_box)

    @QtCore.Slot()
    def remove_account(self):
        with Session() as session:
            account = session.query(Account).filter_by(
                client_name=get_current_client(session).name
            ).filter_by(name=self.account_name).first()
            session.delete(account)
            session.commit()
        self.parent.message_box.setText(f'Conta {self.account_name} removida!')
        self.parent.message_box.show()
        self.parent.update_input_account_items()
        self.close()

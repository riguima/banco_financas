from PySide6 import QtWidgets, QtGui, QtCore

from database import Session
from domain import get_current_client
from models import Account, Client, Transaction
from components import ChooseAccount, HLayout


class AddMoney(ChooseAccount):

    def __init__(self):
        super().__init__()
        self.setFixedSize(250, 200)
        self.message_box = QtWidgets.QMessageBox()

        self.button.setText('Adicionar dinheiro')
        self.button.clicked.connect(self.add_money)

        self.value_text = QtWidgets.QLabel('Valor')
        self.input_value = QtWidgets.QLineEdit()
        self.input_value.setValidator(QtGui.QDoubleValidator())
        self.input_value_layout = HLayout(self.value_text, self.input_value)

        self.layout.addLayout(self.input_value_layout)

    @QtCore.Slot()
    def add_money(self):
        with Session() as session:
            account = session.query(Account).filter_by(
                client_name=get_current_client().name
            ).get(self.input_account.currentText())
            account.transactions.append(Transaction(
                value=float(self.input_value.text().replace(',', '.'))
            ))
            session.commit()
            self.message_box.setText(f'Transação de R${self.input_value.text()} realizada!')
            self.message_box.show()
            self.close()


class ExtractModel(QtCore.QAbstractTableModel):

    def __init__(self, data, header):
        super().__init__()
        self._data = data
        self._header = header

    def data(self, index, role=QtCore.Qt.ItemDataRole.DisplayRole):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self._data[index.row(), index.column()]

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Orientation.Horizontal and role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self._header[section]

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._data[0])


class Extract(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.input = QtWidgets.QLineEdit()
        self.transactions_table = QtWidgets.QTableView()
        self.transactions_table.setModel(ExtractModel([['teste']], ['Transacao']))

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.transactions_table)


class AddAccount(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.message_box = QtWidgets.QMessageBox()
        self.input = QtWidgets.QLineEdit()
        self.button = QtWidgets.QPushButton('Adicionar conta')
        self.button.clicked.connect(self.add_account)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.button)

    @QtCore.Slot()
    def add_account(self):
        with Session() as session:
            client = get_current_client()
            client.accounts.append(Account(name=self.input.text()))
            session.commit()
        self.message_box.setText(f'Conta {self.input.text()} Adicionada')
        self.message_box.show()


class RemoveAccount(ChooseAccount):

    def __init__(self):
        super().__init__()
        self.setFixedSize(250, 150)
        self.message_box = QtWidgets.QMessageBox()
        self.button.setText('Remover conta')
        self.button.clicked.connect(self.remove_account)

    @QtCore.Slot()
    def remove_account(self):
        with Session() as session:
            account = session.query(Account).filter_by(
                client_name=get_current_client().name
            ).get(self.input_account.currentText())
            session.delete(account)
            session.commit()
        self.message_box.setText(f'Conta {self.input_account.currentText()} Removida')
        self.message_box.show()
        self.close()

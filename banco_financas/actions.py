from PySide6 import QtWidgets, QtGui, QtCore
from datetime import datetime

from database import Session
from domain import get_current_client
from models import Account, Transaction
from components import ChooseAccount, HLayout, Button, BaseWidget


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
                client_name=get_current_client(session).name
            ).filter_by(name=self.input_account.currentText()).first()
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


class Extract(ChooseAccount):

    def __init__(self):
        super().__init__()
        self.setFixedSize(350, 500)
        self.transactions_table = QtWidgets.QTableView()
        self.transactions_table.setModel(ExtractModel([['', '']], ['Valor', 'Data']))
        self.transactions_table.setColumnWidth(0, 200)
        self.transactions_table.setColumnWidth(1, 122)
        self.button.setText('Mostrar extrato')
        self.button.clicked.connect(self.show_extract)

        self.layout.addWidget(self.transactions_table)

    def show_extract(self) -> None:
        with Session() as session:
            account = session.query(Account).filter_by(
                client_name=get_current_client(session).name
            ).filter_by(name=self.input_account.currentText()).first()
            if account:
                data = []
                for t in account.transactions:
                    data.append([f'R${t.value:.2f}'.replace('.', ','),
                                 datetime.strftime(t.date, '%d/%m/%Y')])
                self.transactions_table.model().set_data(data if data else [['', '']])


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
                client_name=get_current_client(session).name
            ).filter_by(name=self.input_account.currentText()).first()
            session.delete(account)
            session.commit()
        self.message_box.setText(f'Conta {self.input_account.currentText()} Removida')
        self.message_box.show()
        self.update_input_account_items()
        self.close()

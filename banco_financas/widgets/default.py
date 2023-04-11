from PySide6 import QtWidgets, QtGui, QtCore
from datetime import datetime

from repositories import AccountRepository
from helpers import HLayout, Button, BaseWidget


class AdicionarDinheiro(BaseWidget):

    def __init__(self, account_name: str, parent: QtWidgets.QWidget):
        super().__init__()
        self.parent = parent
        self.account_name = account_name
        self.setFixedSize(250, 150)
        self.message_box = QtWidgets.QMessageBox()

        self.value_text = QtWidgets.QLabel('Valor')
        self.input_value = QtWidgets.QLineEdit()
        self.input_value.setValidator(QtGui.QDoubleValidator())
        self.input_value_layout = HLayout(self.value_text, self.input_value)

        self.button = Button('Adicionar dinheiro')
        self.button.clicked.connect(self.add_money)

        self.layout.addLayout(self.input_value_layout)
        self.layout.addWidget(self.button)

    @QtCore.Slot()
    def add_money(self):
        AccountRepository().make_transaction(
            self.account_name,
            value=float(self.input_value.text().replace(',', '.')),
        )
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

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Orientation.Horizontal and role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self._header[section]

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._data[0])


class VerExtrato(BaseWidget):

    def __init__(self, account_name: str, parent: QtWidgets.QWidget) -> None:
        super().__init__()
        self.parent = parent
        self.account_name = account_name
        self.setFixedSize(380, 500)

        self.label_start_date = QtWidgets.QLabel('Data inicial')
        self.input_start_date = QtWidgets.QDateEdit()
        self.input_start_date.setDisplayFormat('dd/MM/yyyy')
        self.layout_start_date = HLayout(self.label_start_date,
                                         self.input_start_date)

        self.label_final_date = QtWidgets.QLabel('Data final')
        self.input_final_date = QtWidgets.QDateEdit()
        self.input_final_date.setDisplayFormat('dd/MM/yyyy')
        self.layout_final_date = HLayout(self.label_final_date,
                                         self.input_final_date)

        self.transactions_table = QtWidgets.QTableView()
        self.transactions_table.setModel(ExtractModel([['', '']],
                                                      ['Valor', 'Data']))
        self.transactions_table.setColumnWidth(0, 200)
        self.transactions_table.setColumnWidth(1, 152)

        self.button_show_extract = Button('Mostrar extrato')
        self.button_show_extract.clicked.connect(self.show_extract)

        self.layout.addLayout(self.layout_start_date)
        self.layout.addLayout(self.layout_final_date)
        self.layout.addWidget(self.transactions_table)
        self.layout.addWidget(self.button_show_extract)

    @QtCore.Slot()
    def show_extract(self) -> None:
        transactions = AccountRepository().get_transactions(
            self.account_name, self.input_start_date.date(),
            self.input_final_date.date()
        )
        data = []
        for t in transactions:
            data.append([f'R${t.value:.2f}'.replace('.', ','),
                         datetime.strftime(t.date, '%d/%m/%Y')])
        if not data:
            data = [['', '']]
        self.transactions_table.setModel(ExtractModel(data, ['Valor', 'Data']))


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
        AccountRepository().add(self.input_name.text())
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
        AccountRepository().delete(self.account_name)
        self.parent.message_box.setText(f'Conta {self.account_name} removida!')
        self.parent.message_box.show()
        self.parent.update_input_account_items()
        self.close()

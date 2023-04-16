from PySide6 import QtWidgets, QtCore

from helpers import ChooseAccount, Button
from widgets.default import AddAccount, RemoveTransaction


class MainWindow(QtWidgets.QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet('font-size: 20px')
        self.setFixedSize(250, 170)
        self.message_box = QtWidgets.QMessageBox()

        self.accounts = ChooseAccount()
        self.accounts_button = Button('Contas')
        self.accounts_button.clicked.connect(self.accounts.show)

        self.remove_transaction = RemoveTransaction()
        self.remove_transaction_button = Button('Remover transação')
        self.remove_transaction_button.clicked.connect(
            self.remove_transaction.show)

        self.add_account = AddAccount()
        self.add_account_button = Button('Adicionar conta')
        self.add_account_button.clicked.connect(self.add_account.show)

        self.finalize_transactions_button = Button('Finalizar transações')
        self.finalize_transactions_button.clicked.connect(
            self.finalize_transactions)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.accounts_button)
        self.layout.addWidget(self.add_account_button)
        self.layout.addWidget(self.remove_transaction_button)
        self.layout.addWidget(self.finalize_transactions_button)

    @QtCore.Slot()
    def finalize_transactions(self):
        self.message_box.setText('')
        self.message_box.show()
        self.close()

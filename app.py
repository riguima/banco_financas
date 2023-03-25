from PySide6 import QtWidgets, QtCore
from actions import AddMoney, AddAccount, RemoveAccount, Extract
import sys


class App(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.add_money = AddMoney()
        self.add_money_button = QtWidgets.QPushButton('Adicionar dinheiro')
        self.add_money_button.clicked.connect(self.add_money.show)

        self.extract = Extract()
        self.show_extract_button = QtWidgets.QPushButton('Ver extrato')
        self.show_extract_button.clicked.connect(self.extract.show)

        self.add_account = AddAccount()
        self.add_account_button = QtWidgets.QPushButton('Adicionar conta')
        self.add_account_button.clicked.connect(self.add_account.show)

        self.remove_account = RemoveAccount()
        self.remove_account_button = QtWidgets.QPushButton('Remover conta')
        self.remove_account_button.clicked.connect(self.remove_account.show)

        self.finalize_transactions_button = QtWidgets.QPushButton('Finalizar transações')
        self.finalize_transactions_button.clicked.connect(self.finalize_transactions)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.add_money_button)
        self.layout.addWidget(self.show_extract_button)
        self.layout.addWidget(self.add_account_button)
        self.layout.addWidget(self.remove_account_button)
        self.layout.addWidget(self.finalize_transactions_button)

    @QtCore.Slot()
    def finalize_transactions(self):
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    widget = App()
    widget.setFixedSize(300, 300)
    widget.show()
    sys.exit(app.exec())

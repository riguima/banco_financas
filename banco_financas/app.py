from PySide6 import QtWidgets, QtCore
from widgets.default import AddAccount
import sys

from helpers import Button, HLayout, ChooseAccount
from database import Session
from models import Client


class Main(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setStyleSheet('font-size: 20px')
        self.setFixedSize(250, 150)
        self.message_box = QtWidgets.QMessageBox()
        self.accounts = ChooseAccount()
        self.accounts_button = Button('Contas')
        self.accounts_button.clicked.connect(self.accounts.show)

        self.add_account = AddAccount()
        self.add_account_button = Button('Adicionar conta')
        self.add_account_button.clicked.connect(self.add_account.show)
        self.finalize_transactions_button = Button('Finalizar transações')
        self.finalize_transactions_button.clicked.connect(
            self.finalize_transactions)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.accounts_button)
        self.layout.addWidget(self.add_account_button)
        self.layout.addWidget(self.finalize_transactions_button)

    @QtCore.Slot()
    def finalize_transactions(self):
        self.message_box.setText('')
        self.message_box.show()
        self.close()


class Login(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setStyleSheet('font-size: 20px')
        self.setFixedSize(300, 250)
        self.main_window = Main()
        self.message_box = QtWidgets.QMessageBox()

        self.name_text = QtWidgets.QLabel('Usuário')
        self.input_name = QtWidgets.QLineEdit()
        self.input_name_layout = HLayout(self.name_text, self.input_name)

        self.password_text = QtWidgets.QLabel('Senha')
        self.input_password = QtWidgets.QLineEdit()
        self.input_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.input_password_layout = HLayout(self.password_text, self.input_password)

        self.login_button = Button('Login')
        self.login_button.clicked.connect(self.make_login)
        self.register_button = Button('Cadastrar')
        self.register_button.clicked.connect(self.register)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.contentsMargins().setBottom(0)
        self.layout.addLayout(self.input_name_layout)
        self.layout.addLayout(self.input_password_layout)
        self.layout.addWidget(self.login_button)
        self.layout.addWidget(self.register_button)

    @QtCore.Slot()
    def make_login(self):
        with Session() as session:
            client = session.query(Client).get(self.input_name.text())
            if client and client.password == self.input_password.text():
                self.show_main_window()
            else:
                self.message_box.setText('Usuário ou senha incorretos!')
                self.message_box.show()

    @QtCore.Slot()
    def register(self):
        with Session() as session:
            client = session.query(Client).get(self.input_name.text())
            if client:
                self.message_box.setText('Usuário já cadastrado!')
                self.message_box.show()
            else:
                client = Client(name=self.input_name.text(), password=self.input_password.text())
                session.add(client)
                session.commit()
                self.show_main_window()

    def show_main_window(self):
        with open('current_client.txt', 'w') as f:
            f.write(self.input_name.text())
        self.message_box.setText(f'Bem vindo {self.input_name.text()}!')
        self.message_box.show()
        self.close()
        self.main_window.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    widget = Login()
    widget.show()
    sys.exit(app.exec())

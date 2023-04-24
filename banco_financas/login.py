from PySide6 import QtWidgets, QtCore

from database import Session
from models import ClientModel
from domain import Client
from helpers import HLayout, Button
from main_window import MainWindow


class Login(QtWidgets.QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet('font-size: 20px')
        self.setFixedSize(300, 200)
        self.main_window = MainWindow()
        self.message_box = QtWidgets.QMessageBox()

        self.name_text = QtWidgets.QLabel('Usuário')
        self.input_name = QtWidgets.QLineEdit()
        self.input_name_layout = HLayout(self.name_text, self.input_name)

        self.password_text = QtWidgets.QLabel('Senha')
        self.input_password = QtWidgets.QLineEdit()
        self.input_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.input_password_layout = HLayout(self.password_text,
                                             self.input_password)

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
            client = session.query(ClientModel).get(self.input_name.text())
            if client and client.password == self.input_password.text():
                self.show_main_window()
            else:
                self.message_box.setText('Usuário ou senha incorretos!')
                self.message_box.show()

    @QtCore.Slot()
    def register(self):
        with Session() as session:
            client = session.query(ClientModel).get(self.input_name.text())
            if client:
                self.message_box.setText('Usuário já cadastrado!')
                self.message_box.show()
            else:
                client = ClientModel(name=self.input_name.text(),
                                password=self.input_password.text())
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

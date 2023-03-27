from PySide6 import QtWidgets

from database import Session
from domain import get_current_client


class Button(QtWidgets.QPushButton):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet('background-color: #187bcd; color: white')


class HLayout(QtWidgets.QHBoxLayout):

    def __init__(self, label, input):
        super().__init__()
        self.addWidget(label)
        self.addWidget(input)


class ChooseAccount(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setStyleSheet('font-size: 20px')
        self.account_text = QtWidgets.QLabel('Conta')
        self.input_account = QtWidgets.QComboBox()
        self.input_account.addItems([a.name for a in get_current_client().accounts])
        self.input_account_layout = HLayout(self.account_text, self.input_account)

        self.button = Button()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addLayout(self.input_account_layout)

    def show(self):
        super().show()
        self.layout.addWidget(self.button)

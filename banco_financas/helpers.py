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


class BaseWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setStyleSheet('font-size: 20px')
        self.back_button = Button('Voltar')
        self.back_button.clicked.connect(self.close)
        self.layout = QtWidgets.QVBoxLayout(self)

    def show(self):
        super().show()
        self.layout.addWidget(self.back_button)


class ChooseAccount(BaseWidget):

    def __init__(self):
        super().__init__()
        self.account_text = QtWidgets.QLabel('Conta')
        self.input_account = QtWidgets.QComboBox()
        self.input_account_layout = HLayout(self.account_text, self.input_account)

        self.button = Button()
        self.back_button = Button('Voltar')
        self.back_button.clicked.connect(self.close)

        self.layout.addLayout(self.input_account_layout)

    def update_input_account_items(self):
        self.input_account.clear()
        with Session() as session:
            self.input_account.addItems([a.name for a in get_current_client(session).accounts])

    def show(self):
        self.update_input_account_items()
        self.layout.addWidget(self.button)
        super().show()


def create_widget_button(text: str, widget: QtWidgets.QWidget):
    button = Button('Adicionar dinheiro')
    button.clicked.connect(widget.show)

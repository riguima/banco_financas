from PySide6 import QtWidgets, QtCore

from database import Session
from domain import get_current_client, get_action_widget


class Button(QtWidgets.QPushButton):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setStyleSheet('background-color: #187bcd; color: white')


class HLayout(QtWidgets.QHBoxLayout):

    def __init__(self, label: QtWidgets.QLabel,
                 line_edit: QtWidgets.QLineEdit) -> None:
        super().__init__()
        self.addWidget(label)
        self.addWidget(line_edit)


class BaseWidget(QtWidgets.QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet('font-size: 20px')
        self.back_button = Button('Voltar')
        self.back_button.clicked.connect(self.close)
        self.layout = QtWidgets.QVBoxLayout(self)

    def show(self) -> None:
        super().show()
        self.layout.addWidget(self.back_button)


class ChooseAccount(BaseWidget):

    def __init__(self) -> None:
        super().__init__()
        self.setFixedSize(300, 200)
        self.message_box = QtWidgets.QMessageBox()
        self.widget = None
        self.account_text = QtWidgets.QLabel('Conta')
        self.input_account = QtWidgets.QComboBox()
        self.input_account_layout = HLayout(self.account_text,
                                            self.input_account)

        self.action_text = QtWidgets.QLabel('Acão')
        self.input_action = QtWidgets.QComboBox()
        self.input_action.addItems(['Ver extrato', 'Adicionar dinheiro',
                                    'Remover conta'])
        self.input_action_layout = HLayout(self.action_text, self.input_action)

        self.action_button = Button('Fazer ação')
        self.action_button.clicked.connect(self.make_action)

        self.layout.addLayout(self.input_account_layout)
        self.layout.addLayout(self.input_action_layout)
        self.layout.addWidget(self.action_button)

    def update_input_account_items(self) -> None:
        self.input_account.clear()
        with Session() as session:
            self.input_account.addItems(
                [a.name for a in get_current_client(session).accounts])

    def show(self) -> None:
        self.update_input_account_items()
        super().show()

    @QtCore.Slot()
    def make_action(self) -> None:
        self.widget = get_action_widget(
            self.input_account.currentText(), self.input_action.currentText(),
            self
        )
        self.widget.show()

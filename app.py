from PySide6 import QtWidgets, QtCore
import sys


class App(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.adicionar_dinheiro_botao = QtWidgets.QPushButton('Adicionar dinheiro')
        self.ver_extrato_botao = QtWidgets.QPushButton('Ver extrato')
        self.adicionar_conta_botao = QtWidgets.QPushButton('Adicionar conta')
        self.remover_conta_botao = QtWidgets.QPushButton('Remover conta')
        self.finalizar_transacoes_botao = QtWidgets.QPushButton('Finalizar transações')

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.adicionar_dinheiro_botao)
        self.layout.addWidget(self.ver_extrato_botao)
        self.layout.addWidget(self.adicionar_conta_botao)
        self.layout.addWidget(self.remover_conta_botao)
        self.layout.addWidget(self.finalizar_transacoes_botao)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    widget = App()
    widget.setFixedSize(300, 300)
    widget.show()
    sys.exit(app.exec())

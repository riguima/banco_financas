from banco_dedados import Conta, Session
from contas import ContaPadrao
from utils import mostrar_menu


class Caixa(ContaPadrao):

    def escolher_fonte_renda(self, conta):
        opcoes = ['Salario', 'Investimentos', 'Outros']
        fonte_de_renda = mostrar_menu('Fonte de renda', opcoes, 'Escolha a fonte de renda: ')
        with Session() as session:
            conta_model = session.query(Conta).filter_by(conta=conta).first()
            conta_model.fonte_de_renda = fonte_de_renda

    def adicionar_dinheiro(self, conta):
        self.escolher_fonte_renda(conta)
        super().adicionar_dinheiro(conta)

class Investimentos(ContaPadrao):

    def adicionar_dinheiro(self, conta):
        super().adicionar_dinheiro(conta)



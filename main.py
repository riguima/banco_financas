import locale
from banco_dedados import Conta, Session
from utils import mostrar_menu, limpar_tela
import sys
import os
import inspect
import contas
import classes

locale.setlocale(locale.LC_ALL, 'pt_BR.utf-8')


def obter_classe(nome):
    modulo = sys.modules['classes']
    for nome_classe, obj in inspect.getmembers(modulo):
        if inspect.isclass(obj) and nome_classe == nome:
            return obj()
    return contas.ContaPadrao()


saved = False


def main():
    global saved
    limpar_tela()
    with Session() as session:
        contas = [c.conta for c in session.query(Conta).all()]
    opcoes = ['Adicionar dinheiro', 'Ver extrato', 'Adicionar conta', 'Remover conta', 'Finalizar transaçoes']
    opcao = mostrar_menu('Menu Principal', opcoes, 'Escolha uma opçao: ')
    limpar_tela()
    if opcao == 'Adicionar dinheiro':
        opcao = mostrar_menu('Adicionar dinheiro', [*contas, 'Voltar ao menu anterior'], 'Escolha uma conta: ')
        if opcao != 'Voltar ao menu anterior':
            saved = True
            classe = obter_classe(opcao)
            classe.adicionar_dinheiro(opcao)
    elif opcao == 'Ver extrato':
        opcao = mostrar_menu('Ver extrato', [*contas, 'Voltar ao menu anterior'], 'Escolha uma conta: ')
        if opcao != 'Voltar ao menu anterior':
            classe = obter_classe(opcao)
            conta = classe.obter_conta(opcao, conexao)
            period = mostrar_menu('Ver extrato',
                                  ['Últimas 5 transações', 'Buscar por período', 'Voltar ao menu anterior'],
                                  'Escolha uma opção: ')
            if period == 'Últimas 5 transações':
                conta.ver_extrato_ultimas_transacoes()
            elif period == 'Buscar por período':
                inicio = input('Digite a data de início (DD/MM/AAAA): ')
                fim = input('Digite a data de fim (DD/MM/AAAA): ')
                conta.ver_extrato_por_periodo(inicio, fim)
    elif opcao == 'Adicionar conta':
        while True:
            conta = input('Digite o nome da conta (ou pressione enter para voltar): ')
            if not conta:
                break
            if len(conta) < 3:
                print('O nome da conta deve ter pelo menos 3 caracteres.')
                continue
            if conta in contas:
                print('Essa conta já existe. Por favor, digite outro nome.')
                continue
            contas.append(conta)
            print(f'Conta "{conta}" adicionada com sucesso!')
            break
        else:
            print('Voltando para o menu principal...')
    elif opcao == 'Remover conta':
        opcao = mostrar_menu('Remover conta', [*contas, 'Voltar ao menu anterior'], 'Escolha uma conta: ')
        if opcao != 'Voltar ao menu anterior':
            with Session() as session:
                conta = session.query(Conta).filter_by(conta=opcao).first()
                session.delete(conta)
                session.commit()
    elif opcao == 'Finalizar transaçoes':
        input("Transação concluída." if saved else "Finalização concluída. Não houve nenhum saldo nas contas: ")
        exit()
    else:
        input("Opção inválida, digite novamente: ")
    main()


if __name__ == "__main__":
    main()
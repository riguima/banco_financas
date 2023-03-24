import pandas as pd
import datetime
import locale
from banco_dedados import Session, Conta, Transacao
import re
from prettytable import PrettyTable
from extrato import get_transacoes_cached

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def format_transacao(transacao):
    transacao["data"] = pd.to_datetime(transacao["data"]).strftime('%d/%m/%Y %H:%M')
    transacao["valor"] = locale.currency(float(transacao["valor"]), grouping=True)
    return transacao


class ContaPadrao:

    def adicionar_dinheiro(self, conta):
        while True:
            valor = input("Digite o valor a ser adicionado (use vírgula para separar os centavos): ")
            if '.' in valor and ',' not in valor:
                # Valor com ponto e sem vírgula, adiciona vírgula após o último número inteiro
                regex = r'(?P<int>\d{1,3})(?P<thousands>\.\d{3})*\.(?P<decimal>\d{2})$'
                match = re.match(regex, valor.strip())
                if match:
                    groups = match.groupdict()
                    int_part = groups.get('int', '').replace('.', '')
                    decimal_part = groups.get('decimal', '')
                    valor = f'{int_part},{decimal_part}'
            elif ',' in valor and '.' not in valor:
                # Valor com vírgula e sem ponto, adiciona ".00" se houver apenas um dígito após a vírgula
                regex = r'^\d+,\d{1}$'
                match = re.match(regex, valor.strip())
                if match:
                    valor = valor.strip().replace(',', ',00')
            valor = valor.replace(".", "").replace(",", ".")
            try:
                valor = float(valor)
                if valor <= 0:
                    raise ValueError
                break
            except ValueError:
                print("Valor inválido, digite novamente.")
        # Consulta a conta na sessão
        with Session() as session:
            conta_banco = session.query(Conta).filter_by(conta=conta).first()
            # Atualiza o saldo na conta
            conta_banco.saldo += valor
            # Cria objeto Transacao
            transacao = Transacao(data=datetime.datetime.now(), valor=valor, conta=conta)
            # Adiciona objeto à sessão
            session.add(transacao)
            # Confirma a sessão para inserir o objeto na tabela
            print(f"{locale.currency(valor, grouping=True)} adicionados na conta '{conta}'")
            session.commit()

    def ver_extrato(self, conta):
        data_atual = datetime.datetime.now()
        data_limite = data_atual - datetime.timedelta(days=30)
        transacoes = get_transacoes_cached(conta, self.conn)
        transacoes_filtradas = [t for t in transacoes if t['data'] >= data_limite]
        transacoes_filtradas = sorted(transacoes_filtradas, key=lambda t: t['data'], reverse=True)
        extrato = PrettyTable(['Data', 'Valor'])
        extrato.align['Data'] = 'l'
        for t in transacoes_filtradas[:5]:
            extrato.add_row([t['data'], locale.currency(t['valor'], grouping=True)])
        print(extrato)
        print('1) Buscar por período')
        print('2) Sair')
        opcao = input('Escolha uma opção: ')
        if opcao == '1':
            data_inicio = input('Digite a data de início no formato dd/mm/aaaa: ')
            data_fim = input('Digite a data de fim no formato dd/mm/aaaa: ')
            data_inicio = datetime.datetime.strptime(data_inicio, '%d/%m/%Y')
            data_fim = datetime.datetime.strptime(data_fim, '%d/%m/%Y') + datetime.timedelta(days=1)
            transacoes_filtradas = [t for t in transacoes if data_inicio <= t['data'] <= data_fim]
            transacoes_filtradas = sorted(transacoes_filtradas, key=lambda t: t['data'], reverse=True)
            extrato = PrettyTable(['Data', 'Valor'])
            extrato.align['Data'] = 'l'
            for t in transacoes_filtradas:
                extrato.add_row([t['data'], locale.currency(t['valor'], grouping=True)])
            print(extrato)
        elif opcao == '2':
            return
        else:
            input('Opção inválida, pressione Enter para continuar.')
        # Cria a tabela prettytable e adiciona as linhas com as transações
        table = PrettyTable()
        table.field_names = ["DATA", "CONTA", "VALOR"]
        for i, transacao in df_conta.iterrows():
            data_formatada = transacao["data"]
            conta_formatada = transacao["conta"]
            valor_formatado = transacao["valor"]
            table.add_row([data_formatada, conta_formatada, valor_formatado])
        print(f"\nExtrato da conta '{conta}':")
        print(table)
        with Session() as session:
            conta_model = session.query(Conta).filter_by(conta=conta).first()
            input(f'O saldo total de R${conta_model.saldo:.2f}: '.replace('.', ','))

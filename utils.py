import os


def mostrar_menu(titulo, opcoes, mensagem):
    print(titulo)
    for e, opcao in enumerate(opcoes):
        print(f'{e + 1}. {opcao}')
    opcao = input(mensagem)
    if not opcao.isdigit():
        mostrar_menu(titulo, opcoes, 'Digite apenas numeros: ')
    elif int(opcao) - 1 not in range(len(opcoes)):
        mostrar_menu(titulo, opcoes, f'Digite um numero de 1 a {len(opcoes)}')
    return opcoes[int(opcao) - 1]


def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')
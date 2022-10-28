from pickletools import opcodes
import os
import menu
import time
import tela 
from vendas import historico
nome = ''
#---------------------- Impressões de formatação detexto--------------------------------------------#

print_catalogo_vazio = """
	|--------------------------------------------------------------------------------------------------|
	|                                  Seja bem vindo ao Organico’s !!!                                |
	|                       ----------------------------------------------------                       |
	|         Para imprimir o relátorio, o usuário precisa cadastrar uma venda.                        |
	|         Não existe vendas cadastradas.                                                           |
	|                                                                                                  |
	|--------------------------------------------------------------------------------------------------|
	"""

relat = f'''
    |--------------------------------------------------------------------------------------------------|
    |                                  Vendas feita no dia.                                            |
    |                                                                                                  |
    |--------------------------------------------------------------------------------------------------|
    |         Produtos                                                     Preço                       |
    |                                                                                                  |'''

fim = """
    |--------------------------------------------------------------------------------------------------|
                """


def Relatorio(user):
    nome = user

    #--------------------------------Função para gerar relatorios---------------------------#
    if len(historico) <=0:
        print(print_catalogo_vazio)
        time.sleep(3)
        menu.menu_funcs()
    else:
        print(historico)
        tela.LimparTela()
        print(relat, end='')
        for i in range(len(historico)):
            print(f"""
    |         {str(historico[i][0]):<20s}.  .  .  .  .  .  .  .  .  .  .  .  .  . R$: {str(historico[i][1]):<6s}                  |""", end=''
            )
        
        total = 0
        for i in range(len(historico)):
            total += float(historico[i][1])
        
        maior = 0
        for i in range(len(historico)):
            if float(maior) < float(historico[i][1]):
                maior = float(historico[i][1])
        
        menor = 999999999999
        for i in range(len(historico)):
            if float(menor) > float(historico[i][1]):
                menor = float(historico[i][1])
        print(f"""
    |--------------------------------------------------------------------------------------------------|
    |             Total de vendas | Item com maior valor | Item com menor valor | Ticket médio         | 
                  R$: {total:.2f}        R$: {maior:.2f}              R$: {menor:.2f}              R$: {total / len(historico):.2f}            """, end=''
            )
        print(fim)
        sair(historico, nome)

def sair(vendas, nome):
    print("\nPara Sair aperte 'S': ")
    qt = '1'
    while qt != 'S':
        qt = input("Tecla: ").upper()
        if qt == 'S':
            menu.menu_funcs(vendas)
        else:
            print('Opção invalida!!')
            tela.LimparTela()
            Relatorio(vendas, nome)

#--------------Final da opção 1---------------------------------------------------#

    #relatorio()
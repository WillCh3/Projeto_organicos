import os
import time
import cadastro
import vendas
import relatorio
import tela 
from cadastro import catalogo
from vendas import carrinho


#---------------------------------------Menu inicial---------------------------------------------------#
print_catalogo_vazio = """
	|--------------------------------------------------------------------------------------------------|
	|                                  Seja bem vindo ao Organico’s !!!                                |
	|                       ----------------------------------------------------                       |
	|         Para fazer uma venda ou deletar, o usuário precisa cadastrar um item ao catálogo.        |
	|         Não existe produtos cadastrados.                                                         |
	|                                                                                                  |
	|--------------------------------------------------------------------------------------------------|
	"""


print_boasvindas = """
	|--------------------------------------------------------------------------------------------------|
	|                                                                                                  |
	|                                  Seja bem vindo ao Organico’s !!!                                |
	|                       ----------------------------------------------------                       |
	|                                                                                                  |
	|--------------------------------------------------------------------------------------------------|
	"""

print_menu = """
	|--------------------------------------------------------------------------------------------------|
	|             Selecione o menu apertando as teclas sugeridas                                       |
	|                                                                                                  |
	|                       1 - Cadastro                                                               |
	|                       2 - Vendas                                                                 |
	|                       3 - Relatórios                                                             |
	|                       S - Sair                                                                   |
	|--------------------------------------------------------------------------------------------------|
	"""
# Catalogo teste
user = ''

def Menu_inicial():
	id = 0 
	global user
	tela.LimparTela()
	while user.isdigit() or len(user) < 3:
		tela.LimparTela()
		print(print_boasvindas)
		if id == 1:
			print('\tPor favor, Digite um nome de usuário Valido!!!')
		user = input("\tDigite seu nome: ")
		id =1
		#print('Por favor, Digite um nome de usuário Valido!!!')

	menu_funcs()


def menu_funcs(itens = []):
	carrinho = itens
	tela.LimparTela()
	print(print_menu)

	first_choice = 0
	while first_choice != 'S':
		first_choice= input ('\tTecla: ')

		if first_choice.upper() == "S":
			tela.LimparTela()
			print(f"{user}, agradeço sua companhia e espero que tenha ajudado.")
			exit()

		elif first_choice == "1":
			tela.LimparTela()
			cadastro.cad_menu()
			

		elif first_choice == "2":
			tela.LimparTela()
			Menu_vendas()

		elif first_choice == "3":
			tela.LimparTela()
			Menu_relatorio()
			
		elif first_choice == "4":
			tela.LimparTela()
			cadastro.deletar_item_catalago()

		else:
			tela.LimparTela()
			print(print_menu)
			print('\tPor favor, aperte uma das teclas sugeridas!!!')

	

#----------------------------------------- Menu Vendas -----------------------------------------#

print_menu_car ='''
    |--------------------------------------------------------------------------------------------------|
    |                                    Escolha uma função                                            |
    |--------------------------------------------------------------------------------------------------|
    |        Adicionar item - 1      Deletar item - 2       checkout  -3          Sair - 'S'           |
    |--------------------------------------------------------------------------------------------------|'''


def Menu_vendas():
	print(print_menu_car)
	func = input('\tEscolha uma Função: ')
	if len(catalogo) == 0:
		tela.LimparTela()
		print(print_catalogo_vazio)
		time.sleep(5)
		menu_funcs()
	else:
		if func == '1':
			vendas.Vendas()

		elif func == '2':
			vendas.Deletar()
		
		elif func == '3':
			vendas.finalizarVenda()
		
		elif func == 's':
			menu_funcs()


#----------------------------------------- Menu Reltorios -----------------------------------------#

menu_relatorio = """
    |--------------------------------------------------------------------------------------------------|
    |             Selecione uma função apertando as teclas sugeridas                                   |
    |                                                                                                  |
    |             Imprimir relátorio        - 1                                                        |
    |             Para sair                 - S                                                        |
    |--------------------------------------------------------------------------------------------------|
    """
def Menu_relatorio():
	tela.LimparTela()
	print(menu_relatorio)
	func = input('\tEscolha uma Função: ')
	if func == '1':
		relatorio.Relatorio(user)

	if func == 'S':
		print('Saindo!!!')
		menu_funcs()
		

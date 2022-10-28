import os
import time
import menu
import tela 
from cadastro import catalogo
from registro import Historico_vendas
import pandas as pd

print_addCar = """
    |----------------------------|
    |     Itens no carrinh       |
    |----------------------------|
"""
print_carr ='''
    |--------------------------------------------------------------------------------------------------|
    |                                    Total de produtos comprados                                   |
    |--------------------------------------------------------------------------------------------------|
    |         Produtos                                                     Preço                       |
    |                                                                                                  |'''

print_prod ='''
    |--------------------------------------------------------------------------------------------------|
    |                                      Produtos cadastrados                                        |
    |--------------------------------------------------------------------------------------------------|
    |       Id             Produtos                                                   Preço            |
    |                                                                                                  |'''

print_fim =  """
    |--------------------------------------------------------------------------------------------------|
"""
#Variaveis--------------
carrinho = []
total = 0
historico = []
Historico_vendas.carregar(historico)

def Print_catalogo():
    tela.LimparTela()
    print(print_prod, end='')
    for i, produto in  enumerate(catalogo):
        print(f"""
    |        {i}    .   .    {produto:<20s}.  .  .  .  .  .  .  .  .  .  .  .  .  R$: {str(catalogo[produto]):<6s}       |""", end=''
        )
    print(print_fim)     

def Vendas():
    fecha = "S"
    lista_de_venda = [] # mudança para nome de item por indice no carrinho de vendas

    for item in catalogo: # mudança para nome de item por indice no carrinho de vendas
        lista_de_venda.append(item) # mudança para nome de item por indice no carrinho de vendas
    
    while fecha != "N":
        tela.LimparTela()
        Print_catalogo()
        itemadd = input("por favor digite o ID do produto a ser adicionado ou a tecla 'S' para sair: ")
        if itemadd.upper()== "S":
            fecha= "N"
            menu.menu_funcs(carrinho)
     
        while not itemadd.isdigit() or  int(itemadd) > len(lista_de_venda) - 1 : #verifica se o produto está cadastrado. # mudança para nome de item por indice no carrinho de vendas
            
            tela.LimparTela()
            Print_catalogo()
            print("produto não cadastrado")
            itemadd = (input("por favor digite o código do produto a ser adicionado: "))

        print(len(lista_de_venda))
        carrinho.append([lista_de_venda[(int(itemadd))], catalogo[(lista_de_venda[int(itemadd)])]]) # mudança para nome de item por indice no carrinho de vendas
            #valorCarrinho.append(catalogo[itemadd])
        print(print_addCar, end='')
        for i in range(len(carrinho)):
            print(f"""
        Item: {carrinho[i][0]}       """,end='')
        
        total = 0
        for i in range(len(carrinho)):
            total += carrinho[i][1]
        print(f"""
        \n        Total        R$: {total:.2f}""", end=''
    )
            
        fecha = str(input("\n\ndeseja adicionar mais intens? (S/N): ")).upper()
        #return carrinho
    tela.LimparTela()
    Historico_vendas.exportar(historico)
    menu.Menu_vendas()
    

def Deletar():
    tela.LimparTela()
    print(print_addCar, end='')
    for i in range(len(carrinho)):
        print(f"""
    {i} . . {carrinho[i][0]}       """,end='')
        
    total = 0
    for i in range(len(carrinho)):
        total += carrinho[i][1]
    print(f"""
        \n    Total        R$: {total:.2f}"""
    )
#------------------------------------------------------------------------------------#
    print('\n')
    itemDelete = input("\tFavor informe o ID deseja deletar ou a tecla 'S' para sair: ")

    if itemDelete.lower() == 's':
        menu.Menu_vendas()
    else:
        while int(itemDelete) > len(carrinho) :
            print("produto não encontrado no carrinho ") #verifica se o item está no carrinho
            itemDelete = input("\tFavor informe qual ID deseja deletar ou a tecla 'S' para sair 123: ")
            if itemDelete.lower() == 's':
                menu.Menu_vendas()
        carrinho.pop(int(itemDelete))

        for i in range(len(carrinho)):
                print(f"""
            Item: {carrinho[i][0]}       """,end='')
            
        total = 0

        for i in range(len(carrinho)):
            total += carrinho[i][1]
        print(f"""
            \n        Total        R$: {total:.2f}""", end='')
        print(f'''
        \nitem Deletado com sucesso!!!
        Voltando ao menu anterior
        ''')
        
        time.sleep(3)
        Historico_vendas.exportar(historico)
        menu.menu_funcs(carrinho)
        

def finalizarVenda():
    tela.LimparTela()
    total = 0

    for i in range(len(carrinho)):
            total += carrinho[i][1]
            historico.append(carrinho[i]) # adicionei aqui o carrinho, pois la em baixo estava adicionando itens vazios

    print(f'''
    Venda Finalizada com sucesso!

    Seu Total a pagar é de R$: {total:.2f} '''"\n"
    )

    print("Voltando ao menu anterior")
    
    #historico.append(carrinho)  #################################
    carrinho.clear()   # mudei para clear para nao gerar item vazio
    
    time.sleep(5)
    Historico_vendas.exportar(historico)
    menu.menu_funcs(historico)
    







    


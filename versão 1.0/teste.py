catalogo = {}
produto = ''
valor = ''


def cadastro():
    produto = input('\tNome do Produto: ')
    while produto != 'S':
        produto = input('\tNome do Produto: ')

        if produto.upper() == 'S':
            print('\tVoltando ao menu principal')
            break
        elif produto.isalpha() == False or len(produto) <= 2 :
            print('Entrada Inválida')
            cadastro()

        else:
            while type(valor) != float:
                valor = input(f'\tQual o valor de {produto}: ')
                if valor.upper() == 'S':
                    print('\tVoltando ao menu principal')
                    
                elif valor.replace(".", "", 1).isdigit() == False:
                    print('\tEntrada Inválida')

                else:
                    valor = round(float(valor),2)
                    catalogo[(produto.lower()).capitalize()] = valor

cadastro()
    
print (catalogo)

import json
import csv


class Catalogo:
    @staticmethod
    def carregar():
        with open('catalogo.json', encoding='utf-8') as openfile:
            catalogo = json.load(openfile)
        return catalogo

    def exportar(dict):

        catalogo_txt = json.dumps(dict, indent=4)
        with open('catalogo.json', 'w') as df:
            df.write(catalogo_txt)

class Historico_vendas:
    @staticmethod
    def carregar(array):
        with open('historico_de_vendas.csv', encoding='utf-8') as arquivo_referencia:

            historico = csv.reader(arquivo_referencia, delimiter=',')
            for i in historico:
                array.append(i)
        return array

    def exportar(array):

        with open('historico_de_vendas.csv', 'w', newline='') as csvfile:

            for i in array:

                csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL,delimiter=',')

                csvwriter.writerow(i)
       

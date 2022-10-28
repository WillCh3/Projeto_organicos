from flask import Flask, redirect, render_template, request, url_for
from flask.helpers import flash
import pandas as pd
import time
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'super secret'
catalogo = pd.read_csv('catalogo.csv', index_col='produtos')
itens_deletados = pd.read_csv('itens_deletados.csv', index_col='produtos')
cart = pd.read_csv('cart.csv', sep=',', index_col='Produto')
total = 0


@app.route('/') 
def home():
    return redirect('/hortifruti/1')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html', catalogo = catalogo)

@app.route('/cadastro/<string:nome_produto>')
def editar(nome_produto):
    nome_produto = nome_produto.replace('_', ' ')
    return render_template('editar.html',
                                nome_produto = nome_produto,
                                valor = catalogo.loc[nome_produto]['valor'],
                                quantidade = catalogo.loc[nome_produto]['quantidade']
                                )


@app.route('/alteracoes_produto')
def altera_item():
    argumentos = request.args.to_dict()

    antigo_nome = argumentos['antigo_nome']
    novo_nome = argumentos["novo_nome"]
    quantidade = argumentos["quantidade"]
    preco = argumentos["preco"]

    catalogo.loc[antigo_nome, 'quantidade'] = quantidade
    catalogo.loc[antigo_nome, 'valor'] = preco
    catalogo.rename(index={antigo_nome: novo_nome}, inplace=True)
    catalogo.to_csv('catalogo.csv')
    time.sleep(2)
    flash('Produto alterado com sucesso !', 'alert alert-success')
    return redirect('/cadastro')

@app.route('/deletar_produto/<string:nome_produto>')
def deletar(nome_produto):

    quantidade = catalogo.loc[nome_produto, 'quantidade']
    preco = catalogo.loc[nome_produto, 'valor']
    itens_deletados.loc[nome_produto] = [quantidade, preco]

    catalogo.drop(nome_produto, inplace=True)

    itens_deletados.to_csv('itens_deletados.csv')
    catalogo.to_csv('catalogo.csv')
    flash(f'Produto {nome_produto} Zerado no Estoque !', 'alert delete-sucess')
    return redirect('/cadastro')

@app.route('/cadastro_filtro_preco_crescente')
def filtro_pcrescente():
    return render_template('cadastro.html', catalogo = catalogo.sort_values(by=['valor']))

@app.route('/cadastro_filtro_preco_decrescente')
def filtro_pdecrescente():
    return render_template('cadastro.html', catalogo = catalogo.sort_values(by=['valor'], ascending=False))

@app.route('/cadastro_filtro_quantidade_decrescente')
def filtro_qcrescente():
    return render_template('cadastro.html', catalogo = catalogo.sort_values(by=['quantidade'], ascending=False))

@app.route('/cadastro_filtro_quantidade_crescente')
def filtro_qdecrescente():
    return render_template('cadastro.html', catalogo = catalogo.sort_values(by=['quantidade']))

@app.route('/cadastro_filtro_alfabetico')
def filtro_alfabetico():
    return render_template('cadastro.html', catalogo = catalogo.sort_index())

@app.route('/cadastro_pesquisa')
def pesquisa():
    argumentos = request.args.to_dict()
    mascara = catalogo[catalogo.index.str.contains(argumentos['pesquisa'])]
    return render_template('cadastro.html',catalogo = mascara)
   
   
@app.route('/recuperacao')
def recove():
    return render_template('recuperacao_prod.html',itens_deletados = itens_deletados)

@app.route('/recuperacao_pesquisa')
def pesquisa_recover():
    argumentos = request.args.to_dict()
    mascara = itens_deletados[itens_deletados.index.str.contains(argumentos['pesquisa'])]
    return render_template('recuperacao_prod.html',itens_deletados = mascara)

@app.route('/recuper_para_cad/<id>')
def restauracao(id):

    quantidade = itens_deletados.loc[id, 'quantidade']
    preco = itens_deletados.loc[id, 'valor']

    catalogo.loc[id] = [quantidade, preco]

    itens_deletados.drop(id, inplace=True)

    itens_deletados.to_csv('itens_deletados.csv')
    catalogo.to_csv('catalogo.csv')

    flash(f'Produto {id} Recuperado com sucesso !', 'alert alert-success')
    return redirect(request.referrer)


# rotas divino 

@app.route('/listar')
def listar():
    argumento = request.args.to_dict()
    produto = argumento['produto']
    preco = argumento['preco']
    quantidade = argumento['quantidade']
    catalogo.loc[produto]=[quantidade, preco]
    catalogo.to_csv('catalogo.csv')
    flash(f'{produto} adicionado com sucesso !', 'alert alert-success')
    return redirect('/cadastro')

#rotas Lucas Henrique
@app.route('/hortifruti/<pag>')
def vitrine(pag):
    pag=int(pag)
    catalogo_pag = catalogo.iloc[12*(pag-1):12*pag]

    for index, row in cart.iterrows():
            cart.loc[index, "total"] = float(row["valor"]) * float(row["Quantidade"])
    
    total = cart["total"].astype(float).sum()

    if pag < 1:
        return redirect('/hortifruti/1')
    elif len(catalogo_pag) == 0:
        return redirect(request.referrer)

    return render_template('hortifruti.html',   catalogo = catalogo_pag, 
                                                pag=pag, 
                                                total = total)

@app.route('/produto_adicionado/<produtos>/<valor>')
def teste(produtos , valor):

    if produtos in cart.index.values:
        cart.loc[produtos,"Quantidade"] = float(cart.loc[produtos,"Quantidade"]) + 1 
    else:
        cart.loc[produtos] =  [valor, 1, 0]

    cart.to_csv('cart.csv')

    flash(f'{produtos} adicionado !', 'alert alert-success')     

    return redirect(request.referrer)

@app.route('/produto_excluido/<produtos>')
def excluir(produtos):
    cart.drop(produtos, inplace = True)
    cart.to_csv('cart.csv')
    flash(f'{produtos} Removido !', 'alert delete-sucess')
    return redirect('/finalizar')
  
@app.route('/finalizar')
def finalizar():
    argumentos = request.args.to_dict()
    
    if len(argumentos) == 0:
        for index, row in cart.iterrows():
            cart.loc[index, "total"] = float(row["valor"]) * float(row["Quantidade"])      
    else: 
        for key in argumentos:
            cart.loc[key,"Quantidade"] = argumentos[key]
            cart.loc[key, "total"] = float(argumentos[key]) * float(cart.loc[key,"valor"])

    total = cart["total"].astype(float).sum()

    return render_template('Checkout.html' ,    cart =cart, 
                                                total = total)

@app.route('/obrigado')
def historico():
    df_historico = pd.read_csv('cart.csv', sep=',', index_col='Produto')
    df_historico['data']= datetime.today()
    df_sales =pd.read_csv('sales.csv',  sep=',', index_col='Produto')
    result = [df_historico, df_sales]

    for index,row in cart.iterrows():
        catalogo.loc[index, 'quantidade'] = catalogo.loc[index, 'quantidade'] - int(row['Quantidade'])
        if catalogo.loc[index, 'quantidade'] <= 0:
            deletar(index)
        
  
    df_result =pd.concat(result)
    df_result.to_csv('sales.csv')
    indexes = cart['Quantidade'].astype(int) > 0
    cart.drop(cart[indexes].index, axis = 0, inplace = True)
    cart.to_csv('cart.csv')

    flash('Obrigado pela preferência !', 'alert alert-success' )
    return home()

@app.route('/hortifruti_pesquisa')
def hortifruti_pesquisa():
    argumentos = request.args.to_dict()
    mascara = catalogo[catalogo.index.str.contains(argumentos['pesquisa'])]

    for index, row in cart.iterrows():
            cart.loc[index, "total"] = float(row["valor"]) * float(row["Quantidade"])
    
    total = cart["total"].astype(float).sum()

    if len(mascara) == 0:
        return render_template('pesquisa_null.html')

    return render_template('hortifruti.html',   catalogo = mascara, 
                                                pag=1, 
                                                total = total)
    
#filtro vendas
@app.route('/vendas_filtro_preco_crescente')
def vendas_filtro_pcrescente():
    global catalogo
    catalogo = catalogo.sort_values(by=['valor'])
    return vitrine(1)

@app.route('/vendas_filtro_preco_decrescente')
def vendas_filtro_pdecrescente():
    global catalogo
    catalogo = catalogo.sort_values(by=['valor'], ascending=False)
    return vitrine(1)

@app.route('/vendas_filtro_quantidade_decrescente')
def vendas_filtro_qcrescente():
    global catalogo
    catalogo = catalogo.sort_values(by=['quantidade'], ascending=False)
    return vitrine(1)

@app.route('/vendas_filtro_quantidade_crescente')
def vendas_filtro_qdecrescente():
    global catalogo
    catalogo = catalogo.sort_values(by=['quantidade'])
    return vitrine(1)

@app.route('/vendas_filtro_alfabetico')
def vendas_filtro_alfabetico():
    global catalogo
    catalogo = catalogo.sort_index()
    return vitrine(1)


relat = pd.read_csv('./sales.csv')
df = pd.DataFrame(relat)
df_relat = pd.DataFrame(catalogo)

@app.route('/relatorio')
def relatorio():
    mais_prod = df_relat.nlargest(3, 'quantidade')
    menos_prod = df_relat.nsmallest(3, 'quantidade')

    mais_vend = df.groupby('Produto').sum().nlargest(5, 'Quantidade').round()
    menos_vend = df.groupby('Produto').sum().nsmallest(5, 'Quantidade').round()

    print(menos_vend)
    total_vendas = df['valor'].sum()
    ticke_medio = total_vendas / len(df)
    return render_template('relatorio.html', 
                                df= df, 
                                mais_vend= mais_vend, 
                                menos_vend= menos_vend, 
                                ticke_medio= ticke_medio, 
                                total_vendas=total_vendas,
                                mais_prod= mais_prod,
                                menos_prod= menos_prod)


if __name__ == "__main__":
    app.run(debug=True)






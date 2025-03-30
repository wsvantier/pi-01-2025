from flask import Flask, url_for, render_template, request, redirect, jsonify
import pymysql
from datetime import datetime, date

hoje = date.today()

app = Flask(__name__)

# Função para conectar ao banco de dados MariaDB
def mariadb(query):
    con = pymysql.connect(
        host='192.168.1.100',
        user='willian',
        password='22101998',
        database='pi',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    with con.cursor() as c:
        c.execute(query)
        saida = c.fetchall()
    
    con.commit()
    con.close()
    return saida

# Rota para página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para exibição do estoque
@app.route('/estoque')
def estoque():
    return render_template('estoque.html', hoje=hoje,dados=mariadb(
        'SELECT ID, Descricao, Categoria, DATE_FORMAT(Validade, "%d/%m/%Y") Validade, Quantidade FROM Estoque WHERE Quantidade > 0 ORDER BY 4;'
    ))

# Rota para adicionar compras ao estoque
@app.route('/estoque/compra', methods=['GET', 'POST'])
def compra():
    if request.method == 'POST':
        desc = request.form['descricao']
        categoria = request.form['categoria']
        fornecedor = request.form['fornecedor']
        quantidade = request.form['quantidade']
        validade = request.form['validade']
        vencimento = request.form['divida']
        valor = request.form['valor']

        # Inserção de dados no estoque
        mariadb(f'INSERT INTO Estoque (Descricao, Categoria, Validade, Quantidade) VALUES ("{desc}", "{categoria}", "{validade}", "{quantidade}");')
        
        # Obtendo ID do fornecedor
        fornecedor_id = mariadb(f'SELECT DISTINCT Id FROM Fornecedor WHERE Nome = "{fornecedor}";')
        id_forn = fornecedor_id[0]['Id']
        
        # Inserção na tabela de contas a pagar
        mariadb(f'INSERT INTO Contas_a_Pagar (Fornecedor, Data_de_Vencimento, Valor) VALUES ("{id_forn}", "{vencimento}", "{valor}") ;')
        return redirect(url_for('estoque'))
    
    return render_template('adicionar_produto.html', dados=mariadb('SELECT * FROM Fornecedor'))


@app.route('/estoque/descarte/<int:id>')
def descarte(id):
    
    mariadb(f'UPDATE Estoque SET Quantidade = 0 WHERE ID = "{id}"')
    return redirect(url_for('estoque'))


# Rota para listar fornecedores
@app.route('/fornecedores')
def fornecedores():
    return render_template('fornecedores.html', dados=mariadb('SELECT * FROM Fornecedor'))

# Rota para cadastrar fornecedores
@app.route('/fornecedores/cadastro', methods=['GET', 'POST'])
def cad_fornecedor():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        tel = request.form['telefone']

        mariadb(f'INSERT INTO Fornecedor (Nome, Email, Telefone) VALUES ("{nome}", "{email}", "{tel}")')
        return redirect(url_for('fornecedores'))
    return render_template('cadastrar_fornecedor.html')

@app.route('/fornecedores/alterar/<int:id>', methods=['GET','POST'])
def alt_fornecedor(id):
    
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        tel = request.form['telefone']
        mariadb(f'UPDATE Fornecedor SET Nome = "{nome}", Email = "{email}", Telefone = "{tel}" WHERE ID = "{id}";')
        return redirect(url_for('fornecedores'))
    
    return render_template('alterar_fornecedor.html', fornecedor=mariadb(f'SELECT * FROM Fornecedor WHERE ID = "{id}"')[0])

# Rota para exibição das vendas
@app.route('/vendas')
def vendas():
    return render_template('vendas.html' ,dados = mariadb(' SELECT c.Nome AS ID_Cliente, v.ID, v.Preco, v.Fiado FROM Vendas AS v JOIN Clientes AS c ON v.ID_Cliente = c.ID'))

@app.route('/vendas/<id>')
def itens_venda(id):
    return render_template('Itens_venda.html', dados = mariadb(f'SELECT e.Descricao AS ID_Produto, i.Valor_Unidade, i.Quantidade, i.Total FROM Item_Venda AS i JOIN Estoque AS e ON i.ID_Produto = e.ID WHERE ID_Venda = "{id}" '))
    
    
# Rota para adicionar vendas
@app.route('/vendas/adicionar_vendas', methods=['GET', 'POST'])
def ad_vendas():
     
    return render_template('ad_vendas.html', item_produtos=mariadb('SELECT * FROM Estoque;'), clientes=mariadb('SELECT * FROM Clientes'))

@app.route('/finalizar_compra', methods=['POST'])
def finalizar_compra():
    # Obter dados do formulário
    cliente = request.form.get('cliente')  # Nome do cliente
    fiado = request.form.get('fiado')  # Se a compra é fiada (Sim/Não)
    
    # Pegar os itens do carrinho
    total_itens = int(request.form.get('total_itens', 0))  # Número de itens no carrinho
    itens_carrinho = []

    # Percorrer todos os produtos do carrinho
    for i in range(total_itens):
        produto_id = request.form.get(f'produto_id_{i}')
        descricao = request.form.get(f'descricao_{i}')
        quantidade = int(request.form.get(f'quantidade_{i}'))
        preco = float(request.form.get(f'preco_{i}'))
        total = float(request.form.get(f'total_{i}'))

        # Criar um dicionário com os dados do item e adicionar à lista de itens
        itens_carrinho.append({
            'produto_id': produto_id,
            'descricao': descricao,
            'quantidade': quantidade,
            'preco': preco,
            'total': total
        })

    # Aqui você pode processar a compra como desejar, por exemplo:
    # - Inserir os dados no banco de dados
    # - Gerar uma fatura
    # - Enviar uma confirmação ao usuário

    # Exemplo de resposta
    resposta = {
        "mensagem": "Compra finalizada com sucesso!",
        "cliente": cliente,
        "fiado": fiado,
        "itens": itens_carrinho
    }
    
    id_cliente = request.form['cliente']
    
    
    def soma(valor):
        total = 0
        for x in valor:
            total += x['total']
            
        return total
        
    mariadb(f'INSERT INTO Vendas (ID_Cliente, Preco, Fiado) VALUES ("{id_cliente}","{soma(itens_carrinho)}","{resposta["fiado"]}");')
    
    id_venda = mariadb('SELECT ID AS ID FROM Vendas ORDER BY 1 DESC LIMIT 1;')
        
    try:
        id_venda = id_venda[0]['ID']
    except:
        id_venda = 1
    
    
       
        
    if resposta['fiado'] == 'SIM':
        mariadb(f'INSERT INTO Contas_a_Receber (ID_Cliente,Valor) VALUES ("{id_cliente}","{soma(itens_carrinho)}")')
    
    
   
    for x in itens_carrinho:
        mariadb(f'INSERT INTO Item_Venda (ID_Produto, ID_Venda, Quantidade, Valor_Unidade, Total) VALUES ("{x["produto_id"]}","{id_venda}","{x["quantidade"]}","{x["preco"]}","{x["total"]}")')
        mariadb(f'UPDATE Estoque SET Quantidade = Quantidade - {x["quantidade"]} WHERE ID = {x["produto_id"]}')
    return jsonify(resposta)


# Rota para listar contas a receber (fiado)
@app.route('/receber')
def lista_fiado():
    return render_template('lista_receber.html', dados=mariadb(
        'SELECT r.ID, c.Nome, r.Valor, DATE_FORMAT(r.Data_da_Venda, "%d/%m/%Y") AS Data_da_Venda, r.Situacao FROM Contas_a_Receber r JOIN Clientes c ON c.ID = r.ID_Cliente WHERE Situacao = "PENDENTE";'
    ))


@app.route('/receber/<id>')
def receber(id):
    mariadb(f'UPDATE Contas_a_Receber SET Situacao = "PAGO" WHERE ID = {id} ;')
    return redirect(url_for('lista_fiado'))


# Rota para listar contas a pagar
@app.route('/dividas')
def lista_pagar():
    return render_template('lista_pagar.html', hoje=hoje , dados=mariadb(
        'SELECT d.ID , f.nome Fornecedor, DATE_FORMAT(d.Data_de_Vencimento, "%d/%m/%Y") AS Data_de_Vencimento, d.Valor, d.Situacao FROM Contas_a_Pagar AS d JOIN Fornecedor AS f ON f.ID = d.Fornecedor WHERE Situacao = "PENDENTE" ORDER BY 3 ;'
    ))
    
@app.route('/dividas/<id>')
def pagar(id):
    
    mariadb(f'UPDATE Contas_a_Pagar SET Situacao = "PAGA" WHERE ID = {id} ;')
    
    return redirect(url_for('lista_pagar'))
    

# Criando um filtro para converter string para datetime no Jinja2
@app.template_filter('strptime')
def strptime_filter(value, format='%d/%m/%Y'):
    return datetime.strptime(value, format).date()

# Rota para exibir clientes
@app.route('/clientes')
def clientes():
    return render_template('clientes.html', dados=mariadb('SELECT * FROM Clientes;'))

# Rota para cadastrar clientes
@app.route('/cliente/cadastro', methods=['GET', 'POST'])
def cad_cliente():
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        mariadb(f'INSERT INTO Clientes (Nome, Telefone) VALUES ("{nome}", "{telefone}")')
        redirect(url_for('clientes'))
    return render_template('cadastrar_cliente.html')

@app.route('/cliente/alterar/<int:id>', methods = ['GET','POST'] )
def alt_cliente(id):
    
    if request.method == 'POST':
        nome = request.form['nome']
        tel = request.form['telefone']
        
        mariadb(f'UPDATE Clientes SET Nome = "{nome}", Telefone = "{tel}" WHERE ID = "{id}"')
        return redirect(url_for('clientes'))
    
    return render_template('alterar_cliente.html', cliente = mariadb(f'SELECT * FROM Clientes WHERE ID = "{id}"')[0])
    
    



# Executando a aplicação Flask
if __name__ == '__main__':   
    app.run(debug=True, host='0.0.0.0')

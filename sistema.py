import pymysql.cursors


conexao = pymysql.connect(
    host='localhost',
    user='root',
    password='1234',
    db='erp',
    charset='utf8mb4',
    cursorclass= pymysql.cursors.DictCursor
)

from time import sleep
import matplotlib.pyplot as plt


def logarcadastrar():
    usuarioExistente = 0
    autenticado = False #a variavel atentico vai receber dentro do while o que retornar da variavel autenticado
    usuarioMaster = False #esta variavel serve para identificar se o nivel do usuario é igual a 2. Se usuaraio igual a 2 ele estara logando como usuario master
    if decisao == 1:      #se o usuario decidir somente logar. Depois que o usuario digirar 1 ele entrara no processo de log verificando se ha um usuario e senha dentro do banco de dados
        nome = input('Digite seu nome: ')
        senha = input('Digite sua senha: ')
        for linha in resultado:    #este for é uma verificaçao dentro da variavel resultado onde estara guardado os dados de todos os usuarios. ele verificara linha por linha se ha um usuario com este nome e senha
            #depois que ele entra dentro deste if ele pergunta se o usuario é master
            if nome == linha['nome'] and senha == linha['senha']: # estou verificando se os valores digitados já constam dentro do banco de dados do usuario, se tiver recebera uma mensagem para digitar outro usuario
                autenticado = True  # ele vai ser autenticado de qualquer forma
                print(f'bem vindo ao programa, {linha["nome"]}!  ')
                if linha['nivel'] == 1: #precisa perguntar se o nivle do usuario é igual a master para definir o tipo de acesso do usuario
                    usuarioMaster = False #se não é usuario master é falso
                elif linha['nivel'] == 2:
                    usuarioMaster = True  #se ele for usuario master entao é verdadeiro
                break
            else:                         #caso não seja autenticado
                autenticado = False
        if not autenticado: #essa mensagem será exibida se ele não for autenticado
            print('Email ou senha invalidos. Tente novamente')
    elif decisao == 2:      #se digitar a decisão 2 ele começara um novo cadastro
        print('Faça seu cadastro!')
        nome = input('Digite seu nome: ')
        senha = input('Digite sua senha: ')
        for linha in resultado: # fazendo a mesma verificaçao que la em cima. para saber se ha usuario existente antes de finalizar o cadastro. ele vai procurar em todas as linhas da variavel resultado para saber se os dados digitados ja constam dentro de algum cadastro feito anteriormente
            if nome == linha['nome'] and senha == linha['senha']:
                usuarioExistente = 1   # se o resultado for 1 quer dizer que ele esta tentando cadastrar um usuario e senha que ja foram cadastrados anteriormente
        if usuarioExistente == 1:
            print('Usuario já cadastrado! Tente um nome diferente.')
        elif usuarioExistente == 0:
            try:
                with conexao.cursor() as cursor:  #se não existir esse usuario entao ele fara uma conexao com o banco de dados para armazenar o novo login de usuario
                    cursor.execute('insert into cadastros(nome,senha,nivel) values(%s,%s,%s)',(nome,senha,1)) #aqui é o comando para inserir os dados no banco de dados
                    conexao.commit()
                print('Usuario cadastrado com sucesso!')
            except:   #se por algum motivo não conseguir se conectar ao banco de dados aparecera uma mensagem de erro aqui
                print('Erro ao inserir os dados no banco de dados')
    return autenticado,usuarioMaster  #vai ser retornado dentro do while e la dentro sera chamado a funçaorecad


def cadastrarProduto():   #inserindo os dados do cadastro atraves dessa funçao
    nome = input('Digite o nome do produto: ' )
    ingredientes = input('Digite os ingredientes do produto:  ')
    grupo = input('Digite o grupo pertencente as esse produto: ')
    preco = float(input('Digite o preço do produto: '))
    try:
        with conexao.cursor() as cursor: #aqui conectamos com o banco de dados sql
            cursor.execute('insert into produtos(nome,ingredientes,grupo,preco) values (%s,%s,%s,%s)',(nome,ingredientes,grupo,preco)) #aqui estamos executando um comando em sql para inserir os dados que foram digitados em python dentro da tabela sql
            conexao.commit()
            print('Produto cadastrado com sucesso!')
    except:   #caso não consiga inserir os dados aparecerá este erro!
        print('Erro ao inserir os produtos no banco de dados')


def listarProdutos(): #funçao para apresentar os produtos cadastrados
    produtos = []
    try:
        with conexao.cursor() as cursor: #conectando ao banco de dados
            cursor.execute('select * from produtos')    #usando uma funçao em sql para visualizar os dados
            produtosCadastrados = cursor.fetchall()
    except:
        print('Erro ao conectar ao banco de dados!')
    for i in produtosCadastrados:
        produtos.append(i)
    if len(produtos) != 0:
        for i in range(0,len(produtos)):
            print(f'{produtos[i]}')
    else:
        print('Nenhum produto cadastrado!')


def excluirProdutos():
    idDeletar = int(input('Digite o ID do produto que deseja deletar: '))
    try:
        with conexao.cursor() as cursor:
            cursor.execute(f'delete from produtos where id = {idDeletar}')
            conexao.commit()

    except:
        print(f'Erro ao excluir o produto com ID {idDeletar}')


def listarPedidos():
    pedidos = []
    decision = 0
    while decision != 2:
        pedidos.clear()
        try:
            with conexao.cursor() as cursor:
                cursor.execute('select * from pedidos')
                listaPedidos = cursor.fetchall()
        except:
            print('Erro ao se conectar ao banco de dados!')
        for i in listaPedidos:
            pedidos.append(i)
        if len(pedidos) != 0:
            for i in range(0,len(pedidos)):
                print(pedidos[i])
        else:
            print('Nenhum pedido foi feito!')


        decision = int(input('''
        Digite:
         [1] Produto entregue
         [2] Voltar'''))
        if decision == 1:
            idDeletar = int(input('Digite o ID do produto entregue: '))
            try:
                with conexao.cursor() as cursor:
                    cursor.execute(f'delete from pedidos where id = {idDeletar}')
                    conexao.commit()
                print('Produto dado como entregue!')
            except:
                print(f'Erro ao excluir o produto {idDeletar}')


#gerando estatistica para criação de grafico
def gerarEstatistica():
    nomeProduto = []
    nomeProduto.clear() #limpando a lista para que não acumule produtos na conta
    try:
        with conexao.cursor() as cursor:    #conexão com banco de dados
            cursor.execute('select * from produtos')
            produtos = cursor.fetchall() #colocando tudo de produtos dentro da variabel produtos
    except:
        print('Erro ao fazer consulta no banco de dados')
    try:
        with conexao.cursor() as cursor:    # conexão com o banco de dados
            cursor.execute('select * from estatistica_vendido')
            vendido = cursor.fetchall()  # colocando tudo da tabela estatistica vendido dentro da variavel vendido
    except:
        print('Erro ao fazer a consulta dentro do banco de dados')
        #pedir uma decisão do usuario
    estado = int(input('''Digite
    [0] SAIR
    [1] PESQUISAR POR NOME
    [2] PESQUISAR POR GRUPO
    '''))
    if estado == 1:
        decisao3 = int(input('''Digite
        [1] Pesquisar por valor monetario
        [2] Pesquisar por quantidade vendida
        '''))
        if decisao3 == 1:  #varrendo toda a variavel que criamos para colocar todos os dados dos produtos
            for i in produtos:
                nomeProduto.append(i['nome']) #inserindo apenas o nome dos produtos dentro da tabela produtos
            valores = []  #criando uma variavel para inserir os valores
            valores.clear()
            for h in range(0,len(nomeProduto)): #varrer todas esta lista
                somaValor = -1   #para cada nome do produto vai ser varrido ou procurado dentro da tabela estatistica vendido
                for i in vendido:
                    if i['nome'] == nomeProduto[h]:
                        somaValor += i['preco']  #cada vez que for somar, será somado o preço que foi vendido determinado produto
                if somaValor == -1:
                    valores.append(0)
                elif somaValor > 0:
                    valores.append(somaValor + 1)

            plt.plot(nomeProduto, valores)  #o eixo x do grafico será o nome de cada produto      e o eixo y será os valores
            plt.ylabel('quantidade vendida em reais ')  #especificando o eixo y da tabela
            plt.xlabel('produtos')   #especificando o eixo x da tabela
            plt.show()   #mostrar a tabela na tela
        if decisao3 == 2:
            grupoUnico = []
            grupoUnico.clear()
            try:
                with conexao.cursor() as cursor:
                    cursor.execute('select * from produtos')
                    grupo = cursor.fetchall()
            except:
                print('Erro na consulta')
            try:
                with conexao.cursor() as cursor:
                    cursor.execute('select * from estatistica_vendido')
                    vendidoGrupo = cursor.fetchall()
            except:
                print('Erro na consulta')
            for i in grupo:
                grupoUnico.append(i['nome'])
            grupoUnico = sorted(set(grupoUnico)) #vai varrer toda a lista e ver se tem elementos repeditos. se tiver elementos repetidos ele vai apaga-los
            quantidade_final = []
            quantidade_final.clear()
            for h in range(0,len(grupoUnico)):
                quantidade_unitaria = 0
                for i in vendidoGrupo:
                    if grupoUnico[h] == i['nome']:
                        quantidade_unitaria += 1
                quantidade_final.append(quantidade_unitaria) #vai quantificar a quantidade de produtos vendidos pelo nome1
            plt.plot(grupoUnico,quantidade_final)
            plt.ylabel('quantidade unitaria vendida')
            plt.xlabel('produtos')
            plt.show()
    elif estado == 2:
        decisao3 = int(input('''Digite
         [1] Pesquisar por valor monetario
         [2] Pesquisar por quantidade vendida
         '''))
        if decisao3 == 1:  # varrendo toda a variavel que criamos para colocar todos os dados dos produtos
            for i in produtos:
                nomeProduto.append(i['grupo'])  # inserindo apenas o nome dos produtos dentro da tabela produtos
            valores = []  # criando uma variavel para inserir os valores
            valores.clear()
            for h in range(0, len(nomeProduto)):  # varrer todas esta lista
                somaValor = -1  # para cada nome do produto vai ser varrido ou procurado dentro da tabela estatistica vendido
                for i in vendido:
                    if i['grupo'] == nomeProduto[h]:
                        somaValor += i['preco']  # cada vez que for somar, será somado o preço que foi vendido determinado produto
                if somaValor == -1:
                    valores.append(0)
                elif somaValor > 0:
                    valores.append(somaValor + 1)

            plt.plot(nomeProduto,
                     valores)  # o eixo x do grafico será o nome de cada produto      e o eixo y será os valores
            plt.ylabel('quantidade vendida em reais ')  # especificando o eixo y da tabela
            plt.xlabel('produtos')  # especificando o eixo x da tabela
            plt.show()  # mostrar a tabela na tela

        if decisao3 == 2:
            grupoUnico = []
            grupoUnico.clear()
            try:
                with conexao.cursor() as cursor:
                    cursor.execute('select * from produtos')
                    grupo = cursor.fetchall()
            except:
                print('Erro na consulta')
            try:
                with conexao.cursor() as cursor:
                    cursor.execute('select * from estatistica_vendido')
                    vendidoGrupo = cursor.fetchall()
            except:
                print('Erro na consulta')
            for i in grupo:
                grupoUnico.append(i['grupo'])
            grupoUnico = sorted(
                set(grupoUnico))  # vai varrer toda a lista e ver se tem elementos repeditos. se tiver elementos repetidos ele vai apaga-los
            quantidade_final = []
            quantidade_final.clear()
            for h in range(0, len(grupoUnico)):
                quantidade_unitaria = 0
                for i in vendidoGrupo:
                    if grupoUnico[h] == i['grupo']:
                        quantidade_unitaria += 1
                quantidade_final.append(
                    quantidade_unitaria)  # vai quantificar a quantidade de produtos vendidos pelo nome1
            plt.plot(grupoUnico, quantidade_final)
            plt.ylabel('quantidade unitaria vendida')
            plt.xlabel('produtos')
            plt.show()



autentico = False
while not autentico:
    decisao = int(input('''Digite uma opção:  
[1] Logar no programa
[2] Cadastrar novo usuario '''))
    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from cadastros') #isso aqui vai armazenar os cadastros dentro do banco de dados dentro do mysql
            resultado = cursor.fetchall()
        #vão ser armazenado dentro da variavel resultado. todas as colunas e todas as linhas
    except: #se não conseguir acessar o banco de dados ele dará um aviso
        print('Erro ao conectar com o banco de dados')
    autentico,usuarioSupremo = logarcadastrar()  #será inserido dentro desta variavel o que retornar da funçao logarcadastrar



if autentico:
    print('Autenticado!')
    decisaoUsuario = 1
    while decisaoUsuario != 0:
        decisaoUsuario = int(input('''
            [0] Para sair
            [1] Para cadastrar
            [2] Listar produtos catalogados
            [3] Listar Pedidos
            [4] Visualizar as estatisticas
            '''))
        if decisaoUsuario == 1:
            cadastrarProduto() #chamando a funçao feita por nós.
        if usuarioSupremo == True:  # só poderá cadastrar produtos se for administrador, ou seja, usuario supremo
            if decisaoUsuario == 2:
                listarProdutos()
                delete = int(input('''
                [1] Excluir Produto
                [2] Voltar ao menu anterior'''))
                if delete == 1:
                    excluirProdutos()
        else:
            print('Esta opcçao é inacessivel para este usuario!')

        if decisaoUsuario == 3:
            listarPedidos()
        if decisaoUsuario == 4:
            gerarEstatistica()



print('Finalizando o programa...')


sleep(3)1
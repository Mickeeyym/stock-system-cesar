import json
import os
from time import sleep
import uuid

arquivo = os.path.join(os.path.dirname(__file__), 'bancoDados.json')

def carregar_bancoDados():
    # Verifica se o arquivo existe, se não existir, cria um arquivo com lista vazia
    if not os.path.exists(arquivo):
        with open(arquivo, 'w') as f:
            json.dump([], f, indent=4)
    
    # Carrega o conteúdo do arquivo
    with open(arquivo, 'r') as f:
        return json.load(f)

class Produto:

    def __init__(self, nome, descriçao, preçoCompra, preçoVenda, quantidade):
        self.id = str(uuid.uuid4()) #Gerar id único
        self.nome = nome
        self.descriçao = descriçao
        self.preçoCompra = preçoCompra
        self.preçoVenda = preçoVenda
        self.quantidade = quantidade

    def toDictonary(self):  #Método para transformar os atributos do OBJ em dicionário
        return {
                'Id': self.id,
                'Nome': self.nome, 
                'Descricao': self.descriçao, 
                'Preco de Compra': self.preçoCompra,
                'Preco de Venda': self.preçoVenda, 
                'Quantidade': self.quantidade}

def produtoExiste(nome, descricao):

    produtos = carregar_bancoDados()
    for p in produtos:
        if ((p['Nome']==nome) | (p['Descricao']==descricao)):
            return True
    return False

def buscarIdProduto(idProduto):
    produtos = carregar_bancoDados()
    for p in produtos:
        if (p['Id']==idProduto):
            return p
    return None

# Função para atualizar os Produtos a partir do ID

def atualizaProduto():
    listarProdutos()
    idProduto = str(input("Digite o ID do produto que deseja atualizar: "))

    produto = buscarIdProduto(idProduto)
        
    while(produto is None):
        print("Produto com ID fornecido não encontrado")
        idProduto = str(input("Por favor, digite o ID do produto que deseja atualizar: "))
        produto = buscarIdProduto(idProduto)
    
    print("-"*50)
    print("PRODUTO SELECIONADO")
    print()
    print(f"Nome: {produto['Nome']}\nDescrição: {produto['Descricao']}\nPreço de Compra: {produto['Preco de Compra']}\nPreço de Venda: {produto['Preco de Venda']}\nQuantidade: {produto['Quantidade']} ")
    print()
    print("-"*50)
    print()
    
    # Permite ao usuário atualizar ou não os campos individualmente
    produto['Nome'] = str(input(f"Nome [{produto['Nome']}]: ") or produto['Nome'])
    produto['Descricao'] = str(input(f"Descrição [{produto['Descricao']}]: ") or produto['Descricao'])
    produto['Preco de Compra'] = float(input(f"Preço de Compra [{produto['Preco de Compra']}]: ") or produto['Preco de Compra'])
    produto['Preco de Venda'] = float(input(f"Preço de Venda [{produto['Preco de Venda']}]: ") or produto['Preco de Venda'])
    produto['Quantidade'] = int(input(f"Quantidade [{produto['Quantidade']}]: ") or produto['Quantidade'])

    produtos = carregar_bancoDados()

    for i, p in enumerate(produtos):
        if (p['Id']==idProduto):
            produtos[i]=produto
            break
    
    with open(arquivo, 'w') as f:
        json.dump(produtos, f, indent=4, ensure_ascii=False)
    
    print()
    print("PRODUTO ATUALIZADO COM SUCESSO!")

#Função para deletar o produto

def deletarProduto():
    listarProdutos()
    idProduto = str(input("Digite o ID do produto que deseja deletar: "))

    produto = buscarIdProduto(idProduto)

    while(produto is None):
        print("Produto com ID fornecido não encontrado")
        idProduto = str(input("Por favor, digite o ID do produto que deseja deletar: "))
        produto = buscarIdProduto(idProduto)
    
    print("-"*50)
    print("PRODUTO SELECIONADO")
    print()
    print(f"Nome: {produto['Nome']}, Descrição: {produto['Descricao']}, Preço de Compra: {produto['Preco de Compra']}, Preço de Venda: {produto['Preco de Venda']}, Quantidade: {produto['Quantidade']} ")
    print()
    print("-"*50)
    print()

    produtos = carregar_bancoDados()

    for i, p in enumerate(produtos):
        if (p['Id']==idProduto):
            del produtos[i]
            break
    
    with open(arquivo, 'w') as f:
        json.dump(produtos, f, indent=4, ensure_ascii=False)
    
    print()
    print("PRODUTO EXCLUIDO COM SUCESSO!")

    
# Função para listar os Produtos existentes

def listarProdutos():

    produtos = carregar_bancoDados()

    if produtos:
        print()
        print("LISTA DE PRODUTOS")
        print()

        for p in produtos:
            print("-"*50)
            print(f"ID: {p['Id']}")
            print(f"Nome: {p['Nome']}")
            print(f"Descrição: {p['Descricao']}")
            print(f"Preço de Compra: {p['Preco de Compra']}")
            print(f"Preço de Venda: {p['Preco de Venda']}")
            print(f"Quantidade: {p['Quantidade']}")
            print("-"*50)

    else:
        print("NENHUM USUÁRIO CADASTRADO")


#Função para adicionar Produtos ao Banco de dados

def adicionarProduto():
    nome = str(input("Digite o nome do produto que deseja adicionar: "))
    descricao = str(input("Digite a descrição do produto: "))
    preçoCompra = float(input("Digite o preço compra do produto: "))
    preçoVenda = float(input("Digite o preço de venda do produto: "))
    quantidade = int(input("Digite a quantidade do produto: "))

    while(produtoExiste(nome, descricao)):
        print("Erro: Produto já existe no banco de dados")
        print("Por favor, faça novamente: ")
        nome = str(input("Digite o nome do produto que deseja adicionar: "))
        descricao = str(input("Digite a descrição do produto: "))
        produtoExiste(nome, descricao)  

    produto = Produto(nome, descricao, preçoCompra, preçoVenda, quantidade) #Instanciando o Produto como OBJ

    produtoLista = carregar_bancoDados()  

    produtoLista.append(produto.toDictonary())

    # Salva a lista atualizada no arquivo
    with open(arquivo, 'w') as f:
        json.dump(produtoLista, f, indent=4, ensure_ascii=False)

    print("PRODUTO ADICIONADO COM SUCESSO!")
     
# Menu inicial do programa

def menu():
    print("-"*50)
    print("\n--- Sistema de Gerenciamento de Estoque ---")
    print("\n1. Gerenciar Produtos")
    print("2. Gerenciar Fornecedores")
    print("3. Gerenciar Usuários")
    print("4. Sair\n")
    print("-"*50)
    print()

# Menu do Gerenciamente de Produto

def menuProduto():
    print("-"*50)
    print("\n--- MENU GERENCIAMENTO DE PRODUTO ---")
    print("\n1. Adicionar Produtos")
    print("2. Listar Produtos")
    print("3. Atualizar Produtos")
    print("4. Excluir Produtos")
    print("5. Voltar ao Menu Anterior\n")
    print("-"*50)
    print()

def main():

    while True:
        menu()
        opcaoInicial = int(input("Informe a opção desejada: "))
        match (opcaoInicial):
            case 1:
                while True:
                    menuProduto()
                    opcaoProduto = int(input("Informe a opção desejada: "))
                    match(opcaoProduto):
                        case 1:
                            print("\n1. Adicionar Produtos")
                            adicionarProduto()
                            print()
                        
                        case 2:
                            print("\n2. Listar Produtos")
                            listarProdutos()
                            print()

                        case 3:
                            print("\n3. Atualizar Produtos")
                            atualizaProduto()
                            print()
                        
                        case 4:
                            print("\n4. Excluir Produtos")
                            deletarProduto()
                            print()
                        
                        case 5:
                            print("\n5. Voltar ao Menu Anterior")
                            print()
                            break                    
            case 2:
                print("Em desenvolvimento") 
            case 3:
                print("Em desenvolvimento")
            case 4:
                break
            
    
    print("Programa Finalizado")
                              

if __name__ == "__main__":
    main()



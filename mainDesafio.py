import json
import os
import uuid

arquivo = os.path.join(os.path.dirname(__file__), 'produtos.json')

def carregar_bancoDados():
    # Verifica se o arquivo existe, se não existir, cria um arquivo com lista vazia
    if not os.path.exists(arquivo):
        with open(arquivo, 'w', encoding="utf-8") as f:
            json.dump([], f, indent=4)
    
    # Carrega o conteúdo do arquivo
    with open(arquivo, 'r', encoding="utf-8") as f:
        return json.load(f)

# Salva a lista atualizada no arquivo

def salvarArquivo(produtos):
    with open(arquivo, 'w', encoding="utf-8") as f:
        json.dump(produtos, f, indent=4, ensure_ascii=False)

class Produto:

    def __init__(self, nome, unidadeMedida,descriçao):
        self.id = str(uuid.uuid4().int)[:4] #Gerar id único de 4 dígitos
        self.nome = nome
        self.unidadeMedida = unidadeMedida
        self.descriçao = descriçao

    def toDictonary(self):  #Método para transformar os atributos do OBJ em dicionário
        return {
                'Id': self.id,
                'Nome': self.nome,
                'Descrição': self.descriçao,
                'Unidade de Medida': self.unidadeMedida, 
                }

def produtoExiste(nome, descricao):
    produtos = carregar_bancoDados()
    for p in produtos:
        if ((p['Nome']==nome) | (p['Descrição']==descricao)):
            return True
    return False

def buscarIdProduto(idProduto):
    produtos = carregar_bancoDados()
    for p in produtos:
        if (p['Id']==idProduto):
            return p
    return None

#Função para adicionar Produtos ao Banco de dados

def adicionarProduto():
    nome = str(input("Digite o nome do produto que deseja adicionar: "))
    descricao = str(input("Digite a descrição do produto: "))
    unidadeMedida = str(input("Digite a unidade de medida do produto que deseja adicionar: "))

    while(produtoExiste(nome, descricao)):
        print("Erro: Produto já existe no banco de dados")
        print("Por favor, faça novamente: ")
        nome = str(input("Digite o nome do produto que deseja adicionar: "))
        descricao = str(input("Digite a descrição do produto: "))
        produtoExiste(nome, descricao)  

    produto = Produto(nome, unidadeMedida, descricao) #Instanciando o Produto como OBJ

    produtoLista = carregar_bancoDados()  

    produtoLista.append(produto.toDictonary())

    salvarArquivo(produtoLista)

    print("PRODUTO ADICIONADO COM SUCESSO!")

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
            print(f"Descrição: {p['Descrição']}")
            print(f"Unidade de Medida: {p['Unidade de Medida']}")
            print("-"*50)

    else:
        print("NENHUM USUÁRIO CADASTRADO")

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
    print(f"Nome: {produto['Nome']}\nDescrição: {produto['Descrição']}\nUnidade de Medida: {produto['Unidade de Medida']}\n ")
    print()
    print("-"*50)
    print()
    
    # Permite ao usuário atualizar ou não os campos individualmente
    produto['Nome'] = str(input(f"Nome [{produto['Nome']}]: ") or produto['Nome'])
    produto['Descrição'] = str(input(f"Descrição [{produto['Descrição']}]: ") or produto['Descrição'])
    produto['Unidade de Medida'] = str(input(f"Unidade de Medida [{produto['Unidade de Medida']}]: ") or produto['Unidade de Medida'])

    produtos = carregar_bancoDados()

    for i, p in enumerate(produtos):
        if (p['Id']==idProduto):
            produtos[i]=produto
            break
    
    salvarArquivo(produtos)
    
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
    print(f"Nome: {produto['Nome']}, Descrição: {produto['Descrição']}, Unidade de Medida: {produto['Unidade de Medida']} ")
    print()
    print("-"*50)
    print()

    produtos = carregar_bancoDados()

    for i, p in enumerate(produtos):
        if (p['Id']==idProduto):
            del produtos[i]
            break
    
    salvarArquivo(produtos)
    
    print()
    print("PRODUTO EXCLUIDO COM SUCESSO!")
  
# Começo do CRUD Usuários      

class Usuario:      
    def __init__(self, id, nome, email, telefone, funcao):   
        self.id = id   
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.funcao = funcao

    def to_dict(self):   #o metodo to_dict é um método da classe usuario que converte uma instancia da classe em um dicionario python. Ou seja, o to_dict transforma os atributos do objeto usuarioem um dicionario. Vai retornar cada atributo em forma de uma chave do dicionario
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone,
            'funcao': self.funcao
        }

class UsuarioCRUD:
    def __init__(self, arquivo='usuarios.json'):
        self.arquivo = arquivo  
        self.usuarios = self.carregar_usuarios() or []

    def carregar_usuarios(self):   
        if os.path.exists(self.arquivo):
            with open(self.arquivo, 'r', encoding="utf-8") as f:
                if os.path.getsize(self.arquivo) > 0:  
                    return [Usuario(**d) for d in json.load(f)]    
            return []

    def salvar_usuarios(self):
        with open(self.arquivo, 'w', encoding="utf-8") as f:
            json.dump([usuario.to_dict() for usuario in self.usuarios], f, indent = 4, ensure_ascii=False)  #json.dump salva a lista de dicionarios

    def cadastrar_usuario(self, id, nome, email, telefone, funcao):
        novo_usuario = Usuario(id, nome, email, telefone, funcao)
        self.usuarios.append(novo_usuario)
        self.salvar_usuarios()  #chama a função salvar.usuarios() para que seja executada (ou seja, seja salvo o novo usuario)
        print(f'Usuário {nome} cadastrado com sucesso!')

    def listar_usuarios(self):
        if not self.usuarios:
            print("Nenhum usuário cadastrado.")
            return
        for usuario in self.usuarios:  
            print(f'ID: {usuario.id}, Nome: {usuario.nome}, Email: {usuario.email}, Telefone: {usuario.telefone}, Função: {usuario.funcao}')

    def atualizar_usuario(self, usuario_id, nome, email, telefone, funcao):
        for usuario in self.usuarios:
            if usuario.id == usuario_id:  #verifica se o id do usuário atual é igual ao id fornecido (ou seja, verifica se esse usuário/id existe no sistema)
                usuario.nome = nome
                usuario.email = email
                usuario.telefone = telefone
                usuario.funcao = funcao
                self.salvar_usuarios()
                print(f'Usuário com ID {usuario_id} atualizado com sucesso!')
                return
        print(f'Usuário com ID {usuario_id} não encontrado.')

    def excluir_usuario(self, usuario_id):
        for usuario in self.usuarios:
            if usuario.id == usuario_id:
                self.usuarios.remove(usuario)
                self.salvar_usuarios()
                print(f'Usuário com ID {usuario_id} excluído com sucesso!')
                return
        print(f'Usuário com ID {usuario_id} não encontrado.')

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

def menuUsuarios():
    print("-"*50)
    print("\n--- MENU DE USUÁRIOS ---")
    print("\n1. Cadastrar Usuário")
    print("2. Listar Usuários")
    print("3. Atualizar Usuário")
    print("4. Excluir Usuário")
    print("5. Sair")
    print("-"*50)
    print()

def main():

    while True:
        menu()
        opcaoInicial = int(input("Informe a opção desejada: "))
        
        while ((opcaoInicial<1) | (opcaoInicial>4)):
            print()
            print("Por favor digite um valor válido para navegar no menu")
            opcaoInicial = int(input("Informe a opção desejada: "))
            print()

        match (opcaoInicial):
            case 1:
                while True:
                    menuProduto()
                    opcaoProduto = int(input("Informe a opção desejada: "))

                    while ((opcaoProduto<1) | (opcaoProduto>5)):
                        print()
                        print("Por favor digite um valor válido para navegar no menu")
                        opcaoProduto = int(input("Informe a opção desejada: "))
                        print()

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
                crud = UsuarioCRUD()
                while True:
                    menuUsuarios()
                    opcaoUsuario = int(input("Informe a opção desejada: "))

                    while ((opcaoUsuario<1) | (opcaoUsuario>5)):
                        print()
                        print("Por favor digite um valor válido para navegar no menu")
                        opcaoUsuario = int(input("Informe a opção desejada: "))
                        print()
                    
                    match (opcaoUsuario):
                        case 1:
                            id = str(uuid.uuid4())
                            nome = input("Nome: ")
                            email = input("Email: ")
                            telefone = input("Telefone: ")
                            funcao = input("Função: ")
                            crud.cadastrar_usuario(id, nome, email, telefone, funcao)
                            print("USUÁRIO ADICIONADO COM SUCESSO")
                        
                        case 2:
                            crud.listar_usuarios()
                        
                        case 3: 
                            usuario_id = str(input("ID do Usuário a ser atualizado: "))
                            nome = input("Novo Nome: ")
                            email = input("Novo Email: ")
                            telefone = input("Novo Telefone: ")
                            funcao = input("Nova função do usuário: ")
                            crud.atualizar_usuario(usuario_id, nome, email, telefone, funcao)
                            print("USUÁRIO ATUALIZADO COM SUCESSO")
                        
                        case 4:
                            usuario_id = str(input("ID do Usuário a ser excluído: "))
                            crud.excluir_usuario(usuario_id)
                            print("USUÁRIO EXCLUÍDO COM SUCESSO")
                        
                        case 5:
                            print("Saindo do sistema de usuários...")
                            break

            case 4:
                break
                
    print("Programa Finalizado")
                              
if __name__ == "__main__":
    main()



import json
import os
import uuid
from datetime import datetime

arquivo = os.path.join(os.path.dirname(__file__), 'produtos.json')
arquivoFornecedor = os.path.join(os.path.dirname(__file__), 'fornecedores.json')

# Manipulação do json de produtos

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

# Manipulação do json de fornecedores

def carregar_bancoDadosFornecedor():
    # Verifica se o arquivo existe, se não existir, cria um arquivo com lista vazia
    if not os.path.exists(arquivoFornecedor):
        with open(arquivoFornecedor, 'w', encoding="utf-8") as f:
            json.dump([], f, indent=4)
    
    # Carrega o conteúdo do arquivo
    with open(arquivoFornecedor, 'r', encoding="utf-8") as f:
        return json.load(f)

def salvarArquivoFornecedor(fornecedores):
    # Salva a lista atualizada no arquivo
    with open(arquivoFornecedor, 'w', encoding="utf-8") as f:
        json.dump(fornecedores, f, indent=4, ensure_ascii=False)

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

class Fornecedor:

    def __init__(self, nome, cnpj_cpf, email, telefone, cep, endereço, cidade, estado, país):
        self.id = str(uuid.uuid4().int)[:4]
        self.nome = nome
        self.cnpj_cpf = cnpj_cpf
        self.email = email
        self.telefone = telefone
        self.cep = cep
        self.endereço = endereço
        self.cidade = cidade
        self.estado = estado
        self.país = país
        

    def toDictionary(self):  #Método para transformar os atributos do OBJ em dicionário
        return {
                'Id': self.id,
                'Nome': self.nome, 
                'CNPJ/CPF': self.cnpj_cpf, 
                'E-mail': self.email,
                'Telefone': self.telefone, 
                'CEP': self.cep,
                'Endereço': self.endereço,
                'Cidade': self.cidade,
                'Estado': self.estado,
                'País': self.país,
                }

def fornecedorExiste(nome, cnpj_cpf):

    fornecedores = carregar_bancoDadosFornecedor()
    for p in fornecedores:
        if ((p['Nome']==nome) or (p['CNPJ/CPF']==cnpj_cpf)):
            return True
    return False

def buscarIdFornecedor(idFornecedor):
    fornecedores = carregar_bancoDadosFornecedor()
    for p in fornecedores:
        if (p['Id']==idFornecedor):
            return p
    return None

#Função para adicionar Fornecedores ao Banco de dados

def adicionarFornecedor():
    nome = str(input("Digite o nome do fornecedor que deseja adicionar: "))
    cnpj_cpf = str(input("Digite o CNPJ/CPF do fornecedor: "))
    email = str(input("Digite o e-mail do fornecedor: "))
    telefone = str(input("Digite o telefone do fornecedor: "))
    cep = str(input("Digite o CEP do fornecedor: "))
    endereço = str(input("Digite o endereço do fornecedor: "))
    cidade = str(input("Digite a cidade do fornecedor: "))
    estado = str(input("Digite o estado do fornecedor: "))
    país = str(input("Digite o país do fornecedor: "))

    while(fornecedorExiste(nome, cnpj_cpf)):
        print("Erro: Fornecedor já existe no banco de dados")
        print("Por favor, faça novamente: ")
        nome = str(input("Digite o nome do fornecedor que deseja adicionar: "))
        cnpj_cpf = str(input("Digite o CNPJ/CPF do fornecedor: "))
        fornecedorExiste(nome, cnpj_cpf)  

    fornecedor = Fornecedor(nome, cnpj_cpf, email, telefone, cep, endereço, cidade, estado, país) #Instanciando o Fornecedor como OBJ

    fornecedorLista = carregar_bancoDadosFornecedor()  

    fornecedorLista.append(fornecedor.toDictionary())

    salvarArquivoFornecedor(fornecedorLista)

    print("FORNECEDOR ADICIONADO COM SUCESSO!")

# Função para listar os Fornecedores existentes

def listarFornecedores():

    fornecedores = carregar_bancoDadosFornecedor()

    if fornecedores:
        print()
        print("LISTA DE FORNECEDORES")
        print()

        for p in fornecedores:
            print("-"*50)
            print(f"ID: {p['Id']}")
            print(f"Nome: {p['Nome']}")
            print(f"CNPJ/CPF: {p['CNPJ/CPF']}")
            print(f"E-mail: {p['E-mail']}")
            print(f"Telefone: {p['Telefone']}")
            print(f"CEP: {p['CEP']}")
            print(f"Endereço: {p['Endereço']}")
            print(f"Cidade: {p['Cidade']}")
            print(f"Estado: {p['Estado']}")
            print(f"País: {p['País']}")

    else:
        print("NENHUM FORNECEDOR CADASTRADO")

# Função para atualizar os Fornecedores a partir do ID

def atualizarFornecedor():
    listarFornecedores()
    idFornecedor = str(input("Digite o ID do fornecedor que deseja atualizar: "))

    fornecedor = buscarIdFornecedor(idFornecedor)
        
    while(fornecedor is None):
        print("Fornecedor com ID fornecido não encontrado")
        idFornecedor = str(input("Por favor, digite o ID do fornecedor que deseja atualizar: "))
        fornecedor = buscarIdFornecedor(idFornecedor)
    
    print("-"*50)
    print("FORNECEDOR SELECIONADO")
    print()
    print(f"Nome: {fornecedor['Nome']}\nCNPJ/CPF: {fornecedor['CNPJ/CPF']}\nE-mail: {fornecedor['E-mail']}\nTelefone: {fornecedor['Telefone']}\nCEP: {fornecedor['CEP']}\nEndereço: {fornecedor['Endereço']}\nCidade: {fornecedor['Cidade']}\nEstado: {fornecedor['Estado']}\nPaís: {fornecedor['País']} ")
    print()
    print("-"*50)
    print()
    
    # Permite ao usuário atualizar ou não os campos individualmente
    fornecedor['Nome'] = str(input(f"Nome [{fornecedor['Nome']}]: ") or fornecedor['Nome'])
    fornecedor['CNPJ/CPF'] = str(input(f"CNPJ/CPF [{fornecedor['CNPJ/CPF']}]: ") or fornecedor['CNPJ/CPF'])
    fornecedor['E-mail'] = str(input(f"E-mail [{fornecedor['E-mail']}]: ") or fornecedor['E-mail'])
    fornecedor['Telefone'] = str(input(f"Telefone [{fornecedor['Telefone']}]: ") or fornecedor['Telefone'])
    fornecedor['CEP'] = str(input(f"CEP [{fornecedor['CEP']}]: ") or fornecedor['CEP'])
    fornecedor['Endereço'] = str(input(f"Endereço [{fornecedor['Endereço']}]: ") or fornecedor['Endereço'])
    fornecedor['Cidade'] = str(input(f"Cidade [{fornecedor['Cidade']}]: ") or fornecedor['Cidade'])
    fornecedor['Estado'] = str(input(f"Estado [{fornecedor['Estado']}]: ") or fornecedor['Estado'])
    fornecedor['País'] = str(input(f"País [{fornecedor['País']}]: ") or fornecedor['País'])

    fornecedores = carregar_bancoDadosFornecedor()

    for i, p in enumerate(fornecedores):
        if (p['Id']==idFornecedor):
            fornecedores[i]=fornecedor
            break
    
    salvarArquivoFornecedor(fornecedores)
    
    print()
    print("FORNECEDOR ATUALIZADO COM SUCESSO!")

#Função para deletar o fornecedor

def deletarFornecedor():
    listarFornecedores()
    idFornecedor = str(input("Digite o ID do fornecedor que deseja deletar: "))

    fornecedor = buscarIdFornecedor(idFornecedor)

    while(fornecedor is None):
        print("Fornecedor com ID fornecido não encontrado")
        idFornecedor = str(input("Por favor, digite o ID do produto que deseja deletar: "))
        fornecedor = buscarIdFornecedor(idFornecedor)
    
    print("-"*50)
    print("PRODUTO SELECIONADO")
    print()
    print(f"Nome: {fornecedor['Nome']}\nCNPJ/CPF: {fornecedor['CNPJ/CPF']}\nE-mail: {fornecedor['E-mail']}\nTelefone: {fornecedor['Telefone']}\nCEP: {fornecedor['CEP']}\nEndereço: {fornecedor['Endereço']}\nCidade: {fornecedor['Cidade']}\nEstado: {fornecedor['Estado']}\nPaís: {fornecedor['País']} ")
    print()
    print("-"*50)
    print()

    fornecedores = carregar_bancoDadosFornecedor()

    for i, p in enumerate(fornecedores):
        if (p['Id']==idFornecedor):
            del fornecedores[i]
            break
    
    salvarArquivoFornecedor(fornecedores)
    
    print()
    print("FORNECEDOR EXCLUIDO COM SUCESSO!")

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

# Começo do CRUD Categorias

class Categoria:      
    def __init__(self, id,nome, descricao):   
        self.id = id   
        self.nome = nome
        self.descricao = descricao        

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao  
        }

class categoriaCRUD:
    def __init__(self, arquivo='categorias.json'):
        self.arquivo = arquivo  
        self.categorias = self.carregar_categorias() or []

    def carregar_categorias(self):   
        if os.path.exists(self.arquivo):
            with open(self.arquivo, 'r', encoding="utf-8") as f:
                if os.path.getsize(self.arquivo) > 0:  
                    return [Categoria(**d) for d in json.load(f)]
        return []

    def salvar_categorias(self):
        with open(self.arquivo, 'w', encoding="utf-8") as f:
            json.dump([categoria.to_dict() for categoria in self.categorias], f, indent = 4, ensure_ascii=False)

    def cadastrar_categoria(self, categoria_id, nome, descricao):
        nova_categoria = Categoria(categoria_id, nome, descricao)
        self.categorias.append(nova_categoria)
        self.salvar_categorias()  
        print(f'Categoria {nome} cadastrado com sucesso!')

    def ler_categorias(self):
        if not self.categorias:
            print("Nenhuma categoria cadastrada.")
            return
        for categoria in self.categorias:   
            print(f'ID: {categoria.id}, Nome: {categoria.nome}, Descrição: {categoria.descricao}')

    def atualizar_categoria(self, categoria_id, nome, descricao):
        for categoria in self.categorias:
            if categoria.id == categoria_id: 
                categoria.nome = nome
                categoria.descricao = descricao
                self.salvar_categorias()
                print(f'Categoria com ID {categoria_id} atualizado com sucesso!')
                return
        print(f'Categoria com ID {categoria_id} não encontrado.')

    def excluir_categoria(self, categoria_id):
        for categoria in self.categorias:
            if categoria.id == categoria_id:
                self.categorias.remove(categoria)
                self.salvar_categorias()
                print(f'Categoria com ID {categoria_id} excluído com sucesso!')
                return
        print(f'Categoria com ID {categoria_id} não encontrado.')

# Começo CRUD Estoque

class Estoque:      
    def __init__(self, id, dataEntrada, idProduto, quantidade, precoCompraU):  
        self.id = id
        self.dataEntrada = dataEntrada
        self.idProduto = idProduto
        self.quantidade = quantidade
        self.precoCompraU = precoCompraU

    def to_dict(self):  
        return {
            'id': self.id,
            'Data de Entrada': self.dataEntrada,
            'id do Produto': self.idProduto,
            'Quantidade': self.quantidade,
            'Preço Unitário do Produto': self.precoCompraU
        }

class EstoqueCRUD:
    def __init__(self, arquivo='estoque.json'):
        self.arquivo = arquivo  
        self.estoques = self.carregar_estoques() or []

    def carregar_estoques(self):   
        if os.path.exists(self.arquivo):
            with open(self.arquivo, 'r', encoding="utf-8") as f:
                if os.path.getsize(self.arquivo) > 0:  
                    dados = json.load(f)
                    estoques = []
                    for d in dados:
                        # Renomeando as chaves para corresponder aos parâmetros do __init__
                        d_renomeado = {
                            'id': d.get('id'),
                            'dataEntrada': d.get('Data de Entrada'),
                            'idProduto': d.get('id do Produto'),
                            'quantidade': d.get('Quantidade'),
                            'precoCompraU': d.get('Preço Unitário do Produto')
                        }
                        estoques.append(Estoque(**d_renomeado))
                    return estoques
        return []
        
    def salvar_estoques(self):
        with open(self.arquivo, 'w', encoding="utf-8") as f:
            json.dump([estoque.to_dict() for estoque in self.estoques], f, indent = 4, ensure_ascii=False)  

    def cadastrar_estoque(self, id, dataEntrada, idProduto, quantidade, precoCompraU):
        novo_estoque = Estoque(id, dataEntrada, idProduto, quantidade, precoCompraU)
        self.estoques.append(novo_estoque)
        self.salvar_estoques()  
        print(f'Produto {idProduto} cadastrado no estoque com sucesso com data de entrada {dataEntrada}')

    def listar_estoques(self):
        if not self.estoques:
            print("Nenhum estoque de produtos cadastrado.")
            return
        for estoque in self.estoques:  
            print(f'ID: {estoque.id}, Data de Entrada: {estoque.dataEntrada}, id do Produto: {estoque.idProduto}, Quantidade: {estoque.quantidade}, Preço Unitário do Produto: {estoque.precoCompraU}')

    def atualizar_estoque(self, estoque_id, dataEntrada, idProduto, quantidade, precoCompraU):
        for estoque in self.estoques:
            if estoque.id == estoque_id:
                estoque.dataEntrada = dataEntrada  
                estoque.idProduto = idProduto
                estoque.quantidade = quantidade
                estoque.precoCompraU = precoCompraU
                self.salvar_estoques()
                print(f'Estoque com ID {estoque_id} atualizado com sucesso!')
                return
        print(f'Estoque com ID {estoque_id} não encontrado.')

    def excluir_estoque(self, estoque_id):
        for estoque in self.estoques:
            if estoque.id == estoque_id:
                self.estoques.remove(estoque)
                self.salvar_estoques()
                print(f'Estoque com ID {estoque_id} excluído com sucesso!')
                return
        print(f'Estoque com ID {estoque_id} não encontrado.')

# Menu inicial do programa

def menu():
    print("-"*50)
    print("\n--- Sistema de Gerenciamento de Estoque ---")
    print("\n1. Gerenciar Produtos")
    print("2. Gerenciar Fornecedores")
    print("3. Gerenciar Usuários")
    print("4. Gerenciar Categorias")
    print("5. Gerenciar Estoque")
    print("6. Sair\n")
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

# Menu do Gerenciamente de Fornecedor

def menuFornecedor():
    print("-"*50)
    print("\n--- MENU GERENCIAMENTO DE FORNECEDOR ---")
    print("\n1. Adicionar Fornecedores")
    print("2. Listar Fornecedores")
    print("3. Atualizar Fornecedores")
    print("4. Excluir Fornecedores")
    print("5. Voltar ao Menu Anterior\n")
    print("-"*50)
    print()

# Menu do Gerenciamente de Usuário

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

# Menu de Gerenciamento de Categorias

def menuCategorias():
    print("-"*50)
    print("\n--- MENU DE CATEGORIAS ---")
    print("\n1. Cadastrar Categoria")
    print("2. Listar Categorias")
    print("3. Atualizar Categorias")
    print("4. Excluir Categoria")
    print("5. Sair")
    print("-"*50)
    print()

# Menu de Gerenciamento de Estoque

def menuEstoque():
    print("-"*50)
    print("\n--- MENU DE ESTOQUE ---")
    print("\n1. Cadastrar Estoque")
    print("2. Listar Estoque")
    print("3. Atualizar Estoque")
    print("4. Excluir Estoque")
    print("5. Sair")
    print("-"*50)
    print()

def main():

    while True:
        menu()
        opcaoInicial = int(input("Informe a opção desejada: "))
        
        while ((opcaoInicial<1) | (opcaoInicial>6)):
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
                while True:
                    menuFornecedor()
                    opcaoFornecedor = int(input("Informe a opção desejada: "))

                    while ((opcaoFornecedor<1) | (opcaoFornecedor>5)):
                        print()
                        print("Por favor digite um valor válido para navegar no menu")
                        opcaoFornecedor = int(input("Informe a opção desejada: "))
                        print()

                    match(opcaoFornecedor):
                        case 1:
                            print("\n1. Adicionar Fornecedores")
                            adicionarFornecedor()
                            print()
                        
                        case 2:
                            print("\n2. Listar Fornecedores")
                            listarFornecedores()
                            print()

                        case 3:
                            print("\n3. Atualizar Fornecedores")
                            atualizarFornecedor()
                            print()
                        
                        case 4:
                            print("\n4. Excluir Fornecedores")
                            deletarFornecedor()
                            print()
                        
                        case 5:
                            print("\n5. Voltar ao Menu Anterior")
                            print()
                            break  
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
                            id = str(uuid.uuid4().int)[:4]
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
                crud = categoriaCRUD()
                while True:
                    menuCategorias()
                    opcaoCategoria = int(input("Informe a opção desejada: "))

                    while ((opcaoCategoria<1) | (opcaoCategoria>5)):
                        print()
                        print("Por favor digite um valor válido para navegar no menu")
                        opcaoCategoria = int(input("Informe a opção desejada: "))
                        print()
                    
                    match (opcaoCategoria):
                        case 1:
                            categoria_id = str(uuid.uuid4().int)[:4] 
                            nome = input("Nome: ")
                            descricao = input("Descrição: ")
                            crud.cadastrar_categoria(categoria_id, nome, descricao)
                        
                        case 2:
                            crud.ler_categorias()
                        
                        case 3: 
                            categoria_id = str(input("ID da Categoria a ser atualizada: "))
                            nome = input("Novo Nome: ")
                            descricao = input("Nova descrição da categoria: ")
                            crud.atualizar_categoria(categoria_id, nome, descricao)
                        
                        case 4:
                            categoria_id = str(input("ID da categoria a ser excluída: "))
                            crud.excluir_categoria(categoria_id)

                        case 5:
                            print("Saindo do sistema de usuários...")
                            break

            case 5:
                crud = EstoqueCRUD()
                while True:
                    menuEstoque()
                    opcaoEstoque = int(input("Informe a opção desejada: "))

                    while ((opcaoEstoque<1) | (opcaoEstoque>5)):
                        print()
                        print("Por favor digite um valor válido para navegar no menu")
                        opcaoEstoque = int(input("Informe a opção desejada: "))
                        print()
                    
                    match(opcaoEstoque):
                        case 1:
                            id = str(uuid.uuid4().int)[:4]

                            dataEntrada = input("Digite a data de entrada (dd/mm/yyyy): ")

                            listarProdutos()
                            print()

                            idProduto = input("ID do Produto: ")

                            # Verifica se o ID do produto foi digitado corretamente
                            produto = buscarIdProduto(idProduto)

                            while (produto is None):
                                print("Produto com ID fornecido não encontrado")
                                idProduto = str(input("Por favor, digite o ID do produto que deseja adicionar ao estoque: "))
                                produto = buscarIdProduto(idProduto)
                                print()

                            quantidade = input("Quantidade: ")
                            precoCompraU = input("Preço Unitário do Produto: ")
                            crud.cadastrar_estoque(id, dataEntrada, idProduto, quantidade, precoCompraU)
                        
                        case 2:
                            crud.listar_estoques()
                        
                        case 3:
                            estoque_id = str(input("ID do estoque a ser atualizado: "))
                            dataEntrada = input("Digite a nova data de entrada (dd/mm/yyyy): ")
                            idProduto = input("Novo ID do Produto: ")
                            quantidade = input("Quantidade atualizada: ")
                            precoCompraU = input("Preço Unitário do Produto: ")
                            crud.atualizar_estoque(estoque_id, dataEntrada, idProduto, quantidade, precoCompraU)
                        
                        case 4:
                            estoque_id = str(input("ID do Estoque a ser excluído: "))
                            crud.excluir_estoque(estoque_id)
                        
                        case 5:
                            print("Saindo do sistema de estoque...")
                            break
            case 6:
                break
                    
         
    print("Programa Finalizado")
                              
if __name__ == "__main__":
    main()



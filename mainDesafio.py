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
    def __init__(self, id,nome):   
        self.id = id   
        self.nome = nome        

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome 
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
            print(f'ID: {categoria.id}, Nome: {categoria.nome}')

    def atualizar_categoria(self, categoria_id, nome):
        for categoria in self.categorias:
            if categoria.id == categoria_id: 
                categoria.nome = nome
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
    def __init__(self, id, idProduto, quantidade=0):

        self.id = id
        self.idProduto = idProduto
        self.quantidade = quantidade
        self.total_quantidade = quantidade
    

    def to_dict(self):  
        return {
            'id': self.id,
            'id do Produto': self.idProduto,
            'Quantidade': self.quantidade
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
                            'idProduto': d.get('id do Produto'),
                            'quantidade': d.get('Quantidade')
                        }
                        estoques.append(Estoque(**d_renomeado))
                    return estoques
        return []
        
    def salvar_estoques(self):
        with open(self.arquivo, 'w', encoding="utf-8") as f:
            json.dump([estoque.to_dict() for estoque in self.estoques], f, indent = 4, ensure_ascii=False)  

    def cadastrar_estoque(self, id, idProduto):
        novo_estoque = Estoque(id, idProduto)
        self.estoques.append(novo_estoque)
        self.salvar_estoques()  
        print(f'Produto {idProduto} cadastrado no estoque com sucesso!')

    def listar_estoques(self):
        if not self.estoques:
            print("Nenhum estoque de produtos cadastrado.")
            return
        for estoque in self.estoques:
            print(f'ID: {estoque.id}, id do Produto: {estoque.idProduto}, Quantidade: {estoque.quantidade}')

    def atualizar_estoque(self, estoque_id, idProduto):
        for estoque in self.estoques:
            if estoque.id == estoque_id:  
                estoque.idProduto = idProduto
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
    
    def realizar_movimentacao_saida(self, idEstoque, quantidade_retirada):
        # Subtrai a quantidade do estoque especificado e salva o arquivo JSON.
        for estoque in self.estoques:
            if estoque.id == idEstoque:
                if estoque.quantidade >= quantidade_retirada:
                    estoque.quantidade -= quantidade_retirada
                    self.salvar_estoques()
                    print(f"{quantidade_retirada} unidades retiradas. Nova quantidade de estoque (ID {idEstoque}): {estoque.quantidade}")
                    return True
                else:
                    print("Quantidade insuficiente no estoque.")
                    return False
        print("Estoque não encontrado.")
        return False

    
    def realizar_movimentaçao_entrada(self, idEstoque, quantidade_adicionada):
        for estoque in self.estoques:
            if (estoque.id==idEstoque):
                estoque.quantidade += quantidade_adicionada
                self.salvar_estoques()
                print(f"{quantidade_adicionada} unidades adicionadas. Nova quantidade de estoque (ID {idEstoque}): {estoque.quantidade}")
                return True
     
# Começo CRUD Movimentação de Entrada

class MovimentaçaoEntrada:
    def __init__(self, id, idEstoque, dataEntrada, quantidade):  
        self.id = id 
        self.idEstoque = idEstoque 
        self.dataEntrada = dataEntrada
        self.quantidade = quantidade
    
    def to_dict(self):  
        return {
            'id': self.id,
            'id de Estoque': self.idEstoque,
            'Data de Entrada': datetime.strftime(self.dataEntrada, "%d/%m/%Y"),
            'Quantidade': self.quantidade
        }

class MovimentaçaoEntradaCRUD:
    def __init__(self, estoqueCrud, arquivo='movimentaçaoEntrada.json'):
        self.estoqueCrud = estoqueCrud
        self.arquivo = arquivo  
        self.movimentaçoesEntrada = self.carregar_movimentaçoesEntrada() or []
    
    def carregar_movimentaçoesEntrada(self):   
        if os.path.exists(self.arquivo):
            with open(self.arquivo, 'r', encoding="utf-8") as f:
                if os.path.getsize(self.arquivo) > 0:  
                    dados = json.load(f)
                    movimentaçoesEntrada = []
                    for d in dados:
                        # Renomeando as chaves para corresponder aos parâmetros do __init__
                        d_renomeado = {
                            'id': d.get('id'),
                            'idEstoque': d.get('id de Estoque'),
                            'dataEntrada': datetime.strptime(d.get('Data de Entrada'), "%d/%m/%Y"),
                            'quantidade': d.get('Quantidade')
                        }
                        movimentaçoesEntrada.append(MovimentaçaoEntrada(**d_renomeado))
                    return movimentaçoesEntrada
        return []
    
    def salvar_movimentaçoesEntrada(self):
        with open(self.arquivo, 'w', encoding="utf-8") as f:
            json.dump([movimentaçaoEntrada.to_dict() for movimentaçaoEntrada in self.movimentaçoesEntrada], f, indent = 4, ensure_ascii=False)

    def cadastrar_movimentaçaoEntrada(self, id, idEstoque, dataEntrada, quantidade):
        if (self.estoqueCrud.realizar_movimentaçao_entrada(idEstoque, quantidade)):
            nova_movimentaçao = MovimentaçaoEntrada(id, idEstoque, dataEntrada, quantidade)
            self.movimentaçoesEntrada.append(nova_movimentaçao)
            self.salvar_movimentaçoesEntrada()  
            print(f'A movimentação de entrada {id} foi cadastrada com sucesso!')
        else:
            print("Falha ao cadastrar movimentação: quantidade insuficiente ou estoque não encontrado.")  

    def listar_movimentaçoesEntrada(self):
        if not self.movimentaçoesEntrada:
            print("Nenhuma movimentação de estoque cadastrada.")
            return
        for movimentaçaoEntrada in self.movimentaçoesEntrada:  
            print(f'ID: {movimentaçaoEntrada.id}, Id de Estoque: {movimentaçaoEntrada.idEstoque}, Data de Entrada: {movimentaçaoEntrada.dataEntrada}, Quantidade: {movimentaçaoEntrada.quantidade}')

    def atualizar_movimentaçaoEntrada(self, movimentaçao_id, idEstoque, dataEntrada, quantidade):
        for movimentaçaoEntrada in self.movimentaçoesEntrada:
            if movimentaçaoEntrada.id == movimentaçao_id:
                quantidade_original = movimentaçaoEntrada.quantidade

                # Etapa 2: Reverte o efeito da quantidade original no estoque
                self.estoqueCrud.realizar_movimentacao_saida(idEstoque, quantidade_original)

                # Atualiza os dados da movimentação
                movimentaçaoEntrada.idEstoque = idEstoque  
                movimentaçaoEntrada.dataEntrada = dataEntrada
                movimentaçaoEntrada.quantidade = quantidade

                # Etapa 4: Aplica a nova quantidade no estoque
                if not self.estoqueCrud.realizar_movimentaçao_entrada(idEstoque, quantidade):
                    print(f"Falha ao aplicar nova quantidade ao estoque (ID {idEstoque}).")
                    return
                
                # Salva as alterações no arquivo JSON
                self.salvar_movimentaçoesEntrada()
                print(f'Movimentação de entrada com ID {movimentaçao_id} atualizada com sucesso!')
                return
        print(f'Movimentação de entrada com ID {movimentaçao_id} não encontrada.')
    
    def excluir_movimentaçaoEntrada(self, movimentaçao_id):
        for movimentaçaoEntrada in self.movimentaçoesEntrada:
            if movimentaçaoEntrada.id == movimentaçao_id:
                self.movimentaçoesEntrada.remove(movimentaçaoEntrada)
                self.salvar_movimentaçoesEntrada()
                print(f'Movimentção de Entrada com ID {movimentaçao_id} excluído com sucesso!')
                return
        print(f'Movimentção de Entrada com ID {movimentaçao_id} não encontrado.')

# Começo CRUD Movimentação de Saída

class Movimentaçao:
    def __init__(self, id, idEstoque, dataSaida, quantidade, destino):  
        self.id = id 
        self.idEstoque = idEstoque 
        self.dataSaida = dataSaida
        self. quantidade = quantidade
        self.destino = destino

    def to_dict(self):  
        return {
            'id': self.id,
            'id de Estoque': self.idEstoque,
            'Data de Saída': datetime.strftime(self.dataSaida, "%d/%m/%Y"),
            'Quantidade': self.quantidade,
            'Destino': self.destino
        }

class MovimentaçaoCRUD:
    def __init__(self, estoqueCrud, arquivo='movimentaçao.json'):
        self.estoqueCrud = estoqueCrud
        self.arquivo = arquivo  
        self.movimentaçoes = self.carregar_movimentaçoes() or []

    def carregar_movimentaçoes(self):   
        if os.path.exists(self.arquivo):
            with open(self.arquivo, 'r', encoding="utf-8") as f:
                if os.path.getsize(self.arquivo) > 0:  
                    dados = json.load(f)
                    movimentaçoes = []
                    for d in dados:
                        # Renomeando as chaves para corresponder aos parâmetros do __init__
                        d_renomeado = {
                            'id': d.get('id'),
                            'idEstoque': d.get('id de Estoque'),
                            'dataSaida': datetime.strptime(d.get('Data de Saída'), "%d/%m/%Y"),
                            'destino': d.get('Destino')
                        }
                        movimentaçoes.append(Movimentaçao(**d_renomeado))
                    return movimentaçoes
        return []

    def salvar_movimentaçoes(self):
        with open(self.arquivo, 'w', encoding="utf-8") as f:
            json.dump([movimentaçao.to_dict() for movimentaçao in self.movimentaçoes], f, indent = 4, ensure_ascii=False)  

    def cadastrar_movimentaçao(self, id, idEstoque, quantidade, dataSaida, destino):
        if (self.estoqueCrud.realizar_movimentacao_saida(idEstoque, quantidade)):
            nova_movimentaçao = Movimentaçao(id, idEstoque, dataSaida, quantidade, destino)
            self.movimentaçoes.append(nova_movimentaçao)
            self.salvar_movimentaçoes()  
            print(f'A movimentação {id} foi cadastrada com sucesso!')
        else:
            print("Falha ao cadastrar movimentação de saída: quantidade insuficiente ou estoque não encontrado.")
    
    def listar_movimentaçoes(self):
        if not self.movimentaçoes:
            print("Nenhuma movimentação de saída cadastrada.")
            return
        for movimentaçao in self.movimentaçoes:  
            print(f'ID: {movimentaçao.id}, Id de Estoque: {movimentaçao.idEstoque}, Data de Saída: {movimentaçao.dataSaida}, Quantidade: {movimentaçao.quantidade} Destino: {movimentaçao.destino}')

    def atualizar_movimentaçao(self, movimentaçao_id, idEstoque, dataSaida, quantidade, destino):
        for movimentaçao in self.movimentaçoes:
            if movimentaçao.id == movimentaçao_id:

                # Recupera a quantidade original
                quantidade_original = movimentaçao.quantidade

                # Reverte o efeito da quantidade original no estoque
                self.estoqueCrud.realizar_movimentaçao_entrada(idEstoque, quantidade_original)      

                movimentaçao.idEstoque = idEstoque  
                movimentaçao.dataSaida = dataSaida
                movimentaçao.quantidade = quantidade
                movimentaçao.destino = destino

                # Aplica a nova quantidade no estoque
                if not self.estoqueCrud.realizar_movimentacao_saida(idEstoque, quantidade):
                    print(f"Falha ao aplicar nova quantidade ao estoque (ID {idEstoque}).")
                    return

                self.salvar_movimentaçoes()
                print(f'Movimentação de saída com ID {movimentaçao_id} atualizada com sucesso!')
                return
        print(f'Estoque com ID {movimentaçao_id} não encontrado.')

    def excluir_movimentaçao(self, movimentaçao_id):
        for movimentaçao in self.movimentaçoes:
            if movimentaçao.id == movimentaçao_id:
                self.movimentaçoes.remove(movimentaçao)
                self.salvar_movimentaçoes()
                print(f'Movimentção de Saída com ID {movimentaçao_id} excluído com sucesso!')
                return
        print(f'Movimentção de Saída com ID {movimentaçao_id} não encontrado.')

# Menu inicial do programa

def menu():
    print("-"*50)
    print("\n--- Sistema de Gerenciamento de Estoque ---")
    print("\n1. Gerenciar Produtos")
    print("2. Gerenciar Fornecedores")
    print("3. Gerenciar Usuários")
    print("4. Gerenciar Categorias")
    print("5. Gerenciar Estoque")
    print("6. Gerenciar Movimentação de Sáida")
    print("7. Gerenciar Movimentação de Entrada")
    print("8. Sair\n")
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

# Menu de Gerenciamento de Movimentação

def menuMovimentação():
    print("-"*50)
    print("\n--- MENU DE MOVIMENTAÇÃO ---")
    print("\n1. Cadastrar Movimentação")
    print("2. Listar Movimentação")
    print("3. Atualizar Movimentação")
    print("4. Excluir Movimentação")
    print("5. Sair")
    print("-"*50)
    print()

# Menu de Gerenciamento de Movimentação de Entrada

def menuMovimentaçãoEntrada():
    print("-"*50)
    print("\n--- MENU DE MOVIMENTAÇÃO ---")
    print("\n1. Cadastrar Movimentação de Entrada")
    print("2. Listar Movimentação de Entrada")
    print("3. Atualizar Movimentação de Entrada")
    print("4. Excluir Movimentação de Entrada")
    print("5. Sair")
    print("-"*50)
    print()

def main():

    while True:
        menu()
        opcaoInicial = int(input("Informe a opção desejada: "))
        
        while ((opcaoInicial<1) | (opcaoInicial>8)):
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
                            crud.cadastrar_categoria(categoria_id, nome)
                        
                        case 2:
                            crud.ler_categorias()
                        
                        case 3: 
                            categoria_id = str(input("ID da Categoria a ser atualizada: "))
                            nome = input("Novo Nome: ")
                            crud.atualizar_categoria(categoria_id, nome)
                        
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

                            crud.cadastrar_estoque(id, idProduto)
                        
                        case 2:
                            crud.listar_estoques()
                        
                        case 3:
                            crud.listar_estoques()
                            estoque_id = str(input("ID do estoque a ser atualizado: "))
                            idProduto = input("Novo ID do Produto: ")
                            crud.atualizar_estoque(estoque_id, idProduto)
                        
                        case 4:
                            crud.listar_estoques()
                            estoque_id = str(input("ID do Estoque a ser excluído: "))
                            crud.excluir_estoque(estoque_id)
                        
                        case 5:
                            print("Saindo do sistema de estoque...")
                            break
            case 6:
                crudE = EstoqueCRUD()
                crud = MovimentaçaoCRUD(crudE)
                while True:
                    menuMovimentação()
                    opcaoMovimentaçao = int(input("Informe a opção desejada: "))

                    while ((opcaoMovimentaçao<1) | (opcaoMovimentaçao>5)):
                        print()
                        print("Por favor digite um valor válido para navegar no menu")
                        opcaoMovimentaçao = int(input("Informe a opção desejada: "))
                        print()
                    
                    match (opcaoMovimentaçao):
                        case 1:
                            id = str(uuid.uuid4().int)[:4]

                            data = input("Digite a data de saída (dd/mm/yyyy): ")
                            dataSaida = datetime.strptime(data, "%d/%m/%Y")

                            crudE.listar_estoques()
                            print()

                            idEstoque = input("Digite o id do estoque que deseja fazer a mavimentação: ")
                            quantidade = int(input("Digite a quantidade de produtos do estoque que irá retirar: "))
                            destino = input("Digite o destino desses produtos: ")

                            crud.cadastrar_movimentaçao(id, idEstoque, quantidade, dataSaida, destino)
                        
                        case 2:
                            crud.listar_movimentaçoes()
                        
                        case 3:
                            crud.listar_movimentaçoes()
                            movimentaçao_id = str(input("ID da movimentação a ser atualizada: "))
                            data = input("Digite a nova data de saída (dd/mm/yyyy): ")
                            dataSaida = datetime.strptime(data, "%d/%m/%Y")
                            idEstoque = input("Novo ID do Estoque: ")
                            quantidade = int(input("Digite a nova quantidade: "))
                            destino = input("Digite o novo destino do produto: ")
                            crud.atualizar_movimentaçao(movimentaçao_id, idEstoque, dataSaida, quantidade, destino)

                        case 4:
                            crud.listar_movimentaçoes()
                            movimentaçao_id = str(input("ID da movimentação a ser excluído: "))
                            crud.excluir_movimentaçao(movimentaçao_id)

                        case 5:
                            print("Saindo do sistema de movimentação...")
                            break              

            case 7:
                crudE = EstoqueCRUD()
                crud = MovimentaçaoEntradaCRUD(crudE)
                while True:
                    menuMovimentaçãoEntrada()
                    opcaoMovimentaçaoEntrada = int(input("Informe a opção desejada: "))

                    while ((opcaoMovimentaçaoEntrada<1) | (opcaoMovimentaçaoEntrada>5)):
                        print()
                        print("Por favor digite um valor válido para navegar no menu")
                        opcaoMovimentaçaoEntrada = int(input("Informe a opção desejada: "))
                        print()

                    match(opcaoMovimentaçaoEntrada):
                        case 1:
                            id = str(uuid.uuid4().int)[:4]

                            data = input("Digite a data de Entrada (dd/mm/yyyy): ")
                            dataEntrada = datetime.strptime(data, "%d/%m/%Y")

                            crudE.listar_estoques()
                            print()

                            idEstoque = input("Digite o id do estoque que deseja fazer a mavimentação de entrada: ")
                            quantidade = int(input("Digite a quantidade de produtos do estoque que irá adicionar: "))
                            crud.cadastrar_movimentaçaoEntrada(id, idEstoque, dataEntrada, quantidade)

                        case 2:
                            crud.listar_movimentaçoesEntrada()

                        case 3:
                            crud.listar_movimentaçoesEntrada()
                            movimentaçao_id = str(input("ID da movimentação de entrada a ser atualizada: "))
                            data = input("Digite a nova data de entrada (dd/mm/yyyy): ")
                            dataEntrada = datetime.strptime(data, "%d/%m/%Y")
                            idEstoque = input("Novo ID do Estoque: ")
                            quantidade = int(input("Digite a nova quantidade: "))
                            crud.atualizar_movimentaçaoEntrada(movimentaçao_id, idEstoque, dataEntrada, quantidade)

                        case 4:
                            crud.listar_movimentaçoesEntrada()
                            movimentaçao_id = str(input("ID da movimentação de entrada a ser excluído: "))
                            crud.excluir_movimentaçaoEntrada(movimentaçao_id)

                        case 5:
                            break
            case 8:
                break
                                      
    print("Programa Finalizado")
                              
if __name__ == "__main__":
    main()



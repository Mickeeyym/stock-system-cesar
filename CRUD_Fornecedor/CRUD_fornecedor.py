import json
import os
from time import sleep
import uuid

arquivo = os.path.join(os.path.dirname(__file__), 'arquivo_fornecedor.json')

def carregar_bancoDados():
    # Verifica se o arquivo existe, se não existir, cria um arquivo com lista vazia
    if not os.path.exists(arquivo):
        with open(arquivo, 'w', encoding="utf-8") as f:
            json.dump([], f, indent=4)
    
    # Carrega o conteúdo do arquivo
    with open(arquivo, 'r', encoding="utf-8") as f:
        return json.load(f)

class Fornecedor:

    def __init__(self, nome, cnpj_cpf, email, telefone, cep, endereço, cidade, estado, país):
        self.id = str(uuid.uuid4()) #Gerar id único
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

    fornecedores = carregar_bancoDados()
    for p in fornecedores:
        if ((p['Nome']==nome) or (p['CNPJ/CPF']==cnpj_cpf)):
            return True
    return False

def buscarIdFornecedor(idFornecedor):
    fornecedores = carregar_bancoDados()
    for p in fornecedores:
        if (p['Id']==idFornecedor):
            return p
    return None

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

    fornecedores = carregar_bancoDados()

    for i, p in enumerate(fornecedores):
        if (p['Id']==idFornecedor):
            fornecedores[i]=fornecedor
            break
    
    with open(arquivo, 'w') as f:
        json.dump(fornecedores, f, indent=4, ensure_ascii=False)
    
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

    fornecedores = carregar_bancoDados()

    for i, p in enumerate(fornecedores):
        if (p['Id']==idFornecedor):
            del fornecedores[i]
            break
    
    with open(arquivo, 'w', encoding="utf-8") as f:
        json.dump(fornecedores, f, indent=4, ensure_ascii=False)
    
    print()
    print("FORNECEDOR EXCLUIDO COM SUCESSO!")

    
# Função para listar os Fornecedores existentes

def listarFornecedores():

    fornecedores = carregar_bancoDados()

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
            print("-"*50)

    else:
        print("NENHUM FORNECEDOR CADASTRADO")


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

    fornecedorLista = carregar_bancoDados()  

    fornecedorLista.append(fornecedor.toDictionary())

    # Salva a lista atualizada no arquivo
    with open(arquivo, 'w', encoding="utf-8") as f:
        json.dump(fornecedorLista, f, indent=4, ensure_ascii=False)

    print("FORNECEDOR ADICIONADO COM SUCESSO!")
     
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

def main():

    while True:
        menu()
        opcaoInicial = int(input("Informe a opção desejada: "))
        match (opcaoInicial):
            case 1:
                print("Em desenvolvimento")
            case 2:
                while True:
                    menuFornecedor()
                    opcaoFornecedor = int(input("Informe a opção desejada: "))
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
                print("Em desenvolvimento")
            case 4:
                break
            
    
    print("Programa Finalizado")
                              

if __name__ == "__main__":
    main()



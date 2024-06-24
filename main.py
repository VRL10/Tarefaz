import uuid
from abc import ABC, abstractmethod
from datetime import datetime

# Definindo listas globais
usuarios_comuns = []
tarefas = []

# Classe base das classes Usuario_comum e Usuario_adm
class Usuario(ABC):
    def __init__(self, usuario, senha):
        self._usuario = usuario
        self._senha = senha

    @property
    def usuario(self):
        return self._usuario

    @property
    def senha(self):
        return self._senha

    @abstractmethod
    def autenticar(self, usuario_digitado, senha_digitada):
        pass

# Cadastra e Autentica os usuários comuns
class Usuario_comum(Usuario):
    def __init__(self, usuario, senha):
        super().__init__(usuario, senha)
        self._id = uuid.uuid4()

    @property
    def id(self):
        return self._id

    def autenticar(self, usuario_digitado, senha_digitada):
        if usuario_digitado == self._usuario and senha_digitada == self._senha:
            print('O acesso foi feito com sucesso')
            return True
        else:
            print('O acesso foi negado!')
            return False

# Por enquanto, não irei fazer nada nessa classe, apenas direi se conseguiu ou não autenticar.(O usuário ADM foi colocado como um pré definido)
class Usuario_adm(Usuario):
    def __init__(self, usuario='victor', senha='victor'):
        super().__init__(usuario, senha)
        self._id = uuid.uuid4()

    @property
    def id(self):
        return self._id

    def autenticar(self, usuario_digitado, senha_digitada):
        if usuario_digitado == self._usuario and senha_digitada == self._senha:
            print('O acesso foi feito com sucesso')
            return True
        else:
            print('O acesso foi negado!')
            return False

# Cadastra as tarefas para os respectivos usuários comuns e também as altera
class Tarefas:
    importancias = ['Baixa', 'Normal', 'Alta', 'Urgente']
    prioridades = ['Baixa', 'Média', 'Alta']
    status_validos = ['Em andamento', 'Concluída', 'Cancelada']

    def __init__(self, titulo, descricao, data_prazo, importancia, prioridade, status):
        self._titulo = titulo
        self._descricao = descricao
        self._data_prazo = datetime.strptime(data_prazo, '%d-%m-%Y')
        self.importancia = importancia  # Atributo privado acessado por setter
        self.prioridade = prioridade  # Atributo privado acessado por setter
        self.status = status  # Atributo privado acessado por setter
        self._id_tarefa = uuid.uuid4()
        self._id_usuario = None

    def cadastrar_tarefa_ao_usuario(self, id_usuario):
        self._id_usuario = id_usuario

    @property
    def id_tarefa(self):
        return self._id_tarefa

    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self, value):
        self._titulo = value

    @property
    def descricao(self):
        return self._descricao

    @descricao.setter
    def descricao(self, value):
        self._descricao = value

    @property
    def data_prazo(self):
        return self._data_prazo

    @data_prazo.setter
    def data_prazo(self, value):
        self._data_prazo = datetime.strptime(value, '%d-%m-%Y')

    @property
    def importancia(self):
        return self._importancia

    @importancia.setter
    def importancia(self, value):
        if value in self.importancias:
            self._importancia = value
        else:
            raise ValueError('Importância inválida.')

    @property
    def prioridade(self):
        return self._prioridade

    @prioridade.setter
    def prioridade(self, value):
        if value in self.prioridades:
            self._prioridade = value
        else:
            raise ValueError('Prioridade inválida.')

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value in self.status_validos:
            self._status = value
        else:
            raise ValueError('Status inválido.')


# Classe responsável por chamar as outras classes, quando precisar! Ela basicamente tem as funções compativeis com as opções do Menu.
# Quando se escolhe uma opção faz as perguntas e chama as outras classes
class Sistema:
    def __init__(self):
        self.admin = Usuario_adm()

    def cadastrar_usuario_comum(self):
        usuario = input("Digite o nome do usuário: ")
        senha = input("Digite a senha: ")
        novo_usuario = Usuario_comum(usuario, senha)
        usuarios_comuns.append(novo_usuario)
        print('Usuario Comum foi adicionado com sucesso!')

    def logar_usuario_adm(self):
        usuario_digitado = input("Digite o nome do usuário: ")
        senha_digitada = input("Digite a senha: ")
        if self.admin.autenticar(usuario_digitado, senha_digitada):
            self.menu_adm()
        else:
            print("Falha na autenticação do administrador.")

    def logar_usuario_comum(self):
        usuario_digitado = input("Digite o nome do usuário: ")
        senha_digitada = input("Digite a senha: ")
        for usuario in usuarios_comuns:
            if usuario.autenticar(usuario_digitado, senha_digitada):
                self.menu_usuario(usuario)
                return
        print("Falha na autenticação do usuário comum.")

    def cadastrar_tarefa(self, id_usuario):
        titulo = input("Digite o título da tarefa: ")
        descricao = input("Digite a descrição da tarefa: ")
        data_prazo = input("Digite a data de prazo (dd-mm-aaaa): ")
        importancia = input("Digite a importância (Baixa, Normal, Alta, Urgente): ")
        prioridade = input("Digite a prioridade (Baixa, Média, Alta): ")
        status = input("Digite o status (Em andamento, Concluída, Cancelada): ")

        try:
            nova_tarefa = Tarefas(titulo, descricao, data_prazo, importancia, prioridade, status)
            nova_tarefa.cadastrar_tarefa_ao_usuario(id_usuario)
            tarefas.append(nova_tarefa)
            print("Tarefa cadastrada com sucesso!")
        except ValueError as e:
            print(f"Erro ao cadastrar a tarefa: {e}")

    def menu_adm(self):
        while True:
            opcao = input('''----- Menu Administrador -----
OP1 - Cadastrar Usuário Comum
OP2 - Sair
Digite a opção desejada: ''')
            if opcao == 'OP1':
                self.cadastrar_usuario_comum()
            elif opcao == 'OP2':
                break
            else:
                print("Opção inválida, tente novamente.")

    def menu_usuario(self, usuario):
        nome_usuario = usuario.usuario
        while True:
            opcao = input(f'''Bem-vindo usuário comum {nome_usuario}
----- Digite a opção desejada -----
OP1 - Cadastrar Tarefa
OP2 - Visualizar Tarefas do Usuário
OP3 - Alterar Atributos da Tarefa
OP4 - Sair
''')
            if opcao == 'OP1':
                self.cadastrar_tarefa(usuario.id)
            elif opcao == 'OP2':
                self.visualizar_tarefas(usuario.id)
            elif opcao == 'OP3':
                self.alterar_tarefa(usuario.id)
            elif opcao == 'OP4':
                break
            else:
                print("Opção inválida, tente novamente.")

    def visualizar_tarefas(self, id_usuario):
        tarefas_usuario = [tarefa for tarefa in tarefas if tarefa._id_usuario == id_usuario]
        if not tarefas_usuario:
            print("Nenhuma tarefa encontrada para este usuário.")
        else:
            for tarefa in tarefas_usuario:
                print(f"Título: {tarefa.titulo}, Descrição: {tarefa.descricao}, Data Prazo: {tarefa.data_prazo.strftime('%d-%m-%Y')}, Importância: {tarefa.importancia}, Prioridade: {tarefa.prioridade}, Status: {tarefa.status}")

    def alterar_tarefa(self, id_usuario):
        tarefas_usuario = [tarefa for tarefa in tarefas if tarefa._id_usuario == id_usuario]
        if not tarefas_usuario:
            print("Nenhuma tarefa encontrada para este usuário.")
        else:
            for i, tarefa in enumerate(tarefas_usuario, 1):
                print(f"{i} - Título: {tarefa.titulo}, Descrição: {tarefa.descricao}, Data Prazo: {tarefa.data_prazo.strftime('%d-%m-%Y')}, Importância: {tarefa.importancia}, Prioridade: {tarefa.prioridade}, Status: {tarefa.status}")
            escolha = int(input("Digite o número da tarefa que deseja alterar: "))
            if 1 <= escolha <= len(tarefas_usuario):
                tarefa_escolhida = tarefas_usuario[escolha - 1]
                atributo = input("Digite o atributo que deseja alterar (titulo, descricao, data_prazo, importancia, prioridade, status): ")
                novo_valor = input(f"Digite o novo valor para {atributo}: ")
                try:
                    setattr(tarefa_escolhida, atributo, novo_valor)
                    print("Atributo alterado com sucesso!")
                except ValueError as e:
                    print(f"Erro ao alterar o atributo: {e}")
                except AttributeError:
                    print("Atributo inválido.")

# Exemplo de uso:
sistema = Sistema()
while True:
    opcao = input('''----- Digite a opção desejada -----
OP1 - Logar com conta ADM
OP2 - Logar com Usuário comum
OP3 - Cadastrar Usuário Comum
OP4 - Sair
''')
    if opcao == 'OP1':
        sistema.logar_usuario_adm()
    elif opcao == 'OP2':
        sistema.logar_usuario_comum()
    elif opcao == 'OP3':
        sistema.cadastrar_usuario_comum()
    elif opcao == 'OP4':
        break
    else:
        print("Opção inválida, tente novamente.")

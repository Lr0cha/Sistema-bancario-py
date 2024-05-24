import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime
from pathlib import Path

ROOT_PATH = Path(__file__).parent #pegar o caminho da pasta

class ContasIterador:
    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self._index]
            return f"""\
            Agência:\t{conta.agencia}
            Número:\t\t{conta.numero}
            Titular:\t{conta.cliente.nome}
            Saldo:\t\tR$ {conta.saldo:.2f}
        """
        except IndexError:
            raise StopIteration
        finally:
            self._index += 1


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

    def excedeu_limite_transacao(self,conta):
        data_atual = datetime.now().strftime("%d/%m/%Y")
        transacoes = conta.historico.transacoes
        numero_transacoes_dia = 0
        for transacao in transacoes:
            data_transacao = datetime.strptime(transacao['data'], "%d/%m/%Y %H:%M")
            if data_transacao.strftime("%d/%m/%Y") == data_atual:
                numero_transacoes_dia += 1  
        if numero_transacoes_dia >= 10:
            return False 
        return True
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: ('{self.cpf}')>"

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property #encapsulamento
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n Operação falhou! Você não tem saldo suficiente.")

        elif valor > 0:
            self._saldo -= valor
            print("\nSaque realizado com sucesso! ")
            return True

        else:
            print(f"\n Operação falhou! O valor informado é inválido.")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\nDepósito realizado com sucesso!")
        else:
            print("\nOperação falhou! O valor informado é inválido.")
            return False

        return True
    


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print(f"\nOperação falhou! O valor do saque excede o limite.")

        elif excedeu_saques:
            print(f"\nOperação falhou! Número máximo de saques excedido.")

        else:
            return super().sacar(valor)

        return False
    
    def __repr__(self):
        return f"<{self.__class__.__name__}: ('{self.agencia}', '{self.numero}', '{self.cliente.nome}')>"

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            }
        )
    
    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if tipo_transacao is None or tipo_transacao.lower() == transacao["tipo"].lower():
                yield transacao



class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def menu():
    menu = """\n\n
    =================== MENU ===================
    Digite uma das opções:\n
    [D]\tDepositar
    [S]\tSacar
    [E]\tExtrato
    [NC]\tNova conta
    [LC]\tListar contas
    [NU]\tNovo usuário
    [F]\tFinalizar
    => """
    return input(textwrap.dedent(menu)).upper()

def log_transacao(func):
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        data_atual = datetime.now().strftime("Dia %d/%m/%Y às %H:%M")
        try:
            with open(ROOT_PATH /"log.txt", "a", encoding="utf-8") as arquivo:
                arquivo.write(
                    f"[{data_atual}] [Operação:{func.__name__.upper()}] [Executada com argumentos {args} e {kwargs}]\n"
                )
            print(f"{func.__name__.upper()}: {datetime.now().strftime("Dia %d/%m/%Y às %H:%M")}")
        except IOError as exc:
            print(f"Erro ao abrir o arquivo {exc}")
        except Exception as exc:
            print(f"Erro ao manipular o arquivo {exc}")
        return resultado
    return envelope


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n Cliente não possui conta!")
        return

    return cliente.contas[0] #acessa a primeira conta do cliente encontrada

@log_transacao
def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return
    conta = recuperar_conta_cliente(cliente)  # Recuperando a conta associada ao cliente
    if not conta:
        return
    valido = cliente.excedeu_limite_transacao(conta)
    if valido:
        valor = float(input("Informe o valor do depósito: "))
        transacao = Deposito(valor)  # Criando uma instância de transação de depósito
        cliente.realizar_transacao(conta, transacao)  # Realizando a transação de depósito
        return
    print("Limite diário de transações já foi atingido!")
    

@log_transacao
def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print(f"\nCliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)  # Recuperando a conta associada ao cliente
    if not conta:
        return
    valido = cliente.excedeu_limite_transacao(conta)
    if valido:
        valor = float(input("Informe o valor do saque: "))
        transacao = Saque(valor)  # Criando uma instância de transação de saque
        cliente.realizar_transacao(conta, transacao)  # Realizando a transação de saque
        return
    print("Limite diário de transações já foi atingido!")

@log_transacao
def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print(f"\nCliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)  # Recuperando a conta associada ao cliente
    if not conta:
        return

    print("\n================ EXTRATO ================")
    existe_transacao = False
    extrato = ""
    for transacao in conta.historico.gerar_relatorio():
            existe_transacao = True
            extrato += f"\n{transacao['tipo']}:\tR$ {transacao['valor']:.2f}\ntransação realizada às {transacao['data']}\n"
    if not existe_transacao:
           extrato = "Não foram realizadas movimentações."
    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")

@log_transacao
def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n Já existe cliente com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)  # Criando uma instância de PessoaFisica

    clientes.append(cliente)  # Adicionando o cliente à lista de clientes

    print(f"\nCliente criado com sucesso!")

@log_transacao
def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado, fluxo de criação de conta encerrado!")
        return
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)  # Criando uma nova conta corrente associada ao cliente
    contas.append(conta)  # Adicionando a nova conta à lista de contas
    cliente.contas.append(conta)  # Associando a nova conta ao cliente

    print(f"\n Conta criada com sucesso!")

@log_transacao
def listar_contas(contas):
    for conta in ContasIterador(contas):
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def main():
    clientes = []  # Lista vazia de clientes
    contas = []  # Lista vazia das contas dos clientes

    while True:
        opcao = menu()

        if opcao == "D":
            depositar(clientes)  

        elif opcao == "S":
            sacar(clientes) 

        elif opcao == "E":
            exibir_extrato(clientes)

        elif opcao == "NU":
            criar_cliente(clientes)

        elif opcao == "NC":
            numero_conta = len(contas) + 1  # Número da conta incremental
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "LC":
            listar_contas(contas)

        elif opcao == "F":
            break 

        else:
            print("\n Operação inválida, por favor selecione novamente a operação desejada.")

main()




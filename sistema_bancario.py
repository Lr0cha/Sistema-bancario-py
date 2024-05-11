import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

#cores do print
VERMELHO = "\033[31m" 
COR_PADRAO = "\033[0m" 
VERDE = "\033[32m"

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
            print(f"\n{VERMELHO} Operação falhou! Você não tem saldo suficiente. {COR_PADRAO}")

        elif valor > 0:
            self._saldo -= valor
            print(f"\n{VERDE} Saque realizado com sucesso! {COR_PADRAO}")
            return True

        else:
            print(f"\n{VERMELHO} Operação falhou! O valor informado é inválido. {COR_PADRAO}")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"\n{VERDE} Depósito realizado com sucesso! {COR_PADRAO}")
        else:
            print(f"\n{VERMELHO} Operação falhou! O valor informado é inválido. {COR_PADRAO}")
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
            print(f"\n{VERMELHO} Operação falhou! O valor do saque excede o limite. {COR_PADRAO}")

        elif excedeu_saques:
            print(f"\n{VERMELHO} Operação falhou! Número máximo de saques excedido. {COR_PADRAO}")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            {VERDE}Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}{COR_PADRAO}
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
                "data": datetime.now().strftime("%d-%m-%Y %H:%M"),
            }
        )


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


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print(f"\n{VERMELHO} Cliente não possui conta! @@@{COR_PADRAO}")
        return

    return cliente.contas[0] #acessa a primeira conta do cliente encontrada


def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print(f"\n{VERMELHO} Cliente não encontrado! {COR_PADRAO}")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)  # Criando uma instância de transação de depósito

    conta = recuperar_conta_cliente(cliente)  # Recuperando a conta associada ao cliente
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)  # Realizando a transação de depósito


def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print(f"\n{VERMELHO} Cliente não encontrado! {VERDE}")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)  # Criando uma instância de transação de saque

    conta = recuperar_conta_cliente(cliente)  # Recuperando a conta associada ao cliente
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)  # Realizando a transação de saque


def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print(f"\n{VERMELHO} Cliente não encontrado!{COR_PADRAO}")
        return

    conta = recuperar_conta_cliente(cliente)  # Recuperando a conta associada ao cliente
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"{VERDE}\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}{COR_PADRAO}")
    print("==========================================")


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print(f"\n{VERMELHO} Já existe cliente com esse CPF! {COR_PADRAO}")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)  # Criando uma instância de PessoaFisica

    clientes.append(cliente)  # Adicionando o cliente à lista de clientes

    print(f"\n{VERDE} Cliente criado com sucesso! {COR_PADRAO}")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print(f"\n{VERMELHO} Cliente não encontrado, fluxo de criação de conta encerrado! {COR_PADRAO}")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)  # Criando uma nova conta corrente associada ao cliente
    contas.append(conta)  # Adicionando a nova conta à lista de contas
    cliente.contas.append(conta)  # Associando a nova conta ao cliente

    print(f"\n{VERDE} Conta criada com sucesso! {COR_PADRAO}")


def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def main():
    clientes = []  # Lista vazia de clientes
    contas = []  # Lista vazia das contas dos clientes

    while True:
        opcao = menu()

        if opcao == "D":
            depositar(clientes)  # Função para depositar dinheiro

        elif opcao == "S":
            sacar(clientes)  # Função para sacar dinheiro

        elif opcao == "E":
            exibir_extrato(clientes)  # Função para exibir o extrato da conta

        elif opcao == "NU":
            criar_cliente(clientes)  # Função para criar um novo cliente

        elif opcao == "NC":
            numero_conta = len(contas) + 1  # Número da conta incremental
            criar_conta(numero_conta, clientes, contas)  # Função para criar uma nova conta

        elif opcao == "LC":
            listar_contas(contas)  # Função para listar todas as contas

        elif opcao == "F":
            break

        else:
            print(f"\n{VERMELHO} Operação inválida, por favor selecione novamente a operação desejada. {COR_PADRAO}")


main()




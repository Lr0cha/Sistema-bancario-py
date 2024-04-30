import textwrap

#menu principal
def menu():
    menu_banco = '''
    --------------------------------------------------
    [D]\tDepositar
    [S]\tSacar
    [E]\tExtrato
    [U]\tNovo usuário
    [C]\tCriar conta
    [L]\tListar contas
    [F]\tFinalizar\n
    Digite uma das letras para operar sua conta:'''
    return input(textwrap.dedent(menu_banco)) #retornar opção digitada

#listas vazias
contas = []
usuarios = []

#cores do print
VERMELHO = "\033[31m" 
COR_PADRAO = "\033[0m" 
VERDE = "\033[32m"

def validar_usuario(cpf):
    for usuario in usuarios:
        if usuario["cpf"] == cpf: #se já existir o usuario no sistema
            return True
    else:
        return False
            
    
def criar_usuario():
    cpf = input("Digite o número do seu CPF[Somente os números]: ")
    existe_cpf = validar_usuario(cpf)
    if existe_cpf:
        print("CPF digitado já existe no sistema.")
    else:
        nome = input("Digite seu nome completo:")
        data_nasc = input("Digite sua data de nascimento[dd-mm-aaaa]:")
        endereco = input ("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
        usuarios.append({"cpf" : cpf, "nome" : nome,  "data_nasc" : data_nasc, "endereco" : endereco })
        print(f"{VERDE}Usuário cadastrado com sucesso.{COR_PADRAO}")

def nome_usuario(cpf):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario["nome"]

def criar_conta(*, agencia, nr_conta):
    cpf = input("Digite o CPF que será vinculado com a conta[Somente os números]:")
    existe_cpf = validar_usuario(cpf)
    if existe_cpf:
        nome = nome_usuario(cpf)
        contas.append({"agencia" : agencia, "numero_conta" : nr_conta, "usuario" : nome})
        print(f"{VERDE}Conta cadastrada com sucesso.{COR_PADRAO}")
        return nr_conta + 1
    else:
        print(f"{VERMELHO}Não é possível criar uma conta sem um já cpf cadastrado!{COR_PADRAO}")
        return nr_conta

def listar_contas():
    if contas == []:
        print(f"{VERMELHO}Nenhuma conta cadastrada no sistema{COR_PADRAO}")
        return
    print("\t----------CONTAS CADASTRADAS----------")
    for conta in contas:
        print(f"Agência:\t {conta["agencia"]}")
        print(f"C/C:\t\t {conta["numero_conta"]}")
        print(f"Agência:\t {conta["usuario"]}")
        print("-" *50)
    

def depositar(saldo, valor, extrato,/): 
    if valor > 0.0:
        saldo += valor 
        extrato += f"-Deposito efetuado: R${valor}\n" #Agregado para se apresentar no extrato
        print(f"{VERDE}Depósito de R${valor} efetuado com sucesso.{COR_PADRAO}")
    else:
        print(f"{VERMELHO}Não é possível depositar valores negativos!{COR_PADRAO}")
    return saldo , extrato

def sacar_conta(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if valor > saldo:
        print(f"{VERMELHO}Não há saldo suficiente na conta\nTotal disponível: {saldo:.2f}{COR_PADRAO}")
    elif valor > limite:
        print(f"{VERMELHO}Limite de R$500.00 por saque ultrapassado, tente novamente.{COR_PADRAO}")
    elif numero_saques >= limite_saques:
        print(f"{VERMELHO}Número máximo de saques diários já atingido!{COR_PADRAO}")
    elif valor > 0.0:
        print(f"{VERDE}Saque de R${valor} realizado com sucesso.{COR_PADRAO}")
        numero_saques += 1 #Incrementar 1 para usar no controle de saques diários disponíveis
        extrato += f"-Saque efetuado: R${valor}\n"
        saldo -= valor #debitar o dinheiro da conta 
    else: 
        print(f"{VERMELHO}Por favor, insira um valor maior que zero para sacar da conta.{COR_PADRAO}")
    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    mensagem = ""
    mensagem += (extrato if extrato else "Não houve movimentação na conta.")
    mensagem += f"\nSaldo atual da conta: {saldo:.2f}"
    return mensagem

def main():
    saldo = 0.0
    LIMITE = 500
    LIMITE_SAQUES = 3
    AGENCIA="0001"
    extrato = ""
    numero_conta = 1
    numero_saques = 0
    while True:
        op = menu()
        if op.upper() == "D":
            print("\t\tDepósito:")           
            valor = float(input("Quanto você deseja depositar:"))
            saldo,extrato = depositar(saldo,valor,extrato)
        elif op.upper() == "S":
            qtd_saques = LIMITE_SAQUES - numero_saques #Saques diários disponíveis
            print("\t\tSaque:")
            print(f"Quantidade de saques disponíveis {qtd_saques}\n")
            saque = float(input("Quanto você deseja retirar(Máx. de R$500 por saque)"))
            saldo, extrato, numero_saques = sacar_conta(saldo = saldo , valor = saque, limite = LIMITE,limite_saques = LIMITE_SAQUES, 
                                        numero_saques=numero_saques, extrato = extrato )      
        elif op.upper() == "E":
            print("=============EXTRATO=============")
            mensagem = exibir_extrato(saldo, extrato = extrato)
            print(mensagem)
            print("=================================")
        elif op.upper() == "U":
            criar_usuario()
        elif op.upper() == "C": 
            numero_conta = criar_conta(agencia = AGENCIA, nr_conta = numero_conta)
        elif op.upper() == "L":
            listar_contas()
        elif op.upper() == "F":
            break
        else:
            print(f"{VERMELHO}Operação inválida, por favor selecione novamente a operação desejada.{COR_PADRAO}")
        input("Pressione qualquer TECLA para continuar...")

main()




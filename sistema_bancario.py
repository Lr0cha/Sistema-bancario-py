menu = '''




[D]epositar
[S]acar
[E]xtrato
[F]inalizar\n
Digite uma das letras para operar sua conta:'''


saldo = 0.0
LIMITE = 500
LIMITE_SAQUES = 3
extrato = ""
numero_saques = 0
while True:
    print(menu)
    op = input()
    if op.upper() == "D":
        print("\t\tDepósito:")
        while True:           
            valor = float(input("Quanto você deseja depositar:"))
            if valor > 0.0:
                saldo += valor
                extrato += f"- Depósito efetuado: R${saldo:.2f}\n"
                break
            else:
                print("Valor de depósito deve ser positivo. Por favor, tente novamente.")
    elif op.upper() == "S":
        qtd_saques = LIMITE_SAQUES - numero_saques
        print("\t\tSaque:")
        print(f"Quantidade de saques disponíveis {qtd_saques}\n")
        saque = float(input("Quanto você deseja retirar(Máx. de R$500 por saque)"))
        
        if saque > saldo:
            print(f"Não há saldo suficiente\n Total disponível: {saldo:.2f}")
        elif saque > LIMITE:
            print("Limite de R$500.00 por saldo ultrapassado, tente novamente.")
        elif numero_saques >= LIMITE_SAQUES:
            print("Número de saques diários já atingido!")
        elif saque > 0.0:
            numero_saques += 1
            extrato += f"- Saque efetuado: R${saque}\n"
            saldo -= saque
        else: 
            print("Por favor, insira um valor maior que zero para sacar da conta.")
    elif op.upper() == "E":
        print("==========EXTRATO==========")
        print(extrato if extrato else "Nenhuma transação efetuada.")
        print(f"Total da conta: {saldo:.2f}")
        print("===========================")
    elif op.upper() == "F":
        break
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")




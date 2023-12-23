from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime

class Transacao(ABC):
    def __init__(self, valor):
        self.valor = valor

    @abstractmethod
    def efetuar(self, conta):
        pass

class Deposito(Transacao):
    def efetuar(self, conta):
        if self.valor > 0:
            conta.saldo += self.valor
            conta.historico.adicionar_transacao(f"Depósito: R$ {self.valor:.2f}")
        else:
            print("Valor inválido para depósito")

class Saque(Transacao):
    def efetuar(self, conta):
        if self.valor <= 0:
            print("Valor inválido para saque")
        elif conta.saldo < self.valor:
            print("Saldo insuficiente na conta")
        elif self.valor > conta.limite_valor_saque:
            print(f"Valor do saque ultrapassa o limite diário de R$ {conta.limite_valor_saque:.2f}")
        elif conta.saques >= conta.limite_quantidade_saque:
            print(f"Limite de saques diários atingido: {conta.limite_quantidade_saque}")
        else:
            conta.saldo -= self.valor
            conta.historico.adicionar_transacao(f"Saque: R$ {self.valor:.2f}")
            conta.saques += 1

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

    def __str__(self):
        return "\n".join(self.transacoes)

class ContaBancaria:
    def __init__(self):
        self.limite_valor_saque = 500.0
        self.limite_quantidade_saque = 3
        self.saldo = 0.0
        self.saques = 0
        self.historico = Historico()

    def __str__(self):
        return f"{self.historico}\nSaldo: R$ {self.saldo:.2f}"

    def depositar(self, valor):
        Deposito(valor).efetuar(self)

    def sacar(self, valor):
        Saque(valor).efetuar(self)


class Cliente:
    def __init__(self, nome, cpf, endereco, data_de_nascimento):
        self.nome = nome
        self.cpf = cpf
        self.endereco = endereco
        self.data_de_nascimento = data_de_nascimento
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        if conta in self.contas:
            transacao.efetuar(conta)
        else:
            print("Conta não encontrada")

class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, endereco, data_de_nascimento):
        super().__init__(nome, cpf, endereco)
        self.data_de_nascimento = data_de_nascimento

class PessoaJuridica(Cliente):
    def __init__(self, nome, cpf, endereco, data_de_nascimento):
        super().__init__(nome, cpf, endereco)
        self.data_de_nascimento = data_de_nascimento


class Conta:
    def __init__(self, saldo, numero, agencia, cliente, historico):
        self.saldo = saldo
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = historico

    @classmethod
    def nova_conta(cls, saldo, numero, agencia, cliente):
        historico = Historico()
        return cls(saldo, numero, agencia, cliente, historico)

    def depositar(self, valor):
        Deposito(valor).efetuar(self)

    def sacar(self, valor):
        Saque(valor).efetuar(self)

class ContaCorrente(Conta):
    def __init__(self, saldo , numero , agencia , cliente , historico , limite , limite_de_saque):
        super().__init__(saldo , numero , agencia , cliente , historico)
        self.limite = limite
        self.limite_de_saque = limite_de_saque

class ContaPoupanca(Conta):
    def __init__(self, saldo , numero , agencia , cliente , historico , limite , limite_saque):
        super().__init__(saldo , numero , agencia , cliente , historico)
        self.limite = limite
        self.limite_saque = limite_saque

class ContaPJ(Conta):
    def __init__(self, saldo, numero , agencia , cliente , historico , cnpj , limite , limite_saque):
        super().__init__(saldo , numero , agencia , cliente , historico)
        self.cnpj = cnpj
        self.limite = limite
        self.limite_saque = limite_saque





def cadastrar_cliente():
    nome = str (input("Digite o nome do cliente: "))
    cpf = str(input("Digite o CPF do cliente: "))
    endereco = str(input("Digite o endereco do cliente: "))
    data_de_nascimento = str(input("Digite a data de nascimento do cliente: "))
    return Cliente(nome, cpf, endereco, data_de_nascimento)

def cadastrar_conta():
    cliente = cadastrar_cliente()
    tipo_conta = input("Digite o tipo de conta (C para Conta Corrente, P para Conta Poupança, J para Conta PJ): ")
    if tipo_conta.upper() == "C":
        return ContaCorrente(cliente)
    elif tipo_conta.upper() == "P":
        return ContaPoupanca(cliente)
    elif tipo_conta.upper() == "J":
        return ContaPJ(cliente)
    else:
        print("Tipo de conta inválido")
        return None

menu = '''  
[1] Depositar  
[2] Sacar  
[3] Histórico
[4] Cadastrar Conta 
[5] Minha Conta
[0] Sair  
=> '''
conta = None

while True:
    opcao = input(menu)
    if opcao == '1':
        conta.depositar()
    elif opcao == '2':
        conta.sacar()
    elif opcao == '3':
        print(Historico)
    elif opcao == '4':
        conta = cadastrar_conta()
        print(f"Seja bem-vindo(a), {conta.cliente.nome}!")
    elif opcao == '5':
        if conta is None:
            print("Nenhuma conta cadastrada")
        else:
            print(conta.cliente.nome, conta)
    elif opcao == '0':
        break
    else:
        print('opcao invalida, tente novamente')


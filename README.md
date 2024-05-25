# Sistema-Bancario-py
Este é um programa desenvolvido de forma didática para auxiliar na aprendizagem dos conceitos de Python. Estou continuamente atualizando este projeto à medida que adquiro novas habilidades durante o curso de Python AI Backend Developer oferecido pela DIO.

# Conceitos Iniciais:

* Funções: O programa inicial estava estruturado em funções para realizar operações bancárias como depositar, sacar, exibir extrato, criar novo usuário, criar conta e listar contas. Essas funções eram chamadas a partir de um menu principal.
  
* Cadastro de Usuários e Contas: Permiti a criação de clientes e contas(que são armazenadas em listas e dicionários), porém não estam vinculadas as operações do sistema.

* Exibição de Extrato: O programa permitia visualizar o extrato da conta, mostrando as transações realizadas e o saldo atual.

# Novas Implementações:

* Orientação a Objetos: A reformulação do programa introduziu uma abordagem mais orientada a objetos, com classes como Cliente, Conta, PessoaFisica, entre outras, para representar entidades do sistema bancário. Isso proporciona uma estrutura mais organizada e modular para o código.

* Cadastro de Usuários e Contas: O sistema agora permiti cadastrar novos usuários associados a um CPF e criar contas vinculadas a esses usuários e suas operações realizadas.

* Histórico de Transações: Foi adicionada a funcionalidade de registrar e exibir um histórico de transações para cada conta bancária, permitindo um acompanhamento mais detalhado das operações realizadas.

* Logging de Transações: Implementou-se um sistema de logging para registrar as operações realizadas pelo usuário, ajudando na auditoria e depuração do sistema.

* Iteração sobre Contas: Criou-se uma classe ContasIterador para iterar sobre as contas bancárias cadastradas no sistema, facilitando a exibição de informações e listagem de contas.

* Melhorias na Interface do Usuário: Pequenas melhorias na apresentação das informações ao usuário foram feitas, como mensagens de confirmação, correção de formatação e organização do menu.

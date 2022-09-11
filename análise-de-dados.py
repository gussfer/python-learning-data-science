# Exercicio prático de Análise de dados: Dados de Telecomunicações
  # Bibliotecas: Pandas (interação com os dados) ; Plotly (visualização dos dados)
'''
Você trabalha em uma empresa de telecom e tem clientes de vários serviços diferentes, 
entre os principais: internet e telefone. O problema é que, analisando o histórico dos 
clientes dos últimos anos, você percebeu que a empresa está com 'Churn'  
de mais de 26% dos clientes. Isso representa uma perda de milhões para a empresa.

O que a empresa precisa fazer para resolver isso?
  - diminuir as taxas de desistência: identificar quem são os envolvidos nos chrun e atuar a partir disso

Base de Dados: https://drive.google.com/drive/folders/1T7D0BlWkNuy_MDpUHuBG44kT80EmRYIs?usp=sharing 
Link Original do Kaggle: https://www.kaggle.com/radmirzosimov/telecom-users-dataset 
'''
# BASE DE DADOS: historico dos clientes dos últimos ANOS

# Churn: cancelamento de pacotes 
'''
ESTRUTURA LÓGICA

• PASSO 1 : ACESSAR O HISTÓRICO DOS CLIENTES
• PASSO 2 : TRATAR OS DADOS
• PASSO 3 : ANÁLISE GERAL
• PASSO 4 : ANÁLISE ESPECÍFICA  
'''

## PASSO 1 : ACESSAR O HISTÓRICO DOS CLIENTES

import pandas as pd

clientes = pd.read_csv('telecom_users.csv')
display(clientes.head())
clientes.info()  

## PASSO 2 : TRATAR OS DADOS

# - Deletar colunas inuteis
# axis = 0 --> linha
# axis = 1 --> coluna

clientesTrat = clientes.drop(['Unnamed: 0', 'Codigo', 'IDCliente', 'Aposentado'], axis = 1)  # metodo .drop() de deleção
clientesTrat.info()  

# - Valores reconhecidos de forma errada: corrigir valores de colunas alvo

clientesTrat['TotalGasto'] = pd.to_numeric(clientesTrat['TotalGasto'], errors= "coerce") # corrigir coluna 'TotalGasto'
clientesTrat.info()

# - Tratar valores vazios: excluir linhas com valores vazios, nesse caso

clientesTrat = clientesTrat.dropna(how="all", axis=1) # excluir colunas vazias
clientesTrat = clientesTrat.dropna(how="any", axis=0)  # excluir linhas vazias
print(clientesTrat.info())

## PASSO 3 : ANÁLISE GERAL

# coluna alvo: Churn - contar valores 'sim' e 'nao'

print(clientesTrat['Churn'].value_counts()) # metodo ..value_counts() contam valores diferentes dentro de uma coluna alvo
print(clientesTrat['Churn'].value_counts(normalize=True).map("{:.1%}".format))

print("-------------------------------")

print(clientesTrat['Dependentes'].value_counts())

print("-------------------------------")

print(clientesTrat['FormaPagamento'].value_counts())

# PASSO 4 : ANÁLISE ESPECÍFICA  

# - encontrar padrões: relacionar cancelamentos (Churn), com outras colunas para isso
# - analisar gráficos com diferenças discrepantes entre pessoas que cancelam e não cancelam (análise qualitativa)

import plotly.express as px

for coluna in clientesTrat.columns:
  graficos = px.histogram(clientesTrat, x= coluna, color='Churn')
  graficos.show()
  

'''
• Quem é solteiro e sem dependentes, tende a cancelar mais do que os com dependentes

Proposta: melhorar planos individuais;
• Clientes novos tendem a cancelar mais que os antigos

Proposta: criar bonus de fidelidade; produtos extra no primeiro ano
• Clientes com fibra ótica cancelam mais que os outros

Proposta: investigar a fundo sobre problemas da fibra e resolver
• Clientes sem serviço de segurança, backup e suporte cancelam mais que os outros

Proposta: investigar a fundo sobre problemas da segurança, backup e suporte e resolver
• Clientes com contrato mensal tendem a cancelar mais que os outros

Proposta: oferecer promoções de adesão durante o primeiro ano
• Clientes que pagam via boleto tendem a cancelar mais que os outros

Proposta: investigar a fundo sobre problemas com optantes por boleto e resolver
• Clientes com gasto total menores tendem a cancelar mais

Proposta: criar plano de fidelidade
'''

import os
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import repository_gestao_impressoras as repo

load_dotenv()

def getConnection():
    # Conecta ao banco de dados Oracle
    user_name = os.getenv('user_name')
    password = os.getenv('password')
    host = os.getenv('host')
    port = os.getenv('port')
    service_name = os.getenv('service_name')
    
    # Verifica se todos os valores necessários foram fornecidos
    if None in [user_name, password, host, port, service_name]:
        print("Erro: Algum valor necessário está ausente.")
        return None
    
    dsn = f"oracle+oracledb://{user_name}:{password}@{host}:{port}/{service_name}"
    return create_engine(dsn)

# # Função para executar a consulta
# def query_impressoras():
#     engine = getConnection()
    
#     # Verifica se a conexão foi estabelecida com sucesso
#     if engine is None:
#         print("Erro: Não foi possível estabelecer conexão com o banco de dados.")
#         return None
    
#     # Consulta SQL para selecionar todas as colunas da tabela 'impressoras'
#     query = "SELECT * FROM impressora"
    
#     # Executa a consulta e carrega os resultados em um DataFrame
#     df = pd.read_sql(query, engine)
    
#     # Retorna o DataFrame com os resultados da consulta
#     return df

# Executa a consulta e imprime os resultados


# Executa a consulta e imprime os resultados
impressoras = repo.query_impressoras()
for impressora in impressoras:
    print(impressora)
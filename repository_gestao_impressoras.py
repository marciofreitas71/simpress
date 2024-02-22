from sqlalchemy import create_engine, Table, Column, Integer, MetaData, DateTime, String
from sqlalchemy.sql import select
from sqlalchemy import select
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

def getConnection():
    # Conecta ao banco de dados Oracle
    user_name = os.getenv('user_name')
    password = os.getenv('password')
    host = os.getenv('host')
    port = os.getenv('port')
    service_name = os.getenv('service_name')
    dsn = f"oracle+oracledb://{user_name}:{password}@{host}:{port}/{service_name}"
    return create_engine(dsn)

def cadastrarDadosImpressoras(dataframe):
    
    engine = getConnection()

    # Escreve os dados no banco de dados Oracle
    with engine.connect() as conn:
        table_name = 'impressora'
        dataframe.to_sql(table_name, con=engine, index=False, if_exists='append')

    # Fecha a conexão com o banco de dados
    engine.dispose()

def cadastrarContagemImpressoras(dataframe):
    
    engine = getConnection()

    # Escreve os dados no banco de dados Oracle
    with engine.connect() as conn:
        table_name = 'contagem_impressora'
        dataframe.to_sql(table_name, con=engine, index=False, if_exists='append')

    # Fecha a conexão com o banco de dados
    engine.dispose()

def recuperarDadosImpressoras(dataframe):
    engine = getConnection()
    
    # cria objeto Metadata
    metadata = MetaData()

    # associa objeto de conexão ao Metadata
    metadata.bind = engine

    table = Table(
        'impressora',
        metadata,
        autoload_with=engine
        )
    
    # criar uma expressão SQL dinâmica com a condição de atualização
    unique_values_list = list(dataframe['SERIALNUMBER'].unique())
    query = select(table.columns['id'], table.columns['serialnumber']).where(table.columns['serialnumber'].in_(unique_values_list))
    resultdf = pd.DataFrame()

    # Executa a consulta
    with engine.connect() as conn:
        conn.begin()
        try:
            result = conn.execute(query)
            #Constroi DataFrame com os resultados da consulta
            sql_data = pd.DataFrame(result.fetchall(), columns=['IMPRESSORA_ID', 'SERIALNUMBER'])
            resultdf = pd.merge(dataframe, sql_data, how='right', on='SERIALNUMBER')
            #print(resultdf)
            #trans.commit()
        except:
            #trans.rollback()
            raise
        finally:
            conn.close()

    # Fecha a conexão com o banco de dados
    engine.dispose()
    # print(sql_data)
    return resultdf

def recuperarDadosLocaisImpressoras():
    engine = getConnection()
    
    # cria objeto Metadata
    metadata = MetaData()

    # associa objeto de conexão ao Metadata
    metadata.bind = engine

    table = Table(
        'contagem_impressora',
        metadata,
        autoload_with=engine
        )
    
    # criar uma expressão SQL dinâmica com a condição de atualização
    query = select(
    table.columns['id'],
    table.columns['impressora_id'], 
    table.columns['contador_pb'],
    table.columns['contador_cor'],
    table.columns['contador_total'],
    table.columns['data_leitura'],
    table.columns['created_at']
    )

    resultdf = pd.DataFrame()

    # Executa a consulta
    with engine.connect() as conn:
        conn.begin()
        try:
            result = conn.execute(query)
            # Constroi DataFrame com os resultados da consulta
            sql_data = pd.DataFrame(result.fetchall(), columns=result.keys())
            # Encontra a data mais atual na coluna 'data_leitura'
            data_mais_atual = pd.to_datetime(sql_data['data_leitura']).max()
            # Filtra os registros com a mesma data mais atual
            resultado = sql_data[sql_data['data_leitura'].dt.strftime('%Y-%m-%d') == data_mais_atual.strftime('%Y-%m-%d')]

        except:
            raise
        finally:
            conn.close()

    # Fecha a conexão com o banco de dados
    engine.dispose()
    return resultado

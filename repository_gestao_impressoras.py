from sqlalchemy import create_engine, Table, Column, Integer, MetaData, DateTime, String
from sqlalchemy.sql import select
import pandas as pd


def getConnection():
    # Conecta ao banco de dados Oracle
    username = 'GESTAO_IMPRESSAO'
    password = 'je8u_asdfa'
    host = 'ba1linha'
    port = '1523'
    service_name = 'dese'
    dsn = f"oracle+oracledb://{username}:{password}@{host}:{port}/{service_name}"
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
            resultdf = pd.merge(dataframe, sql_data, how='inner', on='SERIALNUMBER')
            #print(resultdf)
            #trans.commit()
        except:
            #trans.rollback()
            raise
        finally:
            conn.close()

    # Fecha a conexão com o banco de dados
    engine.dispose()
    return resultdf

def atualizarStatusLitigiosidade(dataAtual):

    engine = getConnection()
    
    # cria objeto Metadata
    metadata = MetaData()

    # associa objeto de conexão ao Metadata
    metadata.bind = engine

    table_name = Table(
        'atena_litigiosidade',
        metadata, 
        Column("created_at", DateTime),
        Column("status", Integer),
        Column("variavel", String))

    valStatus = 0

    print(dataAtual)

    # Cria a expressão SQL para atualização
    #upd = text(f"UPDATE {table_name} SET status = 0 WHERE created_at < :data_limite")
    # criar uma expressão SQL dinâmica com a condição de atualização
    stmt = table_name.update().where(table_name.c.created_at < dataAtual).values(status=valStatus)
    
    # Executa a atualização
    with engine.connect() as conn:
        trans = conn.begin()
        try:
            result = conn.execute(stmt)
            #print(result.rowcount)
            trans.commit()
        except:
            trans.rollback()
            raise
        finally:
            conn.close()

    # Fecha a conexão com o banco de dados
    engine.dispose()

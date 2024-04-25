from sqlalchemy import create_engine, Table, Column, Integer, MetaData, DateTime, String
from sqlalchemy.sql import select
from sqlalchemy import select
from dotenv import load_dotenv
from datetime import datetime
import config as config
import pandas as pd
from io import StringIO
import logging
import zeep
import re
import os



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

def recuperarDadosImpressoras():
    engine = getConnection()
    
    # Cria objeto Metadata
    metadata = MetaData()

    # Associa objeto de conexão ao Metadata
    metadata.bind = engine

    table = Table(
        'impressora',
        metadata,
        autoload_with=engine
    )

    # Cria uma expressão SQL dinâmica para selecionar todas as colunas
    query = select(
        table.columns['id'],
        table.columns['printerdeviceid'], 
        table.columns['printerbrandname'],
        table.columns['printermodelname'],
        table.columns['serialnumber'],
        table.columns['created_at'],
        table.columns['status']
    )

    resultdf = pd.DataFrame()

    # Executa a consulta
    with engine.connect() as conn:
        conn.begin()
        try:
            result = conn.execute(query)
            # Constroi DataFrame com os resultados da consulta
            resultdf = pd.DataFrame(result.fetchall(), columns=result.keys())
            resultdf = resultdf.sort_values(by='printerdeviceid')
        except:
            raise
        finally:
            conn.close()

    # Fecha a conexão com o banco de dados
    engine.dispose()
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

def send_soap_request_and_write_to_csv(wsdl_url, service_method, output_csv, payload):
    # Create a SOAP client using the WSDL URL
    client = zeep.Client(wsdl=wsdl_url)

    # Access the service method and send the request with the payload
    service = client.service
    method_to_call = getattr(service, service_method)
    response = method_to_call(**payload)
    
    # Parse the response string into Python objects
    df = pd.read_json(StringIO(response))
    print(df)
    df.to_csv(output_csv, sep=';', index=False)

def carregar_dados_excel(url, sheet):
    tables = pd.read_excel(url, sheet_name=sheet)
    return tables

def carregar_dados_csv(url):
    tables = pd.read_csv(url, delimiter=';')
    return tables

def insert_printer(input_csv, brand_name):
    df = carregar_dados_csv(input_csv)
    df = df[['PrinterDeviceID', 'BrandName', 'PrinterModelName', 'SerialNumber']]
    df = df[df['BrandName'] == brand_name].sort_values(by=['SerialNumber'])
    df = df.rename(columns={"BrandName" : "PRINTERBRANDNAME"})
    df['created_at'] = datetime.now()
    df['status'] = 1
    df = df.fillna(0)
    df.columns = df.columns.str.upper()
    print(df)

    repo.cadastrarDadosImpressoras(df)

def recuperar_dados_webservice(data):
    
    dateTimeEnd = f"{data} 02:00:00"
    wsdl_url = config.wsdl_url
    service_method = config.service_method
    output_csv = config.output_csv
    payload = config.payload
    timeout = 5   
        
    logging.info("Executando a função recuperar_dados_webservice... ")

    # Atualize o payload com a nova dateTimeEnd
    payload['dateTimeEnd'] = dateTimeEnd

    try:
        # Criar um cliente SOAP usando a URL do WSDL com timeout
        client = zeep.Client(wsdl=wsdl_url, transport=zeep.Transport(timeout=timeout))
        logging.info("Criado um cliente SOAP usando a URL do WSDL com timeout")

        # Acessar o método do serviço e enviar a solicitação com os dados
        service = client.service
        method_to_call = getattr(service, service_method)
        response = method_to_call(**payload)
        logging.info("Acessar o método do serviço e enviar a solicitação com os dados")

        # Analisar a string de resposta em objetos Python
        df = pd.read_json(StringIO(response))
        # Filtrando para que apenas as impressoras HP sejam mostradas
        return df.loc[df['BrandName'] == 'HP']
    except zeep.exceptions.Fault as e:
        logging.error(f"Erro durante a execução da função: {str(e)}")
        # Você pode decidir levantar a exceção novamente ou retornar um valor padrão, dependendo do caso.
        raise
    except zeep.exceptions.TransportError as e:
        logging.error(f"Erro de transporte durante a execução da função: {str(e)}")
        # Trate o erro de transporte conforme necessário
        raise
   
    # df3 = pd.merge(df_remoto, df_local, on='SERIALNUMBER', how='outer')
def inserir_contagem_impressoras(df_remoto):
    df_remoto = df_remoto.rename(columns={"ReferenceMono" : "CONTADOR_PB", "ReferenceColor" : "CONTADOR_COR", "DateTimeRead" : "DATA_LEITURA"})
    df_remoto.columns = df_remoto.columns.str.upper()
    df_remoto['CONTADOR_TOTAL'] = df_remoto['CONTADOR_PB'] + df_remoto['CONTADOR_COR']